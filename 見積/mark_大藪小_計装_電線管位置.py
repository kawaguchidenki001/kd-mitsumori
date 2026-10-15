# -*- coding: utf-8 -*-
"""大藪小学校 計装設備工事（No.261005）― 見積の電線管・プルボックス・コア抜きが図面のどこかを赤で記入（R8.10.15）
   使い方：python3 mark_大藪小_計装_電線管位置.py <計装図面PDF（M-16～M-20 の5枚）> <出力PDF>
   図面（客先の設計図）はリポジトリに入れない。出力は M-17・M-18・M-20 の3枚。
   R8.10.15 Kの指示：M-20（室外機置場）の電線管を含める（最初の位置図に戻す）。M-17（SR-1 引込）は床下配管：
   SR-1 の下から床下を通って外壁を抜き、外で冷媒管まで立ち上げ、冷媒管に飛びついたらそこからは共巻き（屋内側PBは無し）。
   番号①～⑧（見積・内訳の電線管・ボックスの順）と数量は build_大藪小_計装設備.py が出力した 見積_大藪小_計装設備.json から取る。
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
K_E25 = "電線管　E25EP-25 屋内露出（SR-2立下り）"
K_E63 = "電線管　E63EP-63 床下（SR-1引込）"
K_G70 = "溶融亜鉛メッキ電線管　G70GP-70 屋外露出（SR-1立上り）"
K_G22 = "溶融亜鉛メッキ電線管　G22GP-22 屋外露出（室外機置場）"
K_G28 = "溶融亜鉛メッキ電線管　G28GP-28 屋外露出（室外機置場）"
K_G36 = "溶融亜鉛メッキ電線管　G36GP-36 屋外露出（室外機置場）"
K_HT = "機械はつりφ100 200mm（SR-1 外壁貫通）"
K_PB = "防水プルボックス300×300×200SUS屋外（SR-1立上り上部）"

# ---- M-17（1枚目）SR-1 引込：SR-1 の下→床下（破線）→外壁を抜く★→外で冷媒管まで立上り→PB→冷媒管共巻き ----
p = doc[1]
WALL, PIPE, Y = 1296.7, 1317.9, 346.4
E63 = [(1232.7, 325.3), (1232.7, 340.7), (1234.3, 343.1), (1236.0, 345.0), (1238.4, Y), (WALL, Y)]
line(p, E63, 1.4, "[4 2] 0")                                     # ② E63 床下（破線）
line(p, [(WALL, Y), (PIPE, Y)], 1.4)                              # ③ G70 外へ抜いた後～立上り
circle(p, (PIPE, Y), 2.2, 0.9); circle(p, (PIPE, Y), 4.0, 0.9)   #    立上り
rect(p, (PIPE - 4.6, Y - 4.6 - 9, PIPE + 4.6, Y + 4.6 - 9), 0.9)   # ⑧ PB（立上り上部）
circle(p, (1301.3, 340.3), 3.2, 0.8)                              # ⑦ ★機械はつり（外壁）
rect(p, (1196, 296, 1338, 376), 1.2); text(p, (1196, 292), "②③⑦⑧ 左下の拡大図", 7)
inset(p, (1200, 300, 1335, 375), (110, 850, 488, 1060), "拡大図：SR-1 引込（M-17）床下配管",
      [("②", (1255, 362), (1258, Y)), ("③", (1309, 362), (1309, Y)), ("⑦", (1290, 326), (1300.5, 338.5)),
       ("⑧", (1330, 322), (PIPE + 3, Y - 12))])
legend(p, (505, 850, 965, 990), [HEAD,
    "② " + item(K_E63) + "（SR-1の下から床下を通って外壁まで・破線）",
    "③ " + item(K_G70) + "（外壁を抜いた後、冷媒管まで立上り）",
    "⑦ " + item(K_HT) + "（★印 床下から外へ）",
    "⑧ " + item(K_PB),
    "　⑧から先は冷媒管に共巻き。床下配管なので屋内側のプルボックスは無し",
    "　中は a×2・b×3・c×3。図面凡例の「E60」は無い規格のため E63 で計上",
    NOTE], 8.5)

# ---- M-18（2枚目）SR-2 立下り ----
p = doc[2]
line(p, [(517.6, 579.0), (517.6, 586.4)], 1.6)
circle(p, (522.3, 585.2), 8.5, 0.9)
inset(p, (478, 548, 558, 608), (700, 785, 940, 965), "拡大図：SR-2（M-18）", [("①", (545, 600), (517.6, 583))])
legend(p, (960, 785, 1400, 880), [HEAD,
    "① " + item(K_E25),
    "　天井内は転がし（電線管なし）", NOTE], 8.5)

# ---- M-20（3枚目）室外機置場（最初の位置図と同じ線）----
p = doc[4]
Y28, YD = 527.8, 555.0
line(p, [(969.3, Y28), (513.5, Y28), (513.5, YD)], 1.5)                      # ⑤ G28 a・d・h
for x in (643.1, 742.7, 842.6): line(p, [(x, Y28), (x, YD)], 1.5)
G36 = [[(552.7, YD), (552.7, 532.0), (837.1, 532.0), (837.1, YD)],           # ⑥ G36 f・g 自立ユニット→GHP-1
       [(552.7, 536.1), (737.2, 536.1), (737.2, YD)],                        #   →GHP-2
       [(552.7, 540.4), (637.4, 540.4), (637.4, YD)],                        #   →GHP-3
       [(552.7, 540.4), (516.1, 540.4), (516.1, YD)]]                        #   →GHP-4
for g in G36: line(p, g, 1.3, "[3 1.2] 0")
for g in ([(856.6, 557.5), (878.6, 557.5), (878.6, 589.9), (866.9, 589.9)],   # ④ G22 d・e GHP-1→遠隔監視アダプタ
          [(856.6, 562.9), (873.2, 562.9), (873.2, 584.5), (866.9, 584.5)]):
    line(p, g, 1.5)
inset(p, (505, 500, 985, 600), (100, 692, 868, 844), "拡大図：室外機置場（M-20）",
      [("⑤", (940, 512), (930, Y28)), ("⑥", (790, 547), (790, 532.0)), ("⑥", (690, 547), (690, 536.1)),
       ("④", (897, 597), (878.6, 589.9))])
legend(p, (100, 870, 620, 1010), [HEAD,
    "④ " + item(K_G22) + "（d・e GHP-1～遠隔監視アダプタ）",
    "⑤ " + item(K_G28) + "（a・d・h 置場入口～GHP-1～4）",
    "⑥ " + item(K_G36) + "（f・g 自立ユニット～GHP-1～4、赤破線）",
    "　建物～置場の c・a・h は冷媒管共巻き（電線管なし）", NOTE], 8.5)

doc.select([1, 2, 4])
doc.save(OUT, garbage=3, deflate=True)
print("saved", OUT)
