# -*- coding: utf-8 -*-
"""足近保育園駐車場照明 LED投光器取替工事（大興建設株式会社 御中）R8.11.11
   元：R1.10.30 No.191018「足近保育園駐車場照明設置工事」（LED投光器取付 100W×4台 ほか、計 567,000）。
   Kの指示：7年前に付けた LED の取替、宛先・現場は同じ、LED 1台取替、LED は材工 33,000。法定福利費はなし。
   R8.11.11 Kの指示：高所作業車費 15,000・撤去品処分費 1,000 を追加。
   諸経費は元の見積の雑費（約1割）にならって 3,000（Kの指示なし。不要なら削除）。見積No は新規（空欄）。
"""
import json, base64

rows = []
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note})
    return qty * int(price)

s = 0
s += it("LED投光器取替", "100W　既設撤去共", 1, "台", 33_000, "材工共（Kの指示）")
s += it("高所作業車費", "", 1, "日", 15_000, "Kの指示（R8.11.11）")
s += it("撤去品処分費", "既設投光器", 1, "式", 1_000, "Kの指示（R8.11.11）")
s += it("諸経費", "", 1, "式", 3_000, "元の見積の雑費にならって約1割")

data = {"header": {"name": "足近保育園駐車場照明　LED投光器取替工事", "client": "大興建設株式会社", "honorific": "御中",
                   "date": "2026-11-11", "staff": "河口", "no": ""},
        "place": "足近保育園", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_大興建設_足近保育園_LED投光器取替.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/ajika-led-torikae.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_大興建設_足近保育園_LED投光器取替.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=ajika-led-torikae\n")
for r in rows: print(f"  {r['name']} {r['spec']} {r['qty']}{r['unit']} {r['price']:,}")
print(f"計（税抜）{s:,}")
