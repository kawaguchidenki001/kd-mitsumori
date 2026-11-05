# -*- coding: utf-8 -*-
"""忠節マンション引掛シーリング取付（株式会社廣瀬住建 御中）R8.11.5
   Kの指示：引掛けシーリング取付 5,000、既設照明器具処分 1,500、諸経費 500（計 7,000）。用紙1枚。見積No は新規（空欄）。
"""
import json, base64

rows = []
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note})
    return qty * int(price)

s = 0
s += it("引掛けシーリング取付", "", 1, "式", 5_000)
s += it("既設照明器具処分", "", 1, "式", 1_500)
s += it("諸経費", "", 1, "式", 500)

data = {"header": {"name": "忠節マンション引掛シーリング取付", "client": "株式会社廣瀬住建", "honorific": "御中",
                   "date": "2026-11-05", "staff": "河口", "no": ""},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_廣瀬住建_忠節マンション_引掛シーリング.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/chusetsu-ceiling.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_廣瀬住建_忠節マンション_引掛シーリング.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=chusetsu-ceiling\n")
for r in rows: print(f"  {r['name']:<16}{r['qty']:>2}{r['unit']}{r['price']:>8,}")
print(f"計（税抜）{s:,}")
