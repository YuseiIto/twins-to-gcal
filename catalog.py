from typing import List
from util import readCsvFromFile
from course import Course, RawCourse
from course_code import CourseCode


class Catalog:
    __body: dict[CourseCode, Course] = {}

    def __init__(self, file: str):
        """Initialize a catalog from a CSV file which is exported from kdb.
        Args:
            file (str): A CSV file path.
        """
        rows: List[RawCourse] = readCsvFromFile(file)
        for record in rows:
            tmp = Course(record)
            if tmp is not None:
                self.__body[tmp.code] = tmp

    def __contains__(self, key: CourseCode):
        return key in self.__body.keys()

    def __getitem__(self, key: CourseCode):
        return self.__body[key]

    def __repr__(self):
        return repr(self.__body)
