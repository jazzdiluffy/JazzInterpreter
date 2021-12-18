import sys
import enum


def yellAboutError(errorInfo="Something got wrong!"):
    sys.stderr.write(errorInfo)


class ErrorType(enum.Enum):
    UnexpectedError = -1
    MissingProgramStartPoint = 1
    RedeclarationError = 2


class ErrorHandler:
    def __init__(self):
        self.linenumber_placeholder = 2

    def raise_error(self, code=-1):
        errors_description = {
            -1: f"[ERROR]: Got unexpected error {self.linenumber_placeholder}",
            1: f"[ERROR]: Missing 'main()' function in program!",
            2: f"[ERROR]: You have variables with same names "
        }
        match code:
            case ErrorType.MissingProgramStartPoint.value:
                yellAboutError(errors_description[1])
            case ErrorType.RedeclarationError.value:
                yellAboutError(errors_description[2])
            case _:
                print("[DEBUG]: Got incorrect code for raising error")


class RedeclarationException(Exception):
    pass


class ValueException(Exception):
    pass


class UnexpectedTypeException(Exception):
    pass
