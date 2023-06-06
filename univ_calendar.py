import toml
from typing import TypedDict, Any
from weekday import WeekdayEn, WeekdayJa
from datetime import datetime, timedelta
from module import Module

RawModuleSchedule = TypedDict(
    "RawModuleSchedule",
    {
        "base": str,  # yyyy/mm/dd-yyyy/mm/dd
        "excludes": list[str],  # yyyy/mm/dd
        "overrides": dict[WeekdayEn, list[str]],  # yyyy/mm/dd
    },
)

RawCalendar = TypedDict(
    "RawCalendar",
    {"modules": dict[str, RawModuleSchedule]},
)


def sanitizeModule(module: dict[str, Any]):
    sanitized = {}
    if module["base"] is None:
        raise ValueError("base is not defined")
    sanitized["base"] = module["base"]

    if module["excludes"] is None:
        sanitized["excludes"] = []
    else:
        sanitized["excludes"] = module["excludes"]

    if module["overrides"] is None:
        sanitized["overrides"] = {}
    else:
        sanitized["overrides"] = {
            WeekdayEn(k): v for k, v in module["overrides"].items()
        }

    return sanitized


def sanitizeCalendar(calendar: dict[str, Any]):
    if calendar["modules"] is None:
        raise ValueError("modules is not defined")

    modules = {
        name: sanitizeModule(module) for name, module in calendar["modules"].items()
    }

    return {"modules": modules}


class Calendar:
    __data: RawCalendar

    def __init__(self, file):
        """Initialize a calendar from a TOML file.
        Args:
            file (str): A TOML file path.
        """
        self.file = file
        print(f"Reading {file}...")
        with open(file, "r") as f:
            toml_string = f.read()
        self.__data = sanitizeCalendar(toml.loads(toml_string))

    def __parseDatetime(self, src: str):
        return datetime.strptime(src, "%Y/%m/%d")

    def __readExcludes(self, module: Module):
        excludes = []
        try:
            excludes = [
                self.__parseDatetime(d)
                for d in self.__data["modules"][repr(module)]["excludes"]
            ]
        except KeyError:
            pass
        return excludes

    def computeExcludes(self, module: Module, weekdayEn: str):
        excludedDays = self.__readExcludes(module)
        for d in WeekdayEn:
            if d != weekdayEn:
                continue
            excludedDays.extend(self.getOverrides(module, d))
        return excludedDays

    def getOverrides(self, module: Module, weekdayEn: WeekdayEn):
        overrides = []
        try:
            overrides = self.__data["modules"][repr(module)]["overrides"][weekdayEn]
        except KeyError:
            pass

        overrides = [self.__parseDatetime(d) for d in overrides]
        return overrides

    def computeFirstDay(self, module: Module, weekdayJa: WeekdayJa):
        moduleObj = self.__data["modules"][repr(module)]
        base = moduleObj["base"].split("-")
        start = self.__parseDatetime(base[0])
        targetWeekday = weekdayJa.toInt()
        return start + timedelta(days=(targetWeekday - start.weekday()) % 7)

    def computeLastDay(self, module: Module, weekdayJa: WeekdayJa):
        moduleObj = self.__data["modules"][repr(module)]
        base = moduleObj["base"].split("-")
        end = self.__parseDatetime(base[1])
        return end
