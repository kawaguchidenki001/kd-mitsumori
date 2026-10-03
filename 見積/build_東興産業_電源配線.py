# -*- coding: utf-8 -*-
"""東興産業株式会社　既設工場 電源配線工事（R8.10.1）
   参考：当社見積 No.260505（R8.5.8 既設工場射出成形機電源配線工事）の書き方
   材料：Kの材料表（CVT60 60m／CVT150 20m／IV14緑 15m／IV38緑 20m／VE54 2本／VE70 1本
         ／2号コネ・ビニルブッシング／FEVE-50A・65A／ダクタークリップ54・70／端子150-8CB×6／キャップ150 赤白青×2）
   単価：複合単価（電気設備工事積算実務マニュアル2026 岐阜県）。
         電線・ケーブルは材料費だけを扇港電機 見積 No.26091545（R8.9.30）の実仕入単価に置き換え、
         経費は（材料費＋労務費）の増えた割合だけ増やす（Kの指示：ケーブルの値上がりを考慮）。
   VE は DB に登録が無いため HIVE 露出の複合単価を使う（付属品＝コネクタ・ブッシング含む）。
   端子・キャップ・FEVE・ダクタークリップは雑材消耗品に含める。
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

# (DB材料単価, 材料費(ロス・付属品込), 労務費, 経費, 複合単価, 実仕入単価)
DB = {
    "CVT60":  (4_394,  4_844, 2_312, 1_620,  8_780,  4_856),
    "CVT150": (10_977, 12_102, 3_863, 3_147, 19_100, 12_049),
    "IV14":   (366,      442,   564,   314,  1_320,    444),
    "IV38":   (952,    1_100,   902,   545,  2_550,  1_157),
}
def adj(k):
    mat, mc, lab, exp, comp, net = DB[k]
    mc2 = net * mc / mat
    exp2 = exp * (mc2 + lab) / (mc + lab)
    return sig(mc2 + lab + exp2), lab, comp

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, pl, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return qty * int(price)

sub = 0
# 1枚に収めるため分類行は立てない（Kの指示 R8.10.3）
for k, nm, sp, q, unit in [("CVT60", "ケーブル配線", "ＣＶＴ６０sq", 60, "ｍ"),
                           ("CVT150", "ケーブル配線", "ＣＶＴ１５０sq", 20, "ｍ"),
                           ("IV14", "電線配線", "ＩＶ１４sq 緑", 15, "ｍ"),
                           ("IV38", "電線配線", "ＩＶ３８sq 緑", 20, "ｍ")]:
    p, lab, comp = adj(k)
    if k == "CVT150": p = sig(p * 0.95)   # 150sqを5%値下げ（Kの指示）
    sub += it(nm, sp, q, unit, p, lab)   # 備考に仕入単価は書かない（お客様に出る）
    print(f"   {k}: 複合単価{comp:,} → 補正後{p:,}（仕入{DB[k][5]:,}）")
sub += it("電線管取付", "ＶＥ５４ 露出", 8, "ｍ", 7_540, 4_399, "2本。コネクタ・ブッシング共")
sub += it("電線管取付", "ＶＥ７０ 露出", 4, "ｍ", 9_360, 5_471, "1本。ブッシング共")
# 電線管支持材を追加（Kの指示）：ダクタークリップ54用×6・70用×3（材料約300＋取付500）/個
sub += it("電線管支持材", "ダクタークリップ", 1, "式", sig(9 * 800), 9 * 500)
ZATSU = sig(sub * 0.03)
sub += it("雑費", "", 1, "式", ZATSU, 0)   # 雑材消耗品→雑費、品名のみ（Kの指示）

labor = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
WELFARE, KEIHI = 16.5, 10.0
w_amt = 0   # 法定福利費は無し（Kの指示）
k_raw = jsround(sub * KEIHI / 100)
TARGET = (sub + w_amt + k_raw) // 1000 * 1000
rows.append({"name": "諸経費", "rate": KEIHI, "adj": (TARGET - sub - w_amt) - k_raw})

data = {"header": {"name": "既設工場 電源配線工事", "client": "東興産業株式会社", "honorific": "御中",
                   "date": "2026-10-01", "staff": "河口", "no": "261001"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}

root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_東興産業_電源配線.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/toukou-dengen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    if r.get("type") == "cat": print("\n【" + r["name"] + "】"); continue
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:34]:36}{r['qty']:>4}{r['unit']:<2}{r['price']:>9,}{r['qty']*r['price']:>11,}  {r['note']}")
k_amt = TARGET - sub - w_amt; tax = jsround(TARGET * 0.1)
print(f"\n小計 {sub:,}／法定福利費 {w_amt:,}（労務費{labor:,}×{WELFARE}%）／諸経費 {k_amt:,}／計（税抜）{TARGET:,}／税込 {TARGET+tax:,}")
print("人工", round(labor / 28_200, 1))
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_東興産業_電源配線.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=toukou-dengen\n")
