# -*- coding: utf-8 -*-
"""岐阜市中央卸売市場北側高架衝突防止設置工事 電気工事 ―― 改訂版（R8.09.01）

ご指示
  ・1円単位は繰り上げ（単価・金額とも10円単位に切上げ）
  ・塗装費は 80,000円／タイマー制御盤は 180,000円
  ・それ以外は全て2割増し（×1.2）
  ・電工費・高所作業車損料は 1,000円単位（切上げ）
  ・法定福利費と諸経費を追加
  ・合計（税込）は 1,000円単位
  ・提出先 永井建設株式会社／日付 2026-09-01
"""
import json, base64, os, math

def jsround(x):          # JavaScript の Math.round と同じ「.5は切上げ」
    return math.floor(x + 0.5)

def up(v, unit=10):
    return int(math.ceil(v / float(unit))) * unit

UP = 1.2
NOTE_UP  = "旧単価×1.2（2割増し）、1円単位繰り上げ"
NOTE_UP1000 = "旧単価×1.2（2割増し）、1,000円単位繰り上げ"
NOTE_FIX = "ご指示額"

# (品名, 仕様, 数量, 単位, 旧単価, 固定額, 丸め単位)
SRC = [
 ("鋼製電線管",              "CP19",                    10, "本",   1332, None,     10),
 ("鋼製電線管",              "CP25",                     4, "本",   1804, None,     10),
 ("金属製可とう電線管（防水）", "#17",                      6, "m",    1040, None,     10),
 ("硬質ビニル電線管",         "HIVE16",                   6, "本",    684, None,     10),
 ("同上付属品",              "支持材共",                  1, "式",   6200, None,     10),
 ("ビニルアウトボックス",      "4×54",                     5, "個",    428, None,     10),
 ("プルボックス（SUS被せ蓋）", "200×200×200",              3, "個",  14484, None,     10),
 ("電線ケーブル",            "EM-EEF2.0-2C",            45, "m",     230, None,     10),
 ("電線ケーブル",            "EM-EEF1.6-2C",            25, "m",     161, None,     10),
 ("電線ケーブル",            "DV2.0-2C",                15, "m",     120, None,     10),
 ("引き込み支持材料",         "碍子含む",                  1, "式",  15000, None,     10),
 ("タイマー制御盤",          "SUS製",                     1, "面", 150000, 180000,   10),
 ("配線用遮断器",            "2P50AF/20AT",              1, "組",   5171, None,     10),
 ("同上取付改造費",          "",                          1, "式",  30000, None,     10),
 ("回転灯（100φ）",          "SF10-M2JN-Y（相当品）",      2, "台",  25000, None,     10),
 ("同上取付支持金具",         "SZK103（相当品）",           2, "個",   7000, None,     10),
 ("消耗品材料費",            "",                          1, "式",  10900, None,     10),
 ("電工費",                 "",                          1, "式", 378700, None,   1000),
 ("高所作業車損料",          "",                          1, "式", 131800, None,   1000),
 ("塗装費",                 "露出配管",                   1, "式",  11600,  80000,   10),
]

WELFARE_RATE = 16.5     # 法定福利費＝労務費×％
KEIHI_RATE   = 15.0     # 諸経費＝純工事費×％
TARGET_EX    = 1_390_000   # 計（税抜）… 税込を1,000円単位にするため10,000円単位に丸め

rows = []
for name, spec, qty, unit, old, fixed, step in SRC:
    if fixed is not None:
        price, note = fixed, f"{NOTE_FIX}（旧 {old:,}円）"
    else:
        price = up(old * UP, step)
        note = (NOTE_UP1000 if step == 1000 else NOTE_UP) + f"（旧 {old:,}円）"
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": price, "note": note}
    if name == "電工費":
        r["pl"] = price          # 法定福利費の算定基礎＝労務費
        r["note"] += "／法定福利費の算定基礎（労務費）"
    rows.append(r)

direct = sum(r["qty"] * r["price"] for r in rows)
labor  = sum(r["qty"] * r.get("pl", 0) for r in rows)

welfare_amt = jsround(labor * WELFARE_RATE / 100)
keihi_amt   = TARGET_EX - direct - welfare_amt
keihi_adj   = keihi_amt - jsround(direct * KEIHI_RATE / 100)

rows.append({"name": "法定福利費", "welfare": WELFARE_RATE,
             "note": f"労務費（電工費）{labor:,}円 × {WELFARE_RATE}%"
                     "（健保5.0＋介護0.8＋厚年9.15＋子ども子育て0.36＋雇用1.05 事業主負担相当）"})
rows.append({"name": "諸経費", "rate": KEIHI_RATE, "adj": keihi_adj,
             "note": f"純工事費 {direct:,}円 × {KEIHI_RATE}%＋端数調整 {keihi_adj:+,}円"
                     f"（計（税抜）を{TARGET_EX:,}円・合計（税込）を1,000円単位に丸め）"})

j = {"header": {"name": "岐阜市中央卸売市場北側高架衝突防止設置工事　電気工事",
                "client": "永井建設株式会社", "honorific": "御中",
                "date": "2026-09-01", "staff": "河口", "no": "260825"},
     "place": "岐阜市茜部新所2丁目5番地　岐阜市中央卸売市場",
     "remarks": "", "taxMode": "out", "taxRate": 10, "priceMode": "comp", "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(out, "見積_岐阜市中央卸売市場_高架衝突防止_電気工事_改.json")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- 検算（JSONを読み直して applyComputed を再現）----
d = json.load(open(p, encoding="utf-8"))
items = [r for r in d["rows"] if "qty" in r]
sums  = [r for r in d["rows"] if "qty" not in r]
mat = sum(r["qty"] * r["price"] for r in items)
lab = sum(r["qty"] * r.get("pl", 0) for r in items)
print(f"{'品名':32}{'数量':>5} {'単価':>10} {'金額':>12}")
for r in items:
    print(f"{(r['name']+' '+r['spec']).strip():32}{r['qty']:>3}{r['unit']:<2}"
          f"{r['price']:>10,} {r['qty']*r['price']:>12,}")
    assert r["price"] % 10 == 0
print(f"{'小　計（純工事費）':32}{'':>5} {'':>10} {mat:>12,}")
running = mat
for r in sums:
    base = mat if "rate" in r else (lab if "welfare" in r else running)
    rt   = r.get("rate", r.get("welfare", r.get("expense")))
    adj  = r.get("adj", 0)
    amt  = jsround(base * rt / 100) + adj
    running += amt
    print(f"{r['name']:32}{rt:>4}% {base:>10,} {amt:>12,}")
tax = jsround(running * 0.1)
print(f"{'計（税抜）':32}{'':>5} {'':>10} {running:>12,}")
print(f"{'消費税10%':32}{'':>5} {'':>10} {tax:>12,}")
print(f"{'合　計':32}{'':>5} {'':>10} {running+tax:>12,}")
assert running == TARGET_EX and (running + tax) % 1000 == 0
print("明細", len(items), "件 ／ 集計行", len(sums), "件")

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
b64 = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + b64
open(os.path.join(out, "取込リンク_岐阜市中央卸売市場_改.txt"), "w").write(url + "\n")
print("URL長", len(url))
