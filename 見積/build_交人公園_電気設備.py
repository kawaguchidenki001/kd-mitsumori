# -*- coding: utf-8 -*-
"""交人公園整備工事　電気設備工事（永井建設株式会社 御中）
   発注者：岐阜市都市建設部公園整備課／設計書（令和8年度・入札用＝単価空欄）より拾い出し。

   数量の根拠（設計書 内訳表 6〜7頁／電気設備工構造図(1)(2) 図面番号12・13）
     電気設備工 － 照明設備工   照明灯 LED 水銀灯250W相当 …………… 4 基（単価表 SJ0070）
                                引込柱・分電盤 ………………………… 1 基（単価表 SJ0072）
                － 電線管路工   電線管 FEP30 …………………………… 162 m（単価表 SJ0080）
                                電線 EM-CE3.5□-2C …………………… 162 m（単価表 SJ0082）
     公園施設等撤去工            照明灯撤去 ……………………………… 4 基（単価表 SJ0520）

   単価は設計書の単価表の構成に合わせ、電気設備工事積算実務マニュアル2026（岐阜県）の
   複合単価を積み上げたもの。★は同マニュアルに登録が無く材料実勢から積み上げた項目。
   掘削・埋戻し（作業土工）は設計書上「基盤整備」に別計上されているため本見積に含めない。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    """単価の丸め：四捨五入で上3桁、最小単位は10円（1円単位は出さない）"""
    v = float(v)
    if v <= 0: return 0
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - 3)
    if step < 10: step = 10
    n = int(math.floor(v / step + 0.5))
    return (n if n >= 1 else 1) * step

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return qty * int(price)

# ---- 内訳は設計書の単価表（SJ0070/0071/0072/0080/0081/0082/0520）の構成どおりに分けて計上 ----
# 材料：扇港電機 見積 No.26091322（R8.9.28）の NET×1.2。メーカー別のNET合計を定価比で各品へ按分。
#   照明器具 定価1,833,000→NET1,412,000（×0.7703）／引込柱・分電盤 定価410,360→NET264,000（×0.6433）
R_LAMP = 1_412_000 / 1_833_000 * 1.2
R_HIKI = 264_000 / 410_360 * 1.2
def m(teika, r): return sig(teika * r)

def zero(name, spec, note=""):
    rows.append({"name": name, "spec": spec, "qty": 1, "unit": "式", "price": 0, "note": note, "zero": True})

sub = 0
cat("01 照明設備工")
# 照明灯 LED 水銀灯250W相当 4基（設計書 SJ0070・数量計算書：1基当り コンクリート0.18m3・スパイラル0.9m・砕石0.36m2）
sub += it("LEDポールライト", "岩崎電気 E50110/NSAZ9 昼白色", 4, "台", m(184_000, R_LAMP), 0, "扇港NET×1.2（定価184,000）")
sub += it("照明柱", "岩崎電気 段付鋼管ポール H=5.3m 地中引込式", 4, "本", m(211_000, R_LAMP), 0, "扇港NET×1.2（定価211,000）")
sub += it("ジョイントユニット", "岩崎電気 EFMT68-15A", 4, "個", m(14_400, R_LAMP), 0, "扇港NET×1.2（定価14,400）")
sub += it("自動点滅器", "岩崎電気 PHM1003-2SB 100V/3A", 4, "個", m(18_850, R_LAMP), 0, "扇港NET×1.2（定価18,850）")
sub += it("ポール運賃", "", 1, "式", m(120_000, R_LAMP), 0, "扇港NET×1.2（定価120,000）")
sub += it("照明灯設置", "350kg以下 建柱", 4, "基", 38_900, 38_900, "ポール灯の労務費51,888を建柱と器具取付に配分")
sub += it("照明器具取付", "", 4, "台", 13_000, 13_000, "同上")
sub += it("自動点滅器取付", "ポール取付", 4, "個", 4_600, 4_597, "複合単価の労務費")
sub += it("接地工事", "Ｄ種 接地棒φ10×1500", 4, "極", 9_880, 5_161, "複合単価")
zero("基礎コンクリート", "18-8-25BB 0.72m3　別途", "0.18m3×4基")
sub += it("スパイラルダクト", "φ500 t=0.6", 3.6, "m", 6_000, 2_000, "★0.9m×4基")
zero("基礎砕石", "RC-40 t=100 1.44m2　別途", "0.36m2×4基")
zero("土工費（照明灯）", "床掘4.0m3・埋戻し3.2m3　別途", "設計書 土量集計表。基盤整備に計上")
# 引込柱・分電盤 1基（設計書 SJ0072：コンクリート0.21m3・スパイラル1.1m・砕石0.36m2・電線3m）
sub += it("引込柱", "パナソニック スッキリポール XDKM0163A L6.3m", 1, "本", m(79_500, R_HIKI), 0, "扇港NET×1.2（定価79,500）")
sub += it("アウトカバー", "パナソニック DDF412A", 1, "個", m(3_460, R_HIKI), 0, "扇港NET×1.2（定価3,460）")
sub += it("分電盤", "パナソニック スッキリボックス DDB5313KA", 1, "面", m(169_000, R_HIKI), 0, "扇港NET×1.2（定価169,000）。2枚扉")
sub += it("分電盤 内器ユニット", "", 1, "式", m(158_400, R_HIKI), 0, "扇港NET×1.2（定価158,400）")
sub += it("引込柱 組立据付", "", 1, "基", 45_000, 45_000, "★")
sub += it("分電盤取付", "", 1, "面", 18_000, 18_000, "★")
sub += it("電線", "ＥＭ－ＣＥ３.５□－２Ｃ", 3, "m", 1_090, 479, "引込柱内")
sub += it("接地工事", "Ｄ種 接地棒φ10×1500", 1, "極", 9_880, 5_161, "複合単価")
zero("基礎コンクリート", "18-8-25BB 0.21m3　別途")
sub += it("スパイラルダクト", "φ500 t=0.6", 1.1, "m", 6_000, 2_000, "★")
zero("基礎砕石", "RC-40 t=100 0.36m2　別途")
zero("土工費（引込柱）", "床掘1.3m3・埋戻し1.0m3　別途", "設計書 土量集計表。基盤整備に計上")

cat("02 電線管路工")
# 電線管 FEP30 162m（設計書 SJ0080：FEP敷設＋再生砂0.09m3/m＋埋設標識シート）
sub += it("波付硬質合成樹脂管", "ＦＥＰ３０ 構内地中", 162, "m", 1_400, 733, "複合単価")
sub += it("再生砂", "管巻き", 14.6, "m3", 6_000, 2_222, "★0.09m3/m×162m")
sub += it("埋設標識シート", "Ｗ＝150 ２倍", 162, "m", 380, 113, "複合単価")
sub += it("電線", "ＥＭ－ＣＥ３.５□－２Ｃ 管内", 162, "m", 1_090, 479, "複合単価")
sub += it("雑材消耗品", "", 1, "式", 27_000, 0, "圧着端子・テープ・標識類ほか")
zero("土工費（電線管）", "床掘16.2m3　別途", "設計書 土量集計表。基盤整備に計上")

cat("03 公園施設等撤去工")
# 照明灯撤去 4基（設計書 SJ0520：灯撤去＋基礎とりこわし0.31m3/基＋殻運搬）
sub += it("照明灯撤去", "350kg以下", 4, "基", 22_900, 15_578, "複合単価の撤去費")
sub += it("基礎とりこわし", "無筋", 1.24, "m3", 12_000, 8_000, "★0.31m3×4基")
sub += it("殻運搬・処分", "無筋", 1.24, "m3", 4_000, 0, "★")

# ---- 集計 ------------------------------------------------------------------
cat("経　費")
labor = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
sub = int(round(sub))
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100   # 100円単位（Kの指示）
k_raw = jsround(sub * KEIHI / 100)
TARGET = (sub + w_amt + k_raw) // 1000 * 1000
k_amt = TARGET - sub - w_amt
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費",     "rate": KEIHI,     "adj": k_amt - k_raw})

data = {"header": {"name": "交人公園整備工事　電気設備工事",
                   "client": "永井建設株式会社", "honorific": "御中",
                   "date": "2026-09-28", "staff": "河口", "no": "260915"},
        "place": "岐阜市大学北２丁目地内",
        "validity": "発行日より1ヶ月", "remarks": "",
        "taxMode": "ex", "taxRate": 10, "rows": rows}

root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_交人公園整備工事_電気設備工事.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/kojin-park.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    if r.get("type") == "cat": print("\n【" + r["name"] + "】"); continue
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:38]:40}{r['qty']:>6}{r['unit']:<3}{r['price']:>10,}{round(r['qty']*r['price']):>12,}")
tax = jsround(TARGET * 0.1)
print(f"\n{'小　計（純工事費）':22}{sub:>12,}")
print(f"{'法定福利費':22}{w_amt:>12,}   （労務費 {round(labor):,}×{WELFARE}%）")
print(f"{'諸経費':22}{k_amt:>12,}   （純工事費×{KEIHI}%＋端数調整）")
print(f"{'計（税抜）':22}{TARGET:>12,}\n{'消費税10%':22}{tax:>12,}\n{'合　計':22}{TARGET+tax:>12,}")
assert TARGET % 1000 == 0

payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_交人公園_電気設備.txt", "w").write(
    url + "\nhttps://kd-mitsumori.pages.dev/#q=kojin-park\n")
print("URL長", len(url))
