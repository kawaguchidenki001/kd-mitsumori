# -*- coding: utf-8 -*-
"""境川中学校 夜間照明設備新設工事 参考見積 生成
設計書(FAX 2026-08-25)の細目別内訳の行構成・数量をそのまま踏襲する。
設計書は「材料行 → 小計 → 電工費(1式) → 高所作業車損料(1式) → 合計」の構成であり、
材料行の単価は材料費、労務は電工費に一括計上する様式のため、
複合単価データの p(複合単価) − t(取付手間=労務費+経費) を材料単価に、
Σ(数量×t) を電工費に充てる。
"""
import json, gzip, base64, math

DB = json.loads(gzip.open('/home/user/kd-mitsumori/.claude/skills/mitsumori-one-shot/references/unit_prices_slim.json.gz','rt',encoding='utf-8').read())
def q(name, spec, work=None):
    hit=[e for e in DB if e['n']==name and e['s']==spec and (work is None or e['w']==work)]
    assert len(hit)==1, (name,spec,work,len(hit))
    return hit[0]

def r100(x): return int(round(x/100.0))*100

# ---- 単価拾い（複合単価DB） ---------------------------------------------
box   = q('プルボックス','SS300×300×200 WP-SUS')          # 支柱BOX
cet38 = q('ケーブル','EM-CET 38mm2','管内')                # 幹線
gp42  = q('電線管','GP-42 溶融亜鉛めっき','露出')          # 露出配管 GZ42（/m）
fep50 = q('波付硬質ポリエチレン管(FEP)','50','地中')
cet14 = q('ケーブル','EM-CET 14mm2','FEP管内配線')
hive28= q('電線管','HIVE 28','露出')                        # 立上配管（/m）
eef26 = q('ケーブル','EM-EEF 2.6mm-3C','管内')
eef20 = q('ケーブル','EM-EEF 2.0mm-3C','管内')
pole  = q('建柱･コンクリート柱','16m 建柱車 根かせ・バンド共(16-19-50)')
panel = q('分電盤','主幹:MCCB 3P 100AF／75A 分岐:MCCB 2P1E 20A-10 予備-2')
mccb  = q('配線用遮断器','MCCB 3P 100A RC：25kA')
kousho= q('高所作業車','トラック架装・伸縮ブーム（作業高9.7m）バスケット型 積載荷重200kg 運転機械経費')
neg   = q('根切り','機械 バックホウ0.13m3')
umeb  = q('埋戻し','機械 バックホウ0.13m3')
zando = q('建設発生土処理','人力（場内敷ならし ）')
flood = q('LED屋外灯 投光器','LPJ1N-180 LN 一般形','18000lm以上')   # 電工費の手間参考

def mat(e): return e['p']-e['t']          # 材料費 ＝ 複合単価 − 取付手間
G42_L, HIVE_L = 3.66, 4.0                  # 定尺（厚鋼電線管3.66m／HIVE4m）
KOUSHO = kousho['p']                       # 高所作業車 日額

rows=[]; labor=0.0
def cat(name): rows.append({"type":"cat","name":name})
def it(name, spec, qty, unit, price, note="", t=0.0):
    global labor
    labor += qty*t
    price=int(round(price))
    rows.append({"name":name,"spec":spec,"qty":qty,"unit":unit,"price":price,"note":note})
    return qty*price

# ===== 1. 受電設備工事 ====================================================
cat("1. 受電設備工事")
s=0
s+=it("キュービクル内改造費","ブレーカー増設他材工共",1,"式",150000,
       "材工共。MCCB 3P100A 複合単価44,900＋盤内改造・二次側配線・停電作業の推定。キュービクルメーカー確認要")
PANEL=240000
s+=it("夜間照明盤","WP、SUS、鍵付き",1,"面",PANEL,
       "分電盤(主幹3P100AF/75A・分岐20A-10)材料費%d円に、SUS防雨外箱割増と点滅回路(タイマー・電磁接触器)を加算した推定。盤メーカー見積要"%mat(panel),
       t=panel['t'])
