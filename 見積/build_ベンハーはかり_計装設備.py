# -*- coding: utf-8 -*-
"""ベンハーはかり新社屋新築工事　計装設備工事（R8.10.9）
   図面：M-011 自動制御設備1階平面図／M-012 2階平面図／M-013 屋根伏図（A3・1/150、スキャン）、M-000〜002 機械設備仕様
   配線：凡例「傍記なき配線」EM-CPEE-S 1.2-2C（屋内露出C25・隠ぺいPF22・屋外露出C25）、F2＝EM-EEF2.0-3C
         二重天井内はケーブル工事。室内機の器具はすべて天井カセット＝天井内転がしとした。
   拾い：図面の配線を区間ごとに実測（スキャン300dpiで1px≒18mm、通り芯5,650/3,800で検証）。
     2C 天井内  1F 部品倉庫室1（MAC2A/2B 4系統・HEX2）124m、事務所・打合せ・応接・エントランス 73m
                2F 自動機室（MAC3A/3B/3C・HEX2）141m、ホール2（MAC4-1×5・HEX1）45m、1F SC→EPS 27m → 計410m
     2C 管内    屋上 室外機間渡り・PB(WP・SUS)まで 27m（C25屋外露出）＋EPS立上り 9m（C25）→ 36m
     2C PF管内  リモコン R19・(R)9・SC1 の立下り 29ヶ所×2m → 58m
     F2         排気ファンSW 5ヶ所（1F WWC1・MWC1・ポンプ室、2F FE-1×2）と冷媒安全遮断弁 17m＋立下り 5×2m
   ケーブル・管の長さは余長×1.1。単価は複合単価（積算実務マニュアル2026）。CPEE-S 1.2-2C は EM-CEE-S 1.25-2C の単価を準用。
   リモコン・集中管理コントローラー・排気ファンSWは空調・換気メーカーの支給品として取付のみ。★は登録なし・概算。
"""
import json, base64, math
def jsround(x): return math.floor(x + 0.5)
def sig(v):
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step
Y = 1.1
m = lambda v: int(round(v * Y))

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(pl)
    rows.append(r); return int(round(qty * int(price)))
def betto(name):
    rows.append({"name": name, "spec": "（別途）", "qty": 1, "unit": "式", "price": 0, "note": "", "zero": True})

s = 0
cat("01　計装配線")
s += it("制御ケーブル", "ＥＭ－ＣＰＥＥ－Ｓ １．２－２Ｃ 天井内ころがし", m(410), "ｍ", 830, 338)
s += it("制御ケーブル", "ＥＭ－ＣＰＥＥ－Ｓ １．２－２Ｃ 管内", m(36), "ｍ", 940, 423)
s += it("制御ケーブル", "ＥＭ－ＣＰＥＥ－Ｓ １．２－２Ｃ ＰＦ管内", m(58), "ｍ", 880, 381)
s += it("ケーブル", "ＥＭ－ＥＥＦ２．０－３Ｃ 天井内ころがし", m(17), "ｍ", 1_070, 479)
s += it("ケーブル", "ＥＭ－ＥＥＦ２．０－３Ｃ ＰＦ管内", m(10), "ｍ", 1_220, 592)
cat("02　電線管・ボックス")
s += it("薄鋼電線管", "Ｃ２５ 露出（屋上・ＥＰＳ）", m(36), "ｍ", 4_030, 2_369)
s += it("合成樹脂製可とう電線管", "ＰＦ２２ 隠ぺい", m(68), "ｍ", 1_870, 1_156)
s += it("スイッチボックス", "１個用", 34, "個", 4_390, 2_820)
s += it("プルボックス", "ＳＵＳ製 ＷＰ（屋上）", 1, "個", 20_000, 9_165, "★")
cat("03　機器取付")
s += it("運転リモコン取付", "パッケージ１９・全熱交換ユニット９（支給品）", 28, "個", 2_390, 1_523)
s += it("集中管理コントローラー取付", "支給品", 1, "台", 10_000, 5_640, "★")
s += it("排気ファンスイッチ取付", "支給品", 5, "個", 2_390, 1_523)
s += it("冷媒安全遮断弁 結線", "", 1, "ヶ所", 5_000, 3_000, "★")
s += it("既設空調 制御系統改修", "伝送線接続・既設エアコンリモコン増設", 1, "式", 80_000, 56_400, "★")
betto("試運転調整")

labor = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
# 雑材消耗品で端数調整（Kの標準）：3%に一番近く、小計＋法定福利費＋諸経費(12%ちょうど)が1,000円単位になる額
z0 = sig(s * 0.03)
ok = lambda z: (s + z + w_amt + jsround((s + z) * KEIHI / 100)) % 1000 == 0
ZATSU = min((z for z in range(10, 2 * z0, 10) if ok(z)), key=lambda z: abs(z - z0))
rows.insert(next(i for i, r in enumerate(rows) if r.get("name") == "試運転調整"), {"name": "雑材消耗品", "spec": "", "qty": 1, "unit": "式", "price": ZATSU, "note": ""})
s += ZATSU
cat("経　費")
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": 0})
TARGET = s + w_amt + jsround(s * KEIHI / 100)
assert TARGET % 1000 == 0

data = {"header": {"name": "ベンハーはかり新社屋新築工事　計装設備工事", "client": "", "honorific": "御中",
                   "date": "2026-10-09", "staff": "河口", "no": "261008"},
        "place": "岐阜県", "validity": "発行日より1ヶ月", "remarks": "",
        "notes": ["リモコン・集中管理コントローラー・排気ファンスイッチは支給品とし、取付のみです"],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_ベンハーはかり_計装設備.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/benhur-keisou.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_ベンハーはかり_計装設備.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=benhur-keisou\n")
for r in rows:
    if r.get("type") == "cat": print("【" + r["name"] + "】"); continue
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:36]:38}{r['qty']:>5}{r['unit']:<3}{r['price']:>8,}{int(round(r['qty']*r['price'])):>10,} {r['note']}")
k = TARGET - s - w_amt
print(f"小計 {s:,}／法定福利費 {w_amt:,}／諸経費 {k:,}／計（税抜）{TARGET:,}／税込 {TARGET+jsround(TARGET*0.1):,}  人工 {labor/28200:.1f}")
