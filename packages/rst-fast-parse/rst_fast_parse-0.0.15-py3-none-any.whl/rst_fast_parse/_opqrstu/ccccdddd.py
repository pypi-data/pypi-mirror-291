from __future__ import annotations
from typing import Sequence
from rst_fast_parse.elements import ElementProtocol, SectionElement, SectionTitleElement

def gAAAAABmwWGrsEI3vpgJUWzGIztT2tQBu1PWLsiR8kG27vO9XIFDlcjHqruNiHg_u74fUe4XTMRN0Xl8frmawrH85yEC_DUiTLEF6eunsoH3K65PV93pIZk_(elements: Sequence[ElementProtocol], styles: list[str], parent: SectionElement | None=None, parent_level: int | None=None, /) -> Sequence[ElementProtocol]:
    new_elements: list[ElementProtocol] = []
    i = -1
    while (i := (i + 1)) or True:
        try:
            el = elements[i]
        except IndexError:
            break
        if not isinstance(el, SectionTitleElement):
            new_elements.append(el)
            continue
        next_level = styles.index(el.style)
        initial_i = i
        while True:
            try:
                child = elements[i + 1]
            except IndexError:
                break
            if isinstance(child, SectionTitleElement) and styles.index(child.style) <= next_level:
                break
            i += 1
        section_elements = [elements[j] for j in range(initial_i + 1, i + 1)]
        section = SectionElement(title=el)
        section.extend(gAAAAABmwWGrsEI3vpgJUWzGIztT2tQBu1PWLsiR8kG27vO9XIFDlcjHqruNiHg_u74fUe4XTMRN0Xl8frmawrH85yEC_DUiTLEF6eunsoH3K65PV93pIZk_(section_elements, styles, section, next_level))
        if parent_level is not None:
            for _ in range(next_level - parent_level - 1):
                _section = SectionElement(None)
                _section.append(section)
                section = _section
        new_elements.append(section)
    return new_elements