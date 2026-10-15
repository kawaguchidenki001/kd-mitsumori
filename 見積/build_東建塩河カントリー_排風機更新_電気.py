# -*- coding: utf-8 -*-
"""東建塩河カントリー2階男子便所排風機更新工事　電気工事（戸島工業株式会社 御中）
   現地写真（天井見上げ・天井内排風機EF-14）より拾い出し。
   ・白枠で示された天井撤去範囲内の器具＝ダウンライト1台・天井埋込スピーカー1個 → 脱着
   ・天井内排風機 EF-14 の電源切離し・再接続
   単価：複合単価（tankatool）の撤去費および取付手間（労務費＋経費）による。
   運搬費は実費（車両1台×2回：撤去時・復旧時）。法定福利費は計上しない（ご指示）。
"""
import json, math, base64

def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - 3)
    if step < 10: step = 10
    return int(math.floor(v / step + 0.5)) * step

rows = []
def it(name, spec, qty, unit, price, note=""):
    rows.append({"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note})

# 複合単価DB（tanka-search）より
#  LED埋込天井灯 ダウンライト LRS1-08 LN：撤去 2,600／労務 5,894＋経費 3,862＝取付手間 9,756
#  スピーカー 3W 天井埋込形（アッテネータなし）：撤去 2,430／労務 5,499＋経費 3,221＝取付手間 8,720
#  電動機結線 直入始動方式（労務費のみ）：複合 7,210／撤去 2,160
it("天井照明　撤去",   "ダウンライト　既設再使用（仮保管共）",        1, "台", sig(2600),
   "複合単価 LED埋込天井灯LRS1-08LN の撤去費")
it("天井照明　再取付", "ダウンライト　結線・点灯確認共",            1, "台", sig(9756),
   "同 取付手間（労務5,894＋経費3,862）")
it("スピーカー　撤去", "天井埋込形　既設再使用（仮保管共）",         1, "個", sig(2430),
   "複合単価 スピーカー3W天井埋込形 の撤去費")
it("スピーカー　再取付","天井埋込形　結線・音出し確認共",           1, "個", sig(8720),
   "同 取付手間（労務5,499＋経費3,221）")
it("排風機　電源切離し", "ＥＦ－１４　既設フレキ・プルボックス部",      1, "台", sig(2160),
   "複合単価 電動機結線（直入始動方式）の撤去費")
it("排風機　電源再接続", "ＥＦ－１４　結線・絶縁測定・試運転共",       1, "台", sig(7210),
   "同 複合単価（労務費のみ）")
it("雑材消耗品",      "圧着端子・絶縁テープ・結束材等",            1, "式", 1000)
it("運搬費",        "車両１台（撤去時・復旧時　各１回）",          2, "回", 8000,
   "実費計上（ご指示）")

sub = sum(r["qty"] * r["price"] for r in rows)
KEI = 12.0                                   # 諸経費＝純工事費×12%（社内標準）
kei_raw = math.floor(sub * KEI / 100 + 0.5)
total = int((sub + kei_raw) // 1000 * 1000)  # 計（税抜）を1,000円単位に
kei = total - sub
rows.append({"name": "諸経費", "rate": KEI, "adj": int(kei - kei_raw)})

f = lambda v: format(int(round(v)), ",")
print("■ 明細")
for r in rows:
    if "qty" not in r:
        print("   %-44s %10s %10s" % (r["name"] + "（純工事費×%.0f％）" % KEI, "", f(kei))); continue
    print("   %-16s %-30s %3s %-3s %9s %10s"
          % (r["name"][:16], r["spec"][:30], r["qty"], r["unit"], f(r["price"]), f(r["qty"] * r["price"])))
print("   %-52s %10s" % ("小　計（純工事費）", f(sub)))
print("   %-52s %10s" % ("計（税抜）", f(total)))
print("   %-52s %10s" % ("消費税10％", f(math.floor(total * 0.1 + 0.5))))
print("   %-52s %10s" % ("合　計（税込）", f(total + math.floor(total * 0.1 + 0.5))))
assert total % 1000 == 0

data = {"header": {"name": "東建塩河カントリー2階男子便所排風機更新工事",
                   "client": "戸島工業株式会社", "honorific": "御中",
                   "date": "2026-10-15", "staff": "河口", "no": "261016"},
        "place": "", "validity": "発行日より1ヶ月", "remarks": "",
        "taxMode": "ex", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_東建塩河カントリー_排風機更新_電気.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/shiokawa-haifuki.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
u = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(
    json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_東建塩河カントリー_排風機更新.txt", "w").write(
    u + "\nhttps://kd-mitsumori.pages.dev/#q=shiokawa-haifuki\n")
print("   URL長", len(u))
