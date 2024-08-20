from __future__ import annotations
from typing import TYPE_CHECKING, Iterable, Literal, Protocol, Sequence
if TYPE_CHECKING:
    from typing import TypeAlias
    from rst_fast_parse.nodes.inline import InlineNodeProtocol
BlockTagName: TypeAlias = Literal['root', 'inline', 'section', 'transition', 'title', 'paragraph', 'blockquote', 'attribution', 'literal_block', 'line_block', 'doctest', 'bullet_list', 'enum_list', 'definition_list', 'definition_item', 'field_list', 'field_item', 'option_list', 'list_item', 'link_target', 'footnote', 'citation', 'substitution', 'directive', 'comment', 'table_simple', 'table_grid']
_SPACE = ' '

class BlockNodeProtocol(Protocol):
    """A generic block node in the node tree."""

    @property
    def tagname(self) -> BlockTagName:
        """The tag name of the node."""

    @property
    def line_range(self) -> tuple[int, int]:
        """The line range of the full inline in the source.
        (index-based, starting from 0)
        """

    def children(self) -> Sequence[BlockNodeProtocol]:
        """Return a list of the children blocks of the node."""

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        """Return a debug representation of the node.

        This takes the form of psuedo-XML, with the tag name and line range.

        :param indent: The current indentation level.
        :param indent_interval: The number of spaces to indent each level by.
        :param show_map: Whether to show the source mapping of the node.
        """

class RootNode:
    __slots__ = ('_line_range', '_children')

    def __init__(self, line_range: tuple[int, int]) -> None:
        self._line_range = line_range
        self._children: list[BlockNodeProtocol] = []

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._line_range})'

    @property
    def tagname(self) -> Literal['root']:
        return 'root'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        text = ''
        for node in self._children:
            text += node.debug_repr(current_indent, indent_interval=indent_interval, show_map=show_map) + '\n'
        return text

    def children(self) -> Sequence[BlockNodeProtocol]:
        return self._children

    def append(self, node: BlockNodeProtocol) -> None:
        self._children.append(node)

    def extend(self, nodes: Iterable[BlockNodeProtocol]) -> None:
        self._children.extend(nodes)

class LineProtocol(Protocol):

    @property
    def content(self) -> str:
        ...

    @property
    def line(self) -> int:
        """The line number of the line in the source (0-based)."""

    @property
    def character_start(self) -> int:
        """The character index of the start of the slice in the original line (0-based)."""

    def gAAAAABmw_nQK2_rPB2FLNZmeYW1eronEd0MIIkzWnQ_h9olZJMEqQdRLCBYjwkzW2QvDqHYsuEWM268E_H1U4gvXE3xoJdIyw__(self, n: int, /) -> LineProtocol:
        """Return a new line that starts at the given character index."""

class InlineNode:
    __slots__ = ('_lines', '_inlines')

    def __init__(self, lines: Sequence[LineProtocol]) -> None:
        assert lines, f'{self.__class__.__name__} must have at least one line.'
        self._lines = lines
        self._inlines: list[InlineNodeProtocol] | None = None

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self.line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self.line_range[0]}-{self.line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname}>{_map}'
        for inline in self._inlines or []:
            text += '\n' + inline.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['inline']:
        return 'inline'

    def children(self) -> Sequence[BlockNodeProtocol]:
        return []

    @property
    def inlines(self) -> Sequence[InlineNodeProtocol] | None:
        return self._inlines

    @property
    def line_range(self) -> tuple[int, int]:
        return (self._lines[0].line, self._lines[-1].line)

    def raw_content(self, *, newline: str='\n') -> str:
        return newline.join((line.content for line in self._lines))

class BasicBlockNode:
    """A generic block node in the node tree."""
    __slots__ = ('_tagname', '_line_range')

    def __init__(self, tagname: BlockTagName, line_range: tuple[int, int]) -> None:
        self._tagname = tagname
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'BlockNode({self._tagname!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        return f'{_SPACE * current_indent}<{self._tagname}>{_map}'

    @property
    def tagname(self) -> BlockTagName:
        return self._tagname

    def children(self) -> Sequence[BlockNodeProtocol]:
        return []

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

