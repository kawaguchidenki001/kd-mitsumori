# -*- coding: utf-8 -*-
"""海津市 各小学校屋内運動場 空調設備設置工事 ―― 3. 自動制御設備 参考見積
   （海西小・石津小・下多度小）

内訳書：大建設計「02 設計内訳明細書」Ⅰ-C/Ⅱ-C/Ⅲ-C 機械設備 の 3.自動制御設備 の
行構成・摘要をそのまま踏襲する。

単価の根拠
  同じ設計事務所・同一様式の先行案件（城山小屋体 Ⅲ-C.機械設備）の「採用単価」を第一優先で使用。
  城山シートに無い項目は 複合単価DB × 補正率 R=0.823 で城山の単価水準に合わせる。
    （検証：EP-31 4,350→3,580 / EP-39 5,270→4,330 / EP-63 9,960→8,200 / EP-75 11,900→9,800
      いずれも比 0.822〜0.824、GP-22 4,840→4,000 も 0.826）
  プルボックス 150×150×100 は城山採用単価 8,770円/個をそのまま採用。
  電線管塗装工事（1式）は 屋内露出電線管長 × 塗装複合単価 × 0.823 を 1,000円単位に丸め。
    （検証：城山 E31 23m+E39 50m+E63 25m+E75 11m → 58,000×0.823=47,734 ≒ 採用 47,000）

数量
  設計内訳書の数量をそのまま採用。図面が未着のため図面拾いは未実施（誤差検証は図面入手後）。
経費
  設計内訳と同じく本書は直接工事費のみ。共通仮設費・現場管理費・一般管理費は元請一括計上。
"""
import json, base64, os

R = 0.823                      # 複合単価 → 城山採用単価 の補正率
def adj(v, step=10):           # 城山単価と同じく10円単位
    return int(round(v * R / step)) * step

# ---- 城山小（先行案件）採用単価 ---------------------------------------------
SHIRO = "単価: 城山小屋体 自動制御設備 採用単価（大建設計・同一様式）"
PANEL_6 = 3_460_000            # SR-1 エアコン制御盤（室内機6台系統）メーカー見積×0.85
P_TORITSUKE = 79_800           # 盤取付費／面
P_CE35   = 970                 # 室内機ファン用電源線 EM-CE 3.5sq-2c 冷媒管共巻き
P_CEE3C  = 880                 # 室内外機連絡配線 EM-CEE 1.25sq-3c 冷媒管共巻き
P_CEE2C  = 660                 # ワイヤードリモコン／風量コントロール配線 EM-CEE 1.25sq-2c
P_E31    = 3_580               # 電線管 E31 屋内露出
P_E39    = 4_330               # 電線管 E39 屋内露出
P_PB150  = 8_770               # プルボックス 150×150×100 鋼板製錆止め指定色処理

# ---- 城山シートに無い項目（複合単価DB × R） --------------------------------
P_E25 = adj(3_370)             # 電線管 EP-25 露出 3,370円/m → 2,770円/m
NOTE_E25 = f"複合単価 電線管EP-25露出 3,370円/m × 補正率{R}（城山採用単価水準）"

PAINT = {25: 290, 31: 340, 39: 440}      # 塗装工事 電線管 複合単価/m
def paint_lump(dims):
    """dims = [(呼び径, m), ...] → 1式金額（1,000円単位）"""
    raw = sum(PAINT[d] * m for d, m in dims)
    return int(round(raw * R / 1000)) * 1000, raw

# ---- 海西小の制御盤（室内機4台系統） ---------------------------------------
# 集中リモコン・風量コントロールリモコン・課金(コイン式)装置を含む盤で、
# 固定部60%＋室内機台数比例部40% として 6台系統の城山単価から換算。
PANEL_4 = int(round(PANEL_6 * (0.6 + 0.4 * 4 / 6) / 1000)) * 1000   # → 2,999,000

rows, TOT = [], {}
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit,
                 "price": int(price), "note": note})
    return qty * int(price)

def school(title, n_unit, panel, panel_note, ce35, cee3c, wired, fan, pipes, pb, paint_dims):
    cat(title)
    s = 0
    s += it("SR-1　エアコン制御盤", "集中リモコン・風量コントロールリモコン・課金(コイン式)装置等 含む",
            1, "面", panel, panel_note)
    s += it("盤取付費", "調整含む", 1, "面", P_TORITSUKE, SHIRO)
    s += it("室内機ファン用電源線", "EM-CE 3.5sq-2c　冷媒管共巻き", ce35, "m", P_CE35, SHIRO)
    s += it("室内外機連絡配線", "EM-CEE 1.25sq-3c　冷媒管共巻き", cee3c, "m", P_CEE3C, SHIRO)
    s += it("ワイヤードリモコン配線", "EM-CEE 1.25sq-2c", wired, "m", P_CEE2C, SHIRO)
    s += it("風量コントロール配線", "EM-CEE 1.25sq-2c", fan, "m", P_CEE2C, SHIRO)
    for dia, m in pipes:
        p, nt = {25: (P_E25, NOTE_E25), 31: (P_E31, SHIRO), 39: (P_E39, SHIRO)}[dia]
        s += it("電線管", f"屋内露出　E {dia}φ", m, "m", p, nt)
    s += it("プルボックス", "鋼板製錆止め指定色処理　150×150×100", pb, "個", P_PB150, SHIRO)
    amt, raw = paint_lump(paint_dims)
    detail = "＋".join(f"E{d} {m}m" for d, m in paint_dims)
    s += it("電線管塗装工事", "", 1, "式", amt,
            f"塗装複合単価×補正率{R}：{detail} = {raw:,}円 → {amt:,}円")
    TOT[title] = s
    return s

# ===== Ⅰ-C 海西小（室内機4台） =====
school("Ⅰ-C 海西小学校屋内運動場　3.自動制御設備", 4, PANEL_4,
       f"室内機4台系統。城山小(6台)採用単価{PANEL_6:,}円を固定60%＋台数比例40%で換算した推定額。要メーカー見積",
       28, 28, 68, 68, [(25, 20), (31, 50)], 6, [(25, 20), (31, 50)])

# ===== Ⅱ-C 石津小（室内機6台） =====
school("Ⅱ-C 石津小学校屋内運動場　3.自動制御設備", 6, PANEL_6, SHIRO + "（室内機6台系統・城山と同構成）",
       100, 100, 68, 68, [(25, 26), (31, 42), (39, 26)], 9, [(25, 26), (31, 42), (39, 26)])

# ===== Ⅲ-C 下多度小（室内機6台） =====
school("Ⅲ-C 下多度小学校屋内運動場　3.自動制御設備", 6, PANEL_6, SHIRO + "（室内機6台系統・城山と同構成）",
       100, 100, 84, 68, [(25, 26), (31, 42), (39, 26)], 9, [(25, 26), (31, 42), (39, 26)])

j = {"header": {"name": "各小学校屋内運動場空調設備設置工事　自動制御設備（海西小・石津小・下多度小）",
                "client": "大建設計株式会社", "honorific": "御中",
                "date": "2026-09-01", "staff": "河口"},
     "place": "海津市地内（海西小学校・石津小学校・下多度小学校 各屋内運動場）",
     "remarks": "", "taxMode": "out", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(out, "見積_海津市_自動制御設備_3校.json")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- 検算（JSONを読み直して集計）--------------------------------------------
d = json.load(open(p, encoding="utf-8"))
net = sum(r["qty"] * r["price"] for r in d["rows"] if "qty" in r)
for k, v in TOT.items():
    print(f"{k:44} {v:>12,.0f}")
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
