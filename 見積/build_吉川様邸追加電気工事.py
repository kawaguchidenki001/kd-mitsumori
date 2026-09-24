# -*- coding: utf-8 -*-
"""吉川様邸追加電気工事（有限会社廣瀬工務店 御中）　明細はKの指示どおり"""
import json, base64

rows = [
    {"name": "材料費", "spec": "", "qty": 1, "unit": "式", "price": 12000, "note": ""},
]
# 材料費の中身（説明だけの行。数量・単位・金額は空欄で合計に入れない ref 行）
for t in ["モール本体、部材 1式", "片切スイッチ、スイッチボックス、引掛シーリング",
          "防水コンセント（スマートタイプ）", "ケーブルVVF1.6-2C、3C"]:
    rows.append({"name": t, "spec": "", "qty": "", "unit": "", "price": 0, "ref": True, "note": "材料費の内訳"})
rows += [
    {"name": "電工費", "spec": "", "qty": 1, "unit": "式", "price": 25000, "note": ""},
    {"name": "諸経費", "spec": "", "qty": 1, "unit": "式", "price": 4000, "note": ""},
    {"name": "小　　計", "spec": "", "qty": 0, "unit": "", "price": 0, "sum": True},
]
data = {"header": {"name": "吉川様邸追加電気工事", "client": "有限会社廣瀬工務店", "honorific": "御中",
                   "date": "2026-09-24", "staff": "河口", "no": "260923"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "",
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_吉川様邸追加電気工事.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/yoshikawa-tsuika.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_吉川様邸追加電気工事.txt", "w").write(url + "\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=yoshikawa-tsuika\n")
s = sum(r["qty"] * r["price"] for r in rows if not r.get("ref") and not r.get("sum"))
print(f"計（税抜） {s:,} ／ 消費税 {s//10:,} ／ 税込 {s + s//10:,}")
