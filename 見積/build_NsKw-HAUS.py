# -*- coding: utf-8 -*-
"""ＮｓＫｗ－ＨＡＵＳ 新築工事（名古屋市名東区社口）— 電気工事 見積
提出先：株式会社廣瀬住建／設計：城秀幸建築設計室。図面 E-1〜E-4／P-1 より拾い出し。
・照明器具は器具表(E-1)の品番・個数・定価による（掛率0.65）。仕様欄は器具記号＋型番のみ
・スイッチ／コンセント／弱電の箇所数は配線図(E-2〜E-4)の読み取り値（要照合）
・電線量は回路数と平均こう長からの推定（要確認）
"""
import json, base64, gzip, math, os

def sig(v):
    """単価の丸め：四捨五入で上3桁、最小単位は10円（1円単位は出さない）"""
    v = float(v)
    if v <= 0: return 0
    step = 10 ** (int(math.floor(math.log10(v))) + 1 - 3)
    if step < 10: step = 10
    n = int(math.floor(v / step + 0.5))
    return (n if n >= 1 else 1) * step

_R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = json.loads(gzip.open(_R + "/.claude/skills/mitsumori-one-shot/references/unit_prices_slim.json.gz",
                          "rt", encoding="utf-8").read())
def q(n,s,w=None):
    r=[e for e in DB if e['n']==n and e['s']==s and (w is None or e['w']==w)]
    assert r,(n,s,w); return r[0]['p']

RATE = 0.65        # 照明器具の掛率（定価×0.65）

SW1   = q('埋込形スイッチの取付け費','1Ｐ15Ａ×1')          # 3040
SW3W  = q('埋込形スイッチの取付け費','3Ｗ15Ａ×1')          # 3940
SW4W  = q('埋込形スイッチの取付け費','4Ｗ15Ａ×1')          # 4550
CN2P  = q('埋込形コンセントの取付け費','2Ｐ15Ａ×1')        # 3000
CNE   = q('埋込形コンセントの取付け費','2Ｐ15Ａ×1 接地極付') # 3720
TV    = q('テレビ端子','SH-7F 1端子接栓形')                 # 10600
LAN   = q('情報用モジュラージャック','カテゴリー6 1個用')     # 4250
C16   = q('ケーブル','EM-EEF 1.6mm-2C','木造部分サドル止め･ステープル止め')  # 1010
C20   = q('ケーブル','EM-EEF 2.0mm-2C','木造部分サドル止め･ステープル止め')  # 1290
C163  = q('ケーブル','EM-EEF 1.6mm-3C','木造部分サドル止め･ステープル止め')  # 1300