s+=it("支柱BOX(WP、SUS)","300×300×200",6,"面",mat(box),
       "複合単価 プルボックス SS300×300×200 WP-SUS の材料費", t=box['t'])
s+=it("幹線ケーブル","EM-CET38sq",120,"m",mat(cet38),
       "複合単価 EM-CET 38mm2 管内 の材料費", t=cet38['t'])
pipe1_mat = mat(gp42)*G42_L
s+=it("露出配管(厚鋼電線管)","GZ42",32,"本",pipe1_mat,
       "複合単価 電線管GP-42溶融亜鉛めっき 露出 の材料費 %d円/m×3.66m(定尺)"%mat(gp42), t=gp42['t']*G42_L)
P1 = pipe1_mat*32
s+=it("同上附属品","カップリング・ノーマルベンド・ボックスコネクタ他",1,"式",r100(P1*0.15),"配管材料費の15%")
s+=it("配管支持材","",1,"式",r100(P1*0.10),"配管材料費の10%")
mat1 = s-150000
s+=it("雑材消耗品","",1,"式",r100(mat1*0.03),"材料費計の3%")
s+=it("電工費","",1,"式",r100(labor),"複合単価の取付手間(労務費＋経費)の積上げ")
s+=it("高所作業車損料","",1,"式",KOUSHO*2,
       "%d円/日×2日。作業高9.7m級の日額。体育館外壁の露出配管用"%KOUSHO)
S1=s; labor=0.0

# ===== 2. 分岐配管配線設備工事 ===========================================
cat("2. 分岐配管配線設備工事")
s=0
s+=it("埋設配管","FEP50",500,"m",mat(fep50),"複合単価 波付硬質ポリエチレン管(FEP)50 地中 の材料費",t=fep50['t'])
s+=it("分岐配線ケーブル","EM-CET14sq",620,"m",mat(cet14),"複合単価 EM-CET 14mm2 FEP管内配線 の材料費",t=cet14['t'])
hive_mat = mat(hive28)*HIVE_L
s+=it("立上配管(合成樹脂管)","HIVE28",24,"本",hive_mat,
      "複合単価 電線管HIVE28 露出 の材料費 %d円/m×4m(定尺)。4本/柱×6柱"%mat(hive28), t=hive28['t']*HIVE_L)
s+=it("立上配線ケーブル","EM-EEF2.6-3C",120,"m",mat(eef26),"複合単価 EM-EEF 2.6mm-3C 管内 の材料費。20m/柱×6柱",t=eef26['t'])
s+=it("投光器用配線ケーブル","EM-EEF2.0-3C",50,"m",mat(eef20),"複合単価 EM-EEF 2.0mm-3C 管内 の材料費",t=eef20['t'])
P2 = mat(fep50)*500 + hive_mat*24
s+=it("同上附属品","ベンド・接続材・防水処理材他",1,"式",r100(P2*0.15),"配管材料費の15%")
s+=it("配管支持材","",1,"式",r100(P2*0.10),"配管材料費の10%")
mat2 = s
s+=it("雑材消耗品","",1,"式",r100(mat2*0.03),"材料費計の3%")
s+=it("電工費","",1,"式",r100(labor),"複合単価の取付手間(労務費＋経費)の積上げ")
s+=it("高所作業車損料","",1,"式",KOUSHO*3,
      "%d円/日×3日。作業高9.7m級の日額。16m柱には作業高20m級が必要につき要確認"%KOUSHO)
DOBOKU = neg['p']*90 + umeb['p']*60
s+=it("土木費","掘削・埋戻し(FEP50埋設用)",1,"式",r100(DOBOKU),
      "掘削幅0.3m×深0.6m×500m＝90m3。根切り(機械BH0.13)%d円/m3×90＋埋戻し(機械BH0.13)%d円/m3×60"%(neg['p'],umeb['p']))
s+=it("残土運搬・処分費","",1,"式",r100(zando['p']*36),
      "残土30m3×ほぐし率1.2＝36m3。建設発生土処理(人力・場内敷ならし)%d円/m3で代用。場外運搬処分費は要確認"%zando['p'])
S2=s; labor=0.0

