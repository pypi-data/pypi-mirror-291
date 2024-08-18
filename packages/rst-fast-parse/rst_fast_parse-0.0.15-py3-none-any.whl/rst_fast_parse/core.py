from __future__ import annotations
from enum import Enum
from typing import Protocol, Sequence, TypedDict
from rst_fast_parse.diagnostics import Diagnostic, DiagnosticList
from rst_fast_parse.elements import ElementProtocol, RootElement
from rst_fast_parse._vwxyz import gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__

class gAAAAABmwWGrmZpA57O5ROYSae7pL3VIB2meq1webJNcny0SP7xoT0mzcmDb2XEjDcmzP4AD51XaPT4PYXRQL8xw_fKs_W1eEg__:

    def __init__(self, block_parsers: Sequence[gAAAAABmwWGrkanrBNHaKw_Pe_Hh1VuQmMD_RNwoeo4sqkykLle0cDVgWLbrtA_6YhYodvmGgyEKlYaaZADg8dXc6Fxq5MgAzA__], directives: dict[str, gAAAAABmwWGrDIpYZZ7yYdeb0mE6VyfwKXsWXOVkKKo_Xsxa7c_vaTF7faSPPAE3NOA2bmatqA5c8EXH1ybuWiSvecrmPHvBLg__], *, gAAAAABmwWGrSMYKPvoK4J_KvLi9aRqMqLjCy1ML2IBfBT9WSaODJDoh8qjGLzDZvb15Qy7O3CFB__OoEBH8_c_u_ilRPZ2klQ__: bool=True) -> None:
        self._gAAAAABmwWGrSMYKPvoK4J_KvLi9aRqMqLjCy1ML2IBfBT9WSaODJDoh8qjGLzDZvb15Qy7O3CFB__OoEBH8_c_u_ilRPZ2klQ__ = gAAAAABmwWGrSMYKPvoK4J_KvLi9aRqMqLjCy1ML2IBfBT9WSaODJDoh8qjGLzDZvb15Qy7O3CFB__OoEBH8_c_u_ilRPZ2klQ__
        self._block_parsers = block_parsers
        self._directives = directives

    @property
    def gAAAAABmwWGrSMYKPvoK4J_KvLi9aRqMqLjCy1ML2IBfBT9WSaODJDoh8qjGLzDZvb15Qy7O3CFB__OoEBH8_c_u_ilRPZ2klQ__(self) -> bool:
        return self._gAAAAABmwWGrSMYKPvoK4J_KvLi9aRqMqLjCy1ML2IBfBT9WSaODJDoh8qjGLzDZvb15Qy7O3CFB__OoEBH8_c_u_ilRPZ2klQ__

    @property
    def directives(self) -> dict[str, gAAAAABmwWGrDIpYZZ7yYdeb0mE6VyfwKXsWXOVkKKo_Xsxa7c_vaTF7faSPPAE3NOA2bmatqA5c8EXH1ybuWiSvecrmPHvBLg__]:
        return self._directives

    def gAAAAABmwWGroPJVNkn7_RsYTIeEOUlOwnAGBAIuYZTqBy8xi8aPuOQewKKwrSCFf3bYCFpsmW7zqzCIjqR3AQjaChgEUtdWYA__(self, source: gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__) -> tuple[RootElement, DiagnosticList]:
        end_of_file = False
        start = source.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__.line if source.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__ else 0
        end = source.gAAAAABmwWGri0a4TPKygBbkCJ2jlddcGvs2nelefvke5Rm3AHDPfu_yLeYcJ94us_T6_Jw6sgnJHKCrqa5oJjf6eKFKJfRjgA__.line if source.gAAAAABmwWGri0a4TPKygBbkCJ2jlddcGvs2nelefvke5Rm3AHDPfu_yLeYcJ94us_T6_Jw6sgnJHKCrqa5oJjf6eKFKJfRjgA__ else 0
        parent = RootElement((start, end))
        diagnostics: list[Diagnostic] = []
        while not end_of_file:
            for parser in self._block_parsers:
                result = parser(source, parent, diagnostics, self)
                if result == gAAAAABmwWGrxEdHoQSKE02clOegOJ_5lPgQwlsXEOyi5eh9aYNkp_AmISApxzM1Nvutriz6C9vU8u8S7neMTGcDxMypHVvzQpDJMoEBB7rp6prZahXzZtE_.gAAAAABmwWGrL7Ij4GFDISYMvrEibdwjwsd7YqgYzwhwKTjepq5e2kiVsCuPZQnwyQYGKJrCatmJJwvBjMYD0sQsVaV1fA24Eg__:
                    break
                elif result == gAAAAABmwWGrxEdHoQSKE02clOegOJ_5lPgQwlsXEOyi5eh9aYNkp_AmISApxzM1Nvutriz6C9vU8u8S7neMTGcDxMypHVvzQpDJMoEBB7rp6prZahXzZtE_.gAAAAABmwWGroP_f4JEoXevKxlQ3yEGUHmb4HI2hS7XjO5rtDqX63n8PAlDIHUAcY6VM2_ViIbq3LPo9h63i5Bw9vrL6DqpUIg__:
                    continue
                elif result == gAAAAABmwWGrxEdHoQSKE02clOegOJ_5lPgQwlsXEOyi5eh9aYNkp_AmISApxzM1Nvutriz6C9vU8u8S7neMTGcDxMypHVvzQpDJMoEBB7rp6prZahXzZtE_.gAAAAABmwWGrS_Ta5Cm8PVp3FYVMUfRUtx0GMd_oiE8W6WZIIfrJ1amWPnlL1qAJ1JqxgnYP8csSmNBGc83bGOI2TzjWPUi0Pw__:
                    end_of_file = True
                    break
                else:
                    raise RuntimeError(f'Unknown parser result: {result!r}')
            else:
                if (line := source.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__):
                    raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
            source.gAAAAABmwWGrzKoi5rLt43aBQpECwFju_ggqUVMdpr3g0c2l0fKyqmdgIyqxrfKDXXQt1cZdMtHs2NPcmIqbRtPAfaTqu6iqjQ__()
            if source.gAAAAABmwWGrfaZ44CFljUw7I7xUyNnTTKFn2xM5a3ZzaAfTESvxeb15IZ9__Dr29oTwqVGaPwyjS3FgOz4W4j8IJuJCx3yepg__:
                break
        return (parent, diagnostics)

    def gAAAAABmwWGrR_kR1u1tn0JORjJsNka3P3cawZvY2fS_2k_FF64_D9ifPMn1_EKEQI7zczzKsfMojKxX8jPbdJlKoB5QXhF7YA__(self, source: gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__, parent: gAAAAABmwWGrGEP3mtga7I7_FhLLQHNdnfd4jKSK8Cq3xDtEZGR98YI4BsJ7FUBrpz81wozmMum1W6FskJlzDfA_ra8NUuKSpQ__, diagnostics: gAAAAABmwWGrzWmXziR9LtwT29NtRBRBSfcBCYyltqOvApGVcp9MdZNrYj8CRXUKd0gV_nxeGEu8dgSnPA6c2_BkFGfylp9RjS7J4De8YmchngfNgCuZhWA_, /) -> None:
        old_gAAAAABmwWGrSMYKPvoK4J_KvLi9aRqMqLjCy1ML2IBfBT9WSaODJDoh8qjGLzDZvb15Qy7O3CFB__OoEBH8_c_u_ilRPZ2klQ__ = self._gAAAAABmwWGrSMYKPvoK4J_KvLi9aRqMqLjCy1ML2IBfBT9WSaODJDoh8qjGLzDZvb15Qy7O3CFB__OoEBH8_c_u_ilRPZ2klQ__
        try:
            self._gAAAAABmwWGrSMYKPvoK4J_KvLi9aRqMqLjCy1ML2IBfBT9WSaODJDoh8qjGLzDZvb15Qy7O3CFB__OoEBH8_c_u_ilRPZ2klQ__ = False
            end_of_file = False
            while not end_of_file:
                for parser in self._block_parsers:
                    result = parser(source, parent, diagnostics, self)
                    if result == gAAAAABmwWGrxEdHoQSKE02clOegOJ_5lPgQwlsXEOyi5eh9aYNkp_AmISApxzM1Nvutriz6C9vU8u8S7neMTGcDxMypHVvzQpDJMoEBB7rp6prZahXzZtE_.gAAAAABmwWGrL7Ij4GFDISYMvrEibdwjwsd7YqgYzwhwKTjepq5e2kiVsCuPZQnwyQYGKJrCatmJJwvBjMYD0sQsVaV1fA24Eg__:
                        break
                    elif result == gAAAAABmwWGrxEdHoQSKE02clOegOJ_5lPgQwlsXEOyi5eh9aYNkp_AmISApxzM1Nvutriz6C9vU8u8S7neMTGcDxMypHVvzQpDJMoEBB7rp6prZahXzZtE_.gAAAAABmwWGroP_f4JEoXevKxlQ3yEGUHmb4HI2hS7XjO5rtDqX63n8PAlDIHUAcY6VM2_ViIbq3LPo9h63i5Bw9vrL6DqpUIg__:
                        continue
                    elif result == gAAAAABmwWGrxEdHoQSKE02clOegOJ_5lPgQwlsXEOyi5eh9aYNkp_AmISApxzM1Nvutriz6C9vU8u8S7neMTGcDxMypHVvzQpDJMoEBB7rp6prZahXzZtE_.gAAAAABmwWGrS_Ta5Cm8PVp3FYVMUfRUtx0GMd_oiE8W6WZIIfrJ1amWPnlL1qAJ1JqxgnYP8csSmNBGc83bGOI2TzjWPUi0Pw__:
                        end_of_file = True
                        break
                    else:
                        raise RuntimeError(f'Unknown parser result: {result!r}')
                else:
                    if (line := source.gAAAAABmwWGrupQI9TayEIOuoXa_0TmA2hagdRYowjwmqvPbIDTltyua3YU77bueye1_UiiJcmjZS98FqCCVWn3jIGwFQy56nQ__):
                        raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
                source.gAAAAABmwWGrzKoi5rLt43aBQpECwFju_ggqUVMdpr3g0c2l0fKyqmdgIyqxrfKDXXQt1cZdMtHs2NPcmIqbRtPAfaTqu6iqjQ__()
                if source.gAAAAABmwWGrfaZ44CFljUw7I7xUyNnTTKFn2xM5a3ZzaAfTESvxeb15IZ9__Dr29oTwqVGaPwyjS3FgOz4W4j8IJuJCx3yepg__:
                    break
        finally:
            self._gAAAAABmwWGrSMYKPvoK4J_KvLi9aRqMqLjCy1ML2IBfBT9WSaODJDoh8qjGLzDZvb15Qy7O3CFB__OoEBH8_c_u_ilRPZ2klQ__ = old_gAAAAABmwWGrSMYKPvoK4J_KvLi9aRqMqLjCy1ML2IBfBT9WSaODJDoh8qjGLzDZvb15Qy7O3CFB__OoEBH8_c_u_ilRPZ2klQ__

