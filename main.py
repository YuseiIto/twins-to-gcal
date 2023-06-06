# coding: utf-8
import sys
from catalog import Catalog
from icalendar import Calendar as iCalendar, Event  # type: ignore
from univ_calendar import Calendar
from subscription import Subscription

if len(sys.argv) < 4:
    print(
        """[Error] No input file.\n\n
Usage: main.py <catalog> <subscription> <calendar>\n
catalog: An exported CSV file from the kdb.
 It must be converted to UTF-8 first.\n
subscription: Cource codes to attend.
Typically an exported file from TWINS.)"""
    )
    sys.exit(1)

catalog = Catalog(sys.argv[1])
calendar = Calendar(sys.argv[3])
subscription = Subscription(sys.argv[2], catalog)

cal = iCalendar()
cal.add("prodid", "-//yuseiito//kdb2ics//JA")
cal.add("version", "2.0")
cal.add("calscale", "GREGORIAN")
cal.add("method", "REQUEST")

for c in subscription.courses_iter():
    print(f"Processing {c.name} ({c.code}).")
    for m in c.modules:
        for d, periods in c.classDays:
            firstDay = calendar.computeFirstDay(m, d)
            lastDay = calendar.computeLastDay(m, d)
            excludedDays = calendar.computeExcludes(m, d)
            includedDays = calendar.getOverrides(m, d)

            for unit in periods:
                event = Event()
                event.add("summary", c.name)
                start, end = unit.toTimeDelta()
                event.add("dtstart", firstDay + start)
                event.add("dtend", firstDay + end)
                event.add("rrule", {"freq": "weekly", "until": lastDay})

                # When DTSTART is with time, EXDATE must be with time.
                # https://stackoverflow.com/questions/25170070/google-calendar-api-rrule-and-exdate
                for ex in excludedDays:
                    event.add("exdate", ex + start)
                for inc in includedDays:
                    event.add("rdate", inc + start)
                event.add("description", c.code)
                cal.add_component(event)

with open("kdb.ics", "wb") as f:
    f.write(cal.to_ical())

