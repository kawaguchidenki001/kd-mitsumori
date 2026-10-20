# -*- coding: utf-8 -*-
"""岐阜ベルト外部追加工事（永井建設株式会社 御中）R8.10.20
   Kの指示：外部追加工事 1式 100,000円、諸経費 10,000円、合計 110,000円。
   添付のメモ（岐阜ベルト 外部追加）の内容を、その下に内訳として書く（金額欄は空欄・合計に入れない ref 行）。用紙1枚（分類行なし）。
   メモ下の図（AC・CVT14sq・リモコン配線×2）は×で消してあるので書かない。
   見積Noは新規（Drive・アプリに同じ工事名の見積なし）→ 空欄（アプリが採番）。
"""
import json, base64

UCHIWAKE = [
    "インターホン　配管配線・取付",
    "電気錠　配管配線・取付（電線支給）",
    "ポール照明　3台取付",
    "スパイク照明　1台取付",
    "ポール照明　EEスイッチ取付",
    "ゲート電源　配管配線・接続",
    "自販機電源",
]
rows = [{"name": "外部追加工事", "spec": "", "qty": 1, "unit": "式", "price": 100_000, "note": ""}]
for t in UCHIWAKE:
    rows.append({"name": "・" + t, "spec": "", "qty": "", "unit": "", "price": 0, "ref": True, "note": "外部追加工事の内訳"})
rows.append({"name": "諸経費", "rate": 10.0, "adj": 0})   # 100,000×10%＝10,000（Kの指示）

data = {"header": {"name": "岐阜ベルト外部追加工事", "client": "永井建設株式会社", "honorific": "御中",
                   "date": "2026-10-20", "staff": "河口", "no": ""},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_永井建設_岐阜ベルト外部追加.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/gifu-belt-gaibu.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_永井建設_岐阜ベルト外部追加.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=gifu-belt-gaibu\n")
for r in rows: print(r)
print("小計 100,000／諸経費 10,000／計（税抜）110,000")
