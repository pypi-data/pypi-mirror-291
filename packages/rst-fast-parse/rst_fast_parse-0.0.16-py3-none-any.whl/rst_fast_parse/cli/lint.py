from __future__ import annotations
import argparse
from pathlib import Path
import sys
from typing import Sequence
from rst_fast_parse.parse import parse_string

def lint(sys_args: Sequence[str] | None=None, /) -> None:
    parser = argparse.ArgumentParser(description='Simple parser CLI')
    parser.add_argument('file_paths', metavar='PATH or -', nargs='+', help='Path to the file to parse or - for stdin')
    parser.add_argument('--no-inline', action='store_true', help='Do not parse inline blocks')
    parser.add_argument('--print-ast', action='store_true', help='Print the AST after parsing')
    parser.add_argument('--ast-maps', action='store_true', help='Add source maps to the AST')
    args = parser.parse_args(sys_args)
    paths: list[str] = args.file_paths
    parse_inlines: bool = not args.no_inline
    print_ast: bool = args.print_ast
    ast_sourcemaps: bool = args.ast_maps
    num_diagnostics = 0
    for path in paths:
        if path == '-':
            repr_path = '<stdin>'
            content: str = sys.stdin.read()
            nodes, diagnostics = parse_string(content, parse_inlines=parse_inlines, inline_sourcemaps=ast_sourcemaps)
        else:
            repr_path = path
            if not Path(path).is_file():
                print(f'{repr_path}: No such file')
                num_diagnostics += 1
                continue
            nodes, diagnostics = parse_string(Path(path).read_text('utf8'), parse_inlines=parse_inlines, inline_sourcemaps=ast_sourcemaps)
        if print_ast:
            print(nodes.debug_repr(show_map=ast_sourcemaps).rstrip())
            print('')
        for diagnostic in diagnostics:
            num_diagnostics += 1
            print(f'{repr_path}:{diagnostic}')
    if num_diagnostics:
        print('')
        print(f'Found {num_diagnostics} error.')
        raise SystemExit(1)
    else:
        print('All checks passed!')
if __name__ == '__main__':
    lint()