# ===== 3. 建柱工事 ========================================================
cat("3. 建柱工事")
s=0
s+=it("コンクリート柱","16-19-500",6,"本",mat(pole),
      "複合単価 建柱･コンクリート柱 16m建柱車 根かせ・バンド共(16-19-50) %d円の材料費"%pole['p'])
s+=it("同上運搬費","特車申請他含む",1,"式",300000,
      "16m長尺柱6本。特殊車両通行許可申請＋トレーラー運搬4台分の推定。運送会社見積要")
s+=it("建柱費","アースオーガ車使用",6,"本",pole['t'],
      "上記複合単価の取付手間(労務費＋経費＝建柱車運転経費含む)")
s+=it("残土運搬処理費","",1,"式",r100(zando['p']*7.5),
      "建柱穴φ0.7m×深2.7m×6本＝6.2m3×ほぐし率1.2＝7.5m3。建設発生土処理%d円/m3"%zando['p'])
s+=it("セフティーガードポール用","SGPE-P100-200",6,"枚",24000,
      "イワブチ セフティガード ポール用 幅1000×長2000（取付バンド共）。複合単価DB・器具定価データとも未収録のため実勢からの推定。★単価要確認")
S3=s

# ===== 4. 投光器設置工事 ==================================================
cat("4. 投光器設置工事")
s=0
FL, LV, BR = 302000, 65500, 112700
s+=it("水銀灯700W相当LED灯","NYS35245K-LE2",24,"台",FL,
      "パナソニック パークビームER 25,400lm/143W。定価302,000円・掛率未適用。4台/組×6基")
s+=it("前方カットルーバー","NYK40355",24,"台",LV,
      "NYK40355の定価未確認。同クラス(水銀灯700形相当用)NYK41005 定価65,500円で代用。掛率未適用。4台/組×6基")
s+=it("投光器架台(省施工型)","XDYK2400",6,"組",BR,
      "パナソニック 4灯用投光器台 省施工型。定価112,700円・掛率未適用。1組/基×6基")
mat4=s
s+=it("雑材消耗品","",1,"式",r100(mat4*0.02),"材料費計の2%")
FL_T = flood['t']
s+=it("電工費","",1,"式",r100(FL_T*24*0.7),
      "複合単価 LED屋外灯 投光器(18000lm以上)の取付手間%d円/台×24台×0.7。省施工型架台による地組・クレーン建込のため0.7掛"%FL_T)
s+=it("高所作業車損料","",1,"式",KOUSHO*2,"%d円/日×2日。照射角調整用"%KOUSHO)
S4=s

# ===== 単価の掛率と丸め（ご指示 R8.9.10）=================================
#   全体は1.3倍。キュービクル内改造費・土木費・建柱費のみ2倍。
#   丸めは 100円単位（切上げ）、10万円以上は1,000円単位（切上げ）。
X2 = {"キュービクル内改造費", "土木費", "建柱費"}
def r_price(v):
    if v <= 0: return 0
    step = 1000 if v >= 100000 else 100
    return int(math.ceil(round(v/step, 9))) * step
S1 = S2 = S3 = S4 = 0
_CAT2SUM = {"1. 受電設備工事": "S1", "2. 分岐配管配線設備工事": "S2",
            "3. 建柱工事": "S3", "4. 投光器設置工事": "S4"}
_cur = None
_sums = {"S1": 0, "S2": 0, "S3": 0, "S4": 0}
for _r in rows:
    if _r.get("type") == "cat":
        _cur = _CAT2SUM.get(_r["name"]); continue
    if "qty" not in _r: continue
    _m = 2.0 if _r["name"] in X2 else 1.3
    _r["price"] = r_price(_r["price"] * _m)
    _r["note"] = (_r["note"] + "／" if _r["note"] else "") + ("2倍" if _m == 2.0 else "1.3倍")
    if _cur: _sums[_cur] += _r["qty"] * _r["price"]
S1, S2, S3, S4 = _sums["S1"], _sums["S2"], _sums["S3"], _sums["S4"]

