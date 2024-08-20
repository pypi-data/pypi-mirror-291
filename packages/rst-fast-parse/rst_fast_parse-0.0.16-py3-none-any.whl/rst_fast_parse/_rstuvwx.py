from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import re
import sys
from typing import TYPE_CHECKING, Callable, Final, Mapping, Optional, Tuple, TypedDict
from rst_fast_parse._opqrstu.ccccbbbb import NulledStr, gAAAAABmw_nQrxQ8oYk58G8bWja9f0Bligp32_mtaHVTIGvBERt3xFf9J_kXxOhNyqp7hRZAEdpmaFe8bMwtPMKDegoBO_t1kw__, gAAAAABmw_nQG6I9Mw_GOql3wnLmE4ALq8KSxu8gv00GaWX9kAWaGfnCDw0wLeANS6aMRrkB0fnin6JKC4gzdWvE__S7ljXhqQ__, gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_, gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__, gAAAAABmw_nQ_6Wg7yYBKLQJ2DO67Ka1_z9TsafekpmYM_jOucSc9_cd_MOD0bg6y7Xh3208GhKIDdgO56O_eRNL_QWWK35vLnu__BkBmiFdCbVPGN_SNQA_
from rst_fast_parse._hijklmn.bbbbbbbb import gAAAAABmw_nQSDRQ8Fx44GK5ZjliDe2vEFe3Jh6bTC8Mz8q5CIacJh_sXQg0T1V7n8Tyjvx_kfv3sd_XE4qWvY3XmA208pzjxkxS_vdRIog5FfUECONxyiU_, gAAAAABmw_nQji4aWRoL6iJQq6g7HMKReQ_6RkvZl8cbXNEQfYsVIPKnkCPltsOlh90I_p4V5vhwQ2UmGTv7i_nOut122DZnlw__, gAAAAABmw_nQWLUJIUltzqqXjUENzNYPHfCWcDTQqigAmDuvz5Byaga0xz_TRUAggNR9G1PB_zNcMU8fkjLFzRx7KYB3iTOdiw__, gAAAAABmw_nQGB1DCp1RDgUIHdQGFpBPCN_2_GyqYXyNKwKWniZ76zXuXb5X3bLb99smc_fsftbUSYlog_JCYiC9LX2qr069KruL2Uq7wAqvdrHouAtJr_U_, gAAAAABmw_nQNYibkTOE1hh18lhrxv_xfaHVczWfLF6FV5DOH694G4m9PpPCOfFbRvsYDT2fQw_QcMq6oUQBWvWnjUfnGlVB6A__
from rst_fast_parse._hijklmn.bbbbaaaa import gAAAAABmw_nQuvc_tG9LEjxsuimSo_KF5CcBrCh8m7DhxjT87n45lhB6xivvEq18F45xBiQ5iFbskOBmzOMMnocb5mqUAWLP9Q__, gAAAAABmw_nQRFW4WCsw9Mid3hCiDS5xyL9769r4yoi1hch1G1wHlN16U3_DMOvuPMF5aZyE_0gd1CEBLD_JUo_Q3R9vir_Q1w__
from rst_fast_parse.diagnostics import Diagnostic, DiagnosticCode
from rst_fast_parse.nodes.block import InlineNode, LineProtocol
from rst_fast_parse.nodes.inline import BasicInlineNode, CitationReferenceNode, EmbeddedReferenceNode, EmbeddedUriNode, FootnoteReferenceNode, InlineNodeProtocol, InlineTargetNode, PhraseReferenceNode, ProblematicNode, RoleNode, SimpleReferenceNode, StandaloneUriNode, SubstitutionReferenceNode, TextNode
if TYPE_CHECKING:
    from typing import TypeAlias
    from rst_fast_parse._core import gAAAAABmw_nQ9PTMQEnJGf89Y27v_b38jrWb_Z2WlMU2GvEt6N1G2rMHoL1eFcqRR7s_8cJXFO_Bxw133o5NWnbc4sLnHpxN5g__, gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_
_dataclass_kwargs = {}
if sys.version_info >= (3, 10):
    _dataclass_kwargs['slots'] = True
gAAAAABmw_nQk6jskitR23cYNZUuHIApdaRs70vGcPIKmSAPrQQLaIiomsnnX6s5jlAOhQ6747O98lodQZ7wTBqL8vysiCdyAA__: Final[str] = '"\'(<\\[{༺༼᚛⁅⁽₍〈❨❪❬❮❰❲❴⟅⟦⟨⟪⟬⟮⦃⦅⦇⦉⦋⦍⦏⦑⦓⦕⦗⧘⧚⧼⸢⸤⸦⸨〈《「『【〔〖〘〚〝〝﴾︗︵︷︹︻︽︿﹁﹃﹇﹙﹛﹝（［｛｟｢«‘“‹⸂⸄⸉⸌⸜⸠‚„»’”›⸃⸅⸊⸍⸝⸡‛‟'
gAAAAABmw_nQywQ894zMZQaBCm8_u77o2a57wLVqYkUu_BKsimg0AB8v_2T9sgVvpj_SPX7qHfJA3SwqwnIAHDBkJLQHmNYNAg__: Final[str] = '"\')>\\]}༻༽᚜⁆⁾₎〉❩❫❭❯❱❳❵⟆⟧⟩⟫⟭⟯⦄⦆⦈⦊⦌⦎⦐⦒⦔⦖⦘⧙⧛⧽⸣⸥⸧⸩〉》」』】〕〗〙〛〞〟﴿︘︶︸︺︼︾﹀﹂﹄﹈﹚﹜﹞）］｝｠｣»’”›⸃⸅⸊⸍⸝⸡‛‟«‘“‹⸂⸄⸉⸌⸜⸠‚„'
gAAAAABmw_nQhIpnVSdrrHedgy4g6Ov5VFia4bRvkVBO2W4qHTh0Ps4_mlYgIO0GS_Huq6Gv4Fgojctz_2wCYLGjGph_i_utgg__: Final[str] = '\\-/:֊¡·¿;·՚-՟։־׀׃׆׳״؉؊،؍؛؞؟٪-٭۔܀-܍߷-߹࠰-࠾।॥॰෴๏๚๛༄-༒྅࿐-࿔၊-၏჻፡-፨᐀᙭᙮᛫-᛭᜵᜶។-៖៘-៚᠀-᠊᥄᥅᧞᧟᨞᨟᪠-᪦᪨-᪭᭚-᭠᰻-᰿᱾᱿᳓‐-‗†-‧‰-‸※-‾⁁-⁃⁇-⁑⁓⁕-⁞⳹-⳼⳾⳿⸀⸁⸆-⸈⸋⸎-⸛⸞⸟⸪-⸮⸰⸱、-〃〜〰〽゠・꓾꓿꘍-꘏꙳꙾꛲-꛷꡴-꡷꣎꣏꣸-꣺꤮꤯꥟꧁-꧍꧞꧟꩜-꩟꫞꫟꯫︐-︖︙︰-︲﹅﹆﹉-﹌﹐-﹒﹔-﹘﹟-﹡﹣﹨﹪﹫！-＃％-＇＊，-／：；？＠＼｡､･𐄀𐄁𐎟𐏐𐡗𐤟𐤿𐩐-𐩘𐩿𐬹-𐬿𑂻𑂼𑂾-𑃁𒑰-𒑳'
gAAAAABmw_nQDGTMbzA_aWw0xyJLKz2k_3cJZrUxw7tktMJD4aq_pIwE9DdDB1IIT55w_fFVO9V6FvwtenX0w58n5M8eRl_LcKx2vxcYE_kIPkDO0MqWOJs_: Final[str] = '\\\\.,;!?'
gAAAAABmw_nQEeA4Tsrb5wXWunqdAjh61rGstoE0HPoiDFqyTHnA92lA2Bqlr2uYX8c4Qo6PUGf_IlVkV4mfmquLfUkKxIUl3A__: Final[Mapping[str, str]] = {'»': '»', '‘': '‚', '’': '’', '‚': '‘’', '“': '„', '„': '“”', '”': '”', '›': '›'}
gAAAAABmw_nQ5gkVCdHK775bDswri_L1vIduGnSIeg2IvPaypLZbz7v8zA0LZq8tCi6FLIOXS2prYxkGGHY0gu1TDLSelRYnpDXDaX1ipPCNQT3CD6h_IDs_: Final[str] = f'(^|(?<=\\s|[{gAAAAABmw_nQk6jskitR23cYNZUuHIApdaRs70vGcPIKmSAPrQQLaIiomsnnX6s5jlAOhQ6747O98lodQZ7wTBqL8vysiCdyAA__}{gAAAAABmw_nQhIpnVSdrrHedgy4g6Ov5VFia4bRvkVBO2W4qHTh0Ps4_mlYgIO0GS_Huq6Gv4Fgojctz_2wCYLGjGph_i_utgg__}]))'
gAAAAABmw_nQ3bM8qMzeZ6dFPmh5YLkeEK3DtHHh3_nju4EgyIsyaXOL_4m_WZY3hInQS8nG1SBSqALswTs4j_5NDBxuHZ7i_Q__: Final[str] = f'($|(?=\\s|[\x00{gAAAAABmw_nQDGTMbzA_aWw0xyJLKz2k_3cJZrUxw7tktMJD4aq_pIwE9DdDB1IIT55w_fFVO9V6FvwtenX0w58n5M8eRl_LcKx2vxcYE_kIPkDO0MqWOJs_}{gAAAAABmw_nQhIpnVSdrrHedgy4g6Ov5VFia4bRvkVBO2W4qHTh0Ps4_mlYgIO0GS_Huq6Gv4Fgojctz_2wCYLGjGph_i_utgg__}{gAAAAABmw_nQywQ894zMZQaBCm8_u77o2a57wLVqYkUu_BKsimg0AB8v_2T9sgVvpj_SPX7qHfJA3SwqwnIAHDBkJLQHmNYNAg__}]))'
gAAAAABmw_nQQfKwNJXeQCqsKIZquXHUZKQ6VVtxG6un5TR3Wg8_Sfx2fm0rmMgzvnr0Ln5vwk7AVpUucr3uFw8E36r3TXCkuJCu3q5sAIJgtbfUJavJBtc_: Final[str] = f'((?:[ \\n]+|^)<{gAAAAABmw_nQji4aWRoL6iJQq6g7HMKReQ_6RkvZl8cbXNEQfYsVIPKnkCPltsOlh90I_p4V5vhwQ2UmGTv7i_nOut122DZnlw__}(([^<>]|\\x00[<>])+){gAAAAABmw_nQGB1DCp1RDgUIHdQGFpBPCN_2_GyqYXyNKwKWniZ76zXuXb5X3bLb99smc_fsftbUSYlog_JCYiC9LX2qr069KruL2Uq7wAqvdrHouAtJr_U_}>)$'
pass

