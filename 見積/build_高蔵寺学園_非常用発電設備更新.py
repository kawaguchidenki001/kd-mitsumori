# -*- coding: utf-8 -*-
"""非常用発電設備　更新工事（学校法人 高蔵寺学園 御中）R8.10.31
   資料：Kの写真（見積書の様式：宛名・件名・品名と数量。単価は空欄）。Drive「大興建設　高蔵寺幼稚園　発電機取替」。
   本体：防災型非常用発電装置 普通騒音型 東京電機製 30kVA(24kW) 3相3線 220V 60Hz 3600min-1
         → 東京電機 LTシリーズ 普通形 TQGP30LT（26/30kVA、クボタ V1505）相当（Web検索の結果。カタログで要確認）。
   単価（★は確認できていない）：
     ・本体 ★5,000,000：東京電機・代理店の見積が取れていない（メーカーサイトはこの環境から開けない）。見積が来たら差し替える。
     ・重量・揚重：25tラフタークレーン 1日（撤去と据付を同じ日、回送費込）、重量とび 2名。
     ・電気工事：人工 28,200×（1＋経費0.4）＝39,480。撤去 2人工、アンカー打設・結線 2人工＋材料、ケーブル加工 0.5人工＋端子材、
       労務費（搬入据付の補助・配線の手直し）2人工、消防立会 1人工。
     ・試運転調整費：メーカー技術員による試運転・切替試験。官庁申請：消防署（発電設備設置届）・警察署（道路使用許可）。
   経費：諸経費 5%・一般管理費 3%（純工事費に対して）、出精値引きで計を 10万円単位に。見積No は新規（空欄＝アプリが採番）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

NIN = 28_200 * 1.4                  # 39,480
HONTAI = 5_000_000                  # ★

rows = []
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note})
    return qty * int(price)

s = 0
rows.append({"name": "防災型非常用発電装置本体　普通騒音型", "spec": "", "qty": "", "unit": "", "price": 0, "note": "", "ref": True})
s += it("東京電機製　30kVA(24kW)　3相3線", "220V　60Hz　3600min-1", 1, "台", HONTAI, "★TQGP30LT 相当。代理店見積で差し替え")
s += it("重量作業費（玉掛作業）", "", 1, "式", 80_000, "★重量とび 2名")
s += it("揚重機費（25tラフタークレーン）", "", 1, "式", 95_000, "★1日 オペ付・回送費込")
s += it("機材損料（消耗品費含む）", "", 1, "式", 35_000, "★")
s += it("横引四角支柱組立解体費", "", 1, "式", 90_000, "★")
s += it("既設発電機撤去", "", 1, "式", sig(NIN * 2), "2人工")
s += it("基礎縫い付け（アンカー打設）・結線作業", "", 1, "式", sig(NIN * 2 + 10_000), "2人工＋アンカー材")
s += it("ケーブル加工費", "", 1, "式", sig(NIN * 0.5 + 10_000), "0.5人工＋端子材")
s += it("労務費", "", 1, "式", sig(NIN * 2), "搬入据付の補助・配線手直し 2人工")
s += it("車輌使用料", "", 1, "式", 25_000, "★")
s += it("産廃処分費", "", 1, "式", 60_000, "★既設発電機・廃油・蓄電池")
s += it("官庁申請（消防署・警察署）", "", 1, "式", 50_000, "★発電設備設置届・道路使用許可")
s += it("試運転調整費", "", 1, "式", 150_000, "★メーカー技術員")
s += it("消防立会費", "", 1, "式", sig(NIN), "1人工")
NET = s
SHOKEI = sig(NET * 0.05)
IPPAN = sig(NET * 0.03)
s += it("諸経費", "", 1, "式", SHOKEI, "純工事費×5%")
s += it("一般管理費", "", 1, "式", IPPAN, "純工事費×3%")
TOTAL = s // 100_000 * 100_000
NEBIKI = TOTAL - s
s += it("出精値引き", "", 1, "式", NEBIKI)
assert s == TOTAL

data = {"header": {"name": "非常用発電設備　更新工事", "client": "学校法人　高蔵寺学園", "honorific": "御中",
                   "date": "2026-10-31", "staff": "河口", "no": ""},
        "place": "高蔵寺幼稚園", "validity": "発行日より1ヶ月", "remarks": "",
        "notes": ["既設の基礎・幹線を利用します（基礎工事・幹線の更新は含みません）"],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_高蔵寺学園_非常用発電設備更新.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/kozoji-hatsudenki.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_高蔵寺学園_非常用発電設備更新.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=kozoji-hatsudenki\n")
for r in rows:
    if r.get("ref"): print("  " + r["name"]); continue
    print(f"  {(r['name']+' '+r['spec'])[:40]:42}{r['qty']:>2}{r['unit']}{r['price']:>11,}  {r['note']}")
print(f"純工事費 {NET:,}／諸経費 {SHOKEI:,}／一般管理費 {IPPAN:,}／出精値引き {NEBIKI:,}／計（税抜）{TOTAL:,}／税込 {TOTAL + jsround(TOTAL*0.1):,}")
