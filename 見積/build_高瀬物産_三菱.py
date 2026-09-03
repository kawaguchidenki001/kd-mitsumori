# -*- coding: utf-8 -*-
"""高瀬物産 室内機入替工事（三菱電機）— 産廃処理費・運搬費・諸経費を鑑の小計の下へ／諸経費でまるめ
KD見積では「小計の下」に出るのは集計行（率計上・経費）のみなので、この3項目を経費行(expense)にする。
経費行の金額は round(基礎額×率/100)＋端数調整(adj) で決まるため、
率は目安として持たせ、狙った金額との差を adj で合わせる（アプリの「まるめ→諸経費で」と同じ仕組み）。
税抜合計は1,000円単位で切り捨て、端数は諸経費で吸収する。
"""
import json, base64, math

PANEL_PRICE = 36000     # ワイドパネル PAC-SK65WP（ご指示価格）
KOJI_OFF    = 0.8       # 空調更新工事（設備機器設置工事・配管工事）は2割引き
SETS = {
 'PLZX-ERMP224H6': (2974000, 513000, "P224形（8馬力）　同時ツイン　三相200V　ワイヤードリモコン　標準パネル",
   "室内機PL-ERP112HA5×2＋室外機PUZ-ERMP224KA6＋リモコンPAR-48MA＋パネルPLP-P160HWH×2＋分岐管SDD-50WR9", 2),
 'PLZ-ERMP160H6':  (2066000, 354000, "P160形（6馬力）　シングル　三相200V　ワイヤードリモコン　標準パネル",
   "室内機PL-ERP160HA5＋室外機PUZ-ERMP160LA16＋リモコンPAR-48MA＋パネルPLP-P160HWH", 1),
}
def kiki(model):
    """エアコン本体＋仕様の注記行＋ワイドパネル（室内機1台に1セット）＋パネル仕様の注記行"""
    teika, price, spec, comp, n_in = SETS[model]
    note=(f"三菱電機 スリムER 4方向天井カセット形〈i-スクエア〉。{comp}。"
          f"機器費{price:,}円（定価{teika:,}円に対し掛率{price/teika:.3f}）。税抜合計をご指示額に合わせるため機器費で調整")
    return [
      {"name":f"パッケージエアコン　{model}","spec":"","qty":1,"unit":"セット","price":price,"note":note},
      {"name":spec,"spec":"","qty":0,"unit":"　","price":0,"note":f"{model} の仕様（注記行。数量・単価・金額は空欄で出力）"},
      {"name":"ワイドパネル　PAC-SK65WP","spec":"","qty":n_in,"unit":"セット","price":PANEL_PRICE,
       "note":f"{model} の室内機{n_in}台に対し1台1セット。ご指示価格{PANEL_PRICE:,}円／セット"},
      {"name":"外形970×1490　対応可能天井開口860×1380〜910×1430","spec":"","qty":0,"unit":"　","price":0,
       "note":"ワイドパネルの仕様（注記行）。既設開口の実測後に品番を確定すること。純正品で塞げない寸法の場合は木製ワイドパネルでの製作対応となる"},
    ]

def expense_row(name, target, running, note):
    """running（上記計）に対し target 円になる経費行を作る。率は目安、差は adj で吸収。"""
    rate = round(target/running*100, 3)
    adj  = target - round(running*rate/100)
    return {"name":name,"spec":"","expense":rate,"adj":adj,"note":note}, running+target

REF="パナソニックHVAC&CCシステムズ参考見積"
JOBS=[
 dict(tag="A", no="260828", rno="V80DX04-001", taxMode="ex",
   title="高瀬物産名古屋支店　事務所系統　室内機2台入替工事",
   sets=['PLZX-ERMP224H6'], setti=292090, haikan=202680, sanpai=60000, unpan=20000, sho=60000,
   sn="機器搬入据付106,610／機器撤去35,680／リモコン取外し取付8,750／ワイドパネル取付・開口調整20,000×2枚／スライドブロック6,880×2／ユニック車40,000／室外機転倒防止金具8,690／運搬11,140／試運転調整12,300／現場雑費15,160",
   hn="冷媒被覆銅管9.52×3m・15.88×2m・25.40×1m／ACドレン25A×2m／継手・補助材・支持材／配管工費26,560／配管切離し再接続10,000×3台／配線切離し再接続8,130×3台／ラッキング補修10,000／ガス回収16,250／フロン破壊処理3,130×8HP／気密試験10,000／真空引き＋冷媒充填15,000／運搬・現場雑費",
   shn="共通仮設費4,000／現場管理費21,000／一般管理費35,000",
   target=1120000, f="見積_高瀬物産_室内機2台入替_三菱", u="取込リンク_高瀬物産_2台"),
 dict(tag="B", no="260827", rno="V80DX01-001", taxMode="ex",
   title="高瀬物産名古屋支店　事務所系統　室内機3台入替工事",
   sets=['PLZX-ERMP224H6','PLZ-ERMP160H6'], setti=426250, haikan=324950, sanpai=65000, unpan=30000, sho=80000,
   sn="機器搬入据付179,570／機器撤去45,680／リモコン取外し取付8,750×2／ワイドパネル取付・開口調整20,000×3枚／スライドブロック6,880×4／ユニック車40,000／室外機転倒防止金具8,690×2／運搬11,140／試運転調整12,300／現場雑費15,160",
   hn="冷媒被覆銅管9.52×5m・15.88×4m・25.40×1m／ACドレン25A×4m／継手・補助材・支持材／配管工費26,560／配管切離し再接続10,000×5台／配線切離し再接続8,130×5台／ラッキング補修10,000×2／ガス回収16,250×2系統／フロン破壊処理3,130×14HP／気密試験10,000×2／真空引き＋冷媒充填15,000×2／運搬・現場雑費",
   shn="共通仮設費5,000／現場管理費26,000／一般管理費49,000",
   target=1750000, f="見積_高瀬物産_室内機3台入替_三菱", u="取込リンク_高瀬物産_3台"),
]

