# -*- coding: utf-8 -*-
"""海津市3校 屋内運動場 空調設備設置工事 3.自動制御設備 ―― 改訂版（R8.09.01／戸島工業株式会社 宛）

ご指示
  ・SR-1 エアコン制御盤／盤取付費は別途 → SR-1 は「SR-1　エアコン制御盤（別途）」の行名のみ表示
    （数量・単価・金額は空欄。盤取付費の行は削除）
  ・電線管付属品／電線管支持材／結線作業費／消耗雑材費 を追加
  ・電線管塗装費は6倍
  ・その他の単価は2割増し（×1.2）
  ・電線・電線管の数量は1割増し（×1.1、m数は切上げ）
"""
import json, base64, os, math

UP_P, UP_Q, PAINT_X = 1.2, 1.1, 6
def q11(v):  return int(math.ceil(round(v * UP_Q, 6)))   # 数量1割増し（切上げ・浮動小数誤差を丸めてから）
def r10(v):  return int(math.floor(v / 10.0 + 0.5)) * 10

# 旧単価 → 2割増し（いずれも端数の出ない整数）
P = {"電源線": 970, "連絡線": 880, "リモコン": 660,
     "E25": 2770, "E31": 3580, "E39": 4330, "PB": 8770}
P = {k: int(v * UP_P) for k, v in P.items()}
assert all(int(v) == v for v in P.values())

ATT_R, SUP_R, ZAT_R = 0.15, 0.10, 0.03   # 付属品／支持材＝電線管金額×、消耗雑材費＝材料計×
KESSEN = 25_000                          # 結線作業費 円/台

NOTE_P = "旧単価×1.2（2割増し）"
NOTE_Q = "数量: 図面拾い×1.1（1割増し・切上げ）"

rows, TOT = [], {}
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit,
                 "price": int(price), "note": note})
    return qty * int(price)

def school(title, units, ce35, cee3c, remo, pipes, pb, paint_old):
    """pipes = [(呼び径, 図面拾いm), ...]"""
    cat(title)
    # 別途扱いの制御盤（行名のみ・数量/単価/金額は空欄）
    rows.append({"name": "SR-1　エアコン制御盤（別途）", "spec": "", "qty": 0, "unit": "　",
                 "price": 0, "note": "盤本体・盤取付費とも別途（本見積に含まず）"})
    s = 0
    s += it("室内機ファン用電源線", "EM-CE 3.5sq-2c　冷媒管共巻き", q11(ce35), "m", P["電源線"],
            f"{NOTE_P}／{NOTE_Q}（{ce35}m→{q11(ce35)}m）")
    s += it("室内外機連絡配線", "EM-CEE 1.25sq-3c　冷媒管共巻き", q11(cee3c), "m", P["連絡線"],
            f"{NOTE_P}／{NOTE_Q}（{cee3c}m→{q11(cee3c)}m）")
    for nm in ("ワイヤードリモコン配線", "風量コントロール配線"):
        s += it(nm, "EM-CEE 1.25sq-2c", q11(remo), "m", P["リモコン"],
                f"{NOTE_P}／{NOTE_Q}（{remo}m→{q11(remo)}m）")
    pipe_amt = 0
    for dia, m in pipes:
        a = it("電線管", f"屋内露出　E {dia}φ", q11(m), "m", P[f"E{dia}"],
               f"{NOTE_P}／{NOTE_Q}（{m}m→{q11(m)}m）")
        pipe_amt += a; s += a
    att = r10(pipe_amt * ATT_R)
    sup = r10(pipe_amt * SUP_R)
    s += it("電線管付属品", "カップリング・ノーマルベンド・ボックスコネクタ等", 1, "式", att,
            f"電線管金額 {pipe_amt:,}円 × {ATT_R:.0%}")
    s += it("電線管支持材", "サドル・振れ止め金具・アンカー等", 1, "式", sup,
            f"電線管金額 {pipe_amt:,}円 × {SUP_R:.0%}")
    s += it("プルボックス", "鋼板製錆止め指定色処理　150×150×100", pb, "個", P["PB"],
            f"{NOTE_P}／数量: 図面の⊠記号 実数（数量増しなし）")
    mat = s                                   # 材料費計（消耗雑材費の算定基礎）
    s += it("電線管塗装工事", "", 1, "式", paint_old * PAINT_X,
            f"ご指示により6倍（旧 {paint_old:,}円）")
    s += it("結線作業費", "電源線・連絡線・リモコン線・風量線の室内機側／盤側 端末結線",
            units, "台", KESSEN, "室内機1台あたり一式。単価はご指示があれば差替え")
    s += it("消耗雑材費", "", 1, "式", r10(mat * ZAT_R), f"材料費計 {mat:,}円 × {ZAT_R:.0%}")
    TOT[title] = s
    return s

# 図面拾い数量（前回見積）をベースに1割増し
school("Ⅰ-C 海西小学校屋内運動場　3.自動制御設備", 4,  28,  28,  68, [(25, 20), (31, 14)],            6,  9_000)
school("Ⅱ-C 石津小学校屋内運動場　3.自動制御設備", 6, 100, 100, 245, [(25, 28), (31, 38), (39, 18)], 9, 24_000)
school("Ⅲ-C 下多度小学校屋内運動場　3.自動制御設備", 6, 100, 100, 247, [(25, 25), (31, 38), (39, 19)], 9, 23_000)

j = {"header": {"name": "各小学校屋内運動場空調設備設置工事　自動制御設備（海西小・石津小・下多度小）",
                "client": "戸島工業株式会社", "honorific": "御中",
                "date": "2026-09-01", "staff": "河口", "no": "260901"},
     "place": "海津市地内（海西小学校・石津小学校・下多度小学校 各屋内運動場）",
     "remarks": "消費税は含まれておりません", "taxMode": "ex", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(out, "見積_海津市_自動制御設備_3校_改.json")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

d = json.load(open(p, encoding="utf-8"))
net = 0
for r in d["rows"]:
    if r.get("type") == "cat":
        print("\n【" + r["name"] + "】"); continue
    a = r["qty"] * r["price"]; net += a
    nm = (r["name"] + "　" + r["spec"]).strip()
    print(f"  {nm[:52]:54}{r['qty'] or '':>5}{r['unit']:<3}"
          f"{(f'{r[chr(112)+chr(114)+chr(105)+chr(99)+chr(101)]:,}' if r['price'] else ''):>9}"
          f"{(f'{a:,}' if a else ''):>12}")
print()
for k, v in TOT.items(): print(f"{k:44} {v:>12,}")
print(f"{'合計（税抜のみ・消費税は含まず）':40} {net:>12,}")
assert net == sum(TOT.values())
print("明細", sum(1 for r in d["rows"] if "qty" in r), "件 ／ 分類",
      sum(1 for r in d["rows"] if r.get("type") == "cat"), "件")

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
b64 = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + b64
open(os.path.join(out, "取込リンク_海津市_自動制御設備_改.txt"), "w").write(url + "\n")
print("URL長", len(url))
