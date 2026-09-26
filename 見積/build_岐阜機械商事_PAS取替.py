# -*- coding: utf-8 -*-
"""岐阜機械商事　高圧気中開閉器（SOG機能付PAS 200A）取替工事　2パターン（方向性／無方向性）
   本体：扇港電機 見積 No.26090892-P001（R8.9.15）の NET×1.2
     方向性  CLD-217SE-D（エナジーサポート）NET 235,000
     無方向性 CLS-215SE-D（エナジーサポート）NET 135,000
   取付・撤去：電気設備工事積算実務マニュアル2026（岐阜県）
     高圧気中開閉器 7.2kV 200A 制御装置付 柱上取付け 労務費 54,039 ×1.47（経費）
     同 撤去費 23,800
   ★＝単価表に無く、実勢から見込んだ項目（要確認）
"""
import json, base64, math

def jsround(x): return math.floor(x + 0.5)
def sig(v):
    v = float(v)
    if v <= 0: return 0
    step = max(10, 10 ** (int(math.floor(math.log10(v))) + 1 - 3))
    return max(1, int(math.floor(v / step + 0.5))) * step

TORI_PL = 54_039
TORI    = sig(TORI_PL * 1.47)          # 79,400（労務費＋経費）
TEKKYO  = 23_800

def build(kind, no, fname):
    hou = (kind == "方向性")
    model, net = ("CLD-217SE-D", 235_000) if hou else ("CLS-215SE-D", 135_000)
    rel = "ＤＧＲ" if hou else "ＧＲ"
    rows = []
    def it(name, spec, qty, unit, price, pl=0, note=""):
        r = {"name": name, "spec": spec, "qty": qty, "unit": unit, "price": int(price), "note": note}
        if pl: r["pl"] = int(round(pl))
        rows.append(r); return qty * int(price)
    s = 0
    s += it("高圧気中開閉器（ＰＡＳ）", f"ＳＯＧ・{rel}付 7.2kV 200A {kind} {model}", 1, "台", sig(net * 1.2), 0,
            f"扇港電機見積 No.26090892 NET{net:,}×1.2")
    s += it("ＰＡＳ取付", "柱上 制御装置共", 1, "台", TORI, TORI_PL, "複合単価の労務費54,039×1.47（本体別）")
    s += it("既設ＰＡＳ撤去", "柱上 制御装置共", 1, "台", TEKKYO, round(TEKKYO / 1.47), "複合単価の撤去費")
    s += it("高圧結線替え", "引込側・負荷側", 1, "式", 30_000, 20_000, "★")
    s += it("制御線接続替え", "ＳＯＧ制御装置", 1, "式", 15_000, 10_000, "★")
    s += it("地絡継電器試験", f"{rel}動作特性試験・復電確認", 1, "式", 35_000, 20_000, "★")
    s += it("停電・中部電力協議", "供給停止・再送電 立会い", 1, "式", 30_000, 0, "★")
    s += it("高所作業車", "柱上作業用", 1, "式", 60_000, 0, "Kの標準（1式60,000）")
    s += it("撤去品処分費", "既設ＰＡＳ", 1, "式", 10_000, 0, "★")
    z = sig(s * 0.03); s += it("雑材消耗品", "", 1, "式", z, 0, "上記計の3%")
    labor = sum(r["qty"] * r.get("pl", 0) for r in rows)
    WELFARE, KEIHI = 16.5, 10.0
    w_raw = jsround(labor * WELFARE / 100); w_amt = w_raw // 1000 * 1000
    k_raw = jsround(s * KEIHI / 100)
    TARGET = (s + w_amt + k_raw) // 1000 * 1000
    k_amt = TARGET - s - w_amt
    rows.append({"name": "法定福利費", "welfare": WELFARE, "adj": w_amt - w_raw})
    rows.append({"name": "諸経費", "rate": KEIHI, "adj": k_amt - k_raw})
    data = {"header": {"name": f"高圧気中開閉器（ＰＡＳ）取替工事　{kind}", "client": "岐阜機械商事", "honorific": "御中",
                       "date": "2026-09-26", "staff": "河口", "no": no},
            "place": "", "validity": "発行日より1ヶ月", "remarks": "",
            "taxMode": "ex", "taxRate": 10, "rows": rows}
    root = "/home/user/kd-mitsumori"
    json.dump(data, open(f"{root}/見積/見積_岐阜機械商事_PAS取替_{kind}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(data, open(f"{root}/q/{fname}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    url = "https://kawaguchidenki001.github.io/kd-mitsumori/#import=" + base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    open(f"{root}/見積/取込リンク_岐阜機械商事_PAS取替_{kind}.txt", "w").write(url + f"\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q={fname}\n")
    print(f"\n==== {kind}（No.{no}）")
    for r in rows:
        if "qty" in r: print(f"  {(r['name']+'　'+r['spec'])[:40]:42}{r['qty']:>3}{r['unit']:<2}{r['price']:>9,}{r['qty']*r['price']:>10,}  {r['note']}")
    print(f"  小計 {s:,}／法定福利費 {w_amt:,}（労務費{labor:,}×16.5%）／諸経費 {k_amt:,}／計（税抜）{TARGET:,}／税込 {TARGET + jsround(TARGET*0.1):,}")
    return TARGET

build("方向性", "260926", "pas-houkou")
build("無方向性", "260927", "pas-muhoukou")
