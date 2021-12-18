from Variable import Variable


class TypeConverter:
    def __init__(self):
        pass

    def convert_type(self, declared_type, value):
        if declared_type == value.type:
            return value
        elif declared_type == "int" and value.type == "bool":
            return self.convert_bool_to_int(value)
        elif declared_type == "bool" and value.type == "int":
            return self.convert_int_to_bool(value)
        elif value.type in declared_type:
            return Variable(declared_type, value.value)

    def convert_bool_to_int(self, value):
        if not value.value:
            return Variable("int", 0)
        return Variable("int", 1)

    def convert_int_to_bool(self, value):
        if value.value == 0:
            return Variable("bool", False)
        return Variable("bool", True)