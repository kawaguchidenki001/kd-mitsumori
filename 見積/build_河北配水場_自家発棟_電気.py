# -*- coding: utf-8 -*-
"""河北配水場自家用発電機設備棟築造工事　電気設備工事（R8.10.30）
   資料：工事設計書（丹羽広域事務組合、改浄R0804）の「第AE-1号 建築電気工事 明細書」（数量はこのとおり）と
         「第AM-1号 建築機械工事」の 有圧換気扇 VE-1（科目別内訳書-1号）。図面 AE-10・AE-11・AE-13。
   Kの依頼：電気工事の見積、有圧扇も含む（→ 消音チャンバー（亜鉛鉄板・GW内貼り）は板金なので含めない）。
   単価：積算実務マニュアル2026（岐阜県）の複合単価。★は概算。
     ・LSS1-4-65 は マニュアルの 高効率形 LSS1H-4-65 LN（パナソニック XLX460NENP LE9 相当）。
     ・B14 センサー付ウォールライト（NNFS21811C LE9 相当）は 防湿防雨形 LBF3RP-2-13 の単価 ★。
     ・電灯分電盤 GL-1（主幹 MCCB 3P 50A、分岐 MCCB 2P 20A×1・ELCB 2P 20A×4）は マニュアルの 分電盤 6回路 121,000 に
       漏電遮断器分を足して ★。
     ・有圧換気扇 VE-1（400φ 低騒音形 単相100V、三菱 EWF-40DSA2 相当 定価 97,000）は 定価×0.7＋取付（設備機械工 0.58人）。
       付属品（SUS製ウェザーカバー FD・防鳥網付、取付枠・防護枠、電気シャッター）の定価は未確認のため ★概算。
   経費：法定福利費 16.5%（労務費は取付手間の約2/3、100円単位）、諸経費 12%、計を1,000円単位に（諸経費の adj）。
   宛名は未定（空欄）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, t=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if t: r["pl"] = jsround(t * 2 / 3)
    rows.append(r); return qty * int(price)

M = "積算マニュアル電気"
s = 0
cat("電灯設備")
s += it("電線", "EM-IE 2.0mm　管内", 247, "ｍ", 580, 468, f"{M}（設計書 246.5m）")
s += it("電線管", "E19　露出", 28, "ｍ", 2_490, 2_114, M)
s += it("電線管", "E25　露出", 31, "ｍ", 3_370, 2_835, M)
s += it("電線管", "E31　露出", 3, "ｍ", 4_350, 3_605, M)
s += it("露出ボックス", "角形 1個用 1方出　E19", 3, "個", 4_940, 4_224, M)
s += it("露出ボックス", "角形 1個用 2方出　E31", 1, "個", 5_910, 4_320, M)
s += it("丸形露出ボックス", "1方出　E19", 1, "個", 4_850, 4_215, M)
s += it("丸形露出ボックス", "2方出　E19", 3, "個", 4_940, 4_224, M)
s += it("丸形露出ボックス", "2方出　E25", 1, "個", 5_130, 4_243, M)
s += it("丸形露出ボックス", "3方出　E25", 6, "個", 5_220, 4_252, M)
s += it("露出スイッチボックス", "樹脂 1個用 1方出　HI22", 1, "個", 4_940, 4_224, "★角形1個用 E19 の単価")
s += it("プルボックス", "金属　200×200×200", 4, "個", 15_900, 12_784, M)
s += it("プルボックス", "金属　300×300×200", 1, "個", 22_200, 17_143, M)
s += it("プルボックス", "樹脂　200×200×200（屋外）", 1, "個", 16_000, 12_794, f"{M} 合成樹脂製防水形")
s += it("LED照明器具", "LSS1-4-65（A65）", 7, "台", 29_100, 9_528, f"{M} LSS1H-4-65")
s += it("LED照明器具", "1470lm センサー機能付 防湿・防雨形（B14）", 1, "台", 33_800, 7_714, "★LBF3RP-2-13 の単価")
s += it("LED誘導灯", "SH1-FBF20-C（C20）", 1, "台", 22_800, 8_761, M)
s += it("スイッチ", "1P15A×3　金属プレート", 1, "個", 5_170, 4_546, M)
s += it("コンセント", "2P15A 接地極付×2　金属プレート", 2, "個", 3_710, 2_869, M)
s += it("コンセント", "2P15A 抜止形 ET×1　金属プレート", 1, "個", 3_570, 2_856, M)
s += it("電灯分電盤", "GL-1　壁掛形 鋼板製", 1, "面", 145_000, 38_000, "★分電盤6回路121,000＋ELCB分")
s += it("ボンディング", "E19", 5, "個", 230, 209, M)
s += it("ボンディング", "E25", 13, "個", 230, 210, M)
s += it("ボンディング", "E31", 1, "個", 280, 252, M)

# ---- 有圧換気扇 VE-1：定価×0.7＋取付 ----
KAKE = 0.7
FAN_TORI = sig(29_000 * 0.58 * 1.25)            # 設備機械工 0.58人（設計書 第1号代価表）＋その他25%
cat("換気設備")
s += it("有圧換気扇　VE-1", "400φ 低騒音形 単相100V", 1, "台", sig(97_000 * KAKE) + FAN_TORI, FAN_TORI,
        f"三菱 EWF-40DSA2 相当 定価97,000×0.7＋取付{FAN_TORI:,}")
s += it("SUS製ウェザーカバー", "防火ダンパー・防鳥網付（400φ用）", 1, "個", sig(95_000 * KAKE + 6_000), 6_000, "★定価 約95,000×0.7＋取付")
s += it("防護枠・取付枠", "400φ用", 1, "個", sig(21_000 * KAKE), 0, "★定価 約21,000×0.7")
s += it("電気シャッター", "400φ用", 1, "個", sig(45_000 * KAKE + 3_000), 3_000, "★定価 約45,000×0.7＋結線")

labor = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
k_raw = jsround(s * KEIHI / 100)
TOTAL = (s + w_amt + k_raw) // 1000 * 1000
cat("経　費")
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": TOTAL - s - w_amt - k_raw})

data = {"header": {"name": "河北配水場自家用発電機設備棟築造工事　電気設備工事", "client": "", "honorific": "御中",
                   "date": "2026-10-30", "staff": "河口", "no": ""},
        "place": "大口町河北二丁目地内", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_河北配水場_自家発棟_電気.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/kahoku-jikahatsu.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_河北配水場_自家発棟_電気.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=kahoku-jikahatsu\n")
sub, cur = {}, None
for r in rows:
    if r.get("type") == "cat": cur = r["name"]; print("【" + cur + "】"); continue
    if "qty" in r:
        a = r["qty"] * r["price"]; sub[cur] = sub.get(cur, 0) + a
        print(f"  {(r['name']+' '+r['spec'])[:38]:40}{r['qty']:>4}{r['unit']:<2}{r['price']:>9,}{a:>10,}  {r['note']}")
for k, v in sub.items(): print(f"{k} 計 {v:,}")
print(f"小計 {s:,}／法定福利費 {w_amt:,}（労務費 {labor:,}）／諸経費 {TOTAL - s - w_amt:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}")
