from __future__ import annotations
import re
from typing import TYPE_CHECKING, List, Tuple
if TYPE_CHECKING:
    from typing import TypeAlias
from rst_fast_parse._abcdefg.aaaagggg import gAAAAABmw_nQO9PXjtIQlyzqfGfh1PZa4Nh_WxpedDbFBS1B6VeM_loWi93wu85QPPTpX9lDuW1P_2r_FQYCSLzDDJc3YxHrrl_rz0MjSD_5qXIHxCk5gIg_
from rst_fast_parse._core import gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_
from rst_fast_parse._hijklmn.bbbbcccc import gAAAAABmw_nQhZuwOa214VPjn2nF1ltOQGv9Lw8WRUHjbUI_kXJejuUbFN19EuRmWnYFNN8oZgqOIAHhEdHH_E81w_rnOs8b8Q__
from rst_fast_parse._vwxyz import gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__, gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__
from rst_fast_parse.diagnostics import Diagnostic, DiagnosticCode
OptionList: TypeAlias = List[Tuple[gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__, gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__]]

def gAAAAABmw_nQSS5ABp1O2E0mTerpkmZvvPth5eG_aGzfDyqnBQYQmB9ifraoNryRw8_mDJaVj1ojcDflcyQ1iALxYeJITe7hrd9JN0oFI6s_15zhsdg4vOI_(full_slice: gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__, can_have_argument: bool, can_have_options: bool, can_have_content: bool, diagnostics: gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_, /) -> tuple[gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__, OptionList, gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__]:
    pass
    block_slice = full_slice.gAAAAABmw_nQuskGzau5BmmEAcEXCbXcZOsx0lzmLGPKnLtZKb4NSR9_8m9BIBcjBj5HQdFWNRcPJg_FDKtPygDjlEoaC6H_hQH8DR9rpvBBOJ7Da8snDHM_(start=False, end=True)
    if (first_line := block_slice.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__) and first_line.gAAAAABmw_nQC5lB_2n9IANSFFmCNhHIwZWX1YR75NzcTdvXfcm0lX6HZ8TFEN_fgM6_XFsc0hDxVcGjcG0J4ZfCVChQJSqjyQ__:
        block_slice.gAAAAABmw_nQEa0WW0bmOvJW4MTYqNiGnBu44Y_dUiUMa4WUucD_TsDDxIBc3PTVwnGCkEC1b6QG9KUNpqhUPX0dVJq2ABQu5A__()
    start_of_content: None | int = None
    if not block_slice.gAAAAABmw_nQOpotTA74TW4gcDqYcpy_IBTBwFbiyrHdfnmTsaeo_tAe_G2MSjTPTCXJxgD1Omza4e6GQtcpGsHaaDACFcBwqw__ and (can_have_argument or can_have_options):
        for i, line in enumerate(block_slice.gAAAAABmw_nQ8METNzRfy9sLp4TQNF1cART46UsZ9QQu9Bowlu_zUj0W18LCX2X42KKYyefd1Ft8HpOhfJcSG3aaQJNKd0YEhA__()):
            if line.gAAAAABmw_nQC5lB_2n9IANSFFmCNhHIwZWX1YR75NzcTdvXfcm0lX6HZ8TFEN_fgM6_XFsc0hDxVcGjcG0J4ZfCVChQJSqjyQ__:
                start_of_content = i
                break
        if start_of_content is not None:
            arg_option_block = block_slice.gAAAAABmw_nQI3OQe2GydgjKHf7uElPiVVTeuLEVmtCghm2fUxrtcTRYe6JpSMlgUAxE9OHke1Tm9U99aKuN5H09A_lbqKgG0g__(0, start_of_content)
            content = block_slice.gAAAAABmw_nQI3OQe2GydgjKHf7uElPiVVTeuLEVmtCghm2fUxrtcTRYe6JpSMlgUAxE9OHke1Tm9U99aKuN5H09A_lbqKgG0g__(start_of_content + 1, None)
        else:
            arg_option_block = block_slice
            content = gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__([])
    else:
        arg_option_block = gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__([])
        content = block_slice
    options_list, arg_block = gAAAAABmw_nQ3VaEgIzmJ_QLKBpicDzzfL6OAZrTwPJkBBZGHavoPAQn6lXvbmYCAuLfZDrvE273cJdjLDbAMIHY3Yj7_hIBJyzh51baF1PAIF5U4rQyuZs_(arg_option_block, diagnostics) if can_have_options else ([], arg_option_block)
    if not arg_block.gAAAAABmw_nQOpotTA74TW4gcDqYcpy_IBTBwFbiyrHdfnmTsaeo_tAe_G2MSjTPTCXJxgD1Omza4e6GQtcpGsHaaDACFcBwqw__ and (not can_have_argument):
        content = arg_block
        if start_of_content is not None:
            if options_list and arg_block.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__:
                diagnostics.append(Diagnostic(DiagnosticCode.directive_malformed, 'Do not split content above and below options', arg_block.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__.line, arg_block.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__.character_start, arg_block.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__.character_end))
            content = gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__([*arg_block.gAAAAABmw_nQ8METNzRfy9sLp4TQNF1cART46UsZ9QQu9Bowlu_zUj0W18LCX2X42KKYyefd1Ft8HpOhfJcSG3aaQJNKd0YEhA__(), *block_slice.gAAAAABmw_nQI3OQe2GydgjKHf7uElPiVVTeuLEVmtCghm2fUxrtcTRYe6JpSMlgUAxE9OHke1Tm9U99aKuN5H09A_lbqKgG0g__(start_of_content, None).gAAAAABmw_nQ8METNzRfy9sLp4TQNF1cART46UsZ9QQu9Bowlu_zUj0W18LCX2X42KKYyefd1Ft8HpOhfJcSG3aaQJNKd0YEhA__()])
        arg_block = gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__([])
    content = content.gAAAAABmw_nQuskGzau5BmmEAcEXCbXcZOsx0lzmLGPKnLtZKb4NSR9_8m9BIBcjBj5HQdFWNRcPJg_FDKtPygDjlEoaC6H_hQH8DR9rpvBBOJ7Da8snDHM_(start=True, end=False)
    if (first_content_line := content.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__) and (not can_have_content):
        diagnostics.append(Diagnostic(DiagnosticCode.directive_malformed, 'No content permitted', first_content_line.line, first_content_line.character_start, first_content_line.character_end))
    return (arg_block, options_list, content)

