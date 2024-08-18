from __future__ import annotations
import re
from typing import TYPE_CHECKING, List, Tuple
if TYPE_CHECKING:
    from typing import TypeAlias
from rst_fast_parse._abcdefg.aaaagggg import gAAAAABmwWGrN7mi43jdZFVNY9I8zAXvmZ8sTtkKKqpmXcocps475E3MFVW1YASPIBHQXtDasoMJYfLTKWf7qEmL66wZLB1D8nqZuT_GhcYLeqHzhXBQakc_
from rst_fast_parse.core import gAAAAABmwWGrzWmXziR9LtwT29NtRBRBSfcBCYyltqOvApGVcp9MdZNrYj8CRXUKd0gV_nxeGEu8dgSnPA6c2_BkFGfylp9RjS7J4De8YmchngfNgCuZhWA_
from rst_fast_parse.diagnostics import Diagnostic, DiagnosticCode
from rst_fast_parse._hijklmn.bbbbbbbb import gAAAAABmwWGrdzh_0XVxbcs9fYh6Gz1uNtYyvd4HCrZnWE0eQ1Xa8nz2YG9JGq1CqwGjBIc21_Z6kLWazNKr_19z0vVqJ8gW6A__
from rst_fast_parse._vwxyz import gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__, gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__
OptionList: TypeAlias = List[Tuple[gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__, gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__]]

def gAAAAABmwWGrzaYnV_04SE3maH_xHwbFp7KCl2MPU9ZThgZMrgJ37g8FRFWNeprC6T_93I7xQKOu3IeqDAsPXG5FmqbNGUmArbh91VgwpFu1dHfVhX_8t_I_(full_slice: gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__, can_have_argument: bool, can_have_options: bool, can_have_content: bool, diagnostics: gAAAAABmwWGrzWmXziR9LtwT29NtRBRBSfcBCYyltqOvApGVcp9MdZNrYj8CRXUKd0gV_nxeGEu8dgSnPA6c2_BkFGfylp9RjS7J4De8YmchngfNgCuZhWA_, /) -> tuple[gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__, OptionList, gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__]:
    block_slice = full_slice.gAAAAABmwWGr0uMPMiYNw3_CSmh1bZjGBJlBqEvDO4B5jQuTt3HHFa_cQi3kMy1rtB6CxzKaNXPJ1T5y8ulzrOL2oBkLF_y1_RLhLqPMQfv9VzLvpedKBps_(start=False, end=True)
    if (first_line := block_slice.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__) and first_line.gAAAAABmwWGrviQK31PhhbhzPZxF037YnOW0fR_BjAngEmj_10KNheIBLl8H04Rr5kDaFr0R1IfAKVBM9iESOb_5DhTnG7s3_w__:
        block_slice.gAAAAABmwWGrzKoi5rLt43aBQpECwFju_ggqUVMdpr3g0c2l0fKyqmdgIyqxrfKDXXQt1cZdMtHs2NPcmIqbRtPAfaTqu6iqjQ__()
    start_of_content: None | int = None
    if not block_slice.gAAAAABmwWGrfaZ44CFljUw7I7xUyNnTTKFn2xM5a3ZzaAfTESvxeb15IZ9__Dr29oTwqVGaPwyjS3FgOz4W4j8IJuJCx3yepg__ and (can_have_argument or can_have_options):
        for i, line in enumerate(block_slice.gAAAAABmwWGrQt_tLZO11j2k5DKHVSb01J74hlIY3_S0CIMhb2VMZiP6JfdpKjvq3JcY_PREuxW4Ju3_xRqyAXycg46bMi0Fvg__()):
            if line.gAAAAABmwWGrviQK31PhhbhzPZxF037YnOW0fR_BjAngEmj_10KNheIBLl8H04Rr5kDaFr0R1IfAKVBM9iESOb_5DhTnG7s3_w__:
                start_of_content = i
                break
        if start_of_content is not None:
            arg_option_block = block_slice.gAAAAABmwWGrZ_OeWtFMjvP_QJr14bWY83sxqR5CEba2a2SKciJlVx6S3x_9j4itYWr31ODs_28u1K_73plYhFrHVcLc4r9qtw__(0, start_of_content)
            content = block_slice.gAAAAABmwWGrZ_OeWtFMjvP_QJr14bWY83sxqR5CEba2a2SKciJlVx6S3x_9j4itYWr31ODs_28u1K_73plYhFrHVcLc4r9qtw__(start_of_content + 1, None)
        else:
            arg_option_block = block_slice
            content = gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__([])
    else:
        arg_option_block = gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__([])
        content = block_slice
    options_list, arg_block = gAAAAABmwWGr1d0hpptDbmuQ410J1xvHZyNFoGk_liGTGE3h8V5FYtGwxgSSdYLEAuwUe90HxUh_M_q63eVAt0VOFZv5QW2pucZPj4vvUZG1IPbMo3FGWcc_(arg_option_block, diagnostics) if can_have_options else ([], arg_option_block)
    if not arg_block.gAAAAABmwWGrfaZ44CFljUw7I7xUyNnTTKFn2xM5a3ZzaAfTESvxeb15IZ9__Dr29oTwqVGaPwyjS3FgOz4W4j8IJuJCx3yepg__ and (not can_have_argument):
        content = arg_block
        if start_of_content is not None:
            if options_list and arg_block.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__:
                diagnostics.append(Diagnostic(DiagnosticCode.directive_malformed, 'Do not split content above and below options', arg_block.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__.line))
            content = gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__([*arg_block.gAAAAABmwWGrQt_tLZO11j2k5DKHVSb01J74hlIY3_S0CIMhb2VMZiP6JfdpKjvq3JcY_PREuxW4Ju3_xRqyAXycg46bMi0Fvg__(), *block_slice.gAAAAABmwWGrZ_OeWtFMjvP_QJr14bWY83sxqR5CEba2a2SKciJlVx6S3x_9j4itYWr31ODs_28u1K_73plYhFrHVcLc4r9qtw__(start_of_content, None).gAAAAABmwWGrQt_tLZO11j2k5DKHVSb01J74hlIY3_S0CIMhb2VMZiP6JfdpKjvq3JcY_PREuxW4Ju3_xRqyAXycg46bMi0Fvg__()])
        arg_block = gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__([])
    content = content.gAAAAABmwWGr0uMPMiYNw3_CSmh1bZjGBJlBqEvDO4B5jQuTt3HHFa_cQi3kMy1rtB6CxzKaNXPJ1T5y8ulzrOL2oBkLF_y1_RLhLqPMQfv9VzLvpedKBps_(start=True, end=False)
    if (first_content_line := content.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__) and (not can_have_content):
        diagnostics.append(Diagnostic(DiagnosticCode.directive_malformed, 'No content permitted', first_content_line.line))
    return (arg_block, options_list, content)

