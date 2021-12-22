from Parser.JazzParser import *
from Parser.NodeSTBuilder import NodeType
from ErrorHandler import *
from TypeConverter import TypeConverter
from Variable import Variable
from collections import deque


class JazzInterpreter:
    def __init__(self):
        self.parser = JazzParser()
        self.syntax_tree = None
        self.func_table = None
        self.declaration_table = [dict()]
        self.visibility_scope = 0

    def start(self, prog=None):
        self.syntax_tree, self.func_table, has_syntax_errors = self.parser.parse(prog)
        if not has_syntax_errors:
            self.handleCaseWithoutSyntaxErrors()

    def handleCaseWithoutSyntaxErrors(self):
        mainFuncKey = "main"
        if mainFuncKey in self.func_table.keys():
            start_node = self.func_table["main"].children["body"]
            self.handleNode(start_node)
            for d in self.declaration_table:
                for key in d.keys():
                    # if "result" in key:
                    print(f"{key}: {d[key]}")
                print()
        else:
            ErrorHandler().raise_error(code=ErrorType.MissingProgramStartPoint.value)
            return

    def handleNode(self, node):
        if node is None:
            return "None Node"
        node_type = node.type

        match node_type:
            case NodeType.Program.value:
                self.handleNode(node.children)
            case NodeType.SentenceList.value:
                for child in node.children:
                    self.handleNode(child)
            case NodeType.Declaration.value:
                # declaration-node has field value which equals type-node, and this type-node has field value
                # which equals int-node or bool-node
                type = node.value.value
                # declaration-node has children: VARIABLE and expression|args_list
                children = node.children
                try:
                    self.declare(type, children)
                except RedeclarationException:
                    ErrorHandler().raise_error(ErrorType.RedeclarationError.value)
                except ValueException:
                    print("[DEBUG]: Value Exception")
                    pass
                except UnexpectedTypeException:
                    print("[DEBUG]: Unexpected Type Exception")
                    pass
            case NodeType.Assignment.value:
                try:
                    return self.handle_assignment(node)
                except UndeclaredException:
                    ErrorHandler().raise_error(ErrorType.UndeclaredError.value)
            case NodeType.Expression.value:
                return self.handleNode(node.children)
            case NodeType.ListExpressions.value:
                pass
            case NodeType.ListArgs.value:
                if len(node.children) == 1:
                    return self.configure_list(node)
                return self.configure_list(node)[::-1]
            case NodeType.Variable.value:
                try:
                    return self.extract_variable_value(node)
                except UndeclaredException:
                    ErrorHandler().raise_error(ErrorType.UndeclaredError.value)
            case NodeType.Constant.value:
                return Variable("bool", node.value) if node.value == "true" or node.value == "false" else Variable(
                    "int", node.value)
            case NodeType.BinaryOperator.value:
                return self.handle_binary_operator(node)
            case NodeType.UnaryOperator.value:
                return self.handle_unary_operator(node)
            case NodeType.If.value:
                self.handle_if(node)
            case NodeType.For.value:
                self.handle_for(node)
            case NodeType.FuncDeclaration.value:
                pass
            case NodeType.Function.value:
                pass
            case NodeType.ReturnSpecification.value:
                pass
            case NodeType.Parameters.value:
                pass
            case NodeType.Parameter.value:
                pass
            case NodeType.CallFunction.value:
                # node: type: func_call, value: name of calling function
                returned_values = self.handle_function_call(node)
                pass
            case _:
                print("[DEBUG]: Errors in grammar and syntax tree building")

    def declare(self, decl_type, children):
        # Example: cint a = {1, 2, 3}
        # where {1, 2, 3} is declaration_value
        declaration_value = children[1]
        declaration_name = children[0].value
        match declaration_value.type:
            case NodeType.Expression.value:
                expression = self.handleNode(declaration_value)
                self.add_to_declare_table(decl_type, declaration_name, expression)
            case NodeType.ListArgs.value:
                args_list = self.handleNode(declaration_value)
                self.add_to_declare_table(decl_type, declaration_name, self.make_variable_instance(args_list))

    def add_to_declare_table(self, decl_type, decl_name, value):
        expression = self.configure_declaration(decl_type, value)
        declaration_table_in_scope = self.declaration_table[self.visibility_scope]
        if decl_name not in declaration_table_in_scope.keys():
            declaration_table_in_scope[decl_name] = expression
        else:
            raise RedeclarationException

    def configure_declaration(self, type, value):
        types_without_vm_modifiers = ["int", "cint", "bool", "cbool"]
        if type in types_without_vm_modifiers and value.type in types_without_vm_modifiers:
            if type == "cbool" and isinstance(value.value, int):
                return Variable("cbool", bool(value.value))
            elif type == "cint" and isinstance(value.value, bool):
                return Variable("cint", int(value.value))
            return self.configure_variable(type, value)
        elif "v" in type and "v" in value.type:
            a = self.configure_vector(type, value)
            return a
        elif "m" in type and "m" in value.type:
            return self.configure_matrix(type, value)

        else:
            raise UnexpectedTypeException

    def configure_variable(self, type, value):
        return TypeConverter().convert_type(type, value)

    def configure_vector(self, type, value):
        if "c" in type:
            elems_type = type[2:]
        else:
            elems_type = type[1:]
        converted_vector_values = [TypeConverter().convert_type(elems_type, elem) for elem in value.value]
        return Variable(type, converted_vector_values)

    def configure_matrix(self, type, decl_value):
        value = decl_value.value
        if "c" in type:
            elems_type = type[2:]
        else:
            elems_type = type[1:]
        rectangular_matrix_length = len(value[0])
        converted_matrix_elems = value
        # check is matrix rectangular
        for i in range(len(value)):
            if len(value[i]) != rectangular_matrix_length:
                raise ValueException
        for i in range(len(value)):
            converted_matrix_elems[i] = [TypeConverter().convert_type(elems_type, elem) for elem in
                                         converted_matrix_elems[i]]
            a = converted_matrix_elems[i]
        return Variable(type, converted_matrix_elems)

    # [i[::-1] for i in numbers[::-1]]
    # returns reversed in all dimensions list
    # TODO: {{1,2,3}} case should handle correctly
    def configure_list(self, node):
        result = []

        if len(node.children) == 2:
            tmp_right = self.configure_list(node.children[1])
            result.append(tmp_right)
            tmp_left = self.configure_list(node.children[0])
            if isinstance(tmp_left[0], list):
                result += tmp_left
            else:
                result.append(tmp_left)
        else:
            return self.configure_expression_list(node.children[0])[::-1]
        return result

    def make_variable_instance(self, value):
        if isinstance(value[0], list):
            if type(value[0][0].value) is int:
                return Variable("mint", value)
            else:
                return Variable("mbool", value)
        else:
            if type(value[0].value) is int:
                return Variable('vint', value)
            else:
                return Variable('vbool', value)

    # returns reversed list of expressions
    def configure_expression_list(self, node):
        result = []
        # expression_list: expression_list expression | expression
        # so we add handled expression and dive into next expression list
        # it will continue until there are no more expressions_list in grammar
        # so there will be only one child
        if len(node.children) == 2:
            result.append(self.handleNode(node.children[1]))
            add = self.configure_expression_list(node.children[0])
            result += add
        else:
            result.append(self.handleNode(node.children[0]))
        return result

    def extract_variable_value(self, node):
        if node.value in self.declaration_table[self.visibility_scope].keys():
            return self.declaration_table[self.visibility_scope][node.value]
        else:
            raise UndeclaredException

    def handle_binary_operator(self, node):
        first_operand = node.children[0]
        second_operand = node.children[1]
        match node.value:
            case "+":
                return self.handle_binary_plus(first_operand, second_operand)
            case "-":
                return self.handle_binary_minus(first_operand, second_operand)
            case "*":
                return self.handle_matrix_multiplication(first_operand, second_operand)
            case ".*":
                return self.handle_elemental_multiplication(first_operand, second_operand)
            case ">":
                return self.handle_greater_operator(first_operand, second_operand)
            case "<":
                return self.handle_less_operator(first_operand, second_operand)
            case ("and" | "&&"):
                return self.handle_and_operator(first_operand, second_operand)

    def handle_binary_plus(self, first_operand, second_operand):
        lhs = TypeConverter().convert_type("int", self.handleNode(first_operand))
        rhs = TypeConverter().convert_type("int", self.handleNode(second_operand))
        return Variable("int", lhs.value + rhs.value)

    def handle_binary_minus(self, first_operand, second_operand):
        lhs = TypeConverter().convert_type("int", self.handleNode(first_operand))
        rhs = TypeConverter().convert_type("int", self.handleNode(second_operand))
        return Variable("int", lhs.value - rhs.value)

    def handle_greater_operator(self, first_operand, second_operand):
        lhs = TypeConverter().convert_type("int", self.handleNode(first_operand))
        rhs = TypeConverter().convert_type("int", self.handleNode(second_operand))
        return Variable("bool", lhs.value > rhs.value)

    def handle_less_operator(self, first_operand, second_operand):
        lhs = TypeConverter().convert_type("int", self.handleNode(first_operand))
        rhs = TypeConverter().convert_type("int", self.handleNode(second_operand))
        return Variable("bool", lhs.value < rhs.value)

    def handle_matrix_multiplication(self, first_operand, second_operand):
        lhs = self.handleNode(first_operand)
        rhs = self.handleNode(second_operand)
        if "m" in lhs.type:
            lhs = self.configure_matrix("mint", lhs)
        else:
            print("[DEBUG]: trying to use matrix multiplication operator fot non-matrix operand")
            pass
        if "m" in rhs.type:
            rhs = self.configure_matrix("mint", rhs)
        else:
            print("[DEBUG]: trying to use matrix multiplication operator fot non-matrix operand")
            pass
        # check if matrices could me multiplied
        # condition: number of colons of first operand == number of rows of second operand
        if len(lhs.value[0]) != len(rhs.value):
            raise ValueException
        result_matrix = []
        # fill by zeros
        for i in range(len(rhs.value[0])):
            result_matrix.append([Variable("int", 0) for j in range(len(lhs.value))])
        for i in range(len(lhs.value)):
            for j in range(len(rhs.value[0])):
                for k in range(len(rhs.value)):
                    result_matrix[i][j].value += lhs.value[i][k].value * rhs.value[k][j].value
        return Variable("mint", result_matrix)

    def handle_elemental_multiplication(self, first_operand, second_operand):
        lhs = self.handleNode(first_operand)
        rhs = self.handleNode(second_operand)
        # V.*V
        if "v" in lhs.type and "v" in rhs.type:
            return self.elem_mul_VV(lhs, rhs)
        # M.*M
        elif "m" in lhs.type and "m" in rhs.type:
            return self.elem_mul_MM(lhs, rhs)
        # V.*x {1, 2, 3}.*2 = {2, 4, 6}
        elif "v" in lhs.type and "v" not in rhs.type and "m" not in rhs.type:
            return self.elem_mul_Vx(lhs, rhs)
        # x.*V 2.*{1, 2, 3} = {{1, 2, 3}, {1, 2, 3}}
        elif "v" not in lhs.type and "m" not in lhs.type and "v" in rhs.type:
            return self.elem_mul_xV(lhs, rhs)
        # M.*x {{1, 2}, {3, 4}}*2 = {{2, 4}, {6, 8}}
        elif "m" in lhs.type and "v" not in rhs.type and "m" not in rhs.type:
            return self.elem_mul_Mx(lhs, rhs)
        # x.*M 2*{{1, 2}, {3, 4}} = {{2, 4}, {6, 8}}
        elif "v" not in lhs.type and "m" not in lhs.type and "m" in rhs.type:
            return self.elem_mul_xM(lhs, rhs)
        else:
            return self.elem_mul_xx(lhs, rhs)

    def elem_mul_VV(self, first_operand, second_operand):
        lhs = self.configure_vector("vint", first_operand)
        rhs = self.configure_vector("vint", second_operand)
        # check if lhs and rhs dimensions are equal
        if len(lhs.value) != len(rhs.value):
            raise ValueException
        result_vector = []
        for i in range(len(lhs.value)):
            result_vector.append(Variable("int", 0))
        for i in range(len(lhs.value)):
            result_vector[i].value = lhs.value[i].value * rhs.value[i].value
        return Variable("vint", result_vector)

    def elem_mul_MM(self, first_operand, second_operand):
        lhs = self.configure_matrix("mint", first_operand)
        rhs = self.configure_matrix("mint", second_operand)
        # check if lhs and rhs dimensions are equal
        if len(lhs.value) != len(rhs.value) or len(lhs.value[0]) != len(rhs.value[0]):
            raise ValueException
        result_matrix = []
        for i in range(len(lhs.value)):
            result_matrix.append([Variable("int", 0) for j in lhs.value[0]])
        for i in range(len(lhs.value)):
            for j in range(len(lhs.value[0])):
                result_matrix[i][j].value = lhs.value[i][j].value * rhs.value[i][j].value
        return Variable("mint", result_matrix)

    def elem_mul_Vx(self, first_operand, second_operand):
        lhs = self.configure_vector("vint", first_operand)
        rhs = self.configure_variable("int", second_operand)
        result_vector = []
        for i in range(len(lhs.value)):
            result_vector.append(Variable("int", 0))
        for i in range(len(lhs.value)):
            result_vector[i].value = lhs.value[i].value * rhs.value
        return Variable("vint", result_vector)

    def elem_mul_xV(self, first_operand, second_operand):
        lhs = self.configure_variable("int", first_operand)
        rhs = self.configure_vector("vint", second_operand)
        result_matrix = []
        for i in range(lhs.value):
            result_matrix.append(rhs.value)
        return Variable("mint", result_matrix)

    def elem_mul_Mx(self, first_operand, second_operand):
        lhs = self.configure_matrix("mint", first_operand)
        # rhs = self.configure_variable("int", second_operand)
        rhs = second_operand
        result_matrix = []
        for i in range(len(lhs.value)):
            result_matrix.append([Variable("int", 0) for j in lhs.value[0]])
        for i in range(len(lhs.value)):
            for j in range(len(lhs.value[0])):
                result_matrix[i][j].value = lhs.value[i][j].value * rhs.value
        return Variable("mint", result_matrix)

    def elem_mul_xM(self, first_operand, second_operand):
        lhs = self.configure_variable("int", first_operand)
        rhs = self.configure_matrix("mint", second_operand)
        result_matrix = []
        for i in range(len(rhs.value)):
            result_matrix.append([Variable("int", 0) for j in rhs.value[0]])
        for i in range(len(rhs.value)):
            for j in range(len(rhs.value[0])):
                result_matrix[i][j].value = lhs.value * rhs.value[i][j].value
        return Variable("mint", result_matrix)

    def elem_mul_xx(self, first_operand, second_operand):
        return Variable("int", first_operand.value * second_operand.value)

    # TODO: add MV and VM

    def handle_and_operator(self, first_operand, second_operand):
        lhs = self.handleNode(first_operand)
        rhs = self.handleNode(second_operand)
        return Variable("bool", lhs.value and rhs.value)

    def handle_unary_operator(self, node):
        child = node.children[0]
        match node.value:
            case "'":
                return self.handle_matrix_transposition(child)
            case "!":
                return self.handle_negative(child)
            case ">>":
                return self.handle_cyclic_shift(child, is_left=False)
            case "<<":
                return self.handle_cyclic_shift(child)

    def handle_matrix_transposition(self, operand):
        op = self.handleNode(operand)
        if "m" not in op.type:
            raise ValueException
        result_matrix = []
        for i in range(len(op.value[0])):
            result_matrix.append([Variable("int", 0) for j in range(len(op.value))])
        result_matrix = [[Variable("int", op.value[j][i].value) for j in range(len(op.value))] for i in
                         range(len(op.value[0]))]
        return Variable("mint", result_matrix)

    def handle_negative(self, operand):
        op = self.handleNode(operand)
        op = TypeConverter().convert_type("bool", op)
        op.value = not op.value
        return op

    def handle_cyclic_shift(self, operand, is_left=True):
        op = self.handleNode(operand)
        arr_of_bin = deque([int(d) for d in str(bin(op.value))[2:]])
        if not is_left:
            arr_of_bin.rotate(1)
        else:
            arr_of_bin.rotate(-1)
        arr_of_bin = list(arr_of_bin)
        s = [str(i) for i in arr_of_bin]
        res = int("".join(s), 2)
        return Variable("int", res)

    def handle_assignment(self, node):
        # met something like a <- 5
        # a is decl_name
        decl_name = node.value.value
        if decl_name not in self.declaration_table[self.visibility_scope].keys():
            raise UndeclaredException
        try:
            # getting instance of class Variable using decl_name: var is Variable("type", value)
            var = self.declaration_table[self.visibility_scope][decl_name]
            new_value = node.children[0]
            match new_value.type:
                case NodeType.Expression.value:
                    new_value = self.handleNode(new_value)
                case NodeType.ListArgs.value:
                    new_value = self.handleNode(new_value)
                    new_value = self.make_variable_instance(new_value)
            self.assign_to_var(var, decl_name, new_value)
        except TypeException:
            ErrorHandler().raise_error(ErrorType.TypeError.value)
        pass

    def assign_to_var(self, var_instance, decl_name, new_value):
        var_type = var_instance.type
        new_value_type = new_value.type

        if "c" in var_type:
            raise TypeException
        if var_type == new_value_type.replace("c", ""):
            self.declaration_table[self.visibility_scope][decl_name] = Variable(var_type, new_value.value)
        elif var_type == "int" and new_value_type.replace("c", "") == "bool":
            self.declaration_table[self.visibility_scope][decl_name] = Variable(var_type, int(new_value.value))
        elif var_type == "bool" and new_value_type.replace("c", "") == "int":
            self.declaration_table[self.visibility_scope][decl_name] = Variable(var_type, bool(new_value.value))
        else:
            raise TypeException

    def handle_if(self, node):
        # if-node has children = [conditionChild, bodyChild]
        condition = self.handleNode(node.children[0])
        condition = TypeConverter().convert_type("bool", condition).value
        if condition:
            new_interpreter = JazzInterpreter()
            for key in self.declaration_table[self.visibility_scope].keys():
                new_interpreter.declaration_table[self.visibility_scope][key] = \
                    self.declaration_table[self.visibility_scope][key]
            new_interpreter.handleNode(node.children[1])
            try:
                for key in new_interpreter.declaration_table[self.visibility_scope].keys():
                    if key in self.declaration_table[self.visibility_scope]:
                        self.declaration_table[self.visibility_scope][key] = \
                            new_interpreter.declaration_table[self.visibility_scope][key]
            except Exception:
                pass

    def handle_for(self, node):
        # for-node has children: [variableChild, startChild, stopChild, forbodyChild]

        var_name = node.children[0].value
        start = self.handleNode(node.children[1]).value
        stop = self.handleNode(node.children[2]).value
        flag = False
        # check if iterate variable name from for-loop in declaration table
        # if it is, we will replace this var to Variable("int", value) until for-loop finish his work
        if var_name in self.declaration_table[self.visibility_scope].keys():
            flag = True
        try:
            var_copy = 0
            if flag:
                var_copy = self.declaration_table[self.visibility_scope][var_name]
            self.declaration_table[self.visibility_scope][var_name] = Variable("int", start)
            # directly for-loop
            while self.declaration_table[self.visibility_scope][var_name].value < stop:
                # create new interpreter and copy by value vars from declaration table
                new_interpreter = JazzInterpreter()
                for key in self.declaration_table[self.visibility_scope].keys():
                    new_interpreter.declaration_table[self.visibility_scope][key] = \
                        self.declaration_table[self.visibility_scope][key]
                new_interpreter.handleNode(node.children[3])
                # if values from MAIN declaration table have changed while working of NEW interpreter,
                # we have to change them in MAIN declaration table: loop through key in NEW interpreter declaration
                # table and look if key(var_name) is in MAIN declaration table
                # if it is not^ it means that current var_name was declared in inner scope, we skip it
                try:
                    for key in new_interpreter.declaration_table[self.visibility_scope].keys():
                        if key in self.declaration_table[self.visibility_scope]:
                            self.declaration_table[self.visibility_scope][key] = \
                                new_interpreter.declaration_table[self.visibility_scope][key]
                except Exception:
                    pass
                self.declaration_table[self.visibility_scope][var_name].value += 1
            # replace saved var back if needed
            if flag:
                self.declaration_table[self.visibility_scope][var_name] = var_copy
            else:
                del self.declaration_table[self.visibility_scope][var_name]
        except Exception:
            pass

    def handle_function_call(self, node):
        # node: • [Type: func_call - Value: calling function name]
        # self.func_table["calling function name"].children:
        # {'return_spec': • [Type: return_spec - Value: ], 'params': • [Type: parameters - Value: ], 'body': • [Type: sentence_list - Value: ]}
        # return specification and parameters dict keys are optional

        # firstly check was function declared or not and pull out needed info
        function_name = node.value
        if function_name not in self.func_table.keys():
            raise UndeclaredException
        func_declaration_node = self.func_table[function_name]
        return_specification_node = func_declaration_node.children.get("return_spec", None)
        parameters_node = func_declaration_node.children.get("params", None)
        body_node = func_declaration_node.children.get("body", None)

        # these var names of related type should be declared in func body
        # and vars to which to will assign also must have same type
        return_specification = dict()
        if return_specification_node is not None:
            help_arr = []
            self.extract_return_spec(return_specification_node, return_specification, help_arr)
            del help_arr

        # parameters that were declared
        declared_func_parameters = dict()
        if parameters_node is not None:
            self.extract_parameters(parameters_node, declared_func_parameters)
        # simple dictionary: if has no default parameter, value by key is None
        func_assigned_params = dict()
        for key in declared_func_parameters.keys():
            if isinstance(declared_func_parameters[key], Variable):
                _type = declared_func_parameters[key].type
                _val = _type = declared_func_parameters[key].value
                func_assigned_params[key] = Variable(_type, _val)
            else:
                func_assigned_params[key] = None

        # values, that we pass to the func
        passed_values = node.children.get("call", None)

        # parameters with values that will be used inside function body
        # elements from dict will be overridden if it needed
        if passed_values is not None:
            self.assign_passed_values(func_assigned_params, passed_values)
        if self.has_missing_arguments(func_assigned_params):
            print("[DEBUG] Missing args error")


        # pass this new params with passed values into new declaration table
        # start new sub-interpreter for func body

        # our return specifications were saved before
        # loop through keys of sub-interpreter declaration table and check if return-values are contained

        # assign

        pass

    # transforms info about return specification from syntax tree into dict: {"name1": "type1", ...}
    def extract_return_spec(self, node, result_dict, flag):
        # node: Type: return_spec
        # Children: [• [Type: return_spec - Value: ], • [Type: type - Value: int], 'res2'] or just [• [Type: type - Value: int], 'res2']
        children = node.children
        # flag here is array because i had difficulties with implementing this algorithms on python
        # if it was bool, then during coming back after diving maximum deep of recursion, this flag doesnt change

        # one moment it will be 2 elements in children
        # or we are coming back after diving in recursion
        while len(children) != 2 and len(flag) == 0:
            return_var_type = children[1].value
            return_var_name = children[2]
            if result_dict.get(return_var_name):
                raise RedeclarationException
            result_dict[return_var_name] = return_var_type
            self.extract_return_spec(children[0], result_dict, flag)
        # finish if all elements are collected
        if len(flag) != 0:
            return
        # when first condition about consisting of 2 elements worked, we have to add sth in list
        # to check a moment that our algo should finish
        result_dict[children[1]] = children[0].value
        flag.append(0)

    def extract_parameters(self, node, result_dict):
        a = 5
        # """parameters : parameters COMMA parameter
        #               | parameter"""
        # so we add handled expression and dive into next expression list
        # it will continue until there are no more expressions_list in grammar
        # so there will be only one child
        if len(node.children) == 2:
            self.add_parameter_info(node.children[1], result_dict)
            self.extract_parameters(node.children[0], result_dict)
        else:
            self.add_parameter_info(node.children[0], result_dict)

    def add_parameter_info(self, node, result_dict):
        # possible parameter's node children
        # [• (Type: type - Value: vint), 'par2']
        # [• (Type: type - Value: int), 'par1', • (Type: constant - Value: 0)]
        param_var_name = node.children[1]
        param_var_declared_type = node.children[0].value
        if len(node.children) == 2:
            result_dict[param_var_name] = param_var_declared_type
        else:
            val = self.handleNode(node.children[2])
            result_dict[param_var_name] = self.configure_declaration(param_var_declared_type, val)

    def has_missing_arguments(self, dict_assigned):
        for key in dict_assigned.keys():
            if key is None:
                return True
        return False

    def assign_passed_values(self, assign_dict, node):
        configured_values = self.get_configured_values_from_call_list(node)[::-1]

        # for elem in elems in arr assign to params
        # (need mb array for numeration of params)
        pass

    # returns reversed array of passed values
    def get_configured_values_from_call_list(self, node):
        # """call_list : call_list COMMA expression
        #                     | expression"""
        result = []
        if len(node.children) == 2:
            result.append(self.handleNode(node.children[1]))
            add = self.get_configured_values_from_call_list(node.children[0])
            result += add
        else:
            result.append(self.handleNode(node.children[0]))
        return result




if __name__ == '__main__':
    interpreter = JazzInterpreter()
    s = f'/Users/jazzdiluffy/Desktop/JazzInterpreter/Testing/test_interpreter_smth.txt'
    f = open(s, "r")
    program = f.read()
    f.close()
    interpreter.start(program)
