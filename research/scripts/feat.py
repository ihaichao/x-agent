import json,re,statistics as st,datetime as dt,collections
P=json.load(open('all.json'))
seen=set();Q=[]
for p in P:
    if p['id'] in seen: continue
    seen.add(p['id']);Q.append(p)
ZH=set('xiaomustock qinbafrank TJ_Research maojietrading hanking66 TiezhuCrypto dacefupan yuyue_chris cnfinancewatch'.split())
NEWS=set('unusual_whales StockMKTNewz wallstengine KobeissiLetter'.split())
def feats(p):
    t=p['text'] or ''
    n=len(t)
    f={}
    f['长度']= '短(<60字)' if n<60 else '中(60-280)' if n<280 else '长(280+)'
    f['配图']= '视频' if 'video' in p['media'] else '图片' if p['media'] else '纯文字'
    f['引用别人帖']= '是' if p['has_quote'] else '否'
    f['第一人称(我/I)']= '是' if re.search(r'我|\bI\b|\bI\'m|\bmy\b',t) else '否'
    f['提问(?/？)']= '是' if re.search(r'[?？]',t) else '否'
    f['有数字/百分比']= '是' if re.search(r'\d+(\.\d+)?%|\$\d|\d{2,}',t) else '否'
    f['带$代码']= '是' if re.search(r'\$[A-Za-z]{1,5}\b',t) else '否'
    f['BREAKING/突发']= '是' if re.search(r'BREAKING|JUST IN|突发|刚刚',t) else '否'
    f['表情符号']= '是' if re.search(r'[\U0001F300-\U0001FAFF]',t) else '否'
    f['分点列表']= '是' if re.search(r'(^|\n)\s*(\d[\.、)]|[-•▫️])',t) else '否'
    h=(dt.datetime.utcfromtimestamp(p['ts'])+dt.timedelta(hours=8)).hour
    f['北京时间']= '00-06' if h<6 else '06-12' if h<12 else '12-18' if h<18 else '18-24'
    return f
for name,grp in [('中文账号',[p for p in Q if p['acct'] in ZH]),('英文个人账号',[p for p in Q if p['acct'] not in ZH and p['acct'] not in NEWS and p['acct'] not in('BTCdayu','labubu_trader','Jason23818126')])]:
    print('#',name,len(grp))
    agg=collections.defaultdict(list)
    for p in grp:
        for k,v in feats(p).items(): agg[(k,v)].append(p)
    cur=None
    for (k,v),ps in sorted(agg.items()):
        if k!=cur: print(' ',k); cur=k
        xs=[p['x'] for p in ps]
        top=sum(1 for x in xs if x>=2)/len(xs)
        rr=st.median((p['replies']+1)/(p['likes']+1) for p in ps); br=st.median((p['bookmarks'] or 0+1)/(p['likes']+1) for p in ps)
        print(f"    {v:12} n={len(ps):4}  中位倍数={st.median(xs):.2f}  爆款率(≥2倍)={top:.0%}  评/赞={rr:.2f} 藏/赞={br:.2f}")
