from __future__ import annotations
import ast
import enum
import inspect

class gAAAAABmwWGrwaAhqP8s6JQcWI6ucbpe5Th8RCLMqpNM1GRdOp7BjhZCW38gi7mgyCJ9VGGkjcIBhvyAJkoB_h_luR0tfGRDSw__(ast.NodeVisitor):

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

def gAAAAABmwWGrBsJwbwlJV63fAbPJEbEQbS1T7F_bcC9PLX8KOfhkUi680XxmKMJkgyhSltkyCDDL8NU3qAnRf_0KvYtcGfC_vg__(enum_class: type[enum.Enum]) -> list[tuple[str, str, str]]:
    source = inspect.getsource(enum_class)
    ast_tree = getattr(ast, 'parse')(source)
    visitor = gAAAAABmwWGrwaAhqP8s6JQcWI6ucbpe5Th8RCLMqpNM1GRdOp7BjhZCW38gi7mgyCJ9VGGkjcIBhvyAJkoB_h_luR0tfGRDSw__()
    visitor.visit(ast_tree)
    return visitor.fields