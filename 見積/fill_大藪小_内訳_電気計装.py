# -*- coding: utf-8 -*-
"""大藪小学校屋内運動場空調設備設置工事 内訳（設計書 xlsx）に 電気・計装を記入（R8.10.15）
   使い方：python3 fill_大藪小_内訳_電気計装.py <大藪小の内訳.xlsx> <出力.xlsx>
   ・輪之内中の内訳の書き方（品名・仕様・単位・備考「積算マニュアル」）に合わせる
   ・単価は 電気設備工事積算実務マニュアル2026（岐阜県）の複合単価。塗装ありは 電線管＋塗装工事（同マニュアル）
   ・記入したセルは赤字、記入できないセル（見積が必要・マニュアルに無い）は黄色で塗りつぶす
   ・数量は 図面 v10 の拾い（build_大藪小_電気設備_v10.py）と 計装の拾い（build_大藪小_計装設備.py）
   元のブックには図形・外部リンク・入力規則があるので、openpyxl で保存せず XML を直接書き換える
   （書式は既存セルの書式を複製して赤字／黄色を付ける。変えたセルと合計の計算結果はここで計算して書き込む）。
"""
import sys, re, zipfile, html

SRC, OUT = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(SRC)
files = {n: zin.read(n) for n in zin.namelist()}
order = zin.namelist()

def esc(s): return html.escape(str(s), quote=False)

# ---------------- styles ----------------
st = files["xl/styles.xml"].decode("utf8")
def section(tag):
    m = re.search(r"<%s count=\"(\d+)\"[^>]*>(.*?)</%s>" % (tag, tag), st, re.S)
    return m
def items(body, tag):
    return re.findall(r"<%s\b[^>]*/>|<%s\b[^>]*>.*?</%s>" % (tag, tag, tag), body, re.S)
fonts = items(section("fonts").group(2), "font")
fills = items(section("fills").group(2), "fill")
xfs = items(section("cellXfs").group(2), "xf")
new_fonts, new_fills, new_xfs = [], [], []
YELLOW_FILL = '<fill><patternFill patternType="solid"><fgColor rgb="FFFFFF00"/><bgColor indexed="64"/></patternFill></fill>'
yellow_fill_id = len(fills); new_fills.append(YELLOW_FILL)
red_font_cache, xf_cache = {}, {}

def red_font(fid):
    if fid in red_font_cache: return red_font_cache[fid]
    f = fonts[fid]
    if f.endswith("/>"): f = "<font></font>"
    f = re.sub(r"<color\b[^>]*/>", "", f)
    if "<name" in f: f = f.replace("<name", '<color rgb="FFFF0000"/><name', 1)
    else: f = f.replace("</font>", '<color rgb="FFFF0000"/></font>')
    nid = len(fonts) + len(new_fonts); new_fonts.append(f); red_font_cache[fid] = nid
    return nid

def setattr_(x, k, v):
    if re.search(r'\b%s="' % k, x): return re.sub(r'\b%s="[^"]*"' % k, '%s="%s"' % (k, v), x, 1)
    return x.replace("<xf ", '<xf %s="%s" ' % (k, v), 1)

def shrink_(x):
    """縮小して全体を表示（折り返しは外す）"""
    if x.endswith("/>"): x = x[:-2] + "></xf>"
    m = re.search(r"<alignment\b([^>]*?)/?>(?:</alignment>)?", x)
    if m:
        a = re.sub(r'\s(?:wrapText|shrinkToFit)="[^"]*"', "", m.group(1))
        x = x[:m.start()] + '<alignment%s shrinkToFit="1"/>' % a + x[m.end():]
    else:
        x = re.sub(r"(<xf\b[^>]*>)", r'\1<alignment shrinkToFit="1"/>', x, 1)
    return setattr_(x, "applyAlignment", "1")

