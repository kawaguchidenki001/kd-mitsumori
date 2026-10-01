# -*- coding: utf-8 -*-
"""河村様　パワーコンディショナ取替工事（2台）
   元：Kの見積 No.260815（R8.9.29 パワーコンディショナ取替工事（7台））を 2台分に減らしたもの。
   単価は元見積のまま。パワコン間ケーブルは 7台で6本（数珠つなぎ）→ 2台では1本。
   遠隔監視の再設定・系統連系手続きは台数によらず 1式のまま。
   元見積と同じく 法定福利費は立てず、諸経費 11.1%（計を1,000円単位に丸める）。
"""
import json, base64, math
def jsround(x): return math.floor(x + 0.5)

N = 2
rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": price, "note": ""})
    return qty * price

sub = 0
cat("01　機器材料")
sub += it("パワーコンディショナ", "EHF-S99MP5B 三相 9.9kW（ダイヤゼブラ電機）屋外形 AC202V／DC250V", N, "台", 380_000)
sub += it("パワコン間ケーブル", "ZC-PP03　3m（ダイヤゼブラ電機）", N - 1, "本", 6_400)
cat("02　取替工事")
sub += it("パワーコンディショナ　据付", "10kW以下 据付費（既設架台利用）", N, "面", 41_500)
sub += it("取付金具　製作・取付", "既設架台への新形状対応 溶融亜鉛めっき金具共", N, "組", 12_400)
sub += it("入出力配線　接続替え", "DC入力・AC出力／既設ケーブル再使用・端子処理共", N, "か所", 20_700)
sub += it("パワコン間ケーブル　布設・接続", "ZC-PP03 通信接続・動作確認共", N - 1, "か所", 8_290)
sub += it("遠隔監視ユニット　再設定", "計測ユニットのPCS登録変更・通信確認", 1, "式", 41_500)
sub += it("系統連系・保安関係手続き", "設備変更（電力会社協議・FIT事業計画変更）書類作成共", 1, "式", 50_000)
cat("03　撤去")
sub += it("既設パワーコンディショナ　撤去", "EPC-S99MP5-CL／10kW以下 撤去費", N, "面", 12_400)

cat("経　費")
KEIHI = 11.1
k_raw = jsround(sub * KEIHI / 100)
TARGET = (sub + k_raw) // 1000 * 1000
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
