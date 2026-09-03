# -*- coding: utf-8 -*-
"""岐阜市中央卸売市場北側高架衝突防止設置工事 — 電気工事 参考見積
設計内訳書 p.8「2 電気工事」の行構成・数量をそのまま踏襲する。
様式は「材料費行 → 電工費(1式) → 高所作業車損料(1式) → 塗装費(1式)」であり、
材料行の単価は材料費、労務は電工費に一括する形のため、
複合単価の 材料費 を明細単価に、Σ(数量×(労務費+経費)) を電工費に充てる。
共通仮設費・現場管理費・一般管理費は内訳書0-0-1で建築工事と一括計上のため、本見積は直接工事費のみ。
"""
import json, base64
DB = json.load(open('unit_prices.json'))
def q(n,s,w=None):
    r=[e for e in DB if e['name']==n and e['spec']==s and (w is None or e['work']==w)]
    assert len(r)==1,(n,s,w,len(r)); return r[0]
def M(e): return e['material_cost']
def T(e): return e['labor_cost']+e['expense']      # 取付手間＝労務費＋経費

cp19 = q('電線管','CP-19','露出');            cp25 = q('電線管','CP-25','露出')
hive = q('電線管','HIVE 16','露出');          f17  = q('二種金属製可とう電線管(F2)','17 ビニル被覆')
obox = q('アウトレットボックス','四角中深 102×102×54 塗代付')
pbox = q('プルボックス','SS200×200×200 WP-SUS')
e20  = q('ケーブル','EM-EEF 2.0mm-2C','管内'); e16  = q('ケーブル','EM-EEF 1.6mm-2C','管内')
dvsp = q('電線','DV-2R 2個より 2.0mm 径間取付け費','引込用')
mccb = q('配線用遮断器','MCCB 2P 50A RC：5kA')
bant = q('引込開閉器盤','MCCB 3P 50AF 30A×1 屋根なし')     # 屋外盤の取付手間の参考
lamp = q('LED屋外灯 防犯灯','LBF2RP-10 LN 一般形')          # 屋外器具の取付手間の参考
pnt19= q('塗装工事','電線管 C19・E19');       pnt25= q('塗装工事','電線管 C25・E25')
kous = q('高所作業車','トラック架装・伸縮ブーム（作業高9.7m）バスケット型 積載荷重200kg 運転機械経費')

CP_L, HIVE_L = 3.66, 4.0        # 定尺（薄鋼電線管3.66m／HIVE4m）
DV_SPAN = 2                      # DV2.0-2C の径間数（図面：門形2基それぞれに引き下ろし）

rows=[]; labor=0.0
def it(name, spec, qty, unit, price, note="", t=0.0):
    global labor
    labor += qty*t; price=int(round(price))
    rows.append({"name":name,"spec":spec,"qty":qty,"unit":unit,"price":price,"note":note})
    return qty*price
def r100(x): return int(round(x/100.0))*100

C = "複合単価の材料費"
s=0
s+=it("鋼製電線管","CP19",10,"本", M(cp19)*CP_L, f"{C} 電線管CP-19 露出 {M(cp19)}円/m×3.66m(定尺)", t=T(cp19)*CP_L)
s+=it("鋼製電線管","CP25",4,"本",  M(cp25)*CP_L, f"{C} 電線管CP-25 露出 {M(cp25)}円/m×3.66m(定尺)", t=T(cp25)*CP_L)
s+=it("金属製可とう電線管（防水）","#17",6,"m", M(f17), f"{C} 二種金属製可とう電線管(F2)17 ビニル被覆", t=T(f17))
s+=it("硬質ビニル電線管","HIVE16",6,"本", M(hive)*HIVE_L, f"{C} 電線管HIVE16 露出 {M(hive)}円/m×4m(定尺)", t=T(hive)*HIVE_L)
PIPE = M(cp19)*CP_L*10 + M(cp25)*CP_L*4 + M(f17)*6 + M(hive)*HIVE_L*6
s+=it("同上付属品","支持材共",1,"式", r100(PIPE*0.20),
      "配管材料費の20%（カップリング・ノーマルベンド・エントランスキャップ・サドル等）")
s+=it("ビニルアウトボックス","4×54",5,"個", M(obox),
      f"{C} アウトレットボックス四角中深102×102×54。VE(樹脂)製は同項目で代用", t=T(obox))
s+=it("プルボックス（SUS被せ蓋）","200×200×200",3,"個", M(pbox),
      f"{C} プルボックスSS200×200×200 WP-SUS", t=T(pbox))