def style(s, red=False, yellow=False, shrink=False, left=False):
    key = (s, red, yellow, shrink, left)
    if key in xf_cache: return xf_cache[key]
    x = xfs[s]
    if shrink: x = shrink_(x)
    if left: x = re.sub(r'(<alignment\b[^>]*?)\s*horizontal="[^"]*"', r"\1", x).replace("<alignment", '<alignment horizontal="left"', 1)
    if red:
        fid = int(re.search(r'fontId="(\d+)"', x).group(1))
        x = setattr_(setattr_(x, "fontId", red_font(fid)), "applyFont", "1")
    if yellow:
        x = setattr_(setattr_(x, "fillId", yellow_fill_id), "applyFill", "1")
    nid = len(xfs) + len(new_xfs); new_xfs.append(x); xf_cache[key] = nid
    return nid

# ---------------- sheets ----------------
wb = files["xl/workbook.xml"].decode("utf8")
rels = files["xl/_rels/workbook.xml.rels"].decode("utf8")
rid2t = {}
for m in re.finditer(r"<Relationship\b[^>]*>", rels):
    a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(0)))
    rid2t[a["Id"]] = a["Target"]
sheet_file = {}
for m in re.finditer(r"<sheet\b[^>]*>", wb):
    a = dict(re.findall(r'([\w:]+)="([^"]*)"', m.group(0)))
    sheet_file[html.unescape(a["name"])] = "xl/" + rid2t[a["r:id"]].lstrip("/").replace("xl/", "")
sheets = {}
def sx(name):
    f = sheet_file[name]
    if f not in sheets: sheets[f] = files[f].decode("utf8")
    return f

def col2n(c):
    n = 0
    for ch in c: n = n * 26 + ord(ch) - 64
    return n

def put(name, ref, value=None, formula=None, red=False, yellow=False, clear=False, base=None, force=None, left=False):
    """セル ref を書き換え。value(str/int/float) か formula（=なし）。clear=True で値・数式を消す（書式は残す）"""
    f = sx(name); s = sheets[f]
    col, row = re.match(r"([A-Z]+)(\d+)", ref).groups(); row = int(row)
    rm = re.search(r'<row r="%d"[ >].*?</row>|<row r="%d"[^>]*/>' % (row, row), s, re.S)
    if not rm: raise SystemExit(f"row {row} not found in {name}")
    rx = rm.group(0)
    if rx.endswith("/>"): rx = rx[:-2] + "></row>"
    cm = (re.search(r'<c r="%s"(?: [^>]*?)?/>' % ref, rx)                       # 空セル（自己終了）
          or re.search(r'<c r="%s"(?: [^>]*)?(?<!/)>.*?</c>' % ref, rx, re.S))       # 値のあるセル
    old_s = int(re.search(r' s="(\d+)"', cm.group(0)).group(1)) if cm and ' s="' in cm.group(0) else (base or 0)
    if force is not None: old_s = force
    shrink = isinstance(value, str) and not clear     # R8.10.15 Kの指示：文字がはみ出さないよう 縮小して全体を表示
    sid = style(old_s, red, yellow, shrink, left) if (red or yellow or shrink or left) else old_s
    if clear or (value is None and formula is None):
        cx = '<c r="%s" s="%d"/>' % (ref, sid)
    elif formula is not None:
        cx = '<c r="%s" s="%d"><f>%s</f></c>' % (ref, sid, esc(formula))
    elif isinstance(value, (int, float)):
        cx = '<c r="%s" s="%d"><v>%s</v></c>' % (ref, sid, value)
    else:
        cx = '<c r="%s" s="%d" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, sid, esc(value))
    if cm:
        rx2 = rx[:cm.start()] + cx + rx[cm.end():]
    else:   # 列順に挿入
        cells = list(re.finditer(r'<c r="([A-Z]+)\d+"', rx))
        pos = None
        for c in cells:
            if col2n(c.group(1)) > col2n(col): pos = c.start(); break
        if pos is None: pos = rx.rindex("</row>")
        rx2 = rx[:pos] + cx + rx[pos:]
    sheets[f] = s[:rm.start()] + rx2 + s[rm.end():]

