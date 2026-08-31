# -*- coding: utf-8 -*-
"""高瀬物産名古屋支店 室内機入替工事（三菱電機）— 修正版
 ・エアコン本体価格を1,000円単位で繰り上げ
 ・品名欄の主行に品名＋型番、下段（spec）に馬力・ツイン／シングル・電源・リモコン・パネルの仕様
 ・有期一括保険代を削除
 ・「その他経費」を「諸経費」に改称し、運搬費の下へ移動
"""
import json, base64, math
def up1000(v): return math.ceil(v/1000)*1000

SETS = {
 'PLZX-ERMP224H6': (2974000, 475000, "P224形（8馬力）　同時ツイン　三相200V　ワイヤードリモコン　標準パネル",
   "室内機PL-ERP112HA5×2＋室外機PUZ-ERMP224KA6＋リモコンPAR-48MA＋パネルPLP-P160HWH×2＋分岐管SDD-50WR9"),
 'PLZ-ERMP160H6':  (2066000, 330000, "P160形（6馬力）　シングル　三相200V　ワイヤードリモコン　標準パネル",
   "室内機PL-ERP160HA5＋室外機PUZ-ERMP160LA16＋リモコンPAR-48MA＋パネルPLP-P160HWH"),
}
def kiki(model):
    """1行目＝品名＋型番（数量・単価あり）／2行目＝仕様の注記行（数量0・単価0で数量単価金額とも空欄出力）"""
    teika, price, spec, comp = SETS[model]
    note = (f"三菱電機 スリムER 4方向天井カセット形〈i-スクエア〉。{comp}。"
            f"ご指示価格{price:,}円（定価{teika:,}円＝総合カタログ業務用2026-3 積算見積価格・税別に対し掛率{price/teika:.3f}）")
    return [
      {"name":f"パッケージエアコン　{model}","spec":"","qty":1,"unit":"セット","price":price,"note":note},
      {"name":spec,"spec":"","qty":0,"unit":"　","price":0,"note":f"{model} の仕様（注記行。数量・単価・金額は空欄で出力）"},
    ]

REF="パナソニックHVAC&CCシステムズ参考見積"
def koji(no, setti, haikan, sanpai, unpan, shokei, setti_n, haikan_n):
    same=f"{REF}{no}と同額"
    return [
     {"name":"設備機器設置工事","spec":"","qty":1,"unit":"式","price":setti,"note":f"{same}。{setti_n}"},
     {"name":"配管工事","spec":"","qty":1,"unit":"式","price":haikan,"note":f"{same}。{haikan_n}"},
     {"name":"産廃処理費","spec":"","qty":1,"unit":"式","price":sanpai,"note":same},
     {"name":"運搬費","spec":"","qty":1,"unit":"式","price":unpan,"note":same},
     {"name":"諸経費","spec":"","qty":1,"unit":"式","price":shokei,"note":shokei_note(shokei)},
    ]
NOTE_SHO={60000:"共通仮設費4,000／現場管理費21,000／一般管理費35,000",
          80000:"共通仮設費5,000／現場管理費26,000／一般管理費49,000"}
def shokei_note(v): return NOTE_SHO[v]+"（旧「その他経費」を改称）"

JOBS=[
 dict(tag="A", no="260828", ref="V80DX04-001", taxMode="out",
   title="高瀬物産名古屋支店　事務所系統　室内機2台入替工事",
   sets=['PLZX-ERMP224H6'], old=1143770,
   koji=koji("V80DX04-001",292090,202680,60000,20000,60000,
     "機器搬入据付106,610／機器撤去35,680／リモコン取外し取付8,750／ワイドパネル20,000×2枚／スライドブロック6,880×2／ユニック車40,000／室外機転倒防止金具8,690／運搬11,140／試運転調整12,300／現場雑費15,160",
     "冷媒被覆銅管9.52×3m・15.88×2m・25.40×1m／ACドレン25A×2m／継手・補助材・支持材／配管工費26,560／配管切離し再接続10,000×3台／配線切離し再接続8,130×3台／ラッキング補修10,000／ガス回収16,250／フロン破壊処理3,130×8HP／気密試験10,000／真空引き＋冷媒充填15,000／運搬・現場雑費"),
   f="見積_高瀬物産_室内機2台入替_三菱", u="取込リンク_高瀬物産_2台"),
 dict(tag="B", no="260827", ref="V80DX01-001", taxMode="ex",
   title="高瀬物産名古屋支店　事務所系統　室内機3台入替工事",
   sets=['PLZX-ERMP224H6','PLZ-ERMP160H6'], old=1789200,
   koji=koji("V80DX01-001",426250,324950,65000,30000,80000,
     "機器搬入据付179,570／機器撤去45,680／リモコン取外し取付8,750×2／ワイドパネル20,000×3枚／スライドブロック6,880×4／ユニック車40,000／室外機転倒防止金具8,690×2／運搬11,140／試運転調整12,300／現場雑費15,160",
     "冷媒被覆銅管9.52×5m・15.88×4m・25.40×1m／ACドレン25A×4m／継手・補助材・支持材／配管工費26,560／配管切離し再接続10,000×5台／配線切離し再接続8,130×5台／ラッキング補修10,000×2／ガス回収16,250×2系統／フロン破壊処理3,130×14HP／気密試験10,000×2／真空引き＋冷媒充填15,000×2／運搬・現場雑費"),
   f="見積_高瀬物産_室内機3台入替_三菱", u="取込リンク_高瀬物産_3台"),
]

for j in JOBS:
    rows=[{"type":"cat","name":"機器（三菱電機 スリムER）"}]
    for m in j['sets']: rows += kiki(m)
    rows.append({"type":"cat","name":"空調更新工事"})
    rows += j['koji']
    data={"header":{"name":j['title'],"client":"高瀬物産株式会社","honorific":"御中",
                    "no":j['no'],"date":"2026-08-28","staff":"河口"},
          "place":"愛知県名古屋市中村区","remarks":"","taxMode":j['taxMode'],"taxRate":10,"rows":rows}
    net=sum(r['qty']*r['price'] for r in rows if 'qty' in r)
    ki=sum(r['qty']*r['price'] for r in rows if r.get('unit')=='セット')
    print(f"=== {j['tag']} {j['title']}  NO.{j['no']}  taxMode={j['taxMode']}")
    for r in rows:
        if r.get('type')=='cat': print(f"  ■ {r['name']}")
        elif r['qty']==0: print(f"      └ {r['name']}")
        else: print(f"    {r['name'][:34]:34} {r['qty']}{r['unit']:4} {r['price']:>9,}")
    print(f"    機器計 {ki:,} ／ 工事計 {net-ki:,}")
    print(f"    工事価格（税抜）{net:,}  （旧 {j['old']:,} → {net-j['old']:+,}）")
    if j['taxMode']!='ex': print(f"    消費税 {round(net*0.1):,}  税込 {net+round(net*0.1):,}")
    out=f"/home/user/kd-mitsumori/見積/{j['f']}.json"
    open(out,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=1))
    b64=base64.urlsafe_b64encode(json.dumps(data,ensure_ascii=False,separators=(",",":")).encode()).decode().rstrip("=")
    url="https://kawaguchidenki001.github.io/kd-mitsumori/#import="+b64
    open(f"/home/user/kd-mitsumori/見積/{j['u']}.txt",'w').write(url)
    assert json.loads(base64.urlsafe_b64decode(b64+"=="*2).decode())==data
    print(f"    URL長 {len(url)} round-trip OK\n")
