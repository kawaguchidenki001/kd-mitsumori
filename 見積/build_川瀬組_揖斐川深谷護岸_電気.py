# -*- coding: utf-8 -*-
"""令和８年度 揖斐川深谷護岸整備工事　樋管上屋 電気設備工事（株式会社川瀬組 御中）R8.11.11
   資料：数量書（suuryousyo.xls：電気設備工事 細目別内訳 30〜32）、別紙明細（besshimeisai.xls：別紙 00-0009〜0020）、
         図面 49/49「電灯設備図、換気設備図」（照明器具姿図・分電盤結線図）、48/49 特記仕様書（電気設備の部）。
   範囲：樋管上屋の電灯設備（電灯幹線・電灯分岐・コンセント分岐）。数量は数量書・別紙明細のとおり。
         換気設備（有圧換気扇 FE-1・温度スイッチ・搬入据付）は機械設備工事なので含めない。電源切替分電盤は別途工事（図面）。
   単価：積算実務マニュアル2026（岐阜県）の複合単価。★は概算。
     ・A402 反射笠付 LED5100lm 線ぴ取付：LSS7-4-56 の単価 ★、B402 同 非常用（電池内蔵）：K1-LSS1-4-48 の単価 ★
     ・C201 ウォールライト（防水形）LBF3MP/RP-2-06、D201 投光器 LPJ1W-180（壁掛形）
     ・分電盤 L-1（屋内鋼板製壁掛型、主幹 MCCB 2P 50/30、ELCB 2P 50/20×5＋予備）：分電盤6回路 121,000 に ELCB 分 ★
     ・E39・G16（塗装）・熱線センサー（壁付 防水形）・タンブラスイッチ 1P15A×2 は ★概算
   経費：法定福利費 16.5%（労務費は取付手間の約2/3、100円単位）、諸経費 12%、計を1,000円単位に（諸経費の adj）。
   R8.11.12 Kの指示：見直し（照明器具・分電盤を材料見積を考慮した金額に）。見積No 261107（アプリの採番）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, t=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if t: r["pl"] = jsround(t * 2 / 3)
    rows.append(r); return qty * int(price)

M = "積算マニュアル"
s = 0
cat("電灯幹線")
# R8.11.12 Kの指示：見直し → 照明器具・分電盤は材料見積（富永電機 R8.11.12）を考慮：材料（MAT、仕入に粗利2割）＋取付手間（積算マニュアル）
def sig(v):
    import math as _m
    v = float(v); step = max(10, 10 ** (int(_m.floor(_m.log10(v))) + 1 - 3))
    return int(_m.floor(v / step + 0.5)) * step
MAT = {"L1": 200_000, "A402": 9_340, "B402": 29_800, "C201": 13_900, "D201": 82_100}
TOMI = "材料見積（R8.11.12）を考慮＋取付"
s += it("電灯分電盤", "L-1　屋内鋼板製壁掛型", 1, "面", sig(MAT["L1"] + 72_877), 72_877, TOMI)
s += it("電線", "EM-IE 2.0mm　管内", 18, "ｍ", 580, 468, M)
s += it("ケーブル", "EM-CE 8mm2-2C　ピット内", 16, "ｍ", 1_520, 838, M)
s += it("ケーブル", "EM-CE 8mm2-2C　管内", 2, "ｍ", 1_680, 1_026, M)
s += it("電線管", "E31　露出", 2, "ｍ", 4_350, 3_605, M)

cat("電灯分岐")
s += it("照明器具", "A402　反射笠付 LED5100lm 線ぴ取付", 10, "台", sig(MAT["A402"] + 12_032), 12_032, TOMI)
s += it("照明器具", "B402　反射笠付 非常用 電池内蔵 LED5100lm", 2, "台", sig(MAT["B402"] + 12_253), 12_253, TOMI)
s += it("照明器具", "C201　ウォールライト 防水形 LBF3MP/RP-2-06", 1, "台", sig(MAT["C201"] + 7_402), 7_402, TOMI)
s += it("照明器具", "D201　投光器 LPJ1W-180 壁掛形", 2, "台", sig(MAT["D201"] + 74_525), 74_525, TOMI)
s += it("タンブラスイッチ", "1P15A×2　金属プレート", 1, "個", 4_500, 3_900, "★")
s += it("熱線式自動スイッチ用センサー", "壁付 防水形", 1, "個", 25_000, 6_000, "★")
s += it("防雨入線カバー", "", 2, "個", 1_300, 838, M)
s += it("ケーブル", "EM-EEF 2.0mm-2C　管内", 46, "ｍ", 960, 730, M)
s += it("ケーブル", "EM-EEF 2.0mm-3C　管内", 43, "ｍ", 1_220, 905, M)
s += it("電線管", "E25　露出", 19, "ｍ", 3_370, 2_835, M)
s += it("電線管", "E31　露出", 4, "ｍ", 4_350, 3_605, M)
s += it("電線管", "E39　露出", 5, "ｍ", 5_400, 4_400, "★")
s += it("電線管", "G16　露出（塗装有）", 2, "ｍ", 3_300, 2_700, "★")
s += it("2種金属線ぴ", "MM2　A型 40×30", 34, "ｍ", 4_400, 3_797, M)
s += it("ジャンクションボックス", "MM2用", 2, "個", 5_590, 4_289, M)
s += it("露出ボックス", "", 5, "個", 4_940, 4_224, M)
s += it("プルボックス", "SS 300×300×200　錆止め・塗装有", 3, "個", 22_200, 17_143, f"{M}（数量書 1.26㎡）")
s += it("接地端子", "プルボックス用 ET", 3, "個", 2_660, 2_280, M)

cat("コンセント分岐")
s += it("コンセント", "2P15A×1 接地極付　金属プレート", 1, "個", 3_600, 2_859, M)
s += it("コンセント", "2P15A×2 接地極付　金属プレート", 2, "個", 3_710, 2_869, M)
s += it("ケーブル", "EM-EEF 2.0mm-3C　管内", 38, "ｍ", 1_220, 905, M)
s += it("電線管", "E25　露出", 30, "ｍ", 3_370, 2_835, M)
s += it("電線管", "E39　露出", 4, "ｍ", 5_400, 4_400, "★")
s += it("露出ボックス", "", 6, "個", 4_940, 4_224, M)

labor = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
k_raw = jsround(s * KEIHI / 100)
TOTAL = (s + w_amt + k_raw) // 1000 * 1000
cat("経　費")
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": TOTAL - s - w_amt - k_raw})

data = {"header": {"name": "令和８年度　揖斐川深谷護岸整備工事　樋管上屋　電気設備工事", "client": "株式会社川瀬組", "honorific": "御中",
                   "date": "2026-11-12", "staff": "河口", "no": "261107"},
        "place": "三重県桑名市大字下深谷部字外田地先", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_川瀬組_揖斐川深谷護岸_電気.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/ibigawa-fukaya-denki.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_川瀬組_揖斐川深谷護岸_電気.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=ibigawa-fukaya-denki\n")
sub, cur = {}, None
for r in rows:
    if r.get("type") == "cat": cur = r["name"]; print("【" + cur + "】"); continue
    if "qty" in r:
        a = r["qty"] * r["price"]; sub[cur] = sub.get(cur, 0) + a
        print(f"  {(r['name']+' '+r['spec'])[:34]:36}{r['qty']:>4}{r['unit']}{r['price']:>9,}{a:>10,}  {r['note']}")
for k, v in sub.items(): print(f"{k} 計 {v:,}")
print(f"小計 {s:,}／法定福利費 {w_amt:,}（労務費 {labor:,}）／諸経費 {TOTAL - s - w_amt:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}")
