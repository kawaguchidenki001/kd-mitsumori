# -*- coding: utf-8 -*-
"""大藪小学校屋内運動場空調設備設置工事（電気）―― Kの最新版 No.261015 を元に修正（R8.10.14）
   ※R8.10.15 図面 v10 で拾い直した build_大藪小_電気設備_v10.py が最新。この版の出力は _K版261015／q/oyabu-denki-k261015 に分けた。
   元：Kの見積 xlsx（R8.10.12 No.261015、株式会社大幸建築設計事務所 御中、計 8,303,000）。単価は tankatool×1.15。
   Kの指示（R8.10.14）：
     ・数量は整数にする（小数の数量は切り上げ）
     ・壁貫通は機械はつり（tankatool 機械はつり 口径50mm 厚120〜150mm 10,200×1.15）
     ・宛名は元の見積どおり 株式会社大幸建築設計事務所
   経費は元の見積と同じ形：雑費＝小計の約5%で（小計＋雑費）を1万円単位に、諸経費＝（小計＋雑費）×15%。
   ※これより前の build_大藪小_電気設備.py（図面からの拾い出し版）は旧版。
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

rows = []
def it(name, qty, unit, price, note=""):
    q = math.ceil(qty - 1e-9)                 # 数量は整数（切り上げ）
    rows.append({"name": name, "spec": "", "qty": q, "unit": unit, "price": int(price), "note": note + (f"（元 {qty}）" if q != qty else "")})
    return q * int(price)

s = 0
s += it("ケーブル　ＥＭ－ＣＥ３．５sq－３Ｃ　管内", 658, "ｍ", 1_600)
s += it("ケーブル　ＥＭ－ＣＥＴ３８sq　管内", 14.4, "ｍ", 7_160)
s += it("ケーブル　ＥＭ－ＣＥ１４sq－２Ｃ　管内", 3.6, "ｍ", 2_650)
s += it("ケーブル　ＥＭ－ＣＥ２．０sq－３Ｃ　管内", 72, "ｍ", 1_200)
s += it("電線　ＥＭ－ＩＥ５．５sq　管内", 7.6, "ｍ", 920)
s += it("電線管　ＧＰＺ２２　露出　溶融亜鉛メッキ", 25.9, "ｍ", 5_570)
s += it("電線管　ＧＰＺ２８　露出　溶融亜鉛メッキ", 25.9, "ｍ", 7_270)
s += it("電線管　ＧＰＺ３６　露出　溶融亜鉛メッキ", 18.8, "ｍ", 8_790)
s += it("電線管　ＧＰＺ４２　露出　溶融亜鉛メッキ", 54, "ｍ", 11_600)
s += it("電線管　ＧＰＺ５４　露出　溶融亜鉛メッキ", 67.6, "ｍ", 15_900)
s += it("電線管　Ｆ２・ＷＰ２４　ビニル被覆付", 22.2, "ｍ", 3_390)
s += it("電線管　Ｆ２・ＷＰ５０　ビニル被覆付", 3.6, "ｍ", 7_430)
s += it("電線管　ＣＰ２５　露出（塗装共）", 9.6, "ｍ", 4_630)
s += it("電線管　ＥＰ２５　天井内隠ぺい", 20.2, "ｍ", 3_350)
s += it("電線管　ＥＰ３９　天井内隠ぺい", 18, "ｍ", 5_260)
s += it("電線管　ＨＩＶＥ１６　地中埋設", 7.6, "ｍ", 2_310)
s += it("電線管　ＦＥＰ３０　地中埋設", 3, "ｍ", 1_610)
s += it("電線管付属品", 1, "式", 101_000)
s += it("電線管支持材", 1, "式", 273_000)
s += it("プルボックス　150×150×150　ＳＵＳ・ＷＰ", 8, "個", 21_500)
s += it("プルボックス　200×200×200　ＳＵＳ・ＷＰ", 4, "個", 32_800)
s += it("プルボックス　250×250×250　ＳＵＳ・ＷＰ", 6, "個", 47_400)
s += it("プルボックス　500×500×300　ＳＵＳ・ＷＰ", 1, "個", 113_000)
s += it("丸形露出ボックス", 3, "個", 5_800)
s += it("非常用赤色コンセント　２Ｐ１５Ａ　Ｅ付　キャップ付", 3, "個", 4_610)
s += it("防水コンセント　２Ｐ１５Ａ　Ｅ付", 1, "個", 4_610)
s += it("分電盤　Ｌ－ＡＣ　屋外自立型（ＷＰ・ＳＵＳ　国土交通省仕様）", 1, "台", 1_020_000)
s += it("開閉器盤　Ｓ－ＡＣ　屋外壁掛型（ＷＰ・ＳＵＳ）新設", 1, "面", 253_000)
s += it("分電盤改修　既設夜間照明開閉器盤（屋外型ＳＵＳ製）", 1, "式", 253_000)
s += it("接地工事　ＥＤ・ＥＤＥＬＢ　打込式接地棒１４φ×１５００", 2, "箇所", 12_300)
s += it("接地極埋設標　接地抵抗測定共", 2, "箇所", 16_200)
s += it("削孔工事　壁貫通　機械はつり　φ５０（配管貫通口）", 16, "箇所", sig(10_200 * 1.15), "機械はつり 口径50 厚120〜150 10,200×1.15（元は手はつり 9,430）")
s += it("外灯移設工事　既設外灯 東へ約2.5m移設　撤去・基礎掘起し・基礎移設据付・再取付共", 1, "式", 180_000)
s += it("点検調査費　中部電気保安協会", 1, "式", 60_500)

ZATSU_R, KEIHI = 5.0, 15.0
z_raw = jsround(s * ZATSU_R / 100)
BASE = jsround((s + z_raw) / 10_000) * 10_000        # 小計＋雑費を1万円単位に（元の見積と同じ）
rows.append({"name": "雑費", "rate": ZATSU_R, "adj": BASE - s - z_raw})
k_amt = jsround(BASE * KEIHI / 100)
rows.append({"name": "諸経費", "expense": KEIHI, "adj": 0})   # 上記計（小計＋雑費）×15%
TOTAL = BASE + k_amt

data = {"header": {"name": "大藪小学校屋内運動場空調設備設置工事", "client": "株式会社大幸建築設計事務所", "honorific": "御中",
                   "date": "2026-10-14", "staff": "河口", "no": "261015"},   # Kの最新版のNo。見積日は作り直した日
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_大藪小_電気設備_K版261015.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/oyabu-denki-k261015.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_大藪小_電気設備_K版261015.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=oyabu-denki-k261015\n")

for r in rows:
    if "qty" in r: print(f"  {r['name'][:40]:42}{r['qty']:>5}{r['unit']:<3}{r['price']:>10,}{r['qty']*r['price']:>11,} {r['note']}")
print(f"小計 {s:,}／雑費 {BASE - s:,}（5%={z_raw:,}）／小計＋雑費 {BASE:,}／諸経費 {k_amt:,}／計（税抜）{TOTAL:,}／税込 {TOTAL + jsround(TOTAL*0.1):,}")
