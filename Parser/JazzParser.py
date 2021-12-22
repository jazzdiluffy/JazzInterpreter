from Lexer.JazzLexer import JazzLexer
import ply.yacc as yacc
from Parser.NodeSTBuilder import NodeSTBuilder


# TODO make grammars for calling of functions
# TODO make grammars for robot actions
# TODO getting by index

class JazzParser(object):
    tokens = JazzLexer.tokens
    node_builder = NodeSTBuilder()
    precedence = (
        ('right', 'NEGATIVE'),
        ('left', 'AND'),
        ('nonassoc', 'LESS', 'GREATER')
    )

    def __init__(self):
        self.lexer = JazzLexer()
        self.parser = yacc.yacc(module=self)
        self.funcTable = dict()
        self.hasSyntaxErrors = False

    def parse(self, input_data, debug=False):
        parse_result = self.parser.parse(input_data, debug=debug)
        return parse_result, self.funcTable, self.hasSyntaxErrors

    def p_program(self, p):
        """program : sentence_list"""
        self.node_builder.program(p)

    def p_sentence_list(self, p):
        """sentence_list : sentence_list single_sentence
                         | single_sentence"""
        self.node_builder.sentence_list(p)

    def p_single_sentence(self, p):
        """single_sentence : declaration NEW_LINE
                           | assignment NEW_LINE
                           | if NEW_LINE
                           | for NEW_LINE
                           | function NEW_LINE
                           | call_func NEW_LINE"""
        self.node_builder.single_sentence(p)

    def p_declaration(self, p):
        """declaration : type VARIABLE EQUAL expression
                       | type VARIABLE EQUAL LEFT_FIGURE_BRACKET list_args RIGHT_FIGURE_BRACKET"""
        self.node_builder.declaration(p)

    def p_assignment(self, p):
        """assignment : variable ASSIGN expression
                      | variable ASSIGN LEFT_FIGURE_BRACKET list_args RIGHT_FIGURE_BRACKET"""
        self.node_builder.assignment(p)

    def p_expression(self, p):
        """expression : math_expression
                      | variable
                      | constant"""
        self.node_builder.expression(p)

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
        self.node_builder.math_expression(p)

    def p_variable(self, p):
        """variable : VARIABLE"""
       #             | VARIABLE LEFT_BRACKET index RIGHT_BRACKET"""
        self.node_builder.variable(p)

    def p_type(self, p):
        """type : int
                | bool"""
        self.node_builder.type(p)

    def p_int(self, p):
        """int : INT
               | CVINT
               | VINT
               | CMINT
               | MINT
               | CINT"""
        self.node_builder.int(p)

    def p_bool(self, p):
        """bool : BOOL
                | CMBOOL
                | MBOOL
                | CVBOOL
                | VBOOL
                | CBOOL"""
        self.node_builder.bool(p)

    def p_constant(self, p):
        """constant : INT_BINARY
                    | INT_DECIMAL
                    | TRUE
                    | FALSE"""
        self.node_builder.constant(p)

    def p_list_args(self, p):
        """list_args : LEFT_FIGURE_BRACKET list_expressions RIGHT_FIGURE_BRACKET
                     | list_args COMMA LEFT_FIGURE_BRACKET list_args RIGHT_FIGURE_BRACKET
                     | list_expressions"""
        self.node_builder.list_args(p)

    def p_list_expressions(self, p):
        """list_expressions : list_expressions COMMA expression
                            | expression"""
        self.node_builder.list_expressions(p)

    def p_if(self, p):
        """if : IF expression BEGINIF NEW_LINE sentence_list ENDIF"""
        self.node_builder.if_build(p)

    def p_for(self, p):
        """for : FOR VARIABLE EQUAL expression DOUBLE_DOT expression BEGINFOR NEW_LINE sentence_list ENDFOR"""
        self.node_builder.for_build(p)

    def p_function(self, p):
        """function : return_spec FUNCTION VARIABLE LEFT_BRACKET parameters RIGHT_BRACKET BEGIN NEW_LINE sentence_list END
                    | return_spec FUNCTION VARIABLE LEFT_BRACKET RIGHT_BRACKET BEGIN NEW_LINE sentence_list END
                    | FUNCTION VARIABLE LEFT_BRACKET parameters RIGHT_BRACKET BEGIN NEW_LINE sentence_list END
                    | FUNCTION VARIABLE LEFT_BRACKET RIGHT_BRACKET BEGIN NEW_LINE sentence_list END"""
        self.node_builder.function(p, self.funcTable)

    def p_return_spec(self, p):
        """return_spec : return_spec COMMA type VARIABLE EQUAL
                       | type VARIABLE EQUAL
                       | type VARIABLE"""
        self.node_builder.return_spec(p)

    def p_parameters(self, p):
        """parameters : parameters COMMA parameter
                      | parameter"""
        self.node_builder.parameters(p)

    def p_parameter(self, p):
        """parameter : type VARIABLE
                     | type VARIABLE EQUAL constant
                     | type VARIABLE EQUAL LEFT_FIGURE_BRACKET list_args RIGHT_FIGURE_BRACKET"""
        self.node_builder.parameter(p)
    # | type VARIABLE EQUAL list_args
    def p_call_func(self, p):
        """call_func : VARIABLE
                         | VARIABLE call_list
                         | ret_list ASSIGN VARIABLE call_list
                         | ret_list ASSIGN VARIABLE
                         | variable ASSIGN VARIABLE call_list
                         | type VARIABLE EQUAL VARIABLE call_list"""
        self.node_builder.func_call(p)

    def p_ret_list(self, p):
        """ret_list : variable
                    | ret_list COMMA variable"""
        self.node_builder.ret_list(p)

    def p_call_list(self, p):
        """call_list : call_list COMMA expression
                    | expression"""
        self.node_builder.call_list(p)

    def p_error(self, p):
        try:
            print("Syntax error, line: %d\n" % p.lineno)
        except Exception:
            print("Syntax error")
        self.hasSyntaxErrors = True


if __name__ == '__main__':
    parser = JazzParser()
    print("Enter filename: ", end="")
    filename = input()
    s = f'/Users/jazzdiluffy/Desktop/JazzInterpreter/Testing/test_interpreter_{filename}.txt'
    f = open(s, 'r')
    data = f.read()
    f.close()

    syntax_tree, func_table, hasErrors = parser.parse(data, debug=False)
    print(syntax_tree)
