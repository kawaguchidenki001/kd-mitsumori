# -*- coding: utf-8 -*-
"""大藪小学校屋内運動場空調設備設置工事　電気設備工事（R8.10.10、R8.10.14 図面 v7 に合わせて更新）
   ※旧版（図面からの拾い出し）。最新は build_大藪小_電気設備_K版.py（Kの No.261015 を元に修正）。出力は _旧拾い出し版／q/oyabu-denki-old に分けた。
   R8.10.14：Drive の「大藪小_電気設備図 一式_v7.pdf」（R8.10.12）に合わせて、分岐のプルボックスを 500×500×300(D) に、
             外灯移設を v7 の内訳（撤去・基礎移設・再取付・FEP30延長・EM-CE2.0-3C 抜替え55m・掘削埋戻し等）に変更。
             250(D) は v7 の表記で7個（北3・東1・南3。v1 で分岐に数えていた1個は 553(D) に変わり、東面の1個を追加）。
   図面：E-01 特記仕様書／E-02 特記図面・電気配線系統図／E-03 盤結線図／E-04 1階平面図／E-05 2階平面図／E-06 室外機置場平面詳細図
   拾い：PDF のベクトル座標から実測（E-04・E-05 は 1pt＝74.67mm、E-06 は 1pt＝24.89mm。通り芯・室外機置場の枠で校正）。
         幹線・配線は外壁の空調用ブラケット架台に沿った屋外露出（GPZ）。管の太さは図面の「配管詳細」表（本数→管径）による。
         高さは図に無いため、外壁の配管を地上3m と仮定し、室外機置場からの立上り2m、室内機への立下り＋接続2m、
         非常用コンセントへの屋内立下り（C25）2m、1F→2F 外壁立上り4m を加えた。最後に長さ ×1.1（余長）。
   単価：複合単価（電気設備工事積算実務マニュアル2026 岐阜県）。★は登録なし・概算。
   盤（L-AC 屋外自立 SUS／S-AC 屋外壁掛 SUS）は単価表に無いため空欄（メーカー見積で入れる）。
   H・I・J のバッテリーケーブル＋信号線用の2本目の GPZ42 は計装設備工事（No.261005 の G36）で見ているため計上しない。
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

K1, K6 = 74.67, 24.89          # mm/pt（E-04・E-05／E-06）
def m1(pt): return pt * K1 / 1000
YOCHO = 1.1
H_RISE, DROP, OUT_DROP, RISE_2F = 2.0, 2.0, 2.0, 4.0

# ---- E-06 室外機置場（区間長 m）----
R_AF, R_H, R_I, R_J = 9.35, 4.82, 2.71, 0.59
R_1, R_2, R_3, R_4, R_S = 7.18, 9.16, 3.36, 3.23, 5.49     # R_S：L-AC→PB250→S-AC
# ---- E-04 1階 外壁（区間長 m）：PB250（分岐）x=876.4 から東・北と西（南面）へ ----
SE, EAST = m1(932 - 876.4), m1(536.5 - 189.5)
N = {"1-1": m1(932 - 838), "1-2": m1(838 - 811.3), "D": m1(811.3 - 789.7), "2-1": m1(789.7 - 651.4),
     "2-2": m1(651.4 - 624.3), "F": m1(624.3 - 509.1), "3-1": m1(509.1 - 471.6), "3-2": m1(471.6 - 443.2)}
S = {"1-3": m1(876.4 - 837.1), "1-4": m1(837.1 - 810.0), "E": m1(810.0 - 685.5), "2-3": m1(685.5 - 655.6),
     "2-4": m1(655.6 - 625.2), "3-4": m1(625.2 - 472.0), "3-3": m1(472.0 - 441.5), "立上": m1(441.5 - 425.5)}
NCAB = {"1-1": "ABCDF", "1-2": "ABCDF", "D": "BCDF", "2-1": "BCF", "2-2": "BCF", "F": "CF", "3-1": "C", "3-2": "C"}
SCAB = {"1-3": "ABCE3", "1-4": "ABCE3", "E": "BCE3", "2-3": "BC3", "2-4": "BC3", "3-4": "C3", "3-3": "C3", "立上": "3"}
DROP_N = [1.21, 1.21, 1.17, 1.17, 1.17, 1.17]          # 室内機への分岐（平面）北面
DROP_S = [1.50, 1.50, 1.46, 1.46, 1.46, 1.46]          # 同 南面
OUT_PLAN = {"D": 0.93, "E": 1.13, "F": 0.94}           # 非常用コンセントへの分岐（平面・屋外）
F2_3 = 32.02 + 3 * 1.0                                 # E-05 2階 天井内（E25）＋室内機3台

# ---- 配管（屋外露出 GPZ、本数→管径）----
size = lambda n: {1: 22, 2: 28, 3: 36}.get(n, 54)
GP = {22: 0.0, 28: 0.0, 36: 0.0, 42: 0.0, 54: 0.0}
GP[54] += (SE + EAST) + R_AF + H_RISE                  # 5本（A～D・F）＋置場の A～F
for k, v in N.items(): GP[size(len(NCAB[k]))] += v
for k, v in S.items(): GP[size(len(SCAB[k]))] += v
drops_in = [d + DROP for d in DROP_N + DROP_S]          # 室内機 12台
GP[22] += sum(d - 1.0 for d in drops_in)               # 屋外側（立下り1m まで）
GP[22] += sum(OUT_PLAN.values())                       # コンセント分岐の屋外側
GP[22] += R_2 + R_3 + H_RISE + R_4 + RISE_2F + 1.23    # ②・③（置場＋立上り）・④・③の 1F→2F
GP[28] += R_1                                          # ① CE14-2C＋E5.5（2本）
GP[42] += R_H + R_I + R_J + R_S + H_RISE + 1.5         # H・I・J（1本目）、幹線（L-AC→PB→S-AC）
C25 = OUT_DROP * 3                                     # 非常用コンセント 屋内立下り
E25 = F2_3

# ---- 配線 ----
def path_n(last): return SE + EAST + sum(v for k, v in N.items() if list(N).index(k) <= list(N).index(last))
def path_s(last): return sum(v for k, v in S.items() if list(S).index(k) <= list(S).index(last))
base = R_AF + H_RISE
drop_c = lambda i: [d + 1.0 for d in drops_in][i]
CE35 = 0.0
CE35 += base + path_n("1-2") + path_s("1-4")           # A（GHP1 室内機4台）
CE35 += base + path_n("2-2") + path_s("2-4")           # B
CE35 += base + path_n("3-2") + path_s("3-3")           # C
CE35 += sum(drops_in) + 12 * 1.0                       # 室内機への分岐 12本（接続余長1m）
CE35 += base + path_n("D") + OUT_PLAN["D"] + OUT_DROP + 0.5
CE35 += base + path_s("E") + OUT_PLAN["E"] + OUT_DROP + 0.5
CE35 += base + path_n("F") + OUT_PLAN["F"] + OUT_DROP + 0.5
CE35 += R_3 + H_RISE + path_s("立上") + RISE_2F + 1.23 + F2_3   # ③ L-AC→2F 室内機（GHP4）
CE35 += R_2 + 1.0                                       # ② L-AC→GHP-4 室外機
CE35 += R_H + R_I + R_J + 3 * 1.0                       # H・I・J 自立ユニット→GHP-1～3
CET38 = R_S + H_RISE + 1.5 + 1.5                       # 幹線：既設夜間照明開閉器盤→S-AC→L-AC
CE14 = R_1 + 1.0
CE20 = R_4 + 0.5
FUZOKU = 2 * (R_H + R_I + R_J + 3 * 1.0)               # 付属ケーブル（交流電源線・バッテリーケーブル）入線

L = lambda v: round(v * YOCHO)                         # 余長 ×1.1、1m 単位
print("拾い（m・余長前）", {k: round(v, 1) for k, v in GP.items()}, "C25", C25, "E25", round(E25, 1),
      "CE3.5", round(CE35, 1), "CET38", round(CET38, 1), "CE14", round(CE14, 1), "CE2", round(CE20, 1), "付属", round(FUZOKU, 1))

# ---- 見積行 ----
rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r); return int(round(qty * int(price)))
def betto(name):
    rows.append({"name": name, "spec": "（別途）", "qty": 1, "unit": "式", "price": 0, "note": "", "zero": True})

sub = 0
cat("01　幹線設備")
sub += it("開閉器盤　Ｓ－ＡＣ", "屋外壁掛型 ＳＵＳ製 ＭＣＣＢ３Ｐ１００ＡＦ／１００ＡＴ", 1, "面", 0, 0, "単価表に無し・メーカー見積で入れる")
sub += it("分電盤　Ｌ－ＡＣ", "屋外自立型 ＳＵＳ製 主幹ＭＣＣＢ３Ｐ１００ＡＦ 分岐ＥＬＣＢ８", 1, "面", 0, 0, "単価表に無し・メーカー見積で入れる")
sub += it("既設夜間照明開閉器盤改修", "分岐接続", 1, "式", 30_000, 28_200, "★1人工＋材料")
sub += it("ケーブル", "ＥＭ－ＣＥＴ３８sq", L(CET38), "ｍ", 6_230, 1_748, "管内")
sub += it("厚鋼電線管", "ＧＰ４２ 屋外露出", L(R_S + H_RISE + 1.5), "ｍ", 10_100, 5_753, "幹線分")
sub += it("接地工事", "Ｄ種 接地棒打込", 2, "か所", 9_880, 5_161, "ED・EDELB 10φ×1500")
sub += it("接地線", "ＥＭ－ＩＥ５．５sq", 6, "ｍ", 800, 395)
sub += it("電線管", "ＨＩＶＥ１６ 露出", 3, "ｍ", 2_390, 1_495)
sub += it("接地極埋設標", "測定共", 2, "か所", 14_100, 8_657)

cat("02　動力設備（空調電源）")
sub += it("ケーブル", "ＥＭ－ＣＥ３．５sq－３Ｃ", L(CE35), "ｍ", 1_390, 592, "管内 A～F・②・③・H～J")
sub += it("ケーブル", "ＥＭ－ＣＥ１４sq－２Ｃ", L(CE14), "ｍ", 2_300, 818, "① L-AC→自立ユニット")
sub += it("電線", "ＥＭ－ＩＥ５．５sq", L(CE14), "ｍ", 800, 395, "① 接地線")
sub += it("ケーブル", "ＥＭ－ＣＥ２sq－３Ｃ", L(CE20), "ｍ", 1_040, 479, "④ 熱源機")
sub += it("付属ケーブル入線", "交流電源線・バッテリーケーブル（支給品）", L(FUZOKU), "ｍ", 940, 592, "★CE3.5-3C の労務費＋経費")
GPP = {22: (4_840, 2_707), 28: (6_320, 3_497), 36: (7_640, 4_202), 42: (10_100, 5_753), 54: (13_800, 7_755)}
for s in (22, 28, 36, 42, 54):
    v = GP[s] - ((R_S + H_RISE + 1.5) if s == 42 else 0)
    if v > 0: sub += it("厚鋼電線管", f"ＧＰ{s} 屋外露出".translate(str.maketrans("0123456789", "０１２３４５６７８９")), L(v), "ｍ", *GPP[s])
sub += it("薄鋼電線管", "Ｃ２５ 屋内露出", L(C25), "ｍ", 4_030, 2_369, "非常用コンセント立下り")
sub += it("ねじなし電線管", "Ｅ２５ 隠ぺい", L(E25), "ｍ", 2_910, 1_579, "2階 GHP4 室内機")
sub += it("塗装", "Ｃ２５", L(C25), "ｍ", 290, 194, "露出C管の塗装（特記）")
sub += it("防水プリカ", "Ｆ２・ＷＰ５０", 7, "か所", 5_430, 2_341, "自立ユニット A～F・H～J、GHP-1～3")
sub += it("防水プリカ", "Ｆ２・ＷＰ３０", 1, "か所", 2_890, 1_269, "自立ユニット ①")
sub += it("防水プリカ", "Ｆ２・ＷＰ２４", 1, "か所", 2_260, 1_043, "GHP-4 ②")
sub += it("プルボックス", "１５０×１５０×１５０ ＳＵＳ製", 8, "個", 16_400, 6_345, "150(D)")
sub += it("プルボックス", "２００×２００×２００ ＳＵＳ製", 4, "個", 24_700, 8_460, "222(D)")
sub += it("プルボックス", "２５０×２５０×２５０ ＳＵＳ製", 7, "個", 34_900, 10_575, "250(D) ★200と300の中間")
sub += it("プルボックス", "５００×５００×３００ ＳＵＳ製", 1, "個", 79_600, 16_920, "553(D) 分岐（v7）")
sub += it("丸形露出ボックス", "", 5, "個", 5_140, 2_820, "F分岐・コンセント屋内側・熱源機用")
sub += it("非常用コンセント", "２Ｐ１５Ａ Ｅ付 赤 キャップ付", 3, "個", 4_500, 1_889, "★防滴プレート付で代用")
sub += it("防水コンセント", "２Ｐ１５Ａ Ｅ付", 1, "個", 4_500, 1_889, "熱源機用")
sub += it("壁貫通", "コア抜き φ３８", 16, "か所", 8_890, 6_048, "★印 1F15・2F1")

# 外灯移設（v7 E-06【外灯移設】既設外灯を東へ約2.5m移設）。★は概算。人工 28,200、経費は手間の4割
NIN = 28_200 * 1.4
dento = []
def dt(name, spec, qty, unit, price, pl, note=""):
    dento.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "pl": int(pl), "note": note})
    return int(round(qty * int(price)))
sub_d = 0
sub_d += dt("既設外灯撤去", "灯具・ポール取外し 再使用品保管", 1, "基", 22_900, 20_000, "LED屋外灯ポール灯の撤去費")
sub_d += dt("既設基礎掘起し", "再使用品", 1, "箇所", sig(NIN * 0.4), 28_200 * 0.4, "★0.4人工")
sub_d += dt("基礎移設据付", "既設基礎再使用", 1, "箇所", sig(NIN * 0.4), 28_200 * 0.4, "★0.4人工")
sub_d += dt("外灯再取付", "建込・灯具取付・結線・点灯確認", 1, "基", sig(51_888 * 1.23), 51_888, "ポール灯の取付労務＋経費")
sub_d += dt("地中配管延長", "ＦＥＰ３０ 約２．５ｍ 既設管接続・防水処理共", 1, "式", sig(1_400 * 2.5 + 3_000), 733 * 2.5 + 2_000, "★FEP30地中1,400×2.5＋接続")
sub_d += dt("配線抜替え", "ＥＭ－ＣＥ２ｓｑ－３Ｃ 既設撤去・新設入線・両端結線", 55, "ｍ", sig(970 + 130), 431 + 100, "FEP管内970＋撤去130")
sub_d += dt("掘削・埋戻し", "配管部・基礎部 残土処分共", 1, "式", sig(2.2 * (14_600 + 11_100) + 0.5 * 10_000), 2.2 * (9_906 + 6_604), "★約2.2m3 人力")
sub_d += dt("埋設標示シート", "約２．５ｍ", 1, "式", sig(280 * 2.5), 113 * 2.5)
sub_d += dt("防草シート等復旧", "既設同等", 1, "式", 5_000, 3_000, "★")

labor = sum(r["qty"] * r.get("pl", 0) for r in rows + dento if "qty" in r)
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
base_sub = sub + sub_d
z0 = sig(base_sub * 0.03) // 10 * 10
def resid(z):
    r = (base_sub + z + w_amt + jsround((base_sub + z) * KEIHI / 100)) % 1000
    return r if r < 500 else r - 1000
ZATSU = min((z for z in range(10, 2 * z0, 10) if abs(resid(z)) < 10), key=lambda z: abs(z - z0))
sub += it("雑材消耗品", "", 1, "式", ZATSU, 0)

cat("03　電灯設備")
rows.extend(dento); sub += sub_d

cat("経　費")
k_raw = jsround(sub * KEIHI / 100)
TARGET = (sub + w_amt + k_raw + 500) // 1000 * 1000
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": (TARGET - sub - w_amt) - k_raw})

data = {"header": {"name": "大藪小学校屋内運動場空調設備設置工事　電気設備工事", "client": "戸島工業株式会社", "honorific": "御中",
                   "date": "2026-10-14", "staff": "河口", "no": ""},   # 261010 は社宅エアコン取付工事で使用済みのため空欄（保存時にアプリが採番）
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_大藪小_電気設備_旧拾い出し版.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/oyabu-denki-old.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_大藪小_電気設備_旧拾い出し版.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=oyabu-denki-old\n")

for r in rows:
    if r.get("type") == "cat": print("【" + r["name"] + "】"); continue
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:38]:40}{r['qty']:>6}{r['unit']:<3}{r['price']:>9,}{int(round(r['qty']*r['price'])):>11,} {r['note']}")
k_amt = TARGET - sub - w_amt; tax = jsround(TARGET * 0.1)
print(f"小計 {sub:,}／法定福利費 {w_amt:,}（労務費{labor:,.0f}）／諸経費 {k_amt:,}（12%={k_raw:,}）／計（税抜）{TARGET:,}／税込 {TARGET+tax:,}  人工 {labor/28200:.1f}")
