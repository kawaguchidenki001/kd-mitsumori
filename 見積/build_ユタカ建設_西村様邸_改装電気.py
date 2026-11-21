# -*- coding: utf-8 -*-
"""西村様邸改装電気工事（ユタカ建設株式会社 御中）R8.11.21
   Kの指示：内訳（各 1式）と内容の行はKの文のとおり。金額の指示は無いので概算（★）。
   単価の考え方：K の人工 28,200×（1＋0.4）＝39,480／人工 ＋ 材料（ケーブル・器具・ブレーカ等）の概算。
     ユニットバス取替：取外し再取付 0.5人工＋浴暖専用電源配線 0.5人工＋材5,000＋TV取付（電源・アンテナ線）0.5人工＋材5,000
     洗面・脱衣改装：コンセント・スイッチ移設取替 3ヶ所（材1,500＋0.15人工）＋専用電源配線 0.5人工＋材5,000＋暖房機取付 0.3人工
     トイレ改装：コンセント移設取替 1ヶ所＋電灯配線・器具取付 0.3人工＋材2,000＋スイッチ取付
     キッチン改装：IH・自動水栓 取外し再取付 0.8人工＋専用電源配線×3（材5,000＋0.4人工 ×3）＋家電コンセント4個
                   ＋既設コンセント移設取替 2ヶ所＋換気扇撤去 0.3人工＋レンジフードダクト（材15,000＋0.5人工）＋レンジフード用コンセント配線
     分電盤改修 5回路増設：分岐ブレーカ 5個（200V用含む）材15,000＋1人工
     ロスナイ取替 材工：本体 ★35,000（壁掛形 相当、機種未定）＋取替 0.5人工＋撤去品処分
   経費：諸経費 10%、計を1,000円単位に（切り捨て、諸経費の adj）。法定福利費なし。見積No は新規（空欄）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v); step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

NIN = 28_200 * 1.4                   # 39,480
rows = []
def it(name, qty, unit, price, note, lines):
    rows.append({"name": name, "spec": "", "qty": qty, "unit": unit, "price": int(price), "note": note})
    for ln in lines:
        rows.append({"name": "・" + ln, "spec": "", "qty": "", "unit": "", "price": 0, "note": "", "ref": True})
    return qty * int(price)

s = 0
UB = sig(NIN * 0.5 + (NIN * 0.5 + 5_000) + (NIN * 0.5 + 5_000))
s += it("ユニットバス取替", 1, "式", UB, "★取外し再取付0.5人工＋浴暖専用電源0.5人工＋TV取付0.5人工＋材",
        ["電源ケーブル、換気ダクト、リモコン取外し再取付", "浴暖専用電源配線、TV（支給品）取付"])
SM = sig(3 * (1_500 + NIN * 0.15) + (NIN * 0.5 + 5_000) + NIN * 0.3)
s += it("洗面、脱衣改装", 1, "式", SM, "★移設取替3ヶ所＋専用電源0.5人工＋暖房機取付0.3人工＋材",
        ["コンセント、スイッチ移設、取替", "専用電源配線、暖房機（支給品）取付"])
WC = sig((1_500 + NIN * 0.15) + (NIN * 0.3 + 2_000) + (1_500 + NIN * 0.1))
s += it("トイレ改装", 1, "式", WC, "★コンセント移設取替＋電灯配線・器具取付0.3人工＋スイッチ取付＋材",
        ["コンセント移設、取替", "電灯配線、照明器具（支給品）取付", "スイッチ取付"])
KT = sig(NIN * 0.8 + 3 * (5_000 + NIN * 0.4) + 4 * 1_500 + 2 * (1_500 + NIN * 0.15)
         + NIN * 0.3 + (15_000 + NIN * 0.5) + (3_000 + NIN * 0.2))
s += it("キッチン改装", 1, "式", KT, "★IH・水栓0.8人工＋専用回路×3＋家電コンセント4＋移設2＋換気扇撤去＋ダクト＋レンジフード電源",
        ["IH、自動水栓　取外し再取付", "専用電源配線×3（食洗器、家電コンセント×4）", "既設家電コンセント移設、取替",
         "既設換気扇撤去、レンジフードダクト配線", "コンセント配線（レンジフード）"])
rows.append({"name": "（その他）", "spec": "", "qty": "", "unit": "", "price": 0, "note": "", "ref": True})
BAN = sig(15_000 + NIN * 1.0)
s += it("分電盤改修　5回路増設", 1, "式", BAN, "★分岐ブレーカ5個 材15,000＋1人工", [])
LOS = sig(35_000 + NIN * 0.5 + 1_000)
s += it("ロスナイ取替　材・工", 1, "台", LOS, "★本体35,000（機種未定）＋取替0.5人工＋処分", [])

KEIHI = 10.0
k_raw = jsround(s * KEIHI / 100)
TOTAL = (s + k_raw) // 1000 * 1000
rows.append({"name": "諸経費", "rate": KEIHI, "adj": TOTAL - s - k_raw})

data = {"header": {"name": "西村様邸改装電気工事", "client": "ユタカ建設株式会社", "honorific": "御中",
                   "date": "2026-11-21", "staff": "河口", "no": ""},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_ユタカ建設_西村様邸_改装電気.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/nishimura-kaiso.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_ユタカ建設_西村様邸_改装電気.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=nishimura-kaiso\n")
for r in rows:
    if r.get("ref"): print("    " + r["name"]); continue
    if "qty" in r: print(f"  {r['name']:20}{r['qty']:>2}{r['unit']}{r['price']:>9,}  {r['note']}")
print(f"小計 {s:,}／諸経費 {TOTAL - s:,}（10%={k_raw:,}）／計（税抜）{TOTAL:,}／税込 {TOTAL + jsround(TOTAL * 0.1):,}")
