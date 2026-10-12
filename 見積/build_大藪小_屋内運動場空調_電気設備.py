# -*- coding: utf-8 -*-
"""大藪小学校屋内運動場空調設備設置工事 電気設備工事 見積
   ・明細の書き方＝輪之内町中学校空調設備設置工事（No.2412102 R6.12.11）に準拠
   ・数量＝図面E-02〜E-06から実測（ベクタ座標・1pt=75mm／E-06は1pt=25mm）→ 長さ(m)は×1.2
   ・単価＝tankatool（複合単価）×1.15、四捨五入で上3桁・最小10円
   ・盤類（tankatool対象外）＝輪之内の金額×1.1
"""
import json, math, base64

def sig(v):
    v=float(v)
    if v<=0: return 0
    step=10**(int(math.floor(math.log10(v)))+1-3)
    if step<10: step=10
    return int(math.floor(v/step+0.5))*step
TK=lambda p: sig(p*1.15)        # tankatool×1.15
WA=lambda p: sig(p*1.10)        # 輪之内×1.1
Q =lambda m: round(m*1.2,1)     # 長さ×1.2

rows=[]
def it(name,spec,qty,unit,price,note=''):
    rows.append({"name":name,"spec":spec,"qty":qty,"unit":unit,"price":int(price),"note":note})

# ───────── ケーブル・電線（長さ×1.2）─────────
it("ケーブル","EM-CE3.5sq-3C　管内", Q(548.3), "ｍ", TK(1390), "図面A〜F・1〜3・H〜J：1階446.4＋2階61.9＋室外機置場40.0＝548.3m")
it("ケーブル","EM-CET38sq　管内",    Q(12.0),  "ｍ", TK(6230), "幹線①夜間照明開閉器盤〜L-AC")
it("ケーブル","EM-CE14sq-2C　管内",  Q(3.0),   "ｍ", TK(2300), "配線①分電盤L-AC〜自立ユニット")
it("ケーブル","EM-CE2.0sq-3C　管内", Q(60.0),  "ｍ", TK(1040), "配線④熱源機5.0＋外灯配線抜替えL=55.0m")
it("電線",   "EM-IE5.5sq　管内",    Q(6.3),   "ｍ", TK(800),  "接地線 ED・EDELB")
# ───────── 電線管（長さ×1.2）─────────
it("電線管","GPZ22　露出　溶融亜鉛メッキ", Q(21.6), "ｍ", TK(4840),  "1本区間＋室内機引込立下り12箇所")
it("電線管","GPZ28　露出　溶融亜鉛メッキ", Q(21.6), "ｍ", TK(6320),  "2本区間（北8.3＋南13.3）")
it("電線管","GPZ36　露出　溶融亜鉛メッキ", Q(15.7), "ｍ", TK(7640),  "3本区間（北11.8＋南3.9）")
it("電線管","GPZ42　露出　溶融亜鉛メッキ", Q(45.0), "ｍ", TK(10100), "室外機置場 幹線①・配線H〜J")
it("電線管","GPZ54　露出　溶融亜鉛メッキ", Q(56.3), "ｍ", TK(13800), "4本以上区間（北9.9＋南17.4＋東立上り25.7＋引込3.3）")
it("電線管","F2・WP24　ビニル被覆付",     Q(18.5), "ｍ", TK(2950),  "壁貫通部・機器接続部")
it("電線管","F2・WP50　ビニル被覆付",     Q(3.0),  "ｍ", TK(6460),  "盤・自立ユニット接続部")
it("電線管","CP25　露出（塗装共）",       Q(8.0),  "ｍ", TK(4030),  "屋内露出 非常用コンセント引込3箇所ほか")
it("電線管","EP25　天井内隠ぺい",        Q(16.8), "ｍ", TK(2910),  "2階 GHP4内機 分岐")
it("電線管","EP39　天井内隠ぺい",        Q(15.0), "ｍ", TK(4570),  "2階 GHP4内機 主管")
it("電線管","HIVE16　地中埋設",         Q(6.3),  "ｍ", TK(2010),  "接地線用")
it("電線管","FEP30　地中埋設",          Q(2.5),  "ｍ", TK(1400),  "外灯移設に伴う地中配管延長")
it("電線管付属品","",                  1, "式", 0, "配管費の4.0％（輪之内に準拠）")
it("電線管支持材","",                  1, "式", 0, "配管費の10.8％（輪之内に準拠）")
# ───────── ボックス・配線器具（個数は図面どおり）─────────
it("プルボックス","150×150×150　SUS・WP", 8, "個", TK(18700), "1階7＋2階1")
it("プルボックス","200×200×200　SUS・WP", 4, "個", TK(28500))
it("プルボックス","250×250×250　SUS・WP", 6, "個", TK(41200), "tankatool未収録のため200と300の補間値")
it("プルボックス","500×500×300　SUS・WP", 1, "個", TK(98300), "引込部")
it("丸形露出ボックス","",                3, "個", TK(5040),  "非常用コンセント屋内側")
it("非常用赤色コンセント","2P15A　E付　キャップ付", 3, "個", TK(4010))
it("防水コンセント","2P15A　E付",         1, "個", TK(4010),  "室外機置場")
# ───────── 盤類（輪之内×1.1）─────────
it("分電盤","L-AC　屋外自立型（WP・SUS　国土交通省仕様）", 1, "台", WA(930000), "輪之内 分電盤L-AC 930,000×1.1")
it("開閉器盤","S-AC　屋外壁掛型（WP・SUS）新設",        1, "面", WA(230000), "輪之内 分電盤改修 230,000×1.1")
it("分電盤改修","既設夜間照明開閉器盤（屋外型SUS製）",      1, "式", WA(230000), "輪之内 分電盤改修 230,000×1.1")
# ───────── 接地・その他 ─────────
it("接地工事","ED・EDELB　打込式接地棒14φ×1500",  2, "箇所", TK(10700))
it("接地極埋設標","接地抵抗測定共",                2, "箇所", TK(14100))
it("削孔工事","壁貫通　手はつり（配管貫通口）",       16, "箇所", TK(8200), "図面★印16箇所")
it("外灯移設工事","既設外灯 東へ約2.5m移設　撤去・基礎掘起し・基礎移設据付・再取付共", 1, "式", 0, "図面E-06の外灯移設1〜4・7・9項")
it("点検調査費","中部電気保安協会",                1, "式", WA(55000), "輪之内 55,000×1.1")

