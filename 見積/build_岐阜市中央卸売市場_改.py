# -*- coding: utf-8 -*-
"""岐阜市中央卸売市場北側高架衝突防止設置工事 電気工事 ―― 改訂版（R8.09.01）

ご指示
  ・1円単位は繰り上げ（単価・金額とも10円単位に切上げ）
  ・塗装費は 80,000円
  ・タイマー制御盤は 180,000円
  ・それ以外は全て2割増し（×1.2）
  ・提出先 永井建設株式会社／日付 2026-09-01
"""
import json, base64, os, math

def up10(v):                      # 1円単位を繰り上げ → 10円単位
    return int(math.ceil(v / 10.0)) * 10

UP = 1.2
NOTE_UP = "旧単価×1.2（2割増し）、1円単位繰り上げ"
NOTE_FIX = "ご指示額"

# (品名, 仕様, 数量, 単位, 旧単価, 固定額 or None)
SRC = [
 ("鋼製電線管",              "CP19",                    10, "本",   1332, None),
 ("鋼製電線管",              "CP25",                     4, "本",   1804, None),
 ("金属製可とう電線管（防水）", "#17",                      6, "m",    1040, None),
 ("硬質ビニル電線管",         "HIVE16",                   6, "本",    684, None),
 ("同上付属品",              "支持材共",                  1, "式",   6200, None),
 ("ビニルアウトボックス",      "4×54",                     5, "個",    428, None),
 ("プルボックス（SUS被せ蓋）", "200×200×200",              3, "個",  14484, None),
 ("電線ケーブル",            "EM-EEF2.0-2C",            45, "m",     230, None),
 ("電線ケーブル",            "EM-EEF1.6-2C",            25, "m",     161, None),
 ("電線ケーブル",            "DV2.0-2C",                15, "m",     120, None),
 ("引き込み支持材料",         "碍子含む",                  1, "式",  15000, None),
 ("タイマー制御盤",          "SUS製",                     1, "面",      0, 180000),
 ("配線用遮断器",            "2P50AF/20AT",              1, "組",   5171, None),
 ("同上取付改造費",          "",                          1, "式",  30000, None),
 ("回転灯（100φ）",          "SF10-M2JN-Y（相当品）",      2, "台",  25000, None),
 ("同上取付支持金具",         "SZK103（相当品）",           2, "個",   7000, None),
 ("消耗品材料費",            "",                          1, "式",  10900, None),
 ("電工費",                 "",                          1, "式", 378700, None),
 ("高所作業車損料",          "",                          1, "式", 131800, None),
 ("塗装費",                 "露出配管",                   1, "式",  11600,  80000),
]

rows = []
for name, spec, qty, unit, old, fixed in SRC:
    if fixed is not None:
        price, note = fixed, f"{NOTE_FIX}（旧 {old:,}円）" if old else NOTE_FIX
    else:
        price, note = up10(old * UP), f"{NOTE_UP}（旧 {old:,}円）"
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit,
                 "price": price, "note": note})

j = {"header": {"name": "岐阜市中央卸売市場北側高架衝突防止設置工事　電気工事",
                "client": "永井建設株式会社", "honorific": "御中",
                "date": "2026-09-01", "staff": "河口", "no": "260825"},
     "place": "岐阜市茜部新所2丁目5番地　岐阜市中央卸売市場",
     "remarks": "", "taxMode": "out", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(out, "見積_岐阜市中央卸売市場_高架衝突防止_電気工事_改.json")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

d = json.load(open(p, encoding="utf-8"))
net = sum(r["qty"] * r["price"] for r in d["rows"])
print(f"{'品名':30}{'数量':>6} {'単価':>10} {'金額':>12}")
for r in d["rows"]:
    print(f"{(r['name']+' '+r['spec']).strip():30}{r['qty']:>4}{r['unit']:<2}"
          f"{r['price']:>10,} {r['qty']*r['price']:>12,}")
    assert r["price"] % 10 == 0, r
print(f"{'小　計':30}{'':>6} {'':>10} {net:>12,}")
print(f"{'消費税10%':30}{'':>6} {'':>10} {round(net*0.1):>12,}")
print(f"{'合　計':30}{'':>6} {'':>10} {round(net*1.1):>12,}")
print("明細", len(d["rows"]), "件")

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
b64 = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + b64
open(os.path.join(out, "取込リンク_岐阜市中央卸売市場_改.txt"), "w").write(url + "\n")
print("URL長", len(url))
