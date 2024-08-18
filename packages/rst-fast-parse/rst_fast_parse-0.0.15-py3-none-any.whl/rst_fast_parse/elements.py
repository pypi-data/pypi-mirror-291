from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, Callable, Iterable, Literal, Protocol, Sequence
if TYPE_CHECKING:
    from typing import TypeAlias
BlockTagName: TypeAlias = Literal['root', 'inline', 'section', 'transition', 'title', 'paragraph', 'blockquote', 'attribution', 'literal_block', 'line_block', 'doctest', 'bullet_list', 'enum_list', 'definition_list', 'definition_item', 'field_list', 'field_item', 'option_list', 'list_item', 'link_target', 'footnote', 'citation', 'substitution', 'directive', 'comment', 'table_simple', 'table_grid']
_SPACE = ' '

class ElementProtocol(Protocol):
    """A generic element in the document tree."""

    @property
    def tagname(self) -> BlockTagName:
        """The tag name of the element."""

    @property
    def line_range(self) -> tuple[int, int]:
        """The line range of the element in the source.
        (index-based, starting from 0)
        """

    def children(self) -> Sequence[ElementProtocol]:
        """Return a list of the children of the element."""

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        """Return a debug representation of the element.

        This takes the form of psuedo-XML, with the tag name and line range.

        :param indent: The current indentation level.
        :param indent_interval: The number of spaces to indent each level by.
        :param show_map: Whether to show the source mapping of the element.
        """

class RootElement:
    __slots__ = ('_line_range', '_children')

    def __init__(self, line_range: tuple[int, int]) -> None:
        self._line_range = line_range
        self._children: list[ElementProtocol] = []

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

    @property
    def tagname(self) -> Literal['root']:
        return 'root'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        text = ''
        for element in self._children:
            text += element.debug_repr(current_indent, indent_interval=indent_interval, show_map=show_map) + '\n'
        return text

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

    def extend(self, elements: Iterable[ElementProtocol]) -> None:
        self._children.extend(elements)

class LineProtocol(Protocol):

    @property
    def content(self) -> str:
        ...

    @property
    def line(self) -> int:
        """The line number of the line in the source (0-based)."""

class InlineElement:
    __slots__ = ('_lines',)

    def __init__(self, lines: Sequence[LineProtocol]) -> None:
        assert lines, 'InlineElement must have at least one line.'
        self._lines = lines

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self.line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self.line_range[0]}-{self.line_range[1]}' if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname}>{_map}'

    @property
    def tagname(self) -> Literal['inline']:
        return 'inline'

    def children(self) -> Sequence[ElementProtocol]:
        return []

    @property
    def line_range(self) -> tuple[int, int]:
        return (self._lines[0].line, self._lines[-1].line)

    def raw_content(self, *, newline: str='\n') -> str:
        return newline.join((line.content for line in self._lines))

class BasicElement:
    """A generic element in the document tree."""
    __slots__ = ('_tagname', '_line_range')

    def __init__(self, tagname: BlockTagName, line_range: tuple[int, int]) -> None:
        """
        :param tagname: The tag name of the element.
        :param line_range: The line range of the element in the source.
            (index-based, starting from 0)
        """
        self._tagname = tagname
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self._tagname!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        return f'{_SPACE * current_indent}<{self._tagname}>{_map}'

    @property
    def tagname(self) -> BlockTagName:
        return self._tagname

    def children(self) -> Sequence[ElementProtocol]:
        return []

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

class ParagraphElement:
    __slots__ = ('_inline', '_literal')

    def __init__(self, inline: InlineElement, literal: ElementProtocol | None) -> None:
        self._inline = inline
        self._literal = literal

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self.line_range})'

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
    def inline(self) -> InlineElement:
        return self._inline

    @property
    def literal(self) -> ElementProtocol | None:
        return self._literal

    def children(self) -> Sequence[ElementProtocol]:
        return [self._inline] if self._literal is None else [self._inline, self._literal]

    @property
    def line_range(self) -> tuple[int, int]:
        start = self._inline.line_range[0]
        end = self._literal.line_range[1] if self._literal is not None else self._inline.line_range[1]
        return (start, end)

class BlockQuoteElement:
    __slots__ = ('_line_range', '_children')

    def __init__(self, line_range: tuple[int, int]) -> None:
        self._children: list[ElementProtocol] = []
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

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

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

