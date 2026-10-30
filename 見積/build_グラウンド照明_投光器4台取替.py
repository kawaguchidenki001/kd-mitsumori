# -*- coding: utf-8 -*-
"""グラウンド照明設備修繕（LED投光器 4台取替）岐阜市長 柴橋正直 御中（R8.10.30）
   元：R6.10.30 No.241034「グラウンド照明設備修繕（ｺﾝ柱・1000W)」計 1,758,000（税抜）の項目。
   Kの指示：内容は投光器4台の取替のみ。不要な項目（コンクリート柱・根かせブロック・足場ボルト・投光器架台・
           既設架空ケーブルの撤去再取付・建柱車・運搬費）は削除。現行価格で。
   単価（★は確認できていない）：
     ・LED投光器 NYS35345（1000W相当）：R6 198,000 → ★メーカーの価格改定を約1割とみて 218,000。仕入先の見積で確認する。
     ・ケーブル CV2.0sq-3C 12m（投光器4台の結線 3m×4）：R6 380 → ★420（銅価格の上昇分）。
     ・電工費：投光器 4台の撤去・取付・結線（既設柱・既設架台を利用）★35,000×4。
     ・高所作業車費 1日：R6 28,000 → ★30,000。撤去品処分費：既設投光器4台（メタハラランプ含む）★16,000。
     ・雑材・消耗品で 小計を1,000円単位に。諸経費 12%（R6・最近の学校の見積と同じ）、計を1,000円単位に（諸経費の adj）。
   R8.10.30 Kの指示：合計（税抜）1,450,000 に調整（各項目を同じ率で上げる）。
   見積No は新規（空欄＝アプリが採番）。学校名（工事場所）は未定。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)

rows = []
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(pl)
    rows.append(r); return qty * int(price)

# R8.10.30 Kの指示：合計（税抜）を 1,450,000 に → 各項目を同じ率で上げ、雑材で小計 1,295,000、諸経費 12% の端数は adj
TARGET, S_T = 1_450_000, 1_295_000
def sig(v):
    v = float(v); step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step
BASE = {"toukou": 218_000, "cable": 420, "denko": 140_000, "kosho": 30_000, "shobun": 16_000}
UP = (S_T - 6_000) / (4 * BASE["toukou"] + 12 * BASE["cable"] + BASE["denko"] + BASE["kosho"] + BASE["shobun"])
P = {k: sig(v * UP) for k, v in BASE.items()}
s = 0
s += it("LED投光器", "NYS35345　1000W相当", 4, "台", P["toukou"], 0, f"★R6 198,000×約1.1×{UP:.3f}")
s += it("ケーブル", "CV2.0sq-3C", 12, "ｍ", P["cable"], 0, "★")
DENKO, KOSHO, SHOBUN = P["denko"], P["kosho"], P["shobun"]
ZATSU = S_T - (s + DENKO + KOSHO + SHOBUN)                       # 雑材・消耗品で 小計を 1,295,000 に
s += it("雑材・消耗品", "", 1, "式", ZATSU)
s += it("電工費", "投光器 撤去・取付・結線", 1, "式", DENKO, DENKO, "★既設柱・架台利用")
s += it("高所作業車費", "", 1, "日", KOSHO, 0, "★")
s += it("撤去品処分費", "既設投光器 4台", 1, "式", SHOBUN, 0, "★")
assert s == S_T

KEIHI = 12.0
k_raw = jsround(s * KEIHI / 100)
TOTAL = TARGET
rows.append({"name": "諸経費", "rate": KEIHI, "adj": TOTAL - s - k_raw})

data = {"header": {"name": "グラウンド照明設備修繕（LED投光器取替）", "client": "岐阜市長　柴橋正直", "honorific": "御中",
                   "date": "2026-10-30", "staff": "河口", "no": ""},
        "place": "", "validity": "", "remarks": "", "notes": [], "addrKind": "public",
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_グラウンド照明_投光器4台取替.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/ground-toukouki4.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_グラウンド照明_投光器4台取替.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=ground-toukouki4\n")
for r in rows:
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:30]:32}{r['qty']:>3}{r['unit']:<2}{r['price']:>9,}{r['qty']*r['price']:>10,}  {r['note']}")
print(f"小計 {s:,}／諸経費 {TOTAL - s:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}／税込 {TOTAL + jsround(TOTAL*0.1):,}")
