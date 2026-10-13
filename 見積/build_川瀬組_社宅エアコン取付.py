# -*- coding: utf-8 -*-
"""株式会社川瀬組　社宅エアコン取付工事（No.261010）
   元の見積：R8.10.10 No.261010（計 239,000）の明細をそのまま写し、
   「既設エアコン撤去・処分 1台 15,000」を追加（Kの指示 R8.10.13）。
   元の見積どおり法定福利費なし、諸経費10%で計を1,000円単位に端数調整。用紙1枚（分類行なし）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)

rows = []
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note})
    return qty * int(price)

s = 0
s += it("エアコン取付工事", "５．６ｋＷ １８帖用", 1, "台", 159_000)
s += it("配管延長", "部材含む", 4, "ｍ", 4_800)
s += it("コンセント配線", "エアコン用 ２００Ｖ", 1, "ケ所", 25_000)
s += it("窓用アルミパネル取付", "", 1, "ケ所", 14_500)
s += it("既設エアコン撤去・処分", "", 1, "台", 15_000, "追加（Kの指示 R8.10.13）")

KEIHI = 10.0
k_raw = jsround(s * KEIHI / 100)
TARGET = (s + k_raw + 500) // 1000 * 1000
rows.append({"name": "諸経費", "rate": KEIHI, "adj": (TARGET - s) - k_raw})

data = {"header": {"name": "社宅エアコン取付工事", "client": "株式会社川瀬組", "honorific": "御中",
                   "date": "2026-10-13", "staff": "河口", "no": "261010"},   # 元の見積No。見積日は作り直した日
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_川瀬組_社宅エアコン取付.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/shataku-aircon.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_川瀬組_社宅エアコン取付.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=shataku-aircon\n")

for r in rows:
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:30]:32}{r['qty']:>3}{r['unit']:<3}{r['price']:>9,}{r['qty']*r['price']:>10,}")
print(f"小計 {s:,}／諸経費 {TARGET - s:,}（10%={k_raw:,}）／計（税抜）{TARGET:,}／税込 {TARGET + jsround(TARGET*0.1):,}")
