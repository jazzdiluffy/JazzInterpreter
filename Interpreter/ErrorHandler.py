import sys
import enum


def yellAboutError(errorInfo="Somethig got wrong!"):
    sys.stderr.write(errorInfo)


class ErrorType(enum.Enum):
    UnexpectedError = -1
    MissingProgramStartPoint = 1


class ErrorHandler:
    def __init__(self):
        self.linenumber_placeholder = 2



    def raise_error(self, code=-1):
        errors_description = {
            -1: f"[ERROR]: Got unexpected error {self.linenumber_placeholder}",
            1: f"[ERROR]: Missing 'main()' function in program!"
        }
        match code:
            case 1:
                yellAboutError(errors_description[1])
            case _:
                print("[DEBUG]: Got incorrect code for raising error")