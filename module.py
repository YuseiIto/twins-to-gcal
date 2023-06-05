from enum import Enum
from dataclasses import dataclass


class Semester(Enum):
    Spring = "春"
    Autumn = "秋"


class ModuleName(Enum):
    A = "A"
    B = "B"
    C = "C"


@dataclass(frozen=True)
class Module:
    semester: Semester
    module: ModuleName

    def __repr__(self):
        return f"{self.semester.value}{self.module.value}"


def expandModules(modulesStr: str):
    modules = []
    if not modulesStr:
        return modules

    try:
        currentSemester = Semester(modulesStr[0])
    except ValueError:
        # Ignore "通年" items and similar.
        return modules

    for c in modulesStr[1:]:
        if c in [v.value for v in Semester]:
            currentSemester = Semester(c)
        else:
            try:
                mname = ModuleName(c)
            except ValueError:
                # Ignore "集中" items and similar.
                continue

            modules.append(Module(currentSemester, mname))
    return modules
