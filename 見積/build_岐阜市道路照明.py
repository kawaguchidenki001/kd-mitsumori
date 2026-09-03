# -*- coding: utf-8 -*-
"""岐阜市 道路照明設備設置工（H=10m）1基 — 見積
単価表SJ03000（1基当り）の構成と、道路照明設備設置工(1)(2)の数量をそのまま踏襲。
共通仮設費・現場管理費・一般管理費は内訳表の上位で一括計上される様式のため、本見積は直接工事費のみ。
"""
import json, base64
DB = json.load(open('unit_prices.json'))
def q(n,s,w=None):
    r=[e for e in DB if e['name']==n and e['spec']==s and (w is None or e['work']==w)]
    assert r,(n,s,w); return r[0]
oga  = q('建柱車 トラック式アースオーガオーガ径','450mm 吊能力2.0t 運転機械経費')
pole = q('建柱･鋼管柱','10m 建柱車')
eart = q('打込式接地棒(単独)','14mmφ×1500')
ie55 = q('電線','EM-IE 5.5mm2×1','管内')
jari = q('砂利地業','')
c26  = q('ケーブル','EM-EEF 2.6mm-2C','管内')
c16  = q('ケーブル','EM-EEF 1.6mm-3C','管内')
auto = q('自動点滅器','電子式(JIS2形) 200V 6A')

DBN, EST = "複合単価", "実勢による推定。要確認"
rows=[]; T=0
def cat(n): rows.append({"type":"cat","name":n})
def it(name,spec,qty,unit,price,note=""):
    global T
    price=int(round(price)); rows.append({"name":name,"spec":spec,"qty":qty,"unit":unit,"price":price,"note":note})
    T+=qty*price

cat("基礎工")
it("基礎掘削及びスパイラルダクト立込","φ500 2m以下",1,"基", oga['composite_price']/10 + 5000,
   f"単価表SJ03010。{DBN} 建柱車トラック式アースオーガ450mm吊能力2.0t {oga['composite_price']:,}円/日を10基/日で割戻し＋普通作業員。要確認")
it("スパイラルダクト","φ500×t0.6",1.7,"m",3500, f"型枠兼用。{EST}")
it("基礎砕石","RC-30 t=100",0.2,"m2", jari['composite_price']*0.1,
   f"{DBN} 砂利地業 {jari['composite_price']:,}円/m3×t0.1m")
it("基礎コンクリート","24-8-25(20)高炉 小型構造物・人力打設",0.3,"m3",25000,
   f"生コン＋人力打設。施工P単価表CB240010相当。{EST}")
it("アンカーフレーム","4-M24-L600",1,"組",25000, EST)
it("接地設置工","φ14×1500 D種接地3m以内（接地棒・低減剤共）",1,"極",
   eart['composite_price'] + ie55['composite_price']*3 + 3500,
   f"単価表SJ03030。{DBN} 打込式接地棒(単独)14mmφ×1500 {eart['composite_price']:,}円＋電線EM-IE5.5×3m＋接地抵抗低減剤1袋（低減剤はDB未収録につき推定）")
it("根巻きコンクリート","18-8-40BB 0.075m3・型枠0.6m2共",1,"箇所",6000,
   f"単価表SJ03040。生コン＋型枠。{EST}")

cat("灯柱工")
it("道路照明灯柱","IS10.3B 埋設型 単独 H=10m（STK400 溶融亜鉛メッキHDZT77＋ポリエステル粉体塗装 シルバーメタリック）",
   1,"本",240000, f"照明用テーパーポール。複合単価DB未収録（DBの建柱･鋼管柱10mは無塗装の一般鋼管柱）につき{EST}")
it("道路照明灯建柱","350kg以下 建柱車",1,"基", pole['composite_price']-q('建柱･鋼管柱','10m 建柱車')['material_cost'],
   f"施工歩掛表WE210800。{DBN} 建柱･鋼管柱10m建柱車 {pole['composite_price']:,}円の取付手間（労務費＋経費）")
it("引込フックバンド","",1,"個",5000, EST)
it("管理銘板","",1,"枚",3000, EST)

cat("照明器具取付工")
it("LED照明器具","KCE150-3C相当品",1,"組",150000,
   f"道路照明用LED 150W級。複合単価DB未収録（DBのLED屋外灯投光器18000lm以上の材料費138,475円が近い水準）につき{EST}")
it("照明器具取付","新設（高所作業車共）",1,"台",25000, f"施工歩掛表WE211500。{EST}")
it("専用ケーブル","直線型ポール用",1,"本",8000, EST)
it("ジョイントユニット","テストスイッチ有",1,"個",12000, EST)
it("電線","VVF2.6mm×2C",10,"m", c26['composite_price'], f"{DBN} ケーブルEM-EEF2.6mm-2C 管内")
it("電線","VVF1.6mm×3C",10,"m", c16['composite_price'], f"{DBN} ケーブルEM-EEF1.6mm-3C 管内")

cat("自動点滅器取付")
it("光電式自動点滅器","200V/6A 電子式 分離型 受台付（ポール取付共）",1,"個", auto['composite_price']+2200,
   f"単価表SJ03070。{DBN} 自動点滅器 電子式(JIS2形)200V 6A {auto['composite_price']:,}円＋分離型受台付の割増")
it("ターミナルキャップ","φ22",1,"個",1500, EST)
it("ニップル","φ22",1,"個",800, EST)

data={"header":{"name":"道路改良工事　道路照明設備設置工（H=10m）","client":"岐阜市",
                "honorific":"御中","date":"2026-08-29","staff":"河口"},
      "place":"岐阜市加野4丁目地内","remarks":"","taxMode":"out","taxRate":10,"rows":rows}

net=sum(r['qty']*r['price'] for r in rows if 'qty' in r)
assert abs(net-T)<1
for r in rows:
    if r.get('type')=='cat': print('■',r['name'])
    else: print(f"   {r['name'][:20]:20} {r['qty']:>5}{r['unit']:3} {r['price']:>9,} {r['qty']*r['price']:>10,.0f}")
print("-"*58)
print(f"   道路照明設備設置工 1基当り（税抜・経費別） {net:>10,.0f}")
print(f"   参考 税込 {net*1.1:>10,.0f}")

out='/home/user/kd-mitsumori/見積/見積_岐阜市_道路照明設備設置工1基.json'
open(out,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=1))
b64=base64.urlsafe_b64encode(json.dumps(data,ensure_ascii=False,separators=(",",":")).encode()).decode().rstrip("=")
url="https://kawaguchidenki001.github.io/kd-mitsumori/#import="+b64
open('/home/user/kd-mitsumori/見積/取込リンク_岐阜市道路照明.txt','w').write(url)
assert json.loads(base64.urlsafe_b64decode(b64+"=="*2).decode())==data
print("URL長",len(url),"round-trip OK")
