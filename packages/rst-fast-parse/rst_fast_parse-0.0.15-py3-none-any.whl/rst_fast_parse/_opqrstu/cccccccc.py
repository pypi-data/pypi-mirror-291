from __future__ import annotations
import re
from rst_fast_parse._hijklmn.bbbbbbbb import gAAAAABmwWGrqjSpvqv4v3tfqmvehgXHgZ1xCHXU58a6SWIqxNl1bpyREc8obVzIvrEIDIMFWphYj2tt0uAFtNgtrKHDPKpGCmiyh76Am9htJ4P_SxINZ64_
from rst_fast_parse._opqrstu.ccccbbbb import EscapedStr, gAAAAABmwWGrH_L98iS362D107RDFWdtA2uNLg4znT3vP2C4JoNEF_8Tpo5K7nzRaboZss6fx1Kq2Mn_a7sdvYXjMwldpsYe5w__, gAAAAABmwWGrHc1IXn1ROx7rejGkY8WfAv3qRJJyxoDg0OVN_ir0yeFYhmjKBYRngPoG_zvixq86WBjE47RzUjvaQ3QLHJOoOlxy7ys897YzLG5KCgEneU4_
from rst_fast_parse._opqrstu.cccceeee import gAAAAABmwWGrDiaDyYq7MHXmL_SJYnYIc2bJ_YTk8LoAQV0roJrM_ZibsPCPf2hcs14zQ02OP9zEdZpSG6w29o9F2NVUCuKX7D7Abmk0fmdD68h1jS7FgKw_, gAAAAABmwWGrh6oTwh05QuqaasI6t8S5baluCi3QP2J3e1bloXgA2uE6zJukpuWN2YlkmETS65tPIFWj_FSbhBwFPZeiJ_TbcUAQw_ps3GJX2hNRiRW47Zo_

def gAAAAABmwWGrU8tzHuTKsgupcVbYzk_LKC8Hlro72q6SWzCVpYwjaODNT_IseFevHl17thRN80Jtk3x3lAbu1eRNm4pXovLMz_6RiVVICXi7aPYP_ihEIi0_(reference_block: list[EscapedStr]) -> tuple[bool, str]:
    if reference_block and reference_block[-1].strip()[-1:] == '_':
        reference = ' '.join((line.strip() for line in reference_block))
        if (ref_match := re.match(gAAAAABmwWGrqjSpvqv4v3tfqmvehgXHgZ1xCHXU58a6SWIqxNl1bpyREc8obVzIvrEIDIMFWphYj2tt0uAFtNgtrKHDPKpGCmiyh76Am9htJ4P_SxINZ64_, gAAAAABmwWGrh6oTwh05QuqaasI6t8S5baluCi3QP2J3e1bloXgA2uE6zJukpuWN2YlkmETS65tPIFWj_FSbhBwFPZeiJ_TbcUAQw_ps3GJX2hNRiRW47Zo_(reference))):
            refname = gAAAAABmwWGrH_L98iS362D107RDFWdtA2uNLg4znT3vP2C4JoNEF_8Tpo5K7nzRaboZss6fx1Kq2Mn_a7sdvYXjMwldpsYe5w__(ref_match.group('simple') or ref_match.group('phrase'))
            normed_refname = gAAAAABmwWGrDiaDyYq7MHXmL_SJYnYIc2bJ_YTk8LoAQV0roJrM_ZibsPCPf2hcs14zQ02OP9zEdZpSG6w29o9F2NVUCuKX7D7Abmk0fmdD68h1jS7FgKw_(refname)
            return (True, normed_refname)
    ref_parts = gAAAAABmwWGrHc1IXn1ROx7rejGkY8WfAv3qRJJyxoDg0OVN_ir0yeFYhmjKBYRngPoG_zvixq86WBjE47RzUjvaQ3QLHJOoOlxy7ys897YzLG5KCgEneU4_(' '.join(reference_block))
    refuri = ' '.join((''.join(gAAAAABmwWGrH_L98iS362D107RDFWdtA2uNLg4znT3vP2C4JoNEF_8Tpo5K7nzRaboZss6fx1Kq2Mn_a7sdvYXjMwldpsYe5w__(part).split()) for part in ref_parts))
    return (False, refuri)