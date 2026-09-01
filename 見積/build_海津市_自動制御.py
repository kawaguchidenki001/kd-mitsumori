# -*- coding: utf-8 -*-
"""海津市 各小学校屋内運動場 空調設備設置工事 ―― 3. 自動制御設備 参考見積
   （海西小・石津小・下多度小）

■ 数量：図面拾い出し（山田建築事務所 R8.09 図面集）
  海西小  M-05 自動制御設備1階平面図 / M-06 同2階平面図 / M-07 盤詳細図・系統図
  石津小  M-04 自動制御設備平面図     / M-05 盤詳細図・系統図
  下多度小 M-05 同1階平面図 / M-06 同2階平面図 / M-07 盤詳細図・系統図

  各図の【配線ｻｲｽﾞ一覧表】は A=1本 / B=2本 / C=3本 / D=4本 / E=5本 / F=6本
  （EM-CEE-1.25sq-2C、屋内露出 E25=A･B、E31=C･D、E39=E･F）。
  制御盤から室内機を数珠つなぎに結ぶ 1 本のルートで、盤に近いほど条数が増える。
  ルート区間長は 400〜500dpi でラスタライズし、通り芯（海西 X1-X7=33,400 /
  石津 X1-X5=24,000 / 下多度 Y6-Y2=17,200）でスケール較正して実測（±0.3m）。

  ・電線管長 ＝ 区間長の合計（サイズ別）＋各室内機への立下げ・盤への立上り
  ・リモコン線長 ＝ Σ(区間長 × 条数)
    ワイヤードリモコン配線と風量コントロール配線は同一ルート・同一長。
  ・プルボックス ＝ 図面の ⊠ 記号の実数

■ 単価：同一設計事務所・同一様式の先行案件（城山小屋体 Ⅲ-C 自動制御設備）の
  「採用単価」を第一優先。城山に無い項目は 複合単価DB × 補正率 R=0.823。
  （検証：EP-31 4,350→3,580 / EP-39 5,270→4,330 / EP-63 9,960→8,200 /
    EP-75 11,900→9,800、GP-22 4,840→4,000 いずれも比 0.822〜0.826）

■ 経費：設計内訳と同じく直接工事費のみ（共通仮設費・現場管理費・一般管理費は元請一括）。
"""
import json, base64, os

R = 0.823
def adj(v, step=10):
    return int(round(v * R / step)) * step

SHIRO   = "単価: 城山小屋体 自動制御設備 採用単価（大建設計・同一様式）"
PANEL_6 = 3_460_000
P_TORITSUKE = 79_800
P_CE35, P_CEE3C, P_CEE2C = 970, 880, 660
P_E31, P_E39 = 3_580, 4_330
P_PB150 = 8_770
P_E25 = adj(3_370)                      # → 2,770 円/m
NOTE_E25 = f"複合単価 電線管EP-25露出 3,370円/m × 補正率{R}（城山採用単価水準）"

PAINT = {25: 290, 31: 340, 39: 440}     # 塗装工事 電線管 複合単価/m
def paint_lump(dims):
    raw = sum(PAINT[d] * m for d, m in dims)
    return int(round(raw * R / 1000)) * 1000, raw

# 海西小の制御盤（室内機4台系統）：固定60%＋台数比例40% で 6台系統単価から換算
PANEL_4 = int(round(PANEL_6 * (0.6 + 0.4 * 4 / 6) / 1000)) * 1000   # → 2,999,000

rows, TOT = [], {}
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit,
                 "price": int(price), "note": note})
    return qty * int(price)

