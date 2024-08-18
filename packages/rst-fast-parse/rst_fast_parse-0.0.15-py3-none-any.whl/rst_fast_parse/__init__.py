"""A fast, incremental parser for reStructuredText."""
from rst_fast_parse import diagnostics, elements
from rst_fast_parse.parse import get_default_directives, nest_sections, parse_string
__version__ = '0.0.15'
__all__ = ('parse_string', 'get_default_directives', 'nest_sections', 'elements', 'diagnostics')