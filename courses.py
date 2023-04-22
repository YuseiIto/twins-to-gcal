import csv
from class_days import parseCalendar,JP_WEEKDAY

def readCsvFromFile(file):
    print(f"Reading {file}...")
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        content = [row for row in reader]
        return content

def readCourseCodes(file):
    print(f"Reading {file}...")
    with open(file, "r") as f:
        reader = csv.reader(f)
        content = [row[0] for row in reader] # Remove quotation marks
    return content

def parseClassDays(periodStr:str):
    currentDay = JP_WEEKDAY.index(periodStr[0])
    currentSeq = [0,0]
    classDays = [[] for _ in range (7)]
    print(f'init {currentDay} {currentSeq}')
    for c in periodStr[1:]:
        if c.isdigit():
            if currentSeq[0] == 0:
                print(f'seq begins {c}')
                currentSeq[0] = int(c)
                currentSeq[1] = int(c)
            elif currentSeq[1] +1 == int(c):
                print(f'seq extend {c}')
                currentSeq[1] = int(c)
            else:
                # End of sequence
                print(f'seq finish {currentSeq}')
                classDays[currentDay].append(currentSeq)
                currentSeq = [0,0]
        elif c== ',':
            pass
        else:
            if currentSeq[0] != 0:
                classDays[currentDay].append(currentSeq)
            currentDay = JP_WEEKDAY.index(c)
            currentSeq = [0,0]

    if currentSeq[0] != 0:
        classDays[currentDay].append(currentSeq)
    return classDays

def expandModules(modulesStr:str):
    modules = []
    currentSemester = modulesStr[0]
    for c in modulesStr[1:]:
        if c in ['春','秋']:
            currentSemester = c
        else:
            modules.append(f"{currentSemester}{c}")
    return modules 

