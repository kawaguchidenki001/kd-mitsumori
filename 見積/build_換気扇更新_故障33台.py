# -*- coding: utf-8 -*-
"""有圧換気扇 故障機器 33台 更新（R8.10.30）
   資料：1階・2階平面図（故障機器を赤字、番号①～㉝）、換気設備 機器表（三菱 有圧換気扇 低騒音形 3φ200V、丸数字は Kの書込み）。
   番号と機器：給気（VS）13台・排気（VE）20台
     ①② VS-104'、③ VS-103（下段）、④ VS-110（下段）、⑤ VS-101、⑨⑩⑪ VS-201、⑳㉑ VS-105'、㉒㉓ VS-105、㉔ VS-107
     ⑥⑦ VE-201、⑧⑫ VE-113、⑬⑭ VE-112、⑮⑯⑰ VE-104'、⑱ VE-104、⑲ VE-105'、㉕ VE-107、
     ㉖㉗㉙㉚㉛ VE-103'、㉘ VE-103、㉜ VE-110'、㉝ VE-102
   範囲：本体の取替え（既設撤去・新設取付・結線の脱着・試運転）。取付枠・ウェザーカバー・シャッター・フィルター等の付属品は既設流用。
   単価：
     ・本体 ★定価は未確認のため仮（三菱 産業用有圧換気扇 三相200V の概算）×0.7。商社見積が来たら差し替える。
     ・取替え工事：設備機械工 29,000×（取付 0.5～0.7人＋撤去はその5割）×1.25（その他）、羽根径で 3段階（公共建築工事積算基準 40cm 0.58人）。
     ・結線：積算マニュアル 電動機結線 直入始動方式 7,210＋撤去 2,160。
     ・高所作業車（VS-201・VE-201・嵩天部 VE-112・113）★2日、撤去品処分、試運転調整。
   R8.10.30 Kの指示：材料（有圧換気扇本体）は支給 → 本体の金額を外し、取替え工事・結線脱着だけ。注記に「支給品」と書く。
   経費：法定福利費 16.5%（労務費は取替え工事＋結線、100円単位）、諸経費 12%、計を1,000円単位に（諸経費の adj）。
   宛名：戸島工業株式会社、工事名：換気設備 有圧換気扇更新工事（R8.10.30 Kの指示）。見積Noは新規（空欄＝アプリが採番）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

KAKE = 0.7
KIKAI = 29_000                     # 設備機械工
def koji(size):                    # 取替え工事（撤去＋取付）
    n = 0.5 if size <= 35 else (0.58 if size == 40 else 0.7)
    return KIKAI * n * 1.5 * 1.25
KESSEN = 7_210 + 2_160             # 結線 脱着

# (型式, 区分, 羽根径cm, ★定価, 台数, 機器番号)
UNITS = [
    ("EG-50ETB3-Q", "給気", 50, 140_000, 6, "VS-104'・105・105'（①②⑳㉑㉒㉓）"),
    ("EG-45DTB3-Q", "給気", 45, 115_000, 1, "VS-101（⑤）"),
    ("EF-45ETB3-Q", "給気", 45,  98_000, 2, "VS-103・110 下段（③④）"),
    ("EF-25ATB3-Q", "給気", 25,  48_000, 1, "VS-107（㉔）"),
    ("EWG-50ETA",   "給気", 50, 160_000, 3, "VS-201 上部（⑨⑩⑪）"),
    ("EG-50ETB3",   "排気", 50, 140_000, 6, "VE-103'・110'（㉖㉗㉙㉚㉛㉜）"),
    ("EG-50DTB3",   "排気", 50, 130_000, 4, "VE-104'・105'（⑮⑯⑰⑲）"),
    ("EG-45DTB3",   "排気", 45, 115_000, 1, "VE-104（⑱）"),
    ("EF-45ETB3",   "排気", 45,  98_000, 1, "VE-103（㉘）"),
    ("EF-35CTB3",   "排気", 35,  66_000, 1, "VE-102（㉝）"),
    ("EG-40BTB3",   "排気", 40,  90_000, 5, "VE-107・112・113（㉕⑬⑭⑧⑫）"),
    ("EWG-50ETA",   "排気", 50, 160_000, 2, "VE-201 上部（⑥⑦）"),
]
assert sum(u[4] for u in UNITS) == 33

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
s = 0
for kubun in ("給気", "排気"):
    cat(f"有圧換気扇 更新（{kubun}ファン）")
    for model, kb, size, teika, q, where in UNITS:
        if kb != kubun: continue
        work = koji(size) + KESSEN
        price = sig(work)                    # R8.10.30 本体は支給品（材料費なし）
        bango = where.split("（")[0]          # 見積書には機器番号だけ（丸数字は備考に）
        rows.append({"name": f"有圧換気扇取替　{model}", "spec": f"{size}cm　{bango}", "qty": q, "unit": "台",
                     "price": price, "pl": jsround(work * 0.8),
                     "note": f"{where}　取替え工事{jsround(koji(size)):,}＋結線脱着{KESSEN:,}（本体支給）"})
        s += q * price

cat("共通")
KOSHO = 70_000                    # ★高所作業車 2日（回送共）
SHOBUN = 33 * 2_000               # 撤去品処分
SHIUNTEN = sig(KIKAI * 0.5 * 1.25)
for nm, sp, q, u, p, pl, note in [
    ("高所作業車", "VS-201・VE-201・嵩天部 ほか　2日", 1, "式", KOSHO, 0, "★回送共"),
    ("撤去品処分費", "有圧換気扇 33台", 1, "式", SHOBUN, 0, "2,000×33"),
    ("試運転調整", "33台", 1, "式", SHIUNTEN, SHIUNTEN * 0.8, "設備機械工 0.5人"),
]:
    rows.append({"name": nm, "spec": sp, "qty": q, "unit": u, "price": int(p), "note": note, **({"pl": jsround(pl)} if pl else {})})
    s += q * int(p)

labor = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
k_raw = jsround(s * KEIHI / 100)
TOTAL = (s + w_amt + k_raw) // 1000 * 1000
cat("経　費")
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": TOTAL - s - w_amt - k_raw})

data = {"header": {"name": "換気設備 有圧換気扇更新工事", "client": "戸島工業株式会社", "honorific": "御中",
                   "date": "2026-10-30", "staff": "河口", "no": ""},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "", "notes": ["有圧換気扇本体は支給品とし、取替え工事のみです"],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_換気扇更新_故障33台.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/yuatsu-koshin33.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_換気扇更新_故障33台.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=yuatsu-koshin33\n")
sub, cur = {}, None
for r in rows:
    if r.get("type") == "cat": cur = r["name"]; print("【" + cur + "】"); continue
    if "qty" in r:
        a = r["qty"] * r["price"]; sub[cur] = sub.get(cur, 0) + a
        print(f"  {(r['name']+' '+r['spec'])[:46]:48}{r['qty']:>3}{r['unit']}{r['price']:>9,}{a:>11,}  {r['note']}")
for k, v in sub.items(): print(f"{k} 計 {v:,}")
print(f"小計 {s:,}／法定福利費 {w_amt:,}（労務費 {labor:,}）／諸経費 {TOTAL - s - w_amt:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}")
