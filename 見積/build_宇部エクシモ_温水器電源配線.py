# -*- coding: utf-8 -*-
"""宇部エクシモ温水器電源配線工事（戸島工業株式会社 御中）
   単価は公共建築工事の複合単価（材料費＋労務費＋経費）。
   複合単価データに無いもの（メタルモールA型・コーナーボックス・ELB2P1E20A・器具脱着）は
   材料実勢＋手間からの推定で、note に★を付けた。
"""
import json, base64, math, os

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    n = 3 if v >= 1000 else 2 if v >= 100 else 1 if v >= 10 else 0
    if n == 0: return int(math.ceil(v))
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - n)
    return int(math.ceil(round(v / step, 9))) * step

rows = []
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return qty * int(price)

s = 0
s += it("ケーブル配線", "VVF2.0mm-3C 管内", 15, "m", 1_150, 592, "複合単価")
s += it("電線管", "EP-25 露出", 2, "m", 3_370, 1_889, "複合単価")
s += it("メタルモール", "A型", 2.5, "m", sig(350 + 1_410 + 680), 1_410, "★材料350＋手間（線ぴ相当）")
s += it("コーナーボックス", "A型用", 1, "個", sig(250 + 1_400), 1_100, "★材料250＋手間")
s += it("スイッチボックス", "1個用 深形", 1, "個", 5_150, 2_820, "複合単価")
s += it("埋込形コンセント", "1ET 接地端子付 新金属プレート共", 1, "個", 3_600, 1_889, "複合単価（大角形 金属製プレート共）")
s += it("分電盤改修", "ELB2P1E20A 1個増設", 1, "個", sig(4_500 + 7_445 + 3_499), 7_445, "★材料4,500＋盤加工・母線接続手間")
s += it("照明器具 脱着", "下面開放40W×2", 2, "台", 7_000, 5_000, "★取外し・再取付")
ZATSU = 73_000 - int(round(s))                                   # 小計を1,000円単位に調整
s += it("雑費", "", 1, "式", ZATSU, 0, "消耗雑材費。小計調整")

KEIHI = 10.0
labor = sum(r["qty"] * r.get("pl", 0) for r in rows)
s = int(round(s))
k_raw = jsround(s * KEIHI / 100)
TARGET = (s + k_raw) // 1000 * 1000                  # 計（税抜）を1,000円単位（切捨て）
rows.append({"name": "諸経費", "rate": KEIHI, "adj": (TARGET - s) - k_raw})

data = {"header": {"name": "宇部エクシモ温水器電源配線工事", "client": "戸島工業株式会社", "honorific": "御中",
                   "date": "2026-09-12", "staff": "河口", "no": "260912"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "",
        "taxMode": "out", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_宇部エクシモ_温水器電源配線工事.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:34]:36}{r['qty']:>5}{r['unit']:<3}{r['price']:>8,}{round(r['qty']*r['price']):>9,}")
tax = jsround(TARGET * 0.1)
print(f"\n{'小　計（純工事費）':20}{s:>9,}\n{'諸経費':20}{TARGET-s:>9,}   （純工事費×{KEIHI}%＋端数調整）")
print(f"{'計（税抜）':20}{TARGET:>9,}\n{'消費税10%':20}{tax:>9,}\n{'合　計':20}{TARGET+tax:>9,}")
assert TARGET % 1000 == 0 and s == 73_000
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
json.dump(data, open(root + "/q/ube-exsymo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(root + "/見積/取込リンク_宇部エクシモ_温水器電源配線.txt", "w").write(url + "\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=ube-exsymo\n")
print("URL長", len(url))
