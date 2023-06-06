from weekday import WeekdayJa
from dataclasses import dataclass
from typing import List, Tuple, Optional
from datetime import timedelta


@dataclass()
class ClassUnit:
    """A single unit of a class.
    The classes on consecutive periods are grouped into a single ClassUnit."""

    start: int
    end: int

    def __periodToTime(self, period: int) -> timedelta:
        match int(period):
            case 1:
                return timedelta(hours=8, minutes=40)
            case 2:
                return timedelta(hours=10, minutes=10)
            case 3:
                return timedelta(hours=12, minutes=15)
            case 4:
                return timedelta(hours=13, minutes=45)
            case 5:
                return timedelta(hours=15, minutes=15)
            case 6:
                return timedelta(hours=16, minutes=45)
            case 7:
                return timedelta(hours=18, minutes=15)
            case 8:
                return timedelta(hours=20, minutes=45)
            case _:
                raise ValueError(f"Invalid period: {period}")

    def isJustBefore(self, i: int):
        return self.end + 1 == i

    def toTimeDelta(self) -> Tuple[timedelta, timedelta]:
        length = self.end - self.start + 1
        start = self.__periodToTime(self.start)
        end = (
            start
            + timedelta(minutes=75) * length
            + timedelta(minutes=15) * (length - 1)
        )

        return (start, end)


WeekdayDict = dict[WeekdayJa, List[ClassUnit]]


class ClassDays:
    __week: WeekdayDict
    __raw: str

    def __init__(self, raw: str):
        """Parse a string like "月1,2" into a list of ClassDay object.
        Args:
            raw(str): A string like "月1,2".
        """
        self.__raw = raw.strip()
        self.__week = {WeekdayJa(weekday): [] for weekday in WeekdayJa}

        if not self.__raw:
            return

        try:
            currentDay: Optional[WeekdayJa] = WeekdayJa(self.__raw[0])
        except ValueError:
            # Ignore "集中" items and similar.
            return

        currentSeq = None
        for c in self.__raw[1:]:
            if c.isdigit() and currentDay is not None:
                if currentSeq is None:
                    currentSeq = ClassUnit(int(c), int(c))
                elif currentSeq.isJustBefore(int(c)):
                    currentSeq.end = int(c)
                else:
                    # End of sequence
                    self.__week[currentDay].append(currentSeq)
                    currentSeq = ClassUnit(int(c), int(c))
            elif c in ",・":
                pass
            else:
                if currentSeq is not None and currentDay is not None:
                    self.__week[currentDay].append(currentSeq)
                currentSeq = None

                try:
                    currentDay = WeekdayJa(c)
                except ValueError:
                    currentDay = None

        if currentSeq is not None and currentDay is not None:
            self.__week[currentDay].append(currentSeq)

    def __iter__(self):
        return self.__week.items().__iter__()

    def __repr__(self):
        return f"From: {self.__raw}. Detecetd Len: {str([(k.value,len(l)) for k,l in self.__week.items()])}"