for j in JOBS:
    same=f"{REF}{j['rno']}と同額"
    rows=[{"type":"cat","name":"機器（三菱電機 スリムER）"}]
    for m in j['sets']: rows += kiki(m)
    rows.append({"type":"cat","name":"空調更新工事"})
    rows += [
      {"name":"設備機器設置工事","spec":"","qty":1,"unit":"式","price":round(j['setti']*KOJI_OFF),
       "note":f"{same}の{j['setti']:,}円を2割引き（×{KOJI_OFF}）。{j['sn']}"},
      {"name":"配管工事","spec":"","qty":1,"unit":"式","price":round(j['haikan']*KOJI_OFF),
       "note":f"{same}の{j['haikan']:,}円を2割引き（×{KOJI_OFF}）。{j['hn']}"},
    ]
    base=sum(r['qty']*r['price'] for r in rows if 'qty' in r)      # 小計（純工事費）
    raw = base + j['sanpai'] + j['unpan'] + j['sho']
    pre = (raw//1000)*1000                                          # 税抜を1,000円単位で切り捨て
    sho = pre - (base + j['sanpai'] + j['unpan'])                   # 端数は諸経費で吸収
    r1,run = expense_row("産廃処理費", j['sanpai'], base, f"{same}。小計の下に経費として計上")
    r2,run = expense_row("運搬費",   j['unpan'],  run,  f"{same}。小計の下に経費として計上")
    r3,run = expense_row("諸経費",   sho,        run,
        f"{j['shn']}（旧「その他経費」を改称）＝{j['sho']:,}円。税抜合計を1,000円単位で切り捨てるため端数{raw-pre:,}円を減算")
    rows += [r1,r2,r3]

    data={"header":{"name":j['title'],"client":"高瀬物産株式会社","honorific":"御中",
                    "no":j['no'],"date":"2026-09-01","staff":"河口"},
          "place":"愛知県名古屋市中村区","remarks":"","taxMode":j['taxMode'],"taxRate":10,"rows":rows}

    # --- アプリの applyComputed を再現して検算 ---
    running=base; amts=[]
    for r in (r1,r2,r3):
        a=round(running*r['expense']/100)+r['adj']; amts.append(a); running+=a
    assert amts==[j['sanpai'], j['unpan'], sho], (amts, j['sanpai'], j['unpan'], sho)
    assert running==pre and pre%1000==0, (running,pre)
    assert pre==j['target'], (pre, j['target'])

    print(f"=== {j['tag']} {j['title']}  NO.{j['no']}  ({j['taxMode']})")
    for r in rows:
        if r.get('type')=='cat': print(f"  ■ {r['name']}")
        elif 'expense' in r: pass
        elif r['qty']==0: print(f"      └ {r['name']}")
        else: print(f"    {r['name'][:32]:32} {r['qty']}{r['unit']:4} {r['price']:>9,}")
    print(f"  小　　　計                                    {base:>9,}")
    for r,a in zip((r1,r2,r3),amts):
        print(f"    {r['name']:<10}（上記計×{r['expense']}%＋端数調整{r['adj']:+d}）      {a:>9,}")
    print(f"  計（税抜）                                    {pre:>9,}   ← 1,000円単位（旧 {raw:,}）")
    if j['taxMode']!='ex': print(f"  消費税 {round(pre*0.1):,}／税込 {pre+round(pre*0.1):,}")
    out=f"/home/user/kd-mitsumori/見積/{j['f']}.json"
    open(out,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=1))
    b64=base64.urlsafe_b64encode(json.dumps(data,ensure_ascii=False,separators=(",",":")).encode()).decode().rstrip("=")
    url="https://kawaguchidenki001.github.io/kd-mitsumori/#import="+b64
    open(f"/home/user/kd-mitsumori/見積/{j['u']}.txt",'w').write(url)
    assert json.loads(base64.urlsafe_b64decode(b64+"=="*2).decode())==data
    print(f"  URL長 {len(url)} round-trip OK\n")
