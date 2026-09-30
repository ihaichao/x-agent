import json,sys,time,urllib.request,urllib.parse,concurrent.futures as cf,os
CUTOFF=time.time()-45*86400
def fetch(url):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(url,timeout=30))
        except Exception as e: time.sleep(2**i)
    return None
def scrape(n):
    out=[];cur=None
    for page in range(12):
        url=f"https://api.fxtwitter.com/2/profile/{n}/statuses"+(f"?cursor={urllib.parse.quote(cur)}" if cur else "")
        d=fetch(url)
        if not d or not d.get('results'): break
        old=0
        for r in d['results']:
            a=(r.get('author') or {}).get('screen_name','')
            if r.get('reposted_by') or a.lower()!=n.lower(): continue
            if r.get('created_timestamp',0)<CUTOFF: old+=1; continue
            out.append(dict(acct=n,id=r['id'],url=r['url'],text=r.get('text'),likes=r.get('likes'),reposts=r.get('reposts'),replies=r.get('replies'),
              quotes=r.get('quotes'),bookmarks=r.get('bookmarks'),views=r.get('views'),ts=r.get('created_timestamp'),created=r.get('created_at'),lang=r.get('lang'),
              reply=bool(r.get('replying_to')),media=[m.get('type') for m in ((r.get('media') or {}).get('all') or [])],
              has_quote=bool(r.get('quote')),quote_text=((r.get('quote') or {}).get('text') or '')[:300],long=r.get('is_note_tweet'),
              article=(r.get('article') or {}).get('title') if r.get('article') else None,qa=((r.get('quote') or {}).get('author') or {}).get('screen_name'),rt=(r.get('replying_to') or {}).get('screen_name') if isinstance(r.get('replying_to'),dict) else r.get('replying_to')))
        if old>=len(d['results'])//2: break
        cur=(d.get('cursor') or {}).get('bottom')
        if not cur: break
    json.dump(out,open(f"data/{n}.json","w"),ensure_ascii=False)
    return n,len(out)
os.makedirs("data",exist_ok=True)
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(scrape,sys.argv[1:]): print(r,flush=True)
