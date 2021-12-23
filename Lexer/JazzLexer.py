# ------------------------------------------------------------
# Lexer.py
#
# tokenizer for language from task
# ------------------------------------------------------------
import ply.lex as lexer


def binary_to_decimal(num):
    return int(num, 2)


class JazzLexer(object):
    def __init__(self):
        self.lexer = lexer.lex(module=self)

    reserved = {
        "true": "TRUE", "false": "FALSE", "bool": "BOOL", "cmbool": "CMBOOL", "mbool": "MBOOL",
        "cvbool": "CVBOOL", "vbool": "VBOOL", "cbool": "CBOOL",

        "int": "INT", "cvint": "CVINT", "vint": "VINT", "cmint": "CMINT", "mint": "MINT", "cint": "CINT",

        "for": "FOR", "beginfor": "BEGINFOR", "endfor": "ENDFOR",

        "if": "IF", "beginif": "BEGINIF", "endif": "ENDIF",

        "move": "MOVE", "right": "RIGHT", "left": "LEFT", "wall": "WALL", "exit": "EXIT",

        "function": "FUNCTION", "begin": "BEGIN", "end": "END",

        "and": "AND", "sum": "SUM", "call": "CALL"
    }

    primitive_tokens = [
        "PLUS",
        "MINUS",
        "EQUAL",
        "GREATER",
        "LESS",
        "ASSIGN",
        "LEFT_BRACKET",
        "RIGHT_BRACKET",
        "COMMA",
        "LEFT_CYCLIC_SHIFT",
        "RIGHT_CYCLIC_SHIFT",
        "NEGATIVE",
        "MATRIX_MUL",
        "ELEMENTAL_MUL",
        "TRANSPOSITION",
        "DOUBLE_DOT",
        "LEFT_FIGURE_BRACKET",
        "RIGHT_FIGURE_BRACKET",
        "NEW_LINE",
        "VARIABLE",
        "INT_BINARY",
        "INT_DECIMAL"
    ]

    tokens = primitive_tokens + list(reserved.values())

    t_PLUS = r"\+"
    t_MINUS = r"\-"
    t_EQUAL = r"\="
    t_GREATER = r"\>"
    t_LESS = r"\<"
    t_ASSIGN = r"\<\-"
    t_LEFT_BRACKET = r"\("
    t_RIGHT_BRACKET = r"\)"
    t_COMMA = r"\,"
    t_LEFT_CYCLIC_SHIFT = r"\<\<"
    t_RIGHT_CYCLIC_SHIFT = r"\>\>"
    t_NEGATIVE = r"\!"
    t_MATRIX_MUL = r"\*"
    t_ELEMENTAL_MUL = r"\.\*"
    t_TRANSPOSITION = r"\'"
    t_DOUBLE_DOT = r"\:"
    t_LEFT_FIGURE_BRACKET = r"\{"
    t_RIGHT_FIGURE_BRACKET = r"\}"
    t_AND = r"\&\&"

    t_ignore = ' \t'

    def t_VARIABLE(self, t):
        r"""[a-zA-Z][a-zA-Z_0-9]*"""
        t.type = self.reserved.get(t.value, "VARIABLE")  # Check for reserved words
        return t

    def t_INT_BINARY(self, t):
        r"""0[01]+"""
        t.value = binary_to_decimal(t.value)
        return t

    def t_INT_DECIMAL(self, t):
        r"""\d+"""
        t.value = int(t.value)
        return t

    def t_LINE_BREAK(self, t):
        r"""\.\.\.\n+"""
        # Assign new value to line number depending on amount of \n escape-sequences
        t.lexer.lineno += len(t.value) - 3
        pass

    def t_NEW_LINE(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)
        return t

    def t_error(self, t):
        print("\n[ERROR_HANDLER] Illegal character: '%s'" % t.value[0])
        print("[ERROR_HANDLER] Line: '%d'\n" % t.lexer.lineno)
        t.lexer.skip(1)

    def t_comment(self, t):
        r"""//.*\n+"""
        t.lexer.lineno += len(t.value) - len(t.value.replace("\n", ""))
        pass

    def token(self):
        return self.lexer.token()

    def input(self, data):
        return self.lexer.input(data)


if __name__ == '__main__':
    print("Test filename: ", end="")
    filename = input()
    filepath = '/Users/jazzdiluffy/Desktop/JazzInterpreter/Testing/test_interpreter_' + filename + '.txt'

    f = open(filepath, 'r+')
    data = f.read()
    f.close()
    lexer = JazzLexer()
    lexer.input(data)
    while True:
        token = lexer.token()
        if token is None:
            break
        else:
            print(token)
