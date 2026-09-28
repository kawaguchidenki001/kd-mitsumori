# -*- coding: utf-8 -*-
"""正門移設工事　安全対策設備（機器）見積
   構成：河口電機「安全対策設備 ご提案書 v2」（R8.9.17）
   価格：富永電機 見積 GY-1713（R8.9.24）の NET×1.2（Kの指示）
     竹中エンジニアリング 定価187,600 → NET132,000（セット）
     パナソニック V NNY22682LE9 NET80,000／X DYDX2309H NET80,000
     日本セック 定価840,000 → NET714,000（＝定価×0.85）→ 各品 定価×0.85×1.2＝定価×1.02
   富永見積に無いもの（TP-Linkカメラ・microSD・給電材）は単価空欄（Kの指示）
   工事費：電気設備工事積算実務マニュアル2026（岐阜県）の複合単価。★は単価表に無く見込んだ項目。
   図面が無いため、配線・配管の長さや掘削量は仮の数量（現地調査で確定）。
"""
import math
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return max(1, int(math.floor(v / step + 0.5))) * step
import json, base64
rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, note="", ref=False, pl=0):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if ref: r["ref"] = True
    if pl: r["pl"] = int(round(pl))
    rows.append(r)
X12 = lambda net: net * 12 // 10
SEC = lambda teika: teika * 102 // 100          # 日本セック：定価×0.85×1.2

cat("1 出庫時の回転灯・音声（②③）")
it("車両出庫注意喚起システム", "竹中エンジニアリング LHU-100Y-SET(11BE)", 1, "式", X12(132_000), "富永 NET132,000×1.2")
for n, sp, q, u in [("LED回転灯 黄色", "LHU-100Y", 1, "台"), ("壁面取付ブラケット", "BRV-100", 1, "個"),
                    ("赤外線センサー", "PR-11BE", 2, "台")]:
    it(n, sp, q, u, 0, "セット構成品", ref=True)
it("回転灯取付", "壁面ブラケット共", 1, "台", 8_000, "★", pl=5_500)
it("赤外線センサー取付", "", 2, "台", 6_000, "★", pl=4_000)
it("動作・音声設定調整", "", 1, "式", 15_000, "★", pl=10_000)

cat("2 防犯カメラ（⑤）")
it("屋外Wi-Fiカメラ", "TP-Link Tapo C325WB", 1, "台", 0, "富永見積に記載なし（TP-Link取扱なし）")
it("microSDカード", "高耐久 256GB", 1, "枚", 0, "富永見積に記載なし")
it("給電・通信材", "PoEインジェクター・LANケーブル等", 1, "式", 0, "富永見積に記載なし")
it("カメラ取付", "", 1, "台", 37_300, "複合単価（固定レンズ付カメラ 取付け費のみ）", pl=25_380)
it("防水コンセント", "2P15A 抜け止め 接地端子付", 1, "個", 4_010, "カメラ電源用", pl=1_889)
it("カメラ設定調整", "Wi-Fi接続・アプリ設定", 1, "式", 10_000, "★", pl=7_000)

cat("3 正門前照明（⑦）")
it("LEDモールライト", "パナソニック NNY22682 LE9", 1, "台", X12(80_000), "富永 NET80,000×1.2")
it("ポール 地中埋込型", "パナソニック DYDX2309H", 1, "本", X12(80_000), "富永 NET80,000×1.2")
it("自動点滅器", "電子式 100V 3A", 1, "個", 14_400, "外灯の点滅用（ご提案書に無いため追加）", pl=4_597)
it("ポール建柱・灯具取付", "", 1, "基", sig(51_888 * 1.47), "複合単価の労務費51,888×1.47（本体別）", pl=51_888)
it("屋外灯基礎", "400×400×1100", 1, "基", 104_000, "複合単価。★仕様は現地で確認", pl=5_080)
it("地中配管", "ＦＥＰ３０", 20, "m", 1_400, "★数量仮", pl=733)
it("埋設標識シート", "幅150 2倍", 20, "m", 380, "★数量仮", pl=113)
it("根切り", "人力", 3.6, "m3", 14_600, "★数量仮（20m×0.3×0.6）", pl=9_906)
it("埋戻し", "人力", 3.6, "m3", 8_000, "★数量仮", pl=5_600)
it("ケーブル", "ＥＭ－ＣＥ３.５－２Ｃ 管内", 20, "m", 1_090, "★数量仮", pl=479)

