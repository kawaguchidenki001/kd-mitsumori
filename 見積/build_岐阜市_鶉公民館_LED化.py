# -*- coding: utf-8 -*-
"""鶉公民館LED化工事（岐阜市長 柴橋正直 様）R8.11.9
   資料：2 工事費内訳書（様式・品名・数量）、3 仕様書（既設撤去・処分、LED設置、試運転調整。原則 直付）、
         4 別紙 施設照明器具一覧（既設の器具記号・部屋・台数。灯数・ランプは「要確認」）。誘導灯・既設LEDは対象外。
   器具の単価（材料のみ）＝積算実務マニュアル2026（岐阜県）の複合単価 − 取付手間。既設光量合わせの読み替え（★は要確認）：
     ・パイプ吊型 40形（A・B）：LSS1-4-48（4800lm）＋パイプ吊具 ★3,000（手間 ★＋2,000）
     ・直付型 40形 C（事務室・多目的室・会議室）：LSS1-4-48（40形2灯相当 4800lm）★
     ・直付型 40形 D（湯沸室・倉庫）：LSS1-4-30（40形1灯相当 3000lm）★
     ・直付型 20形 E・F：LSS1-2-15（1500lm）
     ・LED角形照明（和室）：★角形 4100lm 級（LRS15-4-41 の材料）、手間 ★10,000
     ・非常灯 H（研修ホール JE8.4V 30W）：K1-LRS11-3（高天井用）、I・J・K：K1-LRS11-1（低天井用）
   機器取替工事費＝取付手間＋撤去（取付の3割）＋撤去品処分（89台 ★1,000/台、蛍光管・電池含む）＋研修ホールの移動式足場 ★30,000。
   雑材及び消耗品費＝器具費×3%、試験及び調整費＝（器具費＋機器取替工事費＋雑材）×2.5%（内訳書の 0.025）。
   諸経費 12%、計を1,000円単位に（諸経費の adj）。
   R8.11.9 Kの指示：内訳書 v2 の型番に差し替え、照明器具は定価×0.5（下の T のコメント）。上の読み替えは初版のもの。税込表示（内訳書に消費税・合計の行あり）。見積No は新規（空欄）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step

# R8.11.9 Kの指示：内訳書 v2 で型番を指定。照明器具は 定価×0.5（定価は Web 検索：パナソニックのカタログ・販売店の希望小売価格、
#   公共型番は三菱電機の同形式品の参考基準価格）。取付手間は積算マニュアル。
KAKE = 0.4                                     # R8.11.9 Kの指示：売値は 定価×0.4（0.5 から変更。原価の入力はやめた）
# 種類: (定価, 取付手間, メモ)
T = {
    "P439": (29_200, 8_754 + 2_000, "パナソニック。手間 LSS9-4-30＋パイプ吊2,000（既設吊りパイプ利用★）"),
    "P469": (39_900, 9_297 + 2_000, "パナソニック。手間 LSS9-4-65＋パイプ吊2,000（既設吊りパイプ利用★）"),
    "S1065": (33_200, 11_131, "三菱 LSS10-4-65 LN9"),
    "S930": (23_700, 8_754, "三菱 LSS9-4-30 LN9"),
    "S915": (19_300, 5_964, "三菱 LSS9-2-15 LN9"),
    "SQ": (98_200, 9_897, "パナソニック（連続調光型）。手間 LSS15-4-41"),
    "E3": (97_200, 13_550, "三菱 EL-DB31111B"),
    "E2": (54_800, 11_425, "三菱 EL-DB21111B（定価★）"),
    "E1": (52_000, 11_274, "三菱 EL-DB11111B"),
}
LIGHT = [  # (品名, 部屋, 台数, 種類, 一覧表)
    ("LEDパイプ吊 40形 XFX439KEN LE9", "1階研修ホール", 28, "P439", "A"),
    ("LEDパイプ吊 40形 XFX469KEN LE9", "1階ステージ", 5, "P469", "B"),
    ("LEDベースライト 直付型 40形 LSS10-4-65", "1階事務室", 6, "S1065", "C"),
    ("LEDベースライト 直付型 40形 LSS10-4-65", "1階多目的室", 4, "S1065", "C"),
    ("LEDベースライト 直付型 40形 LSS10-4-65", "1階会議室１", 5, "S1065", "C"),
    ("LEDベースライト 直付型 40形 LSS10-4-65", "1階会議室２", 12, "S1065", "C"),
    ("LEDベースライト 直付型 40形 LSS9-4-30", "1階湯沸室", 2, "S930", "D"),
    ("LEDベースライト 直付型 40形 LSS9-4-30", "1階倉庫１", 4, "S930", "D"),
    ("LEDベースライト 直付型 40形 LSS9-4-30", "1階倉庫２", 3, "S930", "D"),
    ("LEDベースライト 直付型 20形 LSS9-2-15", "1階物入", 1, "S915", "E"),
    ("LEDベースライト 直付型 20形 LSS9-2-15", "1階倉庫（階段下）", 1, "S915", "F"),
    ("LEDスクエア 直付型 XL682PFVJ LA9", "1階和室", 4, "SQ", "G"),
]
EMER = [
    ("1階研修ホール", 2, "E3", "H"), ("1階ステージ", 1, "E2", "I"), ("1階事務室", 1, "E2", "I"),
    ("1階湯沸室", 1, "E2", "I"), ("1階多目的室", 1, "E2", "I"), ("1階会議室１", 1, "E2", "I"),
    ("1階会議室２", 1, "E2", "I"), ("1階和室", 1, "E2", "I"), ("1階玄関", 1, "E2", "J"),
    ("1階廊下・ホール", 2, "E2", "J"), ("1階廊下", 1, "E2", "J"), ("1階廊下", 1, "E1", "K"),
]
EMER_NAME = {"E3": "LED非常灯専用型 K1-LRS11-3", "E2": "LED非常灯専用型 K1-LRS11-2", "E1": "LED非常灯専用型 K1-LRS11-1"}

rows = []
def cat(n): rows.append({"type": "cat", "name": n})
def it(name, spec, qty, unit, price, note="", pl=0, cost=0):
    r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
    if pl: r["pl"] = int(pl)
    if cost: r["cost"] = int(cost)                 # 原価（KD見積の原価表・粗利用。見積書には出ない）
    rows.append(r); return qty * int(price)

kiki, tori, n_all = 0, 0, 0
cat("1　LED照明器具")
for nm, rm, q, k, ls in LIGHT:
    teika, t, memo = T[k]
    kiki += it(nm, rm, q, "台", sig(teika * KAKE), f"既設光量合わせ（一覧表{ls}）　定価{teika:,}×{KAKE}　{memo}")
    tori += q * t; n_all += q
cat("2　LED非常灯")
for rm, q, k, ls in EMER:
    teika, t, memo = T[k]
    kiki += it(EMER_NAME[k], rm, q, "台", sig(teika * KAKE), f"既設光量合わせ（一覧表{ls}）　定価{teika:,}×{KAKE}　{memo}")
    tori += q * t; n_all += q
assert n_all == 89

cat("3　工事費")
TEKKYO = jsround(tori * 0.3)
SHOBUN = n_all * 1_000
ASHIBA = 30_000
KOJI = sig(tori + TEKKYO + SHOBUN + ASHIBA)
s = kiki
s += it("機器取替工事費", "", 1, "式", KOJI,
        f"取付{tori:,}＋撤去{TEKKYO:,}＋処分★{SHOBUN:,}＋移動式足場★{ASHIBA:,}", jsround((tori + TEKKYO) * 2 / 3))
ZATSU = sig(kiki * 0.03)
s += it("雑材及び消耗品費", "", 1, "式", ZATSU, "器具費×3%")
SHIKEN = sig((kiki + KOJI + ZATSU) * 0.025)
s += it("試験及び調整費", "", 1, "式", SHIKEN, "（器具費＋機器取替工事費＋雑材）×2.5%")

KEIHI = 12.0
k_raw = jsround(s * KEIHI / 100)
TOTAL = (s + k_raw) // 1000 * 1000
cat("4　諸経費")
rows.append({"name": "諸経費", "rate": KEIHI, "adj": TOTAL - s - k_raw})

data = {"header": {"name": "鶉公民館LED化工事", "client": "岐阜市長　柴橋正直", "honorific": "様",
                   "date": "2026-11-09", "staff": "河口", "no": ""},
        "place": "岐阜市中鶉７丁目11番地（鶉公民館）", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
        "addrKind": "public", "taxMode": "in", "taxRate": 10, "rows": rows}
root = "/home/user/kd-mitsumori"
json.dump(data, open(root + "/見積/見積_岐阜市_鶉公民館_LED化.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root + "/q/uzura-kominkan-led.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
open(root + "/見積/取込リンク_岐阜市_鶉公民館_LED化.txt", "w").write(url + "\nhttps://kd-mitsumori.pages.dev/#q=uzura-kominkan-led\n")
sub, cur = {}, None
for r in rows:
    if r.get("type") == "cat": cur = r["name"]; print("【" + cur + "】"); continue
    if "qty" in r:
        a = r["qty"] * r["price"]; sub[cur] = sub.get(cur, 0) + a
        print(f"  {(r['name']+' '+r['spec'])[:34]:36}{r['qty']:>3}{r['unit']}{r['price']:>9,}{a:>10,}  {r['note']}")
for k, v in sub.items(): print(f"{k} 計 {v:,}")
print(f"器具費 {kiki:,}／小計 {s:,}／諸経費 {TOTAL - s:,}（12%={k_raw:,}）／計（税抜）{TOTAL:,}／税込 {TOTAL + jsround(TOTAL*0.1):,}")
