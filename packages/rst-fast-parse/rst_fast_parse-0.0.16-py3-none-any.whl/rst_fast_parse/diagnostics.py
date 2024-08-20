from __future__ import annotations
import enum
from typing import TYPE_CHECKING, Iterator, Protocol, TypedDict
from rst_fast_parse._opqrstu.cccciiii import gAAAAABmw_nQEtm39b_pxabmd4HYmC1pUuReQ0hCDhPxu74afdD5z9se5H0bMirP7Thg2ULQMatIqMbSJXFOH8FDOVLrXjUz0A__
if TYPE_CHECKING:
    from typing_extensions import NotRequired

class DiagnosticCode(enum.Enum):
    """Diagnostic codes."""
    tab_in_line = 'source.tab_in_line'
    'Warns on tabs in a line, which can degrade performance of source mapping.'
    blank_line = 'block.blank_line'
    'Warns on missing blank lines between syntax blocks.'
    title_line = 'block.title_line'
    'Warns on issues with title under/over lines.'
    title_disallowed = 'block.title_disallowed'
    'Warns on unexpected titles in a context where they are not allowed.'
    paragraph_indentation = 'block.paragraph_indentation'
    'Warns on unexpected indentation of a paragraph line.'
    literal_no_content = 'block.literal_no_content'
    'Warns on literal blocks with no content.'
    target_malformed = 'block.target_malformed'
    'Warns on malformed hyperlink targets.'
    substitution_malformed = 'block.substitution_malformed'
    'Warns on malformed substitution definition.'
    table_malformed = 'block.table_malformed'
    'Warns on malformed tables.'
    inconsistent_title_level = 'block.inconsistent_title_level'
    'Warns on inconsistent title levels, e.g. a level 1 title style followed by a level 3 style.'
    directive_indented_option = 'block.directive_indented_options'
    'Warns if the second line of a directive starts with an indented `:`.'
    directive_malformed = 'block.directive_malformed'
    'Warns on malformed directives.'
    inline_no_closing_marker = 'inline.no_closing_marker'
    'Warns on inline markup with no closing marker.'
    inline_role_malformed = 'inline.role_malformed'
    'Warns on malformed inline roles.'
    inline_role_no_name = 'inline.role_no_name'
    'Warns on inline roles with no name.'

    @classmethod
    def get_fields(cls) -> list[tuple[str, str, str]]:
        """Return the name, code, and description."""
        return gAAAAABmw_nQEtm39b_pxabmd4HYmC1pUuReQ0hCDhPxu74afdD5z9se5H0bMirP7Thg2ULQMatIqMbSJXFOH8FDOVLrXjUz0A__(cls)

class DiagnosticJson(TypedDict):
    """A dictionary representation of a diagnostic, that can be JSON serialized."""
    code: str
    message: str
    line_start: int
    line_end: NotRequired[int]
    'if missing ``line_start == line_end``'
    character_start: NotRequired[int]
    'If missing, the character start is 0.'
    character_end: NotRequired[int]
    'If missing, the character start is at the end of the line.'

class Diagnostic:
    """A diagnostic message."""
    __slots__ = ('_message', '_code', '_line_start', '_line_end', '_character_start', '_character_end')

    def __init__(self, code: DiagnosticCode, message: str, /, line_start: int, character_start: int, character_end: int | None, line_end: int | None=None) -> None:
        """Initialize the diagnostic.

        :param code: The diagnostic code.
        :param message: The diagnostic message.
        :param line_start: The line number where the diagnostic starts (0-based).
        """
        self._message = message
        self._code = code
        self._line_start = line_start
        self._character_start = character_start
        self._character_end = character_end
        self._line_end = line_start if line_end is None else line_end

    @property
    def code(self) -> DiagnosticCode:
        """The diagnostic code."""
        return self._code

    @property
    def message(self) -> str:
        """The diagnostic message."""
        return self._message

    @property
    def line_start(self) -> int:
        """The line number where the diagnostic starts."""
        return self._line_start

    def __repr__(self) -> str:
        return f'Diagnostic({self._code.value!r}, {self._message!r}, {self._line_start!r})'

    def __str__(self) -> str:
        return f'{self._line_start + 1}:{self._character_start + 1}: {self._message} [{self._code.value}]'

    def as_dict(self) -> DiagnosticJson:
        """Return the diagnostic as a dictionary."""
        data: DiagnosticJson = {'code': self._code.value, 'message': self._message, 'line_start': self._line_start}
        if self._line_start != self._line_end:
            data['line_end'] = self._line_end
        if self._character_start:
            data['character_start'] = self._character_start
        if self._character_end is not None:
            data['character_end'] = self._character_end
        return data

    @classmethod
    def from_dict(cls, data: DiagnosticJson) -> Diagnostic:
        """Create a diagnostic from a dictionary."""
        return cls(_load_from_value(data['code']), data['message'], data['line_start'], data.get('character_start', 0), data.get('character_end', None), line_end=data.get('line_end', None))

def _load_from_value(value: str) -> DiagnosticCode:
    """Load an enum member from its value.

    :raises ValueError: If the value is not found in the enum.
    """
    for member in DiagnosticCode:
        if member.value == value:
            return member
    raise ValueError(f'{value} is not a valid value for {DiagnosticCode.__name__}')

class DiagnosticList(Protocol):
    """A list of diagnostics."""

    def __iter__(self) -> Iterator[Diagnostic]:
        ...

    def append(self, diagnostic: Diagnostic) -> None:
        ...