# -*- coding: utf-8 -*-
"""市民会館大ﾎｰﾙ1階南ﾄｲﾚ電気工事（戸島工業株式会社 御中）R8.11.25
   Kの指示：過去の見積 No.260113（R8.1.14「市民会館大ﾎｰﾙ1階北男子ﾄｲﾚ洗浄便座取付」計 120,000）を参考に作る。
     単価は把握しているもの（積算単価DB：tanka-search の unit_prices.json）に直す。
     変更：EM-EEF1.6-3C 15ｍ／EM-EEF2.0-3C 削除／メタルモール MM-A 6ｍ／ジャンクションボックス MM-A 1個追加／
           コンセント 1個／ジョイントボックス 削除。そのほか（付属品・スイッチボックス2・コーナーボックス2）は過去の見積のまま。
   書き方は過去の見積のとおり：材料の単価 → 電工費 1式 → 雑費 1式 → 諸経費 1式、税抜（消費税は含まれておりません）。
   材料単価：DB の材料費（ロス込み）を上3桁（10円未満は10円単位）に。
     EM-EEF1.6-3C 管内 236／1種金属線ぴ A型 704／スイッチボックス 1個用 深形 906／
     ★コーナーボックス：DB に A型用が無いので「ボックス 直角2方出 30」1,183／ジャンクションボックス 角形 A型 1,306／
     埋込コンセント 2P15A×1 接地極・接地端子付 金属製プレート共 745。
     同上付属品は過去の見積と同じ比率（メタルモールの 1,660÷4,400）。
   R8.11.25 Kの指示：コンセントの下に「既設メタルモール、ボックス等脱着・加工（電工費に含む）」「既設配線切替（電工費に含む）」を追加、電工費 76,000。
   電工費（当初）：DB の歩掛の労務費（公共工事の電工 28,200/人工 ベース）×1.4（当社の 39,480/人工）を 1,000円単位に。
   雑費 約5%・諸経費 約10%、計は 1,000円単位に切り捨て（諸経費は 1,000円単位、端数は雑費で合わせる。過去の見積と同じ形）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v); step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

rows = []
def it(name, qty, unit, price, note=""):
    rows.append({"name": name, "spec": "", "qty": qty, "unit": unit, "price": int(price), "note": note})
    return qty * int(price)

# (名称, 数量, 単位, DB材料費, DB労務費, メモ)
MAT = [
    ("ケーブル　EM-EEF1.6-3C", 15, "ｍ", 236, 479, "DB 耐火ケーブル EM-EEF1.6-3C 管内"),
    ("メタルモール　MM-A", 6, "ｍ", 704, 1_974, "DB 1種金属線ぴ A型"),
    ("スイッチボックス　MM-A", 2, "個", 906, 2_820, "DB 線ぴ用スイッチボックス 1個用 深形"),
    ("コーナーボックス　MM-A", 2, "個", 1_183, 2_820, "★DB ボックス 直角2方出 30（A型用が無いので近いもの）"),
    ("ジャンクションボックス　MM-A", 1, "個", 1_306, 2_820, "DB ジャンクションボックス 角形 A型（Kの指示で追加）"),
    ("コンセント　1ET　新金プレート含む", 1, "個", 745, 1_889, "DB 埋込コンセント 2P15A×1 接地極・接地端子付 金属製プレート共"),
]
s = 0; labor = 0
for i, (nm, q, u, mat, lab, memo) in enumerate(MAT):
    s += it(nm, q, u, sig(mat), memo)
    labor += q * lab
    if i == 1:   # メタルモールの直後に「同上付属品」（過去の見積と同じ比率）
        mm = q * sig(mat)
        s += it("同上付属品", 1, "式", jsround(mm * 1_660 / 4_400 / 10) * 10, "メタルモールの金額×1,660/4,400（過去の見積の比率）")
mat_total = s
# R8.11.25 Kの指示：コンセントの下に「既設メタルモール、ボックス等脱着・加工」「既設配線切替」（どちらも電工費に含む・金額なし）
for nm in ("既設メタルモール、ボックス等脱着・加工（電工費に含む）", "既設配線切替（電工費に含む）"):
    rows.append({"name": nm, "spec": "", "qty": "", "unit": "", "price": 0, "note": "", "ref": True})
DENKO = 76_000          # R8.11.25 Kの指示（当初は DB の労務費×1.4＝49,000）
s += it("電工費", 1, "式", DENKO, f"Kの指示 76,000（DB の労務費 {labor:,}×1.4＝{jsround(labor*1.4/1000)*1000:,}）")
TOTAL = int(s * 1.05 * 1.10) // 1000 * 1000          # 雑費 約5%・諸経費 約10%、1,000円単位に切り捨て
SHOKEIHI = jsround((TOTAL - TOTAL / 1.10) / 1000) * 1000
ZAPPI = TOTAL - s - SHOKEIHI
s += it("雑費", 1, "式", ZAPPI, "約5%（計を1,000円単位にする端数調整を含む）")
s += it("諸経費", 1, "式", SHOKEIHI, "約10%")
assert s == TOTAL

data = {"header": {"name": "市民会館大ﾎｰﾙ1階南ﾄｲﾚ電気工事", "client": "戸島工業株式会社", "honorific": "御中",
                   "date": "2026-11-25", "staff": "河口", "no": ""},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
fname = "戸島工業_市民会館大ホール1階南トイレ電気"; qname = "shiminkaikan-minami-toilet"
json.dump(data, open(f"{root}/見積/見積_{fname}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(f"{root}/q/{qname}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(f"{root}/見積/取込リンク_{fname}.txt", "w").write(url + f"\nhttps://kd-mitsumori.pages.dev/#q={qname}\n")
for r in rows:
    if r.get("ref"): print("  " + r["name"]); continue
    print(f"  {r['name'][:26]:28}{r['qty']:>3}{r['unit']}{r['price']:>8,}{r['qty']*r['price']:>9,}  {r['note']}")
print(f"材料計 {mat_total:,}／計（税抜）{TOTAL:,}")
