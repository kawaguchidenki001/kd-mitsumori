# -*- coding: utf-8 -*-
"""東建塩河カントリー2階男子便所排風機更新工事（戸島工業株式会社 御中）R8.10.16
   Kの依頼：添付写真の
     ・天井照明、スピーカーの撤去再取付（天井点検口まわりの天井板を外す範囲：ダウンライト1台・スピーカー1台）
     ・排風機（EF-14）電源の切り離し、再接続
   単価：積算実務マニュアル2026 電気（岐阜県）。脱着＝撤去費＋取付手間（労務費＋経費）。
   経費：法定福利費＝労務費×16.5%（100円切捨て）、諸経費＝純工事費×12%。計（税抜）は雑材消耗品で1,000円単位に合わせる。
   分類行なし（明細が少ないので1枚）。見積Noは新規（Drive に同じ工事名の見積なし）→ 空欄（アプリが採番）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - 3)
    if step < 10: step = 10
    n = int(math.floor(v / step + 0.5))
    return (n if n >= 1 else 1) * step

M = "積算マニュアル電気"
# (品名, 仕様, 数量, 単位, 撤去費, 取付手間, 撤去の労務, 取付の労務, 根拠)
ITEMS = [
    ("照明器具 脱着", "ダウンライト　一時撤去・再取付", 1, "台", 2_600, 9_519, 2_600, 5_894, "LED埋込天井灯 ダウンライト LRS1-05 LN"),
    ("スピーカー 脱着", "天井埋込形　一時撤去・再取付", 1, "個", 2_430, 8_720, 2_430, 5_499, "スピーカー 3W 天井埋込形"),
    ("排風機 電源切り離し・再接続", "EF-14　結線取外し・再結線・動作確認共", 1, "台", 2_160, 7_210, 2_160, 4_907, "電動機結線 直入始動方式"),
]
rows, sub, labor = [], 0, 0
for nm, sp, q, u, rm, inst, rm_l, inst_l, why in ITEMS:
    price = sig(rm + inst); pl = rm_l + inst_l
    rows.append({"name": nm, "spec": sp, "qty": q, "unit": u, "price": price,
                 "note": f"{M}：撤去費{rm:,}＋取付手間{inst:,}（{why}）", "pl": pl})
    sub += q * price; labor += q * pl

WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
# 雑材消耗品（3%程度）で 小計＋法定福利費＋諸経費 を1,000円単位に
best = None
for z in range(10, 3000, 10):
    s = sub + z; total = s + w_amt + jsround(s * KEIHI / 100)
    if total % 1000 == 0 and (best is None or abs(z - sub * 0.03) < abs(best - sub * 0.03)): best = z
ZATSU = best
rows.append({"name": "雑材消耗品", "spec": "", "qty": 1, "unit": "式", "price": ZATSU, "note": "消耗雑材費。小計調整"})
S = sub + ZATSU; k_amt = jsround(S * KEIHI / 100); TOTAL = S + w_amt + k_amt
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": 0})

data = {"header": {"name": "東建塩河カントリー2階男子便所排風機更新工事", "client": "戸島工業株式会社", "honorific": "御中",
                   "date": "2026-10-16", "staff": "河口", "no": ""},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_東建塩河_排風機更新.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/toukenshiokawa-fan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_東建塩河_排風機更新.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=toukenshiokawa-fan\n")

for r in rows:
    if "qty" in r: print(f"  {r['name']} {r['spec']:<28}{r['qty']:>3}{r['unit']}{r['price']:>9,}{r['qty']*r['price']:>9,}  {r['note']}")
print(f"小計 {S:,}（雑材 {ZATSU:,}）／法定福利費 {w_amt:,}（労務費 {labor:,}）／諸経費 {k_amt:,}／計（税抜）{TOTAL:,}")
