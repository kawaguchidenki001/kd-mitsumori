# -*- coding: utf-8 -*-
"""大乗教高圧受電設備工事（株式会社トミテック 御中）／見積No.260908
   いただいた R8.9.4 の見積（630,000円 1式・材料支給）に、
   小計の下へ 運搬費（純工事費×5%）と 諸経費（純工事費×12%）を追加した版。
   計（税抜）は1,000円単位になるよう諸経費で端数調整。税抜表示（消費税は出さない）。
"""
import json, base64, os, math

def jsround(x): return math.floor(x + 0.5)

rows = []
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note})
    return qty * int(price)
def memo(text):
    """内容の説明行（数量・単位・単価・金額は空欄）"""
    rows.append({"name": text, "spec": "", "qty": 0, "unit": "　", "price": 0})

sub = it("高圧受電設備工事（材料支給）", "", 1, "式", 630_000)
for t in ["・コンクリート柱建柱（10m）、基礎斫り",
          "・装柱、SOG取付",
          "・配管立上げ",
          "・キュービクル　アンカー取付、設置",
          "・高圧ケーブル（6kvCVT38sq）配線、端末処理",
          "・建柱車、高所作業車、4tユニック、重機0.1㎥",
          "・ラフタークレーン　10t"]:
    memo(t)

UNPAN_RATE, KEIHI_RATE = 5.0, 12.0
u_raw = jsround(sub * UNPAN_RATE / 100)
u_amt = u_raw // 1000 * 1000                       # 運搬費は1,000円単位（切捨て）
k_raw = jsround(sub * KEIHI_RATE / 100)
TARGET = (sub + u_amt + k_raw) // 1000 * 1000      # 計（税抜）を1,000円単位（切捨て）
k_amt = TARGET - sub - u_amt                       # 端数は諸経費で吸収
rows.append({"name": "運搬費", "rate": UNPAN_RATE, "adj": u_amt - u_raw})
rows.append({"name": "諸経費", "rate": KEIHI_RATE, "adj": k_amt - k_raw})
net = TARGET

j = {"header": {"name": "大乗教高圧受電設備工事",
                "client": "株式会社トミテック", "honorific": "御中",
                "date": "2026-09-04", "staff": "河口", "no": "260908"},
     "place": "名古屋市熱田区外土居町４−７", "validity": "", "remarks": "",
     "taxMode": "ex", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
json.dump(j, open(os.path.join(out, "見積_大乗教_高圧受電設備工事.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

for r in rows:
    if "qty" not in r: continue
    q = f"{r['qty']:>3}{r['unit']:<3}" if r["qty"] else "      "
    a = f"{r['qty']*r['price']:>10,}" if r["qty"] else ""
    print(f"  {r['name'][:40]:42}{q}{a}")
print(f"\n{'小　計（純工事費）':18}{sub:>10,}")
print(f"{'運搬費':18}{u_amt:>10,}   （純工事費×{UNPAN_RATE}%）")
print(f"{'諸経費':18}{k_amt:>10,}   （純工事費×{KEIHI_RATE}%＋端数調整 {k_amt-k_raw}）")
print(f"{'合計（税抜）':18}{net:>10,}")
assert net % 1000 == 0, net

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
lp = os.path.join(out, "取込リンク_大乗教_高圧受電設備.txt")
open(lp, "w").write(url + "\n")
print("URL長", len(url))

qdir = os.path.join(out, "..", "q"); os.makedirs(qdir, exist_ok=True)
json.dump(j, open(os.path.join(qdir, "daijokyo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
short = "https://kawaguchidenki001.github.io/kd-mitsumori/#q=daijokyo"
open(lp, "a").write(short + "\n")
print("短いリンク", short)