s+=it("電線ケーブル","EM-EEF2.0-2C",45,"m", M(e20), f"{C} ケーブルEM-EEF2.0mm-2C 管内", t=T(e20))
s+=it("電線ケーブル","EM-EEF1.6-2C",25,"m", M(e16), f"{C} ケーブルEM-EEF1.6mm-2C 管内", t=T(e16))
s+=it("電線ケーブル","DV2.0-2C",15,"m", 120,
      "材料費の推定（DV電線のm単価は複合単価DB未収録）。架設手間は径間取付け費で電工費に計上。要確認")
labor += dvsp['labor_cost']+dvsp['expense']   # DV 径間取付け費（2径間）
labor += (dvsp['labor_cost']+dvsp['expense'])*(DV_SPAN-1)
s+=it("引き込み支持材料","碍子含む",1,"式",15000,
      "引留クランプ・碍子・支持金具。複合単価DB未収録につき推定。要確認")
s+=it("タイマー制御盤","SUS製",1,"面",150000,
      "屋外SUS・キーハンドル付。タイムスイッチTB261201N(定価25,400円)＋ELB2P20A＋SUS屋外盤＋組立配線の推定。盤メーカー見積要",
      t=T(bant))
s+=it("配線用遮断器","2P50AF/20AT",1,"組", M(mccb), f"{C} 配線用遮断器MCCB 2P50A RC:5kA", t=T(mccb))
s+=it("同上取付改造費","",1,"式",30000,
      "既設融雪制御盤の一次側へ分岐用ブレーカーを増設。材工共の推定。停電時間帯は監督職員と協議。要確認")
s+=it("回転灯（100φ）","SF10-M2JN-Y（相当品）",2,"台",25000,
      "パトライトは定価非公表。実売相場(22,880円〜)を踏まえた材料費の推定。要確認", t=T(lamp))
s+=it("同上取付支持金具","SZK103（相当品）",2,"個",7000,
      "パトライト 壁面取付ブラケット。定価非公表につき推定。要確認")
MAT = s
s+=it("消耗品材料費","",1,"式", r100(MAT*0.03), "材料費計の3%")
s+=it("電工費","",1,"式", r100(labor),
      f"複合単価の取付手間(労務費＋経費)の積上げ＋DV径間取付け費{DV_SPAN}径間分")
s+=it("高所作業車損料","",1,"式", kous['composite_price']*2,
      f"{kous['composite_price']:,}円/日×2日。高架下GL+4.2mの鉄骨上部への回転灯・配管取付用")
PAINT = pnt19['composite_price']*CP_L*10 + pnt25['composite_price']*CP_L*4
s+=it("塗装費","露出配管",1,"式", r100(PAINT),
      f"材工共。塗装工事 電線管C19・E19 {pnt19['composite_price']}円/m×36.6m＋C25・E25 {pnt25['composite_price']}円/m×14.6m")

data={"header":{"name":"岐阜市中央卸売市場北側高架衝突防止設置工事　電気工事",
                "client":"岐阜市中央卸売市場","honorific":"御中","date":"2026-08-27","staff":"河口"},
      "place":"岐阜市茜部新所2丁目5番地　岐阜市中央卸売市場","remarks":"",
      "taxMode":"out","taxRate":10,"rows":rows}

net=sum(r['qty']*r['price'] for r in rows)
assert net==s, (net,s)
for r in rows: print(f"  {r['name'][:16]:16} {r['spec'][:18]:18} {r['qty']:>5}{r['unit']:2} {r['price']:>9,} {r['qty']*r['price']:>10,.0f}")
print("-"*70)
print(f"  電気工事 直接工事費（税抜・経費別） {net:>12,.0f}")
print(f"  参考: 税込 {net*1.1:>12,.0f}")
print("  明細",len(rows),"件")

out='/home/user/kd-mitsumori/見積/見積_岐阜市中央卸売市場_高架衝突防止_電気工事.json'
open(out,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=1))
b64=base64.urlsafe_b64encode(json.dumps(data,ensure_ascii=False,separators=(",",":")).encode()).decode().rstrip("=")
url="https://kawaguchidenki001.github.io/kd-mitsumori/#import="+b64
open('/home/user/kd-mitsumori/見積/取込リンク_岐阜市中央卸売市場.txt','w').write(url)
assert json.loads(base64.urlsafe_b64decode(b64+"=="*2).decode())==data
print("  URL長",len(url),"round-trip OK")
