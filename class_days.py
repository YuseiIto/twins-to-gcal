import toml
from datetime import datetime,timedelta

JP_WEEKDAY=['月','火','水','木','金','土','日']
EN_WEEKDAY=['mon','tue','wed','thu','fri','sat','sun']

def parseCalendar(file):
    print(f"Reading {file}...")
    with open(file, "r") as f:
        toml_string = f.read()
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def parseDatetime(src:str):
    return datetime.strptime(src, "%Y/%m/%d")

def getOverrides(calendar:dict,module: str,weekdaySlug: str):
    exceptions = []
    try:
        exceptions = calendar['modules'][module]['overrides'][weekdaySlug]
    except KeyError:
        pass
    
    exceptions = [parseDatetime(d) for d in exceptions]
    return exceptions

def readExcludes(calendar:dict,module: str):
    excludes = []
    try:
        excludes = calendar['modules'][module]['excludes']
    except KeyError:
        pass
    return excludes

def computeExcludes(calendar:dict,module: str,weekdayEn: str):
    moduleObj = calendar['modules'][module]
    excludedDays = [parseDatetime(d) for d in  readExcludes(calendar,module)]
    for weekdaySlug in EN_WEEKDAY:
        if weekdaySlug == weekdayEn:
            continue
        excludedDays.extend(getOverrides(calendar,module,weekdaySlug))
    return excludedDays 

def computeFirstDay(calendar:dict,module: str,weekdayJa: str): 
    moduleObj = calendar['modules'][module]
    base= moduleObj['base'].split('-')
    start = parseDatetime(base[0])
    targetWeekday = JP_WEEKDAY.index(weekdayJa)
    return start + timedelta(days=(targetWeekday-start.weekday())%7)

def computeLastDay(calendar:dict,module:str,weekdayJa:str):
    moduleObj = calendar['modules'][module]
    base= moduleObj['base'].split('-')
    end = parseDatetime(base[1])
    return end