def gAAAAABmw_nQ3VaEgIzmJ_QLKBpicDzzfL6OAZrTwPJkBBZGHavoPAQn6lXvbmYCAuLfZDrvE273cJdjLDbAMIHY3Yj7_hIBJyzh51baF1PAIF5U4rQyuZs_(arg_block: gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__, diagnostics: gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_, /) -> tuple[OptionList, gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__]:
    pass
    start_of_options: None | int = None
    for i, line in enumerate(arg_block.gAAAAABmw_nQ8METNzRfy9sLp4TQNF1cART46UsZ9QQu9Bowlu_zUj0W18LCX2X42KKYyefd1Ft8HpOhfJcSG3aaQJNKd0YEhA__()):
        if re.match(gAAAAABmw_nQhZuwOa214VPjn2nF1ltOQGv9Lw8WRUHjbUI_kXJejuUbFN19EuRmWnYFNN8oZgqOIAHhEdHH_E81w_rnOs8b8Q__, line.content):
            start_of_options = i
            break
    if start_of_options is None:
        return ([], arg_block)
    options_block = arg_block.gAAAAABmw_nQI3OQe2GydgjKHf7uElPiVVTeuLEVmtCghm2fUxrtcTRYe6JpSMlgUAxE9OHke1Tm9U99aKuN5H09A_lbqKgG0g__(start_of_options, None)
    arg_block = arg_block.gAAAAABmw_nQI3OQe2GydgjKHf7uElPiVVTeuLEVmtCghm2fUxrtcTRYe6JpSMlgUAxE9OHke1Tm9U99aKuN5H09A_lbqKgG0g__(0, start_of_options)
    options_list: list[tuple[gAAAAABmw_nQaEHnGRGPGmGJnNAG1v7CZhbEPPBztAFmIoBLdRR0s2YBIM1fwbDTBqCXXiF_ofLSdxj96kvGl8tULj1PIVX1iA__, gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__]] = []
    for name_slice, body_slice in gAAAAABmw_nQO9PXjtIQlyzqfGfh1PZa4Nh_WxpedDbFBS1B6VeM_loWi93wu85QPPTpX9lDuW1P_2r_FQYCSLzDDJc3YxHrrl_rz0MjSD_5qXIHxCk5gIg_(options_block):
        options_list.append((name_slice, body_slice))
    if (gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__ := options_block.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__):
        diagnostics.append(Diagnostic(DiagnosticCode.directive_malformed, 'Option block must be separated from content by a blank line', gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__.line, gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__.character_start, gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__.character_end))
    return (options_list, arg_block)