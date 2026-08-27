# -*- coding: utf-8 -*-
"""かにの華北方店 照明器具取替工事 — 3行構成版"""
import json, base64

FULL = json.load(open('/tmp/claude-0/-home-user-kd-mitsumori/de15de47-5fe2-519c-bfeb-a42031aa4390/scratchpad/unit_prices.json'))
PROD = json.load(open('/home/user/kd-mitsumori/products.json'))['items']

FIX = next(p for p in PROD if p['model']=='XFX450DEN LE9')['price']      # 33,600
u = next(e for e in FULL if e['name']=='LED直付天井灯 ベースライトLSS9-4-48'
         and e['spec']=='LN 一般形' and e['work']=='4800lm以上 5300lm以下')
INSTALL, REMOVE = u['labor_cost']+u['expense'], u['removal_cost']        # 9,066 / 2,210
ZAI = 1700                                                              # 雑材消耗品（器具材料費5%）
TORIKAE = FIX + INSTALL + REMOVE + ZAI                                  # 46,576

SHOBUN = 800 + 150*2 + 3000                                             # 4,100
SHOKEI = round((TORIKAE + SHOBUN) * 0.15)                               # 7,601

rows = [
 {"name":"照明器具取替","spec":"蛍光灯40W2灯用 → XFX450DEN LE9（iD 40形 直付Dスタイル W230 5200lm 昼白色）",
  "qty":1,"unit":"台","price":TORIKAE,
  "note":"器具%s（定価・掛率未適用）＋取付費%s＋既存器具撤去%s＋雑材消耗品%s。取付費・撤去費は複合単価 LSS9-4-48 LN一般形(4800〜5300lm)による"
         % (f"{FIX:,}", f"{INSTALL:,}", f"{REMOVE:,}", f"{ZAI:,}")},
 {"name":"撤去品処分費","spec":"蛍光灯器具1台・蛍光ランプ2本","qty":1,"unit":"式","price":SHOBUN,
  "note":"器具処分800＋ランプ処分150×2本＋運搬(処分場搬入・マニフェスト共)3,000。単価DB未収録につき実勢による推定。要確認"},
 {"name":"諸経費","spec":"","qty":1,"unit":"式","price":SHOKEI,
  "note":"純工事費%s×15%%（現場管理費・一般管理費相当）" % f"{TORIKAE+SHOBUN:,}"},
]

data = {
 "header":{"name":"かにの華北方店　照明器具取替工事","client":"株式会社フクダ",
           "honorific":"御中","date":"2026-08-27","staff":"河口"},
 "place":"かにの華 北方店","remarks":"","taxMode":"out","taxRate":10,"rows":rows}

pre = sum(r['qty']*r['price'] for r in rows); tax = round(pre*0.10)
for r in rows: print("%-12s %2s%s %10s   %s" % (r['name'],r['qty'],r['unit'],f"{r['price']:,}",f"{r['qty']*r['price']:,}"))
print("-"*46)
print("工事価格（税抜） %10s" % f"{pre:,}")
print("消費税 10%%       %10s" % f"{tax:,}")
print("合計（税込）     %10s" % f"{pre+tax:,}")
assert pre == TORIKAE + SHOBUN + SHOKEI == 58277

out='/home/user/kd-mitsumori/見積/見積_かにの華北方店_照明器具取替工事.json'
open(out,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=1))
b64=base64.urlsafe_b64encode(json.dumps(data,ensure_ascii=False,separators=(",",":")).encode()).decode().rstrip("=")
url="https://kawaguchidenki001.github.io/kd-mitsumori/#import="+b64
open('/home/user/kd-mitsumori/見積/取込リンク_かにの華北方店.txt','w').write(url)
assert json.loads(base64.urlsafe_b64decode(b64+"=="*2).decode())==data
print("URL長",len(url),"round-trip OK")
