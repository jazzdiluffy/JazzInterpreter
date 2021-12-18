from Parser.JazzParser import *
from Parser.NodeSTBuilder import NodeType
from ErrorHandler import *
from TypeConverter import TypeConverter
from Variable import Variable



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
                    pass
                except UnexpectedTypeException:
                    pass
            case NodeType.Assignment.value:
                pass
            case NodeType.Expression.value:
                return self.handleNode(node.children[0])
            case NodeType.ListExpressions.value:
                pass
            case NodeType.Variable.value:
                pass
            case NodeType.Constant.value:
                return Variable("bool", node.value) if node.value == "true" or node.value == "false" else Variable("int", node.value)
            case NodeType.BinaryOperator.value:
                pass
            case NodeType.UnaryOperator.value:
                pass
            case NodeType.If.value:
                pass
            case NodeType.For.value:
                pass
            case NodeType.FuncDeclaration.value:
                pass
            case NodeType.Function.value:
                pass
            case NodeType.ReturnSpecification.value:
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
                args_list = self.configure_list(self.handleNode(declaration_value))
                self.add_to_declare_table(decl_type, declaration_name, args_list)

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
            return self.configure_variable(type, value)
        elif "v" in type and "v" in value.type:
            return self.configure_vector(type, value)
        elif "m" in type and "m" in value.type:
            return self.configure_matrix(type, value)
        else:
            raise UnexpectedTypeException

    def configure_variable(self, type, value):
        return TypeConverter().convert_type(type, value)

    def configure_vector(self, type, value):
        elems_type = type[1:]
        converted_vector_values = [TypeConverter().convert_type(elems_type, elem) for elem in value.value]
        return Variable(type, converted_vector_values)

    def configure_matrix(self, type, value):
        elems_type = type[1:]
        rectangular_matrix_length = len(value[0])
        converted_matrix_elems = value.value
        # check is matrix rectangular
        for i in range(len(value)):
            if len(value[i]) != rectangular_matrix_length:
                raise ValueException
        for i in range(len(value)):
            converted_matrix_elems[i] = [TypeConverter().convert_type(elems_type, elem) for elem in converted_matrix_elems[i]]
        return Variable(type, converted_matrix_elems)

    def configure_list(self, value):
        pass


if __name__ == '__main__':
    interpreter = JazzInterpreter()
    s = f'/Users/jazzdiluffy/Desktop/JazzInterpreter/Testing/test_interpreter_declaration.txt'
    f = open(s, "r")
    program = f.read()
    f.close()
    interpreter.start(program)
