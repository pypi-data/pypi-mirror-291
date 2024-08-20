from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, Protocol, Sequence
from rst_fast_parse._vwxyz import gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__
from rst_fast_parse.diagnostics import Diagnostic, DiagnosticList
from rst_fast_parse.nodes.block import BlockNodeProtocol, RootNode
if TYPE_CHECKING:
    from rst_fast_parse.parse import DirectiveSpec

class gAAAAABmw_nQ9PTMQEnJGf89Y27v_b38jrWb_Z2WlMU2GvEt6N1G2rMHoL1eFcqRR7s_8cJXFO_Bxw133o5NWnbc4sLnHpxN5g__:
    pass

    def __init__(self, block_parsers: Sequence[gAAAAABmw_nQvitX41E7oQB9sNcqomnR4otn7mI6P6NyPevRnB47C3gUjpZWKjTlWaJtYFHZH9BXS9crDv6ZBVGNR88jhYFtLQ__], directives: dict[str, DirectiveSpec], *, gAAAAABmw_nQvuzQru2G_JO_j__wSPt5m5ClJScp6feS6t_j0XyGV2vI0VX5U6_lkIniwqnH2h_R0avA8S86z9Qjx6iZluvoMw__: bool=True) -> None:
        self._gAAAAABmw_nQvuzQru2G_JO_j__wSPt5m5ClJScp6feS6t_j0XyGV2vI0VX5U6_lkIniwqnH2h_R0avA8S86z9Qjx6iZluvoMw__ = gAAAAABmw_nQvuzQru2G_JO_j__wSPt5m5ClJScp6feS6t_j0XyGV2vI0VX5U6_lkIniwqnH2h_R0avA8S86z9Qjx6iZluvoMw__
        self._block_parsers = block_parsers
        self._directives = directives

    @property
    def gAAAAABmw_nQvuzQru2G_JO_j__wSPt5m5ClJScp6feS6t_j0XyGV2vI0VX5U6_lkIniwqnH2h_R0avA8S86z9Qjx6iZluvoMw__(self) -> bool:
        pass
        return self._gAAAAABmw_nQvuzQru2G_JO_j__wSPt5m5ClJScp6feS6t_j0XyGV2vI0VX5U6_lkIniwqnH2h_R0avA8S86z9Qjx6iZluvoMw__

    @property
    def directives(self) -> dict[str, DirectiveSpec]:
        pass
        return self._directives

    def gAAAAABmw_nQ7TyM_qk4_Mi4tNHzNAO4cosKhTogxRzx0HVnR7ibdgFk42D7KQBF_snUu5Ub5JiY349x_ji07OiTRC9F810Rng__(self, source: gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__, diagnostics: DiagnosticList | None) -> tuple[RootNode, DiagnosticList]:
        pass
        end_of_file = False
        start = source.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__.line if source.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__ else 0
        end = source.gAAAAABmw_nQk_w6BCgqt9PXffXyNws97Ie1UqKrJF7VicqcYHCKPqsrN26d3IZZzg_NauTMvTm5fS824l9U7GHJYjqSjqN7OA__.line if source.gAAAAABmw_nQk_w6BCgqt9PXffXyNws97Ie1UqKrJF7VicqcYHCKPqsrN26d3IZZzg_NauTMvTm5fS824l9U7GHJYjqSjqN7OA__ else 0
        parent = RootNode((start, end))
        diagnostics = [] if diagnostics is None else diagnostics
        while not end_of_file:
            for parser in self._block_parsers:
                result = parser(source, parent, diagnostics, self)
                if result == gAAAAABmw_nQ5cQ0MQIgHdXyUrLPHQRNEHU9o7h9bwhpvj_sYFX8d7sHtovyDVEqhz2vtKzqN8nmkWp90vyWArimsFUtFOqTLt6ioaS4iWn1M2WA0g7CaQc_.gAAAAABmw_nQStHIOt48wAPZ9orIggsbHFlU4YyrY_E6fPjfXXVXEbR2_p8dVfTbfkXSoLYIFYZ6wWgKDUTCmOeS2GS_xyy32g__:
                    break
                elif result == gAAAAABmw_nQ5cQ0MQIgHdXyUrLPHQRNEHU9o7h9bwhpvj_sYFX8d7sHtovyDVEqhz2vtKzqN8nmkWp90vyWArimsFUtFOqTLt6ioaS4iWn1M2WA0g7CaQc_.gAAAAABmw_nQdtzaVQDkQM3B4oyglt6TafsLS5QdMPfWkTZrDmAScTRz_uJiZrljWR1WpkbIcQbaYUkBrqnx0aA1hNnXlKWQqw__:
                    continue
                elif result == gAAAAABmw_nQ5cQ0MQIgHdXyUrLPHQRNEHU9o7h9bwhpvj_sYFX8d7sHtovyDVEqhz2vtKzqN8nmkWp90vyWArimsFUtFOqTLt6ioaS4iWn1M2WA0g7CaQc_.gAAAAABmw_nQ8ebv6y__hPrxyjgcsimzYLzyGkACUwny3erxendm1XY7AgV5WZWt70nL1aJrC6uHzPmLkTrB4hTPrja_TC226w__:
                    end_of_file = True
                    break
                else:
                    raise RuntimeError(f'Unknown parser result: {result!r}')
            else:
                if (line := source.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__):
                    raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
            source.gAAAAABmw_nQEa0WW0bmOvJW4MTYqNiGnBu44Y_dUiUMa4WUucD_TsDDxIBc3PTVwnGCkEC1b6QG9KUNpqhUPX0dVJq2ABQu5A__()
            if source.gAAAAABmw_nQOpotTA74TW4gcDqYcpy_IBTBwFbiyrHdfnmTsaeo_tAe_G2MSjTPTCXJxgD1Omza4e6GQtcpGsHaaDACFcBwqw__:
                break
        return (parent, diagnostics)

    def gAAAAABmw_nQtwFyYw_8K_iV0q_rIC4a8VTY_y3VZFZg2DitLgHmsyxsAK7DZJFgmZxSRpTCI5Kl_yRx2jTF506zk_5xsewIiw__(self, source: gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__, parent: gAAAAABmw_nQFaiKkGqIJQPh2PNhKDt_Ie_0VGgcq5KwFdT8VserbrywvssgsAcDAaSj_0gYdO1KCFPQZEt27bv8qUVwd924cw__, diagnostics: gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_, /) -> None:
        pass
        old_gAAAAABmw_nQvuzQru2G_JO_j__wSPt5m5ClJScp6feS6t_j0XyGV2vI0VX5U6_lkIniwqnH2h_R0avA8S86z9Qjx6iZluvoMw__ = self._gAAAAABmw_nQvuzQru2G_JO_j__wSPt5m5ClJScp6feS6t_j0XyGV2vI0VX5U6_lkIniwqnH2h_R0avA8S86z9Qjx6iZluvoMw__
        try:
            self._gAAAAABmw_nQvuzQru2G_JO_j__wSPt5m5ClJScp6feS6t_j0XyGV2vI0VX5U6_lkIniwqnH2h_R0avA8S86z9Qjx6iZluvoMw__ = False
            end_of_file = False
            while not end_of_file:
                for parser in self._block_parsers:
                    result = parser(source, parent, diagnostics, self)
                    if result == gAAAAABmw_nQ5cQ0MQIgHdXyUrLPHQRNEHU9o7h9bwhpvj_sYFX8d7sHtovyDVEqhz2vtKzqN8nmkWp90vyWArimsFUtFOqTLt6ioaS4iWn1M2WA0g7CaQc_.gAAAAABmw_nQStHIOt48wAPZ9orIggsbHFlU4YyrY_E6fPjfXXVXEbR2_p8dVfTbfkXSoLYIFYZ6wWgKDUTCmOeS2GS_xyy32g__:
                        break
                    elif result == gAAAAABmw_nQ5cQ0MQIgHdXyUrLPHQRNEHU9o7h9bwhpvj_sYFX8d7sHtovyDVEqhz2vtKzqN8nmkWp90vyWArimsFUtFOqTLt6ioaS4iWn1M2WA0g7CaQc_.gAAAAABmw_nQdtzaVQDkQM3B4oyglt6TafsLS5QdMPfWkTZrDmAScTRz_uJiZrljWR1WpkbIcQbaYUkBrqnx0aA1hNnXlKWQqw__:
                        continue
                    elif result == gAAAAABmw_nQ5cQ0MQIgHdXyUrLPHQRNEHU9o7h9bwhpvj_sYFX8d7sHtovyDVEqhz2vtKzqN8nmkWp90vyWArimsFUtFOqTLt6ioaS4iWn1M2WA0g7CaQc_.gAAAAABmw_nQ8ebv6y__hPrxyjgcsimzYLzyGkACUwny3erxendm1XY7AgV5WZWt70nL1aJrC6uHzPmLkTrB4hTPrja_TC226w__:
                        end_of_file = True
                        break
                    else:
                        raise RuntimeError(f'Unknown parser result: {result!r}')
                else:
                    if (line := source.gAAAAABmw_nQyp6agXTgrjWOTHJY1ulqewoTi6AcVKWc_J9EAhSeNgbFFMNVM8EStcNEfOJEXiJXqlvpPSISOHGV30pDw723iQ__):
                        raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
                source.gAAAAABmw_nQEa0WW0bmOvJW4MTYqNiGnBu44Y_dUiUMa4WUucD_TsDDxIBc3PTVwnGCkEC1b6QG9KUNpqhUPX0dVJq2ABQu5A__()
                if source.gAAAAABmw_nQOpotTA74TW4gcDqYcpy_IBTBwFbiyrHdfnmTsaeo_tAe_G2MSjTPTCXJxgD1Omza4e6GQtcpGsHaaDACFcBwqw__:
                    break
        finally:
            self._gAAAAABmw_nQvuzQru2G_JO_j__wSPt5m5ClJScp6feS6t_j0XyGV2vI0VX5U6_lkIniwqnH2h_R0avA8S86z9Qjx6iZluvoMw__ = old_gAAAAABmw_nQvuzQru2G_JO_j__wSPt5m5ClJScp6feS6t_j0XyGV2vI0VX5U6_lkIniwqnH2h_R0avA8S86z9Qjx6iZluvoMw__

