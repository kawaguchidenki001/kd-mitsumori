# -*- coding: utf-8 -*-
"""海津市3校 屋内運動場 空調設備設置工事 3.自動制御設備 ―― 改訂版（R8.09.01／戸島工業株式会社 宛）

ご指示
  ・SR-1 エアコン制御盤／盤取付費は別途 → SR-1 は「SR-1　エアコン制御盤（別途）」の行名のみ表示
    （数量・単価・金額は空欄。盤取付費の行は削除）
  ・電線管付属品／電線管支持材／結線作業費（1式・内容表記なし）／消耗雑材費 を追加
  ・鑑（見積1シート）の小計の下に 法定福利費・諸経費 を計上
  ・プルボックスは1.5倍・100円単位（切上げ）
  ・単価は最低10円単位（切上げ）
  ・合計は1,000円単位（切捨て。端数は諸経費で吸収）
  ・法定福利費・諸経費は見積書上「1 式」表示（諸経費率12%）
  ・電線管塗装費は6倍
  ・その他の単価は2割増し（×1.2）
  ・電線・電線管の数量は1割増し（×1.1、m数は切上げ）
"""
import json, base64, os, math

UP_P, UP_Q, PAINT_X, UP_PB = 1.2, 1.1, 6, 1.5
def jsround(x): return math.floor(x + 0.5)               # JS の Math.round と同じ（.5切上げ）
def q11(v):  return int(math.ceil(round(v * UP_Q, 6)))   # 数量1割増し（切上げ・浮動小数誤差を丸めてから）
def up(v, unit=10):                                      # 単価・金額の丸め（切上げ）
    return int(math.ceil(round(v, 6) / unit)) * unit
def r10(v):  return up(v, 10)                            # 端数のある金額は最低10円単位

# 旧単価 → 2割増し（いずれも端数の出ない整数）
OLD = {"電源線": 970, "連絡線": 880, "リモコン": 660,
       "E25": 2770, "E31": 3580, "E39": 4330, "PB": 8770}
# 単価は最低10円単位（切上げ）。プルボックスのみ1.5倍・100円単位（切上げ）。
P = {k: up(v * UP_P, 10) for k, v in OLD.items() if k != "PB"}
P["PB"] = up(OLD["PB"] * UP_PB, 100)
assert all(v % 10 == 0 for v in P.values()) and P["PB"] % 100 == 0

ATT_R, SUP_R, ZAT_R = 0.15, 0.30, 0.03   # 支持材はご指示により3倍（10%→30%）   # 付属品／支持材＝電線管金額×、消耗雑材費＝材料計×
KESSEN = 25_000                          # 結線作業費 円/台（1式にまとめて計上）

# 労務費比率（複合単価DBの 労務費÷複合単価。法定福利費の算定基礎に使う）
LR = {"電源線": 0.44, "連絡線": 0.51, "リモコン": 0.52,
      "E25": 0.56, "E31": 0.55, "E39": 0.56, "PB": 0.55}
WELFARE_RATE = 16.5      # 法定福利費＝労務費×％
KEIHI_RATE   = 12.0      # 諸経費＝純工事費×％

NOTE_P = "旧単価×1.2（2割増し）"
NOTE_Q = "数量: 図面拾い×1.1（1割増し・切上げ）"

rows, TOT = [], {}
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, note="", lr=0.0):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit,
         "price": int(price), "note": note}
    if lr:
        r["pl"] = int(round(price * lr))
        r["note"] += f"／労務費相当 {lr:.0%}（複合単価DBの労務費比率・法定福利費の算定基礎）"
    rows.append(r)
    return qty * int(price)

def school(title, units, ce35, cee3c, remo, pipes, pb, paint_old):
    """pipes = [(呼び径, 図面拾いm), ...]"""
    cat(title)
    # 別途扱いの制御盤（行名のみ・数量/単価/金額は空欄）
    rows.append({"name": "SR-1　エアコン制御盤（別途）", "spec": "", "qty": 0, "unit": "　",
                 "price": 0, "note": "盤本体・盤取付費とも別途（本見積に含まず）"})
    s = 0
    s += it("室内機ファン用電源線", "EM-CE 3.5sq-2c　冷媒管共巻き", q11(ce35), "m", P["電源線"],
            f"{NOTE_P}／{NOTE_Q}（{ce35}m→{q11(ce35)}m）", LR["電源線"])
    s += it("室内外機連絡配線", "EM-CEE 1.25sq-3c　冷媒管共巻き", q11(cee3c), "m", P["連絡線"],
            f"{NOTE_P}／{NOTE_Q}（{cee3c}m→{q11(cee3c)}m）", LR["連絡線"])
    for nm in ("ワイヤードリモコン配線", "風量コントロール配線"):
        s += it(nm, "EM-CEE 1.25sq-2c", q11(remo), "m", P["リモコン"],
                f"{NOTE_P}／{NOTE_Q}（{remo}m→{q11(remo)}m）", LR["リモコン"])
    pipe_amt = 0
    for dia, m in pipes:
        a = it("電線管", f"屋内露出　E {dia}φ", q11(m), "m", P[f"E{dia}"],
               f"{NOTE_P}／{NOTE_Q}（{m}m→{q11(m)}m）", LR[f"E{dia}"])
        pipe_amt += a; s += a
    att = r10(pipe_amt * ATT_R)
    sup = r10(pipe_amt * SUP_R)
    s += it("電線管付属品", "カップリング・ノーマルベンド・ボックスコネクタ等", 1, "式", att,
            f"電線管金額 {pipe_amt:,}円 × {ATT_R:.0%}")
    s += it("電線管支持材", "サドル・振れ止め金具・アンカー等", 1, "式", sup,
            f"電線管金額 {pipe_amt:,}円 × {SUP_R:.0%}")
    s += it("プルボックス", "鋼板製錆止め指定色処理　150×150×100", pb, "個", P["PB"],
            f"旧単価×{UP_PB}（1.5倍）、100円単位切上げ／数量: 図面の⊠記号 実数（数量増しなし）", LR["PB"])
    mat = s                                   # 材料費計（消耗雑材費の算定基礎）
    s += it("電線管塗装工事", "", 1, "式", paint_old * PAINT_X,
            f"ご指示により6倍（旧 {paint_old:,}円）")
    s += it("結線作業費", "", 1, "式", KESSEN * units,
            f"室内機{units}台 × {KESSEN:,}円/台。単価はご指示があれば差替え", 1.0)
    s += it("消耗雑材費", "", 1, "式", r10(mat * ZAT_R), f"材料費計 {mat:,}円 × {ZAT_R:.0%}")
    TOT[title] = s
    return s