AFTER_MERGE = ("phoneticPr", "conditionalFormatting", "dataValidations", "hyperlinks", "printOptions", "pageMargins",
               "pageSetup", "headerFooter", "rowBreaks", "colBreaks", "customProperties", "cellWatches", "ignoredErrors",
               "smartTags", "drawing", "legacyDrawing", "legacyDrawingHF", "picture", "oleObjects", "controls",
               "webPublishItems", "tableParts", "extLst")
def merge(name, rng):
    """rng（例 A1:V1）を結合。左上以外のセルが空であることを確認"""
    f = sx(name); s = sheets[f]
    a, b = rng.split(":"); row = re.match(r"[A-Z]+(\d+)", a).group(1)
    rx = re.search(r'<row r="%s"[ >].*?</row>' % row, s, re.S).group(0)
    for c in re.finditer(r'<c r="([A-Z]+)%s"[^>]*?(?:/>|>(.*?)</c>)' % row, rx, re.S):
        if col2n(a[:-len(row)]) < col2n(c.group(1)) <= col2n(b[:-len(row)]) and re.search(r"<[vf]>|<is>", c.group(2) or ""):
            raise SystemExit(f"merge {name}!{rng}: {c.group(1)}{row} is not empty")
    if "<mergeCells" in s:
        s = re.sub(r'<mergeCells count="(\d+)">', lambda m: '<mergeCells count="%d">' % (int(m.group(1)) + 1), s, 1)
        s = s.replace("</mergeCells>", '<mergeCell ref="%s"/></mergeCells>' % rng, 1)
    else:
        end = s.index("</sheetData>") + len("</sheetData>")
        pos = min([m.start() for t in AFTER_MERGE for m in [re.compile(r"<%s\b" % t).search(s, end)] if m] or [s.index("</worksheet>")])
        s = s[:pos] + '<mergeCells count="1"><mergeCell ref="%s"/></mergeCells>' % rng + s[pos:]
    sheets[f] = s

RED, YEL = dict(red=True), dict(red=True, yellow=True)
M = "積算マニュアル"; D = "　　〃"

