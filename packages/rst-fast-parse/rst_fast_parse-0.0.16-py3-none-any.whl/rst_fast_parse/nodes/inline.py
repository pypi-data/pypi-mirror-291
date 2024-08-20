from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Protocol, TypedDict
from rst_fast_parse._opqrstu.ccccbbbb import gAAAAABmw_nQJ9rjavwpYo4l7L5f1_NR2zmeVZOAwk91VtA7cKkibm4iwNHDRvrN3arkU0ahXA3SkC_3cMRUVSIWmOcQM5f6zQ__
from rst_fast_parse._opqrstu.cccceeee import gAAAAABmw_nQ5KSvx54yhPOqM0YU5c3HowY_pfAgWiOFoPD5ZPCrbcGkMsUoQDLaTZPIuDKn6P_DLgprRPLRW2zJs3GGCrBOtTKzJfw7cRFGZb_0f3nHxbk_, gAAAAABmw_nQ4mFNeNixGoCGaWW9hQ4nFpQ7QjZVOZMIQRmjiTg7m31ab2Al4YYW2h_onp_M_gewA4x4_FItlV7rnWh2pzazJPHGm596o2MyJ_9XzCo73cA_
if TYPE_CHECKING:
    from typing import TypeAlias
InlineTagname: TypeAlias = Literal['text', 'problematic', 'strong', 'emphasis', 'literal', 'inline_target', 'uri_reference', 'link_reference', 'citation_reference', 'substitution_reference', 'footnote_reference', 'role']
_SPACE = ' '

class SourceMap(TypedDict):
    line_start: int
    line_end: int
    character_start: int
    character_end: int

def _map_to_str(source_map: SourceMap | None) -> str:
    if source_map is None:
        return ''
    line_start = source_map['line_start']
    line_end = source_map['line_end']
    char_start = source_map['character_start']
    char_end = source_map['character_end']
    return f' {line_start}:{char_start}-{line_end}:{char_end}'

class InlineNodeProtocol(Protocol):

    @property
    def tagname(self) -> InlineTagname:
        ...

    @property
    def source_map(self) -> SourceMap | None:
        ...

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        """Return a debug representation of the node.

        This takes the form of psuedo-XML, with the tag name and line range.

        :param indent: The current indentation level.
        :param indent_interval: The number of spaces to indent each level by.
        :param show_map: Whether to show the source mapping of the node.
        """

class BasicInlineNode:
    __slots__ = ('_tagname', '_marker', '_text', '_source_map')

    def __init__(self, tagname: Literal['emphasis', 'strong', 'literal'], marker: str, text: str, /, *, source_map: SourceMap | None) -> None:
        self._tagname = tagname
        self._marker = marker
        self._text = text
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['emphasis', 'strong', 'literal']:
        return self._tagname

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def marker(self) -> str:
        return self._marker

    @property
    def text(self) -> str:
        return self._text

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname}>{_map}'

class TextNode:
    __slots__ = ('_text', '_source_map')

    def __init__(self, text: str, /, *, source_map: SourceMap | None) -> None:
        self._text = text
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['text']:
        return 'text'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname}>{_map}'

class ProblematicNode:
    __slots__ = ('_text', '_source_map')

    def __init__(self, text: str, /, *, source_map: SourceMap | None) -> None:
        self._text = text
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['problematic']:
        return 'problematic'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname}>{_map}'

class InlineTargetNode:
    __slots__ = ('_text', '_source_map')

    def __init__(self, text: str, /, *, source_map: SourceMap | None) -> None:
        self._text = text
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['inline_target']:
        return 'inline_target'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def text(self) -> str:
        return self._text

    @property
    def name(self) -> str:
        return gAAAAABmw_nQ5KSvx54yhPOqM0YU5c3HowY_pfAgWiOFoPD5ZPCrbcGkMsUoQDLaTZPIuDKn6P_DLgprRPLRW2zJs3GGCrBOtTKzJfw7cRFGZb_0f3nHxbk_(gAAAAABmw_nQJ9rjavwpYo4l7L5f1_NR2zmeVZOAwk91VtA7cKkibm4iwNHDRvrN3arkU0ahXA3SkC_3cMRUVSIWmOcQM5f6zQ__(self._text))

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname} name={self.name!r}>{_map}'

class RoleNode:
    __slots__ = ('_name', '_source_map')

    def __init__(self, *, name: str, source_map: SourceMap | None) -> None:
        self._name = name
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['role']:
        return 'role'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def name(self) -> str:
        return self._name

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        if self._name:
            return f'{_SPACE * current_indent}<{self.tagname} name={self._name!r}>{_map}'
        return f'{_SPACE * current_indent}<{self.tagname}>{_map}'

