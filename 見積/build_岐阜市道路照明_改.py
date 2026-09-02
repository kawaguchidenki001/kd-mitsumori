# -*- coding: utf-8 -*-
"""道路改良工事 道路照明設備設置工（H=10m）―― 材料をメーカーNET×1.3に改訂（R8.09.02）

材料単価の根拠：富永電機株式会社 御見積書 No.9021（R8.9.2）
  金額欄合計 833,700円／NET欄合計 581,870円
  ・MARUWA分①〜⑥（金額計 816,500円）→ NET 571,550円 ＝ 0.70掛（816,500×0.7＝571,550 で一致）
  ・スパイラルダクト 17,200円 → NET 10,320円 ＝ 0.60掛
  各品目に上記掛率でNETを配分し、×1.3 を見積単価とする（最低10円単位・切上げ）。
"""
import json, base64, os, math

MARKUP = 1.3
WELFARE_RATE = 16.5   # 法定福利費＝労務費×％
KEIHI_RATE   = 12.0   # 諸経費＝純工事費×％
def jsround(x): return math.floor(x + 0.5)

def sig(v):
    """単価の丸め（Kの標準指示）：1,000円以上は上3桁・100円台は上2桁・10円台は上1桁で切上げ。"""
    v = float(v)
    if v <= 0: return 0
    n = 3 if v >= 1000 else 2 if v >= 100 else 1 if v >= 10 else 0
    if n == 0: return int(math.ceil(v))
    d = int(math.floor(math.log10(v))) + 1          # 桁数
    step = 10 ** (d - n)
    return int(math.ceil(round(v / step, 9))) * step

# (品名, 富永の金額, NET掛率)
NET = {
 "ポール":      (425_000, 0.70),
 "LED":        (258_000, 0.70),
 "ターミナル":   (  6_500, 0.70),
 "自動点滅器":   ( 22_000, 0.70),
 "アンカー":     ( 45_000, 0.70),
 "ポール運賃":   ( 60_000, 0.70),
 "ダクト":      ( 17_200, 0.60),
}
P, NOTE = {}, {}
for k, (teika, r) in NET.items():
    net = int(round(teika * r))
    P[k] = sig(net * MARKUP)
    NOTE[k] = f"富永電機No.9021 {teika:,}円×{r:.2f}＝NET {net:,}円 ×1.3＝{net*MARKUP:,.0f}円（上3桁切上げ）"

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, note="", lr=0.0):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit,
         "price": int(price), "note": note}
    if lr:
        r["pl"] = int(round(price * lr))
        r["note"] = (r["note"] + "／" if r["note"] else "") + f"労務費相当 {lr:.0%}"
    rows.append(r)
    return qty * int(price)

TOT = {}
t = "基礎工"; cat(t); s = 0
s += it("基礎掘削及びスパイラルダクト立込", "φ500 2m以下", 1, "基", sig(11950), "", 0.70)
s += it("スパイラルダクト", "φ500×t0.6×1700", 1, "本", P["ダクト"], NOTE["ダクト"])
s += it("基礎砕石", "RC-30 t=100", 0.2, "m2", sig(967), "上2桁切上げ（旧 967円）", 0.50)
s += it("基礎コンクリート", "24-8-25(20)高炉 小型構造物・人力打設", 0.3, "m3", sig(25000), "", 0.35)
s += it("アンカーフレーム", "4-M24-L600", 1, "組", P["アンカー"], NOTE["アンカー"])
s += it("接地設置工", "φ14×1500 D種接地3m以内（接地棒・低減剤共）", 1, "極", sig(16600), "", 0.55)
s += it("根巻きコンクリート", "18-8-40BB 0.075m3・型枠0.6m2共", 1, "箇所", sig(6000), "", 0.50)
TOT[t] = s

t = "灯柱工"; cat(t); s = 0
s += it("道路照明灯柱", "IA10.3B-S 溶融亜鉛メッキ仕上げ　テーパーポール H=10m", 1, "本",
        P["ポール"], NOTE["ポール"])
s += it("ポール運搬費", "平日朝一番降ろし", 1, "車", P["ポール運賃"], NOTE["ポール運賃"])
s += it("道路照明灯建柱", "350kg以下 建柱車", 1, "基", sig(35780), "", 0.50)
s += it("引込フックバンド", "", 1, "個", sig(5000))
s += it("管理銘板", "", 1, "枚", sig(3000))
TOT[t] = s