# ================= 電気（明細） =================
E = "電気（明細）"
# R8.10.15 Kの指示：PB 250 は 250×250×200 に。外灯移設は1式でなく分けて、できるだけマニュアルの金額で（移設には10tラフター）。
#   保安協会の点検は 85,000。マニュアルに無いもの・マニュアルから算出したものは単価を黄色に。
# R8.10.15 Kの指示：防草シート等復旧は削除。基礎の掘起し・移設据付は マニュアルの機器搬出費・搬入費（岐阜県、円/t×質量）で出し、
#   10tラフターは無し。基礎は E-06 外灯姿図（参考 1/50）で 約400×400×600 → 0.096㎥×2.4t/㎥≒0.23t → 250kg以下 114,000円/t。
KISO = 26200   # 114,000×0.23＝26,220 → 3桁
# R8.10.15 Kの指示：盤は昨年の見積（輪之内中 R7.10.6 L-AC 1,240,000・S-AC 130,000）に1割乗せた金額が定価、その80%で入れる
#   L-AC 1,240,000×1.1×0.8＝1,091,200 → 1,090,000、S-AC 130,000×1.1×0.8＝114,400 → 114,000（3桁）
BAN_L, BAN_S = 1090000, 114000
LABEL = "LABEL"
P1 = [  # 1枚目 rows 5-24（20行）：(品名, 仕様, 数量, 単位, 単価 or None, 備考, 単価セルを黄色に)
    ("電線管", "GP-22 \u3000露出\u3000溶融亜鉛メッキ", 26, "ⅿ", 4840, M, 0),
    ("電線管", "GP-28 \u3000露出\u3000溶融亜鉛メッキ", 8, "ⅿ", 6320, D, 0),
    ("電線管", "GP-42 \u3000露出\u3000溶融亜鉛メッキ", 15, "ⅿ", 10100, D, 0),
    ("電線管", "GP-54 \u3000露出\u3000溶融亜鉛メッキ", 43, "ⅿ", 13800, D, 0),
    ("電線管", "ＥP-25 \u3000隠ぺい（天井内）", 65, "ⅿ", 2910, D, 0),
    ("電線管", "ＥP-31 \u3000隠ぺい（天井内）", 25, "ⅿ", 3770, D, 0),
    ("電線管", "ＥP-39\u3000隠ぺい（天井内）", 19, "ⅿ", 4570, D, 0),
    ("電線管", "ＥP-51 \u3000隠ぺい（天井内）", 31, "ⅿ", 6250, D, 0),
    ("電線管", "CP-25 \u3000露出\u3000塗装あり", 25, "ⅿ", 4030 + 290, "積算マニュアル 管4,030+塗装290", 0),
    ("電線管", "CP-51 \u3000露出\u3000塗装あり", 4, "ⅿ", 8550 + 590, "積算マニュアル 管8,550+塗装590", 0),
    ("電線管", "HIVE16 露出", 6, "ⅿ", 2390, M, 0),
    ("金属製可とう電線管", "F-24\u3000ビニル被覆（防水）付属品共", 17, "か所", 2260, D, 0),
    ("金属製可とう電線管", "F-30\u3000ビニル被覆（防水）付属品共", 1, "か所", 2890, D, 0),
    ("金属製可とう電線管", "F-50\u3000ビニル被覆（防水）付属品共", 7, "か所", 5430, D, 0),
    ("露出ボックス", "丸型1方出\u3000C25\u3000塗装あり", 3, "個", 5040 + 50, "積算マニュアル 5,040+塗装50", 0),
    ("露出ボックス", "丸型3方出\u3000E25", 2, "個", 5220, M, 0),
    ("露出ボックス", "丸型2方出\u3000E25", 1, "個", 5130, D, 0),
    ("プルボックス", "150×150×150\u3000錆止め", 7, "個", 11800, D, 0),
    ("プルボックス", "200×200×200\u3000錆止め", 4, "個", 15900, D, 0),
    ("プルボックス", "250×250×200\u3000錆止め", 6, "個", 19000, D, 0),
]
P2 = [  # 2枚目 rows 28-49（22行）
    ("プルボックス", "150×150×150\u3000SUS WP", 2, "個", 16400, M, 0),
    ("プルボックス", "300×300×200\u3000SUS WP", 3, "個", 37200, D, 0),   # R8.10.15 Kの指示：250 → 300×300×200
    ("プルボックス", "500×500×300\u3000SUS WP", 1, "個", 79600, M, 0),
    ("電線", "EM-IE 5.5sq\u3000管内", 16, "ⅿ", 800, D, 0),
    ("ケーブル", "EM-CE 2.0sq-3C\u3000管内", 11, "ⅿ", 1040, D, 0),
    ("ケーブル", "EM-CE 3.5sq-3C\u3000管内", 610, "ⅿ", 1390, D, 0),
    ("ケーブル", "EM-CE 14sq-2C\u3000管内", 9, "ⅿ", 2300, D, 0),
    ("ケーブル", "EM-CET 38sq\u3000管内", 12, "ⅿ", 6230, D, 0),
    ("新設空調電源盤", "L-AC\u3000屋外自立型 WP・SUS", 1, "面", BAN_L, "メーカー定価×0.8", 0),
    ("新設開閉器盤", "S-AC\u3000屋外壁掛型 WP・SUS", 1, "面", BAN_S, "メーカー定価×0.8", 0),
    ("医用コンセント", "2P15A×1\u3000接地極付\u3000赤色（非常用）", 3, "個", 4600, M, 0),
    ("防水コンセント", "2P15A×1\u3000抜け止め・接地端子付", 1, "個", 4010, D, 0),
    ("接地工事", "打込式接地棒\u300014φ×1500（ED・EDELB）", 2, "か所", 10700, D, 0),
    ("接地埋設標", "接地抵抗測定含む", 2, "枚", 14100, D, 0),
    ("電動機結線費", "室内機15・室外機4・自立ユニット1", 20, "か所", 14400, D, 0),
    ("機械はつり", "φ32-φ38 200mm", 17, "か所", 12300, D, 0),
    ("機械はつり", "φ75-φ88 200mm", 2, "か所", 16100, D, 0),
    ("機械はつり", "φ150 200mm", 1, "か所", 25400, D, 0),
    ("点検調査費", "中部電気保安協会", 1, "式", 85000, "保安協会", 0),
    None, None, None,   # R8.10.15 Kの指示：既設盤改修（夜間照明開閉器盤・1L-2）は2つとも削除
]
P3 = [  # 3枚目 rows 53-71（19行）：外灯移設（E-06【外灯移設】の1～9）
    ("外灯移設工事", "既設外灯を東へ約2.5m移設", None, "", LABEL, "", 0),
    ("外灯撤去", "ポール灯\u3000取外し・再使用品保管", 1, "基", 22900, "積算マニュアル 撤去費", 0),
    ("根切り", "人力（基礎部 2.0・配管部 2.5×0.4×0.6）", 2.6, "㎥", 14600, M, 0),
    ("埋戻し", "人力", 2.2, "㎥", 11100, D, 0),
    ("建設発生土処理", "人力（場内敷ならし）", 0.4, "㎥", 8590, D, 0),
    ("砂利地業", "基礎下", 0.1, "㎥", 9670, D, 0),
    ("既設基礎掘起し", "ｺﾝｸﾘｰﾄ基礎 約400×400×600（0.23t）", 1, "箇所", KISO, "積算マニュアル 機器搬出費", 0),
    ("基礎移設据付", "既設基礎再使用（0.23t）", 1, "箇所", KISO, "積算マニュアル 機器搬入費", 0),
    ("外灯再取付", "建込・灯具取付・結線・点灯確認", 1, "基", 76300, "マニュアル労務費＋諸経費", 1),
    ("波付硬質ポリエチレン管", "FEP30\u3000地中（既設管接続・防水処理共）", 3, "ⅿ", 1400, M, 0),
    ("ケーブル", "EM-CE 2.0sq-3C\u3000FEP管内（抜替え）", 55, "ⅿ", 970, D, 0),
    ("ケーブル撤去", "EM-CE 2.0sq-3C（既設）", 55, "ⅿ", 130, "積算マニュアル 撤去費", 0),
    ("埋設標識シート", "幅150mm\u3000シングル", 3, "ⅿ", 280, M, 0),
]
SLOTS = list(range(5, 25)) + list(range(28, 50)) + list(range(53, 72))
ROWS = P1 + P2 + P3
assert len(P1) == 20 and len(P2) == 22 and len(P3) <= 19
ITEM_SLOTS = [r for r, x in zip(SLOTS, ROWS) if x is not None]
PRICED = [r for r, x in zip(SLOTS, ROWS) if x is not None and x[4] != LABEL]
ES = {}   # 明細行の標準書式（2枚目 row28）
_r28 = re.search(r'<row r="28"[ >].*?</row>', sheets[sx(E)], re.S).group(0)
for col in "BCDEFGH": ES[col] = int(re.search(r'<c r="%s28" s="(\d+)"' % col, _r28).group(1))
_put = put
def put(name, ref, *a, **k):
    col = re.match(r"[A-Z]+", ref).group(0)
    if name == E and int(ref[len(col):]) in ITEM_SLOTS and col in ES: k.setdefault("force", ES[col])
    return _put(name, ref, *a, **k)
