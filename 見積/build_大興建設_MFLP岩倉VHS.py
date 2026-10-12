# -*- coding: utf-8 -*-
"""大興建設株式会社　MFLP岩倉VHS取替工事（R8.10.7）
   Kの指示（LINE）：VHS300×300 サランフィルター付（定価48,600）材工22,000×10箇所、雑費25,000、合計245,000（税抜）。
   諸経費・法定福利費なし。用紙1枚（分類行なし）。替フィルターは金額未定のため計上しない。
"""
import json, base64
rows = [
    {"name": "ガラリ取替", "spec": "ＶＨＳ３００×３００ サランフィルター付", "qty": 10, "unit": "箇所", "price": 22_000, "note": ""},
    {"name": "雑費", "spec": "", "qty": 1, "unit": "式", "price": 25_000, "note": ""},
]
data = {"header": {"name": "MFLP岩倉VHS取替工事", "client": "大興建設株式会社", "honorific": "御中",
                   "date": "2026-10-07", "staff": "河口", "no": "261006"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": ["追加の替えフィルターは1枚2,500円（NET）です。"],   # Kの指示
        "taxMode": "ex", "taxRate": 10, "rows": rows}
assert sum(r["qty"] * r["price"] for r in rows) == 245_000
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_大興建設_MFLP岩倉VHS.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/mflp-iwakura-vhs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_大興建設_MFLP岩倉VHS.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=mflp-iwakura-vhs\n")
print("ok")
