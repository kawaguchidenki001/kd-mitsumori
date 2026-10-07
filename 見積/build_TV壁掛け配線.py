# -*- coding: utf-8 -*-
"""テレビ壁掛け用 配線工事（R8.10.7）
   現状：コンセント・テレビ端子が FL+250。テレビを壁掛けにするため FL+1200 程度に新設。
   ブルーレイレコーダーは下に残るので FL+250 のコンセント・テレビ端子はそのまま使い、
   レコーダー→テレビの HDMI を壁内に通す（5m、Kの指示）。
   単価は材工共・1ケ所あたり（配線・器具・ボックス共、Kの標準）。用紙1枚、法定福利費なし。
   雑材消耗品で端数調整（Kの標準）：小計を1万円単位、諸経費10%ちょうど。
"""
import json, base64, math
def jsround(x): return math.floor(x + 0.5)

rows = []
def it(name, spec, qty, unit, price, pl=0):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": ""}
    if pl: r["pl"] = int(pl)
    rows.append(r); return qty * int(price)
s = 0
# コンセント：住宅用ボックス4,300＋コンセント（埋込2口E付）約3,000＋VVF1.6-2C 2m＋既設壁の開口・通線
s += it("コンセント増設", "ＦＬ＋１２００ 既設より分岐 壁内隠ぺい", 1, "ヶ所", 12_000, 8_000)
# テレビ端子：2分配器（既設ボックス内）＋テレビ端子＋S-5C-FB 2m・F接栓＋ボックス
s += it("テレビ端子増設", "ＦＬ＋１２００ ２分配器・同軸ケーブル共", 1, "ヶ所", 18_000, 10_000)
# HDMI：4K対応5m＋ケーブル出線プレート上下（FL+250・FL+1200）＋壁内通線
s += it("ＨＤＭＩ配線", "４Ｋ対応 ５ｍ 壁内隠ぺい 出線プレート上下共", 1, "式", 18_000, 10_000)
KEIHI = 10.0
S = -(-int(s * 1.03) // 10_000) * 10_000          # 3%程度を足して1万円単位（小額のため切上げ）
s += it("雑材消耗品", "", 1, "式", S - s)
rows.append({"name": "諸経費", "rate": KEIHI, "adj": 0})
TARGET = s + jsround(s * KEIHI / 100)
assert TARGET % 1000 == 0

data = {"header": {"name": "テレビ壁掛け用 配線工事", "client": "", "honorific": "様",
                   "date": "2026-10-07", "staff": "河口", "no": "261007"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_TV壁掛け配線.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/tv-kabekake.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_TV壁掛け配線.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=tv-kabekake\n")
for r in rows:
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:34]:36}{r['qty']:>2}{r['unit']:<3}{r['price']:>8,}")
print(f"小計 {s:,}／諸経費 {TARGET-s:,}／計（税抜）{TARGET:,}／税込 {TARGET+jsround(TARGET*0.1):,}")
