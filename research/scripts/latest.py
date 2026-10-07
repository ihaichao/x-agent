"""抓最近 N 小时的热门帖子，用来选题。

用法：python3 research/scripts/latest.py [小时数，默认 14]
输出两组：英文快讯号（看发生了什么）、中文美股号（看中文圈在聊什么），按浏览量排序。
"""
import json, sys, time, urllib.request, urllib.parse, concurrent.futures as cf

HOURS = float(sys.argv[1]) if len(sys.argv) > 1 else 14
CUTOFF = time.time() - HOURS * 3600
EN = ['KobeissiLetter', 'wallstengine', 'StockMKTNewz', 'unusual_whales', 'amitisinvesting', 'charliebilello']
ZH = ['qinbafrank', 'TJ_Research', 'hanking66', 'maojietrading', 'xiaomustock', 'ShanghaoJin',
      'MacroMargin', 'artinmemes', 'shufen46250836', 'bboczeng', 'cnfinancewatch']


def fetch(url):
    for i in range(3):
        try:
            return json.load(urllib.request.urlopen(url, timeout=30))
        except Exception:
            time.sleep(2 ** i)
    return None


def scrape(n):
    out, cur = [], None
    for _ in range(4):
        url = f"https://api.fxtwitter.com/2/profile/{n}/statuses" + (f"?cursor={urllib.parse.quote(cur)}" if cur else "")
        d = fetch(url)
        if not d or not d.get('results'):
            break
        old = 0
        for r in d['results']:
            if r.get('reposted_by') or (r.get('author') or {}).get('screen_name', '').lower() != n.lower():
                continue
            if r.get('replying_to'):
                continue
            if r.get('created_timestamp', 0) < CUTOFF:
                old += 1
                continue
            out.append((r.get('views') or 0, n, r.get('created_timestamp'), r.get('text') or '', r.get('url')))
        if old:
            break
        cur = (d.get('cursor') or {}).get('bottom')
        if not cur:
            break
    return out


with cf.ThreadPoolExecutor(8) as ex:
    res = dict(zip(EN + ZH, ex.map(scrape, EN + ZH)))

for title, group, k in (('英文快讯', EN, 40), ('中文美股圈', ZH, 25)):
    print(f'##### {title}')
    rows, seen = [], set()
    for n in group:
        rows += res[n]
    for v, n, ts, t, u in sorted(rows, reverse=True)[:k]:
        if u in seen:
            continue
        seen.add(u)
        when = time.strftime('%m-%d %H:%M', time.gmtime(ts + 8 * 3600))
        print(f"{when}(UTC+8) {n[:10]} {v} | {t[:300].replace(chr(10), ' / ')}")
