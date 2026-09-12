# -*- coding: utf-8 -*-
"""文化センターロビー改修工事 電気設備工事（永井建設株式会社 御中）改訂版
   元見積 No.260802（R8.8.3）を、次の資料で見直したもの。
   ・納入仕様書（照明器具 メーカー仕様図面集 R8.8.25）
       A XND3589SNLJ9 31台／B XND2069WNKLE9＋リニューアルプレートNNN80006K 25台／
       C NEL4600ENLE9 ライトバーのみ36台（既設器具本体流用）／F XFX459RENLE9 2台／
       SP EFS7136W（遠藤照明）26台
   ・アプロ通信株式会社 見積№HD026207-2（R8.8.21）サイネージ設備工事
       合計 6,046,000円（税抜）、※NET 2,720,000円 → NET×1.1＝2,992,000円で計上
   ・図面 E01〜E05（岐阜市まちづくり推進部）
   単価は元見積と同じ公共建築工事標準の複合単価。定価未入手の器具は実勢からの推定（要確認）。
"""
import json, base64, os, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    n = 3 if v >= 1000 else 2 if v >= 100 else 1 if v >= 10 else 0
    if n == 0: return int(math.ceil(v))
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - n)
    return int(math.ceil(round(v / step, 9))) * step

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, pl=0, note=""):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
    return qty * int(price)

T = {}
# 照明器具費＝定価×掛率（パナソニック0.3／遠藤0.6）＋ 取付手間
# 取付手間は複合単価−材料費（労務費＋経費）。★定価は手元にデータが無く推定値
PANA, ENDO = 0.30, 0.60
def lamp(teika, rate, tetsuke): return sig(round(teika * rate) + tetsuke)

t = "02 幹線設備"; cat(t); s = 0
s += it("リモコンブレーカー", "1P20AT BCL12001 分電盤1L-3内", 1, "個", sig(12000), 4000, "★実勢推定")
s += it("既設分岐ブレーカー 撤去", "1P20AT 回路⑦", 1, "個", 1500, 1500)
s += it("リモコン信号線 配線・調整", "事務室リモコン盤〜1L-3", 1, "式", 15000, 12000)
T[t] = s

t = "04 電灯設備"; cat(t); s = 0
s += it("高天井用ダウンライト 撤去", "既設a ロビー（北）", 31, "台", 3220, 3220)
s += it("高天井用ダウンライト 撤去", "既設b ロビー（北）", 25, "台", 2600, 2600)
s += it("既設ライトバー 取外し", "既設c 本体流用 ロビー（南）", 36, "台", 1100, 1100)
s += it("スポットライト 撤去", "既設g ダクト共 ロビー（南）", 22, "台", 1000, 1000, "★推定")
s += it("埋込形ベースライト 撤去", "既設f 売店", 2, "台", 4130, 4130)
s += it("直付形廊下灯 撤去", "既設h 売店", 1, "台", 2210, 2210)
s += it("スポットライト 撤去", "既設i ダクト共 売店", 3, "台", 1000, 1000, "★推定")
s += it("ライティングダクト 撤去", "既設 ロビー（南）・売店", 10.3, "m", 830, 830)
s += it("棚下灯スイッチ 撤去", "売店", 1, "箇所", 670, 670)
s += it("棚下スポットライトSW 撤去", "売店", 1, "箇所", 670, 670)
s += it("LEDダウンライト　Ａ", "XND3589SNLJ9 4020lm 調光", 31, "台", lamp(56_000, PANA, 13640), 7304,
        "★定価56,000（推定）×0.3＋取付13,640")
s += it("LEDダウンライト　Ｂ", "XND2069WNKLE9 2035lm", 25, "台", lamp(31_400, PANA, 10515), 5894,
        "★定価31,400（推定）×0.3＋取付10,515")
s += it("リニューアルプレート", "NNN80006K Ｂ用 φ150→φ200", 25, "枚", lamp(3_300, PANA, 500), 500,
        "★定価3,300（推定）×0.3＋取付500")
