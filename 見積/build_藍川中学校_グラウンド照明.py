# -*- coding: utf-8 -*-
"""藍川中学校グラウンド照明設備工事（岐阜市長 柴橋正直 御中）
   R8.1.23 の城西小学校グラウンド照明（No.260129）を雛形に、学校名を藍川中学校へ。
   単価・数量は雛形どおり。日付はご指示により令和8年9月4日。
   諸経費は KD見積の集計行（小計の下に「1 式」）とし、金額は雛形と同額 69,000円。
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
sub += it("LED投光器",      "LD-240D",       7, "台", 32_000)
sub += it("落下防止ワイヤー", "JD-004K",       7, "個",    900)
sub += it("アイボルト",      "SUS　M12",      7, "個",  1_100)
sub += it("リングキャッチ",   "SUS　M6",       7, "個",    550)
sub += it("投光器取付架台",   "PDP2221",       3, "組", 11_100)
sub += it("取付台座",       "TFB-13901N",    7, "個",  7_200)
sub += it("ケーブル",       "CVV2sq-3c",    10, "ｍ",    250)
sub += it("電線管",        "支持材含む",       1, "式",  8_750)
sub += it("メタルハライドランプ", "MF700LS/BH",  4, "個", 14_600)
sub += it("雑材・消耗品",     "",             1, "式",  9_800)
sub += it("取替工料",       "",              1, "式", 212_000, 1.00)   # 全額が労務費
sub += it("高所作業車使用",   "",              1, "日",  37_000)
sub += it("撤去品処分費",     "",             1, "式",  27_000)

# 諸経費：雛形の 69,000円 に合わせる（純工事費 681,000×10％＋端数調整）
KEIHI_RATE = 10.0
k_amt = 69_000
rows.append({"name": "諸経費", "rate": KEIHI_RATE,
             "adj": k_amt - jsround(sub * KEIHI_RATE / 100)})
net = sub + k_amt

j = {"header": {"name": "藍川中学校グラウンド照明設備工事",
                "client": "岐阜市長　柴橋正直", "honorific": "御中",
                "date": "2026-09-04", "staff": "河口", "no": "260904"},
     "place": "藍川中学校", "validity": "", "remarks": "", "addrKind": "public",
     "taxMode": "out", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(out, "見積_藍川中学校_グラウンド照明設備工事.json")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:30]:32}{r['qty']:>4}{r['unit']:<3}{r['price']:>9,}{r['qty']*r['price']:>11,}")
tax = jsround(net * 0.1)
print(f"\n{'小　計（純工事費）':20}{sub:>12,}\n{'諸経費':20}{k_amt:>12,}")
print(f"{'計（税抜）':20}{net:>12,}\n{'消費税10%':20}{tax:>12,}\n{'合　計':20}{net+tax:>12,}")
assert (sub, net, net + tax) == (681_000, 750_000, 825_000), (sub, net)
lab = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
print(f"（参考）労務費 {lab:,}円／×16.5%＝法定福利費 {jsround(lab*0.165):,}円")

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(os.path.join(out, "取込リンク_藍川中学校.txt"), "w").write(url + "\n")
print("URL長", len(url))

# ---- 短い取込リンク（q/aikawa.json をサイトに置き、#q=aikawa で開く） SHORT LINK ----
qdir = os.path.join(out, "..", "q"); os.makedirs(qdir, exist_ok=True)
json.dump(j, open(os.path.join(qdir, "aikawa.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
short = "https://kawaguchidenki001.github.io/kd-mitsumori/#q=aikawa"
open(os.path.join(out, "取込リンク_藍川中学校.txt"), "a").write(short + "\n")
print("短いリンク", short)
