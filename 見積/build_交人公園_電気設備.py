# -*- coding: utf-8 -*-
"""交人公園整備工事　電気設備工事（永井建設株式会社 御中）
   発注者：岐阜市都市建設部公園整備課／設計書（令和8年度・入札用＝単価空欄）より拾い出し。

   数量の根拠（設計書 内訳表 6〜7頁／電気設備工構造図(1)(2) 図面番号12・13）
     電気設備工 － 照明設備工   照明灯 LED 水銀灯250W相当 …………… 4 基（単価表 SJ0070）
                                引込柱・分電盤 ………………………… 1 基（単価表 SJ0072）
                － 電線管路工   電線管 FEP30 …………………………… 162 m（単価表 SJ0080）
                                電線 EM-CE3.5□-2C …………………… 162 m（単価表 SJ0082）
     公園施設等撤去工            照明灯撤去 ……………………………… 4 基（単価表 SJ0520）

   単価は設計書の単価表の構成に合わせ、電気設備工事積算実務マニュアル2026（岐阜県）の
   複合単価を積み上げたもの。★は同マニュアルに登録が無く材料実勢から積み上げた項目。
   掘削・埋戻し（作業土工）は設計書上「基盤整備」に別計上されているため本見積に含めない。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    """単価の丸め：四捨五入で上3桁、最小単位は10円（1円単位は出さない）"""
    v = float(v)
    if v <= 0: return 0
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - 3)
    if step < 10: step = 10
    n = int(math.floor(v / step + 0.5))
    return (n if n >= 1 else 1) * step

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return qty * int(price)

# ---- 照明灯 1基当りの積上げ（設計書 単価表 SJ0070 の構成）--------------------
POLE_P,  POLE_T  = 236_000, 51_888   # LED屋外灯 ポール灯 LST2-60 LN（灯具・照明柱・建柱共）
BASE_P,  BASE_T  =  65_200,  5_080   # 屋外灯基礎 400×400×1100 現場打ち(機械)＝φ500×900 0.18m3相当
AUTO_P,  AUTO_T  =  14_400,  4_597   # 自動点滅器 電子式(JIS2形)100V 3A ポール直付ニップル式 受台付
ED_P,    ED_T    =   9_880,  5_161   # 接地材 D種（打込式接地棒 10φ×1500）
LAMP_P = sig(POLE_P + BASE_P + AUTO_P + ED_P)
LAMP_T = POLE_T + BASE_T + AUTO_T + ED_T

# ---- 引込柱・分電盤 1基当りの積上げ（設計書 単価表 SJ0072 の構成）------------
HIKI_MAT, HIKI_LAB = 110_000, 45_000  # ★引込柱 H=6.3m 亜鉛めっき+ポリエチレン被覆／組立据付
BAN_MAT,  BAN_LAB  =  95_000, 18_000  # ★分電盤 300×900×193 ステンレス粉体塗装／取付
CE_P, CE_T = 1_090, 479               # 電線 EM-CE 3.5mm2-2C 管内
HB_P = jsround(BASE_P * 0.21 / 0.176) # 基礎 0.21m3（スパイラルダクトφ500 1.1m・基礎砕石0.36m2共）
HIKI_P = sig(HIKI_MAT + HIKI_LAB + BAN_MAT + BAN_LAB + CE_P * 3 + ED_P + HB_P)
HIKI_T = HIKI_LAB + BAN_LAB + CE_T * 3 + ED_T + BASE_T

# ---- 電線管 FEP30 1m当り（設計書 単価表 SJ0080 の構成）-----------------------
FEP_P, FEP_T   = 1_400, 733           # 波付硬質ポリエチレン管(FEP) 30 地中
SUNA_P, SUNA_T =   540, 200           # ★再生砂 0.09m3/m（埋戻し材相当）
SHEET_P, SHEET_T = 380, 113           # 埋設標識シート 幅150mm 2倍
KAN_P = sig(FEP_P + SUNA_P + SHEET_P)
KAN_T = FEP_T + SUNA_T + SHEET_T

# ---- 照明灯撤去 1基当り（設計書 単価表 SJ0520 の構成）------------------------
TEK_P = sig(22_900 + 3_720 + 1_240)   # ポール灯撤去22,900＋基礎とりこわし0.31m3＋殻運搬
TEK_T = 21_000

sub = 0
cat("01 照明設備工")
sub += it("照明灯", "LED　水銀灯250W相当", 4, "基", LAMP_P, LAMP_T,
          "灯具・照明柱H=5.3m・建柱・基礎・自動点滅器・接地D種共")
sub += it("引込柱・分電盤", "", 1, "基", HIKI_P, HIKI_T,
          "★引込柱H=6.3m・分電盤300×900×193・電線3m・接地D種・基礎共")

cat("02 電線管路工")
sub += it("電線管", "ＦＥＰ３０", 162, "m", KAN_P, KAN_T, "再生砂・埋設標識シートW=150 2倍共")
sub += it("電線", "ＥＭ－ＣＥ３.５□－２Ｃ", 162, "m", CE_P, CE_T, "管内配線")

_zat_at = len(rows)                       # 雑材消耗品を差し込む位置（電線管路工の末尾）

cat("03 公園施設等撤去工")
sub += it("照明灯撤去", "", 4, "基", TEK_P, TEK_T, "基礎とりこわし・殻運搬共")

ZATSU = sig(2_350_000 - int(round(sub)))
sub += ZATSU
rows.insert(_zat_at, {"name": "雑材消耗品", "spec": "", "qty": 1, "unit": "式",
                      "price": ZATSU, "note": "圧着端子・テープ・標識類ほか。小計調整"})

# ---- 集計 ------------------------------------------------------------------
cat("経　費")
labor = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
sub = int(round(sub))
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 1000 * 1000
k_raw = jsround(sub * KEIHI / 100)
TARGET = (sub + w_amt + k_raw) // 1000 * 1000
k_amt = TARGET - sub - w_amt
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費",     "rate": KEIHI,     "adj": k_amt - k_raw})

data = {"header": {"name": "交人公園整備工事　電気設備工事",
                   "client": "永井建設株式会社", "honorific": "御中",
                   "date": "2026-09-15", "staff": "河口", "no": "260915"},
        "place": "岐阜市大学北２丁目地内",
        "validity": "発行日より1ヶ月", "remarks": "",
        "taxMode": "ex", "taxRate": 10, "rows": rows}

root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_交人公園整備工事_電気設備工事.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/kojin-park.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    if r.get("type") == "cat": print("\n【" + r["name"] + "】"); continue
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:38]:40}{r['qty']:>6}{r['unit']:<3}{r['price']:>10,}{round(r['qty']*r['price']):>12,}")
tax = jsround(TARGET * 0.1)
print(f"\n{'小　計（純工事費）':22}{sub:>12,}")
print(f"{'法定福利費':22}{w_amt:>12,}   （労務費 {round(labor):,}×{WELFARE}%）")
print(f"{'諸経費':22}{k_amt:>12,}   （純工事費×{KEIHI}%＋端数調整）")
print(f"{'計（税抜）':22}{TARGET:>12,}\n{'消費税10%':22}{tax:>12,}\n{'合　計':22}{TARGET+tax:>12,}")
assert TARGET % 1000 == 0

payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_交人公園_電気設備.txt", "w").write(
    url + "\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=kojin-park\n")
print("URL長", len(url))
