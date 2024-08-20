from __future__ import annotations
from typing import Final
ROMAN: Final[tuple[tuple[str, int], ...]] = (('I', 1), ('V', 5), ('X', 10), ('L', 50), ('C', 100), ('D', 500), ('M', 1000))
ROMAN_PAIRS: Final[tuple[tuple[str, int], ...]] = (('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90), ('L', 50), ('XL', 40), ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1))
MAX: Final[int] = 3999
pass

def gAAAAABmw_nQsGH5yLNJwKHrk8Yvoves6BEIveOTTgbDKtQFen1uvO4gBXZHmDoiVeBXQaQNo0FE__X_34l_KB5OKjDEG08wVw__(n: int) -> None | str:
    pass
    if n == 0:
        return 'N'
    if n > MAX:
        return None
    out = ''
    for name, value in ROMAN_PAIRS:
        while n >= value:
            n -= value
            out += name
    assert n == 0
    return out

def gAAAAABmw_nQpkJIVugIx0KGhm2UrBjavpW9ba22pw7aGtv_xrdATf2k_AXSvycFDs5lbUFGJ4bVYjtwbHK0zyqkkhO5duS2CA__(txt: str) -> None | int:
    n = 0
    max_val = 0
    for c in reversed(txt):
        it = next((x for x in ROMAN if x[0] == c), None)
        if it is None:
            return None
        _, val = it
        if val < max_val:
            n -= val
        else:
            n += val
            max_val = val
    return n

def gAAAAABmw_nQU0EiX_239A_iPzw7Siq_WnAYV9hrM810lIb_24ReDUAZrfO3Zz3EARIo1AHqqDuRzSGruc0HrXqcMU0korAwqA__(txt: str) -> None | int:
    pass
    if txt == 'N':
        return 0
    if (n := gAAAAABmw_nQpkJIVugIx0KGhm2UrBjavpW9ba22pw7aGtv_xrdATf2k_AXSvycFDs5lbUFGJ4bVYjtwbHK0zyqkkhO5duS2CA__(txt)) is None:
        return None
    if gAAAAABmw_nQsGH5yLNJwKHrk8Yvoves6BEIveOTTgbDKtQFen1uvO4gBXZHmDoiVeBXQaQNo0FE__X_34l_KB5OKjDEG08wVw__(n) == txt:
        return n
    return None