def school(title, panel, panel_note, ce35, cee3c, remo, pipes, pb, route_note):
    """pipes = [(呼び径, m), ...] 屋内露出電線管（塗装対象と同じ）"""
    cat(title)
    s = 0
    s += it("SR-1　エアコン制御盤", "集中リモコン・風量コントロールリモコン・課金(コイン式)装置等 含む",
            1, "面", panel, panel_note)
    s += it("盤取付費", "調整含む", 1, "面", P_TORITSUKE, SHIRO)
    s += it("室内機ファン用電源線", "EM-CE 3.5sq-2c　冷媒管共巻き", ce35, "m", P_CE35,
            SHIRO + "／数量: 配管設備の冷媒管長と同じ")
    s += it("室内外機連絡配線", "EM-CEE 1.25sq-3c　冷媒管共巻き", cee3c, "m", P_CEE3C,
            SHIRO + "／数量: 配管設備の冷媒管長と同じ")
    s += it("ワイヤードリモコン配線", "EM-CEE 1.25sq-2c", remo, "m", P_CEE2C,
            SHIRO + "／数量: " + route_note)
    s += it("風量コントロール配線", "EM-CEE 1.25sq-2c", remo, "m", P_CEE2C,
            SHIRO + "／数量: ワイヤードリモコン配線と同一ルート・同一長")
    for dia, m in pipes:
        p, nt = {25: (P_E25, NOTE_E25), 31: (P_E31, SHIRO), 39: (P_E39, SHIRO)}[dia]
        s += it("電線管", f"屋内露出　E {dia}φ", m, "m", p, nt)
    s += it("プルボックス", "鋼板製錆止め指定色処理　150×150×100", pb, "個", P_PB150,
            SHIRO + "／数量: 図面の⊠記号 実数")
    amt, raw = paint_lump(pipes)
    detail = "＋".join(f"E{d} {m}m" for d, m in pipes)
    s += it("電線管塗装工事", "", 1, "式", amt,
            f"塗装複合単価×補正率{R}：{detail} = {raw:,}円 → {amt:,}円")
    TOT[title] = s
    return s

# ===== Ⅰ-C 海西小（室内機4台・2階ギャラリー1列） =====
# M-06：A 5.6m / B 11.0m / C 5.5m / D 5.8m（実測）＋各室内機立下げ4本・盤立上り
school("Ⅰ-C 海西小学校屋内運動場　3.自動制御設備", PANEL_4,
       f"室内機4台系統。城山小(6台)採用単価{PANEL_6:,}円を固定60%＋台数比例40%で換算した推定額。要メーカー見積",
       28, 28, 68, [(25, 20), (31, 14)], 6,
       "M-06 2階ｷﾞｬﾗﾘｰ A5.6m×1本＋B11.0m×2本＋C5.5m×3本＋D5.8m×4本＝67m＋立下げ ≒ 68m")

# ===== Ⅱ-C 石津小（室内機6台・西3台/東3台、北側を横断） =====
# M-04：A 9.1 / B 13.3 / C 28.2（西1.2＋北23.3＋東3.7）/ D 10.2 / E 12.4 / F 3.7
school("Ⅱ-C 石津小学校屋内運動場　3.自動制御設備", PANEL_6,
       SHIRO + "（室内機6台系統・城山と同構成）",
       100, 100, 245, [(25, 28), (31, 38), (39, 18)], 9,
       "M-04 A9.1×1＋B13.3×2＋C28.2×3＋D10.2×4＋E12.4×5＋F3.7×6 ＝ 245m")

# ===== Ⅲ-C 下多度小（室内機6台・北ｷﾞｬﾗﾘｰ3台/南ｷﾞｬﾗﾘｰ3台、東側で連絡） =====
# M-06：F 7.6 / E 9.6 / D 9.6 / C 28.9（北0.9＋東19.9＋南8.1）/ B 9.5 / A 9.6
school("Ⅲ-C 下多度小学校屋内運動場　3.自動制御設備", PANEL_6,
       SHIRO + "（室内機6台系統・城山と同構成）",
       100, 100, 247, [(25, 25), (31, 38), (39, 19)], 9,
       "M-06 A9.6×1＋B9.5×2＋C28.9×3＋D9.6×4＋E9.6×5＋F7.6×6 ＝ 247m")

j = {"header": {"name": "各小学校屋内運動場空調設備設置工事　自動制御設備（海西小・石津小・下多度小）",
                "client": "大建設計株式会社", "honorific": "御中",
                "date": "2026-09-01", "staff": "河口"},
     "place": "海津市地内（海西小学校・石津小学校・下多度小学校 各屋内運動場）",
     "remarks": "", "taxMode": "out", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(out, "見積_海津市_自動制御設備_3校.json")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

d = json.load(open(p, encoding="utf-8"))
net = sum(r["qty"] * r["price"] for r in d["rows"] if "qty" in r)
for k, v in TOT.items(): print(f"{k:44} {v:>12,.0f}")
print(f"{'直接工事費（自動制御設備・3校計）':40} {net:>12,.0f}")
print(f"{'消費税10%':40} {round(net*0.1):>12,.0f}")
print(f"{'合計（税込）':40} {round(net*1.1):>12,.0f}")
print("明細", sum(1 for r in d["rows"] if "qty" in r), "件 ／ 分類",
      sum(1 for r in d["rows"] if r.get("type") == "cat"), "件")
assert net == sum(TOT.values())

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
b64 = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + b64
open(os.path.join(out, "取込リンク_海津市_自動制御設備.txt"), "w").write(url + "\n")
print("URL長", len(url))
