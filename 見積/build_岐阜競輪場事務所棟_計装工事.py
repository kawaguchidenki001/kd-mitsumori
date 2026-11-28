# -*- coding: utf-8 -*-
"""岐阜競輪場事務所棟建築機械設備工事のうち 計装工事　R8.11.28
   Kの指示：計装工事の見積。内訳で不足しているものは追加する。
   資料（スキャンPDF 7枚）：設計内訳 (8) 1-5 自動制御設備、(20) 機別紙 P9・P10（P11 給水保温は赤×で対象外）、
     図面 401〜403 機械設備工事特記仕様書、409 自動制御設備 平面図、407 空調設備 機器表・平面図・立面図。
     工事場所 岐阜県岐阜市東栄町5丁目16番地1（特記仕様書）、事務所棟 S造1階建 123.12㎡。
   内訳のとおり（品名・摘要・数量）：
     制御用ケーブル EM-CEE1.25sq-2C 管内16m・天井内57m／厚鋼電線管 GLT22mm 露出14m／1種金属線ぴ A形2m／
     プルボックス SS200×200×100 WP-SUS 2個／コーナーボックス A形1個／スイッチボックス A形 2個用1個／
     防火区画貫通処理 1式（金属管用19φ 1か所）／はつり補修費 1式（ダイヤモンドカッター 50mm×100〜150mm 1か所）
   追加（内訳に無いもの）：
     ・集中リモコン取付（SRS-1：機器表の集中リモコン ON/OFFコントローラー 16グループ。平面図の凡例で「付属品」＝機器と一緒に支給）
     ・支持材（屋外露出の厚鋼電線管：ハードケース置場の屋根上・開放廊下の屋根下）★概算
     ・試運転調整費（集中リモコンのグループ設定・動作確認）0.5人工 ★
     ・雑材消耗品（小計を1万円単位にする端数調整。Kの標準）、法定福利費 16.5%（100円単位切捨て）、諸経費 12%（計を1,000円単位に）
   単価：積算単価DB（tanka-search unit_prices.json）の複合単価。★は概算。
     GLT22 露出 → GP-22 溶融亜鉛めっき 露出 4,840 で代用／コーナーボックス A形 → 線ぴ用ボックス 直角2方出 5,460 で代用
   付記：集中リモコンの電源（1φ100V、機器表）は電気工事（別途）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v); step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

rows = []
def it(name, spec, qty, unit, price, labor, note=""):
    """price：複合単価、labor：その単価のうち労務費（DB の labor_cost。法定福利費の計算に使う）"""
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note, "pl": int(labor)})
    return qty * int(price)

s = 0
# ── 内訳のとおり
s += it("制御用ケーブル", "EM-CEE 1.25sq-2C　管内", 16, "ｍ", 810, 423, "DB EM-CEE1.25-2C 管内")
s += it("制御用ケーブル", "EM-CEE 1.25sq-2C　天井内", 57, "ｍ", 690, 338, "DB EM-CEE1.25-2C 二重天井内")
s += it("厚鋼電線管", "GLT 22mm　露出", 14, "ｍ", 4_840, 2_707, "単価: DB GP-22 溶融亜鉛めっき 露出で代用")
s += it("1種金属線ぴ", "A形", 2, "ｍ", 3_680, 1_974, "DB 1種金属線ぴ A型")
s += it("プルボックス", "SS 200×200×100　WP-SUS", 2, "個", 21_100, 7_050, "DB SS200×200×100 WP-SUS")
s += it("コーナーボックス", "A形", 1, "個", 5_460, 2_820, "単価: DB 線ぴ用ボックス 直角2方出 30 で代用")
s += it("スイッチボックス", "A形　2個用", 1, "個", 5_380, 2_820, "DB 線ぴ用スイッチボックス 2個用 浅形")
s += it("防火区画貫通処理", "金属管用 19φ　1か所", 1, "式", 1_130, 620, "機別紙 P9。DB 防火区画貫通処理 金属管用 19")
s += it("はつり補修費", "ダイヤモンドカッター 50mm×100～150mm　1か所", 1, "式", 10_200, 6_912,
        "機別紙 P10。DB 機械はつり（ダイヤモンドカッター）口径50mm 厚さ120〜150mm")
# ── 追加（内訳に無いもの）
NIN = 28_200 * 1.4                                     # 39,480
s += it("集中リモコン取付", "SRS-1（機器付属品）　結線共", 1, "台", 6_000, 4_000, "★機器表 SRS-1 ON/OFFコントローラー 16グループ（支給品の取付・結線）")
s += it("支持材", "屋根上・開放廊下屋根下", 1, "式", 8_000, 4_000, "★概算（屋外露出の厚鋼電線管）")
SHI = sig(NIN * 0.5)
s += it("試運転調整費", "集中リモコン設定・動作確認", 1, "式", SHI, jsround(SHI * 2 / 3), "★0.5人工（39,480/人工）")
others = s
SUB = int(others * 1.03) // 10_000 * 10_000            # Kの標準：雑材以外×1.03 を1万円単位に切り捨て
ZAI = SUB - others
rows.append({"name": "雑材消耗品", "spec": "", "qty": 1, "unit": "式", "price": ZAI, "note": "小計を1万円単位にする端数調整（Kの標準）", "pl": 0})
s += ZAI
assert s == SUB

labor = sum(r["qty"] * r["pl"] for r in rows)
w_raw = jsround(labor * 16.5 / 100); W_AMT = w_raw // 100 * 100
k_raw = jsround(SUB * 12 / 100)
TOTAL = (SUB + W_AMT + k_raw) // 1000 * 1000
K_AMT = TOTAL - SUB - W_AMT
rows.append({"name": "法定福利費", "welfare": 16.5, "adj": W_AMT - w_raw})
rows.append({"name": "諸経費", "rate": 12.0, "adj": K_AMT - k_raw})

data = {"header": {"name": "岐阜競輪場事務所棟建築機械設備工事のうち 計装工事",
                   "client": "", "honorific": "御中", "date": "2026-11-28", "staff": "河口", "no": ""},
        "place": "岐阜競輪場 事務所棟", "validity": "発行日より1ヶ月", "remarks": "",
        "notes": ["集中リモコンは空調機の付属品（支給品）です",
                  "集中リモコンの電源（1φ100V）は電気工事（別途）です"],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
fname = "岐阜競輪場事務所棟_計装工事"; qname = "keirin-jimusho-keiso"
json.dump(data, open(f"{root}/見積/見積_{fname}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(f"{root}/q/{qname}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(f"{root}/見積/取込リンク_{fname}.txt", "w").write(url + f"\nhttps://kd-mitsumori.pages.dev/#q={qname}\n")
for r in rows:
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:38]:40}{r['qty']:>3}{r['unit']}{r['price']:>8,}{r['qty']*r['price']:>9,}  pl{r['pl']:>6}  {r['note']}")
print(f"小計 {SUB:,}／法定福利費 {W_AMT:,}（労務費 {labor:,}×16.5%={w_raw:,}）／諸経費 {K_AMT:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}")
