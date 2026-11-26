# -*- coding: utf-8 -*-
"""岐阜(6)空調改修等機械工事のうち 電線・配管撤去及びリモコン再取付工事（戸島工業株式会社 御中）R8.11.26
   Kの指示：図面（3枚）の赤枠を見積。過去の見積 No.260912（R8.9.14「岐阜(6)空調改修等機械工事のうち 計装工事」計 735,000）を参考に。
   図面の赤枠と書き込み：
     1枚目 MD-（教場A 暖房設備 1階・2階平面図（撤去））1階 機械室：「機械室内電線・配管撤去 20m程度」
     2枚目 MD-30（教場A 空調設備 3階・R階平面図（撤去））R階 室外機：「既設室外機廻り電線・配管撤去 30m程度」
     3枚目（岐阜(5) 隊舎B 自動制御設備 2階・3階平面図（改修））2階 リモコン 2ケ所：「空調・ロスナイリモコン撤去 再取付 ※軽量内配管は電気工事」
       ★3枚目は 岐阜(5) の図面。見積は 岐阜(6) 教場A として1件にまとめた（Kに確認）。
   書き方は過去の見積のとおり：明細 → 雑材消耗品 → 小計 → 法定福利費 → 諸経費（1枚）。
   単価：積算単価DB（tanka-search unit_prices.json）の撤去費。
     電線・配管撤去 1ｍ＝電線管 GP-22 露出 撤去 800＋ケーブル CV5.5-3C 相当 撤去 200＋制御ケーブル CVV2-2C 撤去 140 → 1,140
     リモコン撤去・再取付 1ケ所（空調＋ロスナイの2個）＝（再取付 4,500［過去の見積のリモコン取付］＋撤去 670［DB リモコンスイッチ撤去］）×2
     ★撤去品処分費は概算 1式 10,000
   雑材消耗品：雑材以外×1.03 を 1万円単位に切り捨てた額を小計にする（Kの標準）。法定福利費＝労務費×16.5%（100円単位切捨て）、
   諸経費 12%、計は 1,000円単位に切り捨て（諸経費の adj）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v); step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

rows = []
def it(name, qty, unit, price, note="", lab=2/3):
    rows.append({"name": name, "spec": "", "qty": qty, "unit": unit, "price": int(price), "note": note,
                 "pl": jsround(int(price) * lab)})
    return qty * int(price)

TEKKYO_M = sig(800 + 200 + 140)
RC = sig((4_500 + 670) * 2)
s = 0
s += it("既設電線・配管撤去　機械室内", 20, "ｍ", TEKKYO_M, "図面の書き込み「20m程度」。GP-22撤去800＋CV5.5-3C相当200＋CVV2-2C相当140（DB 撤去費）")
s += it("既設電線・配管撤去　室外機廻り（屋上）", 30, "ｍ", TEKKYO_M, "図面の書き込み「30m程度」。同上")
s += it("空調・ロスナイリモコン撤去・再取付　結線・動作確認共", 2, "ケ所", RC,
        "（取付4,500［No.260912］＋撤去670［DB］）×2個（空調・ロスナイ）")
s += it("撤去品処分費", 1, "式", 10_000, "★概算", lab=0)
others = s
SUB = int(others * 1.03) // 10_000 * 10_000          # Kの標準：雑材以外×1.03 を1万円単位に切り捨て
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

data = {"header": {"name": "岐阜(6)空調改修等機械工事のうち 電線・配管撤去及びリモコン再取付工事",
                   "client": "戸島工業株式会社", "honorific": "御中", "date": "2026-11-26", "staff": "河口", "no": ""},
        "place": "航空自衛隊岐阜基地 教場A(教育講堂)", "validity": "発行日より1ヶ月", "remarks": "",
        "notes": ["軽量内配管は電気工事（別途）です"],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
fname = "戸島工業_岐阜6_電線配管撤去リモコン再取付"; qname = "gifu6-tekkyo-rc"
json.dump(data, open(f"{root}/見積/見積_{fname}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(f"{root}/q/{qname}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(f"{root}/見積/取込リンク_{fname}.txt", "w").write(url + f"\nhttps://kd-mitsumori.pages.dev/#q={qname}\n")
for r in rows:
    if "qty" in r: print(f"  {r['name'][:30]:32}{r['qty']:>3}{r['unit']}{r['price']:>8,}{r['qty']*r['price']:>9,}  pl{r['pl']:>6}  {r['note']}")
print(f"小計 {SUB:,}／法定福利費 {W_AMT:,}（労務費 {labor:,}×16.5%={w_raw:,}）／諸経費 {K_AMT:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}")