@dataclass(**_dataclass_kwargs)
class gAAAAABmw_nQ_1LLl_2FSskoihYO0yx90m6a9e4zq6InTL8YQdLAqOpy0pKQ7X2IwkEx7PuRy_Yso3OsswnkOa8OAh_WoyXLEw__:
    pass
    initial: str
    uri: str
    phrase_end: str
    strong: str
    emphasis: str
    literal: str
    internal_target: str
    substitution_ref: str

@lru_cache
def gAAAAABmw_nQ203zuwgiLpLd6fybibeSxkJR_0O14K8otDj1wstci3Z_kDncpJeC7j9pdIyLDVpQgKVxdgW_l9cExtk8qbznUSSxAW6bXMbdR2k6SwjHtRA_() -> gAAAAABmw_nQ_1LLl_2FSskoihYO0yx90m6a9e4zq6InTL8YQdLAqOpy0pKQ7X2IwkEx7PuRy_Yso3OsswnkOa8OAh_WoyXLEw__:
    return gAAAAABmw_nQ_1LLl_2FSskoihYO0yx90m6a9e4zq6InTL8YQdLAqOpy0pKQ7X2IwkEx7PuRy_Yso3OsswnkOa8OAh_WoyXLEw__(initial=gAAAAABmw_nQMv4oXeONNn0iPvaDF_Hr0cJONmwL9q9_nXlXfvYEtpGVFHYWkHpz7JAHZAF9tBAhlAuJ5sHjClldSptELWd5GAFB131pcFiH2YISjjDQYyw_(gAAAAABmw_nQ5gkVCdHK775bDswri_L1vIduGnSIeg2IvPaypLZbz7v8zA0LZq8tCi6FLIOXS2prYxkGGHY0gu1TDLSelRYnpDXDaX1ipPCNQT3CD6h_IDs_, gAAAAABmw_nQ3bM8qMzeZ6dFPmh5YLkeEK3DtHHh3_nju4EgyIsyaXOL_4m_WZY3hInQS8nG1SBSqALswTs4j_5NDBxuHZ7i_Q__), uri=f'{gAAAAABmw_nQ5gkVCdHK775bDswri_L1vIduGnSIeg2IvPaypLZbz7v8zA0LZq8tCi6FLIOXS2prYxkGGHY0gu1TDLSelRYnpDXDaX1ipPCNQT3CD6h_IDs_}{gAAAAABmw_nQRFW4WCsw9Mid3hCiDS5xyL9769r4yoi1hch1G1wHlN16U3_DMOvuPMF5aZyE_0gd1CEBLD_JUo_Q3R9vir_Q1w__}{gAAAAABmw_nQ3bM8qMzeZ6dFPmh5YLkeEK3DtHHh3_nju4EgyIsyaXOL_4m_WZY3hInQS8nG1SBSqALswTs4j_5NDBxuHZ7i_Q__}', phrase_end=f'{gAAAAABmw_nQSDRQ8Fx44GK5ZjliDe2vEFe3Jh6bTC8Mz8q5CIacJh_sXQg0T1V7n8Tyjvx_kfv3sd_XE4qWvY3XmA208pzjxkxS_vdRIog5FfUECONxyiU_}(`(?P<suffix>(?P<role>:{gAAAAABmw_nQNYibkTOE1hh18lhrxv_xfaHVczWfLF6FV5DOH694G4m9PpPCOfFbRvsYDT2fQw_QcMq6oUQBWvWnjUfnGlVB6A__}:)?(?P<refend>__?)?)){gAAAAABmw_nQ3bM8qMzeZ6dFPmh5YLkeEK3DtHHh3_nju4EgyIsyaXOL_4m_WZY3hInQS8nG1SBSqALswTs4j_5NDBxuHZ7i_Q__}', strong=f'{gAAAAABmw_nQGB1DCp1RDgUIHdQGFpBPCN_2_GyqYXyNKwKWniZ76zXuXb5X3bLb99smc_fsftbUSYlog_JCYiC9LX2qr069KruL2Uq7wAqvdrHouAtJr_U_}(\\*\\*){gAAAAABmw_nQ3bM8qMzeZ6dFPmh5YLkeEK3DtHHh3_nju4EgyIsyaXOL_4m_WZY3hInQS8nG1SBSqALswTs4j_5NDBxuHZ7i_Q__}', emphasis=f'{gAAAAABmw_nQGB1DCp1RDgUIHdQGFpBPCN_2_GyqYXyNKwKWniZ76zXuXb5X3bLb99smc_fsftbUSYlog_JCYiC9LX2qr069KruL2Uq7wAqvdrHouAtJr_U_}(\\*){gAAAAABmw_nQ3bM8qMzeZ6dFPmh5YLkeEK3DtHHh3_nju4EgyIsyaXOL_4m_WZY3hInQS8nG1SBSqALswTs4j_5NDBxuHZ7i_Q__}', literal=f'{gAAAAABmw_nQWLUJIUltzqqXjUENzNYPHfCWcDTQqigAmDuvz5Byaga0xz_TRUAggNR9G1PB_zNcMU8fkjLFzRx7KYB3iTOdiw__}(``){gAAAAABmw_nQ3bM8qMzeZ6dFPmh5YLkeEK3DtHHh3_nju4EgyIsyaXOL_4m_WZY3hInQS8nG1SBSqALswTs4j_5NDBxuHZ7i_Q__}', internal_target=f'{gAAAAABmw_nQGB1DCp1RDgUIHdQGFpBPCN_2_GyqYXyNKwKWniZ76zXuXb5X3bLb99smc_fsftbUSYlog_JCYiC9LX2qr069KruL2Uq7wAqvdrHouAtJr_U_}(`){gAAAAABmw_nQ3bM8qMzeZ6dFPmh5YLkeEK3DtHHh3_nju4EgyIsyaXOL_4m_WZY3hInQS8nG1SBSqALswTs4j_5NDBxuHZ7i_Q__}', substitution_ref=f'{gAAAAABmw_nQGB1DCp1RDgUIHdQGFpBPCN_2_GyqYXyNKwKWniZ76zXuXb5X3bLb99smc_fsftbUSYlog_JCYiC9LX2qr069KruL2Uq7wAqvdrHouAtJr_U_}(\\|_{{0,2}}){gAAAAABmw_nQ3bM8qMzeZ6dFPmh5YLkeEK3DtHHh3_nju4EgyIsyaXOL_4m_WZY3hInQS8nG1SBSqALswTs4j_5NDBxuHZ7i_Q__}')

