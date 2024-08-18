from __future__ import annotations
import argparse
from pathlib import Path
import sys
from typing import Sequence
from rst_fast_parse.parse import parse_string

def lint(sys_args: Sequence[str] | None=None, /) -> None:
    parser = argparse.ArgumentParser(description='Simple parser CLI')
    parser.add_argument('file_paths', metavar='PATH or -', nargs='+', help='Path to the file to parse or - for stdin')
    parser.add_argument('--print-ast', action='store_true', help='Print the AST after parsing')
    args = parser.parse_args(sys_args)
    paths: list[str] = args.file_paths
    print_ast: bool = args.print_ast
    num_diagnostics = 0
    for path in paths:
        if path == '-':
            repr_path = '<stdin>'
            content: str = sys.stdin.read()
            elements, diagnostics = parse_string(content)
        else:
            repr_path = path
            if not Path(path).is_file():
                print(f'{repr_path}: No such file')
                num_diagnostics += 1
                continue
            elements, diagnostics = parse_string(Path(path).read_text('utf8'))
        if print_ast:
            print(elements.debug_repr().rstrip())
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