class ListItemElement:
    """A generic element in the document tree."""
    __slots__ = ('_line_range', '_children')

    def __init__(self, line_range: tuple[int, int]) -> None:
        """
        :param line_range: The line range of the element in the source.
            (index-based, starting from 0)
        """
        self._line_range = line_range
        self._children: list[ElementProtocol] = []

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

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

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

class ListElement:
    """A list element in the document tree."""
    __slots__ = ('_tagname', '_items')

    def __init__(self, tagname: Literal['line_block', 'option_list'], items: list[ListItemElement]) -> None:
        self._tagname = tagname
        self._items = items

    def __repr__(self) -> str:
        return f'Element({self._tagname!r}, len={len(self._items)})'

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

    def children(self) -> Sequence[ListItemElement]:
        return self._items

class BulletListElement:
    __slots__ = ('_symbol', '_items')

    def __init__(self, symbol: str, items: list[ListItemElement]) -> None:
        self._symbol = symbol
        self._items = items

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, symbol={self._symbol!r})'

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

    def children(self) -> Sequence[ListItemElement]:
        return self._items
ParenType: TypeAlias = Literal['parens', 'rparen', 'period']
EnumType: TypeAlias = Literal['auto', 'arabic', 'loweralpha', 'upperalpha', 'lowerroman', 'upperroman']

class EnumListElement:
    __slots__ = ('_ptype', '_etype', '_start', '_items')

    def __init__(self, ptype: ParenType, etype: EnumType, start: int, items: list[ListItemElement]) -> None:
        self._ptype = ptype
        self._etype = etype
        self._start = start
        self._items = items

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, ptype={self._ptype!r}, etype={self._etype!r}, start={self._start})'

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

    def children(self) -> Sequence[ListItemElement]:
        return self._items

class FieldListElement:
    """A field list element in the document tree."""
    __slots__ = ('_items',)

    def __init__(self, items: list[FieldItemElement]) -> None:
        self._items = items

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, len={len(self._items)})'

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

    def children(self) -> Sequence[FieldItemElement]:
        return self._items

class FieldItemElement:
    __slots__ = ('_line_range', '_name', '_children')

    def __init__(self, name: InlineElement, line_range: tuple[int, int]) -> None:
        """
        :param line_range: The line range of the element in the source.
            (index-based, starting from 0)
        """
        self._line_range = line_range
        self._name = name
        self._children: list[ElementProtocol] = []

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

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
    def name(self) -> InlineElement:
        return self._name

    def children(self) -> Sequence[ElementProtocol]:
        return [self._name, *self._children]

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

class DefinitionListElement:
    """A definition list element in the document tree."""
    __slots__ = ('_items',)

    def __init__(self, items: list[DefinitionItemElement]) -> None:
        self._items = items

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, len={len(self._items)})'

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

    def children(self) -> Sequence[DefinitionItemElement]:
        return self._items

class DefinitionItemElement:
    __slots__ = ('_line_range', '_term', '_children')

    def __init__(self, term: InlineElement, line_range: tuple[int, int]) -> None:
        self._line_range = line_range
        self._term = term
        self._children: list[ElementProtocol] = []

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

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
    def term(self) -> InlineElement:
        return self._term

    def children(self) -> Sequence[ElementProtocol]:
        return [self._term, *self._children]

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

class TransitionElement:
    __slots__ = ('_style', '_line_range')

    def __init__(self, style: str, line_range: tuple[int, int]) -> None:
        self._style = style
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname}>{_map}'

    @property
    def tagname(self) -> Literal['transition']:
        return 'transition'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
        return []

    @property
    def style(self) -> str:
        return self._style

class AttributionElement:
    __slots__ = ('_inline',)

    def __init__(self, inline: InlineElement) -> None:
        self._inline = inline

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self.line_range})'

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
    def inline(self) -> InlineElement:
        return self._inline

    def children(self) -> Sequence[InlineElement]:
        return [self._inline]

class SectionTitleElement:
    __slots__ = ('_overline', '_style', '_inline', '_line_range')

    def __init__(self, overline: bool, style: str, inline: InlineElement, line_range: tuple[int, int]) -> None:
        self._overline = overline
        self._style = style
        self._inline = inline
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

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

    def children(self) -> Sequence[ElementProtocol]:
        return [self._inline]

    @property
    def style(self) -> str:
        return self._style + '/' + self._style if self._overline else self._style

    @property
    def overline(self) -> bool:
        return self._overline

    @property
    def inline(self) -> InlineElement:
        return self._inline