def gAAAAABmw_nQMv4oXeONNn0iPvaDF_Hr0cJONmwL9q9_nXlXfvYEtpGVFHYWkHpz7JAHZAF9tBAhlAuJ5sHjClldSptELWd5GAFB131pcFiH2YISjjDQYyw_(start_prefix: str, end_suffix: str) -> str:
    pass
    start = f'(?P<start>\\*\\*|\\*(?!\\*)|``|_`|\\|(?!\\|)){gAAAAABmw_nQji4aWRoL6iJQq6g7HMKReQ_6RkvZl8cbXNEQfYsVIPKnkCPltsOlh90I_p4V5vhwQ2UmGTv7i_nOut122DZnlw__}'
    whole = f'(?P<whole>(?P<refname>{gAAAAABmw_nQNYibkTOE1hh18lhrxv_xfaHVczWfLF6FV5DOH694G4m9PpPCOfFbRvsYDT2fQw_QcMq6oUQBWvWnjUfnGlVB6A__})(?P<refend>__?)|\\[(?P<footnotelabel>[0-9]+|\\#({gAAAAABmw_nQNYibkTOE1hh18lhrxv_xfaHVczWfLF6FV5DOH694G4m9PpPCOfFbRvsYDT2fQw_QcMq6oUQBWvWnjUfnGlVB6A__})?|\\*|(?P<citationlabel>{gAAAAABmw_nQNYibkTOE1hh18lhrxv_xfaHVczWfLF6FV5DOH694G4m9PpPCOfFbRvsYDT2fQw_QcMq6oUQBWvWnjUfnGlVB6A__}))(?P<fnend>\\]_)){end_suffix}'
    role = f'(?P<role>(:{gAAAAABmw_nQNYibkTOE1hh18lhrxv_xfaHVczWfLF6FV5DOH694G4m9PpPCOfFbRvsYDT2fQw_QcMq6oUQBWvWnjUfnGlVB6A__}:)?)(?P<backquote>`(?!`)){gAAAAABmw_nQji4aWRoL6iJQq6g7HMKReQ_6RkvZl8cbXNEQfYsVIPKnkCPltsOlh90I_p4V5vhwQ2UmGTv7i_nOut122DZnlw__}'
    return f'{start_prefix}(?P<initial_inline>{start}|{whole}|{role})'
gAAAAABmw_nQnEox51bRTV53Cc4Ifcw7myePsTXbWCKZqeswBXRI7hOUKALaVAuv59TL18YfO_1zPkZJi6A_re72GfBpgBbWzOQweHZpGqgn7kI6KPX25mg_: Final[tuple[str, ...]] = ('about', 'acap', 'addbook', 'afp', 'afs', 'aim', 'callto', 'castanet', 'chttp', 'cid', 'crid', 'data', 'dav', 'dict', 'dns', 'eid', 'fax', 'feed', 'file', 'finger', 'freenet', 'ftp', 'go', 'gopher', 'gsm-sms', 'h323', 'h324', 'hdl', 'hnews', 'http', 'https', 'hydra', 'iioploc', 'ilu', 'im', 'imap', 'info', 'ior', 'ipp', 'irc', 'iris.beep', 'iseek', 'jar', 'javascript', 'jdbc', 'ldap', 'lifn', 'livescript', 'lrq', 'mailbox', 'mailserver', 'mailto', 'md5', 'mid', 'mocha', 'modem', 'mtqp', 'mupdate', 'news', 'nfs', 'nntp', 'opaquelocktoken', 'phone', 'pop', 'pop3', 'pres', 'printer', 'prospero', 'rdar', 'res', 'rtsp', 'rvp', 'rwhois', 'rx', 'sdp', 'service', 'shttp', 'sip', 'sips', 'smb', 'snews', 'snmp', 'soap.beep', 'soap.beeps', 'ssh', 't120', 'tag', 'tcp', 'tel', 'telephone', 'telnet', 'tftp', 'tip', 'tn3270', 'tv', 'urn', 'uuid', 'vemmi', 'videotex', 'view-source', 'wais', 'whodp', 'whois++', 'x-man-page', 'xmlrpc.beep', 'xmlrpc.beeps', 'z39.50r', 'z39.50s')

def gAAAAABmw_nQRyc0oiZAxdq1Z9mqU9j8kvdrpJiGE9vOUle6OSyrHGJS3P1zvqB2t3zdXH5dVMoWIGh7l8_cGpOYsE_ad_NnyA__(c1: str, c2: str) -> bool:
    pass
    try:
        i = gAAAAABmw_nQk6jskitR23cYNZUuHIApdaRs70vGcPIKmSAPrQQLaIiomsnnX6s5jlAOhQ6747O98lodQZ7wTBqL8vysiCdyAA__.index(c1)
    except ValueError:
        return False
    return c2 == gAAAAABmw_nQywQ894zMZQaBCm8_u77o2a57wLVqYkUu_BKsimg0AB8v_2T9sgVvpj_SPX7qHfJA3SwqwnIAHDBkJLQHmNYNAg__[i] or c2 in gAAAAABmw_nQEeA4Tsrb5wXWunqdAjh61rGstoE0HPoiDFqyTHnA92lA2Bqlr2uYX8c4Qo6PUGf_IlVkV4mfmquLfUkKxIUl3A__.get(c1, '')

