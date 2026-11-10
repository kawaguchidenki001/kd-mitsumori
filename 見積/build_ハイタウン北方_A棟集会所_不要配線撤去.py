# -*- coding: utf-8 -*-
"""ハイタウン北方 A棟集会所屋根不要配線撤去（岐阜県住宅供給公社 御中）
   内訳・金額はKのご指示どおり（不要配線撤去 1式 20,000円／諸経費 3,000円）。
   R8.11.10 Kの指示：工事名「Ａ棟集会所屋根不要配線撤去等」、工事費 1式 30,000（内容3行）、諸経費 3,000。
   公社あてのため自社住所は公共用（岐阜市柳津町下佐波2-96）、表示は税込。
"""
import json, math, base64

# R8.11.10 Kの指示：工事名を「Ａ棟集会所屋根不要配線撤去等」に、工事費 1式 30,000、その下に内容、諸経費 3,000
rows = [
    {"name": "工事費", "spec": "", "qty": 1, "unit": "式", "price": 30000, "note": "Kの指示"},
    {"name": "・不要線の撤去", "spec": "", "qty": "", "unit": "", "price": 0, "note": "", "ref": True},
    {"name": "・監理人室用（南側へ架空線）の緩み解消", "spec": "", "qty": "", "unit": "", "price": 0, "note": "", "ref": True},
    {"name": "・集会室（西側へ転がし）の一時撤去", "spec": "", "qty": "", "unit": "", "price": 0, "note": "", "ref": True},
    {"name": "諸経費", "rate": 10.0},          # 純工事費30,000×10％＝3,000（Kの指示 3,000）
]
sub = sum(r["qty"] * r["price"] for r in rows if "qty" in r and not r.get("ref"))
kei = math.floor(sub * 10.0 / 100 + 0.5)
pre = sub + kei
tax = math.floor(pre * 0.1 + 0.5)
f = lambda v: format(int(v), ",")
print("■ 明細")
for r in rows:
    if r.get("ref"): print("   " + r["name"])
    elif "qty" in r: print("   %-24s %3s %-3s %9s" % (r["name"], r["qty"], r["unit"], f(r["price"])))
print("   %-24s %22s" % ("小　計", f(sub)))
print("   %-24s %22s" % ("諸経費（純工事費×10％）", f(kei)))
print("   %-24s %22s" % ("計（税抜）", f(pre)))
print("   %-24s %22s" % ("消費税（10％）", f(tax)))
print("   %-24s %22s" % ("合　計（税込）", f(pre + tax)))
assert kei == 3000 and pre == 33000 and pre + tax == 36300

data = {"header": {"name": "Ａ棟集会所屋根不要配線撤去等",
                   "client": "岐阜県住宅供給公社", "client2": "理事長　崎浦　良典", "honorific": "様",
                   "date": "2026-11-10", "staff": "河口", "no": "261101"},
        "place": "ハイタウン北方", "validity": "発行日より1ヶ月", "remarks": "",
        "addrKind": "public",                 # 公共用住所（岐阜市柳津町下佐波2-96）で印刷
        "taxMode": "in", "taxRate": 10,       # 税込表示
        "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_ハイタウン北方_A棟集会所_不要配線撤去.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/hightown-kitagata-haisen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
u = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(
    json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_ハイタウン北方_A棟集会所.txt", "w").write(
    u + "\nhttps://kd-mitsumori.pages.dev/#q=hightown-kitagata-haisen\n")
print("   URL長", len(u))
