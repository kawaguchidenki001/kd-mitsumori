# -*- coding: utf-8 -*-
"""東建塩河カントリー2階男子便所排風機更新工事（戸島工業株式会社 御中）R8.10.16
   Kの依頼：添付写真の
     ・天井照明、スピーカーの撤去再取付（天井点検口まわりの天井板を外す範囲：ダウンライト1台・スピーカー1台）
     ・排風機（EF-14）電源の切り離し、再接続
   単価：積算実務マニュアル2026 電気（岐阜県）。脱着＝撤去費＋取付手間（労務費＋経費）。
   経費：R8.10.16 Kの指示「法定福利費は無し、運搬費で4000円計上」→ 小計 → 運搬費 4,000 → 諸経費（純工事費×12%）。
         小計は 雑材消耗品（3%程度）で1,000円単位に、計（税抜）の1,000円未満は諸経費の adj で合わせる。
   分類行なし（明細が少ないので1枚）。見積Noは新規（Drive に同じ工事名の見積なし）→ 空欄（アプリが採番）。
   R8.10.17 Kの指示：撤去で1日、再取付で1日行くので 運搬費 6,000円、計が6万円程度になるように。「動作確認」は書かない。
         → 3項目のマニュアル脱着の金額を同じ率で上げて 小計 48,000、計（税抜）60,000（端数は諸経費の adj）。
   R8.10.17 Kの指示：64,000円にする → 小計 52,000、諸経費 12%＝6,240 の端数を切捨てて 6,000、計（税抜）64,000。
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
    ("排風機 電源切り離し・再接続", "EF-14　結線取外し・再結線", 1, "台", 2_160, 7_210, 2_160, 4_907, "電動機結線 直入始動方式"),
]
KEIHI, UNPAN, TOTAL, S = 12.0, 6_000, 64_000, 52_000   # R8.10.17 Kの指示：運搬費 6,000（2日）、計 64,000 → 小計 52,000
base = sum(q * sig(rm + inst) for nm, sp, q, u, rm, inst, rm_l, inst_l, why in ITEMS)
UP = S / 1.03 / base                                  # 雑材消耗品（3%程度）を残して 小計 S になる率
rows, sub, labor = [], 0, 0
for nm, sp, q, u, rm, inst, rm_l, inst_l, why in ITEMS:
    price = sig((rm + inst) * UP); pl = jsround((rm_l + inst_l) * UP)
    rows.append({"name": nm, "spec": sp, "qty": q, "unit": u, "price": price,
                 "note": f"{M}：撤去費{rm:,}＋取付手間{inst:,}（{why}）×{UP:.2f}（撤去・再取付で2日）", "pl": pl})
    sub += q * price; labor += q * pl
ZATSU = S - sub
rows.append({"name": "雑材消耗品", "spec": "", "qty": 1, "unit": "式", "price": ZATSU, "note": "消耗雑材費。小計調整"})
u_rate = round(UNPAN / S * 100, 1)                    # 運搬費は小計の下に率計上の行で置き、adj で 4,000 ちょうどに
rows.append({"name": "運搬費", "rate": u_rate, "adj": UNPAN - jsround(S * u_rate / 100), "note": "Kの指示 6,000円（撤去・再取付で2日）"})
k_raw = jsround(S * KEIHI / 100)
k_amt = TOTAL - S - UNPAN                             # 計を 64,000 に（12%との差は adj）
rows.append({"name": "諸経費", "rate": KEIHI, "adj": k_amt - k_raw})
data = {"header": {"name": "東建塩河カントリー2階男子便所排風機更新工事", "client": "戸島工業株式会社", "honorific": "御中",
                   "date": "2026-10-17", "staff": "河口", "no": ""},
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
print(f"小計 {S:,}（雑材 {ZATSU:,}）／運搬費 {UNPAN:,}／諸経費 {k_amt:,}（12%＝{k_raw:,}）／計（税抜）{TOTAL:,}")
