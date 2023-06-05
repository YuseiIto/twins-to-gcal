from dataclasses import dataclass


@dataclass(frozen=True)
class CourseCode:
    code: str

    def __repr__(self):
        return self.code