cat("4 歩行者検知・LED表示（⑧）")
for n, sp, q, u, teika in [("屋外用LED表示器", "日本セック LA(C)60-6(RG)L-O", 1, "台", 510_000),
                           ("メッセージ登録用PCソフト", "CO-ROM", 1, "式", 50_000),
                           ("壁面取付金物", "LA-KNG-O×2", 1, "組", 10_000),
                           ("人感センサー", "MS-100A", 1, "台", 62_000),
                           ("人感センサー取付金物", "BW-14", 1, "個", 5_500),
                           ("中継BOX", "LA-I/F-BOX-B", 1, "台", 58_500),
                           ("RS-232Cケーブル", "RS-232C-CBL", 1, "本", 5_000),
                           ("USBシリアルコンバーター", "CON-USB-SR1", 1, "個", 14_000),
                           ("5年長期保証", "LA(C)60-6(RG)L-O", 1, "式", 125_000)]:
    it(n, sp, q, u, SEC(teika), f"富永 定価{teika:,}→NET×1.2")
it("LED表示器取付", "壁面 取付金物共", 1, "台", 30_000, "★約16kg", pl=20_000)
it("人感センサー取付", "", 1, "台", 8_000, "★", pl=5_500)
it("中継BOX取付", "", 1, "台", 8_000, "★", pl=5_500)
it("信号線", "ＥＭ－ＥＥＦ２.０－２Ｃ 管内", 15, "m", 960, "★数量仮", pl=479)
it("表示文字登録・動作調整", "", 1, "式", 20_000, "★", pl=14_000)

cat("5 電源・共通")
it("分岐ブレーカー増設", "2P", 3, "個", 15_200, "回転灯・カメラ／外灯／表示器", pl=7_445)
it("電源配線", "ＥＭ－ＥＥＦ２.０－２Ｃ 管内", 60, "m", 960, "★数量仮", pl=479)
it("配管", "ＰＦ１６ 露出", 60, "m", 1_650, "★数量仮", pl=1_043)
it("高所作業車", "", 1, "式", 60_000, "Kの標準（1式60,000）")
_sub = sum(r["qty"] * r["price"] for r in rows if "qty" in r and not r.get("ref"))
it("雑材消耗品", "", 1, "式", sig(_sub * 0.03 * 0.3), "工事分の消耗品")

# 経費：法定福利費＝労務費×16.5%（1,000円未満切捨て）／諸経費＝純工事費×10%（計を1,000円単位に）
import math as _m
def jsround(x): return _m.floor(x + 0.5)
_sub = int(round(sum(r["qty"] * r["price"] for r in rows if "qty" in r and not r.get("ref"))))
_lab = sum(r["qty"] * r.get("pl", 0) for r in rows if "qty" in r and not r.get("ref"))
w_raw = jsround(_lab * 0.165); w_amt = w_raw // 1000 * 1000
k_raw = jsround(_sub * 0.10)
TARGET = (_sub + w_amt + k_raw) // 1000 * 1000
rows.append({"name": "法定福利費", "welfare": 16.5, "adj": w_amt - w_raw})
rows.append({"name": "諸経費", "rate": 10.0, "adj": (TARGET - _sub - w_amt) - k_raw})

data = {"header": {"name": "西垣ポンプ正門移設工事", "client": "株式会社川瀬組", "honorific": "御中",
                   "date": "2026-09-28", "staff": "河口", "no": "260929"},
        "place": "", "validity": "発行日より1ヶ月",
        "remarks": "配線・配管の長さ等は現地調査のうえ確定",
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_正門移設工事_安全対策設備.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/seimon-anzen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_正門移設工事_安全対策設備.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=seimon-anzen\n")
c = None; T = {}
for r in rows:
    if r.get("type") == "cat": c = r["name"]; continue
    if "qty" not in r: continue
    if not r.get("ref"): T[c] = T.get(c, 0) + r["qty"] * r["price"]
    print(f"  {'  ' if r.get('ref') else ''}{(r['name']+' '+r['spec'])[:40]:42}{r['qty']:>2}{r['unit']:<2}{r['price']:>9,}  {r['note']}")
for k, v in T.items(): print(f"{k:30}{v:>10,}")
s = int(round(sum(T.values()))); print(f"小計 {s:,}／法定福利費 {w_amt:,}（労務費{_lab:,.0f}）／諸経費 {TARGET-s-w_amt:,}／計（税抜）{TARGET:,}／税込 {TARGET + TARGET//10:,}")
