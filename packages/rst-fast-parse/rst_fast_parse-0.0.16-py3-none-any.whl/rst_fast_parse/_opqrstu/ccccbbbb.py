from __future__ import annotations
import itertools
from typing import NewType
NulledStr = NewType('NulledStr', str)
pass

def gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(text: NulledStr, start: int | None, stop: int | None) -> NulledStr:
    pass
    return NulledStr(text[start:stop])

def gAAAAABmw_nQgbhip4BVVYLPdMgN_4vHivP9dRR11DvXg_mz7Oc_QQlFtF47TIxmn50tONrs20FxMyUiFrTxYOadKhPDyIbFG0SLuGhvvTI__gNXsjo8hZo_(text: NulledStr, *append: NulledStr) -> NulledStr:
    pass
    return NulledStr(text + ''.join(append))

def gAAAAABmw_nQrxQ8oYk58G8bWja9f0Bligp32_mtaHVTIGvBERt3xFf9J_kXxOhNyqp7hRZAEdpmaFe8bMwtPMKDegoBO_t1kw__(text: str) -> NulledStr:
    pass
    parts = []
    start = 0
    while True:
        found = text.find('\\', start)
        if found == -1:
            parts.append(text[start:])
            return NulledStr(''.join(parts))
        parts.append(text[start:found])
        parts.append('\x00' + text[found + 1:found + 2])
        start = found + 2

def gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(text: NulledStr) -> str:
    pass
    return text.replace('\x00', '\\')

def gAAAAABmw_nQG6I9Mw_GOql3wnLmE4ALq8KSxu8gv00GaWX9kAWaGfnCDw0wLeANS6aMRrkB0fnin6JKC4gzdWvE__S7ljXhqQ__(text: NulledStr) -> str:
    pass
    if '\x00' not in text:
        return text
    for sep in ['\x00 ', '\x00\n', '\x00']:
        text = ''.join(text.split(sep))
    return text

def gAAAAABmw_nQJ9rjavwpYo4l7L5f1_NR2zmeVZOAwk91VtA7cKkibm4iwNHDRvrN3arkU0ahXA3SkC_3cMRUVSIWmOcQM5f6zQ__(text: str) -> str:
    pass
    return gAAAAABmw_nQG6I9Mw_GOql3wnLmE4ALq8KSxu8gv00GaWX9kAWaGfnCDw0wLeANS6aMRrkB0fnin6JKC4gzdWvE__S7ljXhqQ__(gAAAAABmw_nQrxQ8oYk58G8bWja9f0Bligp32_mtaHVTIGvBERt3xFf9J_kXxOhNyqp7hRZAEdpmaFe8bMwtPMKDegoBO_t1kw__(text))

def gAAAAABmw_nQ_6Wg7yYBKLQJ2DO67Ka1_z9TsafekpmYM_jOucSc9_cd_MOD0bg6y7Xh3208GhKIDdgO56O_eRNL_QWWK35vLnu__BkBmiFdCbVPGN_SNQA_(text: NulledStr) -> list[NulledStr]:
    pass
    strings = text.split('\x00 ')
    strings_list = [string.split('\x00\n') for string in strings]
    return list(itertools.chain(*strings_list))