class SectionElement:
    __slots__ = ('_title', '_children')

    def __init__(self, title: SectionTitleElement | None) -> None:
        self._title = title
        self._children: list[ElementProtocol] = []

    def __repr__(self) -> str:
        return f'Element({self.tagname!r})'

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
    def title(self) -> SectionTitleElement | None:
        return self._title

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

    def extend(self, element: Iterable[ElementProtocol]) -> None:
        self._children.extend(element)

class LinkTargetElement:
    __slots__ = ('_name', '_norm_name', '_target', '_target_indirect', '_line_range')

    def __init__(self, name: str, normed_name: str, target: str, target_indirect: bool, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._target = target
        self._target_indirect = target_indirect
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

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

    def children(self) -> Sequence[ElementProtocol]:
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

class CitationElement:
    __slots__ = ('_name', '_norm_name', '_line_range', '_children')

    def __init__(self, name: str, normed_name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._children: list[ElementProtocol] = []
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

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

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    @property
    def name(self) -> str:
        """The raw name of the target."""
        return self._name

    @property
    def normed_name(self) -> str:
        """The normalised name of the target."""
        return self._norm_name

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

class FootnoteElement:
    __slots__ = ('_name', '_norm_name', '_line_range', '_children')

    def __init__(self, name: str, normed_name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._children: list[ElementProtocol] = []
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

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

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

class SubstitutionElement:
    __slots__ = ('_name', '_norm_name', '_line_range')

    def __init__(self, name: str, normed_name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = f' {self._line_range[0]}-{self._line_range[1]}' if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname} name={self._norm_name!r}>{_map}'

    @property
    def tagname(self) -> Literal['substitution']:
        return 'substitution'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
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

class DirectiveElement:
    __slots__ = ('_name', '_line_range', '_parsed', '_argument', '_options', '_concrete_children')

    def __init__(self, name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._line_range = line_range
        self._parsed: bool = False
        'Whether the directive has been parsed.'
        self._argument: DirectiveArgument | None = None
        self._options: list[DirectiveOption] = []
        self._concrete_children: list[ElementProtocol] = []

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._name!r}, {self._line_range})'

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

    def append(self, element: ElementProtocol) -> None:
        self._concrete_children.append(element)

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

    def children(self) -> Sequence[ElementProtocol]:
        return self._concrete_children

class WalKChildrenCallback(Enum):
    """A callback for the walk_children function."""
    Continue = 0
    'Continue walking the tree.'
    SkipSelfAndChildren = 1
    "Skip the current element and it's children of the current element."
    SkipChildren = 2
    'Skip the children of the current element.'
    SkipSiblings = 3
    "Skip preceding siblings of the current element\n    (after yielding current element's children).\n    "
    SkipChildrenAndSiblings = 4
    'Skip the children and siblings of the current element.'
    SkipSelfAndChildrenAndSiblings = 5
    'Skip the children and siblings of the current element.'
    Stop = 6
    'Stop walking the tree (before yielding current element).'

def walk_children(element: ElementProtocol, callback: Callable[[ElementProtocol], WalKChildrenCallback] | None=None) -> Iterable[ElementProtocol]:
    """Recursively yield children of the element.

    This is a depth-first traversal.

    :param element: The root element to start from.
    :param callback: An optional callback to control the traversal.
    """
    for child in element.children():
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

def walk_line_inside(initial: ElementProtocol, line: int) -> Iterable[ElementProtocol]:
    """Yield all elements that contain the given line, in order of nesting.

    :param initial: The initial element to start from.
    :param line: The line to search for (index-based, starting from 0).

    Note, the initial element will not be yielded.

    Also note, that it is assumed that all children of an element are in order of appearance,
    and that the line ranges of the elements do not overlap,
    i.e. that we can halt the search when we reach an element
    with a bottom line that is greater than the target line.
    """

    def _callback(element: ElementProtocol) -> WalKChildrenCallback:
        if element.line_range[0] <= line <= element.line_range[1]:
            return WalKChildrenCallback.Continue
        if element.line_range[1] > line:
            return WalKChildrenCallback.SkipSelfAndChildrenAndSiblings
        return WalKChildrenCallback.SkipSelfAndChildren
    yield from walk_children(initial, _callback)