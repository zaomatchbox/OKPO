import ast
from ast import NodeVisitor


def read_sample(filename="cases/1.py"):
    result = ""
    with open(filename, "r") as file:
        result = file.read()
    return result


class Visitor(NodeVisitor):

    def __init__(self, node):
        super().__init__()
        print(node)
        self.root_node = node
        self.score = 0
        self.edges = []
        self.nodes = []  # list of nodes
        self.results = []
        self.process_root_node()

    def visit(self, node):
        """Visit a node."""
        print(node)
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def process_root_node(self):
        for child in ast.iter_child_nodes(node):
            print(child.__class__.__name__)
            score = self.visit(child)
            if score:
                self.score += score
            else:
                print(child.__class__.__name__, 'None')

    def visit_If(self, node):
        print('visit if')
        score = len(node.test.values)
        if len(node.orelse) and node.orelse[0].__class__.__name__ == "If":
            score += self.visit_If(node.orelse[0])
        for child in ast.iter_child_nodes(node):
            print('if childs;', child.__class__.__name__)

        print(score)
        return score

    def visit_FunctionDef(self, node):
        print('func', node)
        # score = Visitor(node).score
        return 1

    def __process_decision_point(self, node):
        self.score += 1
        return 1

    visit_For = visit_While = __process_decision_point


if __name__ == "__main__":
    node = ast.parse(read_sample(filename="cases/2.py"))
    # print(node._attributes)
    visitor = Visitor(node)
    print(visitor.score)
