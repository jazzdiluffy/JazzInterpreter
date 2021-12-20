import sys
import enum


def yellAboutError(errorInfo="Something got wrong!"):
    sys.stderr.write(errorInfo)


class ErrorType(enum.Enum):
    UnexpectedError = -1
    MissingProgramStartPoint = 1
    RedeclarationError = 2
    UndeclaredError = 3
    TypeError = 4


class ErrorHandler:
    def __init__(self):
        self.linenumber_placeholder = 2

    def raise_error(self, code=-1):
        errors_description = {
            -1: f"[ERROR]: Got unexpected error {self.linenumber_placeholder}",
            1: f"[ERROR]: Missing 'main()' function in program!",
            2: f"[ERROR]: You have variables with same names ",
            3: f"[ERROR]: Trying to use undeclared variable/constant/function",
            4: f"[ERROR]: Trying to assign unrelated type"
        }
        match code:
            case ErrorType.MissingProgramStartPoint.value:
                yellAboutError(errors_description[1])
            case ErrorType.RedeclarationError.value:
                yellAboutError(errors_description[2])
            case ErrorType.UndeclaredError.value:
                yellAboutError(errors_description[3])
            case ErrorType.TypeError.value:
                yellAboutError(errors_description[4])
            case _:
                print("[DEBUG]: Got incorrect code for raising error")


class RedeclarationException(Exception):
    pass


class ValueException(Exception):
    pass


class UnexpectedTypeException(Exception):
    pass

class UndeclaredException(Exception):
    pass

class TypeException(Exception):
    pass