# ---- 器具表 E-1（記号・品番・定価・個数）確定値 ----
FIX = [
 ("Ａ－１","LGD3110VLB1","2F:BR-1、BR-2",10200,6),
 ("Ａ－２","LGD3110VLE1","1F:サニタリー／2F:BR-2、BR-3",9200,5),
 ("Ｂ","XAD1130VKCB1","1F:多目的室",12500,1),
 ("Ｃ－１","LGDC3104VLE1","1F:SCL",26200,1),
 ("Ｃ－２","LGDC1104VLE1","1F:WC",23300,1),
 ("Ｄ－１","SLD3033VLB1","1F:L、D",22800,5),
 ("Ｄ－２","SLD1030VLB1","1F:K",19700,5),
 ("Ｅ","XAD3432VCE1","1F:L",21300,1),
 ("Ｆ","XAD3412VCB1","2F:ワードローブ",20000,1),
 ("Ｇ－１","XAD3410VCB1","2F:BR-3",14900,1),
 ("Ｇ－２","XAD3410VCE1","2F:BR-3、パウダールーム",14900,3),
 ("Ｇ－３","XAD3410VCE1","2F:ワードローブ、ブリッジ、WC",14900,7),
 ("Ｈ","SLD1310VLB1","1F:L",20800,2),
 ("Ｉ","SLB80541LB1","2F:BR-3",23900,3),
 ("Ｊ","SLD1039VLB1","1F:ENT",22200,1),
 ("Ｋ","LRDC3144VLE1","外部",26200,1),
 ("Ｌ","LRD3101VLE1","外部",7800,2),
 ("Ｍ－１","NTN81352","1F:ENT、L、サンルーム、D",46200,5),
 ("Ｍ－２","NTN81332","1F:ENT、L、サンルーム、サニタリー",27000,4),
 ("Ｍ－３","NTN81322","1F:D",17500,1),
 ("Ｎ","LGBC70069","2F:パウダールーム",22000,1),
 ("Ｏ","SLBJ71000","2F:ブリッジ",14400,2),
 ("Ｐ－１","LGWC51552LE1","地下ガレージ",26000,1),
 ("Ｐ－２","LGW51502LE1","地下ガレージ",14400,3),
 ("Ｑ","LGW46153KLE1","外部 門扉",39000,1),
 ("Ｒ","LGWC47001CE1","外部",45000,2),
 ("Ｓ","LGW40081LE1","外部",35000,6),
 ("Ｔ－１","DSY5236AWE","1F:L",56000,4),
 ("Ｔ－２","DSY5233AWE","1F:L",26000,3),
]
NFIX = sum(n for *_ ,n in FIX)
TEIKA = sum(p*n for *_ ,p,n in FIX)

rows=[]
def cat(n): rows.append({"type":"cat","name":n})
def it(name,spec,qty,unit,price,note=""):
    rows.append({"name":name,"spec":spec,"qty":qty,"unit":unit,"price":int(price),"note":note})
    return qty*int(price)

READ = "配線図(E-2〜E-4)の読み取り値。要照合"

def sumrow(name):
    rows.append({"name":name,"spec":"","qty":0,"unit":"","price":0,"sum":True})

# 箇所数（配線の本数と器具・スイッチ・コンセントの数を連動させる）
N_SW1, N_SW3, N_SW4, N_SWF = 34, 8, 6, 2               # 片切・3路・4路・換気（消し遅れ）
N_CN2, N_CNE, N_CNW, N_CNA, N_CN200 = 30, 6, 4, 6, 1   # 2口・接地極付・防水・エアコン・200V
N_CIR = 20                                             # 分電盤の回路数

T=0
# ===== 01 電灯コンセント設備（スイッチ・コンセント・配線をまとめる）=====
cat("01 電灯コンセント設備")
T+=it("埋込スイッチ","片切 1P15A",N_SW1,"箇所",SW1, f"{READ}／複合単価 埋込形スイッチの取付け費 1P15A×1")
T+=it("埋込スイッチ","3路 3W15A",N_SW3,"箇所",SW3W, f"{READ}／複合単価 3W15A×1")
T+=it("埋込スイッチ","4路 4W15A",N_SW4,"箇所",SW4W, f"{READ}／複合単価 4W15A×1")
T+=it("消し遅れスイッチ","DF形 トイレ換気用",N_SWF,"箇所",SW1+2000,"1F・2F WC。消し遅れタイマ付につき加算")
T+=it("ライティングコントローラ","NQ28752WZ 5回路 マルチ調光",2,"台",93000,
      "図面注記『ライコンはNQ28752WZ/Panasonicとする』。ライコン①②の2系統。定価・掛率未適用")
T+=it("ライコン 子機","信号線式",2,"台",25000,"1F階段・キッチン脇。品番未指定につき実勢による推定。要確認")
T+=it("2口コンセント","2P15A",N_CN2,"箇所",CN2P, f"{READ}／複合単価 埋込形コンセントの取付け費 2P15A×1")
T+=it("接地極付コンセント","2P15A",N_CNE,"箇所",CNE, f"{READ}／冷蔵庫・洗濯機・ガス乾太ほか")
T+=it("防水コンセント","2P15A 接地極付",N_CNW,"箇所",CNE+2500, f"{READ}／防雨カバー加算")
T+=it("エアコン用コンセント","2P15A 接地極付",N_CNA,"箇所",CNE,
      "機器リストP-1のAC-1〜AC-6で確定")