def gAAAAABmw_nQo9xiNueZPgOtfdxO7fiXz64FmmZ_y_5wiie13vi0b1g0kvVmw9oC_GxaEogCohbAIGWWPM0sP7FzhJEfVY6NUg__(string: NulledStr, start: int, end: int) -> bool:
    pass
    if start == 0:
        return False
    prestart = string[start - 1]
    try:
        poststart = string[end]
    except IndexError:
        return True
    return gAAAAABmw_nQRyc0oiZAxdq1Z9mqU9j8kvdrpJiGE9vOUle6OSyrHGJS3P1zvqB2t3zdXH5dVMoWIGh7l8_cGpOYsE_ad_NnyA__(prestart, poststart)

@dataclass(**_dataclass_kwargs)
class gAAAAABmw_nQDRFHljnIXYFdvGR_QhlA7mcXGZKgkrVukNnARLUCMkUJRW0yQY_lAq7ccgjaqqf_ciM1gqKqL3dL19NA3q_K1XOXUX8APv1q9imbVc9d8Rk_:
    pass
    raw_range: tuple[int, int]
    pass
    content: NulledStr
    pass
    content_range: None | tuple[int, int]
    pass
    end_marker: str
    pass

def gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match: re.Match[str], group: str | int) -> str | None:
    pass
    return match.group(group)

class gAAAAABmw_nQJ6g1a3B3QFuuW9YIjeCeb8Gy48n9d1_Q0J46c86Rx00sN04kFdkkMCItgE1kOv7effB_CaMbwgv_Endg9xWicw__(TypedDict):
    line_start: int
    line_end: int
    character_start: int
    character_end: int

@dataclass(**_dataclass_kwargs)
class gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__:
    pass
    _source_maps: bool
    _offset_to_location: Callable[[int], tuple[LineProtocol, int]]
    pass

    def gAAAAABmw_nQEKW8Z5QVDcz8zAdnVq7_7R6AhOK6wN85691Jhv2Jn3No_RZxF7oXvEanh7Qq5kAWFIU_d0t4A_s1ifiJtjqRaN9rCk3CueZA9kSMe6fASJE_(self, start: int, end: int) -> gAAAAABmw_nQJ6g1a3B3QFuuW9YIjeCeb8Gy48n9d1_Q0J46c86Rx00sN04kFdkkMCItgE1kOv7effB_CaMbwgv_Endg9xWicw__:
        pass
        start_line, start_indent = self._offset_to_location(start)
        end_line, end_indent = self._offset_to_location(end)
        return {'line_start': start_line.line, 'line_end': end_line.line, 'character_start': start_line.gAAAAABmw_nQK2_rPB2FLNZmeYW1eronEd0MIIkzWnQ_h9olZJMEqQdRLCBYjwkzW2QvDqHYsuEWM268E_H1U4gvXE3xoJdIyw__(start_indent).character_start, 'character_end': end_line.gAAAAABmw_nQK2_rPB2FLNZmeYW1eronEd0MIIkzWnQ_h9olZJMEqQdRLCBYjwkzW2QvDqHYsuEWM268E_H1U4gvXE3xoJdIyw__(end_indent).character_start}

    def gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(self, start: int, end: int) -> gAAAAABmw_nQJ6g1a3B3QFuuW9YIjeCeb8Gy48n9d1_Q0J46c86Rx00sN04kFdkkMCItgE1kOv7effB_CaMbwgv_Endg9xWicw__ | None:
        pass
        if not self._source_maps:
            return None
        return self.gAAAAABmw_nQEKW8Z5QVDcz8zAdnVq7_7R6AhOK6wN85691Jhv2Jn3No_RZxF7oXvEanh7Qq5kAWFIU_d0t4A_s1ifiJtjqRaN9rCk3CueZA9kSMe6fASJE_(start, end)
gAAAAABmw_nQs1IDsPQIJs_zHLKOQkcS9nKbLDMJ62FgYfKod0iUrXVxHLcewO0AJF6oCNpjWXE0_SRfYY8Ju_z5QAwd80I7sQ__: TypeAlias = Tuple[Optional[InlineNodeProtocol], int, int]
pass

