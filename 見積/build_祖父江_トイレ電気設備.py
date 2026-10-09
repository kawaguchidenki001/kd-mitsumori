# -*- coding: utf-8 -*-
"""令和8年度 国営公園祖父江地区施設改修工事　電気設備工事（下流側トイレ）
   拾い出し：数量総括表 p.3「電気設備工」、電気設備工数量調書 p.16、計算書 p.55〜59
     照明設備工  トイレ分電盤 W405×D222×H680 1面（基礎共）／既存分電盤改良 W700×D370×H1540 1面
     電線管路工  FEPφ30 71.5m（26.7+29.6+15.2）／EM-CET100sq 282.2m／EM-CE14sq-2C 38.2m／EM-CE22sq-2C 41.7m
     電線管土工  A（FEP30×3）8.9m／B（FEP30×2）14.8m／C（FEP30×1）15.2m … 山砂・埋設シート
     作業土工    床掘 9.0m3／埋戻し 6.3m3
   対象外：電気設備の撤去（ハンドホール・FEP80・CET38・2CT3.5-3C・CVT38）は撤去平面図で「※施工対象外」。
           電源接続盤A・B（便所工）も「施工対象外」。太陽電池電源システム図は参考図（便所に付属）。
   単価：複合単価（積算実務マニュアル2026）。ケーブルは複合単価×1.3（Kの指示）。★は登録なし・概算。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

CABLE = 1.3
rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return int(round(qty * int(price)))

sub = 0
CAB = 0
# 1枚に収めるため分類行は立てない（Kの指示 R8.10.3）
# ★屋外用ステンレス（防水平面ハンドル）。主幹ELCB 3P 50A・分岐（便所3回路＋予備）を想定。
#   DB「主幹ELCB 3P 50AF/50A 分岐MCCB 2P1E-6 予備-2」125,000 に屋外SUS箱の差額を見て×1.4
sub += it("トイレ分電盤", "屋外形 W405×D222×H680", 1, "面", sig(125_000 * 1.4), 49_576, "★屋外SUS製 概算")
# 基礎：コンクリート0.06m3×46,000＋型枠0.57m2×13,500＋基礎砕石0.032m3×9,670
KISO = 0.06 * 46_000 + 0.57 * 13_500 + 0.032 * 9_670
KISO_L = 0.06 * 18_720 + 0.57 * 6_908 + 0.032 * 5_080
def betto(name):   # 別途（0円）行
    rows.append({"name": name, "spec": "（別途）", "qty": 1, "unit": "式", "price": 0, "note": "", "zero": True})
betto("分電盤基礎")   # 基礎は別途（Kの指示）
# ★既存分電盤改良：主幹 MCCB3P 100AF/60AT→225AF/125AT（中性線欠相保護付）、
#   下流側便所 ELCB3P 50AF/30AT→50AF/50AT、EM-CET100sq 接続。器具材料 約73,000＋1.5人工
sub += it("既存分電盤改良", "主幹ＭＣＣＢ・分岐ＥＬＣＢ取替", 1, "面", sig(73_000 + 28_200 * 1.5 * 1.2), 42_300, "★概算")

for nm, sp, q, comp, lab in [("ケーブル配線", "ＥＭ－ＣＥＴ１００sq", 282.2, 13_600, 2_843),
                             ("ケーブル配線", "ＥＭ－ＣＥ１４sq－２Ｃ", 38.2, 2_180, 736),
                             ("ケーブル配線", "ＥＭ－ＣＥ２２sq－２Ｃ", 41.7, 2_950, 939)]:
    c = it(nm, sp + " 管路内", q, "ｍ", sig(comp * CABLE), lab); sub += c; CAB += c
sub += it("電線管", "ＦＥＰ３０ 地中", 71.5, "ｍ", 1_400, 733)

SAND = round(0.08 * 8.9 + 0.07 * 14.8 + 0.06 * 15.2, 1)   # 計算書A/B/C 10m当り 0.8/0.7/0.6m3
SHEET = round(8.9 + 14.8 + 15.2, 1)
# 床掘・埋戻し・山砂は土工として別途、埋設標識シートのみ残す（Kの指示）
sub += it("埋設標識シート", "Ｗ＝150 シングル", SHEET, "ｍ", 280, 113)
sub += it("既設撤去費", "", 1, "式", 60_000, 40_000)   # Kの指示（R8.10.9）
labor = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
# 雑材消耗品で端数調整（Kの標準）：ケーブルを除く工事の3%以下で、小計＋法定福利費＋諸経費(12%ちょうど)が1,000円単位になる額
z0 = sig((sub - CAB) * 0.03) // 10 * 10
ok = lambda z: (sub + z + w_amt + jsround((sub + z) * KEIHI / 100)) % 1000 == 0
ZATSU = min((z for z in range(10, 2 * z0, 10) if ok(z)), key=lambda z: abs(z - z0))   # 3%に一番近い額
sub += it("雑材消耗品", "", 1, "式", ZATSU, 0)
betto("土工")
k_raw = jsround(sub * KEIHI / 100)
TARGET = sub + w_amt + k_raw
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": (TARGET - sub - w_amt) - k_raw})

data = {"header": {"name": "国営公園祖父江地区施設改修工事　電気設備工事", "client": "株式会社川瀬組", "honorific": "御中",
                   "date": "2026-10-09", "staff": "河口", "no": "261003"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "",
        "notes": ["電源接続盤A・Bは含みません", "トイレ分電盤は図面に詳細が無いため概算です"],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_祖父江_トイレ電気設備.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/sobue-toilet.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in rows:
    if r.get("type") == "cat": print("【" + r["name"] + "】"); continue
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:30]:32}{r['qty']:>7}{r['unit']:<3}{r['price']:>9,}{int(round(r['qty']*r['price'])):>11,} {r['note']}")
k_amt = TARGET - sub - w_amt; tax = jsround(TARGET * 0.1)
print(f"小計 {sub:,}／法定福利費 {w_amt:,}（労務費{round(labor):,}）／諸経費 {k_amt:,}／計（税抜）{TARGET:,}／税込 {TARGET+tax:,}")
print("人工", round(labor / 28_200, 1))
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_祖父江_トイレ電気設備.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=sobue-toilet\n")