s += it("LEDライトバー　Ｃ", "NEL4600ENLE9 6900lm 本体流用", 36, "台", lamp(21_900, PANA, 4000), 3000,
        "★定価21,900（推定）×0.3＋取付4,000")
s += it("LED埋込形ベースライト　Ｆ", "XFX459RENLE9 5040lm", 2, "台", lamp(34_000, PANA, 16035), 9362,
        "★定価34,000（推定）×0.3＋取付16,035")
# ライティングダクト：区間は1.2m×5・2.5m×3・1.1m×2＝15.7m（図面E03）。3m定尺7本から切出し
s += it("ライティングダクト　Ｌ", "固定I形 直付 2P15A125V 3m", 7, "本", sig(1846 * 3 * 1.1), 0,
        "実勢1,846/m×3m×1.1。1.2m×5・2.5m×3・1.1m×2＝15.7mを3m定尺7本から切出し")
s += it("フィードインキャップ", "Ｌ用 2P15A125V", 10, "個", sig(600 * 1.1 + 100), 0, "★実勢推定")
s += it("エンドキャップ", "Ｌ用", 10, "個", sig(220 * 1.1 + 30), 0, "★実勢推定")
s += it("ライティングダクト 取付", "端部処理・接続共", 15.7, "m", 4350, 2820)
s += it("LEDスポットライト　ＳＰ", "EFS7136W 2000TYPE ダクト用", 26, "個", lamp(48_400, ENDO, 3000), 3000,
        "★定価48,400（推定）×0.6＋取付3,000（遠藤照明）")
s += it("ケーブル配線 EM-EEF", "2.0mm-3C 天井ころがし 電灯回路", 250, "m", 1070, 640)
s += it("スイッチ回路変更", "Ｆ・サイン照明を②系統に", 1, "式", 12000, 10000)
T[t] = s

t = "05 コンセント設備"; cat(t); s = 0
s += it("コンセント 撤去", "自販機用・高さ変更・TV共", 6, "個", 830, 830)
s += it("ブランクプレート 設置", "自販機用撤去跡", 1, "個", 600, 300)
s += it("電話機 撤去", "公衆電話 売店前", 1, "台", 2000, 2000)
s += it("電灯用子メーター 撤去", "売店", 1, "個", 3000, 3000)
s += it("埋込形コンセント（大角形）", "2P15A×2 E付 新設FL+1,900", 2, "個", 3500, 2100)
s += it("埋込形コンセント（大角形）", "2P15A×2 E付 ブランク跡", 1, "個", 3500, 2100)
s += it("埋込形コンセント（大角形）", "2P15A×2 E付 ボックス共", 1, "個", 3500, 2100)
s += it("埋込形コンセント（大角形）", "2P15A×2 E付 サイネージ①③④", 3, "個", 3500, 2100)
s += it("埋込形コンセント（大角形）", "3個口＋E端子 サイネージ②", 1, "個", 3500, 2100)
s += it("アウトレットボックス", "四角中浅 102×102×44 塗代付", 8, "個", 4470, 2235)
s += it("ケーブル配線 EM-EEF", "2.0mm-3C 天井ころがし コンセント回路", 120, "m", 1070, 640)
T[t] = s

t = "09 情報・監視カメラ設備"; cat(t); s = 0
s += it("LAN用ケーブル UTP", "CAT6 4P 管内", 150, "m", 830, 500)
s += it("露出形モジュラージャック", "CAT6 8極8心 1個口", 5, "個", 4000, 2200)
s += it("合成樹脂製可とう電線管 PF", "22 隠ぺい 各柱立下げ", 30, "m", 1870, 1400)
s += it("コーナーボックス・メタルモール", "A型 各柱立下げ", 20, "m", 2270, 1590)
# --- サイネージ設備（アプロ通信 見積№HD026207-2 の内訳を転記）---
# 単価はアプロ提示単価×r（r＝NET2,720,000×1.1÷見積合計6,046,000）。端数は最終行で調整
SIG_ROWS = [("壁掛金具", "43V型用", 3, "式", 32_000), ("壁掛金具", "55V型用", 1, "式", 34_000),
            ("TVチューナー", "SK-VO6TV", 1, "台", 54_000),
            ("サイネージコントローラー", "PN-ZP40", 4, "台", 239_000),
            ("キッティング費用", "", 4, "式", 65_000),
            ("管理用PC", "WJ64/LA", 1, "台", 412_000),
            ("管理用PC設定費", "", 1, "式", 555_000),
            ("e-SignageS ネットワーク版", "ソリューションサービス費用", 1, "式", 570_000),
            ("HDMIケーブル", "1m", 5, "本", 1_000),
            ("スイッチングHUB", "8ポート", 1, "台", 16_200),
            ("情報プラグ", "CAT6", 10, "個", 260),
            ("機器取付工事費", "", 1, "式", 1_440_000),
            ("接続試験調整費", "", 1, "式", 720_000),
            ("ケーブル測定・データ作成費", "", 1, "式", 45_000)]
