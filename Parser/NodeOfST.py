class NodeOfST:
    def __init__(self, node_type, value, children=None):
        if children is None:
            children = []

        self.type = node_type
        self.value = value
        self.children = children

    def __repr__(self):
        if isinstance(self.value, NodeOfST):
            return "• [" + f"Type: {self.type} - Value: STNode with type: {self.value.children}" + "]"
        return "• [" + f"Type: {self.type} - Value: {self.value}" + "]"

    def __str__(self, level=0):
        result = "\t" * level + repr(self) + "\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result


if __name__ == '__main__':
    root = NodeOfST(node_type="type0", value=0)
    child1 = NodeOfST(node_type="type1", value=1)
    child2 = NodeOfST(node_type="type2", value=2)
    child1child2 = NodeOfST(node_type="type12", value=12)
    child1child1 = NodeOfST(node_type="type11", value=11)
    child2child1 = NodeOfST(node_type="type21", value=21)
    child2child2 = NodeOfST(node_type="type22", value=22)
    child2child2child1 = NodeOfST(node_type="type221", value=221)
    root.children = [child1, child2]
    child1.children = [child1child1, child1child2]
    child2.children = [child2child1, child2child2]
    child2child2.children = [child2child2child1]

    print(root)
