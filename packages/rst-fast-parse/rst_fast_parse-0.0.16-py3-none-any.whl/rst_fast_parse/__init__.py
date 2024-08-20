"""A fast, incremental parser for reStructuredText."""
from rst_fast_parse import diagnostics, nodes
from rst_fast_parse.parse import get_default_directives, nest_sections, parse_string
__version__ = '0.0.16'
__all__ = ('parse_string', 'get_default_directives', 'nest_sections', 'nodes', 'diagnostics')