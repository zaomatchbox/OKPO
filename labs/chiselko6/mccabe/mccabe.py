import ast
from graphviz import Graph, Digraph


class Node:

    def __init__(self, name, type, is_root=False, nodes=None):
        self._name = name
        self.type = type
        self.is_root = is_root
        self._nodes = nodes or []
        self._parent = None

    def add_node(self, node):
        self._nodes.append(node)
        node.parent = self.parent

    @property
    def nodes(self):
        return iter(self._nodes)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class VizGraphNode:

    def __init__(self, lineno, type):
        self.type = type
        self.id = f'#{lineno}_{type}'
        self._nodes = []

    def add_node(self, node):
        self._nodes.append(node)

    @property
    def nodes(self):
        return iter(self._nodes)

    def viz(self, g, visited=None):
        visited = visited or set()
        if self.id in visited:
            return g
        visited.add(self.id)
        for ch in self.nodes:
            g.edge(self.id, ch.id)
            ch.viz(g, visited)
        return g

    def dfs_vertices(self, visited):
        if self.id in visited:
            return
        visited.add(self.id)
        for ch in self.nodes:
            ch.dfs_vertices(visited)

    def dfs_edges(self, visited):
        for ch in self.nodes:
            edge = (self.id, ch.id)
            if edge not in visited:
                visited.add(edge)
                ch.dfs_edges(visited)
        return len(visited)

    def get_mccabe(self, visited=None):
        v_visited, e_visited = set(), set()
        self.dfs_vertices(v_visited)
        self.dfs_edges(e_visited)
        vertices, edges = len(v_visited), len(e_visited)
        return edges - vertices + 2

    def __eq__(self, value):
        return self.id == value.id

    def __neq__(self, value):
        return NotImplemented


class VizGraph:

    def __init__(self, root):
        self.root = root
        self.tails = [root]

    def add_graph(self, graph):
        for tail in self.tails:
            tail.add_node(graph.root)
        self.tails = graph.tails

    def reset_tail(self):
        self.tails = [self.root]

    def add_tail(self, node):
        self.tails.append(node)

    def add_graph_to_root(self, graph):
        self.root.add_node(graph.root)
        if len(self.tails) == 1 and self.tails[0] == self.root:
            self.tails = graph.tails
        else:
            self.tails.extend(graph.tails)

    @property
    def id(self):
        return self.root.id

    def viz(self, g):
        return self.root.viz(g)

    def get_mccabe(self):
        return self.root.get_mccabe()


class VizASTVisitor:

    def run(self, tree):
        self.graph = self.dispatch(tree)

    def dispatch(self, ast_node):
        classname = ast_node.__class__.__name__
        if hasattr(self, f'visit{classname}'):
            graph = getattr(self, f'visit{classname}')(ast_node)
        else:
            if isinstance(ast_node, ast.stmt):
                graph = self.visitSimpleStatement(ast_node)
            else:
                graph = None
        return graph

    def visitSimpleStatement(self, node):
        return VizGraph(VizGraphNode(node.lineno, 'stmt'))

    def visitLoop(self, node):
        graph = VizGraph(VizGraphNode(node.lineno, 'loop'))
        for ch in node.body:
            graph.add_graph(self.dispatch(ch))
        assert len(graph.tails) == 1
        graph.add_graph(graph)
        graph.reset_tail()
        return graph

    def visitIf(self, node):
        if_graph = None
        for ch in node.body:
            if if_graph is None:
                if_graph = self.dispatch(ch)
            else:
                if_graph.add_graph(self.dispatch(ch))
        graph = VizGraph(VizGraphNode(node.lineno, 'condition'))
        graph.add_graph_to_root(if_graph)
        if node.orelse:
            else_graph = None
            for ch in node.orelse:
                if else_graph is None:
                    else_graph = self.dispatch(ch)
                else:
                    else_graph.add_graph(self.dispatch(ch))
            graph.add_graph_to_root(else_graph)
        else:
            graph.add_tail(graph.root)
        return graph

    def visitFunctionDef(self, node):
        graph = VizGraph(VizGraphNode(node.lineno, 'func'))
        for ch in node.body:
            graph.add_graph(self.dispatch(ch))
        return graph

    def visitClassDef(self, node):
        graph = VizGraph(VizGraphNode(node.lineno, 'class'))
        for ch in ast.iter_child_nodes(node):
            graph.add_graph(self.dispatch(ch))
        return graph

    def visitModule(self, node):
        graph = VizGraph(VizGraphNode(0, 'module'))
        for ch in ast.iter_child_nodes(node):
            graph.add_graph(self.dispatch(ch))
        return graph

    def viz(self):
        g = Digraph('G', format='png', engine='neato')
        return self.graph.viz(g)

    def get_mccabe(self):
        return self.graph.get_mccabe()

    def visitWith(self, node):
        graph = VizGraph(VizGraphNode(node.lineno, 'with'))
        for ch in node.body:
            graph.add_graph(self.dispatch(ch))
        return graph

    visitAsyncWith = visitWith
    visitAsyncFunctionDef = visitFunctionDef
    # visitTry = visitTryExcept
    visitAsyncFor = visitFor = visitWhile = visitLoop


class ASTVisitor:

    def __init__(self):
        self.root = Node('__main__', 'root', is_root=True)

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
        return [Node('simple statement', 'stmt')]

    def visitLoop(self, node):
        root = Node('loop', 'loop')
        for ch in ast.iter_child_nodes(node):
            for n in self.dispatch(ch):
                root.add_node(n)
        return [root]

    def visitIf(self, node):
        if_root = Node('if', 'if')
        for ch in node.body:
            for n in self.dispatch(ch):
                if_root.add_node(n)
        res = [if_root]
        if node.orelse:
            else_root = Node('else', 'else')
            for ch in node.orelse:
                for n in self.dispatch(ch):
                    else_root.add_node(n)
            res.append(else_root)
        return res

    def visitFunctionDef(self, node):
        root = Node('def', 'function')
        for ch in ast.iter_child_nodes(node):
            for n in self.dispatch(ch):
                root.add_node(n)
        return [root]

    def visitClassDef(self, node):
        root = Node('class', 'class', )
        for ch in ast.iter_child_nodes(node):
            for n in self.dispatch(ch):
                root.add_node(n)
        return [root]

    def visitModule(self, node):
        root = Node('module', 'module')
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

    def visitWith(self, node):
        root = Node('with', 'with')
        for ch in node.body:
            for n in self.dispatch(ch):
                root.add_node(n)
        return [root]

    visitAsyncWith = visitWith
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
    if x % 2 == 0 and y > 0:
        if c > 0:
            print(a)
        y = 0
    else:
        y = 1
        lala = 3
    x += 1
p = True

with a:
    a += 3
"""


def run_ast():
    tree = compile(CODE, 'lala', 'exec', ast.PyCF_ONLY_AST)
    visitor = ASTVisitor()
    visitor.run(tree)
    visitor.print()
    print(visitor.get_mccabe())


def run_viz():
    tree = compile(CODE, 'lala', 'exec', ast.PyCF_ONLY_AST)
    visitor = VizASTVisitor()
    visitor.run(tree)
    visitor.viz().view()
    print(visitor.get_mccabe())


if __name__ == '__main__':
    run_ast()
    run_viz()