class SimpleReferenceNode:
    __slots__ = ('_text', '_anonymous', '_source_map')

    def __init__(self, *, text: str, anonymous: bool, source_map: SourceMap | None) -> None:
        self._text = text
        self._anonymous = anonymous
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['link_reference']:
        return 'link_reference'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def text(self) -> str:
        """The raw text of the reference."""
        return self._text

    @property
    def name(self) -> str:
        """The name this can be referenced by."""
        return self._text

    @property
    def refname(self) -> str | None:
        """The name this references (None if anonymous)."""
        return self._text.lower() if not self.anonymous else None

    @property
    def anonymous(self) -> bool:
        return self._anonymous

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        target = ''
        if (refname := self.refname) is not None:
            target = f' ref={refname!r}'
        return f'{_SPACE * current_indent}<{self.tagname}{target}>{_map}'

class PhraseReferenceNode:
    __slots__ = ('_text', '_anonymous', '_source_map')

    def __init__(self, *, text: str, anonymous: bool, source_map: SourceMap | None) -> None:
        self._text = text
        self._anonymous = anonymous
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['link_reference']:
        return 'link_reference'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def text(self) -> str:
        """The raw text of the reference (including backslashes)."""
        return self._text

    @property
    def name(self) -> str:
        """The name this can be referenced by."""
        return gAAAAABmw_nQ4mFNeNixGoCGaWW9hQ4nFpQ7QjZVOZMIQRmjiTg7m31ab2Al4YYW2h_onp_M_gewA4x4_FItlV7rnWh2pzazJPHGm596o2MyJ_9XzCo73cA_(gAAAAABmw_nQJ9rjavwpYo4l7L5f1_NR2zmeVZOAwk91VtA7cKkibm4iwNHDRvrN3arkU0ahXA3SkC_3cMRUVSIWmOcQM5f6zQ__(self._text))

    @property
    def refname(self) -> str | None:
        """The name this references (None if anonymous)."""
        return self.name.lower() if not self.anonymous else None

    @property
    def anonymous(self) -> bool:
        return self._anonymous

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        target = ''
        if (refname := self.refname) is not None:
            target = f' ref={refname!r}'
        return f'{_SPACE * current_indent}<{self.tagname}{target}>{_map}'

class EmbeddedReferenceNode:
    __slots__ = ('_text', '_alias', '_anonymous', '_source_map')

    def __init__(self, *, text: str, alias: str, anonymous: bool, source_map: SourceMap | None) -> None:
        self._text = text
        self._alias = alias
        self._anonymous = anonymous
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['link_reference']:
        return 'link_reference'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def text(self) -> str:
        """The raw text of the reference (including backslashes)."""
        return self._text

    @property
    def alias(self) -> str:
        """The raw alias of the reference (including backslashes)."""
        return self._alias

    @property
    def name(self) -> str | None:
        """The name this can be referenced by."""
        if self._anonymous:
            return None
        if (text := gAAAAABmw_nQJ9rjavwpYo4l7L5f1_NR2zmeVZOAwk91VtA7cKkibm4iwNHDRvrN3arkU0ahXA3SkC_3cMRUVSIWmOcQM5f6zQ__(self._text)):
            return gAAAAABmw_nQ4mFNeNixGoCGaWW9hQ4nFpQ7QjZVOZMIQRmjiTg7m31ab2Al4YYW2h_onp_M_gewA4x4_FItlV7rnWh2pzazJPHGm596o2MyJ_9XzCo73cA_(text)
        return self.refname

    @property
    def refname(self) -> str:
        """The name this references."""
        return gAAAAABmw_nQ5KSvx54yhPOqM0YU5c3HowY_pfAgWiOFoPD5ZPCrbcGkMsUoQDLaTZPIuDKn6P_DLgprRPLRW2zJs3GGCrBOtTKzJfw7cRFGZb_0f3nHxbk_(gAAAAABmw_nQJ9rjavwpYo4l7L5f1_NR2zmeVZOAwk91VtA7cKkibm4iwNHDRvrN3arkU0ahXA3SkC_3cMRUVSIWmOcQM5f6zQ__(self._alias))

    @property
    def anonymous(self) -> bool:
        return self._anonymous

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname} ref={self.refname!r}>{_map}'

class StandaloneUriNode:
    __slots__ = ('_raw', '_uri', '_source_map')

    def __init__(self, *, raw: str, uri: str, source_map: SourceMap | None) -> None:
        self._raw = raw
        self._uri = uri
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['uri_reference']:
        return 'uri_reference'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def raw(self) -> str:
        """The raw text of the reference."""
        return self._raw

    @property
    def uri(self) -> str:
        """The referenced URI."""
        return self._uri

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname} ref={self.uri!r}>{_map}'

