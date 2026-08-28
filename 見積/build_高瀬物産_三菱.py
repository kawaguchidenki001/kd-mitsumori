# -*- coding: utf-8 -*-
"""高瀬物産名古屋支店 事務所系統 室内機入替工事 — 三菱電機での自社見積（2種類）
パナソニックHVAC&CCシステムズの参考見積 V80DX04-001(2台) / V80DX01-001(3台) と
同等の内容を、三菱電機 スリムER のセット品番に置き換えたもの。
機器：セット品番1行。定価は三菱電機「総合カタログ 業務用2026-3」積算見積価格（税別）。
      掛率は参考見積の機器価格 ÷ 三菱同等セット定価 から 0.171 を仮置き。
工事：参考見積と工事内容・数量が同一のため、同額を踏襲（法定福利費を含む）。
"""
import json, base64

MK = 0.171   # 掛率（仮置き）
SET = {  # セット品番: (定価, 説明)
 'PLZX-ERMP224H6': (2974000, "事務所ツイン P224形(8馬力) 同時ツイン／三相200V／ワイヤード／標準パネル。室内機PL-ERP112HA5×2＋室外機PUZ-ERMP224KA6＋リモコンPAR-48MA＋パネルPLP-P160HWH×2＋分岐管SDD-50WR9"),
 'PLZ-ERMP160H6' : (2066000, "事務所シングル P160形(6馬力) シングル／三相200V／ワイヤード／標準パネル。室内機PL-ERP160HA5＋室外機PUZ-ERMP160LA16＋リモコンPAR-48MA＋パネルPLP-P160HWH"),
}
def kiki(model, ref):
    teika, desc = SET[model]
    p = int(round(teika*MK/10))*10
    note = (f"三菱電機 スリムER 4方向天井カセット形〈i-スクエア〉。{desc}。"
            f"定価{teika:,}円（総合カタログ業務用2026-3 積算見積価格・税別）×掛率{MK}。"
            f"掛率は参考見積の同等機器{ref:,}円÷定価から算出した仮置き。御社仕切りに合わせて要調整")
    return p, note

def build(no, title, sets, koji, refs):
    rows=[{"type":"cat","name":"機器（三菱電機 スリムER）"}]
    for m, ref in sets:
        p, note = kiki(m, ref)
        rows.append({"name":"パッケージエアコン","spec":m,"qty":1,"unit":"セット","price":p,"note":note})
    rows.append({"type":"cat","name":"空調更新工事"})
    for name, spec, amt, note in koji:
        rows.append({"name":name,"spec":spec,"qty":1,"unit":"式","price":amt,"note":note})
    data={"header":{"name":title,"client":"高瀬物産株式会社","honorific":"御中",
                    "date":"2026-08-28","staff":"河口"},
          "place":"愛知県名古屋市中村区","remarks":"","taxMode":"out","taxRate":10,"rows":rows}
    net=sum(r['qty']*r['price'] for r in rows if 'qty' in r)
    return data, net

