from __future__ import annotations
import re
from typing import Iterable, NewType, Sequence
PositiveInt = NewType('PositiveInt', int)

class gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__:
    __slots__ = ('_content', '_source', '_offset_line', '_offset_char')

    def __init__(self, content: str, /, offset_line: int, offset_char: int, *, source: str | None=None) -> None:
        self._content = content
        self._source = source
        self._offset_line = offset_line
        self._offset_char = offset_char

    def __repr__(self) -> str:
        return f'gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__({self._content!r}, line={self._offset_line}, char={self._offset_char})'

    @property
    def content(self) -> str:
        return self._content

    @property
    def line(self) -> int:
        return self._offset_line

    @property
    def indent(self) -> int:
        return self._offset_char

    @property
    def gAAAAABmwWGrviQK31PhhbhzPZxF037YnOW0fR_BjAngEmj_10KNheIBLl8H04Rr5kDaFr0R1IfAKVBM9iESOb_5DhTnG7s3_w__(self) -> bool:
        return not self._content.strip()

    def gAAAAABmwWGrGbF2ZE8yY4SmPOyX_n9UCVGXx5a5tCtSqxCt5WyQvnKi_e8nVJehQeIIH_wpwBYL6WOsZ7hU_Kxtr2vmFkDHIQ__(self, /, start: PositiveInt | None, stop: None | PositiveInt=None) -> gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__:
        assert start is None or start >= 0
        assert stop is None or stop >= 0
        if self._offset_char is None:
            new_offset = None
        else:
            new_offset = self._offset_char + (start or 0)
        return gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__(self._content[start:stop], offset_line=self._offset_line, offset_char=new_offset, source=self._source)

    def gAAAAABmwWGrmj8NDZybBO_HyrB1N4Q4VVzj_suOUrF4Y7tz__R7YdZgOyjw8etygJDxAZzNI8ayUlGe4zEa1ZDIs6k5C_VFtw__(self, n: PositiveInt) -> gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__:
        assert n >= 0
        new_offset = None if self._offset_char is None else self._offset_char + n
        return gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__(self._content[n:], offset_line=self._offset_line, offset_char=new_offset, source=self._source)

    def rstrip(self) -> gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__:
        return gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__(self._content.rstrip(), offset_line=self._offset_line, offset_char=self._offset_char, source=self._source)

class gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__:
    __slots__ = ('_lines', '_current')

    def __init__(self, lines: Sequence[gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__]) -> None:
        self._lines = lines
        self._current: int = 0
        'The current line index,\n\n        Note it can never be negative, but can be greater than the number of lines.\n        '

    def __repr__(self) -> str:
        return f'gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__(lines={len(self._lines)}, index={self._current})'

    def gAAAAABmwWGrpBJgOdwKShenuDn9xpbNoYseOyE9PvGBySLvSYcarvlBh9joVXi0OUaZe7HlmFatYoWjcJ7XVxUqykiRji_46g__(self, *, newline: str='\n') -> str:
        return newline.join((line.content for line in self._lines[self._current:]))

    @property
    def gAAAAABmwWGrfaZ44CFljUw7I7xUyNnTTKFn2xM5a3ZzaAfTESvxeb15IZ9__Dr29oTwqVGaPwyjS3FgOz4W4j8IJuJCx3yepg__(self) -> bool:
        return not self._lines[self._current:]

    def gAAAAABmwWGrvh99UDuHNFkUU1GeWUpb4lqbnkwljw3FcRRaXX1L46ND52bOx80IJ7G0JdjuE5XRWym5rmyIi3DkoMI_cJAG9A__(self) -> int:
        return len(self._lines[self._current:])

    @property
    def gAAAAABmwWGrO1zXInmQxsYD3P66ptxLinxbc7MrLmLnzTuIQiV2uRwLclKLmNAddl4jj_0azEmOygfTRI272ua45mEgCJWajw__(self) -> int:
        return self._current

    def gAAAAABmwWGrjEn58uQkEP1CVrsGptHLoxNAwpCfligRwIsOLSRyUENykoLF1cQWWc45uZ2SlgTLNLZ1RMAjF9Bjp_y3JLZ1EINRrrGQ30_crdy8FnWuZB0_(self, index: int) -> None:
        self._current = index if index >= 0 else 0

    @property
    def gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__(self) -> None | gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__:
        try:
            return self._lines[self._current]
        except IndexError:
            return None

    @property
    def gAAAAABmwWGri0a4TPKygBbkCJ2jlddcGvs2nelefvke5Rm3AHDPfu_yLeYcJ94us_T6_Jw6sgnJHKCrqa5oJjf6eKFKJfRjgA__(self) -> None | gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__:
        try:
            self._lines[self._current]
            return self._lines[-1]
        except IndexError:
            return None

    def gAAAAABmwWGrQt_tLZO11j2k5DKHVSb01J74hlIY3_S0CIMhb2VMZiP6JfdpKjvq3JcY_PREuxW4Ju3_xRqyAXycg46bMi0Fvg__(self) -> Iterable[gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__]:
        return iter(self._lines[self._current:])

    def gAAAAABmwWGrmOEG_2qPdjv1v7BDUmzXXqUhf7bC4w_MUDRZ_b99VmP0dgOwECzomS_fcluPKbpxX_uz9gPD66Gj9HakHOw4fw__(self, n: int=1) -> None | gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__:
        try:
            return self._lines[self._current + n]
        except IndexError:
            return None

    def gAAAAABmwWGrzKoi5rLt43aBQpECwFju_ggqUVMdpr3g0c2l0fKyqmdgIyqxrfKDXXQt1cZdMtHs2NPcmIqbRtPAfaTqu6iqjQ__(self, n: int=1) -> None:
        self._current += n

    def gAAAAABmwWGr_9KC7xUQ_PFMXyw6PSCxI8tk783MiHSTz3AReWLjI_QHVIWq2NUf75ud2mQukhjhTNzx3S8DD9EHC8SzxuezkA__(self, n: int=1) -> None:
        self._current -= n
        if self._current < 0:
            self._current = 0

    def gAAAAABmwWGrZ_OeWtFMjvP_QJr14bWY83sxqR5CEba2a2SKciJlVx6S3x_9j4itYWr31ODs_28u1K_73plYhFrHVcLc4r9qtw__(self, top_offset: int, bottom_offset: int | None, /, *, start_offset: PositiveInt | None=None, stop_offset: PositiveInt | None=None, strip_min_indent: bool=False) -> gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__:
        new_lines: list[gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__] = []
        for line in self._lines[self._current + top_offset:None if bottom_offset is None else self._current + bottom_offset]:
            if start_offset is None and stop_offset is None:
                new_lines.append(line)
            else:
                new_lines.append(line.gAAAAABmwWGrGbF2ZE8yY4SmPOyX_n9UCVGXx5a5tCtSqxCt5WyQvnKi_e8nVJehQeIIH_wpwBYL6WOsZ7hU_Kxtr2vmFkDHIQ__(start_offset, stop_offset))
        if strip_min_indent:
            indents = [len(line.content) - len(line.content.lstrip()) for line in new_lines if not line.gAAAAABmwWGrviQK31PhhbhzPZxF037YnOW0fR_BjAngEmj_10KNheIBLl8H04Rr5kDaFr0R1IfAKVBM9iESOb_5DhTnG7s3_w__]
            if (min_indent := PositiveInt(min(indents, default=0))):
                new_lines = [line.gAAAAABmwWGrGbF2ZE8yY4SmPOyX_n9UCVGXx5a5tCtSqxCt5WyQvnKi_e8nVJehQeIIH_wpwBYL6WOsZ7hU_Kxtr2vmFkDHIQ__(min_indent) for line in new_lines]
        return self.__class__(new_lines)

    def gAAAAABmwWGr0uMPMiYNw3_CSmh1bZjGBJlBqEvDO4B5jQuTt3HHFa_cQi3kMy1rtB6CxzKaNXPJ1T5y8ulzrOL2oBkLF_y1_RLhLqPMQfv9VzLvpedKBps_(self, *, start: bool=True, end: bool=True) -> gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__:
        start_index = 0
        lines = self._lines[self._current:]
        end_index = len(lines)
        if start:
            for line in lines:
                if not line.gAAAAABmwWGrviQK31PhhbhzPZxF037YnOW0fR_BjAngEmj_10KNheIBLl8H04Rr5kDaFr0R1IfAKVBM9iESOb_5DhTnG7s3_w__:
                    break
                start_index += 1
        if end:
            for line in reversed(lines):
                if not line.gAAAAABmwWGrviQK31PhhbhzPZxF037YnOW0fR_BjAngEmj_10KNheIBLl8H04Rr5kDaFr0R1IfAKVBM9iESOb_5DhTnG7s3_w__:
                    break
                end_index -= 1
        if end_index > start_index:
            return self.__class__(lines[start_index:end_index])
        else:
            return self.__class__([])

    def gAAAAABmwWGrUs0Ngnfo_kkHcakPtPnY_Xig3SgllwSXUn95XN2SHZ_ygKYtZAB7Yhj_W2sZ8d0xFnJmInposS4UHUkBvuU_Ug__(self, *, stop_on_indented: bool=False, advance: bool=False) -> gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__:
        new_lines: list[gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__] = []
        for line in self._lines[self._current:]:
            if line.gAAAAABmwWGrviQK31PhhbhzPZxF037YnOW0fR_BjAngEmj_10KNheIBLl8H04Rr5kDaFr0R1IfAKVBM9iESOb_5DhTnG7s3_w__:
                break
            if stop_on_indented and line.content[0] == ' ':
                break
            new_lines.append(line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmwWGrsstTWtG4dD7pEb6WnM9dzYwTkHG4028_eZifl0oGhBAilEKNqfKWy0pM2ScXOBc7_bWow2Ih_FRk4HYC37ELeA__(self, offset: int, until_blank: bool, /) -> Iterable[tuple[gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__, int | None]]:
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

    def gAAAAABmwWGrUkSxeek_up5aYzUrBzyCNSw3OkZYbJ8pPSh4XUjOE36ri_eClIDXJed5aeiHXmf3C9lRhjSD3UVMcNvz6tfndA__(self, *, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__:
        new_lines: list[gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmwWGrsstTWtG4dD7pEb6WnM9dzYwTkHG4028_eZifl0oGhBAilEKNqfKWy0pM2ScXOBc7_bWow2Ih_FRk4HYC37ELeA__(0, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmwWGrGbF2ZE8yY4SmPOyX_n9UCVGXx5a5tCtSqxCt5WyQvnKi_e8nVJehQeIIH_wpwBYL6WOsZ7hU_Kxtr2vmFkDHIQ__(min_indent) for line in new_lines]
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmwWGrq0ZRJyGe_kuwohKwuYWivwu2Kc9PxUCOfSwqsi_6bhK2jQOstoqBUXsExvEpdpMO0rlAKgFF_1G_EbA6ACvypVVe4zUn3GKA5i1jVPbZURg_(self, *, first_indent: int=0, until_blank: bool=False, strip_indent: bool=True, strip_top: bool=True, strip_bottom: bool=False, advance: bool=False) -> gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__:
        first_indent = PositiveInt(first_indent)
        new_lines: list[gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmwWGrsstTWtG4dD7pEb6WnM9dzYwTkHG4028_eZifl0oGhBAilEKNqfKWy0pM2ScXOBc7_bWow2Ih_FRk4HYC37ELeA__(1, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmwWGrGbF2ZE8yY4SmPOyX_n9UCVGXx5a5tCtSqxCt5WyQvnKi_e8nVJehQeIIH_wpwBYL6WOsZ7hU_Kxtr2vmFkDHIQ__(min_indent) for line in new_lines]
        if self.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__ is not None:
            new_lines.insert(0, self.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__.gAAAAABmwWGrGbF2ZE8yY4SmPOyX_n9UCVGXx5a5tCtSqxCt5WyQvnKi_e8nVJehQeIIH_wpwBYL6WOsZ7hU_Kxtr2vmFkDHIQ__(first_indent))
        if new_lines and advance:
            self._current += len(new_lines) - 1
        block = self.__class__(new_lines)
        if strip_top or strip_bottom:
            return block.gAAAAABmwWGr0uMPMiYNw3_CSmh1bZjGBJlBqEvDO4B5jQuTt3HHFa_cQi3kMy1rtB6CxzKaNXPJ1T5y8ulzrOL2oBkLF_y1_RLhLqPMQfv9VzLvpedKBps_(start=strip_top, end=strip_bottom)
        return block

    def gAAAAABmwWGrwBnbVBgDPaePkaXwNrFt_hz6znu9z6MU2ON75_JtV6jNMIP0XhTMELUVJ_Ckc995YwHRv2qcTziuDuDRapaHJRUMcmXETlsgjAnUaWXOVzM_(self, indent: int, *, always_first: bool=False, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__:
        indent = PositiveInt(indent)
        new_lines: list[gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__] = []
        line_index = self._current
        if always_first:
            if (line := self.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__):
                new_lines.append(line.gAAAAABmwWGrGbF2ZE8yY4SmPOyX_n9UCVGXx5a5tCtSqxCt5WyQvnKi_e8nVJehQeIIH_wpwBYL6WOsZ7hU_Kxtr2vmFkDHIQ__(indent))
            line_index += 1
        for line in self._lines[line_index:]:
            len_total = len(line.content)
            len_indent = len_total - len(line.content.lstrip())
            if len_total != 0 and len_indent < indent:
                break
            if until_blank and len_total == len_indent:
                break
            new_lines.append(line.gAAAAABmwWGrGbF2ZE8yY4SmPOyX_n9UCVGXx5a5tCtSqxCt5WyQvnKi_e8nVJehQeIIH_wpwBYL6WOsZ7hU_Kxtr2vmFkDHIQ__(indent) if strip_indent else line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines).gAAAAABmwWGr0uMPMiYNw3_CSmh1bZjGBJlBqEvDO4B5jQuTt3HHFa_cQi3kMy1rtB6CxzKaNXPJ1T5y8ulzrOL2oBkLF_y1_RLhLqPMQfv9VzLvpedKBps_(start=True, end=False)

def gAAAAABmwWGr2fF80WCcbAjWgOA5DPVUNk4GExQqOogYz0odsB5udXwkjbdt8OFLevbDg0BLol0lflFcGV9tFoptpx4L7bCKlSrQ3R6FWbtEnVCZmI_RfOc_(text: str, *, tab_width: int=8, convert_whitespace: bool=True) -> list[str]:
    if convert_whitespace:
        text = re.sub('[\x0b\x0c]', ' ', text)
    return [s.expandtabs(tab_width).rstrip() for s in text.splitlines()]