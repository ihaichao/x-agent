import json,glob,statistics as st,re,collections
P=[]
for f in glob.glob('data/*.json'): P+=json.load(open(f))
P=[p for p in P if not p['reply'] and p['views']]
by=collections.defaultdict(list)
for p in P: by[p['acct']].append(p)
print(f"{'acct':16}{'n':>5}{'medV':>9}{'medLike':>8}{'medRep':>7}{'medBM':>7}")
for a,ps in sorted(by.items(),key=lambda x:-st.median(p['views'] for p in x[1])):
    mv=st.median(p['views'] for p in ps)
    for p in ps: p['x']=p['views']/mv; p['mv']=mv
    print(f"{a:16}{len(ps):>5}{int(mv):>9}{int(st.median(p['likes'] for p in ps)):>8}{int(st.median(p['replies'] for p in ps)):>7}{int(st.median(p['bookmarks'] or 0 for p in ps)):>7}")
json.dump(P,open('all.json','w'),ensure_ascii=False)
