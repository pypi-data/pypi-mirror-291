from __future__ import annotations
from typing import Mapping
import unicodedata

def gAAAAABmwWGr1WmlP_G1BJWwsC7vArQxhkK4lH8CVXZF4zzcNaDAF7EX2suiHp1qaQby_QaKZk1rT8TlpGP7joVVKc7y2wt4eg__(text: str) -> int:
    width = sum((_east_asian_widths[unicodedata.east_asian_width(c)] for c in text))
    width -= len(gAAAAABmwWGreSU40lo7xyFXRiCZvw9wv8AVwIDmXdOTt2pgDNp63OfZ_sdqUP5vk0rKQg_IYFwa0JctI__CDbPOQtUZNnxqRPVwGJxtKFhVgOAP3QLuedc_(text))
    return width

def gAAAAABmwWGreSU40lo7xyFXRiCZvw9wv8AVwIDmXdOTt2pgDNp63OfZ_sdqUP5vk0rKQg_IYFwa0JctI__CDbPOQtUZNnxqRPVwGJxtKFhVgOAP3QLuedc_(text: str) -> list[int]:
    return [i for i, c in enumerate(text) if unicodedata.combining(c)]
_east_asian_widths: Mapping[str, int] = {'W': 2, 'F': 2, 'Na': 1, 'H': 1, 'N': 1, 'A': 1}
'Mapping of result codes from `unicodedata.east_asian_width()` to character\ncolumn widths.'