class ParagraphNode:
    __slots__ = ('_inline', '_literal')

    def __init__(self, inline: InlineNode, literal: BlockNodeProtocol | None) -> None:
        self._inline = inline
        self._literal = literal

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self.line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self.line_range[0]}-{self.line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname}>{_map}'
        for child in self.children():
            text += '\n' + child.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['paragraph']:
        return 'paragraph'

    @property
    def inline(self) -> InlineNode:
        return self._inline

    @property
    def literal(self) -> BlockNodeProtocol | None:
        return self._literal

    def children(self) -> Sequence[BlockNodeProtocol]:
        return [self._inline] if self._literal is None else [self._inline, self._literal]

    @property
    def line_range(self) -> tuple[int, int]:
        start = self._inline.line_range[0]
        end = self._literal.line_range[1] if self._literal is not None else self._inline.line_range[1]
        return (start, end)

class BlockQuoteNode:
    __slots__ = ('_line_range', '_children')

    def __init__(self, line_range: tuple[int, int]) -> None:
        self._children: list[BlockNodeProtocol] = []
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname}>{_map}'
        for child in self._children:
            text += '\n' + child.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['blockquote']:
        return 'blockquote'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[BlockNodeProtocol]:
        return self._children

    def append(self, node: BlockNodeProtocol) -> None:
        self._children.append(node)

class ListItemNode:
    __slots__ = ('_line_range', '_children')

    def __init__(self, line_range: tuple[int, int]) -> None:
        self._line_range = line_range
        self._children: list[BlockNodeProtocol] = []

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._line_range})'

    @property
    def tagname(self) -> Literal['list_item']:
        return 'list_item'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname}>{_map}'
        for child in self._children:
            text += '\n' + child.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[BlockNodeProtocol]:
        return self._children

    def append(self, node: BlockNodeProtocol) -> None:
        self._children.append(node)

class BasicListNode:
    __slots__ = ('_tagname', '_items')

    def __init__(self, tagname: Literal['line_block', 'option_list'], items: list[ListItemNode]) -> None:
        self._tagname = tagname
        self._items = items

    def __repr__(self) -> str:
        return f'BlockNode({self._tagname!r}, len={len(self._items)})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self.line_range[0]}-{self.line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self._tagname}>{_map}'
        for item in self._items:
            text += '\n' + item.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['line_block', 'option_list']:
        return self._tagname

    @property
    def line_range(self) -> tuple[int, int]:
        return (self._items[0].line_range[0], self._items[-1].line_range[1])

    def children(self) -> Sequence[ListItemNode]:
        return self._items

class BulletListNode:
    __slots__ = ('_symbol', '_items')

    def __init__(self, symbol: str, items: list[ListItemNode]) -> None:
        self._symbol = symbol
        self._items = items

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, symbol={self._symbol!r})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self.line_range[0]}-{self.line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname} symbol={self._symbol!r}>{_map}'
        for item in self._items:
            text += '\n' + item.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['bullet_list']:
        return 'bullet_list'

    @property
    def line_range(self) -> tuple[int, int]:
        return (self._items[0].line_range[0], self._items[-1].line_range[1])

    def children(self) -> Sequence[ListItemNode]:
        return self._items
ParenType: TypeAlias = Literal['parens', 'rparen', 'period']
EnumType: TypeAlias = Literal['auto', 'arabic', 'loweralpha', 'upperalpha', 'lowerroman', 'upperroman']

