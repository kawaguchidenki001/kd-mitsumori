# -*- coding: utf-8 -*-
"""令和7年度 肱江川築堤護岸工事　単価見積（クロージャ固定金具の内訳のみ）（木曽川下流河川事務所長 様）No.260711
   R8.11.17 Kの指示で作った赤枠（8品目）だけの見積。R8.11.18：8品目は クロージャ固定金具 SUS製（74,000）の内訳として振り分けた単価にそろえる。
   R8.11.18 Kの指示：赤枠（8品目）以外は不要（さや管など・クロージャ固定金具の見出しの行も出さない）。
   単価・数量は全体版（build_肱江川築堤護岸_単価見積.py → q/hijiegawa-tanka.json）から取る（先に全体版を作ること）。
"""
import json, base64
root = "/home/user/kd-mitsumori"
full = json.load(open(root + "/q/hijiegawa-tanka.json", encoding="utf-8"))
# R8.11.18 Kの指示：クロージャ 小型用（上）・固定金具の内訳8品目・クロージャ再接続材（下）。固定金具の見出しの行は出さない
rows, on = [], False
for r in full["rows"]:
    if r.get("name") == "クロージャ": rows.append(dict(r)); continue
    if r.get("ref") and r["name"].startswith("クロージャ固定金具"): on = True; continue
    if on and r.get("name") == "クロージャ再接続材": rows.append(dict(r)); break
    if on: rows.append(dict(r))
items = [r for r in rows if not r.get("ref")]
assert len(items) == 10 and rows[0]["name"] == "クロージャ" and rows[-1]["name"] == "クロージャ再接続材"
assert sum(r["qty"] * r["price"] for r in items[1:-1]) == 74_000
data = dict(full); data["rows"] = rows
json.dump(data, open(root + "/見積/見積_肱江川築堤護岸_クロージャ固定金具.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/hijiegawa-closure.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_肱江川築堤護岸_クロージャ固定金具.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=hijiegawa-closure\n")
for r in rows:
    if r.get("ref"): print(f"  {r['name']} {r['spec']} {r['price']:,}（内訳表示）"); continue
    print(f"  {(r['name']+' '+r['spec'])[:34]:36}{r['qty']:>4}{r['unit']}{r['price']:>9,}{r['qty']*r['price']:>10,}")
print(f"計（税抜）{sum(r['qty'] * r['price'] for r in items):,}")