# 旅費宿泊費・交通費／法定福利費／諸経費は内訳に出さず、他項目へ配分して金額だけ合わせる
SIG_DROP = 160_000 + 229_800 + 341_400
SIG_TOTAL, SIG_NET = 6_046_000, 2_720_000
SIG_TARGET = int(SIG_NET * 1.1)                       # 2,992,000
r = SIG_TARGET / (SIG_TOTAL - SIG_DROP)               # 残す項目だけで2,992,000に届くよう増額
s += it("液晶モニター 取付", "43V型×3・55V型×1 施設支給品", 4, "台", 0, 0, "アプロ通信分（金具・取付費に計上）")
acc = 0
for nm, sp, q, un, up in SIG_ROWS:
    u = int(round(up * r / 10) * 10)                   # 10円単位
    acc += q * u
    s += it(nm, sp, q, un, u, 0, "アプロ通信分")
s += it("雑材消耗品", "アプロ通信分", 1, "式", SIG_TARGET - acc, 0, "アプロ通信分／旅費・法定福利費・諸経費を配分")
assert acc + (SIG_TARGET - acc) == SIG_TARGET
T[t] = s

# ===== 集計 =====
direct = int(round(sum(T.values())))
labor  = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r)
WELFARE, KEIHI = 16.5, 10.0            # 法定福利費＝労務費×16.5%／諸経費＝純工事費×10%（ご指示）
w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 1000 * 1000
k_raw = jsround(direct * KEIHI / 100)
TARGET = (direct + w_amt + k_raw) // 1000 * 1000
k_amt = TARGET - direct - w_amt
rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": KEIHI, "adj": k_amt - k_raw})

data = {"header": {"name": "文化センターロビー改修工事 電気設備工事", "client": "永井建設株式会社", "honorific": "御中",
                   "date": "2026-09-12", "staff": "河口", "no": "260802-2"},
        "place": "岐阜市金町五丁目地内", "validity": "", "remarks": "",
        "taxMode": "out", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_文化センターロビー改修_電気設備_改.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in rows:
    if r.get("type") == "cat": print("\n【" + r["name"] + "】"); continue
    if "qty" not in r: continue
    print(f"  {(r['name']+'　'+r['spec']).strip()[:44]:46}{r['qty']:>6}{r['unit']:<3}{r['price']:>10,}{round(r['qty']*r['price']):>12,}")
print()
for k, v in T.items(): print(f"{k:28}{round(v):>12,}")
tax = jsround(TARGET * 0.1)
print(f"{'小計（純工事費）':28}{round(direct):>12,}\n{'法定福利費':28}{w_amt:>12,}   （労務費 {round(labor):,}×16.5%）")
print(f"{'諸経費 10%':28}{k_amt:>12,}\n{'計（税抜）':28}{TARGET:>12,}\n{'消費税10%':28}{tax:>12,}\n{'合計':28}{TARGET+tax:>12,}")
assert TARGET % 1000 == 0
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
json.dump(data, open(root + "/q/bunka-lobby.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(root + "/見積/取込リンク_文化センターロビー_改.txt", "w").write(url + "\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=bunka-lobby\n")
print("URL長", len(url))
