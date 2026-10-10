# -*- coding: utf-8 -*-
"""大興建設株式会社　岐阜機械商事新築電気設備工事　追加工事（R8.10.10）
   元見積：当社 No.250541（R7.6.10 岐阜機械商事新築電気設備工事 32,990,000）
   Kの指示：
     動力幹線 P-K（工作機械）2箇所：金額は CVT100sq 75m と FEP80 70m の合計（2箇所分の延長として計算）
     動力分岐 クレーン 2箇所 120,000／分電盤設置 P-K 2台 160,000
     コンセント配線 トイレ電気温水器 3箇所 16,000／コンセント配線 専用 1箇所 16,000（いずれも1箇所・1台あたり）
   単価：複合単価（電気設備工事積算実務マニュアル2026 岐阜県）。
         CVT100sq は材料費だけを実仕入の値上がり分（扇港電機 R8.9.30：CVT 約1.10倍）に置き換え、
         経費は（材料費＋労務費）の増えた割合だけ増やす（東興産業 No.261001 と同じ方法）。
   元見積に合わせて法定福利費なし、諸経費10%で1,000円単位に端数調整。用紙1枚（分類行なし）。
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

# CVT100sq FEP管内配線：(DB材料単価, 材料費, 労務費, 経費, 複合単価)
mat, mc, lab, exp, comp = 7_354, 8_108, 2_843, 2_228, 13_200
mc2 = mat * 1.10 * mc / mat
exp2 = exp * (mc2 + lab) / (mc + lab)
CVT100 = sig(mc2 + lab + exp2)          # 14,200
FEP80 = 2_530                           # FEP80 地中 複合単価（DB）
CVT_M, FEP_M, N = 75, 70, 2
kansen = CVT100 * CVT_M + FEP80 * FEP_M
KANSEN = sig(kansen / N)                # 1箇所あたり

rows = []
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return int(round(qty * int(price)))

sub = 0
sub += it("動力幹線　Ｐ－Ｋ（工作機械）", "ＣＶＴ１００sq・ＦＥＰ８０", N, "箇所", KANSEN, (lab * CVT_M + 1_269 * FEP_M) / N)
sub += it("動力分岐　クレーン", "", 2, "箇所", 120_000)
sub += it("分電盤設置　Ｐ－Ｋ", "", 2, "台", 160_000)
sub += it("コンセント配線　トイレ電気温水器", "", 3, "箇所", 16_000)
sub += it("コンセント配線　専用", "", 1, "箇所", 16_000)

KEIHI = 10.0
k_raw = jsround(sub * KEIHI / 100)
TARGET = (sub + k_raw + 500) // 1000 * 1000
rows.append({"name": "諸経費", "rate": KEIHI, "adj": (TARGET - sub) - k_raw})

data = {"header": {"name": "岐阜機械商事新築電気設備工事（追加工事）", "client": "大興建設株式会社", "honorific": "御中",
                   "date": "2026-10-10", "staff": "河口", "no": "261009"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_岐阜機械商事_追加工事.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/gifukikai-tsuika.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_岐阜機械商事_追加工事.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=gifukikai-tsuika\n")

for r in rows:
    if "qty" in r:
        print(f"  {r['name']} {r['spec']}  {r['qty']}{r['unit']}  {r['price']:>9,}  {int(round(r['qty']*r['price'])):>10,}")
print(f"動力幹線：CVT100sq {CVT100:,}×{CVT_M}m＋FEP80 {FEP80:,}×{FEP_M}m＝{kansen:,} → 1箇所 {KANSEN:,}")
print(f"小計 {sub:,}／諸経費 {TARGET - sub:,}（10%={k_raw:,}）／計（税抜）{TARGET:,}／税込 {TARGET + jsround(TARGET*0.1):,}")
