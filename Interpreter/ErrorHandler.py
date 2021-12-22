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
    MissingParameterError = 5
    RecursionError = 6
    ReturnSpecificationError = 7
    FunctionReturnAssignmentError = 8


class ErrorHandler:
    def __init__(self):
        self.linenumber_placeholder = 2

    def raise_error(self, code=-1):
        errors_description = {
            -1: f"[ERROR]: Got unexpected error {self.linenumber_placeholder}",
            1: f"[ERROR]: Missing 'main()' function in program!",
            2: f"[ERROR]: You have variables with same names ",
            3: f"[ERROR]: Trying to use undeclared variable/constant/function",
            4: f"[ERROR]: Trying to assign unrelated type",
            5: f"[ERROR]: Missing passing parameters in function call",
            6: f"[ERROR]: Maximum recursion depth reached",
            7: f"[ERROR]: Return specification not completed: declare needed variables in defined configuration",
            8: f"[ERROR]: Function returns values, you should to assign them"
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
            case ErrorType.MissingParameterError.value:
                yellAboutError(errors_description[5])
            case ErrorType.RecursionError.value:
                yellAboutError(errors_description[6])
            case ErrorType.ReturnSpecificationError.value:
                yellAboutError(errors_description[7])
            case ErrorType.FunctionReturnAssignmentError.value:
                yellAboutError(errors_description[8])
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

class MissingParameterException(Exception):
    pass

class RecursionException(Exception):
    pass

class ReturnSpecificationException(Exception):
    pass

class FunctionReturnAssignmentException(Exception):
    pass