for i, r in enumerate(SLOTS):
    x = ROWS[i] if i < len(ROWS) else None
    if x is not None and x[4] == LABEL:   # 見出し行（品名・仕様だけ）
        put(E, f"B{r}", x[0], **RED); put(E, f"C{r}", x[1], **RED)
        for col in "DEFGH": put(E, f"{col}{r}", clear=True)
        continue
    if x is not None:
        b, c, d, u, p, h, y = x
        put(E, f"B{r}", b, **RED); put(E, f"C{r}", c, **RED); put(E, f"D{r}", d, **RED); put(E, f"E{r}", u, **RED)
        if p is None:
            put(E, f"F{r}", clear=True, yellow=True)
            put(E, f"G{r}", formula=f"D{r}*F{r}", yellow=True)
        else:
            put(E, f"F{r}", p, red=True, yellow=bool(y))
            put(E, f"G{r}", formula=f"D{r}*F{r}")
        put(E, f"H{r}", h, **RED)
    else:
        for col in "BCDEFGH": put(E, f"{col}{r}", clear=True)
put(E, "G72", formula="SUM(G3:G71)")

# ================= 空調(明細) 1-3 自動制御設備工事（計装） =================
K = "空調(明細)"
CAL = "ころがし（冷媒管共巻き・天井内）"
def kv(r, b=None, c=None, d=None, u=None, p=None, h=None, yellow_price=False, na=None):
    if b is not None: put(K, f"B{r}", b, **RED)
    if na is not None:   # 該当なし・複合単価に含む
        put(K, f"C{r}", na, **RED)
        for col in "DEFG": put(K, f"{col}{r}", clear=True)
        put(K, f"H{r}", clear=True)
        return
    if c is not None: put(K, f"C{r}", c, **RED)
    if d is not None: put(K, f"D{r}", d, **RED)
    if u is not None: put(K, f"E{r}", u, **RED)
    if p is None:
        put(K, f"F{r}", clear=True, yellow=True); put(K, f"G{r}", formula=f"ROUNDDOWN(D{r}*F{r},0)", yellow=True)
        put(K, f"H{r}", "メーカー見積が必要", **RED)
    else:
        put(K, f"F{r}", p, red=True, yellow=yellow_price); put(K, f"G{r}", formula=f"ROUNDDOWN(D{r}*F{r},0)")
        put(K, f"H{r}", h or M, **RED)
