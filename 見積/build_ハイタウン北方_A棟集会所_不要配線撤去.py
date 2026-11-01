# -*- coding: utf-8 -*-
"""ハイタウン北方 A棟集会所屋根不要配線撤去（岐阜県住宅供給公社 御中）
   内訳・金額はKのご指示どおり（不要配線撤去 1式 20,000円／諸経費 3,000円）。
   公社あてのため自社住所は公共用（岐阜市柳津町下佐波2-96）、表示は税込。
"""
import json, math, base64

rows = [
    {"name": "不要配線撤去", "spec": "Ａ棟集会所屋根", "qty": 1, "unit": "式", "price": 20000, "note": ""},
    {"name": "諸経費", "rate": 15.0},          # 純工事費20,000×15％＝3,000
]
sub = sum(r["qty"] * r["price"] for r in rows if "qty" in r)
kei = math.floor(sub * 15.0 / 100 + 0.5)
pre = sub + kei
tax = math.floor(pre * 0.1 + 0.5)
f = lambda v: format(int(v), ",")
print("■ 明細")
print("   %-24s %3s %-3s %9s %10s" % ("不要配線撤去　Ａ棟集会所屋根", 1, "式", f(20000), f(20000)))
print("   %-24s %22s" % ("小　計", f(sub)))
print("   %-24s %22s" % ("諸経費（純工事費×15％）", f(kei)))
print("   %-24s %22s" % ("計（税抜）", f(pre)))
print("   %-24s %22s" % ("消費税（10％）", f(tax)))
print("   %-24s %22s" % ("合　計（税込）", f(pre + tax)))
assert kei == 3000 and pre == 23000 and pre + tax == 25300

data = {"header": {"name": "Ａ棟集会所屋根不要配線撤去",
                   "client": "岐阜県住宅供給公社", "honorific": "御中",
                   "date": "2026-11-01", "staff": "河口", "no": "261101"},
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
