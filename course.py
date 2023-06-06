from dataclasses import dataclass
from typing import TypedDict, List
from class_days import ClassDays
from module import expandModules,Module
from course_code import CourseCode

RawCourse = TypedDict(
    "RawCourse",
    {
        "科目番号": str,
        "科目名": str,
        "授業方法": str,
        "実施学期": str,
        "曜時限": str,
        "教室": str,
    },
)


@dataclass(init=False)
class Course:
    code: CourseCode
    name: str
    style: str
    modules: List[Module]
    classDays: ClassDays
    room: str

    def __init__(self, record: RawCourse):
        """Initialize a course object from a raw csv pared dictionary.
        Args:
            file (RawCourse): A dictionary item parsed from a CSV file.
        """
        self.code = CourseCode(record["科目番号"])
        self.name = record["科目名"]
        self.style = record["授業方法"]
        self.modules = expandModules(record["実施学期"])
        self.classDays = ClassDays(record["曜時限"])
        self.room = record["教室"]
