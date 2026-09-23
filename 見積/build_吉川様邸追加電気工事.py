# -*- coding: utf-8 -*-
"""吉川様邸追加電気工事（有限会社廣瀬工務店 御中）　明細はKの指示どおり"""
import json, base64

rows = [
    {"name": "材料費", "spec": "", "qty": 1, "unit": "式", "price": 6000, "note": ""},
    {"name": "電工費", "spec": "", "qty": 1, "unit": "式", "price": 25000, "note": ""},
    {"name": "諸経費", "spec": "", "qty": 1, "unit": "式", "price": 3000, "note": ""},
]
data = {"header": {"name": "吉川様邸追加電気工事", "client": "有限会社廣瀬工務店", "honorific": "御中",
                   "date": "2026-09-23", "staff": "河口", "no": "260923"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "",
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_吉川様邸追加電気工事.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/yoshikawa-tsuika.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_吉川様邸追加電気工事.txt", "w").write(url + "\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=yoshikawa-tsuika\n")
s = sum(r["qty"] * r["price"] for r in rows)
print(f"計（税抜） {s:,} ／ 消費税 {s//10:,} ／ 税込 {s + s//10:,}")