t = "照明器具取付工"; cat(t); s = 0
s += it("LED照明器具", "KCE150-3C（SLM4-X20830AW-VK00 電源装置内蔵）", 1, "組",
        P["LED"], NOTE["LED"])
s += it("照明器具取付", "新設（高所作業車共）", 1, "台", sig(25000), "", 0.55)
s += it("専用ケーブル", "直線型ポール用", 1, "本", sig(8000))
s += it("ジョイントユニット", "テストスイッチ有", 1, "個", sig(12000))
s += it("電線", "VVF2.6mm×2C", 10, "m", sig(1270), "", 0.55)
s += it("電線", "VVF1.6mm×3C", 10, "m", sig(970), "", 0.55)
TOT[t] = s

t = "自動点滅器取付"; cat(t); s = 0
s += it("光電式自動点滅器", "200V/6A 電子式 分離型 受台付（ポール取付共）", 1, "個",
        P["自動点滅器"], NOTE["自動点滅器"])
s += it("ターミナルキャップ", "G22", 1, "個", P["ターミナル"], NOTE["ターミナル"])
s += it("ニップル", "φ22", 1, "個", sig(800))
TOT[t] = s

# ---- 経費（法定福利費・諸経費）は内訳に無くても必ず計上する ----
direct = sum(r["qty"] * r["price"] for r in rows if "qty" in r)
labor  = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
w_raw = jsround(labor * WELFARE_RATE / 100)
w_amt = w_raw // 1000 * 1000                      # 法定福利費は1,000円単位（切捨て）
k_raw = jsround(direct * KEIHI_RATE / 100)
TARGET = (direct + w_amt + k_raw) // 1000 * 1000  # 計（税抜）を1,000円単位（切捨て）
k_amt  = TARGET - direct - w_amt                  # 端数は諸経費で吸収
rows.append({"name": "法定福利費", "welfare": WELFARE_RATE, "adj": w_amt - w_raw,
             "note": f"労務費 {round(labor):,}円×{WELFARE_RATE}%（1,000円単位）"})
rows.append({"name": "諸経費", "rate": KEIHI_RATE, "adj": k_amt - k_raw,
             "note": f"純工事費 {round(direct):,}円×{KEIHI_RATE}%＋端数調整"
                     f"（計（税抜）を1,000円単位に）"})

j = {"header": {"name": "道路改良工事　道路照明設備設置工（H=10m）",
                "client": "永井建設株式会社", "honorific": "御中",
                "date": "2026-09-02", "staff": "河口", "no": "260830"},
     "place": "岐阜市加野4丁目地内",
     "remarks": "", "taxMode": "out", "taxRate": 10, "rows": rows}

out = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(out, "見積_岐阜市_道路照明設備設置工1基_改.json")
json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

d = json.load(open(p, encoding="utf-8"))
net = 0
for r in d["rows"]:
    if r.get("type") == "cat": print("\n【" + r["name"] + "】"); continue
    if "qty" not in r: continue
    a = r["qty"] * r["price"]; net += a
    print(f"  {(r['name']+'　'+r['spec']).strip()[:46]:48}{r['qty']:>5}{r['unit']:<3}{r['price']:>9,}{round(a):>11,}")
print()
for k, v in TOT.items(): print(f"{k:24}{round(v):>12,}")
print(f"{'小　計（純工事費）':24}{round(net):>12,}")
run = net
for r in d["rows"]:
    if "qty" in r or r.get("type") == "cat": continue
    base = net if "rate" in r else labor
    rt = r.get("rate", r.get("welfare"))
    amt = jsround(base * rt / 100) + r.get("adj", 0)
    run += amt
    print(f"{r['name']:24}{amt:>12,}   （{rt}% 対象 {round(base):,}）")
tax = jsround(run * 0.1)
print(f"{'計（税抜）':24}{round(run):>12,}")
print(f"{'消費税10%':24}{tax:>12,}")
print(f"{'合　計':24}{round(run)+tax:>12,}")
assert abs(net - sum(TOT.values())) < 1
assert all(r["price"] == sig(r["price"]) for r in d["rows"] if "qty" in r), "単価丸め"
assert round(run) % 1000 == 0, run

payload = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
b64 = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + b64
open(os.path.join(out, "取込リンク_岐阜市道路照明_改.txt"), "w").write(url + "\n")
print("URL長", len(url))