def gAAAAABmw_nQx8uEtbryErvFvHH8mnlJbXB6gSdYpmOYZT1535j_lJQQoOElvyvcEi9wSSs_KoOW628y_IHwOvqEDeDzcJTJhw__(text: NulledStr, offset: int, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__, regexes: gAAAAABmw_nQ_1LLl_2FSskoihYO0yx90m6a9e4zq6InTL8YQdLAqOpy0pKQ7X2IwkEx7PuRy_Yso3OsswnkOa8OAh_WoyXLEw__, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__: gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_) -> None | gAAAAABmw_nQs1IDsPQIJs_zHLKOQkcS9nKbLDMJ62FgYfKod0iUrXVxHLcewO0AJF6oCNpjWXE0_SRfYY8Ju_z5QAwd80I7sQ__:
    pass
    if not re.search('[*_`|]', text):
        return None
    if (match_pat := re.search(regexes.initial, text)) is None:
        return None
    if (match_group := 'start') and (match_text := gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match_pat, match_group)) or ((match_group := 'backquote') and (match_text := gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match_pat, match_group))) or ((match_group := 'refend') and (match_text := gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match_pat, match_group))) or ((match_group := 'fnend') and (match_text := gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match_pat, match_group))):
        if match_text == '*':
            return gAAAAABmw_nQV_Oble0DYOWIo5NqAw_SINkH7uNcHVpm5QB_nL4J9E6flkGfHhLORkchVOoXAjiB2iT4Zr_FZG9chq7ZU1CgMxGzF3d0qKW_gOJS3G8GPao_('emphasis', text, offset, match_pat.start(match_group), match_pat.end(match_group), regexes.emphasis, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__, gAAAAABmw_nQJLGWaOIIgPRIHPVEKTJZHkS3Qg_e5TmNWft7ALnq8A_e7fhyI3QHlE1gTl_ZyEbJWRBX94vInlRYHJeYNrfH2ATCMp77KU3gTDV3_QEpS9k_, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__=gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__)
        if match_text == '**':
            return gAAAAABmw_nQV_Oble0DYOWIo5NqAw_SINkH7uNcHVpm5QB_nL4J9E6flkGfHhLORkchVOoXAjiB2iT4Zr_FZG9chq7ZU1CgMxGzF3d0qKW_gOJS3G8GPao_('strong', text, offset, match_pat.start(match_group), match_pat.end(match_group), regexes.strong, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__, gAAAAABmw_nQXcJCQXeX95GbM8wC7pblJelvZUmInLPUdMFhfb9VPc2tDv3QxTs7DFbm2MLyM9NYqWMH5YkZkk7JwgO_VaJDDA__, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__=gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__)
        if match_text == ']_':
            label: None | NulledStr
            _node: CitationReferenceNode | FootnoteReferenceNode
            if (label := gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match_pat, 'citationlabel')):
                _node = gAAAAABmw_nQ8eH82uhvbQkEIOU4IO88ZKVbjM_Fwxk_FD0fa_OaM6xIpcHM1mMP4cgBJ1qr_fUuxflOmNQ_8eCo08G8_DyeCZ8LQFmwCJ3vaOlP4sJKA5g_(label, offset + match_pat.start('whole'), offset + match_pat.end('whole'), gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__)
            elif (label := gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match_pat, 'footnotelabel')):
                _node = gAAAAABmw_nQcnbEA_PLvaikdVW4_XshX1EuJjwFp9DctW8UZy_5RDih1DQC3yCRVJWjgRoqujZlTii7ZeNuBWxF5sYugSqbxX8RBcLxJkgOdo68fOGJlaI_(label, offset + match_pat.start('whole'), offset + match_pat.end('whole'), gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__)
            else:
                raise RuntimeError('footnote or citation reference without label')
            return (_node, match_pat.start('whole'), match_pat.end('whole'))
        if match_text == '`':
            return gAAAAABmw_nQF17gpDqVpga_PSncLDVvzhRJw7ums4UU4fVoWBKlDR34vuZSgSaX__9wqcih9xODoKj4CoOXkPimYv9HQ4i71ZsTVfi7tq2_4h2j84ngQSdiOoFF3TA_k0sMp3m9n9iy(string=text, prefix_name_range=(match_pat.start('role') + 1, match_pat.end('role') - 1) if gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match_pat, 'role') else None, backquote_range=(match_pat.start('backquote'), match_pat.end('backquote')), regexes=regexes, offset=offset, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__=gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__)
        if match_text == '``':
            return gAAAAABmw_nQV_Oble0DYOWIo5NqAw_SINkH7uNcHVpm5QB_nL4J9E6flkGfHhLORkchVOoXAjiB2iT4Zr_FZG9chq7ZU1CgMxGzF3d0qKW_gOJS3G8GPao_('literal', text, offset, match_pat.start(match_group), match_pat.end(match_group), regexes.literal, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__, gAAAAABmw_nQrU1basa6IIWgYQ91f5FlerTnqwzQVyvWELmvIM9tM5yT2_2cK7GxXWWTZE3RR8R7RZggKd3__xqZA8RT2V0RwM0hohLHQ9z0xwAoaWJ_GL0_, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__=gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__)
        if match_text == '_`':
            return gAAAAABmw_nQV_Oble0DYOWIo5NqAw_SINkH7uNcHVpm5QB_nL4J9E6flkGfHhLORkchVOoXAjiB2iT4Zr_FZG9chq7ZU1CgMxGzF3d0qKW_gOJS3G8GPao_('target', text, offset, match_pat.start(match_group), match_pat.end(match_group), regexes.internal_target, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__, gAAAAABmw_nQ0_5d7JuVbcuGJY3PDMupnjM_Civh_T05nVxmMMFkpcBGcJJF0_ZUtGPGFncDjHkZ1DOueP52iULoy9PFOuoWBaARV9517B1yKSHMjkyzC_c_, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__=gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__)
        if match_text == '|':
            return gAAAAABmw_nQV_Oble0DYOWIo5NqAw_SINkH7uNcHVpm5QB_nL4J9E6flkGfHhLORkchVOoXAjiB2iT4Zr_FZG9chq7ZU1CgMxGzF3d0qKW_gOJS3G8GPao_('substitution_reference', text, offset, match_pat.start(match_group), match_pat.end(match_group), regexes.substitution_ref, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__, gAAAAABmw_nQBYntMjEAVDazjgGykrpWrRbWBjHiVYzZw8ZGeqwpIfQhPXpFrU_CfOuAypNcqZUsK3Gq6bZpoGUlu09Pf3nBGAD9H4VlcvrqM_Prr4dedXo_, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__=gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__)
        if match_text == '_':
            _ref_node = gAAAAABmw_nQE5WwmbNa4wijEJ8KydPJZtXMTkoB49A8gD_xnD_0DKw3ea79SaIlW2OG_IvXLi6SYCbtRDibT_LqUulXJctqnSGAfLoL_NWkA5egxcP_wRQ_(gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match_pat, 'refname'), False, offset + match_pat.start('whole'), offset + match_pat.end('whole'), gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__)
            return (_ref_node, match_pat.start('whole'), match_pat.end('whole'))
        if match_text == '__':
            _ref_node = gAAAAABmw_nQE5WwmbNa4wijEJ8KydPJZtXMTkoB49A8gD_xnD_0DKw3ea79SaIlW2OG_IvXLi6SYCbtRDibT_LqUulXJctqnSGAfLoL_NWkA5egxcP_wRQ_(gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match_pat, 'refname'), True, offset + match_pat.start('whole'), offset + match_pat.end('whole'), gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__)
            return (_ref_node, match_pat.start('whole'), match_pat.end('whole'))
        raise RuntimeError('unknown inline markup construct')
    return None

def gAAAAABmw_nQV_Oble0DYOWIo5NqAw_SINkH7uNcHVpm5QB_nL4J9E6flkGfHhLORkchVOoXAjiB2iT4Zr_FZG9chq7ZU1CgMxGzF3d0qKW_gOJS3G8GPao_(type_name: str, text: NulledStr, offset: int, open_marker_start: int, open_marker_end: int, closing_regex: str, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__, generate_node: Callable[[gAAAAABmw_nQDRFHljnIXYFdvGR_QhlA7mcXGZKgkrVukNnARLUCMkUJRW0yQY_lAq7ccgjaqqf_ciM1gqKqL3dL19NA3q_K1XOXUX8APv1q9imbVc9d8Rk_, gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__], InlineNodeProtocol], gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__: gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_) -> None | gAAAAABmw_nQs1IDsPQIJs_zHLKOQkcS9nKbLDMJ62FgYfKod0iUrXVxHLcewO0AJF6oCNpjWXE0_SRfYY8Ju_z5QAwd80I7sQ__:
    pass
    if gAAAAABmw_nQo9xiNueZPgOtfdxO7fiXz64FmmZ_y_5wiie13vi0b1g0kvVmw9oC_GxaEogCohbAIGWWPM0sP7FzhJEfVY6NUg__(text, open_marker_start, open_marker_end):
        return (None, open_marker_end, open_marker_end)
    if (end_match := re.search(closing_regex, text[open_marker_end:])) and end_match.start(1):
        content_end = open_marker_end + end_match.start(1)
        result = gAAAAABmw_nQDRFHljnIXYFdvGR_QhlA7mcXGZKgkrVukNnARLUCMkUJRW0yQY_lAq7ccgjaqqf_ciM1gqKqL3dL19NA3q_K1XOXUX8APv1q9imbVc9d8Rk_(raw_range=(offset + open_marker_start, offset + open_marker_end + end_match.end(1)), content=gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(text, open_marker_end, content_end), content_range=(offset + open_marker_end, offset + content_end), end_marker=end_match.group(1))
        _node = generate_node(result, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__)
        return (_node, open_marker_start, open_marker_end + end_match.end(1))
    problem_node = ProblematicNode(text[open_marker_start:open_marker_end], source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(offset + open_marker_start, offset + open_marker_end))
    gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__.append(Diagnostic(DiagnosticCode.inline_no_closing_marker, f'Inline {type_name} no closing marker.', **gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQEKW8Z5QVDcz8zAdnVq7_7R6AhOK6wN85691Jhv2Jn3No_RZxF7oXvEanh7Qq5kAWFIU_d0t4A_s1ifiJtjqRaN9rCk3CueZA9kSMe6fASJE_(offset + open_marker_start, offset + open_marker_end)))
    return (problem_node, open_marker_start, open_marker_end)

