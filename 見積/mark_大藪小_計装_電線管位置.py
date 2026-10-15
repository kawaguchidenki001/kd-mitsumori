# -*- coding: utf-8 -*-
"""大藪小学校 計装設備工事（No.261005）― 見積の電線管・プルボックス・コア抜きが図面のどこかを赤で記入（R8.10.15）
   使い方：python3 mark_大藪小_計装_電線管位置.py <計装図面PDF（M-16～M-20 の5枚）> <出力PDF>
   図面（客先の設計図）はリポジトリに入れない。出力は M-17・M-18・M-20 の3枚。
   番号①～⑨ と数量は build_大藪小_計装設備.py が出力した 見積_大藪小_計装設備.json から取る。
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
rect(p, (1196, 296, 1338, 376), 1.2); text(p, (1196, 292), "④⑤⑦⑧⑨ 左下の拡大図", 7)
inset(p, (1200, 300, 1335, 375), (110, 850, 488, 1060), "拡大図：SR-1 引込（M-17）",
      [("④", (1326, 360), (1312, 346.4)), ("⑤", (1255, 362), (1258, 346.4)), ("⑦", (1309, 333), (1301.3, 343)),
       ("⑧", (1287, 332), (1291.9, 343)), ("⑨", (1321, 318), (1303.5, 338.5))])
legend(p, (505, 850, 965, 990), [HEAD,
    "④ " + item("厚鋼電線管Ｇ７０ 屋外露出") + "（屋外PB～冷媒管共巻き）",
    "⑤ " + item("ねじなし電線管Ｅ６３ 屋内露出") + "（屋内PB～SR-1）",
    "⑦ " + item("プルボックス２５０×２５０×２５０ ＳＵＳ製ＷＰ") + "（屋外側）",
    "⑧ " + item("プルボックス２５０×２５０×２５０ 錆止塗装") + "（屋内側）",
    "⑨ " + item("コア抜きφ１００程度") + "（★印）",
    "　中は a×2・b×3・c×3。図面凡例の「E60」は無い規格のため E63 で計上",
    NOTE], 8.5)

# ---- M-18（2枚目）SR-2 立下り ----
p = doc[2]
line(p, [(517.6, 579.0), (517.6, 586.4)], 1.6)
circle(p, (522.3, 585.2), 8.5, 0.9)
inset(p, (478, 548, 558, 608), (700, 785, 940, 965), "拡大図：SR-2（M-18）", [("⑥", (545, 600), (517.6, 583))])
legend(p, (960, 785, 1400, 880), [HEAD,
    "⑥ " + item("ねじなし電線管Ｅ２５ 屋内露出") + "（SR-2 立下り b）",
    "　天井内は転がし（電線管なし）", NOTE], 8.5)

# ---- M-20（4枚目）室外機置場 ----
p = doc[4]
Y28, YD = 527.8, 555.0
line(p, [(969.3, Y28), (513.5, Y28), (513.5, YD)], 1.5)                      # ① G28 a・d・h
for x in (643.1, 742.7, 842.6): line(p, [(x, Y28), (x, YD)], 1.5)
G36 = [[(552.7, YD), (552.7, 532.0), (837.1, 532.0), (837.1, YD)],           # ② G36 f・g 自立ユニット→GHP-1
       [(552.7, 536.1), (737.2, 536.1), (737.2, YD)],                        #   →GHP-2
       [(552.7, 540.4), (637.4, 540.4), (637.4, YD)],                        #   →GHP-3
       [(552.7, 540.4), (516.1, 540.4), (516.1, YD)]]                        #   →GHP-4
for g in G36: line(p, g, 1.3, "[3 1.2] 0")
for g in ([(856.6, 557.5), (878.6, 557.5), (878.6, 589.9), (866.9, 589.9)],   # ③ G22 d・e GHP-1→遠隔監視アダプタ
          [(856.6, 562.9), (873.2, 562.9), (873.2, 584.5), (866.9, 584.5)]):
    line(p, g, 1.5)
inset(p, (505, 500, 985, 600), (100, 692, 868, 844), "拡大図：室外機置場（M-20）",
      [("①", (940, 512), (930, Y28)), ("②", (790, 547), (790, 532.0)), ("②", (690, 547), (690, 536.1)),
       ("③", (897, 597), (878.6, 589.9))])
legend(p, (100, 870, 620, 1010), [HEAD,
    "① " + item("厚鋼電線管Ｇ２８ 屋外露出") + "（a・d・h 置場入口～GHP-1～4）",
    "② " + item("厚鋼電線管Ｇ３６ 屋外露出") + "（f・g 自立ユニット～GHP-1～4、赤破線）",
    "③ " + item("厚鋼電線管Ｇ２２ 屋外露出") + "（d・e GHP-1～遠隔監視アダプタ）",
    "　建物～置場の c・a・h は冷媒管共巻き（電線管なし）", NOTE], 8.5)

doc.select([1, 2, 4])
doc.save(OUT, garbage=3, deflate=True)
print("saved", OUT)