# R8.10.15 Kの指示：SR-1・SR-2・調整費・付属ケーブルは輪之内中と同じ金額で（元の式＝（計装工事）シートの輪之内中の見積へのリンクを戻す）
for r, u in ((125, "U10"), (126, "U11"), (127, "U12")):
    put(K, f"F{r}", formula=f"'（計装工事） '!{u}", red=True); put(K, f"G{r}", formula=f"ROUNDDOWN(D{r}*F{r},0)")
    put(K, f"H{r}", "輪之内中の計装見積", **RED)
put(K, "F128", formula="'（計装工事） '!U13", red=True); put(K, "G128", clear=True); put(K, "H128", clear=True)
# R8.10.15 Kの指示：M-20（室外機置場）の電線管を含める。M-17（SR-1 引込）は床下配管→外壁を抜いて外で冷媒管まで立上り→そこから共巻き
#   （屋内側のプルボックスは無し）。全長が電線管内の f・e は 管内 の単価。「プリカ＆コネクター類（該当なし）」の行は 機械はつり に使う。
KAN = "管内（室外機置場）"
kv(129, c=CAL, d=1006, p=690)
kv(130, c=CAL, d=130, p=830)
kv(131, c=KAN, d=18, p=1620)
kv(132, c=CAL, d=181, p=1660)
kv(133, c=KAN, d=3, p=1040)
kv(134, c="EP-25 屋内露出（SR-2立下り）", d=4, u="m", p=3370)
kv(135, b="電線管　E63", c="EP-63 床下（SR-1引込）", d=7, u="m", p=8630, h="積算マニュアル（E60は無い規格）")
kv(136, b="溶融亜鉛メッキ電線管　G70", c="GP-70 屋外露出（SR-1立上り）", d=3, u="m", p=16700)
kv(137, b="溶融亜鉛メッキ電線管　G22", c="GP-22 屋外露出（室外機置場）", d=3, u="m", p=4840)
kv(138, b="溶融亜鉛メッキ電線管　G28", c="GP-28 屋外露出（室外機置場）", d=12, u="m", p=6320)
kv(139, b="溶融亜鉛メッキ電線管　G36", c="GP-36 屋外露出（室外機置場）", d=18, u="m", p=7640)
kv(140, na="複合単価に含む")
kv(141, b="機械はつり", c="φ100 200mm（SR-1 外壁貫通）", d=1, u="か所", p=17800)
kv(142, b="防水プルボックス300×300×200SUS", c="屋外（SR-1立上り上部）", d=1, u="個", p=37200)
kv(143, na="複合単価に含む")
kv(147, na="複合単価に含む")
for r in range(148, 158): kv(r)
put(K, "C152", "配線・配管の労務は複合単価に含む", **RED)

