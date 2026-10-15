# -*- coding: utf-8 -*-
"""大藪小学校屋内運動場空調設備設置工事 内訳（設計書 xlsx）に 電気・計装を記入（R8.10.15）
   使い方：python3 fill_大藪小_内訳_電気計装.py <大藪小の内訳.xlsx> <出力.xlsx>
   ・輪之内中の内訳の書き方（品名・仕様・単位・備考「積算ﾏﾆｱﾙ」）に合わせる
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

def style(s, red=False, yellow=False):
    key = (s, red, yellow)
    if key in xf_cache: return xf_cache[key]
    x = xfs[s]
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

def put(name, ref, value=None, formula=None, red=False, yellow=False, clear=False, base=None, force=None):
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
    sid = style(old_s, red, yellow) if (red or yellow) else old_s
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

RED, YEL = dict(red=True), dict(red=True, yellow=True)
M = "積算ﾏﾆｱﾙ"; D = "　　〃"

# ================= 電気（明細） =================
E = "電気（明細）"
ROWS = [  # (品名, 仕様, 数量, 単位, 単価 or None, 備考, 単価セルを黄色に)
    ("電線管", "GP-22 　露出　溶融亜鉛メッキ", 26, "ⅿ", 4840, M, 0),
    ("電線管", "GP-28 　露出　溶融亜鉛メッキ", 8, "ⅿ", 6320, D, 0),
    ("電線管", "GP-42 　露出　溶融亜鉛メッキ", 15, "ⅿ", 10100, D, 0),
    ("電線管", "GP-54 　露出　溶融亜鉛メッキ", 43, "ⅿ", 13800, D, 0),
    ("電線管", "ＥP-25 　隠ぺい（天井内）", 65, "ⅿ", 2910, D, 0),
    ("電線管", "ＥP-31 　隠ぺい（天井内）", 25, "ⅿ", 3770, D, 0),
    ("電線管", "ＥP-39　隠ぺい（天井内）", 19, "ⅿ", 4570, D, 0),
    ("電線管", "ＥP-51 　隠ぺい（天井内）", 31, "ⅿ", 6250, D, 0),
    ("電線管", "CP-25 　露出　塗装あり", 25, "ⅿ", 4030 + 290, "積算ﾏﾆｱﾙ 管4,030+塗装290", 0),
    ("電線管", "CP-51 　露出　塗装あり", 4, "ⅿ", 8550 + 590, "積算ﾏﾆｱﾙ 管8,550+塗装590", 0),
    ("電線管", "HIVE16 露出", 6, "ⅿ", 2390, M, 0),
    ("波付硬質ポリエチレン管", "FEP30　地中（外灯移設）", 3, "ⅿ", 1400, D, 0),
    ("金属製可とう電線管", "F-24　ビニル被覆（防水）付属品共", 17, "か所", 2260, D, 0),
    ("金属製可とう電線管", "F-30　ビニル被覆（防水）付属品共", 1, "か所", 2890, D, 0),
    ("金属製可とう電線管", "F-50　ビニル被覆（防水）付属品共", 7, "か所", 5430, D, 0),
    ("露出ボックス", "丸型1方出　C25　塗装あり", 3, "個", 5040 + 50, "積算ﾏﾆｱﾙ 5,040+塗装50", 0),
    ("露出ボックス", "丸型3方出　E25", 2, "個", 5220, M, 0),
    ("露出ボックス", "丸型2方出　E25", 1, "個", 5130, D, 0),
    ("プルボックス", "150×150×150　錆止め", 7, "個", 11800, D, 0),
    ("プルボックス", "200×200×200　錆止め", 4, "個", 15900, D, 0),
    # ---- 2枚目 ----
    ("プルボックス", "250×250×250　錆止め", 6, "個", 19000, "ﾏﾆｱﾙに無し 250×250×200で計上", 1),
    ("プルボックス", "150×150×150　SUS WP", 2, "個", 16400, M, 0),
    ("プルボックス", "250×250×250　SUS WP", 3, "個", 45100, "ﾏﾆｱﾙに無し 300×300×300で計上", 1),
    ("プルボックス", "500×500×300　SUS WP", 1, "個", 79600, M, 0),
    ("電線", "EM-IE 5.5sq　管内", 16, "ⅿ", 800, D, 0),
    ("ケーブル", "EM-CE 2.0sq-3C　管内", 11, "ⅿ", 1040, D, 0),
    ("ケーブル", "EM-CE 2.0sq-3C　FEP管内（外灯抜替え）", 55, "ⅿ", 970, D, 0),
    ("ケーブル", "EM-CE 3.5sq-3C　管内", 610, "ⅿ", 1390, D, 0),
    ("ケーブル", "EM-CE 14sq-2C　管内", 9, "ⅿ", 2300, D, 0),
    ("ケーブル", "EM-CET 38sq　管内", 12, "ⅿ", 6230, D, 0),
    ("新設空調電源盤", "L-AC　屋外自立型 WP・SUS", 1, "面", None, "メーカー見積が必要", 1),
    ("新設開閉器盤", "S-AC　屋外壁掛型 WP・SUS", 1, "面", None, "メーカー見積が必要", 1),
    ("既設盤改修", "夜間照明開閉器盤（屋外型SUS製）", 1, "式", None, "ﾏﾆｱﾙに無し", 1),
    ("既設盤改修", "1L-2　予備回路に空調制御盤SR-1接続", 1, "式", None, "ﾏﾆｱﾙに無し", 1),
    ("医用コンセント", "2P15A×1　接地極付　赤色（非常用）", 3, "個", 4600, M, 0),
    ("防水コンセント", "2P15A×1　抜け止め・接地端子付", 1, "個", 4010, D, 0),
    ("接地工事", "打込式接地棒　14φ×1500（ED・EDELB）", 2, "か所", 10700, D, 0),
    ("接地埋設標", "接地抵抗測定含む", 2, "枚", 14100, D, 0),
    ("電動機結線費", "室内機15・室外機4・自立ユニット1", 20, "か所", 14400, D, 0),
    ("機械はつり", "φ32-φ38 200mm", 17, "か所", 12300, D, 0),
    ("機械はつり", "φ75-φ88 200mm", 2, "か所", 16100, D, 0),
    ("機械はつり", "φ150 200mm", 1, "か所", 25400, D, 0),
    # ---- 3枚目 ----
    ("外灯移設工事", "既設外灯撤去・基礎移設・再取付・掘削埋戻し", 1, "式", None, "ﾏﾆｱﾙに無し", 1),
    ("点検調査費", "中部電気保安協会", 1, "式", None, "ﾏﾆｱﾙに無し", 1),
]
SLOTS = list(range(5, 25)) + list(range(28, 50)) + list(range(53, 72))
assert len(ROWS) <= len(SLOTS)
ES = {}   # 明細行の標準書式（2枚目 row28）
_r28 = re.search(r'<row r="28"[ >].*?</row>', sheets[sx(E)], re.S).group(0)
for col in "BCDEFGH": ES[col] = int(re.search(r'<c r="%s28" s="(\d+)"' % col, _r28).group(1))
_put = put
def put(name, ref, *a, **k):
    col = re.match(r"[A-Z]+", ref).group(0)
    if name == E and int(ref[len(col):]) in SLOTS[:len(ROWS)] and col in ES: k.setdefault("force", ES[col])
    return _put(name, ref, *a, **k)
for i, r in enumerate(SLOTS):
    if i < len(ROWS):
        b, c, d, u, p, h, y = ROWS[i]
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
        put(K, f"H{r}", "見積が必要（輪之内中はメーカー見積）", **RED)
    else:
        put(K, f"F{r}", p, red=True, yellow=yellow_price); put(K, f"G{r}", formula=f"ROUNDDOWN(D{r}*F{r},0)")
        put(K, f"H{r}", h or M, **RED)
kv(125); kv(126); kv(127)
put(K, "F128", clear=True, yellow=True); put(K, "G128", clear=True, yellow=True)
kv(129, c=CAL, d=1006, p=690)
kv(130, c=CAL, d=130, p=830)
kv(131, c=CAL, d=18, p=1440)
kv(132, c=CAL, d=181, p=1660)
kv(133, c=CAL, d=3, p=920)
kv(134, c="EP-25 屋内露出（SR-2立下り）", d=4, u="m", p=3370)
kv(135, b="電線管　E63", c="EP-63 屋内露出（SR-1引込）", d=8, u="m", p=9960, h="積算ﾏﾆｱﾙ（図面のE60は無い規格）")
kv(136, b="溶融亜鉛メッキ電線管　G70", c="GP-70 屋外露出（SR-1引込）", d=3, u="m", p=16700)
kv(137, b="プルボックス250×250×250", c="錆止め（SR-1引込 屋内側）", d=1, u="個", p=19000, h="ﾏﾆｱﾙに無し 250×250×200で計上", yellow_price=True)
kv(138, b="機械はつり", c="φ100 200mm（SR-1引込）", d=1, u="か所", p=17800)
for col in "BCDEFGH": put(K, f"{col}139", clear=True)
kv(140, na="複合単価に含む")
kv(141, na="該当なし")
kv(142, c="屋外側（SR-1引込）", d=1, p=45100, h="ﾏﾆｱﾙに無し 300×300×300で計上", yellow_price=True)
kv(143, na="複合単価に含む")
kv(147, na="複合単価に含む")
for r in range(148, 158): kv(r)
put(K, "C152", "配線・配管の労務は複合単価に含む", **RED)

# ================= メモ（輪之内中のままのシート） =================
put("（計装工事） ", "A1", "※大藪小の計装メーカー見積は未入手。この表は輪之内中の見積のまま（空調(明細) 1-3 はケーブル・電線管を積算ﾏﾆｱﾙで記入、盤・調整等は黄色）", red=True, yellow=True)
put("E複合単価", "E1", "※輪之内中の盤見積のまま。大藪小の L-AC・S-AC は見積未入手（電気（明細）は黄色）", red=True, yellow=True)
put("E見積比較(1)", "F1", "※輪之内中の見積のまま（大藪小は未入手）", red=True, yellow=True)

# ---------------- 計算結果（キャッシュ）を書き込む ----------------
# 開いたときの全再計算（fullCalcOnLoad）は、元のブックにある他ファイル（蒼設計2 等）へのリンクを Excel が
# 開こうとしてエラーが何度も出るので使わない。変えたセルと、その合計がつながるセルだけ ここで計算して値を入れる。
CHAIN = ([(E, f"G{r}") for r in SLOTS[:len(ROWS)]] + [(E, "G72")]
         + [(K, f"G{r}") for r in [125, 126, 127] + list(range(129, 139)) + [142] + list(range(148, 158))] + [(K, "G166")]
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
