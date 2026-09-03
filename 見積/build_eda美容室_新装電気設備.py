# -*- coding: utf-8 -*-
"""eda美容室新装電気設備工事（株式会社廣瀬住建 御中）
   R8.7.29 発行の紙見積（No.260725）をKD見積へ移し、数量・追加項目をご指示どおり改訂。
   pl（労務費相当）は法定福利費を後から足せるように参考値として持たせてある。
"""
import json, base64, os, math

rows = []
def it(name, spec, qty, unit, price, lr=0.0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if lr: r["pl"] = int(round(price * lr))
    rows.append(r)
    return qty * int(price)

net = 0
net += it("電灯配線",         "",                    10, "カ所", 2_800, 0.75)
net += it("電灯配線",         "引掛",                  1, "カ所", 3_000, 0.75)
net += it("コンセント",       "2口",                  5, "箇所", 4_500, 0.60)
net += it("コンセント",       "1E",                   1, "個",  4_500, 0.60)
net += it("専用回路コンセント", "",                     5, "箇所", 11_000, 0.65)
net += it("コンセント差額",    "Sプレート",              4, "個",    800, 0.10)
net += it("片切スイッチ",     "",                    12, "箇所", 4_800, 0.60)
net += it("3路スイッチ",      "",                     2, "箇所", 6_800, 0.60)
net += it("回路配線",         "",                     4, "回路", 6_500, 0.70)
net += it("配線ダクトレール",  "2m",                   2, "カ所", 13_000, 0.35)
net += it("配線ダクトレール",  "3m",                   4, "カ所", 19_500, 0.35)
net += it("ダクトレール吊り金具", "",                   1, "式",  50_000, 0.50)
net += it("スポットライト",    "LGS3511VLB1",         27, "台",  10_400, 0.20)
net += it("ダウンライト",      "LGD1111VLB1",          5, "台",   6_500, 0.20)
net += it("テープライト",      "1.5m　温白色",          1, "台",  13_000, 0.20)
net += it("分電盤取付",       "ELB50A　14回路",        1, "台",  58_000, 0.35)
net += it("雑材・消耗品",     "",                     1, "式",  33_100)
net += it("中電申請手続費",    "",                     1, "式",  34_000)
net += it("運搬費",          "",                     1, "式",  35_000)
net += it("諸経費",          "",                     1, "式",  80_000)

j = {"header": {"name": "eda美容室新装電気設備工事",
                "client": "株式会社廣瀬住建", "honorific": "御中",
                "date": "2026-07-29", "staff": "河口", "no": "260725"},
     "place": "", "validity": "発行日より1ヶ月", "remarks": "",
     "taxMode": "out", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(out, "見積_eda美容室_新装電気設備工事.json")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    print(f"  {(r['name']+'　'+r['spec']).strip()[:34]:36}{r['qty']:>4}{r['unit']:<4}{r['price']:>9,}{r['qty']*r['price']:>11,}")
tax = math.floor(net * 0.1 + 0.5)
print(f"\n{'小計（税抜）':20}{net:>12,}\n{'消費税10%':20}{tax:>12,}\n{'合　計':20}{net+tax:>12,}")
lab = sum(r["qty"] * r.get("pl", 0) for r in rows)
print(f"（参考）労務費相当 {lab:,}円／×16.5%＝法定福利費 {math.floor(lab*0.165+0.5):,}円")

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(os.path.join(out, "取込リンク_eda美容室.txt"), "w").write(url + "\n")
print("URL長", len(url))

# ---- 短い取込リンク（q/eda.json をサイトに置き、#q=eda で開く） SHORT LINK ----
qdir = os.path.join(out, "..", "q"); os.makedirs(qdir, exist_ok=True)
json.dump(j, open(os.path.join(qdir, "eda.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
short = "https://kawaguchidenki001.github.io/kd-mitsumori/#q=eda"
open(os.path.join(out, "取込リンク_eda美容室.txt"), "a").write(short + "\n")
print("短いリンク", short)
