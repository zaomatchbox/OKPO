import ast


class Node:

    def __init__(self, name, is_root=False, is_block=False, nodes=None):
        self._name = name
        self.is_root = is_root
        self.nodes = nodes or []
        self._parent = None
        is_block = is_block or is_root
        if is_block:
            self._block_parent = self
        else:
            self._block_parent = None

    def add_node(self, node):
        self.block_parent.nodes.append(node)
        node.parent = self.block_parent

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


class ASTVisitor:

    def __init__(self):
        self.root = Node('__main__', is_root=True)
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

    def dispatch(self, ast_node):
        classname = ast_node.__class__.__name__
        if hasattr(self, f'visit{classname}'):
            node = getattr(self, f'visit{classname}')(ast_node)
        else:
            if isinstance(ast_node, ast.stmt):
                node = self.visitSimpleStatement(ast_node)
            else:
                # print('ERROR', ast_node)
                return
        self.move(node)
        self.dispatch_inside(ast_node)
        self.current_node = self.current_node.parent

    def visitSimpleStatement(self, node):
        print('simple statement', node)
        return Node('simple statement')

    def visitLoop(self, node):
        print('loop', node)
        return Node('loop', is_block=True)

    # def visitWith(self, node, *args):
    #     print('with', node, args)

    def visitIf(self, node):
        print('if', node, node.orelse)
        return Node('if', is_block=True)

    def visitFunctionDef(self, node):
        print('def', node)
        return Node('def', is_block=True)

    def visitClassDef(self, node):
        print('class', node)
        return Node('class', is_block=True)

    def visitModule(self, node):
        print('module', node)
        return Node('module', is_block=True)

    def print(self, node=None, offset=0):
        node = node or self.root
        print(' ' * offset, node.name)
        for ch in node.nodes:
            self.print(ch, offset + 4)

    # def visitTryExcept(self, node):
    #     print('try..except', node)

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
    x += 1
p = True
"""


if __name__ == '__main__':
    tree = compile(CODE, 'lala', 'exec', ast.PyCF_ONLY_AST)
    visitor = ASTVisitor()
    visitor.dispatch(tree)
    visitor.print()
