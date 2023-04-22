# coding: utf-8
import sys
from courses import readCsvFromFile,readCourseCodes,parseCalendar,expandModules,parseClassDays

from class_days import computeFirstDay,computeLastDay,computeExcludes,getOverrides,JP_WEEKDAY,EN_WEEKDAY

from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta

def periodToTime(period:int)->timedelta:
    match int(period):
        case 1:
            return timedelta(hours=8,minutes=40)
        case 2:
            return timedelta(hours=10,minutes=10)
        case 3:
            return timedelta(hours=12,minutes=15)
        case 4:
            return timedelta(hours=13,minutes=45)
        case 5:
            return timedelta(hours=15,minutes=15)
        case 6:
            return timedelta(hours=16,minutes=45)
        case _:
            raise ValueError(f"Invalid period: {period}")

    
if len(sys.argv) < 4:
    print("[Error] No input file.\n\nUsage: main.py <catalog> <subscription> <calendar>\n catalog: An exported CSV file from the kdb. It must be converted to UTF-8 first.\n subscription: Cource codes to attend. Typically an exported file from TWINS.")
    sys.exit(1)

catalog= readCsvFromFile(sys.argv[1])
subscription = readCourseCodes(sys.argv[2])
calendar = parseCalendar(sys.argv[3])
courses = list(filter(lambda row: row["科目番号"] in subscription,catalog))

cal = Calendar()
cal.add('prodid', '-//yuseiito//kdb2ics//JA')
cal.add('version', '2.0')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'REQUEST')

for c in courses:
    code = c['科目番号']
    name = c["科目名"]

    print(name)
    ms = expandModules(c['実施学期'])
    for m in ms:
        ds = parseClassDays(c['曜時限'])
        print(f"ds: {ds}")
        for d,periods in enumerate(ds):
            for [pStart,pEnd] in periods:
                firstDay= computeFirstDay(calendar,m,JP_WEEKDAY[d])
                lastDay = computeLastDay(calendar,m,JP_WEEKDAY[d])
                excludedDays = computeExcludes(calendar,m,EN_WEEKDAY[d])
                includedDays = getOverrides(calendar,m,EN_WEEKDAY[d])
            
                length = pEnd - pStart + 1

                event = Event()
                event.add('summary', name)
                t = periodToTime(pStart)
                event.add('dtstart', firstDay+t)
                event.add('dtend', firstDay + t + timedelta(minutes=75)*length + timedelta(minutes=15)*(length-1))
                event.add('rrule', {'freq': 'weekly', 'until': lastDay})
                
                # When DTSTART is with time, EXDATE must be with time.
                # https://stackoverflow.com/questions/25170070/google-calendar-api-rrule-and-exdate
                for ex in excludedDays:
                    event.add('exdate', ex+t)
                for inc in includedDays:
                    event.add('rdate', inc+t)
                event.add('description',code)
                cal.add_component(event)

with open('kdb.ics', 'wb') as f:
    f.write(cal.to_ical())