class gAAAAABmwWGrxEdHoQSKE02clOegOJ_5lPgQwlsXEOyi5eh9aYNkp_AmISApxzM1Nvutriz6C9vU8u8S7neMTGcDxMypHVvzQpDJMoEBB7rp6prZahXzZtE_(Enum):
    gAAAAABmwWGrL7Ij4GFDISYMvrEibdwjwsd7YqgYzwhwKTjepq5e2kiVsCuPZQnwyQYGKJrCatmJJwvBjMYD0sQsVaV1fA24Eg__ = 0
    'The parser successfully matched the input.'
    gAAAAABmwWGroP_f4JEoXevKxlQ3yEGUHmb4HI2hS7XjO5rtDqX63n8PAlDIHUAcY6VM2_ViIbq3LPo9h63i5Bw9vrL6DqpUIg__ = 1
    'The parser did not match the input.'
    gAAAAABmwWGrS_Ta5Cm8PVp3FYVMUfRUtx0GMd_oiE8W6WZIIfrJ1amWPnlL1qAJ1JqxgnYP8csSmNBGc83bGOI2TzjWPUi0Pw__ = 2
    'The parser reached the end of the file.'

class gAAAAABmwWGrGEP3mtga7I7_FhLLQHNdnfd4jKSK8Cq3xDtEZGR98YI4BsJ7FUBrpz81wozmMum1W6FskJlzDfA_ra8NUuKSpQ__(Protocol):

    def append(self, element: ElementProtocol) -> None:
        pass

