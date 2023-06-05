from enum import Enum


class WeekdayEn(Enum):
    mon = 0
    tue = 1
    wed = 2
    thu = 3
    fri = 4
    sat = 5
    sun = 6


class WeekdayJa(Enum):
    月 = "月"
    火 = "火"
    水 = "水"
    木 = "木"
    金 = "金"
    土 = "土"
    日 = "日"

    def toInt(self):
        return "月火水木金土日".index(self.value)