# ── 一式項目の金額（配管費に対する輪之内の比率／実勢積上げ）──
pipe = sum(r['qty']*r['price'] for r in rows if r['name']=='電線管')
for r in rows:
    if r['name']=='電線管付属品': r['price']=sig(pipe*0.040)
    if r['name']=='電線管支持材': r['price']=sig(pipe*0.108)
    if r['name']=='外灯移設工事': r['price']=sig(180000)

sub = sum(r['qty']*r['price'] for r in rows)
zap_raw = sub*0.05
zap = int(round((sub+zap_raw)/10000)*10000 - sub)        # 小計＋雑費を1万円単位に（輪之内と同じ作り）
kei_raw = (sub+zap)*0.15
total = int((sub+zap+kei_raw)//1000*1000)
kei = total - sub - zap
print('■ 明細 %d件' % len(rows))
for r in rows:
    print('   %-12s %-34s %7s %-3s %10s %12s' % (r['name'][:12], r['spec'][:34], r['qty'], r['unit'],
          format(r['price'],','), format(int(round(r['qty']*r['price'])),',')))
print('   %-48s %10s %12s' % ('小　計','',format(int(sub),',')))
print('   %-48s %10s %12s' % ('雑費（小計×5％）','',format(zap,',')))
print('   %-48s %10s %12s' % ('諸経費（上記計×15％）','',format(kei,',')))
print('   %-48s %10s %12s' % ('合　計（税抜）','',format(total,',')))
print('   ※配管費計 %s／雑費率 %.2f%%／諸経費率 %.2f%%' % (format(int(pipe),','), zap/sub*100, kei/(sub+zap)*100))

data={"header":{"name":"大藪小学校屋内運動場空調設備設置工事","client":"株式会社大幸建築設計事務所","honorific":"御中",
                "date":"2026-10-12","staff":"河口","no":"261001"},
      "place":"","validity":"発行日より1ヶ月","remarks":"","taxMode":"ex","taxRate":10,
      "rows":rows+[{"name":"雑費","rate":5,"adj":int(zap-round(sub*0.05))},
                   {"name":"諸経費","expense":15,"adj":int(kei-round((sub+zap)*0.15))}]}
root="/home/user/kd-mitsumori"
json.dump(data, open(root+"/見積/見積_大藪小_屋内運動場空調_電気設備.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(data, open(root+"/q/oyabu-taiikukan.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
u="https://kawaguchidenki001.github.io/kd-mitsumori/#import="+base64.urlsafe_b64encode(
    json.dumps(data,ensure_ascii=False,separators=(",",":")).encode()).decode().rstrip("=")
open(root+"/見積/取込リンク_大藪小_屋内運動場空調.txt","w").write(
    u+"\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=oyabu-taiikukan\n")
print('   URL長', len(u))
assert total % 1000 == 0 and (sub+zap) % 10000 == 0
