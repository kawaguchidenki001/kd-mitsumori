# -*- coding: utf-8 -*-
"""ゆずりは浄心店　電気工事（株式会社廣瀬住建 御中）
   R8.6.5 発行の紙見積（No.260605・鑑＋内訳明細5葉）をそのままKD見積へ置き換え。
   金額は一切変更していない。日付のみご指示により令和8年8月30日へ。
"""
import json, base64, os, math

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, lr=0.0):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": ""}
    if lr: r["pl"] = int(round(price * lr))
    rows.append(r)
    return qty * int(price)

T = {}
t = "幹線動力設備"; cat(t); s = 0
s += it("電灯幹線",   "CVT14sq",           1, "ケ所",  53_000, 0.45)
s += it("動力幹線",   "CVT22sq",           1, "ケ所",  65_000, 0.45)
s += it("動力配線",   "CV5.5-3C（室外機へ）", 1, "ケ所",  14_000, 0.55)
s += it("ア－ス配線",  "IV5.5sq",           1, "ケ所",   8_000, 0.60)
s += it("分電盤取付",  "電灯動力混合",         1, "面",  140_000, 0.20)
s += it("消耗雑材費",  "",                  1, "式",   14_000)
T[t] = s

t = "電灯コンセント設備"; cat(t); s = 0
s += it("電灯配線",     "",                37, "ケ所",  3_300, 0.75)
s += it("換気配線",     "",                 4, "ケ所",  3_300, 0.75)
s += it("調光配線",     "",                16, "ケ所",  3_600, 0.75)
s += it("スイッチ配線",  "片切",              6, "ケ所",  4_800, 0.60)
s += it("スイッチ配線",  "3路",              2, "ケ所",  7_200, 0.60)
s += it("スイッチ配線",  "換気用",            4, "ケ所",  5_000, 0.60)
s += it("スイッチ配線",  "調光器　支給品",      2, "ケ所",  3_800, 0.90)
s += it("コンセント配線", "2E",              22, "ケ所",  4_400, 0.60)
s += it("コンセント配線", "2EET",             2, "ケ所",  4_500, 0.60)
s += it("コンセント配線", "専用",              4, "ケ所", 11_800, 0.65)
s += it("コンセント配線", "AC",               1, "ケ所", 11_800, 0.65)
s += it("回路配線",     "",                 5, "ケ所",  4_800, 0.70)
s += it("照明器具取付",  "D1　支給品",         7, "台",   2_800, 0.90)
s += it("照明器具取付",  "D2　支給品",        29, "台",   2_800, 0.90)
s += it("照明器具取付",  "D3　支給品",         3, "台",   2_800, 0.90)
s += it("照明器具取付",  "D4　支給品",         1, "台",   2_800, 0.90)
s += it("照明器具取付",  "LB1　支給品",        4, "台",   3_000, 0.90)
s += it("雑材消耗品費",  "",                 1, "式",  28_500)
T[t] = s

t = "空調設備"; cat(t); s = 0
s += it("パッケージエアコン取付", "天カセ4方向6馬力ワイヤード",        1, "台", 398_000, 0.30)
s += it("ルームエアコン取付",   "2.5kw（8畳用）スタンダード",       1, "台",  88_000, 0.30)
s += it("冷媒配管",          "",                            1, "式", 140_000, 0.50)
s += it("ドレン配管",         "",                            1, "式",  75_000, 0.50)
s += it("室外機架台",         "壁掛",                         1, "式",  67_000, 0.35)
s += it("室内外連絡配線",      "",                            1, "式",  20_000, 0.60)
s += it("外壁貫通工事",       "",                            1, "式",  48_000, 0.70)
s += it("高所作業車費",       "",                            1, "式",  35_000)
s += it("消耗雑材費",        "",                            1, "式",  43_000)
T[t] = s

t = "弱電,防災設備"; cat(t); s = 0
s += it("ケーブル配線",  "LAN　cat6",        6, "ケ所", 14_000, 0.60)
s += it("HDMI配線",    "10m",             1, "ケ所", 18_000, 0.50)
s += it("スピーカー配線", "AE1.2－2C",        4, "ケ所",  6_600, 0.65)
s += it("電話配管",     "PF22",            1, "ケ所", 16_000, 0.65)
s += it("誘導灯配線",    "",                2, "ケ所",  8_300, 0.70)
s += it("誘導灯取付",    "新設",             2, "台",  18_000, 0.25)
s += it("非常灯配線",    "",                5, "ケ所",  6_300, 0.70)
s += it("非常灯取付",    "埋込　NNFB91605C",  5, "台",  22_000, 0.25)
s += it("消耗雑材費",    "",                1, "式",  16_500)
T[t] = s

