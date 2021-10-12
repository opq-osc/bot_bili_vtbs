"""查成分，查看B站关注虚拟主播成分
发送：查成分+B站ID
"""
import json
from pathlib import Path

from botoy import S
from botoy.decorators import ignore_botself, on_regexp
import httpx

vtb_path = Path(__file__).absolute().parent / 'vtbs.json'

with open(vtb_path) as f:
    vtbs_data = json.load(f)


@ignore_botself
@on_regexp(r"查成分(\d+)")
def receive_group_msg(ctx):
    resp = httpx.get(
        f'https://account.bilibili.com/api/member/getCardByMid?mid={ctx._match.group(1)}',
        timeout=10,
    )
    ret = resp.json()
    if ret['code'] != 0:
        return

    card = ret['card']

    vtbs = []
    for mid in card['attentions']:
        mid = str(mid)
        if mid in vtbs_data:
            vtb = vtbs_data[mid]
            vtbs.append(f"{vtb['uname']}({mid})")

    vtb_count = len(vtbs)
    vtb_msg = '、'.join(vtbs)

    S.image(
        card['face'], f"{card['name']}({card['mid']})关注了 {vtb_count} 个vtb:\n{vtb_msg}"
    )
