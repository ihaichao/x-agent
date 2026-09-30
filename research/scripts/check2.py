import json,sys,re,urllib.request,concurrent.futures as cf
KW=re.compile(r'美股|\$[A-Z]{2,5}|纳指|标普|英伟达|特斯拉|美联储|NVDA|TSLA|财报|仓位')
def get(n):
    try:
        u=json.load(urllib.request.urlopen(f"https://api.fxtwitter.com/{n}",timeout=20))['user']
        d=json.load(urllib.request.urlopen(f"https://api.fxtwitter.com/2/profile/{n}/statuses",timeout=30))
        ts=[r.get('text') or '' for r in d.get('results',[]) if (r.get('author') or {}).get('screen_name','').lower()==n.lower()]
        zh=sum(1 for t in ts if len(re.findall(r'[一-鿿]',t))>=max(5,len(t)*0.2))
        st=sum(1 for t in ts if KW.search(t))
        return n,u['followers'],u['name'],f"中文帖{zh}/{len(ts)} 美股相关{st}",(u.get('description') or '').replace('\n',' ')[:50]
    except Exception as e: return n,0,'ERR','',''
with cf.ThreadPoolExecutor(8) as ex:
    for r in sorted(ex.map(get,sys.argv[1:]),key=lambda r:-r[1]): print(r)