T+=it("200Vコンセント","2P20A 接地極付",N_CN200,"箇所",CNE+3000,"1F:サニタリー 洗濯機・ガス乾太用")
# 配線は「1カ所いくら」。単価は No.260114（にぎり長次郎岐阜城東通店）の実績単価。
T+=it("電灯配線","EM-EEF1.6-2C",NFIX,"ケ所",2800,"器具1台あたり配線一式。器具79台分")
T+=it("スイッチ配線","片切",N_SW1,"ケ所",4200,"No.260114の実績単価")
T+=it("スイッチ配線","3路",N_SW3,"ケ所",5500,"★片切4,200＋送り線分")
T+=it("スイッチ配線","4路",N_SW4,"ケ所",6500,"★片切4,200＋送り線分")
T+=it("スイッチ配線","換気用",N_SWF,"ケ所",6500,"No.260114の実績単価")
T+=it("コンセント配線","2口",N_CN2,"ケ所",3400,"No.260114の実績単価")
T+=it("コンセント配線","接地極付",N_CNE,"ケ所",4800,"No.260114のEET単価")
T+=it("コンセント配線","防水",N_CNW,"ケ所",5200,"No.260114の実績単価")
T+=it("コンセント配線","エアコン専用",N_CNA,"ケ所",14000,"No.260114の専用回路単価")
T+=it("コンセント配線","200V専用",N_CN200,"ケ所",14500,"No.260114の専用・防水単価")
T+=it("回路配線","分電盤〜各回路",N_CIR,"ケ所",4800,"No.260114の実績単価。分電盤20回路")
_zat_at = len(rows)                        # 雑材消耗品を差し込む位置（01の末尾）

# ===== 02 照明器具（定価→小計→値引き→計→取付工事費）=====
cat("02 照明器具")
for sym,spec,loc,p,n in FIX:
    T+=it(f"照明器具 {sym}",spec,n,"台",p,f"{loc}／器具表E-1の定価")
sumrow("小　計")
NEBIKI = sum(sig(p*RATE)*n for *_,p,n in FIX) - TEIKA          # 定価計との差額
T+=it("値引き",f"照明器具 定価の{RATE}掛け",1,"式",NEBIKI,"掛率0.65")
sumrow("計")
T+=it("照明器具 取付工事費","ダウンライト・ライン照明ほか",NFIX,"台",3000,
      "住宅用照明器具の取付手間。複合単価DBは公共のベースライト基準で住宅用ダウンライトに過大なため実勢による")

# ===== 03 弱電設備 =====
cat("03 弱電設備")
T+=it("マルチメディアコンセント","",3,"箇所",sig(TV+LAN), f"{READ}／1F:L、2F:BR-2、BR-3")
T+=it("テレビ端子","SH-7F 1端子接栓形",3,"箇所",TV, f"{READ}／複合単価 テレビ端子SH-7F")
T+=it("LAN・電話モジュラ","CAT6 1個用",3,"箇所",LAN, f"{READ}／複合単価 情報用モジュラージャックCAT6")
T+=it("テレビドアホン","WP-24B 7型ワイド",1,"式",74600,
      "玄関子機D＋ハンズフリー受d。products.jsonの定価・掛率未適用。機種は要確認")
T+=it("増設室内子機","",2,"台",22000,"1F:キッチン脇・ENT脇。品番未定につき実勢による推定。要確認")
T+=it("弱電配線","同軸・LAN・インターホン線",1,"式",
      sig(q('SHF 同軸ケーブル','S-5C-FB 衛星放送用')*60 + q('LAN用ケーブル UTPケーブル0.5mm','カテゴリー6 4P')*80 + 900*40),
      "複合単価 S-5C-FB・UTP CAT6 4P による。こう長は推定につき要確認")
