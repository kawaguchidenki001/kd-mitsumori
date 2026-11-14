# -*- coding: utf-8 -*-
"""換気設備 有圧換気扇更新工事（戸島工業株式会社 御中）エフピコ 換気扇33台取替　No.261027 R8.10.30
   R8.11.14 Kの指示「エフピコの最新の見積を出して」：Drive「戸島工業　エフピコ換気扇33台取替」の
   最新の見積書（換気設備 有圧換気扇更新工事_見積書_R8.10.30.xlsx、計 2,065,000）を KD見積 に起こした（金額はそのまま）。
   有圧換気扇本体は支給品（取替え工事のみ）。
   法定福利費 201,800・諸経費 199,000 は元の見積のとおり（率の行の adj で合わせる。労務費は単価の約73.5%）。
   参考：富永電機の材料見積（R8.11.13、三菱 現行品 33台＋バックガード 33個）が Drive に届いている（この見積には入れていない）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
LR = 1_223_030 / 1_664_200          # 労務費の割合（法定福利費 16.5% が元の見積の 201,800 になるように）
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note,
                 "pl": jsround(price * LR)})
    return qty * int(price)

s = 0
cat("有圧換気扇 更新（給気ファン）")
for spec, q, p in [("EG-50ETB3-Q　50cm　VS-104'・105・105'", 6, 47_400),
                   ("EG-45DTB3-Q　45cm　VS-101", 1, 47_400),
                   ("EF-45ETB3-Q　45cm　VS-103・110 下段", 2, 47_400),
                   ("EF-25ATB3-Q　25cm　VS-107", 1, 36_600),
                   ("EWG-50ETA　50cm　VS-201 上部", 3, 47_400)]:
    s += it("有圧換気扇取替", spec, q, "台", p)
cat("有圧換気扇 更新（排気ファン）")
for spec, q, p in [("EG-50ETB3　50cm　VE-103'・110'", 6, 47_400),
                   ("EG-50DTB3　50cm　VE-104'・105'", 4, 47_400),
                   ("EG-45DTB3　45cm　VE-104", 1, 47_400),
                   ("EF-45ETB3　45cm　VE-103", 1, 47_400),
                   ("EF-35CTB3　35cm　VE-102", 1, 36_600),
                   ("EG-40BTB3　40cm　VE-107・112・113", 5, 40_900),
                   ("EWG-50ETA　50cm　VE-201 上部", 2, 47_400)]:
    s += it("有圧換気扇取替", spec, q, "台", p)
cat("共通")
s += it("高所作業車", "VS-201・VE-201・嵩天部 ほか　2日", 1, "式", 70_000)
s += it("撤去品処分費", "有圧換気扇 33台", 1, "式", 66_000)
s += it("試運転調整", "33台", 1, "式", 18_100)
assert s == 1_664_200

labor = sum(r["qty"] * r["pl"] for r in rows if "pl" in r)
W_AMT, K_AMT = 201_800, 199_000     # 元の見積のとおり
w_raw = jsround(labor * 16.5 / 100); k_raw = jsround(s * 12 / 100)
TOTAL = s + W_AMT + K_AMT
assert TOTAL == 2_065_000
cat("経　費")
rows.append({"name": "法定福利費", "welfare": 16.5, "adj": W_AMT - w_raw})
rows.append({"name": "諸経費", "rate": 12.0, "adj": K_AMT - k_raw})

data = {"header": {"name": "換気設備 有圧換気扇更新工事", "client": "戸島工業株式会社", "honorific": "御中",
                   "date": "2026-10-30", "staff": "河口", "no": "261027"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "",
        "notes": ["有圧換気扇本体は支給品とし、取替え工事のみです"],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_戸島工業_エフピコ_換気扇更新.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/fpco-kankisen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_戸島工業_エフピコ_換気扇更新.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=fpco-kankisen\n")
for r in rows:
    if r.get("type") == "cat": print("【" + r["name"] + "】"); continue
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:40]:42}{r['qty']:>3}{r['unit']}{r['price']:>9,}{r['qty']*r['price']:>10,}")
print(f"小計 {s:,}／法定福利費 {W_AMT:,}（労務費 {labor:,}・16.5%={w_raw:,}）／諸経費 {K_AMT:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}")
