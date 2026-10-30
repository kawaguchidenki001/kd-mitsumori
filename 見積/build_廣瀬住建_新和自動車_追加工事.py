# -*- coding: utf-8 -*-
"""新和自動車工業㈱新築工事　追加工事（株式会社廣瀬住建 御中）R8.10.22
   元：当初見積 No.260528（R8.5.23、計 8,650,000）。図面の変更（E01・E03 R8.10.19、E02 R8.10.14、動力盤 P-1 差し替え版）による追加。
   拾い出しは「新和自動車_追加見積拾い出し_v2.xlsx」（2026.10.21）のとおり。自動火災報知設備（E04～E06）は含まない（拾い出しのとおり）。
   R8.10.22 Kの指示：図面にはないが、電動シャッターのスイッチ用の配管も入れる（→ シャッター押釦スイッチ 配管・ボックス 6ケ所）。
   単価の考え方：
     ・当初見積に同じ項目があるものは当初の単価（回路配線 4,800、コンセント配線 2口 6,400、電灯配線 5,600、D1 90,000、
       ホイスト 130,000、スイッチ配線 片切 6,200・3路 8,400、換気扇取付 1 36,400・15 58,400 など）。
     ・動力配線は当初の 空調 65,000・ホイスト 130,000 と同じ組み方：ケーブル（ケーブルラック等の単価）＋立下り 3m の電線管＋結線
       （積算実務マニュアル2026 岐阜県の複合単価）。こう長は拾い出しの「動力盤P-1構成」。
     ・幹線は当初の金額を、マニュアルの（ケーブル＋接地線＋電線管）の単価の比で太さ変更後に直した差額。
     ・防爆照明 H1・H2 は 富永電機の照明見積（R8.8.20）の定価を参考に ★。
     ・盤 2面は 富永電機の盤見積（R8.10.23 No.1023：L-1 定価 329,000、P-1 定価 820,000）の 定価×0.7（R8.10.24 Kの指示）。
       当初の 分電盤設置 L-1 140,000・P-1 110,000 との差額で計上。
   R8.10.24 Kの指示：電気ホイスト・電動シャッター（動力配線 SS1～SS6、SS4 電源）は削除。配線器具の関係（コンセント・スイッチの行）は 1.5倍。
   R8.10.25 Kの指示：電気ホイスト・電動シャッターを見積に戻す（配線器具の 1.5倍 はそのまま）。
     ・減額は図面変更によるもの（F がなくなった、スイッチの変更、トイレのパイプファン → 天井扇）。
       R8.10.25 Kの指摘：F の行の「撤去」は撤去工事と紛らわしいので「減」に。専用回路は表記だけ 50A→30A（金額はそのまま）。D2 の台数差（12→10）は図面変更ではないので入れない。
   R8.10.30 Kの指示：動力幹線 P-1・電灯幹線 L-1 のこう長は 15m（それまでは当初の金額から逆算した約19m）。
   経費：当初見積と同じく 法定福利費なし、諸経費 10%（当初 788,000÷7,862,000≒10%）、計を1,000円単位に（諸経費の adj）。
   R8.10.30 Kの指示：工事名は「新和自動車工業㈱」（親和は誤り）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v); neg = v < 0; v = abs(v)
    if v <= 0: return 0
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    r = int(math.floor(v / step + 0.5)) * step
    return -r if neg else r

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note})
    return qty * int(price)

# ---- 積算実務マニュアル2026（岐阜県）の単価 ----
CVT14, CVT22, CVT38, CVT150 = 2_930, 4_000, 6_030, 19_100          # 600V CVT 管内
IV2, IV35, IV55, IV8, IV22 = 490, 580, 780, 940, 1_720              # IV 管内
CV2_3R, CV35_3R, CV55_3R = 1_110, 1_470, 1_920                      # CV-3C ケーブルラック
CV14_2 = 2_170                                                      # CV14sq-2C 管内
VVF16_3R = 1_020                                                    # VVF1.6-3C ケーブルラック
GP22, GP28, GP36, GP42, GP54, GP82 = 4_840, 6_320, 7_640, 10_100, 13_800, 20_300   # 厚鋼電線管 露出
E25 = 3_370                                                         # ねじなし電線管 E25 露出
ROKUSHUTSU_BOX = 5_040                                              # 露出ボックス 丸型1方出
OUT_3P30A = 8_850                                                   # 露出コンセント 3P30A 接地極付
KESSEN = 7_210                                                      # 電動機結線 直入始動方式
DROP = 3                                                            # 立下りの電線管 3m

# ---- 幹線：当初の金額 ×（変更後の単価÷当初の単価）→ 差額 ----
P1_OLD, P1_NEW = CVT14 + IV8 + GP36, CVT150 + IV22 + GP82
KANSEN_M = 15                                  # R8.10.30 Kの指示：幹線のこう長は P-1・L-1 とも 15m
P1_KANSEN = sig(P1_NEW * KANSEN_M) - 220_000   # 変更後 15m 分 − 当初の金額
L1_OLD, L1_NEW = CVT22 + IV8 + GP42, CVT38 + IV8 + GP54
L1_KANSEN = sig(L1_NEW * KANSEN_M) - 280_000
# R8.10.30 Kの指示：動力幹線は1割（増し）、電灯幹線は 76,000
P1_BASE15 = P1_KANSEN
P1_KANSEN = sig(P1_BASE15 * 1.1)
L1_KANSEN = 76_000

# ---- 動力配線（こう長は拾い出しの「動力盤P-1構成」）----
SS_LEN = [27, 24, 33, 19, 12]                                       # SS1・SS2・SS3・SS5・SS6
SHUTTER = sig(sum((CV2_3R + IV2) * L + GP22 * DROP + KESSEN for L in SS_LEN) / len(SS_LEN))
# 動力コンセント ①～⑦（No.5・11～16）：(こう長, ケーブル+接地線 の単価)
DOU = [(7, CV55_3R + IV55), (11, CV55_3R + IV55), (26, CV55_3R + IV35), (38, CV55_3R + IV55),
       (10, CV35_3R + IV35), (18, CV2_3R + IV2), (27, CV55_3R + IV55)]
DOURYOKU_OUT = sig(sum(L * r + GP28 * DROP + OUT_3P30A for L, r in DOU) / len(DOU))
SS4 = sig(VVF16_3R * 40 + E25 * DROP + KESSEN)                     # 単相100V VVF1.6-3C 約40m
OSHIBOTAN = sig(E25 * 4 + ROKUSHUTSU_BOX)                          # 押釦まで E25 約4m＋ボックス
SENYO_200V = sig((CV14_2 + IV35) * 15 + GP28 * DROP + KESSEN)      # ★こう長 15m と仮定（用途・位置未定）

# ---- 盤：富永 R8.10.23 の定価×0.7（Kの指示）から 当初の金額を引いた差額 ----
P1_NEW_BAN, L1_NEW_BAN = sig(820_000 * 0.7), sig(329_000 * 0.7)
P1_BAN = P1_NEW_BAN - 110_000
L1_BAN = L1_NEW_BAN - 140_000

# ---- 器具 ----
H1 = sig(156_300 * 0.5 * 1.3 + 15_000)         # ★耐圧防爆 面付型 EXICL1021BSA9-16（定価 156,300）
H2 = sig(166_500 * 0.5 * 1.3 + 15_000)         # ★耐圧防爆 ブラケット型 EXICL3041BSA9-16（定価 166,500）
NETSUSEN = sig(16_500 * 0.5 + 6_200)           # 熱線式自動スイッチ WTA13749W（希望小売 16,500）＋スイッチ配線
OUT4 = 3_300                                   # 2口→4口：埋込コンセント 2P15A×2 接地極付 1個分（マニュアル）
WP3_SA = 1_200                                 # 防水 2E-WP→3E-WP 器具の差額

s = 0
cat("幹線動力設備")
s += it("動力幹線　P-1　変更", "CVT14sq → CVT150sq・IV22sq（差額）", 1, "式", P1_KANSEN, f"(15m×{P1_NEW:,}−当初220,000＝{P1_BASE15:,})×1.1（Kの指示）")
s += it("電灯幹線　L-1　変更", "CVT22sq → CVT38sq（差額）", 1, "式", L1_KANSEN, "電灯盤図 R8.10.21 引込CVT38。Kの指示 76,000")
s += it("動力盤　P-1　変更", "主幹250AF・分岐16回路（差額）", 1, "面", P1_BAN, f"富永 定価820,000×0.7＝{P1_NEW_BAN:,}−当初110,000")
s += it("電灯盤　L-1　変更", "主幹100A・分岐29回路（差額）", 1, "面", L1_BAN, f"富永 定価329,000×0.7＝{L1_NEW_BAN:,}−当初140,000")
s += it("動力配線　電気ホイスト", "", 1, "ケ所", 130_000, "当初のホイストと同額")
s += it("動力配線　電動シャッター", "三相200V　SS1・SS2・SS3・SS5・SS6", 5, "ケ所", SHUTTER, "CV2sq-3C＋IV2sq 計115m＋立下り＋結線")
s += it("動力コンセント　三相200V 30A", "接地3P 30A", 7, "ケ所", DOURYOKU_OUT, "CV5.5～2sq 計137m＋立下り＋コンセント")
s += it("電源配線　電動シャッター SS4", "単相100V", 1, "ケ所", SS4, "VVF1.6-3C 約40m")
s += it("シャッター押釦スイッチ　配管・ボックス", "SS1～SS6", 6, "ケ所", OSHIBOTAN, "Kの指示（図面にない）E25 4m＋ボックス")

cat("電灯コンセント設備")
s += it("専用回路　単相200V 30A", "", 2, "ケ所", SENYO_200V, "★CV14sq-2C＋IV3.5sq 15mと仮定（金額は50Aで出したまま、表記だけ30A：Kの指示）")
s += it("回路配線", "", 3, "ケ所", 4_800, "当初単価")
HK = 1.5   # R8.10.24 Kの指示：配線器具の関係は 1.5倍
s += it("壁付コンセント　2口→4口", "器具変更（差額）", 8, "ケ所", sig(OUT4 * HK), f"{OUT4:,}×1.5")
s += it("コンセント配線　防水　3E-WP", "アース付3口 防雨形", 5, "ケ所", sig((10_400 + WP3_SA) * HK), f"(当初の防水10,400＋器具差額)×1.5")
s += it("防水コンセント　2E-WP→3E-WP", "器具変更（差額）", 4, "ケ所", sig(WP3_SA * HK), f"{WP3_SA:,}×1.5")
s += it("コンセント配線　2口", "給湯室", 1, "ケ所", sig(6_400 * HK), "当初単価×1.5")
s += it("照明器具取付　D1", "増設", 3, "台", 90_000, "当初単価")
s += it("電灯配線", "D1 増設分", 3, "ケ所", 5_600, "当初単価")
s += it("照明器具取付　H1", "耐圧防爆形LED 面付型", 1, "台", H1, "★岩崎 EXICL1021BSA9-16")
s += it("照明器具取付　H2", "耐圧防爆形LED ブラケット型", 1, "台", H2, "★岩崎 EXICL3041BSA9-16")
s += it("電灯配線", "H1・H2", 2, "ケ所", 5_600, "当初単価")
s += it("熱線式自動スイッチ", "換気扇連動型（トイレ）", 2, "ケ所", sig(NETSUSEN * HK), f"WTA13749W 相当 {NETSUSEN:,}×1.5")

cat("換気工事")
s += it("換気扇取付　天井扇（トイレ）", "ダクト・フード含む", 2, "台", 58_400, "当初の換気扇取付 15 と同額")

cat("減額（図面変更による減）")
# R8.10.30 Kの指示：照明器具取付 F の減・電灯配線 F 減分 は取り消し
s += it("スイッチ配線　3路", "変更による減", 3, "ケ所", -8_400, "当初単価")
s += it("スイッチ配線　片切", "変更による減", 3, "ケ所", -6_200, "当初単価")
s += it("換気扇取付　1（パイプファン）", "トイレ　天井扇へ変更", 2, "台", -36_400, "当初単価")

KEIHI = 10.0
k_raw = jsround(s * KEIHI / 100)
TOTAL = (s + k_raw) // 1000 * 1000
cat("経　費")
rows.append({"name": "諸経費", "rate": KEIHI, "adj": TOTAL - s - k_raw})

data = {"header": {"name": "新和自動車工業㈱新築工事　追加工事", "client": "株式会社廣瀬住建", "honorific": "御中",
                   "date": "2026-10-30", "staff": "河口", "no": ""},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_廣瀬住建_新和自動車_追加工事.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/shinwa-tsuika.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_廣瀬住建_新和自動車_追加工事.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=shinwa-tsuika\n")

sub = {}
cur = None
for r in rows:
    if r.get("type") == "cat": cur = r["name"]; print("【" + cur + "】"); continue
    if "qty" in r:
        a = r["qty"] * r["price"]; sub[cur] = sub.get(cur, 0) + a
        print(f"  {(r['name']+' '+r['spec'])[:40]:42}{r['qty']:>3}{r['unit']:<3}{r['price']:>10,}{a:>11,}  {r['note']}")
for k, v in sub.items(): print(f"{k} 計 {v:,}")
print(f"小計 {s:,}／諸経費 {TOTAL - s:,}（10%={k_raw:,}）／計（税抜）{TOTAL:,}／税込 {TOTAL + jsround(TOTAL * 0.1):,}")