def gAAAAABmw_nQF17gpDqVpga_PSncLDVvzhRJw7ums4UU4fVoWBKlDR34vuZSgSaX__9wqcih9xODoKj4CoOXkPimYv9HQ4i71ZsTVfi7tq2_4h2j84ngQSdiOoFF3TA_k0sMp3m9n9iy(*, string: NulledStr, backquote_range: tuple[int, int], prefix_name_range: None | tuple[int, int], regexes: gAAAAABmw_nQ_1LLl_2FSskoihYO0yx90m6a9e4zq6InTL8YQdLAqOpy0pKQ7X2IwkEx7PuRy_Yso3OsswnkOa8OAh_WoyXLEw__, offset: int, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__: gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_) -> None | gAAAAABmw_nQs1IDsPQIJs_zHLKOQkcS9nKbLDMJ62FgYfKod0iUrXVxHLcewO0AJF6oCNpjWXE0_SRfYY8Ju_z5QAwd80I7sQ__:
    pass
    role_name_range = prefix_name_range
    role_name = gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(string, prefix_name_range[0], prefix_name_range[1]) if prefix_name_range else None
    if not role_name and gAAAAABmw_nQo9xiNueZPgOtfdxO7fiXz64FmmZ_y_5wiie13vi0b1g0kvVmw9oC_GxaEogCohbAIGWWPM0sP7FzhJEfVY6NUg__(string, backquote_range[0], backquote_range[1]):
        return (None, 0, backquote_range[1])
    raw_start = prefix_name_range[0] - 1 if prefix_name_range else backquote_range[0]
    endmatch = re.search(regexes.phrase_end, gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(string, backquote_range[1], None))
    if not (endmatch and gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(endmatch, 1) and (endmatch.start(1) > 0)):
        problem_node1 = ProblematicNode('`', source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(offset + raw_start, offset + raw_start + 1))
        gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__.append(Diagnostic(DiagnosticCode.inline_no_closing_marker, 'Inline role or phrase reference no closing marker.', **gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQEKW8Z5QVDcz8zAdnVq7_7R6AhOK6wN85691Jhv2Jn3No_RZxF7oXvEanh7Qq5kAWFIU_d0t4A_s1ifiJtjqRaN9rCk3CueZA9kSMe6fASJE_(offset + raw_start, offset + raw_start + 1)))
        return (problem_node1, backquote_range[0], backquote_range[1])
    raw_end = backquote_range[1] + endmatch.end(0)
    raw = gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(string, raw_start, raw_end)
    content = gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(string, backquote_range[1], backquote_range[1] + endmatch.start(1))
    if gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(endmatch, 'role'):
        if prefix_name_range:
            problem_node2 = ProblematicNode(gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(raw), source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(offset + raw_start, offset + raw_end))
            gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__.append(Diagnostic(DiagnosticCode.inline_role_malformed, 'Inline role has both prefix and suffix name.', **gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQEKW8Z5QVDcz8zAdnVq7_7R6AhOK6wN85691Jhv2Jn3No_RZxF7oXvEanh7Qq5kAWFIU_d0t4A_s1ifiJtjqRaN9rCk3CueZA9kSMe6fASJE_(offset + raw_start, offset + raw_end)))
            return (problem_node2, raw_start, raw_end)
        if gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(endmatch, 'suffix'):
            role_name_range = (backquote_range[1] + endmatch.start('suffix') + 1, backquote_range[1] + endmatch.end('suffix') - 1)
            role_name = gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(string, role_name_range[0], role_name_range[1])
    if raw.endswith('_'):
        if role_name is not None:
            problem_node3 = ProblematicNode(gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(raw), source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(offset + raw_start, offset + raw_end))
            gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__.append(Diagnostic(DiagnosticCode.inline_role_malformed, 'Role ends with underscore.', **gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQEKW8Z5QVDcz8zAdnVq7_7R6AhOK6wN85691Jhv2Jn3No_RZxF7oXvEanh7Qq5kAWFIU_d0t4A_s1ifiJtjqRaN9rCk3CueZA9kSMe6fASJE_(offset + raw_start, offset + raw_end)))
            return (problem_node3, raw_start, raw_end)
        anonymous = raw.endswith('__')
        if (result := re.search(gAAAAABmw_nQQfKwNJXeQCqsKIZquXHUZKQ6VVtxG6un5TR3Wg8_Sfx2fm0rmMgzvnr0Ln5vwk7AVpUucr3uFw8E36r3TXCkuJCu3q5sAIJgtbfUJavJBtc_, content)):
            text = gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(content, None, result.start(0))
            alias_raw: NulledStr = gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(result, 1)
            alias: NulledStr = gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(result, 2)
            if alias.endswith('_') and (not (alias.endswith('\x00_') or re.match(regexes.uri, alias))):
                _link_node = gAAAAABmw_nQrnCqOVia_v5ZIugvjALcUmt4Iv2IwNml_kQ_ZVzyIXUYuPBQolfeHSX79esZWscqXQKMv_2e7oDn_tr5hprzyqARdYTtBIesDjJq2L3yZMc_(text, gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(alias, None, -1), anonymous, offset + raw_start, offset + raw_end, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__)
                return (_link_node, raw_start, raw_end)
            else:
                _uri_node = gAAAAABmw_nQPurylqEy98VXAodX3qd_4ESLAohkXND0bU4Dj8xFTmil1WlncmwgRAtYpvJZv_1I_xnRe_DK__ts6NeIwvH0Zz1VzGOPzM15wQ0Ut1eFyhM_(text, alias_raw, alias, anonymous, offset + raw_start, offset + raw_end, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__)
                return (_uri_node, raw_start, raw_end)
        else:
            _ref_node = gAAAAABmw_nQjZiaApu8IpwvAPfJT4PBbXyth60_nsQsz_cyokO6rUKgdyL1WWR8t_CXUn_xPU1kvm1cQN8cBt7ekK6ESTnoCtCWhV4k_XvMSI65WS4ayro_(content, anonymous, offset + raw_start, offset + raw_end, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__)
            return (_ref_node, raw_start, raw_end)
    else:
        _role_node = gAAAAABmw_nQu8_rSepqB_Og9oVa4oDqKXurUGspcSF50qwxy1fYMAObGLqSBhyjnubuk2wlZvHesRYqL29ANMaG5VUw_Br_zsTz27qmVTFGyT8jiFTMRCQ_(raw, role_name, content, offset + raw_start, offset + raw_end, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__=gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__)
        return (_role_node, raw_start, raw_end)