t = "換気設備"; cat(t); s = 0
s += it("ストレ－トシロッコファン取付", "BFS－65SUG2",   1, "台",  86_000, 0.30)
s += it("上記ダクト工事",         "150φ～200φ",    1, "式",  83_000, 0.50)
s += it("換気扇取付",            "VD－10ZC14",    2, "台",  11_800, 0.35)
s += it("上記ダクト工事",         "100φ",         1, "式",  21_000, 0.50)
s += it("排気口取付",            "150φ",         4, "台",   4_600, 0.45)
s += it("給気口取付",            "150φ",         4, "台",   4_720, 0.45)
s += it("ベントキャップ",         "150φ",         1, "個",   6_200, 0.30)
s += it("ベントキャップ",         "200φ",         1, "個",   7_200, 0.30)
s += it("外壁貫通工事",          "吸排気ダクト",     1, "式",  98_000, 0.70)
s += it("コントロールスイッチ取付",  "",             1, "個",   8_500, 0.60)
s += it("消耗雑材費",           "",              1, "式",  18_220)
T[t] = s

# 運搬費・諸経費は集計行（小計の下に「1 式」で並ぶ）。金額は元見積と同額になるよう adj で合わせる。
sub = sum(T.values())                                   # 純工事費 2,557,000
UNPAN_RATE, KEIHI_RATE = 3.0, 10.0
def jsround(x): return math.floor(x + 0.5)
u_amt, k_amt = 76_000, 263_000
rows.append({"name": "運搬費", "rate": UNPAN_RATE,
             "adj": u_amt - jsround(sub * UNPAN_RATE / 100)})
rows.append({"name": "諸経費", "expense": KEIHI_RATE,
             "adj": k_amt - jsround((sub + u_amt) * KEIHI_RATE / 100)})
net = sub + u_amt + k_amt

j = {"header": {"name": "ゆずりは浄心店　電気工事",
                "client": "株式会社廣瀬住建", "honorific": "御中",
                "date": "2026-08-30", "staff": "河口", "no": "260605"},
     "place": "", "validity": "発行日より1ヶ月", "remarks": "",
     "taxMode": "out", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(out, "見積_ゆずりは浄心店_電気工事.json")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    if r.get("type") == "cat": print("\n【" + r["name"] + "】"); continue
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:36]:38}{r['qty']:>4}{r['unit']:<4}{r['price']:>9,}{r['qty']*r['price']:>11,}")
print()
for k, v in T.items(): print(f"{k:22}{v:>12,}")
print(f"{'小　計（純工事費）':22}{sub:>12,}\n{'運搬費':22}{u_amt:>12,}\n{'諸経費':22}{k_amt:>12,}")
tax = math.floor(net * 0.1 + 0.5)
print(f"{'小計（税抜）':22}{net:>12,}\n{'消費税10%':22}{tax:>12,}\n{'合　計':22}{net+tax:>12,}")
assert (T["幹線動力設備"], T["電灯コンセント設備"], T["空調設備"], T["弱電,防災設備"], T["換気設備"]) \
       == (294_000, 605_000, 914_000, 355_000, 389_000), T
assert net == 2_896_000, net
lab = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
print(f"（参考）労務費相当 {lab:,}円／×16.5%＝法定福利費 {math.floor(lab*0.165+0.5):,}円")

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(os.path.join(out, "取込リンク_ゆずりは浄心店.txt"), "w").write(url + "\n")
print("URL長", len(url))

# ---- 短い取込リンク（q/yuzuriha.json をサイトに置き、#q=yuzuriha で開く） SHORT LINK ----
qdir = os.path.join(out, "..", "q"); os.makedirs(qdir, exist_ok=True)
json.dump(j, open(os.path.join(qdir, "yuzuriha.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
short = "https://kawaguchidenki001.github.io/kd-mitsumori/#q=yuzuriha"
open(os.path.join(out, "取込リンク_ゆずりは浄心店.txt"), "a").write(short + "\n")
print("短いリンク", short)
