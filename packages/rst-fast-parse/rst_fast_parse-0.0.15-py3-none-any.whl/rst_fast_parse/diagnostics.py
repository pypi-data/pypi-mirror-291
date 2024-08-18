from __future__ import annotations
import enum
from typing import Iterator, Protocol
from rst_fast_parse._opqrstu.cccciiii import gAAAAABmwWGrBsJwbwlJV63fAbPJEbEQbS1T7F_bcC9PLX8KOfhkUi680XxmKMJkgyhSltkyCDDL8NU3qAnRf_0KvYtcGfC_vg__

class DiagnosticCode(enum.Enum):
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

    @classmethod
    def get_fields(cls) -> list[tuple[str, str, str]]:
        """Return the name, code, and description."""
        return gAAAAABmwWGrBsJwbwlJV63fAbPJEbEQbS1T7F_bcC9PLX8KOfhkUi680XxmKMJkgyhSltkyCDDL8NU3qAnRf_0KvYtcGfC_vg__(cls)

class Diagnostic:
    """A diagnostic message."""
    __slots__ = ('_message', '_code', '_line_start')

    def __init__(self, code: DiagnosticCode, message: str, line_start: int, /) -> None:
        """Initialize the diagnostic.

        :param code: The diagnostic code.
        :param message: The diagnostic message.
        :param line_start: The line number where the diagnostic starts (0-based).
        """
        self._message = message
        self._code = code
        self._line_start = line_start

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
        return f'{self._line_start}: {self._message} [{self._code.value}]'

    def as_dict(self) -> dict[str, str | int]:
        """Return the diagnostic as a dictionary."""
        return {'code': self._code.value, 'message': self._message, 'line_start': self._line_start}

class DiagnosticList(Protocol):
    """A list of diagnostics."""

    def __iter__(self) -> Iterator[Diagnostic]:
        ...

    def append(self, diagnostic: Diagnostic) -> None:
        ...