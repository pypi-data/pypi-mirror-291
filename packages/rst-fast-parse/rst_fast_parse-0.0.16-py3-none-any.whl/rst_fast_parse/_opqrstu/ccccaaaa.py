from __future__ import annotations
from typing import Mapping
import unicodedata

def gAAAAABmw_nQrFj9lpPOduaY2Si585rj_BWxoDG2A78NuHyI1eFS9xtgs9aL2wHgUX_a571D63zcPNg3MW_KfCxkXiUpuzLidQ__(text: str) -> int:
    pass
    width = sum((_east_asian_widths[unicodedata.east_asian_width(c)] for c in text))
    width -= len(gAAAAABmw_nQnO3uR9dX_zVZEWw0HlrQ2fhbp8Mbj9Os7Cl9_CcuLkMS5INl5Y_xiNWJqqzPYb_4S1EVswCxwXGVasuanfrarN7oDTEiW2R5d9OFOm9AROE_(text))
    return width

def gAAAAABmw_nQnO3uR9dX_zVZEWw0HlrQ2fhbp8Mbj9Os7Cl9_CcuLkMS5INl5Y_xiNWJqqzPYb_4S1EVswCxwXGVasuanfrarN7oDTEiW2R5d9OFOm9AROE_(text: str) -> list[int]:
    pass
    return [i for i, c in enumerate(text) if unicodedata.combining(c)]
_east_asian_widths: Mapping[str, int] = {'W': 2, 'F': 2, 'Na': 1, 'H': 1, 'N': 1, 'A': 1}
pass