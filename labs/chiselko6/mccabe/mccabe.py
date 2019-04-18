import ast


class Node:

    def __init__(self, name, type, is_root=False, is_block=False, nodes=None):
        self._name = name
        self.type = type
        self.is_root = is_root
        self.nodes = nodes or []
        self._parent = None
        is_block = is_block or is_root
        if is_block:
            self._block_parent = self
        else:
            self._block_parent = None

    def add_node(self, node):
        self.nodes.append(node)
        node.parent = self.parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def block_parent(self):
        if self._block_parent is not None:
            return self._block_parent
        self._block_parent = self.parent.block_parent
        return self._block_parent

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class VizGraphNode:

    def __init__(self, name, type):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)


class ASTVisitor:

    def __init__(self):
        self.root = Node('__main__', 'root', is_root=True)
        self.current_node = self.root

    def dispatch_list(self, node_list):
        for node in node_list:
            self.dispatch(node)

    def dispatch_inside(self, node):
        for node in ast.iter_child_nodes(node):
            self.dispatch(node)

    def move(self, node):
        self.current_node.add_node(node)
        self.current_node = node

    def run(self, tree):
        nodes = self.dispatch(tree)
        for n in nodes:
            self.root.add_node(n)

    def dispatch(self, ast_node):
        classname = ast_node.__class__.__name__
        if hasattr(self, f'visit{classname}'):
            nodes = getattr(self, f'visit{classname}')(ast_node)
        else:
            if isinstance(ast_node, ast.stmt):
                nodes = self.visitSimpleStatement(ast_node)
            else:
                nodes = []
        return nodes

    def visitSimpleStatement(self, node):
        print('simple statement', node)
        return [Node('simple statement', 'stmt')]

    def visitLoop(self, node):
        print('loop', node)
        root = Node('loop', 'loop', is_block=True)
        for ch in ast.iter_child_nodes(node):
            for n in self.dispatch(ch):
                root.add_node(n)
        return [root]

    def visitIf(self, node):
        print('if', node)
        if_root = Node('if', 'if', is_block=True)
        for ch in node.body:
            for n in self.dispatch(ch):
                if_root.add_node(n)
        else_root = Node('else', 'else', is_block=True)
        for ch in node.orelse:
            for n in self.dispatch(ch):
                else_root.add_node(n)
        return [if_root, else_root]

    def visitFunctionDef(self, node):
        print('def', node)
        root = Node('def', 'function', is_block=True)
        for ch in ast.iter_child_nodes(node):
            for n in self.dispatch(ch):
                root.add_node(n)
        return [root]

    def visitClassDef(self, node):
        print('class', node)
        root = Node('class', 'class', is_block=True)
        for ch in ast.iter_child_nodes(node):
            for n in self.dispatch(ch):
                root.add_node(n)
        return [root]

    def visitModule(self, node):
        print('module', node)
        root = Node('module', 'module', is_block=True)
        for ch in ast.iter_child_nodes(node):
            for n in self.dispatch(ch):
                root.add_node(n)
        return [root]

    def print(self, node=None, offset=0):
        node = node or self.root
        print(' ' * offset, node.name)
        for ch in node.nodes:
            self.print(ch, offset + 4)

    def get_mccabe(self, node=None):
        node = node or self.root
        value = 0
        if node.type == 'if' or node.type == 'else' or node.type == 'loop':
            value = 1
        else:
            value = 0
        for ch in node.nodes:
            value += self.get_mccabe(ch)
        return value

    # visitAsyncWith = visitWith
    visitAsyncFunctionDef = visitFunctionDef
    # visitTry = visitTryExcept
    visitAsyncFor = visitFor = visitWhile = visitLoop


CODE = """
def foo(a, b=10):
  return a + b


class A:

    def bar(self, c):
        c += 10
        return c


while x < 100:
    if x % 2 == 0:
        y = 0
    else:
        y = 1
        lala = 3
    x += 1
p = True
"""


if __name__ == '__main__':
    tree = compile(CODE, 'lala', 'exec', ast.PyCF_ONLY_AST)
    visitor = ASTVisitor()
    visitor.run(tree)
    visitor.print()
    print(visitor.get_mccabe())