def gAAAAABmw_nQJLGWaOIIgPRIHPVEKTJZHkS3Qg_e5TmNWft7ALnq8A_e7fhyI3QHlE1gTl_ZyEbJWRBX94vInlRYHJeYNrfH2ATCMp77KU3gTDV3_QEpS9k_(result: gAAAAABmw_nQDRFHljnIXYFdvGR_QhlA7mcXGZKgkrVukNnARLUCMkUJRW0yQY_lAq7ccgjaqqf_ciM1gqKqL3dL19NA3q_K1XOXUX8APv1q9imbVc9d8Rk_, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> BasicInlineNode:
    pass
    return BasicInlineNode('emphasis', '*', gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(result.content), source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(*result.raw_range))

def gAAAAABmw_nQXcJCQXeX95GbM8wC7pblJelvZUmInLPUdMFhfb9VPc2tDv3QxTs7DFbm2MLyM9NYqWMH5YkZkk7JwgO_VaJDDA__(result: gAAAAABmw_nQDRFHljnIXYFdvGR_QhlA7mcXGZKgkrVukNnARLUCMkUJRW0yQY_lAq7ccgjaqqf_ciM1gqKqL3dL19NA3q_K1XOXUX8APv1q9imbVc9d8Rk_, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> BasicInlineNode:
    pass
    return BasicInlineNode('strong', '**', gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(result.content), source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(*result.raw_range))

def gAAAAABmw_nQrU1basa6IIWgYQ91f5FlerTnqwzQVyvWELmvIM9tM5yT2_2cK7GxXWWTZE3RR8R7RZggKd3__xqZA8RT2V0RwM0hohLHQ9z0xwAoaWJ_GL0_(result: gAAAAABmw_nQDRFHljnIXYFdvGR_QhlA7mcXGZKgkrVukNnARLUCMkUJRW0yQY_lAq7ccgjaqqf_ciM1gqKqL3dL19NA3q_K1XOXUX8APv1q9imbVc9d8Rk_, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> BasicInlineNode:
    pass
    return BasicInlineNode('literal', '``', gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(result.content), source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(*result.raw_range))

def gAAAAABmw_nQ0_5d7JuVbcuGJY3PDMupnjM_Civh_T05nVxmMMFkpcBGcJJF0_ZUtGPGFncDjHkZ1DOueP52iULoy9PFOuoWBaARV9517B1yKSHMjkyzC_c_(result: gAAAAABmw_nQDRFHljnIXYFdvGR_QhlA7mcXGZKgkrVukNnARLUCMkUJRW0yQY_lAq7ccgjaqqf_ciM1gqKqL3dL19NA3q_K1XOXUX8APv1q9imbVc9d8Rk_, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> InlineTargetNode:
    pass
    return InlineTargetNode(gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(result.content), source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(*result.raw_range))

def gAAAAABmw_nQBYntMjEAVDazjgGykrpWrRbWBjHiVYzZw8ZGeqwpIfQhPXpFrU_CfOuAypNcqZUsK3Gq6bZpoGUlu09Pf3nBGAD9H4VlcvrqM_Prr4dedXo_(result: gAAAAABmw_nQDRFHljnIXYFdvGR_QhlA7mcXGZKgkrVukNnARLUCMkUJRW0yQY_lAq7ccgjaqqf_ciM1gqKqL3dL19NA3q_K1XOXUX8APv1q9imbVc9d8Rk_, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> SubstitutionReferenceNode:
    pass
    label = gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(result.content)
    is_reference = False
    anonymous = False
    if result.end_marker.endswith('_'):
        is_reference = True
        if result.end_marker.endswith('__'):
            anonymous = True
    return SubstitutionReferenceNode(label=label, is_reference=is_reference, anonymous=anonymous, source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(*result.raw_range))

def gAAAAABmw_nQ8eH82uhvbQkEIOU4IO88ZKVbjM_Fwxk_FD0fa_OaM6xIpcHM1mMP4cgBJ1qr_fUuxflOmNQ_8eCo08G8_DyeCZ8LQFmwCJ3vaOlP4sJKA5g_(label: NulledStr, start: int, end: int, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> CitationReferenceNode:
    pass
    return CitationReferenceNode(label=label, source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(start, end))

def gAAAAABmw_nQcnbEA_PLvaikdVW4_XshX1EuJjwFp9DctW8UZy_5RDih1DQC3yCRVJWjgRoqujZlTii7ZeNuBWxF5sYugSqbxX8RBcLxJkgOdo68fOGJlaI_(label: NulledStr, start: int, end: int, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> FootnoteReferenceNode:
    pass
    return FootnoteReferenceNode(label=label, source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(start, end))

def gAAAAABmw_nQE5WwmbNa4wijEJ8KydPJZtXMTkoB49A8gD_xnD_0DKw3ea79SaIlW2OG_IvXLi6SYCbtRDibT_LqUulXJctqnSGAfLoL_NWkA5egxcP_wRQ_(text: NulledStr, anonymous: bool, start: int, end: int, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> SimpleReferenceNode:
    pass
    return SimpleReferenceNode(text=text, anonymous=anonymous, source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(start, end))

def gAAAAABmw_nQjZiaApu8IpwvAPfJT4PBbXyth60_nsQsz_cyokO6rUKgdyL1WWR8t_CXUn_xPU1kvm1cQN8cBt7ekK6ESTnoCtCWhV4k_XvMSI65WS4ayro_(text: NulledStr, anonymous: bool, start: int, end: int, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> PhraseReferenceNode:
    pass
    return PhraseReferenceNode(text=gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(text), anonymous=anonymous, source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(start, end))

def gAAAAABmw_nQrnCqOVia_v5ZIugvjALcUmt4Iv2IwNml_kQ_ZVzyIXUYuPBQolfeHSX79esZWscqXQKMv_2e7oDn_tr5hprzyqARdYTtBIesDjJq2L3yZMc_(text: NulledStr, alias: NulledStr, anonymous: bool, start: int, end: int, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> EmbeddedReferenceNode:
    pass
    return EmbeddedReferenceNode(text=gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(text), alias=gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(alias), anonymous=anonymous, source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(start, end))

def gAAAAABmw_nQPurylqEy98VXAodX3qd_4ESLAohkXND0bU4Dj8xFTmil1WlncmwgRAtYpvJZv_1I_xnRe_DK__ts6NeIwvH0Zz1VzGOPzM15wQ0Ut1eFyhM_(text: NulledStr, uri_raw: NulledStr, uri: NulledStr, anonymous: bool, start: int, end: int, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> EmbeddedUriNode:
    pass
    uri_normed = gAAAAABmw_nQG6I9Mw_GOql3wnLmE4ALq8KSxu8gv00GaWX9kAWaGfnCDw0wLeANS6aMRrkB0fnin6JKC4gzdWvE__S7ljXhqQ__(NulledStr(' '.join((''.join(part.split()) for part in gAAAAABmw_nQ_6Wg7yYBKLQJ2DO67Ka1_z9TsafekpmYM_jOucSc9_cd_MOD0bg6y7Xh3208GhKIDdgO56O_eRNL_QWWK35vLnu__BkBmiFdCbVPGN_SNQA_(uri)))))
    if re.match(gAAAAABmw_nQuvc_tG9LEjxsuimSo_KF5CcBrCh8m7DhxjT87n45lhB6xivvEq18F45xBiQ5iFbskOBmzOMMnocb5mqUAWLP9Q__, uri_normed):
        uri_normed = 'mailto:' + uri_normed
    if uri_normed.endswith('\\_'):
        uri_normed = uri_normed[:-2] + '_'
    return EmbeddedUriNode(text=gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(text), uri_raw=gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(uri_raw), uri=uri_normed, anonymous=anonymous, source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(start, end))

def gAAAAABmw_nQu8_rSepqB_Og9oVa4oDqKXurUGspcSF50qwxy1fYMAObGLqSBhyjnubuk2wlZvHesRYqL29ANMaG5VUw_Br_zsTz27qmVTFGyT8jiFTMRCQ_(raw: NulledStr, role_name_or_none: NulledStr | None, content: NulledStr, start: int, end: int, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__: gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_) -> RoleNode:
    pass
    if not role_name_or_none:
        gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__.append(Diagnostic(DiagnosticCode.inline_role_no_name, 'Inline role without name.', **gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQEKW8Z5QVDcz8zAdnVq7_7R6AhOK6wN85691Jhv2Jn3No_RZxF7oXvEanh7Qq5kAWFIU_d0t4A_s1ifiJtjqRaN9rCk3CueZA9kSMe6fASJE_(start, end)))
    return RoleNode(name=role_name_or_none or '', source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(start, end))

def gAAAAABmw_nQ_ktEEUx743NZLZyR9KWU81KYo_Po2ClQZBz4SPxpABd1R8R1bSn60oRIktsentOgyEwLXA9jexO_Sq4x1mzgog8KhEL6DBF0_dgVY9XYxmg_(string: NulledStr, pos: int, regexes: gAAAAABmw_nQ_1LLl_2FSskoihYO0yx90m6a9e4zq6InTL8YQdLAqOpy0pKQ7X2IwkEx7PuRy_Yso3OsswnkOa8OAh_WoyXLEw__, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> None | tuple[int, int, StandaloneUriNode]:
    pass
    if '@' not in string and ':' not in string:
        return None
    if (match := re.search(regexes.uri, string)) is None:
        return None
    if not (schema := gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match, 'scheme')) or schema.lower() in gAAAAABmw_nQnEox51bRTV53Cc4Ifcw7myePsTXbWCKZqeswBXRI7hOUKALaVAuv59TL18YfO_1zPkZJi6A_re72GfBpgBbWzOQweHZpGqgn7kI6KPX25mg_:
        addscheme = 'mailto:' if gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match, 'email') else ''
        raw: NulledStr = gAAAAABmw_nQdamhlP9SUxO9ctdeKaYUZLa3eqYhSPxvIcY8r3IPym4quk1I61yLepqZxxVrzd3NJisdTH7c1wBY1Vpdmea4Hg__(match, 'whole')
        refuri = addscheme + gAAAAABmw_nQG6I9Mw_GOql3wnLmE4ALq8KSxu8gv00GaWX9kAWaGfnCDw0wLeANS6aMRrkB0fnin6JKC4gzdWvE__S7ljXhqQ__(raw)
        uri_node = StandaloneUriNode(raw=gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(raw), uri=refuri, source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(pos + match.start(), pos + match.end()))
        return (match.start(), match.end(), uri_node)
    return None

def gAAAAABmw_nQpvGYjgqvbBRbxuI8XLxN2J_fvli9y4TzNdqkr1HZR43u0uPa3QZ8wYsbdUkxkNErxst_CYaCQMx3dR63bFCVbgit8vgpBaWwIQn6ygi9I_c_(text: NulledStr, pos: int, regexes: gAAAAABmw_nQ_1LLl_2FSskoihYO0yx90m6a9e4zq6InTL8YQdLAqOpy0pKQ7X2IwkEx7PuRy_Yso3OsswnkOa8OAh_WoyXLEw__, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__) -> list[InlineNodeProtocol]:
    pass
    if not text:
        return []
    if (result := gAAAAABmw_nQ_ktEEUx743NZLZyR9KWU81KYo_Po2ClQZBz4SPxpABd1R8R1bSn60oRIktsentOgyEwLXA9jexO_Sq4x1mzgog8KhEL6DBF0_dgVY9XYxmg_(text, pos, regexes, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__)) is not None:
        start, end, _node = result
        return [*gAAAAABmw_nQpvGYjgqvbBRbxuI8XLxN2J_fvli9y4TzNdqkr1HZR43u0uPa3QZ8wYsbdUkxkNErxst_CYaCQMx3dR63bFCVbgit8vgpBaWwIQn6ygi9I_c_(gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(text, None, start), pos, regexes, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__), _node, *gAAAAABmw_nQpvGYjgqvbBRbxuI8XLxN2J_fvli9y4TzNdqkr1HZR43u0uPa3QZ8wYsbdUkxkNErxst_CYaCQMx3dR63bFCVbgit8vgpBaWwIQn6ygi9I_c_(gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(text, end, None), pos + end, regexes, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__)]
    text_node = TextNode(gAAAAABmw_nQTPpiaTFD4LCFVflNndaogcbP8tULRlChX5H5K2PYU6Tg1SqPehz5C4drpOkklnAZ1XKXJcH6XRP4_WPo1juXCq7N_6ACdo1Q0ee5e3UDwXA_(text), source_map=gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__.gAAAAABmw_nQWrODe2b95eS3tDsCNdNRiqJI_7NYyupu8CHL330Dcn3c4Ycez7FiyJnXQ8lG_qDmhS00lPtbhZrAMWaed1HoYw6V2DCcsyXFiLf8i6OTTsY_(pos, pos + len(text)))
    return [text_node]

def gAAAAABmw_nQnRxqoA_C9FeY7o_oPUKvmgk1jJde_ubpIyZlMAVdOvu951axLxdYLl2XSL9ICfpWUY_hVGxZ7pDn_VuYPx1hiw__(inline: InlineNode, gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__: gAAAAABmw_nQ9PTMQEnJGf89Y27v_b38jrWb_Z2WlMU2GvEt6N1G2rMHoL1eFcqRR7s_8cJXFO_Bxw133o5NWnbc4sLnHpxN5g__, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__: gAAAAABmw_nQipwzBodm4uXZsGSqXXckFWKYs_utVRI623uB_j88tQ16LKVnkURIQJPKxU4wC5WMmxpqSzqvEJOb26FDI5SB3g_FoOKAa4OjxfGuDvHUKs4_, *, source_maps: bool=True) -> list[InlineNodeProtocol]:
    pass
    regexes = gAAAAABmw_nQ203zuwgiLpLd6fybibeSxkJR_0O14K8otDj1wstci3Z_kDncpJeC7j9pdIyLDVpQgKVxdgW_l9cExtk8qbznUSSxAW6bXMbdR2k6SwjHtRA_()
    escaped = gAAAAABmw_nQrxQ8oYk58G8bWja9f0Bligp32_mtaHVTIGvBERt3xFf9J_kXxOhNyqp7hRZAEdpmaFe8bMwtPMKDegoBO_t1kw__(inline.raw_content())
    _to_loc: None | dict[int, tuple[LineProtocol, int]] = None

    def _offset_to_location(offset: int) -> tuple[LineProtocol, int]:
        pass
        nonlocal _to_loc
        if _to_loc is None:
            _to_loc = {}
            _offset = 0
            for line in inline._lines:
                line_length = len(line.content)
                for i, _ in enumerate(line.content):
                    _to_loc[_offset + i] = (line, i)
                _to_loc[_offset + i + 1] = (line, i + 1)
                _offset += line_length + 1
        return _to_loc[offset]
    inline_gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__ = gAAAAABmw_nQcD8C8UIIr_FvW6EWOJ7aOxDkD_Aea3oSM68CR_AHl1EeTXHeMQqkZEfqKDhFq07qch0ttbV0x7D7223tiuPlxw__(_source_maps=source_maps, _offset_to_location=_offset_to_location)
    node_list: list[InlineNodeProtocol] = []
    pos = 0
    unprocessed_start = 0
    while (remaining_text := gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(escaped, pos, None)):
        if (result := gAAAAABmw_nQx8uEtbryErvFvHH8mnlJbXB6gSdYpmOYZT1535j_lJQQoOElvyvcEi9wSSs_KoOW628y_IHwOvqEDeDzcJTJhw__(remaining_text, pos, inline_gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__, regexes, gAAAAABmw_nQIe9y6nedqb2RSvsG5IKX90BX_8DDmMhrRKn69UEqn9V8u2ee3koTk1_oRn2fbhslGvBFdC_0lNmNH54YzLz7CQ__)):
            new_node, start, end = result
            if new_node is not None:
                if (unprocessed_text := gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(escaped, unprocessed_start, pos + start)):
                    node_list.extend(gAAAAABmw_nQpvGYjgqvbBRbxuI8XLxN2J_fvli9y4TzNdqkr1HZR43u0uPa3QZ8wYsbdUkxkNErxst_CYaCQMx3dR63bFCVbgit8vgpBaWwIQn6ygi9I_c_(unprocessed_text, unprocessed_start, regexes, inline_gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__))
                unprocessed_start = pos + end
                node_list.append(new_node)
            pos += end
        else:
            break
    if (unprocessed_text := gAAAAABmw_nQZQq2wOFVzVIqU61qaNpEVc_CK2E1LvLh5_DeXXGZTbIWoxP6zFGdowvWA_HGHgehLZrAmqiI065xdqU9PvDRsA__(escaped, unprocessed_start, None)):
        node_list.extend(gAAAAABmw_nQpvGYjgqvbBRbxuI8XLxN2J_fvli9y4TzNdqkr1HZR43u0uPa3QZ8wYsbdUkxkNErxst_CYaCQMx3dR63bFCVbgit8vgpBaWwIQn6ygi9I_c_(unprocessed_text, unprocessed_start, regexes, inline_gAAAAABmw_nQIg39a_mchyt4v3jaUBDXKN_e6IPQGALXkFb550pvCwxwu0LYaIqhTEueRPqCH2YgFhVUAqF74J_6PbCpoHcjVw__))
    return node_list