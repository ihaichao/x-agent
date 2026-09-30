import json,re,statistics as st,datetime as dt,collections
P=json.load(open('zh.json'))
def feats(p):
    t=p['text'] or '';n=len(t);f={}
    f['话题']='聊投资/市场' if p['inv'] else '跑题(生活/社会/八卦)'
    f['形式']='X长文(Article)' if p['is_article'] else ('短(<60字)' if n<60 else '中(60-280字)' if n<280 else '长(280字+)')
    f['配图']='视频' if 'video' in p['media'] else '图片' if p['media'] else '纯文字'
    f['引用别人帖']='是' if p['has_quote'] else '否'
    f['第一人称(我)']='是' if '我' in t else '否'
    f['提问(？)']='是' if re.search(r'[?？]',t) else '否'
    f['有具体数字']='是' if re.search(r'\d+(\.\d+)?%|\d{2,}',t) else '否'
    f['分点(1、/一、)']='是' if re.search(r'(^|\n)\s*(\d[\.、)）]|[一二三四五][、，])',t) else '否'
    f['提到自己买卖']='是' if re.search(r'我.{0,8}(买|卖|加仓|减仓|清仓|止盈|止损|建仓|持有|仓位)',t) else '否'
    f['情绪词(卧槽/太牛/哈哈/傻逼等)']='是' if re.search(r'卧槽|太牛|牛逼|哈哈|傻逼|吃屎|特么|我靠|离谱|笑死|麻了|😂|🤣',t) else '否'
    d=dt.datetime.utcfromtimestamp(p['ts'])+dt.timedelta(hours=8);h=d.hour
    f['北京时间']='00-06' if h<6 else '06-12' if h<12 else '12-18' if h<18 else '18-24'
    f['星期(北京)']='周末' if d.weekday()>=5 else '工作日'
    return f
agg=collections.defaultdict(list)
for p in P:
    for k,v in feats(p).items(): agg[(k,v)].append(p)
order=['话题','形式','配图','引用别人帖','第一人称(我)','提问(？)','有具体数字','分点(1、/一、)','提到自己买卖','情绪词(卧槽/太牛/哈哈/傻逼等)','北京时间','星期(北京)']
for k in order:
    print(k)
    for (kk,v),ps in sorted(agg.items()):
        if kk!=k: continue
        xs=[p['x'] for p in ps]
        rr=st.median((p['replies']+1)/(p['likes']+1) for p in ps); br=st.median(((p['bookmarks'] or 0)+1)/(p['likes']+1) for p in ps)
        print(f"   {v:22} 帖数={len(ps):4} 中位倍数={st.median(xs):.2f} 爆款率(≥2倍)={sum(x>=2 for x in xs)/len(xs):.0%} 大爆率(≥5倍)={sum(x>=5 for x in xs)/len(xs):.1%} 评/赞={rr:.2f} 藏/赞={br:.2f}")