class EnumListNode:
    __slots__ = ('_ptype', '_etype', '_start', '_items')

    def __init__(self, ptype: ParenType, etype: EnumType, start: int, items: list[ListItemNode]) -> None:
        self._ptype = ptype
        self._etype = etype
        self._start = start
        self._items = items

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, ptype={self._ptype!r}, etype={self._etype!r}, start={self._start})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self.line_range[0]}-{self.line_range[1]}' if show_map else ''
        start = f' start={self._start}' if self._start != 1 else ''
        text = f'{_SPACE * current_indent}<{self.tagname} ptype={self._ptype!r} etype={self._etype!r}{start}>{_map}'
        for item in self._items:
            text += '\n' + item.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['enum_list']:
        return 'enum_list'

    @property
    def ptype(self) -> ParenType:
        return self._ptype

    @property
    def etype(self) -> EnumType:
        return self._etype

    @property
    def start(self) -> int:
        return self._start

    @property
    def line_range(self) -> tuple[int, int]:
        return (self._items[0].line_range[0], self._items[-1].line_range[1])

    def children(self) -> Sequence[ListItemNode]:
        return self._items

class FieldListNode:
    __slots__ = ('_items',)

    def __init__(self, items: list[FieldItemNode]) -> None:
        self._items = items

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, len={len(self._items)})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self.line_range[0]}-{self.line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname}>{_map}'
        for item in self._items:
            text += '\n' + item.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['field_list']:
        return 'field_list'

    @property
    def line_range(self) -> tuple[int, int]:
        return (self._items[0].line_range[0], self._items[-1].line_range[1])

    def children(self) -> Sequence[FieldItemNode]:
        return self._items

class FieldItemNode:
    __slots__ = ('_line_range', '_name', '_children')

    def __init__(self, name: InlineNode, line_range: tuple[int, int]) -> None:
        self._line_range = line_range
        self._name = name
        self._children: list[BlockNodeProtocol] = []

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._line_range})'

    @property
    def tagname(self) -> Literal['field_item']:
        return 'field_item'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname}>{_map}'
        text += f'\n{_SPACE * (current_indent + indent_interval)}<name>'
        text += '\n' + self._name.debug_repr(current_indent + 2 * indent_interval, indent_interval=indent_interval, show_map=show_map)
        if self._children:
            text += f'\n{_SPACE * (current_indent + indent_interval)}<body>'
            for child in self._children:
                text += '\n' + child.debug_repr(current_indent + 2 * indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    @property
    def name(self) -> InlineNode:
        return self._name

    def children(self) -> Sequence[BlockNodeProtocol]:
        return [self._name, *self._children]

    def append(self, node: BlockNodeProtocol) -> None:
        self._children.append(node)

class DefinitionListNode:
    __slots__ = ('_items',)

    def __init__(self, items: list[DefinitionItemNode]) -> None:
        self._items = items

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, len={len(self._items)})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self.line_range[0]}-{self.line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname}>{_map}'
        for item in self._items:
            text += '\n' + item.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['definition_list']:
        return 'definition_list'

    @property
    def line_range(self) -> tuple[int, int]:
        return (self._items[0].line_range[0], self._items[-1].line_range[1])

    def children(self) -> Sequence[DefinitionItemNode]:
        return self._items

class DefinitionItemNode:
    __slots__ = ('_line_range', '_term', '_children')

    def __init__(self, term: InlineNode, line_range: tuple[int, int]) -> None:
        self._line_range = line_range
        self._term = term
        self._children: list[BlockNodeProtocol] = []

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._line_range})'

    @property
    def tagname(self) -> Literal['definition_item']:
        return 'definition_item'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname}>{_map}'
        text += f'\n{_SPACE * (current_indent + indent_interval)}<term>'
        text += '\n' + self._term.debug_repr(current_indent + 2 * indent_interval, indent_interval=indent_interval, show_map=show_map)
        if self._children:
            text += f'\n{_SPACE * (current_indent + indent_interval)}<definition>'
            for child in self._children:
                text += '\n' + child.debug_repr(current_indent + 2 * indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    @property
    def term(self) -> InlineNode:
        return self._term

    def children(self) -> Sequence[BlockNodeProtocol]:
        return [self._term, *self._children]

    def append(self, node: BlockNodeProtocol) -> None:
        self._children.append(node)

class TransitionNode:
    __slots__ = ('_style', '_line_range')

    def __init__(self, style: str, line_range: tuple[int, int]) -> None:
        self._style = style
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname}>{_map}'

    @property
    def tagname(self) -> Literal['transition']:
        return 'transition'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[BlockNodeProtocol]:
        return []

    @property
    def style(self) -> str:
        return self._style

