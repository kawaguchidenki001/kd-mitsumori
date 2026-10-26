# -*- coding: utf-8 -*-
"""木曽川中下流用水総合管理所防水改修工事　空調屋外機 電源取外し・再取付（R8.10.26）
   資料：設計図（A-01～A-06・E-01・M-01、独立行政法人水資源機構）、参考資料（数量書：空調屋外機 取外し再取付け 13台）。
   E-01：RP-1（屋外鋼板製自立形）から屋外機 13台（ELB/MCB 3P 50～60A ×13）。
         「空調設備機器の移設復旧に伴う電気配管配線は既設利用とする」「既設配管配線は浮かし養生とし、既設利用とする」。
   Kの依頼：エアコン撤去・再取付に伴う電源の取外し・再取付。
   単価：積算実務マニュアル2026 電気（岐阜県）。電動機結線（直入始動方式以外）14,400、撤去はその3割（4,320）。
         可とう電線管（F2-30 相当）の脱着 約2,600。養生・測定は人工 28,200×（1＋経費0.4）。★は概算。
   経費：法定福利費 16.5%（100円単位）、諸経費 12%、計を1,000円単位に（諸経費の adj）。用紙1枚（分類行なし）。
   宛名：株式会社渡辺組（R8.10.26 Kの指示）。見積No は新規（空欄＝アプリが採番）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

NIN, KEI = 28_200, 0.4
KESSEN, KESSEN_RM = 14_400, 4_320            # 電動機結線 直入始動方式以外（労務費のみ）、撤去＝3割
F2_DATSU = 2_600                             # 二種金属製可とう電線管 F2-30 取外し・再取付（取付手間 2,011＋撤去）
UNIT = sig(KESSEN_RM + KESSEN + F2_DATSU)
UKASHI = sig(NIN * 1.5 * (1 + KEI))          # ★既設配管配線の浮かし養生 1.5人工（取外し時・再取付時）
SOKUTEI = sig(NIN * 0.5 * (1 + KEI))         # ★絶縁抵抗測定（13回路）・試運転立会 0.5人工

rows = [
    {"name": "空調屋外機　電源取外し・再接続", "spec": "PAC-01～08　結線外し・再結線", "qty": 13, "unit": "台",
     "price": UNIT, "pl": KESSEN_RM + KESSEN + 1_400, "note": "電動機結線 直入始動方式以外 14,400＋撤去4,320＋F2脱着"},
    {"name": "既設配管配線　浮かし養生", "spec": "屋上　防水改修範囲", "qty": 1, "unit": "式",
     "price": UKASHI, "pl": NIN * 1.5, "note": "★E-01 特記。1.5人工"},
    {"name": "絶縁抵抗測定・試運転立会", "spec": "空調電源 13回路", "qty": 1, "unit": "式",
     "price": SOKUTEI, "pl": NIN * 0.5, "note": "★0.5人工"},
]
s = sum(r["qty"] * r["price"] for r in rows)
labor = sum(r["qty"] * r["pl"] for r in rows)
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 100 * 100
k_raw = jsround(s * KEIHI / 100)
TOTAL = (s + w_amt + k_raw) // 1000 * 1000
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": TOTAL - s - w_amt - k_raw})

data = {"header": {"name": "木曽川中下流用水総合管理所防水改修工事　空調電源取外し・再取付工事", "client": "株式会社渡辺組", "honorific": "御中",
                   "date": "2026-10-26", "staff": "河口", "no": ""},
        "place": "愛知県稲沢市祖父江町馬飼寺東26-1", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_木曽川中下流_空調電源脱着.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/kisogawa-ac-dengen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_木曽川中下流_空調電源脱着.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=kisogawa-ac-dengen\n")
for r in rows:
    if "qty" in r: print(f"  {r['name']} {r['spec']:<36}{r['qty']:>3}{r['unit']}{r['price']:>9,}{r['qty']*r['price']:>10,}  {r['note']}")
print(f"小計 {s:,}／法定福利費 {w_amt:,}（労務費 {labor:,.0f}）／諸経費 {TOTAL - s - w_amt:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}")
