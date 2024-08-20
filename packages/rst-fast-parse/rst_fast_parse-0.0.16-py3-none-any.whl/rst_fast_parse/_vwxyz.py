from __future__ import annotations
from itertools import takewhile
import re
from typing import Final, Iterable, NewType, Sequence
PositiveInt = NewType('PositiveInt', int)

class gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__:
    pass
    __slots__ = ('_line_content', '_source', '_offset_line', '_offset_start', '_offset_end', '_sliced_content', '_gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__', '_tab_width', '_charcter_start_cache', '_charcter_end_cache')

    def __init__(self, content: str, /, *, line: PositiveInt, start: PositiveInt | None, end: PositiveInt | None, gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__: str | None, source: str | None, tab_width: int) -> None:
        pass
        self._line_content: Final[str] = content
        self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__: Final[str | None] = gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__
        self._tab_width: Final[int] = tab_width
        self._sliced_content: Final[str] = content[start:end]
        self._source: Final[str | None] = source
        self._offset_line: Final[PositiveInt] = line
        self._offset_start: Final[PositiveInt | None] = start
        self._offset_end: Final[PositiveInt | None] = end
        self._charcter_start_cache: int | None = None
        self._charcter_end_cache: int | None = None

    @classmethod
    def gAAAAABmw_nQkPSt6nJ1NPknDkKrk4LKojvTJXep7hBI6f3vZ4Z5ZFoTck4mKDBAZHDp6j_KO5nijPlFptsdmUzmHS55FZEAMA__(cls, original_content: str, /, line: int=0) -> gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__:
        assert line >= 0
        expanded = original_content.expandtabs(8)
        return cls(expanded, line=PositiveInt(line), start=None, end=None, gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__=None if '\t' not in original_content else original_content, source=None, tab_width=8)

    def __repr__(self) -> str:
        return f'gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__(source={self._source}, line={self._offset_line}, start={self._offset_start}, end={self._offset_end})'

    def __str__(self) -> str:
        return self.content

    @property
    def content(self) -> str:
        pass
        return self._sliced_content

    @property
    def line(self) -> int:
        pass
        return self._offset_line

    @property
    def has_tabs(self) -> bool:
        pass
        return self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__ is not None

    @property
    def character_start(self) -> int:
        pass
        if self._offset_start is None:
            return 0
        elif self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__ is None:
            return self._offset_start
        if self._charcter_start_cache is None:
            self._charcter_start_cache = gAAAAABmw_nQabd6FRgGig56sxGIcXIaQLgMdB9BpSFEDR_8bFRacDOKZYs9hdJsEYlXZbG8_Z0kiW_1x2VdXbnmHSWVgGIscatUf5V0paJqDqBjWpOsjhA_(self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__, self._offset_start, self._tab_width)
        return self._charcter_start_cache

    @property
    def character_end(self) -> int:
        pass
        if self._charcter_end_cache is None:
            if self._offset_end is None:
                self._charcter_end_cache = len(self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__) if self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__ is not None else len(self._line_content)
            elif self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__ is None:
                self._charcter_end_cache = self._offset_end
            else:
                self._charcter_end_cache = gAAAAABmw_nQabd6FRgGig56sxGIcXIaQLgMdB9BpSFEDR_8bFRacDOKZYs9hdJsEYlXZbG8_Z0kiW_1x2VdXbnmHSWVgGIscatUf5V0paJqDqBjWpOsjhA_(self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__, self._offset_end, self._tab_width)
        return self._charcter_end_cache

    @property
    def gAAAAABmw_nQC5lB_2n9IANSFFmCNhHIwZWX1YR75NzcTdvXfcm0lX6HZ8TFEN_fgM6_XFsc0hDxVcGjcG0J4ZfCVChQJSqjyQ__(self) -> bool:
        pass
        return not self.content.strip()

    def gAAAAABmw_nQK2_rPB2FLNZmeYW1eronEd0MIIkzWnQ_h9olZJMEqQdRLCBYjwkzW2QvDqHYsuEWM268E_H1U4gvXE3xoJdIyw__(self, n: int, /) -> gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__:
        pass
        assert n >= 0
        if n == 0:
            return self
        return gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__(self._line_content, line=self._offset_line, start=PositiveInt(n) if self._offset_start is None else PositiveInt(self._offset_start + n), end=self._offset_end, source=self._source, tab_width=self._tab_width, gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__=self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__)

    def gAAAAABmw_nQs2zNGtak6xDVNUWILahHPPvpM9SVDQD4eDvJsfiwsvsrA7b9_ONKJqgPChh1dUCE081XYIsjY62Fw9p1anPS5Q__(self, /, start: PositiveInt, stop: PositiveInt) -> gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__:
        pass
        assert start >= 0 and stop >= 0 and (start <= stop)
        offset_start: PositiveInt = start if self._offset_start is None else self._offset_start + start
        offset_end: PositiveInt = offset_start + (stop - start)
        return gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__(self._line_content, line=self._offset_line, start=offset_start, end=offset_end, source=self._source, tab_width=self._tab_width, gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__=self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__)

    def rstrip(self) -> gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__:
        pass
        content_r = self.content[::-1]
        spaces = sum((1 for _ in takewhile(lambda s: s == ' ', content_r)))
        if not spaces:
            return self
        offset_end: PositiveInt = len(content_r) - spaces if self._offset_end is None else self._offset_end - spaces
        return gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__(self._line_content, line=self._offset_line, start=self._offset_start, end=offset_end, source=self._source, tab_width=self._tab_width, gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__=self._gAAAAABmw_nQDcOaLYfvS_KjjrAWU8umXUXTzf2TQp2jQPVlUUmifteJ0489j76RYL8qXjTysYeRsbncRPcGvkXTaUMuELUsgQ__)

class gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__:
    pass
    __slots__ = ('_lines', '_current')

    def __init__(self, lines: Sequence[gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__]) -> None:
        pass
        self._lines = lines
        self._current: int = 0
        pass

    def __repr__(self) -> str:
        return f'gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__(lines={len(self._lines)}, index={self._current})'

    def gAAAAABmw_nQAMV_OdYyjbpw2NMbW5EYxn50JNE9GBVgfNLbuWXUCF1XnH58iWy2QVi3WRrKQRqW5V7O43MezMkUAcf9m24i5A__(self, *, newline: str='\n') -> str:
        pass
        return newline.join((line.content for line in self._lines[self._current:]))

    @property
    def gAAAAABmw_nQOpotTA74TW4gcDqYcpy_IBTBwFbiyrHdfnmTsaeo_tAe_G2MSjTPTCXJxgD1Omza4e6GQtcpGsHaaDACFcBwqw__(self) -> bool:
        pass
        return not self._lines[self._current:]

    def gAAAAABmw_nQEfhX9iAK1Qxiu_gDI_9lDZOXVgqYK2_Uxe8KX2UP4yt5jFhwtsmtQa1lXGvj_3dwUxLx5MXeLaTxYsGXQnSL3Q__(self) -> int:
        pass
        return len(self._lines[self._current:])

    @property
    def gAAAAABmw_nQZU5fSF92qTW09Xt8TvoRH4jiX1VBJ1mUXfUWDwnWz9TowFzDiiBl4gx7GZVhQSUw2AYhdZu2l8EGQxMMcRg1OQ__(self) -> int:
        pass
        return self._current

    def gAAAAABmw_nQD3RACc2YdCEQdvAmZtYUL5_ToCapAvJn57fv7SmpEHQoIawBDpP707l_CCvV9Gjpt9wBE7dOh5NaVIkkVoUhpKkVmSKKcn0abe2EGCGkrsc_(self, index: int) -> None:
        pass
        self._current = index if index >= 0 else 0

    @property
    def gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__(self) -> None | gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__:
        pass
        try:
            return self._lines[self._current]
        except IndexError:
            return None

    @property
    def gAAAAABmw_nQk_w6BCgqt9PXffXyNws97Ie1UqKrJF7VicqcYHCKPqsrN26d3IZZzg_NauTMvTm5fS824l9U7GHJYjqSjqN7OA__(self) -> None | gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__:
        pass
        try:
            self._lines[self._current]
            return self._lines[-1]
        except IndexError:
            return None

    def gAAAAABmw_nQ8METNzRfy9sLp4TQNF1cART46UsZ9QQu9Bowlu_zUj0W18LCX2X42KKYyefd1Ft8HpOhfJcSG3aaQJNKd0YEhA__(self) -> Iterable[gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__]:
        pass
        return iter(self._lines[self._current:])

    def gAAAAABmw_nQfc3m05qz6kjspLmp_Ahs7nx2Xy9YqeUcBYrDWfRDimngZo9ZWKHO7EC31OuHTrTJ5ssUcwaSKbgMTpDWGbt48A__(self, n: int=1) -> None | gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__:
        pass
        try:
            return self._lines[self._current + n]
        except IndexError:
            return None

    def gAAAAABmw_nQEa0WW0bmOvJW4MTYqNiGnBu44Y_dUiUMa4WUucD_TsDDxIBc3PTVwnGCkEC1b6QG9KUNpqhUPX0dVJq2ABQu5A__(self, n: int=1) -> None:
        pass
        self._current += n

    def gAAAAABmw_nQs8m3isHnCF2UO5PuYmzTX7ct5SJZ2oMoXau_28wum2MN_d3ThZlJrXnC6S3KjAdRx__rufpaIS8BqL9W1E3xIA__(self, n: int=1) -> None:
        pass
        self._current -= n
        if self._current < 0:
            self._current = 0

    def gAAAAABmw_nQI3OQe2GydgjKHf7uElPiVVTeuLEVmtCghm2fUxrtcTRYe6JpSMlgUAxE9OHke1Tm9U99aKuN5H09A_lbqKgG0g__(self, top_offset: int, bottom_offset: int | None, /, *, strip_min_indent: bool=False) -> gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__:
        pass
        new_lines: list[gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__] = []
        for line in self._lines[self._current + top_offset:None if bottom_offset is None else self._current + bottom_offset]:
            new_lines.append(line)
        if strip_min_indent:
            indents = [len(line.content) - len(line.content.lstrip()) for line in new_lines if not line.gAAAAABmw_nQC5lB_2n9IANSFFmCNhHIwZWX1YR75NzcTdvXfcm0lX6HZ8TFEN_fgM6_XFsc0hDxVcGjcG0J4ZfCVChQJSqjyQ__]
            if (min_indent := PositiveInt(min(indents, default=0))):
                new_lines = [line.gAAAAABmw_nQK2_rPB2FLNZmeYW1eronEd0MIIkzWnQ_h9olZJMEqQdRLCBYjwkzW2QvDqHYsuEWM268E_H1U4gvXE3xoJdIyw__(min_indent) for line in new_lines]
        return self.__class__(new_lines)

    def gAAAAABmw_nQuskGzau5BmmEAcEXCbXcZOsx0lzmLGPKnLtZKb4NSR9_8m9BIBcjBj5HQdFWNRcPJg_FDKtPygDjlEoaC6H_hQH8DR9rpvBBOJ7Da8snDHM_(self, *, start: bool=True, end: bool=True) -> gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__:
        pass
        start_index = 0
        lines = self._lines[self._current:]
        end_index = len(lines)
        if start:
            for line in lines:
                if not line.gAAAAABmw_nQC5lB_2n9IANSFFmCNhHIwZWX1YR75NzcTdvXfcm0lX6HZ8TFEN_fgM6_XFsc0hDxVcGjcG0J4ZfCVChQJSqjyQ__:
                    break
                start_index += 1
        if end:
            for line in reversed(lines):
                if not line.gAAAAABmw_nQC5lB_2n9IANSFFmCNhHIwZWX1YR75NzcTdvXfcm0lX6HZ8TFEN_fgM6_XFsc0hDxVcGjcG0J4ZfCVChQJSqjyQ__:
                    break
                end_index -= 1
        if end_index > start_index:
            return self.__class__(lines[start_index:end_index])
        else:
            return self.__class__([])

    def gAAAAABmw_nQdYv_dZiRhvw6FLVpzennZ83KkpdDhaH7jdWR1v1pij_Uadgi6AKngsxVjIM_NCPP6VeVyG1P590UnkGWIhxZFg__(self, *, stop_on_indented: bool=False, advance: bool=False) -> gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__:
        pass
        new_lines: list[gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__] = []
        for line in self._lines[self._current:]:
            if line.gAAAAABmw_nQC5lB_2n9IANSFFmCNhHIwZWX1YR75NzcTdvXfcm0lX6HZ8TFEN_fgM6_XFsc0hDxVcGjcG0J4ZfCVChQJSqjyQ__:
                break
            if stop_on_indented and line.content[0] == ' ':
                break
            new_lines.append(line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmw_nQOOZ97h90N1wYMvd1eFPHdwMZos_1Gb2ZOAdWjVL3w3ll_bAgPDUfQS72NTp0p_VFZYF_ZPpBIsLyw2HssXw6zg__(self, offset: int, until_blank: bool, /) -> Iterable[tuple[gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__, int | None]]:
        pass
        for line in self._lines[self._current + offset:]:
            len_total = len(line.content)
            if line.content and line.content[0] != ' ':
                break
            len_indent = len_total - len(line.content.lstrip())
            only_whitespace = len_total == len_indent
            if until_blank and only_whitespace:
                break
            indent = None if only_whitespace else len_indent
            yield (line, indent)

    def gAAAAABmw_nQMw5i_UouyM7NPOwQ81L1Yu6MBOgL_xKDSUdOWAsPeZ_uHPCMYvPF9uHJh2h6p7UTbCfN6mmZh1quRGoVag_3ZQ__(self, *, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__:
        pass
        new_lines: list[gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmw_nQOOZ97h90N1wYMvd1eFPHdwMZos_1Gb2ZOAdWjVL3w3ll_bAgPDUfQS72NTp0p_VFZYF_ZPpBIsLyw2HssXw6zg__(0, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmw_nQK2_rPB2FLNZmeYW1eronEd0MIIkzWnQ_h9olZJMEqQdRLCBYjwkzW2QvDqHYsuEWM268E_H1U4gvXE3xoJdIyw__(min_indent) for line in new_lines]
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmw_nQb1aLPU2EqgguRNXjxBW__6VQUUIKeM0kLNLrY9aUd5y9EYK63Vf89K2SrVicV4rgv4kc2wtZqzsFzLA0z9PdpRyPVX_KN3HHj1FSq1MF_8s_(self, *, first_indent: int=0, until_blank: bool=False, strip_indent: bool=True, strip_top: bool=True, strip_bottom: bool=False, advance: bool=False) -> gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__:
        pass
        first_indent = PositiveInt(first_indent)
        new_lines: list[gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmw_nQOOZ97h90N1wYMvd1eFPHdwMZos_1Gb2ZOAdWjVL3w3ll_bAgPDUfQS72NTp0p_VFZYF_ZPpBIsLyw2HssXw6zg__(1, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmw_nQK2_rPB2FLNZmeYW1eronEd0MIIkzWnQ_h9olZJMEqQdRLCBYjwkzW2QvDqHYsuEWM268E_H1U4gvXE3xoJdIyw__(min_indent) for line in new_lines]
        if self.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__ is not None:
            new_lines.insert(0, self.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__.gAAAAABmw_nQK2_rPB2FLNZmeYW1eronEd0MIIkzWnQ_h9olZJMEqQdRLCBYjwkzW2QvDqHYsuEWM268E_H1U4gvXE3xoJdIyw__(first_indent))
        if new_lines and advance:
            self._current += len(new_lines) - 1
        block = self.__class__(new_lines)
        if strip_top or strip_bottom:
            return block.gAAAAABmw_nQuskGzau5BmmEAcEXCbXcZOsx0lzmLGPKnLtZKb4NSR9_8m9BIBcjBj5HQdFWNRcPJg_FDKtPygDjlEoaC6H_hQH8DR9rpvBBOJ7Da8snDHM_(start=strip_top, end=strip_bottom)
        return block

    def gAAAAABmw_nQrdOIp_tA8SLkb8iLR8mLWfi0Ufr64MEpowizxOES60YntNysWO4J_Ei4zpDkYVNwaJwE2v647s1jF4TNvSOGwWF47SuZTflqkbujkc0gtdQ_(self, indent: int, *, always_first: bool=False, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__:
        pass
        indent = PositiveInt(indent)
        new_lines: list[gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__] = []
        line_index = self._current
        if always_first:
            if (line := self.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__):
                new_lines.append(line.gAAAAABmw_nQK2_rPB2FLNZmeYW1eronEd0MIIkzWnQ_h9olZJMEqQdRLCBYjwkzW2QvDqHYsuEWM268E_H1U4gvXE3xoJdIyw__(indent))
            line_index += 1
        for line in self._lines[line_index:]:
            len_total = len(line.content)
            len_indent = len_total - len(line.content.lstrip())
            if len_total != 0 and len_indent < indent:
                break
            if until_blank and len_total == len_indent:
                break
            new_lines.append(line.gAAAAABmw_nQK2_rPB2FLNZmeYW1eronEd0MIIkzWnQ_h9olZJMEqQdRLCBYjwkzW2QvDqHYsuEWM268E_H1U4gvXE3xoJdIyw__(indent) if strip_indent else line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines).gAAAAABmw_nQuskGzau5BmmEAcEXCbXcZOsx0lzmLGPKnLtZKb4NSR9_8m9BIBcjBj5HQdFWNRcPJg_FDKtPygDjlEoaC6H_hQH8DR9rpvBBOJ7Da8snDHM_(start=True, end=False)

def gAAAAABmw_nQtkxmOq0Adfp9dUP8edoD2_W5RQL9dZtzEfFIpY_Ls_CtHXaSHgXWEGyO5jQzjUBH8BDStrRoAcxVDtHdQ8qEaA__(text: str, *, tab_width: int=8, convert_whitespace: bool=True) -> Iterable[tuple[str, str]]:
    pass
    if convert_whitespace:
        text = re.sub('[\x0b\x0c]', ' ', text)
    return ((s.expandtabs(tab_width).rstrip(), s.rstrip()) for s in text.splitlines())

def gAAAAABmw_nQabd6FRgGig56sxGIcXIaQLgMdB9BpSFEDR_8bFRacDOKZYs9hdJsEYlXZbG8_Z0kiW_1x2VdXbnmHSWVgGIscatUf5V0paJqDqBjWpOsjhA_(original_string: str, expanded_indent: int, tab_size: int) -> int:
    pass
    original_indent = 0
    current_expanded_indent = 0
    for char in original_string:
        if char == '\t':
            next_tab_stop = (current_expanded_indent // tab_size + 1) * tab_size
            current_expanded_indent = next_tab_stop
        else:
            current_expanded_indent += 1
        if current_expanded_indent > expanded_indent:
            break
        original_indent += 1
    return original_indent