class AttributionNode:
    __slots__ = ('_inline',)

    def __init__(self, inline: InlineNode) -> None:
        self._inline = inline

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self.line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self.line_range[0]}-{self.line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname}>{_map}'
        text += '\n' + self._inline.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['attribution']:
        return 'attribution'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._inline.line_range

    @property
    def inline(self) -> InlineNode:
        return self._inline

    def children(self) -> Sequence[InlineNode]:
        return [self._inline]

class SectionTitleNode:
    __slots__ = ('_overline', '_style', '_inline', '_line_range')

    def __init__(self, overline: bool, style: str, inline: InlineNode, line_range: tuple[int, int]) -> None:
        self._overline = overline
        self._style = style
        self._inline = inline
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname} style={self.style!r}>{_map}'
        text += '\n' + self._inline.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['title']:
        return 'title'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[BlockNodeProtocol]:
        return [self._inline]

    @property
    def style(self) -> str:
        return self._style + '/' + self._style if self._overline else self._style

    @property
    def overline(self) -> bool:
        return self._overline

    @property
    def inline(self) -> InlineNode:
        return self._inline

class SectionNode:
    __slots__ = ('_title', '_children')

    def __init__(self, title: SectionTitleNode | None) -> None:
        self._title = title
        self._children: list[BlockNodeProtocol] = []

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self.line_range[0]}-{self.line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname}>{_map}'
        if self._title:
            text += '\n' + self._title.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        for child in self._children:
            text += '\n' + child.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['section']:
        return 'section'

    @property
    def line_range(self) -> tuple[int, int]:
        start = self._title.line_range[0] if self._title else self._children[0].line_range[0] if self._children else 0
        end = self._children[-1].line_range[1] if self._children else self._title.line_range[1] if self._title else 0
        return (start, end)

    @property
    def title(self) -> SectionTitleNode | None:
        return self._title

    def children(self) -> Sequence[BlockNodeProtocol]:
        return self._children

    def append(self, node: BlockNodeProtocol) -> None:
        self._children.append(node)

    def extend(self, nodes: Iterable[BlockNodeProtocol]) -> None:
        self._children.extend(nodes)

