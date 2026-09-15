# -*- coding: utf-8 -*-
"""北一色団地1〜4号棟 外壁改修及び屋上防水工事のうち　電気設備工事
   （永井建設株式会社 御中／発注者：岐阜市まちづくり推進部）

   拾い出しの根拠
     仕様書 3 工事数量(3)「照明器具工事 一式」、4(3)1)「図面に示す既設照明器具を撤去処分の上、新設する」
     電気設備平面図 011〜014（1〜4号棟）の「更新器具」表、015 駐車場 電気設備配置図

       1号棟  XLW202AENZLE9 5台／LBF3MP/RP-2-06 1台
       2号棟  XLW202AENZLE9 5台／LBF3MP/RP-2-06 1台
       3号棟  XLW202AENZLE9 6台／LBF3MP/RP-2-06 2台
       4号棟  XWG201DGNCLE9（非常用照明）6台／LBF3MP/RP-2-06 3台
       駐車場  防犯灯 撤去・再取付／既設ポール 撤去・更新（H=5m、基礎共）

   単価は電気設備工事積算実務マニュアル2026（岐阜県）の複合単価。
   LBF3MP／RP-2-06 は同マニュアルに同一品番の登録がありそのまま採用。
   ★は登録が無く、近い仕様からの積上げ。
   既設配線は流用のため配線・配管の計上は無い（図面に新設配線の表示なし）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    """単価の丸め：四捨五入で上3桁、最小単位は10円（1円単位は出さない）"""
    v = float(v)
    if v <= 0: return 0
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - 3)
    if step < 10: step = 10
    n = int(math.floor(v / step + 0.5))
    return (n if n >= 1 else 1) * step

# ---- 単価（複合単価, 労務費）------------------------------------------------
GYAKU = (34_600, 3_299)   # LED直付天井灯 ベースライト 防湿防雨形 LSS9MP／RP-2-07（XLW202AENZLE9相当）
BRA   = (30_600, 3_299)   # LED直付天井灯・ブラケット 防湿防雨形 LBF3MP／RP-2-06（図面の公共型番と同一）
# ★非常用×防湿防雨の登録が無いため、非常用K1-LSS9-2-15（47,900）に
#   防湿防雨の差額（LSS9MP/RP-2-07 34,600 − LSS9-2-15 16,100 ＝ 18,500）を加算
HIJO  = (sig(47_900 + 18_500), 3_299)
TEKKY = (1_460, 1_050)    # 既設照明器具 撤去処分（20形直付の撤去費）
BOHAN = (sig(2_210 + jsround(5_020 * 1.49)), 6_500)   # ★防犯灯 撤去・再取付（取外し＋再取付）
POLE  = (sig(22_900 + 5_000 + 90_000 + 30_000 + 65_200), 60_000)  # ★ポール撤去・新設H=5m・基礎共
KOUSHO = (65_900, 0)      # 高所作業車 運転機械経費 1日
SHOBUN = (30_000, 0)      # ★発生材処分費（FL器具・安定器・ランプ 29台分）

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, key, note=""):
    price, pl = key
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return qty * int(price)

sub = 0
for no, gyaku, bra, hijo in [("1", 5, 1, 0), ("2", 5, 1, 0), ("3", 6, 2, 0), ("4", 0, 3, 6)]:
    cat("0" + no + "　" + no + "号棟　電灯設備")
    if gyaku:
        sub += it("ＬＥＤベースライト", "逆富士型 ２０形 防湿防雨 ＸＬＷ２０２ＡＥＮＺＬＥ９",
                  gyaku, "台", GYAKU, "単価：LSS9MP／RP-2-07（防湿防雨形 直付 20形）で計上")
    if hijo:
        sub += it("ＬＥＤ非常用照明器具", "直付形 ２０形 防湿防雨 ＸＷＧ２０１ＤＧＮＣＬＥ９",
                  hijo, "台", HIJO, "★非常用K1-LSS9-2-15＋防湿防雨差額で積上げ")
    sub += it("ＬＥＤブラケット", "２０形 防湿防雨 ＬＢＦ３ＭＰ／ＲＰ－２－０６",
              bra, "台", BRA, "複合単価（図面の公共型番と同一）")
    sub += it("既設照明器具 撤去処分", "ＦＬ１０Ｗ・ＦＬ２０Ｗ 直付形",
              gyaku + bra + hijo, "台", TEKKY)

cat("05　屋外電気設備")
sub += it("防犯灯 撤去・再取付", "駐車場", 1, "台", BOHAN, "★取外し・再取付")
sub += it("照明ポール 撤去・更新", "Ｈ＝５ｍ 基礎共", 1, "本", POLE, "★既設ポール撤去・基礎とりこわし・新設ポール・基礎")
sub += it("高所作業車", "１日作業", 1, "台", KOUSHO)
sub += it("発生材処分費", "", 1, "式", SHOBUN, "★ＦＬ器具・安定器・ランプ 29台分")
ZATSU = sig(1_550_000 - int(round(sub)))
sub += it("雑材消耗品", "", 1, "式", (ZATSU, 0), "小計調整")

# ---- 集計 ------------------------------------------------------------------
cat("経　費")
labor = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
sub = int(round(sub))
WELFARE, KEIHI = 16.5, 12.0
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 1000 * 1000
k_raw = jsround(sub * KEIHI / 100)
TARGET = (sub + w_amt + k_raw) // 1000 * 1000
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費",     "rate": KEIHI,     "adj": (TARGET - sub - w_amt) - k_raw})

data = {"header": {"name": "北一色団地１～４号棟 外壁改修及び屋上防水工事　電気設備工事",
                   "client": "永井建設株式会社", "honorific": "御中",
                   "date": "2026-09-15", "staff": "河口", "no": "260916"},
        "place": "岐阜市北一色７丁目１９番",
        "validity": "発行日より1ヶ月", "remarks": "",
        "taxMode": "ex", "taxRate": 10, "rows": rows}

root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_北一色団地_電気設備工事.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/kitaisshiki.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    if r.get("type") == "cat": print("\n【" + r["name"] + "】"); continue
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:40]:42}{r['qty']:>5}{r['unit']:<3}{r['price']:>9,}{round(r['qty']*r['price']):>11,}")
k_amt = TARGET - sub - w_amt
tax = jsround(TARGET * 0.1)
print(f"\n{'小　計（純工事費）':22}{sub:>11,}")
print(f"{'法定福利費':22}{w_amt:>11,}   （労務費 {round(labor):,}×{WELFARE}%）")
print(f"{'諸経費':22}{k_amt:>11,}   （純工事費×{KEIHI}%＋端数調整）")
print(f"{'計（税抜）':22}{TARGET:>11,}\n{'消費税10%':22}{tax:>11,}\n{'合　計':22}{TARGET+tax:>11,}")
assert TARGET % 1000 == 0

payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_北一色団地_電気設備.txt", "w").write(
    url + "\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=kitaisshiki\n")
print("URL長", len(url))
