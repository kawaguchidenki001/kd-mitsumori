# -*- coding: utf-8 -*-
"""岐阜（６）空調改修等機械工事のうち 計装工事（全熱交換器リモコン配線・取付）
   航空自衛隊岐阜基地　教場Ａ（教育講堂）／近畿中部防衛局調達部

対象の根拠：ＭＤ－１５の注記「※全熱交換器のリモコン配線工事は本工事とする。」
数量の根拠：ＭＤ－１３「換気設備機器表」の全熱交換器（ＨＥＵ）台数。
  付属品欄に「コントロールスイッチ」があるのは全熱交換器のみで、排気ファン（ＦＥ）には無い。

  1階 ＨＥＵ1-1(2) 1-2(1) 1-3(1) 1-4(3) 1-5(1) 1-6(1) 1-7(1) ＝10台
  2階 ＨＥＵ2-1(1) 2-2(1) 2-3(1) 2-4(1) 2-5(1) 2-6(1) 2-7(2) 2-8(1) 2-9(2) ＝11台
  3階 ＨＥＵ3-1(1) 3-2(1) 3-3(1) 3-4(2) ＝5台
  合計26台。付属品は機器1台ごとと読み、リモコンも26個とする。

配線長：機器（天井内）→ 室出入口の壁（Ｈ＝1.2m）まで。
  Ｙ方向スパン7,050／Ｘ方向5,800の室が主。水平7m＋立下げ1.5m＋余長1.5m＝10m／台。
  26台×10m＝260m。壁内立下げのＰＦ－16（26箇所×1.5m＝40m）は配線単価に含める。
"""
import json, base64, math, os

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    """単価の丸め：1,000円以上は上3桁・100円台は上2桁・10円台は上1桁で切上げ"""
    v = float(v)
    if v <= 0: return 0
    n = 3 if v >= 1000 else 2 if v >= 100 else 1 if v >= 10 else 0
    if n == 0: return int(math.ceil(v))
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - n)
    return int(math.ceil(round(v / step, 9))) * step

# 複合単価（公共建築工事標準単価）
CEE_P, CEE_T = 810, 640        # EM-CEE 1.25mm2-2C 管内
PF_P,  PF_T  = 1400, 1296      # PF-16 隠ぺい
L_M, PF_M    = 260, 40         # 配線260m／PF管40m

rows = []
def it(name, spec, qty, unit, price, lr=0.0):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": ""}
    if lr: r["pl"] = int(round(price * lr))
    rows.append(r)
    return qty * int(price)

# 配線単価＝ケーブル複合単価＋ＰＦ管を配線1mあたりに按分
w_p = sig(CEE_P + PF_P * PF_M / L_M)
w_t = CEE_T + PF_T * PF_M / L_M                 # 労務費相当
TORITSUKE = sig(4500)                            # 取付手間（全額労務）

sub = 0
sub += it("リモコン配線", "ＥＭ－ＣＥＥ１.２５sq－２Ｃ　ＰＦ管共", L_M, "m", w_p, w_t / w_p)
sub += it("リモコン取付", "全熱交換器用（機器付属品）", 26, "個", TORITSUKE, 1.00)
ZATSU = 396_000 - sub                            # 小計を1,000円単位に合わせる
sub += it("雑材消耗品", "", 1, "式", ZATSU)

labor = sum(r["qty"] * r.get("pl", 0) for r in rows)
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 1000 * 1000
k_raw = jsround(sub * KEIHI / 100)
TARGET = (sub + w_amt + k_raw) // 1000 * 1000    # 計（税抜）を1,000円単位（切捨て）
k_amt = TARGET - sub - w_amt
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費",     "rate": KEIHI,     "adj": k_amt - k_raw})

data = {"header": {"name": "岐阜（６）空調改修等機械工事のうち　計装工事",
                   "client": "", "honorific": "御中",
                   "date": "2026-09-12", "staff": "河口", "no": "260912"},
        "place": "航空自衛隊岐阜基地　教場Ａ（教育講堂）",
        "remarks": "", "taxMode": "out", "taxRate": 10, "rows": rows}

root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_岐阜基地_教場A_計装工事.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

for r in rows:
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:38]:40}{r['qty']:>5}{r['unit']:<3}{r['price']:>8,}{r['qty']*r['price']:>11,}")
tax = jsround(TARGET * 0.1)
print(f"\n{'小　計（純工事費）':20}{sub:>11,}")
print(f"{'法定福利費':20}{w_amt:>11,}   （労務費 {round(labor):,}×{WELFARE}%）")
print(f"{'諸経費':20}{k_amt:>11,}   （純工事費×{KEIHI}%＋端数調整）")
print(f"{'計（税抜）':20}{TARGET:>11,}\n{'消費税10%':20}{tax:>11,}\n{'合　計':20}{TARGET+tax:>11,}")
assert TARGET % 1000 == 0 and sub == 396_000

payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
json.dump(data, open(root + "/q/gifu-keiso.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(root + "/見積/取込リンク_岐阜基地_教場A_計装.txt", "w").write(
    url + "\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=gifu-keiso\n")
print("URL長", len(url))
