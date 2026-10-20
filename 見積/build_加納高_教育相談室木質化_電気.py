# -*- coding: utf-8 -*-
"""永井建設株式会社　加納高等学校北舎1階教育相談室床壁木質化工事　電気設備工事（R8.10.14）
   元資料：設計書「直接工事費 細目別内訳（電気設備工事）」の7項目と、展開図（1階相談室）。
     ・2口コンセント新設 3（展開図1西・1東・3東）。木質化部分（床からH=1,100）は壁裏配線（特記）
     ・既設2口コンセント 撤去復旧 3（展開図2・3西・4）、有線LANポート 撤去復旧 1（展開図3東）
     ・床既設TEL 一時撤去・ボックスレベル調整・再取付 1（床の杉圧縮フローリング新設で床が上がるため）
     ・既設カバープレート 一時撤去・再取付 1
   品名・数量は細目別内訳のとおり。単価は複合単価（電気設備工事積算実務マニュアル2026 岐阜県）から積み上げ。★は概算。
   新設コンセントの電源は近くの既設コンセントから送り（VVF2.0-2C 1箇所6m と仮定）。
   既設の機器は羽目板（胴縁16＋板12mm）の分だけ前に出すため、ボックス継枠を付けて再取付する。
   法定福利費16.5%（100円単位）、諸経費12%で計を1,000円単位に端数調整。用紙1枚（分類行なし）。
   R8.10.20 Kの指示：単価を全て2倍に（労務費も2倍）、諸経費は全体（小計＋法定福利費＝上記計）の15%に。見積No 261019（アプリの採番）。
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

UP = 2   # R8.10.20 Kの指示：単価を全て2倍
rows = []
def it(name, spec, qty, unit, price, pl=0, note=""):
    price = int(price) * UP; pl = pl * UP
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return int(round(qty * int(price)))

KEI = 0.40                       # 経費率（手間に対する経費の目安：複合単価の 経費÷(材料費＋労務費) ≒ 0.4）
VVF_M = 3 * 6                    # 新設コンセント3箇所 × 6m
# 配線・配管材費：VVF2.0-2C 材料費 172/m、スイッチボックス1個用（塗代付）材料 約800×3、ボックス継枠 約400×5（既設コンセント3・LAN1・カバー1）、小物
MAT = sig(VVF_M * 172 + 3 * 800 + 5 * 400 + 1_000)
# 配線配管工事費：VVF2.0-2C 管内の労務 479/m、ボックス取付 2,820×3（壁裏・羽目板開口）に経費
LAB = VVF_M * 479 + 3 * 2_820
WORK = sig(LAB * (1 + KEI))
# 一時撤去・再取付：撤去費（removal_cost）＋取付手間（複合単価−材料）＋継枠取付 約800
def reinstall(comp, mat, rm): return sig(rm + (comp - mat) + 800)
OUT_RE = reinstall(2_830, 520, 670)      # 埋込コンセント 2P15A×2 金属プレート
LAN_RE = reinstall(4_000, 1_080, 830)    # モジュラージャック CAT6 1個口
PLT_RE = reinstall(1_140, 310, 240)      # ブランクプレート 金属製
# ★床TEL：フロアプレート（丸）自在型 新品 5,370＋既設撤去 1,080＋ボックスのレベル調整（嵩上げ）0.3人工 28,200×0.3×1.4
TEL = sig(5_370 + 1_080 + 28_200 * 0.3 * 1.4)

s = 0
s += it("配線・配管材費", "", 1, "式", MAT, 0, "VVF2.0-2C 18m・ボックス3・継枠5・小物")
s += it("配線配管工事費", "", 1, "式", WORK, LAB, "VVF2.0-2C 18m 壁裏配線・ボックス取付3")
s += it("既設コンセント", "機器再使用 一時撤去・再取付", 3, "箇所", OUT_RE, 670 + 1_523 + 800, "撤去670＋取付手間＋継枠")
s += it("新設コンセント", "２Ｐ１５Ａ×２ 新金属プレート", 3, "箇所", 2_830, 1_523, "埋込形コンセント 2P15A×2 金属製プレート共")
s += it("既設ＬＡＮ", "機器再使用 一時撤去・再取付", 1, "箇所", LAN_RE, 830 + 1_889 + 800, "撤去830＋取付手間＋継枠")
s += it("床既設ＴＥＬ", "機器新品 一時撤去・ボックスレベル調整・再取付", 1, "箇所", TEL, 1_080 + 2_453 + 8_460, "★フロアプレート自在型＋レベル調整0.3人工")
s += it("既設カバープレート", "機器再使用 一時撤去・再取付", 1, "箇所", PLT_RE, 240 + 536 + 800, "撤去240＋取付手間＋継枠")

labor = sum(r["qty"] * r.get("pl", 0) for r in rows)
WELFARE, KEIHI = 16.5, 15.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
k_raw = jsround((s + w_amt) * KEIHI / 100)         # 諸経費＝上記計（小計＋法定福利費）×15%
TARGET = (s + w_amt + k_raw + 500) // 1000 * 1000
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "expense": KEIHI, "adj": (TARGET - s - w_amt) - k_raw})

data = {"header": {"name": "加納高等学校北舎1階教育相談室床壁木質化工事　電気設備工事", "client": "永井建設株式会社", "honorific": "御中",
                   "date": "2026-10-20", "staff": "河口", "no": "261019"},   # R8.10.14 にアプリが採番した No
        "place": "岐阜市加納南陽町 地内", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_加納高_教育相談室木質化_電気.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/kano-soudanshitsu.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_加納高_教育相談室木質化_電気.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=kano-soudanshitsu\n")

for r in rows:
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:34]:36}{r['qty']:>3}{r['unit']:<3}{r['price']:>8,}{r['qty']*r['price']:>9,} {r['note']}")
print(f"小計 {s:,}／法定福利費 {w_amt:,}（労務費{labor:,}）／諸経費 {TARGET - s - w_amt:,}（15%={k_raw:,}）／計（税抜）{TARGET:,}／税込 {TARGET + jsround(TARGET*0.1):,}")
