# -*- coding: utf-8 -*-
"""作業内容一覧（場所ごと）：西村様邸改装電気工事（ユタカ建設株式会社 御中）R8.11.21
   Kの指示：作業内容を項目にした PDF も（場所ごとに）。金額は入れない。
   内容は見積（build_ユタカ建設_西村様邸_改装電気.py）と、参考図・LIXIL／TOTO の資料から。
   出力：見積/作業内容_西村様邸_改装電気.pdf（HTML を Chromium で A4 縦の PDF に）
"""
import html, os, subprocess, sys, tempfile

ROOT = "/home/user/kd-mitsumori"
OUT = ROOT + "/見積/作業内容_西村様邸_改装電気.pdf"

HEAD = {"title": "作 業 内 容 一 覧（電気設備工事）", "client": "ユタカ建設株式会社　御中",
        "name": "西村様邸改装電気工事", "place": "岐阜市上佐波2-287", "date": "令和8年11月21日",
        "co": "河口電機株式会社", "staff": "担当：河口"}

# (場所, 補足, [(作業内容, 備考)])
SECTIONS = [
    ("浴室", "ユニットバス取替（TOTO シンラ HLシリーズ 1717）", [
        ("既設ユニットバスの電源ケーブル・換気ダクト・リモコンの取外し、新設ユニットバスへ再取付", ""),
        ("浴室換気暖房乾燥機　専用電源配線・接続", "200V 20A"),
        ("楽湯・床ワイパー用 電源ボックス　専用電源配線・接続", "100V 15A"),
        ("浴室照明（LEDダウンライト等）・おそうじ浴槽　電源接続", ""),
        ("洗面所リモコン　配線・取付", ""),
        ("浴室テレビ　取付（電源・アンテナ接続）", "支給品"),
    ]),
    ("洗面・脱衣室", "洗面化粧台 下台取替・内装改修", [
        ("コンセント・スイッチの移設、取替", ""),
        ("洗面所暖房機（ユニットバスオプション品）　専用電源配線・取付", "200V 20A／支給品"),
        ("洗面化粧台 壁付照明　取外し・復旧", ""),
    ]),
    ("トイレ", "洋便器取替（TOTO ネオレスト 手洗器付）", [
        ("コンセント移設、取替（便器用）", ""),
        ("電灯配線、照明器具取付", "支給品"),
        ("スイッチ取付", ""),
        ("手洗い（カウンター付）自動水栓用 電源新設", ""),
    ]),
    ("キッチン", "キッチン・キッチン収納新設（LIXIL リシェル）", [
        ("IHクッキングヒーター・自動水栓　取外し・再取付", ""),
        ("食洗器　専用電源配線・コンセント", "200V"),
        ("家電コンセント（4ヶ所）　専用電源配線", "専用回路×2"),
        ("既設家電コンセントの移設、取替", ""),
        ("既設換気扇撤去、新設レンジフード用 換気ダクト配管", "φ150"),
        ("レンジフード用コンセント配線", "専用"),
        ("照明器具　取替", "支給品"),
        ("ライティングレール新設、スポットライト取付", "スポットライトは支給品"),
    ]),
    ("分電盤", "分電盤取替", [
        ("分電盤取替　主幹 ELB 3P 50A（中性線欠相保護付）、分岐30回路", "100V×20、200V×7、予備3"),
        ("既設20回路の結線替え", "100V×16、200V×4"),
        ("新設7回路の接続（楽湯・床ワイパー、家電コンセント×2、レンジフード、浴室暖房乾燥機、洗面所暖房機、食洗器）",
         "100V×4、200V×3"),
        ("既設分電盤　撤去・処分", ""),
    ]),
    ("その他", "", [
        ("ロスナイ取替（材料・取付）", "既設品 撤去・処分共"),
    ]),
]

esc = html.escape
rows = []
n = 0
for place, sub, items in SECTIONS:
    rows.append(f'<tr class="sec"><td colspan="3"><b>{esc(place)}</b>'
                + (f'<span class="sub">　{esc(sub)}</span>' if sub else "") + "</td></tr>")
    for work, note in items:
        n += 1
        rows.append(f'<tr><td class="no">{n}</td><td>{esc(work)}</td><td class="note">{esc(note)}</td></tr>')

FONT = "file://" + ROOT + "/pdfassets/bizudpgothic.ttf"
doc = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
@font-face {{ font-family: "BIZUDPGothic"; src: url("{FONT}"); }}
@page {{ size: A4 portrait; margin: 12mm 13mm 11mm 13mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: "BIZUDPGothic", sans-serif; color: #111; font-size: 10pt; margin: 0; }}
h1 {{ text-align: center; font-size: 16pt; letter-spacing: 2px; margin: 0 0 3mm; border-bottom: 1.5px solid #111; padding-bottom: 2mm; }}
.top {{ display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 4mm; }}
.top .l div {{ margin: 1mm 0; }}
.top .l .to {{ font-size: 13pt; border-bottom: 1px solid #111; padding-bottom: 1mm; min-width: 85mm; }}
.top .r {{ text-align: right; }}
.top .r .co {{ font-size: 13pt; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ border: 0.6pt solid #555; padding: 1.15mm 2mm; vertical-align: top; }}
th {{ background: #e9eef3; font-weight: normal; }}
tr.sec td {{ background: #f4f6f8; border-top: 1pt solid #333; font-size: 11pt; }}
tr.sec .sub {{ font-size: 9.5pt; color: #333; }}
td.no {{ width: 9mm; text-align: center; }}
td.note {{ width: 54mm; font-size: 9pt; }}
.foot {{ margin-top: 4mm; font-size: 9.5pt; }}
</style></head><body>
<h1>{esc(HEAD['title'])}</h1>
<div class="top"><div class="l">
<div class="to">{esc(HEAD['client'])}</div>
<div>工事名：{esc(HEAD['name'])}</div><div>工事場所：{esc(HEAD['place'])}</div></div>
<div class="r"><div>{esc(HEAD['date'])}</div><div class="co">{esc(HEAD['co'])}</div><div>{esc(HEAD['staff'])}</div></div></div>
<table><thead><tr><th>No.</th><th>作業内容</th><th>備考</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table>
<div class="foot">※支給品（浴室テレビ・洗面所暖房機・照明器具・スポットライト）は取付のみです。</div>
</body></html>"""

tmp = tempfile.mkdtemp()
hp = os.path.join(tmp, "work.html")
open(hp, "w", encoding="utf-8").write(doc)
js = """
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(500);
  await p.pdf({ path: process.argv[3], format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close(); })().catch(e => { console.error(e); process.exit(1); });
"""
jp = os.path.join(tmp, "pdf.js")
open(jp, "w").write(js)
subprocess.run(["node", jp, hp, OUT], check=True)
assert os.path.getsize(OUT) > 10_000
print("saved", OUT, "items", n)
