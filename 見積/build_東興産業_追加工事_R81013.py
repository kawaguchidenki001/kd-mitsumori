# -*- coding: utf-8 -*-
"""東興産業株式会社　追加工事（R8.10.13）　①コンプレッサー電源配線 ②照明器具配線工事 ③フォークリフト電源配線 を1枚の見積に
   参考：当社見積 No.260507（R8.5.8 LED照明器具取付工事）・No.260508（R8.5.8 クレーン電源配線工事）の品名と単価。
   ① AIRMAN SAS8VD-C（インバータ 7.5kW 三相200V、大東通商 見積 No.144023）。
      内線規程の三相200V電動機 7.5kW（全負荷電流 約34A）→ CV8sq-4C（E共）、インバータ（始動器使用扱い）で 3P 50A。
   ③ 30A 動力コンセントは支給品（取付手間のみ）。電源は既設盤の空き回路からとし、ブレーカーは見ていない。
   参考見積どおり法定福利費なし、諸経費10%。端数は雑費で調整（Kの標準）。
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
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return int(round(qty * int(price)))

CV8 = 2_340                              # No.260508 の CV8sq-4C（tankatool 管内 2,600 の0.9倍）
CV55 = sig(2_060 * CV8 / 2_600)          # CV5.5sq-4C：tankatool 管内 2,060 に同じ比率 → 1,850
# ★iD 40形 直付Dスタイル W230 5200lm 昼白色 XFX450DEN LE9（定価33,600）：仕入を定価の40%と仮定×1.2＋取付3,500＋支持材2,000
LED = sig(33_600 * 0.40 * 1.2 + 3_500 + 2_000)
OUTLET = sig(8_850 - 1_450)              # 露出コンセント 3P30A 接地極付 8,850 から材料1,450を除いた取付手間（支給品）

s = 0
cat("01　コンプレッサー電源配線")
s += it("ケーブル配線", "ＣＶ８sq－４Ｃ", 5, "ｍ", CV8, 987)
s += it("ケースブレーカー取付", "３Ｐ３Ｅ５０Ａ", 1, "台", 28_400, 15_736, "No.260508 ブレーカー取替 3P3E50A 表面形と同額")
cat("02　照明器具配線工事")
s += it("ＬＥＤ照明器具取付", "ｉＤシリーズ Ｄスタイル ５２００ｌｍ 昼白色 支持材含む", 6, "台", LED, 5_500, "★XFX450DEN LE9 定価33,600×0.4×1.2＋取付3,500＋支持材2,000")
s += it("電灯配線", "露出", 6, "ケ所", 7_500, 3_500, "No.260507")
s += it("スイッチ配線", "片切 露出 ＶＥ管立下げ・ボックス含む", 3, "ケ所", 18_500, 8_000, "No.260507（配管はスイッチの立下げのみ）")
s += it("回路配線", "露出", 1, "ケ所", 16_000, 7_000, "No.260507")
cat("03　フォークリフト電源配線")
s += it("ケーブル配線", "ＣＶ５．５sq－４Ｃ", 10, "ｍ", CV55, 846)
s += it("動力コンセント取付", "３Ｐ３０Ａ 接地極付（支給品）", 1, "個", OUTLET, 4_907, "露出コンセント 3P30A 接地極付の取付手間")

KEIHI = 10.0
SUB = int(s * 1.03) // 10_000 * 10_000   # 雑費は3%程度、小計を1万円単位に
cat("雑　費")                            # 鑑に「雑費 1式」と出す
ZATSU = SUB - s
s += it("雑費", "", 1, "式", ZATSU, 0)
rows.append({"name": "諸経費", "rate": KEIHI, "adj": 0})
TARGET = s + jsround(s * KEIHI / 100)

data = {"header": {"name": "コンプレッサー電源配線工事 他（追加工事）", "client": "東興産業株式会社", "honorific": "御中",
                   "date": "2026-10-13", "staff": "河口", "no": ""},   # 新規なので見積Noは保存時にアプリが採番
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_東興産業_追加工事_R81013.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/toukou-tsuika.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_東興産業_追加工事_R81013.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=toukou-tsuika\n")

for r in rows:
    if r.get("type") == "cat": print("【" + r["name"] + "】"); continue
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:40]:42}{r['qty']:>4}{r['unit']:<3}{r['price']:>9,}{int(round(r['qty']*r['price'])):>10,} {r['note']}")
print(f"小計 {s:,}（雑費 {ZATSU:,}）／諸経費 {TARGET - s:,}／計（税抜）{TARGET:,}／税込 {TARGET + jsround(TARGET*0.1):,}")
