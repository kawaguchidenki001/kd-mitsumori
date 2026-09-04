# -*- coding: utf-8 -*-
"""羽島民泊換気扇取替工事（株式会社ファーストクラス 御中）
   脱衣所の天井埋込ダクト用換気扇1台を取替。
   既設：三菱電機 VD-13ZC10（2019年製・100V 13/15.5W）＝運転音大
   新設：同シリーズ現行機 VD-13ZC14（φ100・開口177角で既設と互換）
   器具単価は products.json の定価 24,600円×0.7（掛率のご指示があれば差し替え）。
"""
import json, base64, os, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    """単価の丸め：1,000円以上は上3桁・100円台は上2桁・10円台は上1桁で切上げ。"""
    v = float(v)
    if v <= 0: return 0
    n = 3 if v >= 1000 else 2 if v >= 100 else 1 if v >= 10 else 0
    if n == 0: return int(math.ceil(v))
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - n)
    return int(math.ceil(round(v / step, 9))) * step

rows = []
def it(name, spec, qty, unit, price, note="", lr=0.0):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if lr: r["pl"] = int(round(price * lr))
    rows.append(r)
    return qty * int(price)

TEIKA = 24_600                      # 三菱電機 VD-13ZC14 定価（products.json）
KAKERITSU = 0.70

sub = 0
sub += it("換気扇", "三菱電機　VD-13ZC14　φ100　天井埋込形ダクト用（低騒音形）",
          1, "台", sig(TEIKA * KAKERITSU), f"定価{TEIKA:,}円×{KAKERITSU:.2f}（上3桁切上げ）")
sub += it("換気扇取替手間", "既設撤去・新設取付・試運転共", 1, "台", 18_000, "", 1.00)
sub += it("撤去品処分費", "", 1, "式", 2_000)
sub += it("雑材・消耗品", "", 1, "式", 1_500)

# 経費（法定福利費＝労務費×16.5%／諸経費＝純工事費×12%。どちらも1,000円単位）
labor = sum(r["qty"] * r.get("pl", 0) for r in rows)
WELFARE_RATE, KEIHI_RATE = 16.5, 12.0
w_raw = jsround(labor * WELFARE_RATE / 100)
w_amt = w_raw // 1000 * 1000
k_raw = jsround(sub * KEIHI_RATE / 100)
TARGET = (sub + w_amt + k_raw) // 1000 * 1000        # 計（税抜）を1,000円単位（切捨て）
k_amt = TARGET - sub - w_amt                         # 端数は諸経費で吸収
rows.append({"name": "法定福利費", "welfare": WELFARE_RATE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費",     "rate": KEIHI_RATE,     "adj": k_amt - k_raw})
net = TARGET

j = {"header": {"name": "羽島民泊換気扇取替工事",
                "client": "株式会社ファーストクラス", "honorific": "御中",
                "date": "2026-09-04", "staff": "河口", "no": "260904"},
     "place": "", "validity": "発行日より1ヶ月", "remarks": "",
     "taxMode": "out", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
json.dump(j, open(os.path.join(out, "見積_羽島民泊_換気扇取替工事.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

for r in rows:
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:44]:46}{r['qty']:>3}{r['unit']:<3}{r['price']:>8,}{r['qty']*r['price']:>9,}")
print(f"\n{'小　計（純工事費）':18}{sub:>9,}")
print(f"{'法定福利費':18}{w_amt:>9,}   （労務費 {labor:,}×{WELFARE_RATE}%）")
print(f"{'諸経費':18}{k_amt:>9,}   （純工事費×{KEIHI_RATE}%＋端数調整）")
tax = jsround(net * 0.1)
print(f"{'計（税抜）':18}{net:>9,}\n{'消費税10%':18}{tax:>9,}\n{'合　計':18}{net+tax:>9,}")
assert net % 1000 == 0, net

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
lp = os.path.join(out, "取込リンク_羽島民泊_換気扇取替.txt")
open(lp, "w").write(url + "\n")
print("URL長", len(url))

qdir = os.path.join(out, "..", "q"); os.makedirs(qdir, exist_ok=True)
json.dump(j, open(os.path.join(qdir, "hashima-fan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
short = "https://kawaguchidenki001.github.io/kd-mitsumori/#q=hashima-fan"
open(lp, "a").write(short + "\n")
print("短いリンク", short)
