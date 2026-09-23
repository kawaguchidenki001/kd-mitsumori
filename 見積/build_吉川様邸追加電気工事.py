# -*- coding: utf-8 -*-
"""吉川様邸追加電気工事（有限会社廣瀬工務店 御中）　明細はKの指示どおり"""
import json, base64

rows = [
    {"name": "材料費", "spec": "", "qty": 1, "unit": "式", "price": 8000, "note": "Kの指示で6,000→8,000"},
]
# 主な材料（材料費の内訳。数量だけ出し、金額欄は空欄・合計に入れない ref 行）
MAT = [
    ("モール 出角", "白", 1, "個"), ("モール 入角", "白", 2, "個"), ("モール ノーマル", "白", 1, "個"),
    ("モール コンビネーション", "", 1, "個"), ("モール エンド", "白", 2, "個"),
    ("モール", "白", 1, "本"), ("モール", "茶", 2, "本"), ("モールボックス", "茶", 1, "個"),
    ("片切スイッチ", "ワイド", 1, "組"), ("引掛シーリング", "丸型", 1, "個"),
    ("スマート防水コンセント", "", 1, "個"),
    ("VAケーブル", "1.6×2C", 5, "m"), ("VAケーブル", "1.6×3C", 3, "m"),
]
rows += [{"name": n, "spec": sp, "qty": q, "unit": u, "price": 0, "ref": True, "note": "材料費の内訳"} for n, sp, q, u in MAT]
rows += [
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
