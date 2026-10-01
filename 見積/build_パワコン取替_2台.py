# -*- coding: utf-8 -*-
"""河村様　パワーコンディショナ取替工事（2台）
   元：Kの見積 No.260815（R8.9.29 パワーコンディショナ取替工事（7台））を 2台分に減らしたもの。
   単価は元見積のまま。パワコン間ケーブルは 7台で6本（数珠つなぎ）→ 2台では1本。
   遠隔監視の再設定・系統連系手続きは台数によらず 1式のまま。
   元見積と同じく 法定福利費は立てず、諸経費 11.1%（計を1,000円単位に丸める）。
"""
import json, base64, math
def jsround(x): return math.floor(x + 0.5)
def sig(v):
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

N = 2
rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": price, "note": ""})
    return qty * price

sub = 0
# 内訳は要約して短く（Kの指示）。据付・金具・配線接続替え・パワコン間ケーブル布設を「取付工事」1行に、
# 監視再設定と連系手続きを1行にまとめる。計は元の 1,155,000 のまま（差は諸経費の adj で吸収）
TORITSUKE = (41_500 + 12_400 + 20_700) * N + 8_290 * (N - 1)    # 157,490
cat("01　機器材料")
sub += it("パワーコンディショナ", "EHF-S99MP5B 三相9.9kW", N, "台", 380_000)
sub += it("パワコン間ケーブル", "ZC-PP03 3m", N - 1, "本", 6_400)
cat("02　取替工事")
sub += it("パワコン取付工事", "据付・金具・配線接続替え共", N, "台", sig(TORITSUKE / N))
sub += it("監視設定・連系手続き", "遠隔監視再設定・電力会社協議共", N, "台", sig(91_500 / N))   # 台数で割る（Kの指示）
sub += it("既設パワコン撤去", "EPC-S99MP5-CL", N, "台", 12_400)

cat("経　費")
KEIHI = 11.1
k_raw = jsround(sub * KEIHI / 100)
TARGET = 1_155_000   # 元の計のまま
rows.append({"name": "諸経費", "rate": KEIHI, "adj": (TARGET - sub) - k_raw})

data = {"header": {"name": "パワーコンディショナ取替工事（2台）", "client": "河村", "honorific": "様",
                   "date": "2026-10-01", "staff": "河口", "no": "261002"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_パワコン取替_2台.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/pcs-2dai.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in rows:
    if r.get("type") == "cat": print("【" + r["name"] + "】"); continue
    if "qty" in r: print(f"  {r['name'][:22]:24}{r['qty']:>3}{r['unit']:<3}{r['price']:>9,}{r['qty']*r['price']:>11,}")
tax = jsround(TARGET * 0.1)
print(f"小計 {sub:,}／諸経費 {TARGET-sub:,}／計（税抜）{TARGET:,}／税込 {TARGET+tax:,}")
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_パワコン取替_2台.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=pcs-2dai\n")