class LinkTargetNode:
    __slots__ = ('_name', '_norm_name', '_target', '_target_indirect', '_line_range')

    def __init__(self, name: str, normed_name: str, target: str, target_indirect: bool, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._target = target
        self._target_indirect = target_indirect
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        name = ''
        if self._norm_name:
            name = f' name={self._norm_name!r}'
        target = ''
        if self._target:
            if self._target_indirect:
                target = f' refname={self._target!r}'
            else:
                target = f' refuri={self._target!r}'
        return f'{_SPACE * current_indent}<{self.tagname}{name}{target}>{_map}'

    @property
    def tagname(self) -> Literal['link_target']:
        return 'link_target'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[BlockNodeProtocol]:
        return []

    @property
    def name(self) -> str:
        """The raw name of the target."""
        return self._name

    @property
    def normed_name(self) -> str:
        """The normalised name of the target."""
        return self._norm_name

    @property
    def target(self) -> tuple[bool, str]:
        return (self._target_indirect, self._target)

class CitationNode:
    __slots__ = ('_name', '_norm_name', '_line_range', '_children')

    def __init__(self, name: str, normed_name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._children: list[BlockNodeProtocol] = []
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname} name={self._norm_name!r}>{_map}'
        for child in self._children:
            text += '\n' + child.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['citation']:
        return 'citation'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[BlockNodeProtocol]:
        return self._children

    @property
    def name(self) -> str:
        """The raw name of the target."""
        return self._name

    @property
    def normed_name(self) -> str:
        """The normalised name of the target."""
        return self._norm_name

    def append(self, node: BlockNodeProtocol) -> None:
        self._children.append(node)

class FootnoteNode:
    __slots__ = ('_name', '_norm_name', '_line_range', '_children')

    def __init__(self, name: str, normed_name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._children: list[BlockNodeProtocol] = []
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname} name={self._norm_name!r}>{_map}'
        for child in self._children:
            text += '\n' + child.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['footnote']:
        return 'footnote'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    @property
    def name(self) -> str:
        """The raw name of the target."""
        return self._name

    @property
    def normed_name(self) -> str:
        """The normalised name of the target."""
        return self._norm_name

    def children(self) -> Sequence[BlockNodeProtocol]:
        return self._children

    def append(self, node: BlockNodeProtocol) -> None:
        self._children.append(node)

class SubstitutionNode:
    __slots__ = ('_name', '_norm_name', '_line_range')

    def __init__(self, name: str, normed_name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname} name={self._norm_name!r}>{_map}'

    @property
    def tagname(self) -> Literal['substitution']:
        return 'substitution'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[BlockNodeProtocol]:
        return []

    @property
    def name(self) -> str:
        """The raw name of the target."""
        return self._name

    @property
    def normed_name(self) -> str:
        """The normalised name of the target."""
        return self._norm_name

class DirectiveArgument:
    __slots__ = ('_text', '_line_range')

    def __init__(self, text: str, line_range: tuple[int, int]) -> None:
        self._text = text
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'DirectiveArgument({self._line_range})'

    @property
    def text(self) -> str:
        return self._text

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        return f'{_SPACE * current_indent}<argument>{_map}'

class DirectiveOption:
    __slots__ = ('_name', '_value', '_line_range')

    def __init__(self, name: str, value: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._value = value
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'DirectiveOption({self._name!r}, {self._line_range})'

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        return f'{_SPACE * current_indent}<option name={self._name!r}>{_map}'

class DirectiveNode:
    __slots__ = ('_name', '_line_range', '_parsed', '_argument', '_options', '_concrete_children')

    def __init__(self, name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._line_range = line_range
        self._parsed: bool = False
        'Whether the directive has been parsed.'
        self._argument: DirectiveArgument | None = None
        self._options: list[DirectiveOption] = []
        self._concrete_children: list[BlockNodeProtocol] = []

    def __repr__(self) -> str:
        return f'BlockNode({self.tagname!r}, {self._name!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        text = f'{_SPACE * current_indent}<{self.tagname} name={self.name!r}>{_map}'
        if self._argument:
            text += '\n' + self._argument.debug_repr(current_indent + indent_interval, indent_interval=indent_interval, show_map=show_map)
        if self._options:
            text += f'\n{_SPACE * (current_indent + indent_interval)}<options>'
            for option in self._options:
                text += '\n' + option.debug_repr(current_indent + 2 * indent_interval, indent_interval=indent_interval, show_map=show_map)
        if self._concrete_children:
            text += f'\n{_SPACE * (current_indent + indent_interval)}<body>'
            for child in self._concrete_children:
                text += '\n' + child.debug_repr(current_indent + 2 * indent_interval, indent_interval=indent_interval, show_map=show_map)
        return text

    @property
    def tagname(self) -> Literal['directive']:
        return 'directive'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def append(self, node: BlockNodeProtocol) -> None:
        self._concrete_children.append(node)

    @property
    def name(self) -> str:
        return self._name

    @property
    def parsed(self) -> bool:
        """Whether the directive has been parsed into argument/options/body."""
        return self._parsed

    @property
    def argument(self) -> DirectiveArgument | None:
        return self._argument

    @property
    def options(self) -> Sequence[DirectiveOption]:
        return self._options

    def children(self) -> Sequence[BlockNodeProtocol]:
        return self._concrete_children