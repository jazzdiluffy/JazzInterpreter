from Parser.NodeOfST import NodeOfST
import enum


class NodeType(enum.Enum):
    Program = "program"
    SentenceList = "sentence_list"
    ID = "id"
    Declaration = "declaration"
    Assignment = "assignment"
    Expression = "expression"
    BinaryOperator = "binary_operator"
    UnaryOperator = "unary_operator"
    Variable = "variable"
    Type = "type"
    Int = "int"
    Bool = "bool"
    Constant = "constant"
    ListArgs = "list_args"
    ListExpressions = "list_expressions"
    If = "if"
    For = "for"
    FuncDeclaration = "func_declaration"
    Function = "function"
    ReturnSpecification = "return_spec"
    Parameters = "parameters"
    Parameter = "parameter"
    CallFunction = "func_call"
    ReturnList = "return_list"
    CallList = "call_list"


class NodeSTBuilder:
    def program(self, p):
        p[0] = NodeOfST(node_type=NodeType.Program.value, value="prog", children=[p[1]])

    def sentence_list(self, p):
        if len(p) == 2:
            p[0] = NodeOfST(node_type=NodeType.SentenceList.value, value="", children=[p[1]])
        elif len(p) == 3:
            p[0] = NodeOfST(node_type=NodeType.SentenceList.value, value="", children=[p[1], p[2]])

    def single_sentence(self, p):
        p[0] = p[1]

    def declaration(self, p):
        if len(p) == 5:
            child = NodeOfST(node_type=NodeType.ID.value, value=p[2], children=[])
            p[0] = NodeOfST(node_type=NodeType.Declaration.value, value=p[1], children=[child, p[4]])
        else:
            child = NodeOfST(node_type=NodeType.ID.value, value=p[2], children=[])
            p[0] = NodeOfST(node_type=NodeType.Declaration.value, value=p[1], children=[child, p[5]])

    def assignment(self, p):
        if len(p) == 4:
            p[0] = NodeOfST(node_type=NodeType.Assignment.value, value=p[1], children=[p[3]])
        else:
            p[0] = NodeOfST(node_type=NodeType.Assignment.value, value=p[1], children=[p[4]])

    def expression(self, p):
        p[0] = NodeOfST(node_type=NodeType.Expression.value, value="", children=p[1])

    def math_expression(self, p):
        if len(p) == 4:
            p[0] = NodeOfST(node_type=NodeType.BinaryOperator.value, value=p[2], children=[p[1], p[3]])
        if len(p) == 3 and p[1] != "!":
            p[0] = NodeOfST(node_type=NodeType.UnaryOperator.value, value=p[2], children=[p[1]])
        elif len(p) == 3 and p[1] == "!":
            p[0] = NodeOfST(node_type=NodeType.UnaryOperator.value, value=p[1], children=[p[2]])

    def variable(self, p):
        p[0] = NodeOfST(node_type=NodeType.Variable.value, value=p[1], children=[])

    def type(self, p):
        p[0] = NodeOfST(node_type=NodeType.Type.value, value=p[1], children=[])

    def int(self, p):
        p[0] = p[1]

    def bool(self, p):
        p[0] = p[1]

    def constant(self, p):
        p[0] = NodeOfST(node_type=NodeType.Constant.value, value=p[1])

    def list_args(self, p):
        if len(p) == 2:
            p[0] = NodeOfST(node_type=NodeType.ListArgs.value, value="", children=[p[1]])
        elif len(p) == 4:
            p[0] = NodeOfST(node_type=NodeType.ListArgs.value, value="", children=[p[2]])
        else:
            p[0] = NodeOfST(node_type=NodeType.ListArgs.value, value="", children=[p[1], p[4]])

    def list_expressions(self, p):
        if len(p) == 2:
            p[0] = NodeOfST(node_type=NodeType.ListExpressions.value, value="", children=[p[1]])
        else:
            p[0] = NodeOfST(node_type=NodeType.ListExpressions.value, value="", children=[p[1], p[3]])

    def if_build(self, p):
        conditionChild = p[2]
        bodyChild = p[5]
        p[0] = NodeOfST(node_type=NodeType.If.value, value="", children=[conditionChild, bodyChild])

    def for_build(self, p):
        variableChild = NodeOfST(node_type=NodeType.Variable.value, value=p[2], children=[])
        startChild = p[4]
        stopChild = p[6]
        forbodyChild = p[9]
        p[0] = NodeOfST(node_type=NodeType.For.value, value="",
                        children=[variableChild, startChild, stopChild, forbodyChild])

    def function(self, p, funcTable):
        if len(p) == 11:
            print("[DEBUG] len func 11")
            func_key = p[3]
            returnSpecChild = p[1]
            parametersChild = p[5]
            funcBodyChild = p[9]
            funcTable[func_key] = NodeOfST(node_type=NodeType.FuncDeclaration.value,
                                           value=func_key,
                                           children={"return_spec": returnSpecChild,
                                                     "params": parametersChild,
                                                     "body": funcBodyChild})
            p[0] = NodeOfST(node_type=NodeType.Function.value, value=p[3])
        elif len(p) == 10 and p[1] != NodeType.Function.value:
            print("[DEBUG] len func 10 and has return_spec")
            func_key = p[3]
            returnSpecChild = p[1]
            funcBodyChild = p[8]
            funcTable[func_key] = NodeOfST(node_type=NodeType.FuncDeclaration.value,
                                           value=func_key,
                                           children={"return_spec": returnSpecChild,
                                                     "body": funcBodyChild})
            p[0] = NodeOfST(node_type=NodeType.Function.value, value=p[3])
        elif len(p) == 10 and p[1] == NodeType.Function.value:
            print("[DEBUG] len func 10 and no return_spec")
            func_key = p[2]
            parametersChild = p[4]
            funcBodyChild = p[8]
            funcTable[func_key] = NodeOfST(node_type=NodeType.FuncDeclaration.value,
                                           value=func_key,
                                           children={"params": parametersChild,
                                                     "body": funcBodyChild})
            p[0] = NodeOfST(node_type=NodeType.Function.value, value=p[2])
        else:
            print("[DEBUG] len func else")
            func_key = p[2]
            funcBodyChild = p[7]
            funcTable[func_key] = NodeOfST(node_type=NodeType.FuncDeclaration.value,
                                           value=func_key,
                                           children={"body": funcBodyChild})
            p[0] = NodeOfST(node_type=NodeType.Function.value, value=p[2])

    def return_spec(self, p):
        if len(p) == 3 or len(p) == 4:
            p[0] = NodeOfST(node_type=NodeType.ReturnSpecification.value, value="", children=[p[1], p[2]])
        else:
            p[0] = NodeOfST(node_type=NodeType.ReturnSpecification.value, value="", children=[p[1], p[3], p[4]])

    def parameters(self, p):
        if len(p) == 4:
            p[0] = NodeOfST(node_type=NodeType.Parameters.value, value="", children=[p[1], p[3]])
        else:
            p[0] = NodeOfST(node_type=NodeType.Parameters.value, value="", children=[p[1]])

    def parameter(self, p):
        if len(p) == 3:
            p[0] = NodeOfST(node_type=NodeType.Parameter.value, value="", children=[p[1], p[2]])
        elif len(p) == 5:
            p[0] = NodeOfST(node_type=NodeType.Parameter.value, value="", children=[p[1], p[2], p[4]])
        elif len(p) == 7:
            p[0] = NodeOfST(node_type=NodeType.Parameter.value, value="", children=[p[1], p[2], p[5]])

    def func_call(self, p):
        if len(p) == 2:
            p[0] = NodeOfST(NodeType.CallFunction.value, value=p[1], children={})
        elif len(p) == 3:
            p[0] = NodeOfST(NodeType.CallFunction.value, value=p[1], children={'call': p[2]})
        elif len(p) == 4:
            p[0] = NodeOfST(NodeType.CallFunction.value, value=p[3], children={'return': p[1]})
        elif len(p) == 5:
            p[0] = NodeOfST(NodeType.CallFunction.value, value=p[3], children={'return': p[1], 'call': p[4]})
        elif len(p) == 6:
            p[0] = NodeOfST(NodeType.CallFunction.value, value=p[4], children={'return': [p[1], p[2]], 'call': p[5]})

    def ret_list(self, p):
        if len(p) == 2:
            p[0] = NodeOfST(NodeType.ReturnList.value, value="", children=p[1])
        elif len(p) == 4:
            p[0] = NodeOfST(NodeType.ReturnList.value, value="", children=[p[1], p[3]])

    def call_list(self, p):
        if len(p) == 2:
            p[0] = NodeOfST(NodeType.CallList.value, value="", children=[p[1]])
        else:
            p[0] = NodeOfST(NodeType.CallList.value, value="", children=[p[1], p[3]])

    def ind_exp(self, p):
        if len(p) == 3 and p[1] == ':':
            p[0] = NodeOfST('colon', value=p[1])
        elif len(p) == 3 and p[2] == ':':
            p[0] = NodeOfST('colon', value=p[2])
        else:
            p[0] = NodeOfST('comma', value=p[1])

    def ind(self, p):
        if len(p) == 2:
            p[0] = NodeOfST('index', value="", children=p[1])
        elif len(p) == 3 and (p[2].type == 'colon' or p[2].type == 'comma'):
            p[0] = NodeOfST('index', value="", children=[p[1]])
        elif len(p) == 3 and (p[1].type == 'colon' or p[1].type == 'comma'):
            p[0] = NodeOfST('index', value="", children=[p[1], p[2]])
        elif len(p) == 4:
            p[0] = NodeOfST('index', value="", children=p[2])
