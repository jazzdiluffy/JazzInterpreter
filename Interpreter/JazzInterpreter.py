from Parser.JazzParser import JazzParser
from ErrorHandler import *


class JazzInterpreter:
    def __init__(self):
        self.parser = JazzParser()
        self.syntax_tree = None
        self.func_table = None

    def start(self, prog=None):
        self.syntax_tree, self.func_table, has_syntax_errors = self.parser.parse(prog)
        if not has_syntax_errors:
            self.handleCaseWithoutSyntaxErrors()

    def handleCaseWithoutSyntaxErrors(self):
        mainFuncKey = "main"
        if mainFuncKey in self.func_table.keys():
            print("[DEBUG]: Main func exists: start handling syntax tree ...")

        else:
            ErrorHandler().raise_error(code=ErrorType.MissingProgramStartPoint.value)
            return

    # TODO: make this match-case function using ENUMS, in parser also
    def handleNode(self, node):
        if node is None:
            return "None Node"
        node_type = node.type

        match node_type:
            case "program":
                self.handleNode(node.children)
            case "sentence_list":
                for child in node.children:
                    self.handleNode(child)
            case _:
                print("[DEBUG]: Errors in grammar and syntax tree building")




if __name__ == '__main__':
    interpreter = JazzInterpreter()
    s = f'/Users/jazzdiluffy/Desktop/JazzInterpreter/Testing/test_parser_functions.txt'
    f = open(s, "r")
    program = f.read()
    f.close()
    interpreter.start(program)
