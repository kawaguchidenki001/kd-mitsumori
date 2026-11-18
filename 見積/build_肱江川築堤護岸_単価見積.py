# -*- coding: utf-8 -*-
"""令和7年度 肱江川築堤護岸工事　単価見積（木曽川下流河川事務所長 様）No.260711
   元：Kの見積 No.260711（R8.7.8、計 1,272,520）。R8.11.17 Kの指示「確認して直して」：発注者の「見積依頼 一覧」と
   その赤書き（宛名・工事名・工事場所・有効期限）、赤枠（クロージャの3行 → 見積依頼の「配線工／クロージャ固定金具」の8品目）。
   見積依頼の記載事項：作成年月日を記載／宛名は『木曽川下流河川事務所長』／納入場所は現場（現着単価）／有効期限（工期末）／税抜き単価。
   単価：元の見積と同じく 扇港電機の NET×1.3（100円未満切り捨て）。
     クロージャ固定金具の部品は 扇港電機（決定）見積 No.26090626（R8.9.10、古河電工）の NET：
       接続材受金物 L900 10,600／ケーブル受金物 13,100／ケーブル受平鋼 19,500／光ケーブル支持金物（2条用）9,300。数量も同見積のとおり。
     ★は同見積に無いもの（概算）：接続点銘板・ケーブル銘板（アクリル板）、M12全ネジボルト、スパイラルスリーブ。
   R8.11.18 Kの指示：1枚目の赤枠＝クロージャ固定金具（74,000）の内訳 → クロージャ本体・再接続材は元のまま戻し、固定金具 74,000 を8品目に振り分けた。
   ハンドホールの「参考質量●●kg」は質量が分からないので未記入（メーカーに確認）。
"""
import json, base64, math

def up13(net): return int(math.floor(net * 1.3 / 100) * 100)   # NET×1.3、100円未満切り捨て

rows = []
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note})
    return qty * int(price)

s = 0
s += it("さや管", "IF28", 524, "ｍ", 520, "NET400×1.3")
s += it("クロージャ", "小型用", 1, "組", 78_000, "NET60,000×1.3（R8.7.8 のまま）")
# R8.11.18 Kの指示：見積依頼の1枚目の赤枠（8品目）は「クロージャ固定金具 SUS製（74,000）」の内訳 → 74,000 を8品目に振り分ける
#   振り分けの比：古河電工の部品は（決定）見積 R8.9.10 の NET×1.3、銘板・全ネジボルト・スパイラルスリーブは概算（★）。合計を 74,000 ちょうどに。
FIX_TOTAL = 74_000
FIX = [  # (名称, 規格, 数量, 単位, 比の基にする単価, メモ)
    ("接続点銘板", "アクリル板", 1, "枚", 3_500, "★"),
    ("ケーブル銘板", "アクリル板", 2, "枚", 2_000, "★"),
    ("ケーブル受金物", "L型　SUS304", 2, "本", up13(13_100), "古河電工 NET13,100"),
    ("接続材受金物", "SUS304　L=900", 1, "本", up13(10_600), "古河電工 NET10,600"),
    ("ケーブル支持金物", "2条用　SUS304", 2, "個", up13(9_300), "古河電工 光ケーブル支持金物 NET9,300"),
    ("M12全ネジボルト", "SUS304　L=80", 4, "本", 600, "★ナット・座金共"),
    ("ケーブル受平鋼", "SUS304　L=600", 2, "本", up13(19_500), "古河電工 NET19,500"),
    ("スパイラルスリーブ", "30mm用", 2, "ｍ", 800, "★"),
]
base = sum(q * b for _, _, q, _, b, _ in FIX)
def rnd(v): return int(round(v / 100) * 100) if v >= 1_000 else int(round(v / 10) * 10)
price = [rnd(b * FIX_TOTAL / base) for _, _, q, _, b, _ in FIX]
price[3] += FIX_TOTAL - sum(q * p for (_, _, q, _, _, _), p in zip(FIX, price))   # 端数は接続材受金物（数量1）で合わせる
# 代価表の形：固定金具 1組 74,000 を単価欄に出し（金額欄は空欄・合計に入れない）、その下に内訳8品目
rows.append({"name": "クロージャ固定金具", "spec": "SUS製（下記内訳）", "qty": 1, "unit": "組", "price": FIX_TOTAL, "note": "内訳の計", "ref": True})
fix_sum = 0
for (nm, sp, q, u, b, memo), pr in zip(FIX, price):
    fix_sum += it(nm, sp, q, u, pr, f"74,000 を振り分け（{memo}）")
assert fix_sum == FIX_TOTAL
s += fix_sum
s += it("クロージャ再接続材", "小型用", 1, "組", 36_400, "NET28,000×1.3（R8.7.8 のまま）")
s += it("ハンドホール", "1200×600×650", 1, "基", 149_000, "共和コンクリート NET115,000×1.3")
s += it("ハンドホール蓋", "1200×600　歩道用　シリンダー錠付", 1, "枚", 569_000)
s += it("配管接続材", "FEP80-SGP80A", 2, "ケ所", 7_800, "NET6,000×1.3")
s += it("配管接続材", "FEP80-FEP80", 2, "ケ所", 1_820, "NET1,400×1.3")
s += it("インナーフレキ固定バンド", "IF-28B 同等品以上", 8, "個", 4_900, "NET3,800×1.3")
s += it("インナーフレキ壁面リング", "IF-80R-MA 同等品以上", 4, "個", 8_800, "NET6,800×1.3")
rows.append({"name": "　（ボルト・ナット含む）", "spec": "", "qty": "", "unit": "", "price": 0, "note": "", "ref": True})

data = {"header": {"name": "令和7年度　肱江川築堤護岸工事", "client": "木曽川下流河川事務所長", "honorific": "様",
                   "date": "2026-11-18", "staff": "河口", "no": "260711"},
        "place": "三重県桑名市香取地内", "validity": "工期末", "remarks": "見積有効期限：工期末",   # KD見積の帳票には有効期限の欄が無いので備考に書く
        "notes": ["納入場所は現場です（単価は現着単価です）"],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_肱江川築堤護岸_単価見積.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/hijiegawa-tanka.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_肱江川築堤護岸_単価見積.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=hijiegawa-tanka\n")
for r in rows:
    if r.get("ref"): print(f"  {r['name']} {r['spec']}　{r['qty']}{r['unit']} {r['price']:,}（内訳表示）" if r["price"] else "  " + r["name"]); continue
    print(f"  {(r['name']+' '+r['spec'])[:34]:36}{r['qty']:>4}{r['unit']}{r['price']:>9,}{r['qty']*r['price']:>10,}  {r['note']}")
print(f"計（税抜）{s:,}")
