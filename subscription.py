from typing import List
from course_code import CourseCode
from catalog import Catalog
from course import Course


class Subscription:
    __courses: dict[CourseCode, Course]

    def __init__(self, file: str, catalog: Catalog):
        self.__courses = {}
        with open(file, "r") as f:
            lines: List[str] = f.readlines()

        for record in lines:
            code = CourseCode(record.strip())
            if code in catalog:
                self.__courses[code] = catalog[code]
            else:
                print(f"[WARN] Course {code} is not found in the catalog.")

    def courses_iter(self):
        return self.__courses.values().__iter__()

    def __repr__(self):
        return repr(self.__courses)
