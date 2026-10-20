# -*- coding: utf-8 -*-
"""岐阜ベルト人感センサー取付工事（永井建設株式会社 御中）R8.10.20
   Kの指示：人感センサー取付 壁 1階トイレ 1式 32,000／壁 2階洗面 1式 32,000／諸経費 1式 6,000（計 70,000）。
   用紙1枚（分類行なし）。法定福利費なし。見積Noは新規（Drive・アプリに同じ工事名の見積なし）→ 空欄（アプリが採番）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)

rows = [
    {"name": "人感センサー取付", "spec": "壁　1階トイレ", "qty": 1, "unit": "式", "price": 32_000, "note": ""},
    {"name": "人感センサー取付", "spec": "壁　2階洗面", "qty": 1, "unit": "式", "price": 32_000, "note": ""},
]
s = sum(r["qty"] * r["price"] for r in rows)
KEIHI, K_AMT = 10.0, 6_000                       # 諸経費は Kの指示で 6,000（10% との差は adj）
rows.append({"name": "諸経費", "rate": KEIHI, "adj": K_AMT - jsround(s * KEIHI / 100)})

data = {"header": {"name": "岐阜ベルト人感センサー取付工事", "client": "永井建設株式会社", "honorific": "御中",
                   "date": "2026-10-20", "staff": "河口", "no": ""},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_永井建設_岐阜ベルト人感センサー.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/gifu-belt-sensor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_永井建設_岐阜ベルト人感センサー.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=gifu-belt-sensor\n")
print(f"小計 {s:,}／諸経費 {K_AMT:,}／計（税抜）{s + K_AMT:,}")
