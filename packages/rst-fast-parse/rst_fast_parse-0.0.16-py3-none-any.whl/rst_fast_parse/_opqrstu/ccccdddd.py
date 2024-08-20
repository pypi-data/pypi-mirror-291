from __future__ import annotations
from typing import Sequence
from rst_fast_parse.nodes.block import BlockNodeProtocol, SectionNode, SectionTitleNode

def gAAAAABmw_nQA4hXVZWZ7x8u5Fr9W4c8iJxrbROY2P8uKoprVRQEhpSrFVwuKbiUviV9Zt6l1xtMmHhpf3zwl7CzH94ned4CUj_ZlyEpvHLB_PhFv3TqDd4_(nodes: Sequence[BlockNodeProtocol], styles: list[str], parent: SectionNode | None=None, parent_level: int | None=None, /) -> Sequence[BlockNodeProtocol]:
    pass
    new_nodes: list[BlockNodeProtocol] = []
    i = -1
    while (i := (i + 1)) or True:
        try:
            el = nodes[i]
        except IndexError:
            break
        if not isinstance(el, SectionTitleNode):
            new_nodes.append(el)
            continue
        next_level = styles.index(el.style)
        initial_i = i
        while True:
            try:
                child = nodes[i + 1]
            except IndexError:
                break
            if isinstance(child, SectionTitleNode) and styles.index(child.style) <= next_level:
                break
            i += 1
        section_nodes = [nodes[j] for j in range(initial_i + 1, i + 1)]
        section = SectionNode(title=el)
        section.extend(gAAAAABmw_nQA4hXVZWZ7x8u5Fr9W4c8iJxrbROY2P8uKoprVRQEhpSrFVwuKbiUviV9Zt6l1xtMmHhpf3zwl7CzH94ned4CUj_ZlyEpvHLB_PhFv3TqDd4_(section_nodes, styles, section, next_level))
        if parent_level is not None:
            for _ in range(next_level - parent_level - 1):
                _section = SectionNode(None)
                _section.append(section)
                section = _section
        new_nodes.append(section)
    return new_nodes