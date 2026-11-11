# -*- coding: utf-8 -*-
"""材料リスト（電材屋さんへの見積依頼用・機器類のみ）：令和８年度 揖斐川深谷護岸整備工事 樋管上屋 電気設備工事
   R8.11.11 Kの指示：シンプルに 現場名・材料・数量だけ。数量・仕様は数量書／別紙明細／図面49（姿図・分電盤結線図）から。
"""
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

SITE = "令和８年度　揖斐川深谷護岸整備工事（樋管上屋　電気設備工事）"
ITEMS = [  # (品名, 仕様, 数量, 単位)
    ("電灯分電盤 L-1", "屋内鋼板製壁掛型　1φ2W 100V 60Hz　主幹 MCCB 2P 50AF/30AT　分岐 ELCB 2P 50AF/20AT×6（うち予備1）　PL付（図面49 結線図）", 1, "面"),
    ("LED照明器具 A402", "40形 反射笠付　LED 5100lm　100V　線ぴ取付", 10, "台"),
    ("LED照明器具 B402", "40形 反射笠付　非常用（電池内蔵）　LED 5100lm　100V　線ぴ取付", 2, "台"),
    ("LED照明器具 C201", "ウォールライト 防水形　LED 1020lm　100V（LBF3MP/RP-2-06 相当）", 1, "台"),
    ("LED照明器具 D201", "投光器 壁掛形　LED 22800lm　100V（LPJ1W-180 相当）", 2, "台"),
    ("タンブラスイッチ", "1P15A×2　金属プレート付", 1, "個"),
    ("熱線式自動スイッチ用センサー", "壁付　防水形", 1, "個"),
    ("防雨入線カバー", "", 2, "個"),
    ("コンセント", "2P15A×1　接地極付　125V　金属プレート付", 1, "個"),
    ("コンセント", "2P15A×2　接地極付 一体形　125V　金属プレート付", 2, "個"),
    ("プルボックス", "SS 300×300×200　錆止め・塗装有", 3, "個"),
    ("接地端子（ET）", "プルボックス用", 3, "個"),
]

wb = openpyxl.Workbook(); ws = wb.active; ws.title = "材料リスト"
F = "ＭＳ Ｐゴシック"
thin = Side(style="thin", color="000000"); box = Border(left=thin, right=thin, top=thin, bottom=thin)
ws.page_setup.paperSize = ws.PAPERSIZE_A4; ws.page_setup.orientation = "portrait"
ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
for col, w in zip("ABCDE", (5, 30, 62, 7, 6)): ws.column_dimensions[col].width = w

def put(ref, v, size=10, bold=False, al="left", border=False, fill=False, wrap=False):
    c = ws[ref]; c.value = v; c.font = Font(name=F, size=size, bold=bold)
    c.alignment = Alignment(horizontal=al, vertical="center", wrap_text=wrap)
    if border: c.border = box
    if fill: c.fill = PatternFill("solid", fgColor="EFEFEF")

ws.merge_cells("A1:E1"); put("A1", "材料リスト（見積依頼）", 16, True, "center"); ws.row_dimensions[1].height = 26
ws.merge_cells("A3:E3"); put("A3", "現場名：" + SITE, 11, True)
for c, h in zip("ABCDE", ("No.", "品名", "仕様", "数量", "単位")): put(f"{c}5", h, 10, True, "center", True, True)
r = 6
for i, (nm, sp, q, u) in enumerate(ITEMS, 1):
    put(f"A{r}", i, al="center", border=True); put(f"B{r}", nm, border=True)
    put(f"C{r}", sp, border=True, wrap=True); put(f"D{r}", q, al="right", border=True); put(f"E{r}", u, al="center", border=True)
    ws.row_dimensions[r].height = 30 if len(sp) > 40 else 20
    r += 1
root = "/home/user/kd-mitsumori/見積/"
wb.save(root + "材料リスト_揖斐川深谷護岸_樋管上屋_機器.xlsx")
for i, (nm, sp, q, u) in enumerate(ITEMS, 1): print(i, nm, sp, q, u)
