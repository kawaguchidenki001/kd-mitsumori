# -*- coding: utf-8 -*-
"""岐阜市 畜産センター公園　ポール（スッキリポールプラス スピーカー用）納入　岐阜市長 柴橋正直 様
   依頼：岐阜市役所 都市建設部 公園整備課（FAX R8.9.17）単価と納期の照会
   価格：扇港電機 見積 No.26091263-P001（R8.9.25）NET 66,000 ×1.2（Kの指示）
"""
import json, base64
NET = 66_000
rows = [
    {"name": "ポール", "spec": "スッキリポールプラス スピーカー用 XDPG0220H", "qty": 1, "unit": "本",
     "price": NET * 12 // 10, "note": "扇港電機見積 No.26091263 NET66,000×1.2"},
]
# 組合せの内訳（数量だけ出し、金額欄は空欄・合計に入れない）
for code, name, u in [("DDLR0330H", "上部柱 φ89 L=3,000 グレー", "本"),
                      ("DDLH1310H", "下部柱 φ114 L=3,600 グレー", "本"),
                      ("DDTB0211H", "付属品セット 地中配線用", "組")]:
    rows.append({"name": "　" + code, "spec": name, "qty": 1, "unit": u, "price": 0, "ref": True, "note": "XDPG0220Hの構成品"})
data = {"header": {"name": "畜産センター公園　ポール（スピーカー用）納入", "client": "岐阜市長　柴橋正直", "honorific": "様",
                   "date": "2026-09-28", "staff": "河口", "no": "260928"},
        "place": "岐阜市畜産センター公園", "validity": "発行日より1ヶ月", "remarks": "", "notes": ["納期：お打ち合わせ"],
        "addrKind": "public", "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_岐阜市_畜産センター公園_ポール.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/gifu-chikusan-pole.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_岐阜市_畜産センター公園_ポール.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=gifu-chikusan-pole\n")
t = NET * 12 // 10
print(f"計（税抜）{t:,}／消費税 {t//10:,}／税込 {t + t//10:,}")
