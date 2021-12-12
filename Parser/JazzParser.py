from Lexer.JazzLexer import JazzLexer
import ply.yacc as yacc
from NodeOfST import NodeOfST


class JazzParser(object):
    tokens = JazzLexer.tokens

    def __init__(self):
        self.lexer = JazzLexer()
        self.parser = yacc.yacc(module=self)
        self.hasSyntaxErrors = False

    def p_program(self, p):
        """program : sentence_list"""
        p[0] = NodeOfST(node_type="program", value="prog", children=[p[1]])

    def p_sentence_list(self, p):
        """sentence_list : sentence_list single_sentence
                         | single_sentence"""
        if len(p) == 2:
            p[0] = NodeOfST(node_type="sentence_list", value="", children=[p[1]])
        elif len(p) == 3:
            p[0] = NodeOfST(node_type="sentence_list", value="", children=[p[1], p[2]])

    def p_single_sentence(self, p):
        """single_sentence : declaration NEW_LINE
                           | assignment NEW_LINE"""
        p[0] = p[1]

    def p_declaration(self, p):
        """declaration : type VARIABLE EQUAL expression"""
        child = NodeOfST(node_type="id", value=p[2], children=[p[4]])
        p[0] = NodeOfST(node_type="declaration", value=p[1], children=[child])

    def p_assignment(self, p):
        """assignment : variable ASSIGN expression"""
        child = NodeOfST(node_type="id", value="", children=[p[3]])
        p[0] = NodeOfST(node_type="assignment", value=p[1], children=[child])

    def p_expression(self, p):
        """expression : math_expression
                      | variable
                      | constant"""
        p[0] = NodeOfST(node_type="expression", value="", children=[p[1]])

    def p_math_expression(self, p):
        """math_expression : expression PLUS expression
                           | expression MINUS expression
                           | expression MATRIX_MUL expression
                           | expression ELEMENTAL_MUL expression
                           | expression LEFT_CYCLIC_SHIFT
                           | expression RIGHT_CYCLIC_SHIFT
                           | expression TRANSPOSITION
                           | expression LESS expression
                           | expression GREATER expression
                           | NEGATIVE expression
                           | expression AND expression"""
        if len(p) == 4:
            p[0] = NodeOfST(node_type="binary_operator", value=p[2], children=[p[1], p[3]])

    def p_variable(self, p):
        """variable : VARIABLE"""
        p[0] = NodeOfST(node_type="variable", value=p[1], children=[])

    def p_type(self, p):
        """type : int
                | bool"""
        p[0] = NodeOfST(node_type="type", value="", children=[p[1]])

    def p_int(self, p):
        """int : INT
               | CVINT
               | VINT
               | CMINT
               | MINT
               | CINT"""
        p[0] = NodeOfST(node_type="int", value=p[1])

    def p_bool(self, p):
        """bool : BOOL
                | CMBOOL
                | MBOOL
                | CVBOOL
                | VBOOL
                | CBOOL"""
        p[0] = NodeOfST(node_type="bool", value=p[1])

    def p_constant(self, p):
        """constant : INT_BINARY
                    | INT_DECIMAL
                    | TRUE
                    | FALSE"""
        p[0] = NodeOfST(node_type="constant", value=p[1])

    def p_error(self, p):
        try:
            print("Syntax error, line: %d\n" % p.lineno)
        except Exception:
            print("Syntax error")
        self.hasSyntaxErrors = True


if __name__ == '__main__':
    parser = JazzParser()
    s = '/Users/jazzdiluffy/Desktop/JazzInterpreter/Testing/test_parser_simple_calc.txt'
    f = open(s, 'r')
    data = f.read()
    f.close()

    syntax_tree = parser.parser.parse(data, debug=False)
    print(syntax_tree)