# 図面拾い数量（前回見積）をベースに1割増し
school("Ⅰ-C 海西小学校屋内運動場　3.自動制御設備", 4,  28,  28,  68, [(25, 20), (31, 14)],            6,  9_000)
school("Ⅱ-C 石津小学校屋内運動場　3.自動制御設備", 6, 100, 100, 245, [(25, 28), (31, 38), (39, 18)], 9, 24_000)
school("Ⅲ-C 下多度小学校屋内運動場　3.自動制御設備", 6, 100, 100, 247, [(25, 25), (31, 38), (39, 19)], 9, 23_000)

# ---- 鑑の小計の下に置く集計行（法定福利費・諸経費）----
direct = sum(r["qty"] * r["price"] for r in rows if "qty" in r)
labor  = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
welfare_amt = jsround(labor * WELFARE_RATE / 100)
keihi_raw   = jsround(direct * KEIHI_RATE / 100)
TARGET      = (direct + welfare_amt + keihi_raw) // 1000 * 1000     # 合計を1,000円単位（切捨て）
keihi_amt   = TARGET - direct - welfare_amt
keihi_adj   = keihi_amt - keihi_raw
rows.append({"name": "法定福利費", "welfare": WELFARE_RATE,
             "note": f"労務費 {labor:,}円 × {WELFARE_RATE}%"
                     "（健保5.0＋介護0.8＋厚年9.15＋子ども子育て0.36＋雇用1.05 事業主負担相当）"})
rows.append({"name": "諸経費", "rate": KEIHI_RATE, "adj": keihi_adj,
             "note": f"純工事費 {direct:,}円 × {KEIHI_RATE}%＋端数調整 {keihi_adj:+,}円"
                     f"（合計を1,000円単位に切捨て → {TARGET:,}円）"})

j = {"header": {"name": "各小学校屋内運動場空調設備設置工事　自動制御設備（海西小・石津小・下多度小）",
                "client": "戸島工業株式会社", "honorific": "御中",
                "date": "2026-09-01", "staff": "河口", "no": "260901"},
     "place": "海津市地内（海西小学校・石津小学校・下多度小学校 各屋内運動場）",
     "remarks": "消費税は含まれておりません", "taxMode": "ex", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(out, "見積_海津市_自動制御設備_3校_改.json")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

d = json.load(open(p, encoding="utf-8"))
items = [r for r in d["rows"] if "qty" in r]
sums  = [r for r in d["rows"] if "qty" not in r and r.get("type") != "cat"]
mat = sum(r["qty"] * r["price"] for r in items)
lab = sum(r["qty"] * r.get("pl", 0) for r in items)
for k, v in TOT.items(): print(f"{k:44} {v:>12,}")
print(f"{'小　計（純工事費）':40} {mat:>12,}")
running = mat
for r in sums:
    base = mat if "rate" in r else lab
    rt   = r.get("rate", r.get("welfare"))
    amt  = jsround(base * rt / 100) + r.get("adj", 0)
    running += amt
    print(f"{r['name']:40}{rt:>5}% 対象{base:>10,} {amt:>12,}")
print(f"{'合計（税抜のみ・消費税は含まず）':40} {running:>12,}")
assert mat == sum(TOT.values())
assert running % 1000 == 0, running
assert all(r["price"] % 10 == 0 for r in items), "単価は10円単位"
assert all(r["price"] % 100 == 0 for r in items if r["name"] == "プルボックス")
print("明細", len(items), "件 ／ 分類",
      sum(1 for r in d["rows"] if r.get("type") == "cat"), "件 ／ 集計行", len(sums), "件")

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
b64 = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + b64
open(os.path.join(out, "取込リンク_海津市_自動制御設備_改.txt"), "w").write(url + "\n")
print("URL長", len(url))
