# -*- coding: utf-8 -*-
"""ゆずりは浄心店　電気工事（株式会社廣瀬住建 御中）No.260605／R8.8.30版をベースに修正
   ご指示：動力配線を28,000円／換気扇取付 VD－10ZC14 を13,800円／
           税抜合計が1,000円単位になるよう諸経費で調整。誘導灯（配線・取付）は削除。
   運搬費はベースの65,470円を据え置き（ご指示がないため変更しない）。
   品名・仕様はベースの内訳どおり。
"""
import json, base64, math, os

def jsround(x): return math.floor(x + 0.5)
rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": ""})
    return qty * int(price)

T = {}
t = "幹線動力設備"; cat(t); s = 0
s += it("動力配線", "CV5.5-3C（室外機へ）", 1, "ケ所", 28_000)      # ご指示 18,000→28,000
s += it("消耗雑材費", "", 1, "式", 8_000)
T[t] = s

t = "電灯コンセント設備"; cat(t); s = 0
s += it("電灯配線", "", 37, "ケ所", 3_300)
s += it("換気配線", "", 4, "ケ所", 3_300)
s += it("調光配線", "", 16, "ケ所", 3_600)
s += it("スイッチ配線", "片切", 6, "ケ所", 4_800)
s += it("スイッチ配線", "3路", 2, "ケ所", 7_200)
s += it("スイッチ配線", "換気用", 4, "ケ所", 5_000)
s += it("スイッチ配線", "調光器　支給品", 2, "ケ所", 3_800)
s += it("コンセント配線", "2E", 22, "ケ所", 4_400)
s += it("コンセント配線", "2EET", 2, "ケ所", 4_500)
s += it("コンセント配線", "専用", 4, "ケ所", 11_800)
s += it("コンセント配線", "AC", 1, "ケ所", 11_800)
s += it("回路配線", "", 5, "ケ所", 4_800)
s += it("照明器具取付", "D1　支給品", 7, "台", 2_800)
s += it("照明器具取付", "D2　支給品", 29, "台", 2_800)
s += it("照明器具取付", "D3　支給品", 3, "台", 2_800)
s += it("照明器具取付", "D4　支給品", 1, "台", 2_800)
s += it("照明器具取付", "LB1　支給品", 4, "台", 3_000)
s += it("雑材消耗品費", "", 1, "式", 28_500)
T[t] = s

t = "空調設備"; cat(t); s = 0
s += it("パッケージエアコン取付", "天カセ4方向6馬力ワイヤード", 1, "台", 398_000)
s += it("ルームエアコン取付", "2.5kw（8畳用）スタンダード", 1, "台", 88_000)
s += it("冷媒配管", "", 1, "式", 140_000)
s += it("ドレン配管", "", 1, "式", 75_000)
s += it("室外機架台", "ベース", 1, "式", 16_000)
s += it("室内外連絡配線", "", 1, "式", 20_000)
s += it("貫通工事", "", 1, "式", 30_000)
s += it("室外機ルーバー", "パッケージ", 1, "式", 22_000)
s += it("室外機ルーバー", "ルーム", 1, "式", 16_000)
s += it("消耗雑材費", "", 1, "式", 41_000)
T[t] = s

t = "弱電,防災設備"; cat(t); s = 0
s += it("ケーブル配線", "LAN　cat6", 6, "ケ所", 14_000)
s += it("HDMI配線", "10m", 1, "ケ所", 18_000)
s += it("スピーカー配線", "AE1.2－2C", 4, "ケ所", 6_600)
s += it("電話配管", "PF22", 1, "ケ所", 16_000)
s += it("非常灯配線", "", 5, "ケ所", 6_300)
s += it("非常灯取付", "埋込　NNFB91605C", 5, "台", 22_000)
s += it("消耗雑材費", "", 1, "式", 16_500)
T[t] = s

t = "換気設備"; cat(t); s = 0
s += it("ストレ－トシロッコファン取付", "BFS－40SUG2", 1, "台", 71_000)
s += it("上記ダクト工事", "150φ～200φ", 1, "式", 83_000)
s += it("換気扇取付", "VD－10ZC14", 2, "台", 13_800)          # ご指示 11,800→13,800
s += it("上記ダクト工事", "100φ", 1, "式", 21_000)
s += it("排気口取付", "150φ", 4, "台", 4_600)
s += it("給気口取付", "150φ", 4, "台", 4_720)
s += it("ベントキャップ", "150φ", 1, "個", 6_200)
s += it("ベントキャップ", "200φ", 1, "個", 7_200)
s += it("外壁貫通工事", "吸排気ダクト", 1, "式", 98_000)
s += it("コントロールスイッチ取付", "", 1, "個", 8_500)
s += it("消耗雑材費", "", 1, "式", 18_220)
T[t] = s

# ---- 経費：運搬費はベース据え置き、諸経費で計（税抜）を1,000円単位に ----
sub = sum(T.values())
UNPAN_RATE, KEIHI_RATE = 3.0, 10.0
u_amt = 65_470                                     # ベースの運搬費を据え置き
k_raw = jsround((sub + u_amt) * KEIHI_RATE / 100)
TARGET = (sub + u_amt + k_raw) // 1000 * 1000      # 計（税抜）を1,000円単位（切捨て）
k_amt = TARGET - sub - u_amt
rows.append({"name": "運搬費", "rate": UNPAN_RATE, "adj": u_amt - jsround(sub * UNPAN_RATE / 100)})
rows.append({"name": "諸経費", "expense": KEIHI_RATE, "adj": k_amt - k_raw})

data = {"header": {"name": "ゆずりは浄心店　電気工事", "client": "株式会社廣瀬住建", "honorific": "御中",
                   "date": "2026-08-30", "staff": "河口", "no": "260605"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "",
        "taxMode": "out", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_ゆずりは浄心店_電気工事_R8830.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    if r.get("type") == "cat": print("\n【" + r["name"] + "】"); continue
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:34]:36}{r['qty']:>4}{r['unit']:<4}{r['price']:>9,}{r['qty']*r['price']:>11,}")
print()
for k, v in T.items(): print(f"{k:24}{v:>12,}")
tax = jsround(TARGET * 0.1)
print(f"{'小　計':24}{sub:>12,}\n{'運搬費':24}{u_amt:>12,}\n{'諸経費':24}{k_amt:>12,}")
print(f"{'計（税抜）':24}{TARGET:>12,}\n{'消費税10%':24}{tax:>12,}\n{'合　計':24}{TARGET+tax:>12,}")
assert TARGET % 1000 == 0
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
json.dump(data, open(root + "/q/yuzuriha.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(root + "/見積/取込リンク_ゆずりは浄心店_R8830.txt", "w").write(url + "\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=yuzuriha\n")
print("URL長", len(url))
