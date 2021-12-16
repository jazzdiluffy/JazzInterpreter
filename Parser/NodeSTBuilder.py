from Parser.NodeOfST import NodeOfST


class NodeSTBuilder:
    def program(self, p):
        p[0] = NodeOfST(node_type="program", value="prog", children=[p[1]])

    def sentence_list(self, p):
        if len(p) == 2:
            p[0] = NodeOfST(node_type="sentence_list", value="", children=[p[1]])
        elif len(p) == 3:
            p[0] = NodeOfST(node_type="sentence_list", value="", children=[p[1], p[2]])

    def single_sentence(self, p):
        p[0] = p[1]

    def declaration(self, p):
        if len(p) == 5:
            child = NodeOfST(node_type="id", value=p[2], children=[p[4]])
            p[0] = NodeOfST(node_type="declaration", value=p[1], children=[child])
        else:
            child = NodeOfST(node_type="id", value=p[2], children=[p[5]])
            p[0] = NodeOfST(node_type="declaration", value=p[1], children=[child])

    def assignment(self, p):
        if len(p) == 4:
            child = NodeOfST(node_type="id", value="", children=[p[3]])
            p[0] = NodeOfST(node_type="assignment", value=p[1], children=[child])
        else:
            child = NodeOfST(node_type="id", value="", children=[p[4]])
            p[0] = NodeOfST(node_type="assignment", value=p[1], children=[child])

    def expression(self, p):
        p[0] = NodeOfST(node_type="expression", value="", children=[p[1]])

    def math_expression(self, p):
        if len(p) == 4:
            p[0] = NodeOfST(node_type="binary_operator", value=p[2], children=[p[1], p[3]])

    def variable(self, p):
        p[0] = NodeOfST(node_type="variable", value=p[1], children=[])

    def type(self, p):
        p[0] = NodeOfST(node_type="type", value="", children=[p[1]])

    def int(self, p):
        p[0] = NodeOfST(node_type="int", value=p[1])

    def bool(self, p):
        p[0] = NodeOfST(node_type="bool", value=p[1])

    def constant(self, p):
        p[0] = NodeOfST(node_type="constant", value=p[1])

    def list_args(self, p):
        if len(p) == 2:
            p[0] = NodeOfST(node_type="list_args", value="", children=[p[1]])
        elif len(p) == 4:
            p[0] = NodeOfST(node_type="list_args", value="", children=[p[2]])
        else:
            p[0] = NodeOfST(node_type="list_args", value="", children=[p[1], p[4]])

    def list_expressions(self, p):
        if len(p) == 2:
            p[0] = NodeOfST(node_type="list_expressions", value="", children=[p[1]])
        else:
            p[0] = NodeOfST(node_type="list_expressions", value="", children=[p[1], p[3]])

    def if_build(self, p):
        conditionChild = p[2]
        bodyChild = p[5]
        p[0] = NodeOfST(node_type="if", value="", children=[conditionChild, bodyChild])

    def for_build(self, p):
        variableChild = NodeOfST(node_type="variable", value=p[2], children=[])
        startChild = p[4]
        stopChild = p[6]
        ifbodyChild = p[9]
        p[0] = NodeOfST(node_type="for", value="", children=[variableChild, startChild, stopChild, ifbodyChild])


    def function(self, p, funcTable):
        if len(p) == 11:
            func_key = p[3]
            returnSpecChild = p[1]
            parametersChild = p[5]
            funcBodyChild = p[9]
            funcTable[func_key] = NodeOfST(node_type="func_declaration",
                                                value="",
                                                children=[returnSpecChild, parametersChild, funcBodyChild])
            p[0] = NodeOfST(node_type="function", value=p[3])
        elif len(p) == 10 and p[1] != "function":
            func_key = p[3]
            returnSpecChild = p[1]
            funcBodyChild = p[8]
            funcTable[func_key] = NodeOfST(node_type="func_declaration",
                                                value="",
                                                children=[returnSpecChild, funcBodyChild])
            p[0] = NodeOfST(node_type="function", value=p[3])
        elif len(p) == 10 and p[1] == "function":
            func_key = p[2]
            parametersChild = p[4]
            funcBodyChild = p[8]
            funcTable[func_key] = NodeOfST(node_type="func_declaration",
                                                value="",
                                                children=[parametersChild, funcBodyChild])
            p[0] = NodeOfST(node_type="function", value=p[2])
        else:
            func_key = p[2]
            funcBodyChild = p[8]
            funcTable[func_key] = NodeOfST(node_type="func_declaration",
                                                value="",
                                                children=[funcBodyChild])
            p[0] = NodeOfST(node_type="function", value=p[2])

    def return_spec(self, p):
        if len(p) == 3 or len(p) == 4:
            p[0] = NodeOfST(node_type="return_spec", value="", children=[p[1], p[2]])
        else:
            p[0] = NodeOfST(node_type="return_spec", value="", children=[p[1], p[3], p[4]])

    def parameters(self, p):
        if len(p) == 4:
            p[0] = NodeOfST(node_type="parameters", value="", children=[p[1], p[3]])
        else:
            p[0] = NodeOfST(node_type="parameters", value="", children=[p[1]])

    def parameter(self, p):
        if len(p) == 3:
            p[0] = NodeOfST(node_type="parameter", value="", children=[p[1], p[2]])
        elif len(p) == 5:
            p[0] = NodeOfST(node_type="parameter", value="", children=[p[1], p[2], p[4]])
        elif len(p) == 7:
            p[0] = NodeOfST(node_type="parameter", value="", children=[p[1], p[2], p[5]])