class EmbeddedUriNode:
    __slots__ = ('_text', '_uri_raw', '_uri', '_anonymous', '_source_map')

    def __init__(self, *, text: str, uri_raw: str, uri: str, anonymous: bool, source_map: SourceMap | None) -> None:
        self._text = text
        self._uri_raw = uri_raw
        self._uri = uri
        self._anonymous = anonymous
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['uri_reference']:
        return 'uri_reference'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def text(self) -> str:
        """The raw text of the reference (including backslashes)."""
        return self._text

    @property
    def uri_raw(self) -> str:
        """The raw uri text."""
        return self._uri_raw

    @property
    def uri(self) -> str:
        """The referenced URI."""
        return self._uri

    @property
    def name(self) -> str | None:
        """The name this can be referenced by."""
        if self._anonymous:
            return None
        if (text := gAAAAABmw_nQJ9rjavwpYo4l7L5f1_NR2zmeVZOAwk91VtA7cKkibm4iwNHDRvrN3arkU0ahXA3SkC_3cMRUVSIWmOcQM5f6zQ__(self._text)):
            return gAAAAABmw_nQ4mFNeNixGoCGaWW9hQ4nFpQ7QjZVOZMIQRmjiTg7m31ab2Al4YYW2h_onp_M_gewA4x4_FItlV7rnWh2pzazJPHGm596o2MyJ_9XzCo73cA_(text)
        return gAAAAABmw_nQ4mFNeNixGoCGaWW9hQ4nFpQ7QjZVOZMIQRmjiTg7m31ab2Al4YYW2h_onp_M_gewA4x4_FItlV7rnWh2pzazJPHGm596o2MyJ_9XzCo73cA_(self._uri)

    @property
    def anonymous(self) -> bool:
        return self._anonymous

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname} ref={self.uri!r}>{_map}'

class CitationReferenceNode:
    __slots__ = ('_label', '_source_map')

    def __init__(self, *, label: str, source_map: SourceMap | None) -> None:
        self._label = label
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['citation_reference']:
        return 'citation_reference'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def label(self) -> str:
        return self._label

    @property
    def refname(self) -> str:
        return gAAAAABmw_nQ5KSvx54yhPOqM0YU5c3HowY_pfAgWiOFoPD5ZPCrbcGkMsUoQDLaTZPIuDKn6P_DLgprRPLRW2zJs3GGCrBOtTKzJfw7cRFGZb_0f3nHxbk_(self._label)

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        return f'{_SPACE * current_indent}<{self.tagname} ref={self.refname!r}>{_map}'

class FootnoteReferenceNode:
    __slots__ = ('_label', '_source_map')

    def __init__(self, *, label: str, source_map: SourceMap | None) -> None:
        self._label = label
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['footnote_reference']:
        return 'footnote_reference'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def label(self) -> str:
        return self._label

    @property
    def refname(self) -> str:
        refname = gAAAAABmw_nQ5KSvx54yhPOqM0YU5c3HowY_pfAgWiOFoPD5ZPCrbcGkMsUoQDLaTZPIuDKn6P_DLgprRPLRW2zJs3GGCrBOtTKzJfw7cRFGZb_0f3nHxbk_(self._label)
        if refname and refname[0] == '#':
            return refname[1:]
        elif refname == '*':
            return ''
        return refname

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        refname = self.refname
        target = f' ref={refname!r}' if refname else ''
        return f'{_SPACE * current_indent}<{self.tagname}{target}>{_map}'

class SubstitutionReferenceNode:
    __slots__ = ('_label', '_is_reference', '_anonymous', '_source_map')

    def __init__(self, *, label: str, is_reference: bool, anonymous: bool, source_map: SourceMap | None) -> None:
        self._label = label
        self._is_reference = is_reference
        self._anonymous = anonymous
        self._source_map = source_map

    @property
    def tagname(self) -> Literal['substitution_reference']:
        return 'substitution_reference'

    @property
    def source_map(self) -> SourceMap | None:
        return self._source_map

    @property
    def label(self) -> str:
        return self._label

    @property
    def subname(self) -> str:
        return gAAAAABmw_nQ5KSvx54yhPOqM0YU5c3HowY_pfAgWiOFoPD5ZPCrbcGkMsUoQDLaTZPIuDKn6P_DLgprRPLRW2zJs3GGCrBOtTKzJfw7cRFGZb_0f3nHxbk_(gAAAAABmw_nQJ9rjavwpYo4l7L5f1_NR2zmeVZOAwk91VtA7cKkibm4iwNHDRvrN3arkU0ahXA3SkC_3cMRUVSIWmOcQM5f6zQ__(self._label))

    @property
    def is_reference(self) -> bool:
        return self._is_reference

    @property
    def anonymous(self) -> bool:
        return self._anonymous

    @property
    def refname(self) -> str | None:
        if not self.is_reference or self.anonymous:
            return None
        return gAAAAABmw_nQ5KSvx54yhPOqM0YU5c3HowY_pfAgWiOFoPD5ZPCrbcGkMsUoQDLaTZPIuDKn6P_DLgprRPLRW2zJs3GGCrBOtTKzJfw7cRFGZb_0f3nHxbk_(gAAAAABmw_nQJ9rjavwpYo4l7L5f1_NR2zmeVZOAwk91VtA7cKkibm4iwNHDRvrN3arkU0ahXA3SkC_3cMRUVSIWmOcQM5f6zQ__(self._label))

    def debug_repr(self, current_indent: int=0, /, *, indent_interval: int=2, show_map: bool=True) -> str:
        _map = _map_to_str(self.source_map) if show_map else ''
        refname = self.refname
        target = f' ref={refname!r}' if refname is not None else ' ref=<anonymous>' if self.anonymous else ''
        return f'{_SPACE * current_indent}<{self.tagname} sub={self.subname!r}{target}>{_map}'