# ================= メモ（輪之内中のままのシート） =================
put("（計装工事） ", "A1", "※この表は輪之内中の見積のまま（大藪小の計装メーカー見積は未入手）", red=True, yellow=True, left=True)
put("E複合単価", "E1", "※輪之内中の盤見積のまま（大藪小の L-AC・S-AC は電気（明細）に記入）", red=True, yellow=True, left=True)
put("E見積比較(1)", "F1", "※輪之内中の見積のまま", red=True, yellow=True, left=True)
merge("（計装工事） ", "A1:V1"); merge("E複合単価", "E1:P1"); merge("E見積比較(1)", "F1:P1")

# ---------------- 計算結果（キャッシュ）を書き込む ----------------
# 開いたときの全再計算（fullCalcOnLoad）は、元のブックにある他ファイル（蒼設計2 等）へのリンクを Excel が
# 開こうとしてエラーが何度も出るので使わない。変えたセルと、その合計がつながるセルだけ ここで計算して値を入れる。
CHAIN = ([(E, f"G{r}") for r in PRICED] + [(E, "G72")]
         + [(K, f"F{r}") for r in (125, 126, 127, 128)]
         + [(K, f"G{r}") for r in [125, 126, 127] + list(range(129, 140)) + [141, 142] + list(range(148, 158))] + [(K, "G166")]
         + [("Ｂ電気－計", "G5"), ("Ｂ電気－計", "G20"), ("A空調－計 ", "G7"), ("A空調－計 ", "G22"),
            ("A+B+C", "G5"), ("A+B+C", "G6"), ("A+B+C", "G22")]
         + [("総括", c) for c in ("G5", "G6", "G8", "G10", "G11", "G13", "G14", "G16", "G17", "G19", "G21", "G24")])
VAL = {}
def cell_xml(name, ref):
    s = sheets[sx(name)]
    return (re.search(r'<c r="%s"(?: [^>]*?)?/>' % ref, s) or re.search(r'<c r="%s"(?: [^>]*)?(?<!/)>.*?</c>' % ref, s, re.S))
def V(name, ref):
    if (name, ref) in VAL: return VAL[(name, ref)]
    m = cell_xml(name, ref)
    if not m: return 0
    c = m.group(0); v = re.search(r"<v(?: [^>]*)?>([^<]*)</v>", c)
    if not v or ' t="s"' in c or ' t="inlineStr"' in c or ' t="str"' in c: return 0
    try: return float(v.group(1))
    except ValueError: return 0
def S(name, a, b):
    ca, ra = re.match(r"([A-Z]+)(\d+)", a).groups(); cb, rb = re.match(r"([A-Z]+)(\d+)", b).groups()
    return sum(V(name, f"{chr(c)}{r}") for c in range(ord(ca), ord(cb) + 1) for r in range(int(ra), int(rb) + 1))