def gAAAAABmwWGr1d0hpptDbmuQ410J1xvHZyNFoGk_liGTGE3h8V5FYtGwxgSSdYLEAuwUe90HxUh_M_q63eVAt0VOFZv5QW2pucZPj4vvUZG1IPbMo3FGWcc_(arg_block: gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__, diagnostics: gAAAAABmwWGrzWmXziR9LtwT29NtRBRBSfcBCYyltqOvApGVcp9MdZNrYj8CRXUKd0gV_nxeGEu8dgSnPA6c2_BkFGfylp9RjS7J4De8YmchngfNgCuZhWA_, /) -> tuple[OptionList, gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__]:
    start_of_options: None | int = None
    for i, line in enumerate(arg_block.gAAAAABmwWGrQt_tLZO11j2k5DKHVSb01J74hlIY3_S0CIMhb2VMZiP6JfdpKjvq3JcY_PREuxW4Ju3_xRqyAXycg46bMi0Fvg__()):
        if re.match(gAAAAABmwWGrdzh_0XVxbcs9fYh6Gz1uNtYyvd4HCrZnWE0eQ1Xa8nz2YG9JGq1CqwGjBIc21_Z6kLWazNKr_19z0vVqJ8gW6A__, line.content):
            start_of_options = i
            break
    if start_of_options is None:
        return ([], arg_block)
    options_block = arg_block.gAAAAABmwWGrZ_OeWtFMjvP_QJr14bWY83sxqR5CEba2a2SKciJlVx6S3x_9j4itYWr31ODs_28u1K_73plYhFrHVcLc4r9qtw__(start_of_options, None)
    arg_block = arg_block.gAAAAABmwWGrZ_OeWtFMjvP_QJr14bWY83sxqR5CEba2a2SKciJlVx6S3x_9j4itYWr31ODs_28u1K_73plYhFrHVcLc4r9qtw__(0, start_of_options)
    options_list: list[tuple[gAAAAABmwWGrDpx6_EuaE4jd2TaDVxONMh94igGapCm2AL3Vtf4G6EneKlAiB6xBO7ZskMiXkajPuo6hlD2ZnjrMP3Ime1V9HQ__, gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__]] = []
    for name_slice, body_slice in gAAAAABmwWGrN7mi43jdZFVNY9I8zAXvmZ8sTtkKKqpmXcocps475E3MFVW1YASPIBHQXtDasoMJYfLTKWf7qEmL66wZLB1D8nqZuT_GhcYLeqHzhXBQakc_(options_block):
        options_list.append((name_slice, body_slice))
    if (gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__ := options_block.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__):
        diagnostics.append(Diagnostic(DiagnosticCode.directive_malformed, 'Option block must be separated from content by a blank line', gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__.line))
    return (options_list, arg_block)