class gAAAAABmw_nQ5cQ0MQIgHdXyUrLPHQRNEHU9o7h9bwhpvj_sYFX8d7sHtovyDVEqhz2vtKzqN8nmkWp90vyWArimsFUtFOqTLt6ioaS4iWn1M2WA0g7CaQc_(Enum):
    pass
    gAAAAABmw_nQStHIOt48wAPZ9orIggsbHFlU4YyrY_E6fPjfXXVXEbR2_p8dVfTbfkXSoLYIFYZ6wWgKDUTCmOeS2GS_xyy32g__ = 0
    pass
    gAAAAABmw_nQdtzaVQDkQM3B4oyglt6TafsLS5QdMPfWkTZrDmAScTRz_uJiZrljWR1WpkbIcQbaYUkBrqnx0aA1hNnXlKWQqw__ = 1
    pass
    gAAAAABmw_nQ8ebv6y__hPrxyjgcsimzYLzyGkACUwny3erxendm1XY7AgV5WZWt70nL1aJrC6uHzPmLkTrB4hTPrja_TC226w__ = 2
    pass

class gAAAAABmw_nQFaiKkGqIJQPh2PNhKDt_Ie_0VGgcq5KwFdT8VserbrywvssgsAcDAaSj_0gYdO1KCFPQZEt27bv8qUVwd924cw__(Protocol):
    pass

    def append(self, node: BlockNodeProtocol, /) -> None:
        pass

class gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_(Protocol):
    pass

    def append(self, diagnostic: Diagnostic) -> None:
        pass

class gAAAAABmw_nQvitX41E7oQB9sNcqomnR4otn7mI6P6NyPevRnB47C3gUjpZWKjTlWaJtYFHZH9BXS9crDv6ZBVGNR88jhYFtLQ__(Protocol):
    pass

    def __call__(self, source: gAAAAABmw_nQnTlF7_w3Ecpli5hitLuDOMgI4HDBrwPV3O88Ve39z2LSk4Yy2PbqOoGPvGoUT8YghIokpzXqXf2C7sspjsbIGg__, parent: gAAAAABmw_nQFaiKkGqIJQPh2PNhKDt_Ie_0VGgcq5KwFdT8VserbrywvssgsAcDAaSj_0gYdO1KCFPQZEt27bv8qUVwd924cw__, diagnostics: gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_, context: gAAAAABmw_nQ9PTMQEnJGf89Y27v_b38jrWb_Z2WlMU2GvEt6N1G2rMHoL1eFcqRR7s_8cJXFO_Bxw133o5NWnbc4sLnHpxN5g__, /) -> gAAAAABmw_nQ5cQ0MQIgHdXyUrLPHQRNEHU9o7h9bwhpvj_sYFX8d7sHtovyDVEqhz2vtKzqN8nmkWp90vyWArimsFUtFOqTLt6ioaS4iWn1M2WA0g7CaQc_:
        pass