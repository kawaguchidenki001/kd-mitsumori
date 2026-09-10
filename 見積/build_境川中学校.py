# -*- coding: utf-8 -*-
"""境川中学校 夜間照明設備新設工事 参考見積（岐阜市 ぎふ魅力づくり推進部 市民スポーツ課）

設計書（FAX 2026-08-25）の細目別内訳を、品名・仕様・数量・単位まで
そのまま写している。設計書に無い文字は一切足さない。

4. 投光器設置工事は設計書と同じ代価表の形。
  水銀灯700W相当LED灯 4台／前方カットルーバー 4台／投光器架台 1組 が
  「設置支柱（上記1組分）」1基分の中身で、その小計を単価として6基分を計上する。
  中身の3行は ref:true（金額欄は空欄・合計に入れない）で出す。

単価は複合単価から起こした値に、ご指示の掛率（全体1.3倍、キュービクル内改造費・
土木費・建柱費のみ2倍）を掛け、100円単位／10万円以上は1,000円単位で切上げ済み。
"""
import json, base64, math, os

def jsround(x): return math.floor(x + 0.5)
def r_price(v):
    """単価の丸め：100円単位（切上げ）、10万円以上は1,000円単位（切上げ）"""
    if v <= 0: return 0
    step = 1000 if v >= 100000 else 100
    return int(math.ceil(round(v / step, 9))) * step

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, ref=False):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": ""}
    if ref: r["ref"] = True
    rows.append(r)
    return 0 if ref else qty * int(price)

T = {}

t = "1. 受電設備工事"; cat(t); s = 0
s += it("キュービクル内改造費", "ブレーカー増設他材工共", 1, "式",   300_000)
s += it("夜間照明盤",         "WP、SUS、鍵付き",      1, "面",   312_000)
s += it("支柱BOX（WP、SUS）",  "300×300×200",       6, "面",    32_200)
s += it("幹線ケーブル",        "EM-CET38sq",        120, "m",      4_300)
s += it("露出配管（厚鋼電線管）", "GZ42",              32, "本",      7_100)
s += it("同上附属品",         "",                    1, "式",    33_700)
s += it("配管支持材",         "",                    1, "式",    22_500)
s += it("雑材消耗品",         "",                    1, "式",    39_000)
s += it("電工費",            "",                    1, "式", 2_067_000)
s += it("高所作業車損料",      "",                    1, "式",   172_000)
T[t] = s

t = "2. 分岐配管配線設備工事"; cat(t); s = 0
s += it("埋設配管",          "FEP50",             500, "m",        500)
s += it("分岐配線ケーブル",    "EM-CET14sq",        620, "m",      1_900)
s += it("立上配管（合成樹脂管）", "HIVE28",            24, "本",      2_000)
s += it("立上配線ケーブル",    "EM-EEF2.6-3C",      120, "m",        700)
s += it("投光器用配線ケーブル", "EM-EEF2.0-3C",       50, "m",        500)
s += it("同上附属品",         "",                    1, "式",    44_000)
s += it("配管支持材",         "",                    1, "式",    29_300)
s += it("雑材消耗品",         "",                    1, "式",    47_500)
s += it("電工費",            "",                    1, "式", 2_845_000)
s += it("高所作業車損料",      "",                    1, "式",   258_000)
s += it("土木費",            "",                    1, "式", 1_460_000)
s += it("残土運搬・処分費",    "",                    1, "式",   402_000)
T[t] = s

t = "3. 建柱工事"; cat(t); s = 0
s += it("コンクリート柱",        "16-19-500",       6, "本",   161_000)
s += it("同上運搬費",           "特車申請他含む",     1, "式",   390_000)
s += it("建柱費",              "アースオーガ車使用",  6, "本",    83_400)
s += it("残土運搬処理費",        "",                1, "式",    83_800)
s += it("セフティーガードポール用", "SGPE-P100-200",  6, "枚",    31_200)
T[t] = s

t = "4. 投光器設置工事"; cat(t); s = 0
# 設置支柱1基分の中身（設計書の代価表）。金額欄は空欄・合計には入れない
LED, LOUVER, FRAME = 393_000, 85_200, 147_000
it("水銀灯700W相当LED灯", "NYS35245K-LE2", 4, "台", LED,    ref=True)
it("前方カットルーバー",   "NYK40355",      4, "台", LOUVER, ref=True)
it("投光器架台（省施工型）", "XDYK2400",      1, "組", FRAME,  ref=True)
KUMI = r_price(4 * LED + 4 * LOUVER + FRAME)      # 上記1組分の小計
s += it("設置支柱",       "上記1組分",       6, "基", KUMI)
s += it("雑材消耗品",     "",                1, "式",   247_000)
s += it("電工費",        "",                1, "式", 1_628_000)
s += it("高所作業車損料",  "",                1, "式",   172_000)
T[t] = s

# ---- 諸経費（設計書の様式：共通仮設費・現場管理費・一般管理費）----
cat("諸経費")
direct = sum(T.values())
kari  = jsround(direct * 0.05); jun   = direct + kari
gen   = jsround(jun * 0.17);    genka = jun + gen
ippan_raw = jsround(genka * 0.12)
TARGET = (genka + ippan_raw) // 1000 * 1000        # 工事価格（税抜）を1,000円単位（切捨て）
rows.append({"name": "共通仮設費", "rate": 5})
rows.append({"name": "現場管理費", "expense": 17})
rows.append({"name": "一般管理費", "expense": 12, "adj": TARGET - genka - ippan_raw})

data = {"header": {"name": "境川中学校　夜間照明設備新設工事",
                   "client": "岐阜市 ぎふ魅力づくり推進部 市民スポーツ課",
                   "honorific": "御中", "date": "2026-09-10", "staff": "河口", "no": "260909"},
        "place": "境川中学校（岐阜市柳津町上佐波東3丁目70番地）",
        "remarks": "", "addrKind": "public", "taxMode": "out", "taxRate": 10, "rows": rows}

root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_境川中学校_夜間照明設備新設工事.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

for r in rows:
    if r.get("type") == "cat": print("\n【" + r["name"] + "】"); continue
    if "qty" not in r: continue
    a = "" if r.get("ref") else f"{r['qty']*r['price']:>12,}"
    print(f"  {(r['name']+'　'+r['spec']).strip()[:32]:34}{r['qty']:>5}{r['unit']:<3}{r['price']:>10,}{a}"
          + ("   ←内訳表示（金額なし）" if r.get("ref") else ""))
print()
for k, v in T.items(): print(f"{k:24}{v:>12,}")
tax = jsround(TARGET * 0.1)
print(f"{'直接工事費':24}{direct:>12,}")
print(f"{'共通仮設費 5%':24}{kari:>12,}\n{'現場管理費 17%':24}{gen:>12,}\n{'一般管理費 12%':24}{TARGET-genka:>12,}")
print(f"{'工事価格（税抜）':24}{TARGET:>12,}\n{'消費税10%':24}{tax:>12,}\n{'合計':24}{TARGET+tax:>12,}")
assert TARGET % 1000 == 0
assert KUMI * 6 == T["4. 投光器設置工事"] - 247_000 - 1_628_000 - 172_000

payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + \
      base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
json.dump(data, open(root + "/q/sakaigawa.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(root + "/見積/取込リンク_境川中学校.txt", "w").write(
    url + "\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=sakaigawa\n")
print("URL長", len(url))