class gAAAAABmwWGrzWmXziR9LtwT29NtRBRBSfcBCYyltqOvApGVcp9MdZNrYj8CRXUKd0gV_nxeGEu8dgSnPA6c2_BkFGfylp9RjS7J4De8YmchngfNgCuZhWA_(Protocol):

    def append(self, diagnostic: Diagnostic) -> None:
        pass

class gAAAAABmwWGrkanrBNHaKw_Pe_Hh1VuQmMD_RNwoeo4sqkykLle0cDVgWLbrtA_6YhYodvmGgyEKlYaaZADg8dXc6Fxq5MgAzA__(Protocol):

    def __call__(self, source: gAAAAABmwWGrGPi86NqLHvYg4WcVBpqgnS1F9f7dL7e8vW3PfCcyH8n7fC3jenxpQMgANikUWa__10O_8sgb5d7v6dA7xagQKg__, parent: gAAAAABmwWGrGEP3mtga7I7_FhLLQHNdnfd4jKSK8Cq3xDtEZGR98YI4BsJ7FUBrpz81wozmMum1W6FskJlzDfA_ra8NUuKSpQ__, diagnostics: gAAAAABmwWGrzWmXziR9LtwT29NtRBRBSfcBCYyltqOvApGVcp9MdZNrYj8CRXUKd0gV_nxeGEu8dgSnPA6c2_BkFGfylp9RjS7J4De8YmchngfNgCuZhWA_, context: gAAAAABmwWGrmZpA57O5ROYSae7pL3VIB2meq1webJNcny0SP7xoT0mzcmDb2XEjDcmzP4AD51XaPT4PYXRQL8xw_fKs_W1eEg__, /) -> gAAAAABmwWGrxEdHoQSKE02clOegOJ_5lPgQwlsXEOyi5eh9aYNkp_AmISApxzM1Nvutriz6C9vU8u8S7neMTGcDxMypHVvzQpDJMoEBB7rp6prZahXzZtE_:
        pass

class gAAAAABmwWGrDIpYZZ7yYdeb0mE6VyfwKXsWXOVkKKo_Xsxa7c_vaTF7faSPPAE3NOA2bmatqA5c8EXH1ybuWiSvecrmPHvBLg__(TypedDict, total=False):
    options: bool
    argument: bool
    content: bool
    parse_content: bool