REF = "パナソニックHVAC&CCシステムズ参考見積"
# ---- A: 室内機2台入替（V80DX04-001 総額1,150,000） ----
kojiA = [
 ("設備機器設置工事","",292090, f"{REF}V80DX04-001と同額。機器搬入据付106,610／機器撤去35,680／リモコン取外し取付8,750／ワイドパネル20,000×2枚／スライドブロック6,880×2／ユニック車40,000／室外機転倒防止金具8,690／運搬11,140／試運転調整12,300／現場雑費15,160"),
 ("配管工事","",202680, f"{REF}V80DX04-001と同額。冷媒被覆銅管9.52×3m・15.88×2m・25.40×1m／ACドレン25A×2m／継手・補助材・支持材／配管工費26,560／配管切離し再接続10,000×3台／配線切離し再接続8,130×3台／ラッキング補修10,000／ガス回収16,250／フロン破壊処理3,130×8HP／気密試験10,000／真空引き＋冷媒充填15,000／運搬・現場雑費"),
 ("その他経費","",60000, "共通仮設費4,000／現場管理費21,000／一般管理費35,000"),
 ("産廃処理費","",60000, f"{REF}V80DX04-001と同額"),
 ("運搬費","",20000, f"{REF}V80DX04-001と同額"),
 ("有期一括保険代","",5000, f"{REF}V80DX04-001と同額"),
]
# ---- B: 室内機3台入替（V80DX01-001 総額1,800,000） ----
kojiB = [
 ("設備機器設置工事","",426250, f"{REF}V80DX01-001と同額。機器搬入据付179,570／機器撤去45,680／リモコン取外し取付8,750×2／ワイドパネル20,000×3枚／スライドブロック6,880×4／ユニック車40,000／室外機転倒防止金具8,690×2／運搬11,140／試運転調整12,300／現場雑費15,160"),
 ("配管工事","",324950, f"{REF}V80DX01-001と同額。冷媒被覆銅管9.52×5m・15.88×4m・25.40×1m／ACドレン25A×4m／継手・補助材・支持材／配管工費26,560／配管切離し再接続10,000×5台／配線切離し再接続8,130×5台／ラッキング補修10,000×2／ガス回収16,250×2系統／フロン破壊処理3,130×14HP／気密試験10,000×2／真空引き＋冷媒充填15,000×2／運搬・現場雑費"),
 ("その他経費","",80000, "共通仮設費5,000／現場管理費26,000／一般管理費49,000"),
 ("産廃処理費","",65000, f"{REF}V80DX01-001と同額"),
 ("運搬費","",30000, f"{REF}V80DX01-001と同額"),
 ("有期一括保険代","",10000, f"{REF}V80DX01-001と同額"),
]

JOBS = [
 ("A", "高瀬物産名古屋支店　事務所系統　室内機2台入替工事",
      [('PLZX-ERMP224H6',510230)], kojiA, 1150000, "V80DX04-001",
      "見積_高瀬物産_室内機2台入替_三菱", "取込リンク_高瀬物産_2台"),
 ("B", "高瀬物産名古屋支店　事務所系統　室内機3台入替工事",
      [('PLZX-ERMP224H6',510230),('PLZ-ERMP160H6',353570)], kojiB, 1800000, "V80DX01-001",
      "見積_高瀬物産_室内機3台入替_三菱", "取込リンク_高瀬物産_3台"),
]

for tag, title, sets, koji, ref_total, ref_no, fname, uname in JOBS:
    data, net = build(ref_no, title, sets, koji, ref_total)
    kiki_sum = sum(r['qty']*r['price'] for r in data['rows'] if r.get('unit')=='セット')
    koji_sum = net - kiki_sum
    print(f"=== {tag} {title}  （参考見積 {ref_no}：{ref_total:,}円）")
    for r in data['rows']:
        if r.get('type')=='cat': print(f"  ■ {r['name']}")
        else: print(f"    {r['name'][:14]:14} {r['spec'][:16]:16} {r['qty']}{r['unit']:4} {r['price']:>10,}")
    print(f"    機器計 {kiki_sum:>10,} ／ 工事計 {koji_sum:>10,}")
    print(f"    工事価格（税抜）{net:>12,}   消費税 {round(net*0.1):>10,}   税込 {net+round(net*0.1):>12,}")
    print(f"    参考見積との差 {net-ref_total:+,}円")
    out=f'/home/user/kd-mitsumori/見積/{fname}.json'
    open(out,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=1))
    b64=base64.urlsafe_b64encode(json.dumps(data,ensure_ascii=False,separators=(",",":")).encode()).decode().rstrip("=")
    url="https://kawaguchidenki001.github.io/kd-mitsumori/#import="+b64
    open(f'/home/user/kd-mitsumori/見積/{uname}.txt','w').write(url)
    assert json.loads(base64.urlsafe_b64decode(b64+"=="*2).decode())==data
    print(f"    URL長 {len(url)} round-trip OK\n")
