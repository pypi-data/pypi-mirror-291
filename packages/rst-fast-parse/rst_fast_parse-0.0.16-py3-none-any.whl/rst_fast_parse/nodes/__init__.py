from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, Callable, Iterable
if TYPE_CHECKING:
    from rst_fast_parse.nodes.block import BlockNodeProtocol

class WalKChildrenCallback(Enum):
    """A callback for the walk_children function."""
    Continue = 0
    'Continue walking the tree.'
    SkipSelfAndChildren = 1
    "Skip the current node and it's children of the current node."
    SkipChildren = 2
    'Skip the children of the current node.'
    SkipSiblings = 3
    "Skip preceding siblings of the current node\n    (after yielding current node's children).\n    "
    SkipChildrenAndSiblings = 4
    'Skip the children and siblings of the current node.'
    SkipSelfAndChildrenAndSiblings = 5
    'Skip the children and siblings of the current node.'
    Stop = 6
    'Stop walking the tree (before yielding current node).'

def walk_children(node: BlockNodeProtocol, callback: Callable[[BlockNodeProtocol], WalKChildrenCallback] | None=None) -> Iterable[BlockNodeProtocol]:
    """Recursively yield children of the node.

    This is a depth-first traversal.

    :param node: The root node to start from.
    :param callback: An optional callback to control the traversal.
    """
    for child in node.children():
        result = callback(child) if callback is not None else WalKChildrenCallback.Continue
        if result == WalKChildrenCallback.Continue:
            yield child
            yield from walk_children(child, callback)
            continue
        if result == WalKChildrenCallback.Stop:
            raise StopIteration
        if result == WalKChildrenCallback.SkipSelfAndChildrenAndSiblings:
            break
        if result == WalKChildrenCallback.SkipSiblings:
            yield child
            yield from walk_children(child, callback)
            break
        if result == WalKChildrenCallback.SkipSelfAndChildren:
            continue
        if result == WalKChildrenCallback.SkipChildren:
            yield child
            continue
        if result == WalKChildrenCallback.SkipChildrenAndSiblings:
            yield child
            break
        raise RuntimeError(f'Unknown callback result: {result!r}')

def walk_line_inside(initial: BlockNodeProtocol, line: int) -> Iterable[BlockNodeProtocol]:
    """Yield all block nodes that contain the given line, in order of nesting.

    :param initial: The initial node to start from.
    :param line: The line to search for (index-based, starting from 0).

    Note, the initial node will not be yielded.

    Also note, that it is assumed that all children of an node are in order of appearance,
    and that the line ranges of the blocks do not overlap,
    i.e. that we can halt the search when we reach an node
    with a bottom line that is greater than the target line.
    """

    def _callback(node: BlockNodeProtocol) -> WalKChildrenCallback:
        if node.line_range[0] <= line <= node.line_range[1]:
            return WalKChildrenCallback.Continue
        if node.line_range[1] > line:
            return WalKChildrenCallback.SkipSelfAndChildrenAndSiblings
        return WalKChildrenCallback.SkipSelfAndChildren
    yield from walk_children(initial, _callback)