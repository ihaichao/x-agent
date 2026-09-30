import json,re,statistics as st,collections
ACC='qinbafrank TJ_Research hanking66 maojietrading xiaomustock cnfinancewatch TiezhuCrypto lidangzzz bboczeng MacroMargin rickawsb ShanghaoJin artinmemes shufen46250836 lianyanshe iamramenpanda yiqifacai amy6tina _wmoon SYU77996 Sinus84 168X_Fortune'.split()
INV=re.compile(r'美股|股|\$[A-Za-z]{1,5}|纳指|标普|纳斯达克|英伟达|特斯拉|美联储|加息|降息|美债|收益率|财报|仓位|持仓|买入|卖出|抄底|止盈|止损|ETF|期权|半导体|芯片|存储|光模块|估值|市值|牛市|熊市|大盘|行情|AI|算力|CPI|非农|通胀|油价|黄金|NVDA|TSLA|AAPL|GOOG|META|MSFT|AMZN|AMD|INTC|MU|QQQ|SPY|IPO|回购|营收|利润|基金|投资|交易|涨|跌',re.I)
def iszh(t): 
    c=len(re.findall(r'[一-鿿]',t)); return c>=5 and c>=len(t)*0.2
P=[];seen=set()
for a in ACC:
    for p in json.load(open(f'data/{a}.json')):
        t=p['text'] or ''
        if p['reply'] or not p['views'] or p['id'] in seen: continue
        linkonly=re.fullmatch(r'\s*https://x\.com/i/article/\d+\s*',t)
        if not (iszh(t) or linkonly): continue
        seen.add(p['id']); p['is_article']=bool(linkonly); p['inv']=bool(linkonly or INV.search(t+p.get('quote_text','')))
        P.append(p)
by=collections.defaultdict(list)
for p in P: by[p['acct']].append(p)
print(f"{'账号':16}{'中文帖':>6}{'平时浏览':>9}{'平时赞':>7}{'平时评':>7}{'平时藏':>7}")
for a,ps in sorted(by.items(),key=lambda x:-st.median(p['views'] for p in x[1])):
    mv=st.median(p['views'] for p in ps)
    for p in ps: p['x']=p['views']/mv; p['mv']=mv
    print(f"{a:16}{len(ps):>6}{int(mv):>9}{int(st.median(p['likes'] for p in ps)):>7}{int(st.median(p['replies'] for p in ps)):>7}{int(st.median(p['bookmarks'] or 0 for p in ps)):>7}")
print('总帖数',len(P))
json.dump(P,open('zh.json','w'),ensure_ascii=False)
