import json,sys,urllib.request,concurrent.futures as cf
names=sys.argv[1:]
def get(n):
    try:
        d=json.load(urllib.request.urlopen(f"https://api.fxtwitter.com/{n}",timeout=20))
        u=d.get('user') or {}
        return n,u.get('followers'),u.get('name'),(u.get('description') or '').replace('\n',' ')[:70]
    except Exception as e: return n,None,str(e)[:40],''
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(get,names): print(r)