def RD(x, n):
    p = 10 ** (-n); return math.trunc(x / p) * p if n < 0 else math.trunc(x * 10 ** n) / 10 ** n
import math
for name, ref in CHAIN:
    m = cell_xml(name, ref); f = re.search(r"<f>([^<]*)</f>", m.group(0))
    if not f: raise SystemExit(f"no formula {name}!{ref}")
    expr = html.unescape(f.group(1)); toks = []
    def keep(x): toks.append(x); return f"§{len(toks)-1}§"
    expr = re.sub(r"'([^']+)'!([A-Z]+\d+)", lambda mm: keep(f'V("{mm.group(1)}","{mm.group(2)}")'), expr)
    expr = re.sub(r"SUM\(([A-Z]+\d+):([A-Z]+\d+)\)", lambda mm: keep(f'S("{name}","{mm.group(1)}","{mm.group(2)}")'), expr)
    expr = re.sub(r"\b([A-Z]{1,2}\d+)\b", lambda mm: f'V("{name}","{mm.group(1)}")', expr)
    expr = expr.replace("ROUNDDOWN", "RD")
    for i, t in enumerate(toks): expr = expr.replace(f"§{i}§", t)
    val = eval(expr, {"V": V, "S": S, "RD": RD})
    VAL[(name, ref)] = val
    vs = str(int(val)) if float(val).is_integer() else repr(float(val))
    f_ = sx(name); s = sheets[f_]; m = cell_xml(name, ref); c = m.group(0)
    c2 = re.sub(r"<v(?: [^>]*)?>[^<]*</v>", "", c); c2 = re.sub(r' t="(?:str|e|b|n)"', "", c2, count=1)
    c2 = c2.replace("</c>", f"<v>{vs}</v></c>")
    sheets[f_] = s[:m.start()] + c2 + s[m.end():]
print("電気（明細）計", VAL[(E, "G72")], "自動制御 計", VAL[(K, "G166")], "総括 総合計", VAL[("総括", "G24")])
for f, sxml in sheets.items():
    for c in re.findall(r'<c r="[A-Z]+\d+"[^>]*(?<!/)>.*?</c>', sxml, re.S):
        head = c[:c.index(">")]
        v = re.search(r"<v(?: [^>]*)?>([^<]*)</v>", c)
        if v and " t=" not in head and not re.fullmatch(r"-?[\d.]+(?:E[-+]?\d+)?", v.group(1)):
            raise SystemExit(f"bad cell in {f}: {c[:160]}")
for f, s in sheets.items(): files[f] = s.encode("utf8")
st2 = st
def grow(tag, add):
    global st2
    m = re.search(r"<%s count=\"(\d+)\"([^>]*)>(.*?)</%s>" % (tag, tag), st2, re.S)
    n = int(m.group(1)) + len(add)
    st2 = st2[:m.start()] + '<%s count="%d"%s>%s%s</%s>' % (tag, n, m.group(2), m.group(3), "".join(add), tag) + st2[m.end():]
grow("fonts", new_fonts); grow("fills", new_fills); grow("cellXfs", new_xfs)
files["xl/styles.xml"] = st2.encode("utf8")
# workbook.xml（calcPr）は元のまま。calcChain は数式を変えたので削除（Excel が必要なときに作り直す）
if "xl/calcChain.xml" in files:
    del files["xl/calcChain.xml"]; order.remove("xl/calcChain.xml")
    files["xl/_rels/workbook.xml.rels"] = re.sub(r'<Relationship\b[^>]*calcChain[^>]*/>', "", rels).encode("utf8")
    ct = files["[Content_Types].xml"].decode("utf8")
    files["[Content_Types].xml"] = re.sub(r'<Override\b[^>]*calcChain[^>]*/>', "", ct).encode("utf8")
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for n in order: z.writestr(n, files[n])
print("saved", OUT, "styles +", len(new_xfs), "fonts +", len(new_fonts))
