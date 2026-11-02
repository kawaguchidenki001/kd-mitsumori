# -*- coding: utf-8 -*-
"""柳津生涯学習センター　照明器具改修工事（岐阜市長 柴橋正直 様）R8.11.2
   資料：岐阜市役所の FAX「LED照明器具 内訳明細書」（R8.10.27、P.005/007）。品名・品番・数量はこのとおり。
     NNLK41720J：iD 40形 LED本体 埋込 W190 連結 中用、NNLK41721J：同 右用、NNLK41722J：同 左用、
     NEL4300EN LE9：iD 40形 ライトバー 一般タイプ 3200lm 昼白色 非調光。
     → 第1会議室 4台連結×3列、第2会議室 ×2列、第3会議室 ×4列（中2・右1・左1 で1列）。
   単価：
     ・器具は パナソニック定価×0.65（照明器具の掛率。Kの指示と同じ）。定価は Web 検索（パナソニックのカタログ PDF・販売店）：
       本体 11,000（NNLK41722J は 41720J・41721J と同じ価格とみた ★）、ライトバー 23,300。
     ・取付：積算マニュアル LED埋込天井灯 ベースライト LRS6-4-30 の取付手間 12,724 → 12,700。
     ・撤去：埋込形ベースライト 撤去 4,130（文化センターロビーと同じ）。既設の台数は新設と同じとみた ★。
     ・撤去品処分費 ★：既設器具 36台・蛍光管。
   経費：諸経費 12%（岐阜市 グラウンド照明と同じ）、計を1,000円単位に（諸経費の adj）。税抜。見積No は新規（空欄）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

KAKE = 0.65
HONTAI, BAR = 11_000, 23_300
P_HON, P_BAR = sig(HONTAI * KAKE), sig(BAR * KAKE)      # 7,150 / 15,100
TORI, TEKKYO = 12_700, 4_130

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, note="", pl=0):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(pl)
    rows.append(r); return qty * int(price)

ROOMS = [("第1会議室", 3), ("第2会議室", 2), ("第3会議室", 4)]   # 4台連結の列数
s = 0
for room, n in ROOMS:
    cat(room)
    s += it("LED照明器具　埋込本体", "NNLK41720J", 2 * n, "台", P_HON, f"定価{HONTAI:,}×{KAKE}　連結中用")
    s += it("LED照明器具　埋込本体", "NNLK41721J", n, "台", P_HON, f"定価{HONTAI:,}×{KAKE}　連結右用")
    s += it("LED照明器具　埋込本体", "NNLK41722J", n, "台", P_HON, f"★定価{HONTAI:,}×{KAKE}　連結左用")
    s += it("LED照明器具　ライトバー", "NEL4300EN　LE9", 4 * n, "台", P_BAR, f"定価{BAR:,}×{KAKE}")
    s += it("照明器具取付", "埋込型 40形 W190 連結", 4 * n, "台", TORI, "積算マニュアル LRS6-4-30 取付手間", TORI)
    s += it("既設照明器具撤去", "埋込形 40形", 4 * n, "台", TEKKYO, "★既設は新設と同数とみた", TEKKYO)

cat("共通")
s += it("撤去品処分費", "既設照明器具・蛍光管", 1, "式", 36_000, "★36台")

KEIHI = 12.0
k_raw = jsround(s * KEIHI / 100)
TOTAL = (s + k_raw) // 1000 * 1000
cat("経　費")
rows.append({"name": "諸経費", "rate": KEIHI, "adj": TOTAL - s - k_raw})

data = {"header": {"name": "柳津生涯学習センター　照明器具改修工事", "client": "岐阜市長　柴橋正直", "honorific": "様",
                   "date": "2026-11-02", "staff": "河口", "no": ""},
        "place": "柳津生涯学習センター", "validity": "発行日より1ヶ月", "remarks": "", "notes": [], "addrKind": "public",
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_岐阜市_柳津生涯学習センター_照明改修.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/yanaizu-shogai-led.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_岐阜市_柳津生涯学習センター_照明改修.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=yanaizu-shogai-led\n")
sub, cur = {}, None
for r in rows:
    if r.get("type") == "cat": cur = r["name"]; print("【" + cur + "】"); continue
    if "qty" in r:
        a = r["qty"] * r["price"]; sub[cur] = sub.get(cur, 0) + a
        print(f"  {(r['name']+' '+r['spec'])[:34]:36}{r['qty']:>3}{r['unit']}{r['price']:>8,}{a:>10,}  {r['note']}")
for k, v in sub.items(): print(f"{k} 計 {v:,}")
print(f"小計 {s:,}／諸経費 {TOTAL - s:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}／税込 {TOTAL + jsround(TOTAL*0.1):,}")
