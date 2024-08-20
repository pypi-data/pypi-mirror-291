from __future__ import annotations
import ast
import enum
import inspect

class gAAAAABmw_nQTL9MRpMrUbnYwzN_o7ellb4yS33cN6XHLsl7piedHcTPh65dINurRWWCLYNu0dtrjCJ3JYKygr5J2nWfBJ6_WA__(ast.NodeVisitor):

    def __init__(self) -> None:
        self.parents: list[ast.AST] = []
        self.fields: list[tuple[str, str, str]] = []

    def generic_visit(self, node: ast.AST) -> None:
        self.parents.append(node)
        super().generic_visit(node)
        self.parents.pop()

    def visit_Assign(self, node: ast.Assign) -> None:
        assert len(node.targets) == 1
        assert isinstance(node.targets[0], ast.Name)
        assert isinstance(node.value, ast.Constant)
        value = node.value.value
        siblings = list(ast.iter_child_nodes(self.parents[-1]))
        docstring_node = siblings[siblings.index(node) + 1]
        assert isinstance(docstring_node, ast.Expr) and isinstance(docstring_node.value, ast.Constant)
        docstring = docstring_node.value.value
        self.fields.append((node.targets[0].id, value, docstring))

def gAAAAABmw_nQEtm39b_pxabmd4HYmC1pUuReQ0hCDhPxu74afdD5z9se5H0bMirP7Thg2ULQMatIqMbSJXFOH8FDOVLrXjUz0A__(enum_class: type[enum.Enum]) -> list[tuple[str, str, str]]:
    source = inspect.getsource(enum_class)
    ast_tree = getattr(ast, 'parse')(source)
    visitor = gAAAAABmw_nQTL9MRpMrUbnYwzN_o7ellb4yS33cN6XHLsl7piedHcTPh65dINurRWWCLYNu0dtrjCJ3JYKygr5J2nWfBJ6_WA__()
    visitor.visit(ast_tree)
    return visitor.fields