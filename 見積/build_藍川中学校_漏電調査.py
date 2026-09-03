# -*- coding: utf-8 -*-
"""藍川中学校グラウンド照明漏電調査（岐阜市長 柴橋正直 様）
   R8.2.24 の明郷小学校グラウンド照明漏電調査（No.260219）と同内容で学校名のみ変更。
   日付はご指示により令和8年9月3日。宛先が官公庁のため自社住所は公共用。
"""
import json, base64, os, math

def jsround(x): return math.floor(x + 0.5)
rows = []
def it(name, spec, qty, unit, price, lr=0.0):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": ""}
    if lr: r["pl"] = int(round(price * lr))
    rows.append(r)
    return qty * int(price)

sub = 0
sub += it("絶縁不良調査及び作業費", "", 1, "式", 15_000, 1.00)   # 全額が労務費
sub += it("高所作業車使用費",     "", 1, "式", 15_000)

KEIHI_RATE = 10.0
k_amt = 3_000
rows.append({"name": "諸経費", "rate": KEIHI_RATE,
             "adj": k_amt - jsround(sub * KEIHI_RATE / 100)})
net = sub + k_amt

j = {"header": {"name": "藍川中学校グラウンド照明漏電調査",
                "client": "岐阜市長　柴橋正直", "honorific": "様",
                "date": "2026-09-03", "staff": "河口", "no": "260903"},
     "place": "藍川中学校", "validity": "", "remarks": "", "addrKind": "public",
     "taxMode": "out", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
json.dump(j, open(os.path.join(out, "見積_藍川中学校_グラウンド照明漏電調査.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

for r in rows:
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:26]:28}{r['qty']:>3}{r['unit']:<3}{r['price']:>9,}{r['qty']*r['price']:>10,}")
tax = jsround(net * 0.1)
print(f"\n{'小　計（純工事費）':18}{sub:>10,}\n{'諸経費':18}{k_amt:>10,}")
print(f"{'計（税抜）':18}{net:>10,}\n{'消費税10%':18}{tax:>10,}\n{'合　計':18}{net+tax:>10,}")
assert (sub, net, net + tax) == (30_000, 33_000, 36_300), (sub, net)
lab = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
print(f"（参考）労務費 {lab:,}円／×16.5%＝法定福利費 {jsround(lab*0.165):,}円")

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
lp = os.path.join(out, "取込リンク_藍川中学校_漏電調査.txt")
open(lp, "w").write(url + "\n")
print("URL長", len(url))

# ---- 短い取込リンク（q/aikawa-roden.json） SHORT LINK ----
qdir = os.path.join(out, "..", "q"); os.makedirs(qdir, exist_ok=True)
json.dump(j, open(os.path.join(qdir, "aikawa-roden.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
short = "https://kawaguchidenki001.github.io/kd-mitsumori/#q=aikawa-roden"
open(lp, "a").write(short + "\n")
print("短いリンク", short)
