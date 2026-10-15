# -*- coding: utf-8 -*-
"""大藪小学校 計装設備工事（No.261005）― 見積の電線管・プルボックス・コア抜きが図面のどこかを赤で記入（R8.10.15）
   使い方：python3 mark_大藪小_計装_電線管位置.py <計装図面PDF（M-16～M-20 の5枚）> <出力PDF>
   図面（客先の設計図）はリポジトリに入れない。出力は M-17・M-18 の2枚。
   R8.10.15 Kの指示：M-20（室外機置場）に載っている部分は全て冷媒管共巻き → 電線管なし（M-20 は出さない）。
   番号①～⑥ と数量は build_大藪小_計装設備.py が出力した 見積_大藪小_計装設備.json から取る。
   座標は図面PDFの線（pt）を読んだ値。1/150：1pt＝52.92mm、1/50：1pt＝17.64mm。
"""
import sys, json, pymupdf

SRC, OUT = sys.argv[1], sys.argv[2]
ROOT = "/home/user/kd-mitsumori"
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
RED = (0.88, 0, 0)
data = json.load(open(ROOT + "/見積/見積_大藪小_計装設備.json", encoding="utf-8"))
Q = {r["name"] + r["spec"]: r for r in data["rows"] if "qty" in r}
def item(key):
    r = Q[key]; return f"{r['name']} {r['spec']} {r['qty']}{r['unit']}"

doc = pymupdf.open(SRC)

def line(pg, pts, w=1.6, dashes=None):
    sh = pg.new_shape(); sh.draw_polyline(pts)
    sh.finish(color=RED, width=w, stroke_opacity=0.85, closePath=False, lineCap=1, lineJoin=1, dashes=dashes); sh.commit()
def rect(pg, r, w=1.0):
    sh = pg.new_shape(); sh.draw_rect(pymupdf.Rect(r)); sh.finish(color=RED, width=w); sh.commit()
def circle(pg, c, rad, w=1.0):
    sh = pg.new_shape(); sh.draw_circle(pymupdf.Point(c), rad); sh.finish(color=RED, width=w); sh.commit()
def text(pg, p, s, size, color=RED):
    pg.insert_text(pymupdf.Point(p), s, fontname="ipag", fontfile=FONT, fontsize=size, color=color)

def inset(pg, clip, dst, title, tags):
    """clip を拡大して dst に貼り、tags＝[(番号, 札の位置, 指す点)] を拡大図の上に描く"""
    clip, dst = pymupdf.Rect(clip), pymupdf.Rect(dst)
    sc = dst.width / clip.width
    pm = pg.get_pixmap(clip=clip, dpi=int(72 * sc * 2.5))
    pg.insert_image(dst, pixmap=pm)
    rect(pg, dst, 1.4)
    text(pg, (dst.x0, dst.y0 - 4), title, 11)
    T = lambda p: pymupdf.Point(dst.x0 + (p[0] - clip.x0) * sc, dst.y0 + (p[1] - clip.y0) * sc)
    for n, at, to in tags:
        a, b = T(at), T(to)
        sh = pg.new_shape(); sh.draw_line(a, b); sh.finish(color=RED, width=0.8); sh.commit()
        sh = pg.new_shape(); sh.draw_circle(b, 1.6); sh.finish(color=RED, fill=RED); sh.commit()
        sh = pg.new_shape(); sh.draw_circle(a, 7.5); sh.finish(color=RED, fill=(1, 1, 1), width=1.0); sh.commit()
        text(pg, (a.x - 5, a.y + 4), n, 10.5)

def legend(pg, r, lines, size=10):
    r = pymupdf.Rect(r); r.y1 = r.y0 + len(lines) * (size + 6) + 8      # 行数に合わせた高さ
    sh = pg.new_shape(); sh.draw_rect(r); sh.finish(color=RED, fill=(1, 1, 1), width=1.4); sh.commit()
    y = r.y0 + size + 5
    for i, s in enumerate(lines):
        text(pg, (r.x0 + 6, y), s, size + 1 if i == 0 else size, RED if i == 0 or s.startswith(("①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨")) else (0.25, 0, 0))
        y += size + 6

HEAD = "見積No.261005　計装設備工事　電線管・プルボックス位置（赤）"
NOTE = "数量＝図面の長さ＋立上り・立下り、×1.2（余長）を整数に切上げ"

# ---- M-17（1枚目）SR-1 引込 ----
p = doc[1]
E63 = [(1232.7, 325.3), (1232.7, 340.7), (1234.3, 343.1), (1236.0, 345.0), (1238.4, 346.4), (1289.5, 346.4)]
G70 = [(1303.6, 346.4), (1317.9, 346.4)]
line(p, E63, 1.4); line(p, G70, 1.4)
rect(p, (1288.3, 342.8, 1295.5, 350.0), 0.9); rect(p, (1297.9, 342.8, 1304.8, 350.0), 0.9)   # PB 屋内・屋外
circle(p, (1301.3, 340.3), 3.2, 0.8)                                                      # ★コア抜き
rect(p, (1196, 296, 1338, 376), 1.2); text(p, (1196, 292), "①②④⑤⑥ 左下の拡大図", 7)
inset(p, (1200, 300, 1335, 375), (110, 850, 488, 1060), "拡大図：SR-1 引込（M-17）",
      [("①", (1326, 360), (1312, 346.4)), ("②", (1255, 362), (1258, 346.4)), ("④", (1309, 333), (1301.3, 343)),
       ("⑤", (1287, 332), (1291.9, 343)), ("⑥", (1321, 318), (1303.5, 338.5))])
legend(p, (505, 850, 965, 990), [HEAD,
    "① " + item("溶融亜鉛メッキ電線管　G70GP-70 屋外露出（SR-1引込）"),
    "② " + item("電線管　E63EP-63 屋内露出（SR-1引込）"),
    "④ " + item("防水プルボックス300×300×200SUS屋外側（SR-1引込）"),
    "⑤ " + item("プルボックス250×250×200錆止め（SR-1引込 屋内側）"),
    "⑥ " + item("機械はつりφ100 200mm（SR-1引込）") + "（★印）",
    "　中は a×2・b×3・c×3。図面凡例の「E60」は無い規格のため E63 で計上",
    "　M-20（室外機置場）は全て冷媒管共巻き（電線管なし）",
    NOTE], 8.5)

# ---- M-18（2枚目）SR-2 立下り ----
p = doc[2]
line(p, [(517.6, 579.0), (517.6, 586.4)], 1.6)
circle(p, (522.3, 585.2), 8.5, 0.9)
inset(p, (478, 548, 558, 608), (700, 785, 940, 965), "拡大図：SR-2（M-18）", [("③", (545, 600), (517.6, 583))])
legend(p, (960, 785, 1400, 880), [HEAD,
    "③ " + item("電線管　E25EP-25 屋内露出（SR-2立下り）"),
    "　天井内は転がし（電線管なし）", NOTE], 8.5)

doc.select([1, 2])
doc.save(OUT, garbage=3, deflate=True)
print("saved", OUT)
