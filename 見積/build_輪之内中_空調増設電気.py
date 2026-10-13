# -*- coding: utf-8 -*-
"""輪之内中学校空調増設電気工事（戸島工業株式会社 御中）（R8.10.13）
   内訳は K の指示どおり。品名・仕様は tankatool（電気設備工事積算実務マニュアル2026 岐阜県）の表記に合わせる。
   単価は同マニュアルの複合単価。tankatool に無いもの（ステンレス電線管・125A ブレーカ・付属品・支持材）は★概算。
   用紙1枚（分類行なし）。法定福利費16.5%（100円単位）、諸経費12%で計を1,000円単位に端数調整（雑費・雑材の行が無いため）。
   見積Noは新規なので空欄（Kがアプリで保存するときに採番される）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - 3)
    if step < 10: step = 10
    n = int(math.floor(v / step + 0.5))
    return (n if n >= 1 else 1) * step

rows = []
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return int(round(qty * int(price)))

# ★ステンレス電線管 C31 露出：tankatool に無い。CP-31 露出（材料467・労務3,017・経費率40.5%）を元に、
#   材料をステンレス実勢 約3,000円/m（鋼製の約6倍）、労務を1.2倍（切断・ねじ切りが硬い）にして積み上げ。付属品は別行。
SUS_MAT, SUS_LAB = 3_000 * 1.1, 3_017 * 1.2
SUS31 = sig((SUS_MAT + SUS_LAB) * (1 + 1_491 / (662 + 3_017)))
# ★MCCB 3P 125A：tankatool は 3P100A（44,900・撤去5,890）と 3P225A（69,800・撤去8,620）。電流比で按分（取付＋撤去）
k125 = 25 / 125
MCCB125 = sig(44_900 + (69_800 - 44_900) * k125 + 5_890 + (8_620 - 5_890) * k125)
MCCB125_PL = 19_966 + (29_328 - 19_966) * k125 + 5_890 + (8_620 - 5_890) * k125
# リモコン配線 1箇所：EM-CEE 1.25mm2-2C 管内 810×4m＋1種金属線ぴ(MM1) A型 定尺 3,680×2m＋スイッチボックス 2個用 浅形 5,380
REMO = sig(810 * 4 + 3_680 * 2 + 5_380)
REMO_PL = 423 * 4 + 1_974 * 2 + 2_820

UP = 1.1                                   # 全体の単価を1.1倍（Kの指示 R8.10.13）。労務費 pl は据え置き
def P(v): return sig(v * UP)

s = 0
s += it("ケーブル", "ＥＭ－ＣＥＴ ６０ｍｍ２ 管内", 50, "ｍ", P(9_040), 2_312)
s += it("ケーブル", "ＥＭ－ＣＥＴ １４ｍｍ２ 管内", 20, "ｍ", P(3_080), 1_043)
s += it("電線管", "ＳＵＳ Ｃ３１ 露出", 18, "ｍ", P(SUS31), SUS_LAB, "★ステンレス：CP-31露出を元に材料・労務を置換")
conduit = 18 * P(SUS31)                    # 付属品・支持材は1.1倍後の電線管の10%（二重に掛けない）
s += it("電線管付属品", "", 1, "式", sig(conduit * 0.10), 0, "★電線管の10%（R7.6.10 No.250541 の比率）")
s += it("電線管支持材", "", 1, "式", sig(conduit * 0.10), sig(conduit * 0.05), "★電線管の10%")
s += it("配線用遮断器", "ＭＣＣＢ ３Ｐ３Ｅ １２５Ａ 取替（分電盤改修）", 2, "個", P(MCCB125), MCCB125_PL, "★100Aと225Aの按分（取付＋撤去）。分電盤2面で各1個")
s += it("漏電遮断器", "ＥＬＣＢ ３Ｐ ５０Ａ 増設（分電盤改修）", 1, "個", P(38_900), 15_736, "EMB3-3E50A")
s += it("リモコン配線", "１種金属線ぴ（ＭＭ１）Ａ型共", 2, "箇所", P(810 * 4 + 3_680 * 2 + 5_380), REMO_PL,
        "EM-CEE1.25-2C 810×4＋MM1 A型 3,680×2＋SB2個用 5,380")
s += it("ケーブル撤去", "６００Ｖ ＣＶＴ ３８ｍｍ２ 管内", 50, "ｍ", P(510), 347, "撤去費（管内）")

labor = sum(r["qty"] * r.get("pl", 0) for r in rows)
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
k_raw = jsround(s * KEIHI / 100)
TARGET = (s + w_amt + k_raw + 500) // 1000 * 1000
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": (TARGET - s - w_amt) - k_raw})

data = {"header": {"name": "輪之内中学校空調増設電気工事", "client": "戸島工業株式会社", "honorific": "御中",
                   "date": "2026-10-13", "staff": "河口", "no": "261017"},   # Kがアプリで保存したNo（Drive の 輪之内中学校空調増設電気工事_見積書_R8.10.13.xlsx）。仕様もKの修正に合わせた
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_輪之内中_空調増設電気.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/wanouchi-chu.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_輪之内中_空調増設電気.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=wanouchi-chu\n")

for r in rows:
    if "qty" in r:
        print(f"  {(r['name']+' '+r['spec'])[:40]:42}{r['qty']:>4}{r['unit']:<3}{r['price']:>9,}{int(round(r['qty']*r['price'])):>10,} {r['note']}")
print(f"小計 {s:,}／法定福利費 {w_amt:,}（労務費{labor:,.0f}）／諸経費 {TARGET - s - w_amt:,}（12%={k_raw:,}）／計（税抜）{TARGET:,}／税込 {TARGET + jsround(TARGET*0.1):,}")
