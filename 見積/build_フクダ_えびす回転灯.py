# -*- coding: utf-8 -*-
"""株式会社フクダ　えびす回転灯取替工事
   パトライト SKP-M2-Y（LED回転灯 φ150 AC100V 黄）1台取替。定価26,500（パトライト公表価格）×0.65。
   高所作業車使用・撤去品処分費含む（Kの指示）。高所作業車はKの標準 1式60,000。
"""
import json, base64, math
def jsround(x): return math.floor(x + 0.5)
def sig(v):
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(pl)
    rows.append(r); return qty * int(price)

sub = 0
cat("01　回転灯取替工事")
sub += it("ＬＥＤ回転灯", "パトライト ＳＫＰ－Ｍ２－Ｙ", 1, "台", sig(26_500 * 0.65))
sub += it("回転灯取替費", "既設撤去・取付・結線・動作確認", 1, "台", 30_000, 30_000)
sub += it("高所作業車", "", 1, "式", 60_000)
sub += it("撤去品処分費", "既設回転灯", 1, "式", 5_000)
sub += it("雑材消耗品", "", 1, "式", 3_000)

cat("経　費")
labor = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
WELFARE, KEIHI = 16.5, 10.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
k_raw = jsround(sub * KEIHI / 100)
TARGET = (sub + w_amt + k_raw) // 1000 * 1000
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": (TARGET - sub - w_amt) - k_raw})

data = {"header": {"name": "えびす回転灯取替工事", "client": "株式会社フクダ", "honorific": "御中",
                   "date": "2026-10-02", "staff": "河口", "no": "261004"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_フクダ_えびす回転灯.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/fukuda-kaitentou.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in rows:
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:28]:30}{r['qty']:>2}{r['unit']:<2}{r['price']:>8,}")
tax = jsround(TARGET * 0.1)
print(f"小計 {sub:,}／法定福利費 {w_amt:,}／諸経費 {TARGET-sub-w_amt:,}／計（税抜）{TARGET:,}／税込 {TARGET+tax:,}")
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_フクダ_えびす回転灯.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=fukuda-kaitentou\n")