PF28 = q('合成樹脂製可とう電線管','PF- 28','隠ぺい･コンクリート打込み')   # 2,380/m
T+=it("HDMI用空配管","PF28 2本 壁内〜床下",1,"式",sig(PF28*14),
      "1F:L 天井プロジェクタ用。PF28×2本、こう長7m/本と見込む（要確認）")

# ===== 04 火災警報設備 =====
cat("04 火災警報設備")
T+=it("住宅用火災警報器","無線連動型 煙式",5,"箇所",12000,
      f"{READ}／寝室BR-1〜3・階段ほか。複合単価DBは自火報用煙感知器のみのため実勢による。機種要確認")

# ===== 05 幹線・分電盤 =====
cat("05 幹線・分電盤")
T+=it("住宅用分電盤","単3 100A 20回路",1,"面",120000,
      "2F EPS内。複合単価DBは公共用のみのため住宅用の実勢による。回路数確定後に品番決定。要確認")
T+=it("電気引込工事","中部電力申請共",1,"式",60000,
      "2F東側に引込点表示。引込線取付点金具・計器盤・申請。負担金の要否は要確認")

# 雑材消耗品（全体の3%）を 01 の末尾に差し込む
ZATSU = sig(T*0.03); T+=ZATSU
rows.insert(_zat_at, {"name":"雑材消耗品","spec":"","qty":1,"unit":"式","price":ZATSU,"note":"上記計の3%"})

cat("諸経費")
KEIHI = 15
_net = int(round(sum(r['qty']*r['price'] for r in rows if 'qty' in r)))
_raw = int(_net*KEIHI/100 + 0.5)
_TGT = (_net + _raw)//1000*1000                     # 計（税抜）を1,000円単位（切捨て）
rows.append({"name":"諸経費","rate":KEIHI,"adj":(_TGT-_net)-_raw,
             "note":"純工事費×15%（現場管理費・一般管理費相当）＋端数調整"})

data={"header":{"name":"ＮｓＫｗ－ＨＡＵＳ　新築工事　電気工事","client":"株式会社廣瀬住建",
                "honorific":"御中","date":"2026-09-21","staff":"河口","no":"260922"},
      "place":"名古屋市名東区社口1丁目311","remarks":"","taxMode": "ex","taxRate":10,"rows":rows}

net=int(round(sum(r['qty']*r['price'] for r in rows if 'qty' in r)))
sho=_TGT-net; pre=_TGT; tax=int(pre*0.1+0.5)
bad=[(r['name'],r['price']) for r in rows if 'price' in r and r['price']>0
     and r['price'] % max(10, 10**(int(math.floor(math.log10(r['price'])))+1-3))]
print("単価ルール違反:", bad or "なし")
zero=[r["name"] for r in rows if r.get("price")==0 and not r.get("sum")]
print(f"照明器具 {NFIX}台 定価計 {TEIKA:,}")
print(f"純工事費 {net:,} ／ 諸経費15% {sho:,} ／ 工事価格 {pre:,} ／ 税込 {pre+tax:,}")
print(f"明細 {sum(1 for r in rows if 'qty' in r)} 件、うち単価0（要確認） {len(zero)} 件:")
for z in zero: print("   -",z)

out='/home/user/kd-mitsumori/見積/見積_NsKw-HAUS新築_電気工事.json'
open(out,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=1))
b64=base64.urlsafe_b64encode(json.dumps(data,ensure_ascii=False,separators=(",",":")).encode()).decode().rstrip("=")
url="https://kawaguchidenki001.github.io/kd-mitsumori/#import="+b64
open(_R+'/q/nskw-haus.json','w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=1))
open('/home/user/kd-mitsumori/見積/取込リンク_NsKw-HAUS.txt','w').write(
    url+"\nhttps://kawaguchidenki001.github.io/kd-mitsumori/#q=nskw-haus\n")
assert json.loads(base64.urlsafe_b64decode(b64+"=="*2).decode())==data
print("URL長",len(url),"round-trip OK")
