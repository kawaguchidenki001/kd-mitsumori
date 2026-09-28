# -*- coding: utf-8 -*-
"""正門移設工事　安全対策設備（機器）見積
   構成：河口電機「安全対策設備 ご提案書 v2」（R8.9.17）
   価格：富永電機 見積 GY-1713（R8.9.24）の NET×1.2（Kの指示）
     竹中エンジニアリング 定価187,600 → NET132,000（セット）
     パナソニック V NNY22682LE9 NET80,000／X DYDX2309H NET80,000
     日本セック 定価840,000 → NET714,000（＝定価×0.85）→ 各品 定価×0.85×1.2＝定価×1.02
   富永見積に無いもの（TP-Linkカメラ・microSD・給電材）は単価空欄（Kの指示）
   機器のみ。取付・配線配管・ポール基礎・設定調整は含まない（ご提案書 ※2）
"""
import json, base64
rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, note="", ref=False):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if ref: r["ref"] = True
    rows.append(r)
X12 = lambda net: net * 12 // 10
SEC = lambda teika: teika * 102 // 100          # 日本セック：定価×0.85×1.2

cat("1 出庫時の回転灯・音声（②③）")
it("車両出庫注意喚起システム", "竹中エンジニアリング LHU-100Y-SET(11BE)", 1, "式", X12(132_000), "富永 NET132,000×1.2")
for n, sp, q, u in [("LED回転灯 黄色", "LHU-100Y", 1, "台"), ("壁面取付ブラケット", "BRV-100", 1, "個"),
                    ("赤外線センサー", "PR-11BE", 2, "台")]:
    it(n, sp, q, u, 0, "セット構成品", ref=True)

cat("2 防犯カメラ（⑤）")
it("屋外Wi-Fiカメラ", "TP-Link Tapo C325WB", 1, "台", 0, "富永見積に記載なし（TP-Link取扱なし）")
it("microSDカード", "高耐久 256GB", 1, "枚", 0, "富永見積に記載なし")
it("給電・通信材", "PoEインジェクター・LANケーブル等", 1, "式", 0, "富永見積に記載なし")

cat("3 正門前照明（⑦）")
it("LEDモールライト", "パナソニック NNY22682 LE9", 1, "台", X12(80_000), "富永 NET80,000×1.2")
it("ポール 地中埋込型", "パナソニック DYDX2309H", 1, "本", X12(80_000), "富永 NET80,000×1.2")

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

data = {"header": {"name": "正門移設工事　安全対策設備", "client": "", "honorific": "御中",
                   "date": "2026-09-28", "staff": "河口", "no": "260929"},
        "place": "", "validity": "発行日より1ヶ月",
        "remarks": "機器のみ（取付・配線配管・ポール基礎・設定調整は別途）",
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
    if not r.get("ref"): T[c] = T.get(c, 0) + r["qty"] * r["price"]
    print(f"  {'  ' if r.get('ref') else ''}{(r['name']+' '+r['spec'])[:40]:42}{r['qty']:>2}{r['unit']:<2}{r['price']:>9,}  {r['note']}")
for k, v in T.items(): print(f"{k:30}{v:>10,}")
s = sum(T.values()); print(f"計（税抜）{s:,}／税込 {s + s//10:,}")
