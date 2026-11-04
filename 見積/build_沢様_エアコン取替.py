# -*- coding: utf-8 -*-
"""エアコン取付工事（某所 御中。当初は 沢 博昭 様）R8.11.4
   元：R8.6.30 No.260302「エアコン取替ほか工事」（ルームエアコン取付 2.2kW 6帖用×3台、冷媒配管等延長 3,600/m ほか、
       諸経費 43,500＝小計の10%）。
   Kの指示：エアコン 8畳用 1台取り替え 76,000、配管延長 2m、諸経費 1式。
   配管延長の単価は元の見積と同じ 3,600/m（2分3分・連絡線）。諸経費は元と同じ 10%、計を1,000円単位に（諸経費の adj）。
   税込表示（元の見積と同じく消費税・合計を出す）。
   R8.11.4 Kの指示：宛名は「某所」、工事名は「エアコン取付工事」。税込 100,000 ちょうど（値引きで調整）。見積No は新規（空欄＝アプリが採番）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)

rows = []
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note})
    return qty * int(price)

s = 0
s += it("ルームエアコン取替", "2.5kW　8帖用", 1, "台", 76_000, "Kの指示")
s += it("冷媒配管等延長", "2分3分、連絡線", 2, "ｍ", 3_600, "R8.6.30 No.260302 と同じ単価")

# R8.11.4 Kの指示：税込 100,000 ちょうどに → 元の見積と同じく 諸経費 1式＋値引きで 計（税抜）90,909・消費税 9,091
KEIHI = 10.0
SHOKEI = int(round(s * KEIHI / 100, -2))                   # 8,320 → 8,300
s += it("諸経費", "", 1, "式", SHOKEI)
TOTAL = 90_909                                        # 90,909＋消費税 9,091＝100,000
assert TOTAL + jsround(TOTAL * 0.1) == 100_000
NEBIKI = TOTAL - s
s += it("値引き", "", 1, "式", NEBIKI)
assert s == TOTAL

data = {"header": {"name": "エアコン取付工事", "client": "某所", "honorific": "御中",
                   "date": "2026-11-04", "staff": "河口", "no": ""},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "in", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_沢様_エアコン取替.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/sawa-ac.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_沢様_エアコン取替.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=sawa-ac\n")
for r in rows:
    if "qty" in r: print(f"  {r['name']} {r['spec']:<16}{r['qty']:>3}{r['unit']}{r['price']:>8,}{r['qty']*r['price']:>9,}  {r['note']}")
print(f"諸経費 {SHOKEI:,}／値引き {NEBIKI:,}／計（税抜）{TOTAL:,}／消費税 {jsround(TOTAL*0.1):,}／税込 {TOTAL + jsround(TOTAL*0.1):,}")
