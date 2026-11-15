# -*- coding: utf-8 -*-
"""換気設備 有圧換気扇更新工事（戸島工業株式会社 御中）エフピコ 換気扇33台取替　No.261027 R8.10.30
   R8.11.14 Kの指示「エフピコの最新の見積を出して」：Drive「戸島工業　エフピコ換気扇33台取替」の
   最新の見積書（換気設備 有圧換気扇更新工事_見積書_R8.10.30.xlsx、計 2,065,000）を KD見積 に起こした（金額はそのまま）。
   有圧換気扇本体は支給品（取替え工事のみ）。
   法定福利費 201,800・諸経費 199,000 は元の見積のとおり（率の行の adj で合わせる。労務費は単価の約73.5%）。
   R8.11.15 Kの指示：換気扇本体はこちらで用意することになった → 見積を直す。
     機器＝富永電機 材料見積（R8.11.13）：三菱 現行品（低騒音形）33台＋バックガード（鉄線製）33個、定価計 4,599,900・NET 1,520,000。
     機器の売値＝NET÷0.8（粗利2割）＝1,900,000 を定価の比で各行に分け、取替手間（元の単価）に足す。
     型番は現行品（換気扇見積依頼リスト R8.11.12 の旧→新）。バックガードは各換気扇に1個（50・45cm→G-50EC3、40→G-40EC3、35→G-35EC3、25→G-25EC3）。
     法定福利費は労務費（元のまま）×16.5%、諸経費 12%、計を1,000円単位に（切り捨て、諸経費の adj）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
LR = 1_223_030 / 1_664_200          # 労務費の割合（法定福利費 16.5% が元の見積の 201,800 になるように）
def sig(v):
    v = float(v); step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step
def it(name, spec, qty, unit, price, note="", labor=None):
    lab = price if labor is None else labor          # 労務費の基（取替手間）。機器分は入れない
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note,
                 "pl": jsround(lab * LR)})
    return qty * int(price)
TEIKA_ALL, NET_ALL = 4_599_900, 1_520_000
K = NET_ALL / 0.8 / TEIKA_ALL                      # 定価に対する売値の比（約0.413）
GUARD = {50: 24_800, 45: 24_800, 40: 21_800, 35: 19_000, 25: 16_500}   # G-50EC3（45cmも）/G-40EC3/G-35EC3/G-25EC3 の定価
def fan(model, cm, kigo, q, teika, tori):
    mat = sig((teika + GUARD[cm]) * K)
    return it("有圧換気扇更新", f"{model}　{cm}cm　{kigo}", q, "台", mat + tori,
              f"機器（定価{teika:,}＋ガード{GUARD[cm]:,}）×{K:.4f}＝{mat:,}＋取替{tori:,}", labor=tori)

s = 0
cat("有圧換気扇 更新（給気ファン）")
s += fan("EWG-50ETA2-Q", 50, "VS-104'・105・105'", 6, 136_000, 47_400)
s += fan("EWG-45DTA2-Q", 45, "VS-101", 1, 123_000, 47_400)
s += fan("EWF-45ETA2-Q", 45, "VS-103・110 下段", 2, 135_000, 47_400)
s += fan("EWF-25ATA2-Q", 25, "VS-107", 1, 48_100, 36_600)
s += fan("EWG-50ETA2-Q", 50, "VS-201 上部", 3, 136_000, 47_400)
cat("有圧換気扇 更新（排気ファン）")
s += fan("EWG-50ETA2", 50, "VE-103'・110'", 6, 125_000, 47_400)
s += fan("EWG-50DTA2", 50, "VE-104'・105'", 4, 108_000, 47_400)
s += fan("EWG-45DTA2", 45, "VE-104", 1, 111_000, 47_400)
s += fan("EWF-45ETA2", 45, "VE-103", 1, 122_000, 47_400)
s += fan("EWF-35CTA2", 35, "VE-102", 1, 75_000, 36_600)
s += fan("EWG-40BTA2", 40, "VE-107・112・113", 5, 81_100, 40_900)
s += fan("EWG-50ETA2", 50, "VE-201 上部", 2, 125_000, 47_400)
cat("共通")
s += it("高所作業車", "VS-201・VE-201・嵩天部 ほか　2日", 1, "式", 70_000)
s += it("撤去品処分費", "有圧換気扇 33台", 1, "式", 66_000)
s += it("試運転調整", "33台", 1, "式", 18_100)
assert sum(r["qty"] for r in rows if r.get("name") == "有圧換気扇更新") == 33

labor = sum(r["qty"] * r["pl"] for r in rows if "pl" in r)
w_raw = jsround(labor * 16.5 / 100); W_AMT = w_raw // 100 * 100
k_raw = jsround(s * 12 / 100)
TOTAL = (s + W_AMT + k_raw) // 1000 * 1000
K_AMT = TOTAL - s - W_AMT
cat("経　費")
rows.append({"name": "法定福利費", "welfare": 16.5, "adj": W_AMT - w_raw})
rows.append({"name": "諸経費", "rate": 12.0, "adj": K_AMT - k_raw})

data = {"header": {"name": "換気設備 有圧換気扇更新工事", "client": "戸島工業株式会社", "honorific": "御中",
                   "date": "2026-11-15", "staff": "河口", "no": "261027"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "",
        "notes": ["有圧換気扇は三菱電機 現行品（低騒音形）、バックガード（鉄線製）付です"],
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_戸島工業_エフピコ_換気扇更新.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/fpco-kankisen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_戸島工業_エフピコ_換気扇更新.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=fpco-kankisen\n")
for r in rows:
    if r.get("type") == "cat": print("【" + r["name"] + "】"); continue
    if "qty" in r: print(f"  {(r['name']+' '+r['spec'])[:40]:42}{r['qty']:>3}{r['unit']}{r['price']:>9,}{r['qty']*r['price']:>10,}")
print(f"小計 {s:,}／法定福利費 {W_AMT:,}（労務費 {labor:,}・16.5%={w_raw:,}）／諸経費 {K_AMT:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}")