# ===== 諸経費 =============================================================
cat("諸経費")
rows.append({"name":"共通仮設費","rate":5,   "note":"直接工事費×5%（標準率。要調整）"})
rows.append({"name":"現場管理費","expense":17,"note":"純工事費(直接工事費＋共通仮設費)×17%（標準率。要調整）"})
_direct=sum(r['qty']*r['price'] for r in rows if r.get('type')!='cat' and 'qty' in r)
def _jsr(x): return math.floor(x+0.5)
_kari=_jsr(_direct*0.05); _jun=_direct+_kari
_gen=_jsr(_jun*0.17);     _genka=_jun+_gen
_ippan_raw=_jsr(_genka*0.12)
_TARGET=(_genka+_ippan_raw)//1000*1000          # 工事価格（税抜）を1,000円単位（切捨て）
rows.append({"name":"一般管理費","expense":12,"adj":_TARGET-_genka-_ippan_raw,
             "note":"工事原価×12%（標準率。要調整）＋端数調整（工事価格を1,000円単位に）"})

data={
 "header":{"name":"境川中学校　夜間照明設備新設工事","client":"岐阜市 ぎふ魅力づくり推進部 市民スポーツ課",
           "honorific":"御中","date":"2026-09-09","staff":"河口","no":"260909"},
 "place":"境川中学校（岐阜市柳津町上佐波東3丁目70番地）",
 "remarks":"","taxMode":"out","taxRate":10,"rows":rows}

# ---- 検算 ----------------------------------------------------------------
direct=sum(r['qty']*r['price'] for r in rows if r.get('type')!='cat' and 'qty' in r)
kari=round(direct*0.05); jun=direct+kari
gen=round(jun*0.17); genka=jun+gen
ippan=_TARGET-genka; price=genka+ippan
tax=round(price*0.10)
print("1.受電設備工事      %12s" % f"{S1:,.0f}")
print("2.分岐配管配線設備  %12s" % f"{S2:,.0f}")
print("3.建柱工事          %12s" % f"{S3:,.0f}")
print("4.投光器設置工事    %12s" % f"{S4:,.0f}")
print("直接工事費          %12s  (検算 %s)" % (f"{S1+S2+S3+S4:,.0f}", f"{direct:,.0f}"))
print("共通仮設費 5%%       %12s" % f"{kari:,}")
print("現場管理費 17%%      %12s" % f"{gen:,}")
print("一般管理費 12%%      %12s" % f"{ippan:,}")
print("工事価格(税抜)      %12s" % f"{price:,}")
print("消費税10%%           %12s" % f"{tax:,}")
print("合計(税込)          %12s" % f"{price+tax:,}")
print("明細行数", sum(1 for r in rows if r.get('type')!='cat'), "/ 分類", sum(1 for r in rows if r.get('type')=='cat'))
assert abs(direct-(S1+S2+S3+S4))<1

out='/home/user/kd-mitsumori/見積/見積_境川中学校_夜間照明設備新設工事.json'
open(out,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=1))
payload=json.dumps(data,ensure_ascii=False,separators=(",",":"))
b64=base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
url="https://kawaguchidenki001.github.io/kd-mitsumori/#import="+b64
open('/tmp/claude-0/-home-user-kd-mitsumori/de15de47-5fe2-519c-bfeb-a42031aa4390/scratchpad/url.txt','w').write(url)
print("URL長", len(url))
# 再パース検算
assert json.loads(base64.urlsafe_b64decode(b64+"=="*2).decode())==data
print("round-trip OK ->", out)

# ---- 短い取込リンク（q/sakaigawa.json） ----
import os
qdir='/home/user/kd-mitsumori/q'; os.makedirs(qdir, exist_ok=True)
_d=dict(data); _d.pop("print", None)                   # 短縮リンクは自動印刷なし
open(os.path.join(qdir,'sakaigawa.json'),'w',encoding='utf-8').write(json.dumps(_d,ensure_ascii=False,indent=1))
open('/home/user/kd-mitsumori/見積/取込リンク_境川中学校.txt','w').write(
    url+"\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=sakaigawa\n")
print("短いリンク https://kawaguchidenki001.github.io/kd-mitsumori/#q=sakaigawa")
