from __future__ import annotations
import itertools
from typing import NewType
EscapedStr = NewType('EscapedStr', str)
'A string with backslash escapes converted to nulls.'

def gAAAAABmwWGrou1ABXXkVMK_OwKraQHcX_Vwe_aJqhZDWgUg31iT3eOCtpdyqV9QfddKfOZSglxCCsjqRbWkliuSRTHiataY7r6dgWKmZvhnXiOTwLMyDl4_(text: EscapedStr, *append: EscapedStr) -> EscapedStr:
    return EscapedStr(text + ''.join(append))

def gAAAAABmwWGrqKlbb2FfVQRwb5CcYlkzsxZ2krQ8U1jhnWv71f4h72auCDNWcOhST4gQf_qukmjIYz9dWZt1XqwqsWXQ_9FeNA__(text: str) -> EscapedStr:
    parts = []
    start = 0
    while True:
        found = text.find('\\', start)
        if found == -1:
            parts.append(text[start:])
            return EscapedStr(''.join(parts))
        parts.append(text[start:found])
        parts.append('\x00' + text[found + 1:found + 2])
        start = found + 2

def gAAAAABmwWGrnUHt8zp_9cgZoMkSo_jIWVEff8kU_jrdhSwoSBeSHuMmUUN92ubjezsoaGEXBtdbsdKWApfqH62cNMOME3DeKaAc5IPoeVrpAO3iMFqWqLw_(text: EscapedStr) -> str:
    return text.replace('\x00', '\\')

def gAAAAABmwWGrH_L98iS362D107RDFWdtA2uNLg4znT3vP2C4JoNEF_8Tpo5K7nzRaboZss6fx1Kq2Mn_a7sdvYXjMwldpsYe5w__(text: EscapedStr) -> str:
    if '\x00' not in text:
        return text
    for sep in ['\x00 ', '\x00\n', '\x00']:
        text = ''.join(text.split(sep))
    return text

def gAAAAABmwWGrHc1IXn1ROx7rejGkY8WfAv3qRJJyxoDg0OVN_ir0yeFYhmjKBYRngPoG_zvixq86WBjE47RzUjvaQ3QLHJOoOlxy7ys897YzLG5KCgEneU4_(text: EscapedStr) -> list[EscapedStr]:
    strings = text.split('\x00 ')
    strings_list = [string.split('\x00\n') for string in strings]
    return list(itertools.chain(*strings_list))