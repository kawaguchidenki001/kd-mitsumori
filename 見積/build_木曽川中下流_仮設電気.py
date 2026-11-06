# -*- coding: utf-8 -*-
"""木曽川中下流用水総合管理所防水改修工事　仮設電気工事（株式会社渡辺組 御中）R8.11.6
   R8.11.6 Kの指示：空調電源取外し・再取付工事（No.261025）から仮設を分けた見積。仮設 85,000（本工事は 200,000）。
   仮設電気工事（撤去含む）1式 85,000、漏電遮断器 3P2E30A・幹線配線 CV5.5-3C は項目のみ。諸経費の行なし。
   見積No は新規（空欄＝アプリが採番）。
"""
import json, base64

rows = []
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note})
    return qty * int(price)
def ref(name):                                   # 項目のみ（数量・金額なし）
    rows.append({"name": name, "spec": "", "qty": "", "unit": "", "price": 0, "note": "", "ref": True})

s = 0
s += it("仮設電気工事", "撤去含む", 1, "式", 85_000, "Kの指示")
ref("　漏電遮断器　3P2E30A")
ref("　幹線配線　CV5.5-3C")

data = {"header": {"name": "木曽川中下流用水総合管理所防水改修工事　仮設電気工事", "client": "株式会社渡辺組", "honorific": "御中",
                   "date": "2026-11-06", "staff": "河口", "no": ""},
        "place": "愛知県稲沢市祖父江町馬飼寺東26-1", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_木曽川中下流_仮設電気.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/kisogawa-kasetsu.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_木曽川中下流_仮設電気.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=kisogawa-kasetsu\n")
for r in rows:
    print("  " + r["name"] + ("" if r.get("ref") else f" {r['spec']} {r['qty']}{r['unit']} {r['price']:,}"))
print(f"計（税抜）{s:,}")
