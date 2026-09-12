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
# 照明器具費＝実勢価格（複合単価の材料費）×1.1 ＋ 取付手間（複合単価−材料費）
def lamp(mat, comp): return sig(round(mat * 1.1) + (comp - mat))

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
s += it("LEDダウンライト　Ａ", "XND3589SNLJ9 4020lm 調光", 31, "台", lamp(26460, 40100), 7304,
        "実勢26,460×1.1＋取付13,640")
s += it("LEDダウンライト　Ｂ", "XND2069WNKLE9 2035lm", 25, "台", lamp(16485, 27000), 5894,
        "実勢16,485×1.1＋取付10,515")
s += it("リニューアルプレート", "NNN80006K Ｂ用 φ150→φ200", 25, "枚", sig(1500 * 1.1 + 500), 500, "★実勢推定")
s += it("LEDライトバー　Ｃ", "NEL4600ENLE9 6900lm 本体流用", 36, "台", sig(8600 * 1.1 + 4000), 3000, "★実勢推定")
s += it("LED埋込形ベースライト　Ｆ", "XFX459RENLE9 5040lm", 2, "台", lamp(20265, 36300), 9362,
        "実勢20,265×1.1＋取付16,035")
s += it("ライティングダクト　Ｌ", "固定I形 直付 2P15A125V", 15.7, "m", 6190, 2820)
s += it("LEDスポットライト　ＳＰ", "EFS7136W 2000TYPE ダクト用", 26, "個", sig(24000 * 1.1 + 3000), 3000, "★実勢推定")
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
SIG_NET = 2_720_000
s += it("サイネージ設備工事", "アプロ通信 HD026207-2 一式", 1, "式", SIG_NET * 1.1, 0, "NET 2,720,000×1.1")
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
