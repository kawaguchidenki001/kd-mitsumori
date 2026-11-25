# -*- coding: utf-8 -*-
"""岐阜羽島衛生施設組合　照明修繕 2件（管理者 岐阜市長 柴橋正直 様）R8.11.25
   Kの指示：見積をお願いします。内訳の書き方は添付の過去の見積（R7.11.13 No.251115「現場事務所照明修繕」）を参考に、
            工事名・場所・内訳の書き方を全て合わせる。
   資料：照明器具 材料一覧（見積依頼）v3＝中央管理室・水質試験室（2階照明器具配置図 v11）、
                                       v4＝受変電室・廊下等（2階照明器具配置図 v12）→ 図面ごとに1件ずつ見積。
   書き方（過去の見積のとおり）：修繕名「○○照明修繕」、修繕場所「岐阜市境川5丁目147番地」、宛名 2行＋様、自社住所は公共用（柳津）、
     内訳 １．材料費（器具を型番で）→ ２．労務費 1式 → ３．産廃処理費 1式 → ４．諸経費 1式 → 小計 → 消費税相当額 10% → 合計（税込）。
   単価：当初は過去の見積の単価 → R8.11.25 Kの指示で 今の定価×0.4 に（下の TEIKA）。
     XFX459VEN LE9 15,440／XFX420AEN LE9 9,300／XFX210AEN LE9 7,700／XFX200AEN LE9 6,100／NNLG01515 18,900（過去の見積）
     ★XFX429REN LE9 12,480（過去の XFX429PEN の単価）／★XDL459VGN LE9 38,000（同系列 XDL469VGN 希望小売102,200 から×0.4 前後）
     ★XFX420KEN LE9 10,800（反射笠付。XFX420AEN より少し上）
   労務費：過去の見積と同じ 1台 7,500（撤去・取付・結線）、産廃処理費：1台 1,000（撤去器具）。
   諸経費：過去の見積と同じく 約13% で、小計を 1,000円単位に（切り捨て）。見積No は新規（空欄）。
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
# R8.11.25 Kの指示：材料代は 今の定価×0.4（上3桁に丸め）。定価はパナソニックの希望小売価格（税抜、Web で確認）
def sig(v):
    v = float(v); step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return int(math.floor(v / step + 0.5)) * step
KAKE = 0.4
TEIKA = {"XFX459VEN LE9": 44_400, "XFX429REN LE9": 36_600, "XFX420AEN LE9": 26_800, "XFX420KEN LE9": 27_400,
         "XFX210AEN LE9": 22_150, "XFX200AEN LE9": 17_550, "NNLG01515": 54_300,   # XFX200AEN はカタログ画像で確認
         "XDL459VGN LE9": 97_600}          # R8.11.25 Kのカタログ画像：希望小売価格 97,600（税抜）
PRICE = {k: sig(v * KAKE) for k, v in TEIKA.items()}
EST = set()                              # XFX200AEN の定価 17,550 も R8.11.25 Kのカタログ画像で確認   # XFX200AEN の定価は販売店の税込表示 19,305 から逆算（未確認）
NAME = {"NNLG01515": "LED非常照明", "XDL459VGN LE9": "LED非常用照明器具"}
ROOT = "/home/user/kd-mitsumori"

def build(qname, title, items, fname):
    rows = []
    def it(name, qty, unit, price, note=""):
        rows.append({"name": name, "spec": "", "qty": qty, "unit": unit, "price": int(price), "note": note})
        return qty * int(price)
    rows.append({"name": "１．材料費", "spec": "", "qty": "", "unit": "", "price": 0, "note": "", "ref": True})
    s = 0; n = 0
    for model, q in items:
        note = (f"定価{TEIKA[model]:,}×{KAKE}" if model in TEIKA else "定価不明") + ("（★）" if model in EST else "")
        s += it(f"{NAME.get(model, 'LEDベースライト')}　{model}", q, "台", PRICE[model], note)
        n += q
    LAB = int(math.floor(n * 7_500 / 1000 + 0.5) * 1000)    # 1,000円単位（過去の見積も 105,000・131,000）
    s += it("２．労務費", 1, "式", LAB, f"{n}台×7,500（過去の見積と同じ）を1,000円単位に")
    s += it("３．産廃処理費", 1, "式", n * 1_000, f"撤去器具 {n}台×1,000")
    SUB = jsround(s * 1.13) // 1000 * 1000
    s += it("４．諸経費", 1, "式", SUB - s, "約13%（小計を1,000円単位に）")
    assert s == SUB
    data = {"header": {"name": title, "client": "岐阜羽島衛生施設組合", "client2": "管理者　岐阜市長　柴橋正直",
                       "honorific": "様", "date": "2026-11-25", "staff": "河口", "no": ""},
            "place": "岐阜市境川5丁目147番地", "validity": "発行日より1ヶ月", "remarks": "", "notes": [],
            "addrKind": "public", "taxMode": "in", "taxRate": 10, "rows": rows}
    json.dump(data, open(f"{ROOT}/見積/見積_{fname}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(data, open(f"{ROOT}/q/{qname}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    url = "https://kd-mitsumori.pages.dev/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    open(f"{ROOT}/見積/取込リンク_{fname}.txt", "w").write(url + f"\nhttps://kd-mitsumori.pages.dev/#q={qname}\n")
    print("■", title, f"（{n}台）")
    for r in rows:
        if r.get("ref"): print("  " + r["name"]); continue
        print(f"  {r['name']:30}{r['qty']:>3}{r['unit']}{r['price']:>9,}{r['qty']*r['price']:>10,}  {r['note']}")
    print(f"  小計 {SUB:,}／消費税 {jsround(SUB*0.1):,}／合計（税込）{SUB + jsround(SUB*0.1):,}")

# v3：中央管理室・水質試験室（A 23・B 2・C 2）
build("eisei-chuokanri-led", "中央管理室・水質試験室照明修繕",
      [("XFX459VEN LE9", 23), ("XFX429REN LE9", 2), ("XDL459VGN LE9", 2)], "岐阜羽島衛生施設組合_中央管理室水質試験室照明修繕")
# v4：受変電室・廊下等（A 18・B 7・C 3・D 6・E 1・F 1・G 1・H 2）
build("eisei-juhenden-led", "受変電室・廊下等照明修繕",
      [("XFX459VEN LE9", 18), ("XFX429REN LE9", 7), ("XDL459VGN LE9", 3), ("XFX420AEN LE9", 6),
       ("XFX420KEN LE9", 1), ("XFX210AEN LE9", 1), ("XFX200AEN LE9", 1), ("NNLG01515", 2)],
      "岐阜羽島衛生施設組合_受変電室廊下等照明修繕")
