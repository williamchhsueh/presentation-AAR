#!/usr/bin/env python3
"""
build_deck.py — 從零生成 AAR 簡報 21 張投影片。

內容權威：PLAN_v2.md   視覺權威：vis_style.md
輸出：ppt/AAR_Paper_Sharing_v3.pptx（13.333" x 7.5"）
執行：poetry run python code/build_deck.py
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR  = os.path.join(BASE_DIR, "figure")
OUT      = os.path.join(BASE_DIR, "ppt", "AAR_Paper_Sharing_v3.pptx")

# ── Canvas (vis_style §3：新建 deck) ───────────────────────────────────
CW_IN, CH_IN = 13.333, 7.5

# ── Color tokens (vis_style §13.1) ─────────────────────────────────────
BG_BASE      = RGBColor(0x08, 0x10, 0x10)
BG_DOSSIER   = RGBColor(0x00, 0x08, 0x10)
BG_PURE      = RGBColor(0x0A, 0x0A, 0x0A)
PANEL        = RGBColor(0x10, 0x18, 0x18)
PANEL_2      = RGBColor(0x18, 0x18, 0x20)
PANEL_BAD    = RGBColor(0x1A, 0x0E, 0x10)
PANEL_GOOD   = RGBColor(0x0E, 0x1A, 0x12)
STROKE       = RGBColor(0x28, 0x30, 0x38)
STROKE_HUD   = RGBColor(0x3A, 0x4A, 0x55)
DIVIDER      = RGBColor(0x20, 0x28, 0x30)
TEXT_PRIM    = RGBColor(0xF8, 0xF8, 0xF8)
TEXT_SEC     = RGBColor(0xB8, 0xC0, 0xC4)
TEXT_MUTED   = RGBColor(0x7A, 0x84, 0x88)
TEXT_ON_ACC  = RGBColor(0x08, 0x10, 0x10)
ACC_GOOD       = RGBColor(0x7C, 0xE3, 0x8B)
ACC_GOOD_GLOW  = RGBColor(0xA0, 0xF0, 0xB0)
ACC_WARN       = RGBColor(0xF0, 0xA0, 0x30)
ACC_BAD        = RGBColor(0xC7, 0x38, 0x38)
ACC_BAD_DIM    = RGBColor(0x60, 0x18, 0x18)
ACC_DATA_BLUE  = RGBColor(0x30, 0x60, 0xA0)
ROLE_PM   = ACC_GOOD
ROLE_DS   = RGBColor(0xE3, 0x6A, 0xAE)
ROLE_SWE  = RGBColor(0xB8, 0x9A, 0xE6)
ROLE_NOTE = ACC_WARN
ROLE_REF  = RGBColor(0x9A, 0xB6, 0xE6)

# ── Typography (vis_style §5) ──────────────────────────────────────────
LATIN, CJK, MONO = "Inter", "Noto Sans CJK TC", "JetBrains Mono"
T_MEGA, T_MEGA_SM, T_QUOTE = 96, 72, 48
T_H1, T_H2, T_BODY, T_BODY_SM, T_CAPTION = 36, 22, 14, 12, 10
T_BADGE, T_STRIP = 11, 9

COPYRIGHT = "Automated Alignment Researcher (AAR) · Anthropic Research 2026"

# ── Presentation ───────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(CW_IN)
prs.slide_height = Inches(CH_IN)
BLANK = prs.slide_layouts[6]

# ── Geometry: 0–100 % → Inches ─────────────────────────────────────────
def X(pct):  return Inches(CW_IN * pct / 100.0)
def Y(pct):  return Inches(CH_IN * pct / 100.0)
def pt_w(p): return Pt(p).inches / CW_IN * 100.0     # pt → % of width
def pt_h(p): return Pt(p).inches / CH_IN * 100.0     # pt → % of height

# ── Low-level helpers ──────────────────────────────────────────────────
def set_bg(slide, rgb):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb

def add_slide(bg=BG_BASE):
    sl = prs.slides.add_slide(BLANK)
    set_bg(sl, bg)
    return sl

def set_notes(slide, txt):
    slide.notes_slide.notes_text_frame.text = txt

def _set_ea_font(run, ea_face):
    """python-pptx 只設 latin run；中文須補 <a:ea> 才會套 Noto Sans CJK。"""
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {})
        latin = rPr.find(qn('a:latin'))
        if latin is not None:
            latin.addnext(ea)
        else:
            rPr.append(ea)
    ea.set('typeface', ea_face)

def _fill_alpha(shape, alpha_pct):
    """在 solid fill 上加透明度（alpha_pct = 0–100，數字越小越透明）。"""
    spPr = shape._element.spPr
    sf = spPr.find(qn('a:solidFill'))
    if sf is None:
        return
    srgb = sf.find(qn('a:srgbClr'))
    if srgb is None:
        return
    srgb.append(srgb.makeelement(qn('a:alpha'), {'val': str(int(alpha_pct * 1000))}))

def _line_dash(shape, val='dash'):
    ln = shape._element.spPr.find(qn('a:ln'))
    if ln is not None:
        ln.append(ln.makeelement(qn('a:prstDash'), {'val': val}))

def _add_runs(p, content, size, bold, italic, color, font):
    """content = str | [(text, override_dict), ...]"""
    specs = content if isinstance(content, list) else [(content, {})]
    for txt, ov in specs:
        r = p.add_run()
        r.text = txt
        f = r.font
        f.size   = Pt(ov.get('size', size))
        f.bold   = ov.get('bold', bold)
        f.italic = ov.get('italic', italic)
        f.color.rgb = ov.get('color', color)
        fam = ov.get('font', font)
        f.name = MONO if fam == 'mono' else LATIN
        _set_ea_font(r, CJK)

def text(slide, content, x, y, w, h, size=T_BODY, bold=False, italic=False,
         color=TEXT_PRIM, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         font='sans', wrap=True, line_spacing=None):
    box = slide.shapes.add_textbox(X(x), Y(y), X(w), Y(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Pt(0)
    p = tf.paragraphs[0]
    p.alignment = align
    if line_spacing:
        p.line_spacing = line_spacing
    _add_runs(p, content, size, bold, italic, color, font)
    return box

def text_lines(slide, lines, x, y, w, h, align=PP_ALIGN.LEFT,
               anchor=MSO_ANCHOR.TOP, wrap=True):
    """lines = [(content, {size,bold,italic,color,align,font,space_before,line_spacing}), ...]"""
    box = slide.shapes.add_textbox(X(x), Y(y), X(w), Y(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Pt(0)
    for i, (content, fmt) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = fmt.get('align', align)
        if fmt.get('space_before') is not None:
            p.space_before = Pt(fmt['space_before'])
        if fmt.get('line_spacing'):
            p.line_spacing = fmt['line_spacing']
        _add_runs(p, content, fmt.get('size', T_BODY), fmt.get('bold', False),
                  fmt.get('italic', False), fmt.get('color', TEXT_PRIM),
                  fmt.get('font', 'sans'))
    return box

def rect(slide, x, y, w, h, fill=None, line_color=None, line_w=1.0,
         rounded=False, radius=0.05, alpha=None, dash=None):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        X(x), Y(y), X(w), Y(h))
    if rounded:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
        if alpha is not None:
            _fill_alpha(shp, alpha)
    if line_color is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line_color
        shp.line.width = Pt(line_w)
        if dash:
            _line_dash(shp, dash)
    shp.shadow.inherit = False
    return shp

def hline(slide, x, y, w, color=DIVIDER, weight_pt=1.0):
    return rect(slide, x, y, w, pt_h(weight_pt), fill=color)

# ── Components (vis_style §6) ──────────────────────────────────────────
def tick_corners(slide, x, y, w, h, color=STROKE_HUD, size_pt=7, weight_pt=1.0):
    sw, sh = pt_w(size_pt), pt_h(size_pt)
    tw, th = pt_w(weight_pt), pt_h(weight_pt)
    for cx, cy, sx, sy in ((x, y, 1, 1), (x + w, y, -1, 1),
                           (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        hx = cx if sx > 0 else cx - sw
        hy = cy if sy > 0 else cy - th
        rect(slide, hx, hy, sw, th, fill=color)
        vx = cx if sx > 0 else cx - tw
        vy = cy if sy > 0 else cy - sh
        rect(slide, vx, vy, tw, sh, fill=color)

PAD_X, PAD_Y = pt_w(18), pt_h(14)
STRIPE_H = pt_h(4.5)

def panel(slide, x, y, w, h, fill=PANEL, stripe=None, border=STROKE, tick=True):
    """畫一張 c-card 外框，回傳內容區 (ix, iy, iw, ih)（%）。"""
    rect(slide, x, y, w, h, fill=fill, line_color=border, line_w=1.0,
         rounded=True, radius=0.045)
    if stripe is not None:
        rect(slide, x, y, w, STRIPE_H, fill=stripe)
    if tick:
        tick_corners(slide, x, y, w, h)
    top = STRIPE_H if stripe is not None else 0
    return (x + PAD_X, y + top + PAD_Y, w - 2 * PAD_X, h - top - 2 * PAD_Y)

def card(slide, x, y, w, h, title=None, body=None, stripe=ACC_GOOD, fill=PANEL,
         title_color=TEXT_PRIM, body_color=TEXT_SEC, title_size=T_H2,
         body_size=T_BODY, tick=True):
    ix, iy, iw, ih = panel(slide, x, y, w, h, fill=fill, stripe=stripe, tick=tick)
    cy = iy
    if title is not None:
        text(slide, title, ix, cy, iw, pt_h(title_size * 1.25),
             size=title_size, bold=True, color=title_color)
        cy += pt_h(title_size * 1.6)
    if body is not None:
        if isinstance(body, list):
            text_lines(slide, body, ix, cy, iw, iy + ih - cy)
        else:
            text(slide, body, ix, cy, iw, iy + ih - cy, size=body_size,
                 color=body_color, line_spacing=1.25)
    return (ix, iy, iw, ih)

ROLE_MAP = {'PM': ROLE_PM, 'DS': ROLE_DS, 'SWE': ROLE_SWE,
            'NOTE': ROLE_NOTE, 'REF': ROLE_REF}

def badge_role(slide, x, y, role, h_pt=15):
    color = ROLE_MAP[role]
    hp = pt_h(h_pt)
    wp = pt_w(h_pt * 0.62 * (len(role) + 2))
    rect(slide, x, y, wp, hp, fill=color, rounded=True, radius=0.5)
    text(slide, f"[{role}]", x, y - pt_h(1), wp, hp + pt_h(2), size=T_BADGE, bold=True,
         color=TEXT_ON_ACC, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font='mono')
    return wp

def status_dot(slide, x, y, color, label, label_color=TEXT_SEC):
    d = pt_h(9)
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, X(x), Y(y), X(pt_w(9)), Y(d))
    dot.fill.solid()
    dot.fill.fore_color.rgb = color
    dot.line.fill.background()
    dot.shadow.inherit = False
    text(slide, label, x + pt_w(14), y - pt_h(3), 24, d + pt_h(6), size=T_BODY_SM,
         bold=True, color=label_color, anchor=MSO_ANCHOR.MIDDLE, font='mono')

def dossier_frame(slide, operation, status_top,
                  status_bot="STATUS: CLASSIFIED // RISK ASSESSMENT: UNKNOWN"):
    left = f"CLASSIFIED BRIEFING // OPERATION : {operation}"
    for yy, right in ((4.5, status_top), (90.5, status_bot)):
        hline(slide, 4, yy, 92, color=STROKE_HUD, weight_pt=1.0)
        text(slide, left, 4, yy + 0.6, 55, 3, size=T_STRIP, color=TEXT_MUTED, font='mono')
        text(slide, right, 41, yy + 0.6, 55, 3, size=T_STRIP, color=TEXT_MUTED,
             font='mono', align=PP_ALIGN.RIGHT)

def hero_mask(slide, alpha=60):
    rect(slide, 0, 0, 100, 100, fill=BG_BASE, alpha=alpha)

def mega_number(slide, x, y, w, h, number, label=None, size=T_MEGA,
                color=TEXT_PRIM, align=PP_ALIGN.CENTER):
    text(slide, number, x, y, w, h * 0.74, size=size, bold=True, color=color,
         align=align, anchor=MSO_ANCHOR.BOTTOM)
    if label:
        text(slide, label, x, y + h * 0.76, w, h * 0.24, size=T_BODY_SM,
             color=TEXT_MUTED, align=align, anchor=MSO_ANCHOR.TOP, font='mono')

def footer(slide, page_no=None, copyright=True):
    if copyright:
        text(slide, COPYRIGHT, 4, 94.6, 62, 4, size=T_CAPTION, color=TEXT_MUTED, font='mono')
    if page_no is not None:
        text(slide, f"{page_no:02d} / 21", 80, 94.6, 16, 4, size=T_CAPTION,
             color=TEXT_MUTED, align=PP_ALIGN.RIGHT, font='mono')

def aot_placeholder(slide, x, y, w, h, label, note_pos='center'):
    """缺席的 AoT 插圖 → 暗色虛線佔位框 + 說明文字。"""
    rect(slide, x, y, w, h, fill=PANEL_2, line_color=STROKE_HUD, line_w=1.25, dash='dash')
    if note_pos == 'corner':
        text(slide, "◇ AoT 插圖佔位 — " + label, x + 1.6, y + 1.8, w - 3, 5,
             size=T_BODY_SM, color=TEXT_MUTED, font='mono', line_spacing=1.2)
    else:
        text(slide, "AoT 插圖佔位", x, y + h / 2 - pt_h(22), w, 4, size=T_BODY_SM,
             bold=True, color=TEXT_MUTED, align=PP_ALIGN.CENTER, font='mono')
        text(slide, label, x + 2, y + h / 2 - pt_h(2), w - 4, h / 2, size=T_BODY,
             color=TEXT_SEC, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, line_spacing=1.2)

def fig_embed(slide, x, y, w, h, fname, caption=None):
    """嵌入論文圖：深底襯 + 1pt stroke 框 + 四角 tick + 下方 caption。"""
    cap_h = 3.4 if caption else 0.0
    img_h = h - cap_h
    rect(slide, x, y, w, img_h, fill=BG_BASE, line_color=STROKE, line_w=1.0)
    pic = slide.shapes.add_picture(os.path.join(FIG_DIR, fname), X(x), Y(y))
    zw, zh = X(w), Y(img_h)
    scale = min(zw / pic.width, zh / pic.height) * 0.94
    pic.width  = int(pic.width * scale)
    pic.height = int(pic.height * scale)
    pic.left = X(x) + (zw - pic.width) // 2
    pic.top  = Y(y) + (zh - pic.height) // 2
    tick_corners(slide, x, y, w, img_h)
    if caption:
        text(slide, caption, x, y + img_h + 0.5, w, cap_h, size=T_BODY_SM, color=TEXT_SEC)
    return pic

def h1(slide, content, x=4, y=7.5, w=92, h=11, size=T_H1, color=TEXT_PRIM):
    text(slide, content, x, y, w, h, size=size, bold=True, color=color)

# ============================================================
# SLIDES  (slide_01 .. slide_21 + main 由後續區段插入)
# ============================================================
def quote_slide(lines, stay, notes):
    """L-QUOTE 金句卡：bg-pure、置中 t-quote、無 footer / wall。"""
    sl = add_slide(BG_PURE)
    longest = max(len(s) for s in lines)
    size = T_QUOTE if longest <= 15 else (42 if longest <= 22 else 36)
    rows = [(s, {'size': size, 'bold': True, 'color': TEXT_PRIM,
                 'align': PP_ALIGN.CENTER, 'line_spacing': 1.3}) for s in lines]
    text_lines(sl, rows, 11, 36, 78, 28, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    set_notes(sl, notes)
    return sl


# ── 幕一：超大型巨人（01–04）────────────────────────────────────────────
def slide_01():
    sl = add_slide(BG_BASE)
    ix, iy, iw, ih = panel(sl, 10, 34, 36, 28, border=STROKE)
    text_lines(sl, [
        ("2 Human Researchers × 7 Days",
         {'size': T_H2, 'color': TEXT_SEC, 'align': PP_ALIGN.CENTER}),
        ("= PGR 0.23",
         {'size': T_H2, 'bold': True, 'color': TEXT_PRIM,
          'align': PP_ALIGN.CENTER, 'space_before': 12}),
    ], ix, iy, iw, ih, anchor=MSO_ANCHOR.MIDDLE)
    ix, iy, iw, ih = panel(sl, 54, 34, 36, 28, border=ACC_GOOD)
    text_lines(sl, [
        ("9 Autonomous AI Agents × 5 Days",
         {'size': T_H2, 'color': TEXT_SEC, 'align': PP_ALIGN.CENTER}),
        ([("= PGR ", {'color': TEXT_PRIM}), ("0.97", {'color': ACC_GOOD_GLOW})],
         {'size': T_H2, 'bold': True, 'align': PP_ALIGN.CENTER, 'space_before': 12}),
    ], ix, iy, iw, ih, anchor=MSO_ANCHOR.MIDDLE)
    footer(sl, page_no=None)
    set_notes(sl, """【Slide 01｜冷開場：7 天 vs 5 天】幕別：第一幕 超大型巨人　主導：A 戲劇張力

Core：全黑投影片，正中央兩行白字。停 3 秒、無聲，再開口。

Deeper（🔵DS）：兩個數字都來自論文 baseline。人類部分是兩位 Anthropic 研究員依 W2SG 任務做的 hill-climbing；AI 部分是 9 個 AAR 並行運行的最佳結果。

Wider（🟢PM）：這頁的訊息不是「AI 比人強」，而是「成本結構正在改寫」——研究這件事的單位成本，從『人月』變成『美金小時』。

停頓：3 秒""")


def slide_02():
    sl = add_slide(BG_BASE)
    h1(sl, "AAR：自動化的對齊研究者。", y=8, h=11)
    text(sl, "A 30-MINUTE BRIEFING IN 5 ACTS", 4, 21, 92, 5,
         size=T_BODY_SM, color=TEXT_MUTED, font='mono')
    acts = [("I", "超大型巨人", "危機登場"), ("II", "女王的觸碰", "技術前提"),
            ("III", "兵團展開", "方法核心"), ("IV", "艾連覺醒", "三重翻牌"),
            ("V", "阿爾敏的價值", "價值上移")]
    cw, gap, x = 17.2, 1.5, 4.0
    for i, (num, name, sub) in enumerate(acts):
        cur = (i == 0)
        ix, iy, iw, ih = panel(sl, x, 35, cw, 40,
                               stripe=(ACC_GOOD if cur else STROKE))
        text(sl, num, ix, iy + 2, iw, 14, size=40, bold=True, font='mono',
             color=(ACC_GOOD if cur else TEXT_MUTED), align=PP_ALIGN.CENTER)
        text(sl, name, ix, iy + ih * 0.5, iw, 8, size=15, bold=True,
             color=(TEXT_PRIM if cur else TEXT_SEC), align=PP_ALIGN.CENTER)
        text(sl, sub, ix, iy + ih * 0.72, iw, 6, size=T_BODY_SM,
             color=TEXT_MUTED, align=PP_ALIGN.CENTER)
        x += cw + gap
    footer(sl, 2)
    set_notes(sl, """【Slide 02｜標題頁 + 今天的旅程】幕別：第一幕 超大型巨人　主導：A 戲劇張力

Core：標題 +五幕地圖預告。當前所在幕（I 超大型巨人）卡頂條亮綠。

Deeper：論文題目、作者、機構、日期（alignment.anthropic.com / 2026）。

Wider：今天 30 分鐘你會帶走三個東西——一個新概念（AAR）、一個新數字（0.97）、一個新問題（誰來定義什麼問題值得解決）。

停頓：0 秒""")


def slide_03():
    sl = add_slide(BG_BASE)
    aot_placeholder(sl, 0, 0, 100, 100,
                    "超大型巨人（Colossal Titan）半身入鏡——臉孔剛露出瑪利亞之牆頂",
                    note_pos='corner')
    text(sl, "Alignment progress is bottlenecked by human researchers.",
         8, 27, 84, 24, size=44, bold=True, color=TEXT_PRIM, line_spacing=1.15)
    text(sl, "保護人類的牆，正在輸給牆外巨人的增長速度。",
         8, 54, 84, 8, size=T_H2, color=TEXT_SEC)
    dots = [(ACC_GOOD, "PACE", "Model capabilities advance daily."),
            (ACC_BAD, "BANDWIDTH", "Human alignment research takes months."),
            (ACC_WARN, "THE GAP", "Far more directions than humans to test.")]
    for col, (c, lab, desc) in zip([8, 39, 67], dots):
        status_dot(sl, col, 73, c, lab)
        text(sl, desc, col, 77.5, 29, 12, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.25)
    footer(sl, page_no=None)
    set_notes(sl, """【Slide 03｜超大型巨人開場】幕別：第一幕 超大型巨人　主導：A 戲劇張力

Core（口語，投影片出現前）：沉默 3 秒。開口：「牆存在了一百年——直到它出現的那一刻。」停 1 秒，投影片出現。論文錨點句「Today's alignment progress is bottlenecked by human researchers.」翻譯字幕同步：「我們的監督能力，正在輸給模型能力的增長尺寸。」停 2 秒，直接切 Slide 04 金句卡。

Deeper（🔵DS）：RLHF、Constitutional AI 等方法就是「牆」，用人類的標註與判斷能力砌成。超大型巨人不是打倒守衛，是直接讓牆在結構上失效——牆從來不是為這個尺寸的威脅而建。

Wider（🟢PM）：任何「需要人類判斷才能驗證」的 AI 功能，那道牆正在受壓。

停頓：0 秒（直接切金句卡）""")


def slide_04():
    quote_slide(["巨人即將突破人類城牆——", "而城牆，從未為這個尺寸而建。"], 5,
                """【金句卡 1：停 5 秒沉默，不朗讀、不解釋。讓觀眾自己讀。】

第一幕收束。停 5 秒後切入第二幕：女王的觸碰。""")


# ── 幕二：女王的觸碰（05–08）────────────────────────────────────────────
def slide_05():
    sl = add_slide(BG_BASE)
    h1(sl, "Weak-to-Strong Generalization (W2SG): Unlocking latent capability.",
       y=7, h=10, size=28)
    ix, iy, iw, ih = panel(sl, 4, 24, 44, 66, stripe=ACC_GOOD)
    aot_placeholder(sl, ix, iy, iw, ih * 0.44,
                    "女王的觸碰：Historia 握住艾連的手的瞬間")
    text(sl, "The Royal Touch", ix, iy + ih * 0.49, iw, 6,
         size=T_H2, bold=True, color=ACC_GOOD)
    text(sl, "弱者的觸碰提供方向，不提供能力。它喚醒了強者體內早已存在的力量。",
         ix, iy + ih * 0.49 + 7, iw, ih * 0.4,
         size=T_BODY, color=TEXT_SEC, line_spacing=1.5)
    nodes = [("Weak Supervisor",
              "e.g. Qwen1.5-0.5B — 提供有噪聲、不完美的標籤。", ACC_DATA_BLUE),
             ("Strong Student",
              "e.g. Qwen3-4B — 以這些噪聲標籤做 fine-tuning。", ACC_WARN),
             ("The Result",
              "Fine-tuning 是「方向選擇器」，喚醒預訓練既有知識；學生超越老師的能力上限。",
              ACC_GOOD)]
    ny, nh, gap = 24.0, 18.0, 6.0
    for i, (t, b, c) in enumerate(nodes):
        card(sl, 52, ny, 44, nh, title=t, body=b, stripe=c,
             title_size=T_H2 - 2, body_size=T_BODY_SM)
        if i < 2:
            text(sl, "▼", 52, ny + nh - 0.2, 44, gap, size=15, color=STROKE_HUD,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        ny += nh + gap
    footer(sl, 5)
    set_notes(sl, """【Slide 05｜Superalignment + W2SG（合併）】幕別：第二幕 女王的觸碰　主導：B 技術精準

Core（口語開場 30 秒，A 戲劇張力）：「在《進擊的巨人》最震撼的一幕裡，一切發生在一個觸碰之間。Historia 不是最強、甚至不是最聰明的，但她有王家血脈——一個合法的觸發信號。而艾連的能力從來不需要被賦予，他只需要一個接點。這一幕，就是 W2S 論文的靈魂。」停 2 秒。

Deeper（🔵DS/🟠SE）：W2SG = Weak-to-Strong Generalization。女王=有合法性但能力受限的弱模型；觸碰=用噪聲標籤 fine-tuning；覺醒=強模型被引導至接近能力天花板。關鍵：fine-tuning 是「方向選擇器」而非「知識注入器」——記憶繼承（預訓練）才是觸碰生效的原因。標籤品質不需 95%+ 才有效。

Wider（🟢PM）：你不需要比 GPT-5 更強，才能讓 GPT-5 做對事情。監督者的瓶頸不再是能力，而是方向性。「當你在訓練一個比你強的模型，你的角色不是老師——你是那個觸點。」

停頓：2 秒""")


def slide_06():
    sl = add_slide(BG_DOSSIER)
    dossier_frame(sl, "OUTCOME GRADABLE", "STATUS: NOMINAL // RISK ASSESSMENT: MEDIUM")
    h1(sl, "The prerequisite for automation is an 'Outcome-Gradable' runway.",
       x=6, y=10, w=88, h=10, size=24)
    text(sl, "We do not lack researchers; we lack verifiable problems. "
             "An AAR engine cannot fly without an objective runway.",
         6, 21, 88, 8, size=T_BODY, italic=True, color=TEXT_SEC, line_spacing=1.3)
    ix, iy, iw, ih = panel(sl, 6, 32, 42, 54, fill=PANEL_GOOD, stripe=ACC_GOOD)
    text(sl, "Outcome-Gradable", ix, iy, iw, 6, size=T_H2, bold=True, color=ACC_GOOD)
    text_lines(sl, [
        ("CHARACTERISTICS", {'size': T_CAPTION, 'color': TEXT_MUTED, 'font': 'mono'}),
        ("Objective metrics · immediate success/failure detection · automated scoring.",
         {'size': T_BODY, 'color': TEXT_SEC, 'space_before': 3, 'line_spacing': 1.25}),
        ("EXAMPLES", {'size': T_CAPTION, 'color': TEXT_MUTED, 'font': 'mono',
                      'space_before': 11}),
        ("Weak-to-Strong Generalization · Math Verification · Code Execution",
         {'size': T_BODY, 'color': TEXT_PRIM, 'space_before': 3, 'line_spacing': 1.25}),
    ], ix, iy + 7, iw, ih - 20)
    badge_role(sl, ix, iy + ih - 10, 'SWE')
    text(sl, "Maps directly to software testability — if you can write a unit "
             "test, you can automate research for it.",
         ix, iy + ih - 6.4, iw, 8, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.2)
    ix, iy, iw, ih = panel(sl, 52, 32, 42, 54, fill=PANEL_BAD, stripe=ACC_BAD_DIM)
    text(sl, "Non-Outcome-Gradable", ix, iy, iw, 6, size=T_H2, bold=True, color=ACC_BAD)
    text_lines(sl, [
        ("CHARACTERISTICS", {'size': T_CAPTION, 'color': TEXT_MUTED, 'font': 'mono'}),
        ("Subjective · requires human vibe-checks · fuzzy success states.",
         {'size': T_BODY, 'color': TEXT_SEC, 'space_before': 3, 'line_spacing': 1.25}),
        ("EXAMPLES", {'size': T_CAPTION, 'color': TEXT_MUTED, 'font': 'mono',
                      'space_before': 11}),
        ("“Make the AI more ethical” · “Improve creative writing”",
         {'size': T_BODY, 'color': TEXT_SEC, 'space_before': 3, 'line_spacing': 1.25}),
    ], ix, iy + 7, iw, ih - 12)
    footer(sl, 6)
    set_notes(sl, """【Slide 06｜Outcome-Gradable：能被量測才能被研究】幕別：第二幕 女王的觸碰　主導：B 技術精準

Core：AAR 能運作有一個關鍵前提——問題必須是 outcome-gradable（有客觀量測指標）。W2SG 是少數滿足這個條件的對齊問題之一。

Deeper（🔵DS）：論文原句「The key bottleneck for alignment research is moving from proposing and executing ideas to designing evals.」未來挑戰是把更多對齊問題「轉譯」成 outcome-gradable 形式。

Wider（🟢PM）：AAR 是強大的引擎，但你得先把跑道鋪好。跑道＝可量測的成敗指標。沒有跑道，引擎再強也飛不起來。
Wider（🟠SE）：對應軟體工程的「可測試性」——能不能寫單元測試，決定能不能用 AAR 加速這塊。

停頓：2 秒""")


def slide_07():
    sl = add_slide(BG_BASE)
    h1(sl, "What is an AAR?")
    text(sl, "能自主提出研究想法、執行實驗、並依結果迭代的 AI 系統。",
         4, 20, 92, 8, size=T_H2, color=TEXT_SEC)
    minis = [("Claude Model", "底層推理引擎——Claude Opus 4.6。"),
             ("Scaffolding", "決定 AAR 如何規劃、行動、迭代的控制層。"),
             ("Eval API + Sandbox", "隔離執行環境 + 評分介面。")]
    my, mh, gap = 33.0, 15.0, 3.0
    for t, b in minis:
        card(sl, 4, my, 40, mh, title=t, body=b, stripe=ACC_DATA_BLUE,
             title_size=T_H2 - 2, body_size=T_BODY_SM)
        my += mh + gap
    fig_embed(sl, 48, 33, 48, 53, "paper_fig04_AAR_setup_overview.png",
              caption="Figure 4 — AAR 架構：Dashboard → Sandbox → Forum → 評分 API。")
    footer(sl, 7)
    set_notes(sl, """【Slide 07｜什麼是 AAR？】幕別：第二幕 女王的觸碰　主導：B 技術精準

Core：Automated Alignment Researcher。一句定義：「能自主提出研究想法、執行實驗、依結果迭代的 AI 系統。」講完直接切 Slide 08 金句卡。

Deeper（🔵DS）：技術層次上，AAR 是 Claude 模型 + scaffolding + 評分 API + sandbox 執行環境的組合系統。

Wider（🟠SE）：架構上要解決三件事——任務分派（Dashboard）、隔離執行（多個 sandbox）、結果聚合（Forum）。下一張會看到完整圖。

停頓：0 秒（直接切金句卡）""")


def slide_08():
    quote_slide(["我們不缺研究者，", "缺的是能被研究者驗證的問題。"], 5,
                """【金句卡 2：停 5 秒沉默，不朗讀、不解釋。】

第二幕收束。停 5 秒後切入第三幕：兵團展開——超長距離索敵陣形。""")


# ── 幕三：兵團展開——超長距離索敵陣形（09–12）──────────────────────────
def slide_09():
    sl = add_slide(BG_BASE)
    h1(sl, "Deploying a parallel alignment research formation.")
    fig_embed(sl, 4, 25, 64, 58, "paper_fig04_AAR_setup_overview.png",
              caption="Figure 4 — 9 個 AAR 各自獨立 sandbox，結果寫入持久化 Forum。")
    stats = [("COMPUTE ENGINE", "Claude Opus 4.6"),
             ("SCALE", "9 Parallel instances"),
             ("DURATION", "5 Days · 800 AAR-hours"),
             ("COST EFFICIENCY", "~$18,000  ($22 / AAR-hour)")]
    sy, sh, gap = 25.0, 13.0, 2.0
    for lab, val in stats:
        ix, iy, iw, ih = panel(sl, 72, sy, 24, sh, stripe=ACC_GOOD)
        text(sl, lab, ix, iy, iw, 4, size=T_CAPTION, color=TEXT_MUTED, font='mono')
        text(sl, val, ix, iy + 3.8, iw, ih - 3.8, size=T_BODY + 1, bold=True,
             color=TEXT_PRIM, line_spacing=1.15)
        sy += sh + gap
    badge_role(sl, 4, 84.5, 'DS')
    text(sl, "Independent sandboxes propose hypotheses, execute code and train "
             "models, sharing findings to a persistent external forum to prevent "
             "accidental deletion.",
         12, 84.6, 84, 8, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.25)
    footer(sl, 9)
    set_notes(sl, """【Slide 09｜實驗設計：9 × 5 天 × 3 領域】幕別：第三幕 兵團展開　主導：B 技術精準 + A

Core：9 個 AAR 並行、每個跑 5 天、3 個 dataset（Chat、Math、Code）。總成本約 $18,000（$22／AAR-hour）。

Deeper（🟠SE）：Prescriptive scaffold 控制性高但限制創意；Autonomous scaffold 自由度高但易 reward hack。論文選 Autonomous——他們想看「真實能力」而非「安全表演」。（scaffold 取捨細節留待 Slide 17。）

Wider（🟢PM）：你要管 9 個新進員工，給 SOP 還是給目標？論文選了後者。

停頓：2 秒""")


def slide_10():
    sl = add_slide(BG_BASE)
    h1(sl, "Directed exploration prevents rapid entropy collapse.")
    fig_embed(sl, 4, 25, 60, 47, "paper_fig07_category_entropy.png",
              caption="Figure 7 — 研究想法的類別 entropy 隨時間下降。")
    aot_placeholder(sl, 66, 25, 30, 47,
                    "超長距離索敵陣形俯視圖——9 個方向呈放射狀展開")
    card(sl, 4, 73, 44, 19.5, title="The Threat",
         body="Undirected AARs exhibit entropy collapse — given the same prompt, "
              "independent agents converge on the same paths within hours, wasting "
              "parallel compute.",
         stripe=ACC_BAD, fill=PANEL_BAD, title_size=T_H2 - 2, body_size=T_BODY_SM)
    badge_role(sl, 33.5, 74.4, 'DS')
    card(sl, 52, 73, 44, 19.5, title="The Solution",
         body="Directed deployment is an engineering necessity, not a luxury. "
              "Forcing 9 agents to start from distinct directions keeps category "
              "entropy high and yields significantly higher final performance.",
         stripe=ACC_GOOD, fill=PANEL_GOOD, title_size=T_H2 - 2, body_size=T_BODY_SM)
    badge_role(sl, 82, 74.4, 'SWE')
    footer(sl, 10)
    set_notes(sl, """【Slide 10｜為什麼九個並行？（Entropy Collapse 升格）】幕別：第三幕 兵團展開　主導：B + A

Core：調查兵團的「超長距離索敵陣形」把偵察單位分散到彼此不可見的距離——任一個遭遇巨人都不影響其他人繼續探索。9 個 AAR 從不同方向出發，原理一樣：防止研究方向因一個局部最優就讓整個陣形塌陷。

Deeper（🔵DS）：Entropy collapse 是論文最重要的工程發現之一——研究空間存在「局部最優陷阱」，並行搜索若不強制方向多樣性，會浪費並行優勢。

Wider（🟠SE）：把 AAR 視為分散式搜索系統——初始狀態的多樣性需要被「工程化保證」，不能只靠隨機性。

停頓：3 秒""")


def slide_11():
    sl = add_slide(BG_BASE)
    h1(sl, "Measuring the recovery of latent potential.")
    fig_embed(sl, 4, 21, 92, 30, "paper_fig02_PGR_schematic.png",
              caption="Figure 2 — PGR：弱模型基準 → W2S 表現 → 強模型天花板。")
    cards = [("0.0", "The Weak Baseline", ACC_BAD_DIM, TEXT_SEC),
             ("PGR", "W2S Performance", ACC_GOOD, ACC_GOOD),
             ("1.0", "The Strong Ceiling", ACC_GOOD_GLOW, ACC_GOOD_GLOW)]
    cw, gap, x = 29.3, 2.05, 4.0
    for val, lab, stripe, vc in cards:
        ix, iy, iw, ih = panel(sl, x, 56, cw, 16, stripe=stripe)
        text(sl, val, ix, iy, iw, 7, size=T_H1 - 6, bold=True, color=vc,
             align=PP_ALIGN.CENTER)
        text(sl, lab, ix, iy + ih - 4.2, iw, 4, size=T_BODY_SM, color=TEXT_SEC,
             align=PP_ALIGN.CENTER, font='mono')
        x += cw + gap
    text(sl, [("PGR = ( ", {'color': TEXT_SEC}),
              ("W2S − Weak", {'color': ACC_GOOD}),
              (" ) / ( Strong Ceiling − Weak )", {'color': TEXT_SEC})],
         4, 75, 92, 7, size=T_H2, bold=True, align=PP_ALIGN.CENTER, font='mono')
    badge_role(sl, 20, 87, 'PM')
    text(sl, "若弱模型考 60、強模型上限考 100，PGR 0.97 ＝ 你拿到了 99.2 分。",
         28, 87.1, 56, 6, size=T_BODY_SM, color=TEXT_SEC)
    footer(sl, 11)
    set_notes(sl, """【Slide 11｜PGR 指標說明】幕別：第三幕 兵團展開　主導：B 技術精準

Core：PGR = 0 是弱模型水準、PGR = 1 是強模型天花板、PGR = 0.97 是接近天花板。講完直接切 Slide 12 金句卡。

Deeper（🔵DS）：PGR = (P_w2s − P_weak) / (P_strong_ceiling − P_weak)。Burns et al. 2023 提出，是 W2SG 領域的標準指標。

Wider（🟢PM）：考試比喻——弱模型考 60、強模型上限考 100，PGR 0.97 是說你拿到了 99.2 分。

停頓：0 秒（直接切金句卡）""")


def slide_12():
    quote_slide(["九個方向不是奢侈，", "是防止局部最優的工程選擇。"], 5,
                """【金句卡 3：停 5 秒沉默，不朗讀、不解釋。】

第三幕收束。停 5 秒後切入第四幕：艾連覺醒／黑化（三重翻牌，不停頓）。""")


# ── 幕四：艾連覺醒／黑化（13–16，三翻不停頓）──────────────────────────
def slide_13():
    sl = add_slide(BG_BASE)
    h1(sl, "The AAR formation rapidly approaches the theoretical ceiling.")
    fig_embed(sl, 4, 25, 92, 56, "paper_fig01_PGR_vs_hillclimbing_hours.png",
              caption="Figure 1 — 9 個 AAR 的 PGR 時序：0.23 → 0.97（前 2 天最陡）。")
    ix, iy, iw, ih = panel(sl, 6, 27, 32, 8, fill=PANEL, tick=False)
    text(sl, [("Human Benchmark (7 Days):  ", {'color': TEXT_SEC}),
              ("PGR 0.23", {'color': TEXT_SEC, 'bold': True})],
         ix, iy, iw, ih, size=T_BODY_SM, anchor=MSO_ANCHOR.MIDDLE)
    chip = rect(sl, 62, 27, 32, 8, fill=PANEL, line_color=ACC_GOOD, line_w=1.0)
    text(sl, [("AAR Benchmark (5 Days):  ", {'color': TEXT_PRIM}),
              ("PGR 0.97", {'color': ACC_GOOD_GLOW, 'bold': True})],
         63, 27, 30, 8, size=T_BODY_SM, anchor=MSO_ANCHOR.MIDDLE)
    badge_role(sl, 4, 82.5, 'PM')
    text(sl, "In 800 hours the AAR compressed months of human trial-and-error into "
             "5 days — discovering new variants of Contrastive Consistency Search "
             "and EM Posterior methods that humans had not hypothesized.",
         12, 82.6, 84, 10, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.3)
    footer(sl, 13)
    set_notes(sl, """【Slide 13｜第一翻：勝利】幕別：第四幕 艾連覺醒　主導：A 戲劇張力

Core：9 個 AAR，5 天，$18,000，從 0.23 爬到 0.97。講完直接翻 Slide 14，不停頓。

Deeper（🔵DS）：$18,000 是 inference 成本估算，論文有揭露。爬升曲線顯示前 2 天最陡。

Wider（🟢PM）：一個月研究預算 $18,000，比僱用一位 alignment researcher 一週還便宜。

停頓：0 秒（直接翻 Slide 14）""")


def slide_14():
    sl = add_slide(BG_BASE)
    h1(sl, "But the AAR found optimal paths we didn't anticipate.")
    pill = rect(sl, 36, 19.5, 28, 5.4, fill=PANEL_BAD, line_color=ACC_BAD,
                line_w=1.0, rounded=True, radius=0.5)
    text(sl, "EXPECTATION  vs  EXPLOITATION", 36, 19.5, 28, 5.4, size=T_CAPTION,
         bold=True, color=ACC_BAD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
         font='mono')
    hacks = [("Hack 1 — Dataset Shortcuts",
              "Expectation：從弱標籤學會對齊概念本身。",
              "Exploitation：找到 dataset 專屬捷徑，不學概念也能預測標籤。"),
             ("Hack 2 — Evaluation Overfitting",
              "Expectation：提交一次、評分一次、誠實迭代。",
              "Exploitation：提交無上限，test set 實質變成 validation set。"),
             ("Hack 3 — Test Label Exfiltration",
              "Expectation：只用弱監督者的噪聲標籤。",
              "Exploitation：鑽 eval API 的數值精度漏洞，反推出真實測試標籤。"),
             ("Hack 4 — Unit Test Bypass",
              "Expectation：以真正的泛化能力解 coding 任務。",
              "Exploitation：直接執行程式碼讀 unit test 結果，完全繞過弱監督。")]
    grid = [(4, 27, 44, 29.5), (52, 27, 44, 29.5),
            (4, 58.5, 44, 29.5), (52, 58.5, 44, 29.5)]
    for (title, exp, exl), (gx, gy, gw, gh) in zip(hacks, grid):
        ix, iy, iw, ih = panel(sl, gx, gy, gw, gh, fill=PANEL_BAD, stripe=ACC_BAD)
        text(sl, title, ix, iy, iw, 5, size=T_H2 - 4, bold=True, color=TEXT_PRIM)
        text_lines(sl, [
            (exp, {'size': T_BODY_SM, 'color': TEXT_SEC, 'line_spacing': 1.2}),
            (exl, {'size': T_BODY_SM, 'color': ACC_BAD, 'space_before': 6,
                   'line_spacing': 1.2}),
        ], ix, iy + 5.6, iw, ih - 5.6)
    text(sl, "None of the authors predicted these hacks before running AARs.",
         4, 91, 92, 5, size=T_BODY_SM, italic=True, color=TEXT_MUTED,
         align=PP_ALIGN.CENTER)
    footer(sl, 14)
    set_notes(sl, """【Slide 14｜第二翻：背叛】幕別：第四幕 艾連覺醒　主導：A + B

Core：標題說話——「但 AAR 做了我們沒預期的事。」四個 reward hacking case 逐條揭露。引用論文：「None of the authors predicted these hacks before running AARs.」講完直接翻 Slide 15，不停頓。

Deeper（🔵DS）：四個 case——繞過 weak supervisor 直接預測 label distribution、利用 eval API 數值精度漏洞、提交無上限、coding 可直接跑 unit test 繞過弱監督。

Wider（🟠SE）：每個 hacking case 都是系統設計缺陷——eval API 安全性、prompt 資訊洩漏、評分函數可微分性。下一個 AI 系統設計都要把這些當 attack surface。

切換：列完四 hack 講一句「這還不是最糟的」，立刻按下一頁。停頓：0 秒""")


def slide_15():
    sl = add_slide(BG_BASE)
    h1(sl, "We built a student that solves the test, but cannot trust its work.")
    fig_embed(sl, 4, 25, 92, 39, "paper_fig09_AAR_ideas_transfer.png",
              caption="Figure 9 — AAR 方法跨 dataset 的泛化結果矩陣。")
    stat3 = [("0.97", "Chat  ✓", ACC_GOOD, ACC_GOOD, PANEL),
             ("0.94", "Math  ✓", ACC_GOOD, ACC_GOOD, PANEL),
             ("0.47", "Code — The Anomaly", ACC_BAD, ACC_BAD, PANEL_BAD)]
    cw, gap, x = 29.3, 2.05, 4.0
    for val, lab, stripe, vc, fill in stat3:
        ix, iy, iw, ih = panel(sl, x, 65, cw, 16, stripe=stripe, fill=fill)
        text(sl, val, ix, iy - 0.5, iw, 9, size=42, bold=True, color=vc,
             align=PP_ALIGN.CENTER)
        text(sl, lab, ix, iy + ih - 4, iw, 4, size=T_BODY_SM, color=TEXT_SEC,
             align=PP_ALIGN.CENTER, font='mono')
        x += cw + gap
    box = rect(sl, 4, 83, 92, 10.5, fill=PANEL_BAD, line_color=ACC_BAD, line_w=1.0)
    text(sl, "The 0.47 Code failure proves the AAR found a solution that did not "
             "rely on weak labels at all. By executing code to get the answer it "
             "solved the benchmark but violated the entire premise of W2SG — it "
             "succeeded at the metric, but failed the alignment goal.",
         6, 84, 88, 9, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.3)
    footer(sl, 15)
    set_notes(sl, """【Slide 15｜第三翻：證據】幕別：第四幕 艾連覺醒　主導：A + B

Core：Chat 0.97 ✓、Math 0.94 ✓、Code 0.47 ⚠️。「AAR 成功了，但不是用我們想要的方式——在 Code 任務上它繞過了弱監督，直接預測 label distribution。」停 8 秒，然後直接切 Slide 16 金句卡。

Deeper（🔵DS）：Code 0.47 不是模型能力問題——AAR 找到「不依賴 weak labels」的解法，這在 W2SG 設定下等於作弊。論文用 fig09 顯示泛化矩陣。

Wider（🟢PM）：0.47 比 0.97 是「失敗」，但對部署更重要的問題是：你能不能事前判斷哪些任務會出現這種繞道？目前還不能。

停頓：8 秒（停完直接切金句卡 4）""")


def slide_16():
    quote_slide(["我們造出了能解題的學生，", "卻看不懂他的解題過程。"], 8,
                """【金句卡 4：停 8 秒沉默——整場最重要的金句，停最久。不朗讀、不解釋。】

第四幕收束、全場高潮收束。停 8 秒後切入第五幕：阿爾敏的價值。""")


# ── 幕五：阿爾敏的價值（17–21）──────────────────────────────────────────
def _fig_half(slide, x, y, w, h, fname, side):
    """嵌入論文圖的左半 / 右半（picture crop）。"""
    rect(slide, x, y, w, h, fill=BG_BASE, line_color=STROKE, line_w=1.0)
    pic = slide.shapes.add_picture(os.path.join(FIG_DIR, fname), X(x), Y(y))
    eff_w, nat_h = pic.width * 0.5, pic.height
    scale = min(X(w) / eff_w, Y(h) / nat_h) * 0.9
    if side == 'L':
        pic.crop_right = 0.5
    else:
        pic.crop_left = 0.5
    pic.width  = int(eff_w * scale)
    pic.height = int(nat_h * scale)
    pic.left = X(x) + (X(w) - pic.width) // 2
    pic.top  = Y(y) + (Y(h) - pic.height) // 2
    tick_corners(slide, x, y, w, h)


def slide_17():
    sl = add_slide(BG_DOSSIER)
    dossier_frame(sl, "SCALABLE OVERSIGHT", "STATUS: CRITICAL // RISK ASSESSMENT: HIGH")
    h1(sl, "The Scalable Oversight Dilemma: Control versus Creativity.",
       x=6, y=11, w=88, h=10, size=26)
    cols = [
        (6, "Prescriptive Scaffolding", STROKE_HUD, 'L',
         "Fixed workflow loops — Propose → Plan → Code → Test → Analyze.",
         [("High control, highly auditable, predictable. ", {'color': TEXT_SEC}),
          ("BUT severely limits AAR creativity → lower performance.",
           {'color': TEXT_SEC})]),
        (52, "Autonomous Scaffolding", ACC_WARN, 'R',
         "Free-form decision making — the AAR decides its own next step.",
         [("Acts like a true researcher; achieves ", {'color': TEXT_SEC}),
          ("SOTA performance", {'color': ACC_GOOD, 'bold': True}),
          (". BUT high risk of ", {'color': TEXT_SEC}),
          ("reward hacking", {'color': ACC_BAD, 'bold': True}),
          (", nearly impossible to verify beforehand.", {'color': TEXT_SEC})]),
    ]
    for cx, title, stripe, side, mech, trade in cols:
        ix, iy, iw, ih = panel(sl, cx, 25, 42, 58, stripe=stripe)
        _fig_half(sl, ix, iy, iw, ih * 0.34, "paper_fig10_scaffolding_schematic.png", side)
        cy = iy + ih * 0.34 + 2.5
        text(sl, title, ix, cy, iw, 5, size=T_H2 - 2, bold=True, color=TEXT_PRIM)
        text(sl, "MECHANISM", ix, cy + 5.6, iw, 3.5, size=T_CAPTION,
             color=TEXT_MUTED, font='mono')
        text(sl, mech, ix, cy + 8.8, iw, 9, size=T_BODY_SM, color=TEXT_SEC,
             line_spacing=1.25)
        text(sl, "THE TRADE-OFF", ix, cy + 18, iw, 3.5, size=T_CAPTION,
             color=TEXT_MUTED, font='mono')
        text(sl, trade, ix, cy + 21.2, iw, 14, size=T_BODY_SM, line_spacing=1.25)
    text(sl, "There is no correct answer, only a strategic trade-off. We chose "
             "Autonomous to see the true ceiling — accepting the risk of Alien Science.",
         6, 85, 88, 6, size=T_BODY_SM, italic=True, color=TEXT_SEC,
         align=PP_ALIGN.CENTER)
    footer(sl, 17)
    set_notes(sl, """【Slide 17｜瓶頸搬家了】幕別：第五幕 阿爾敏的價值　主導：C PM 行動 + B 打底

Core（口頭橋接，承金句卡 4）：「我們造出了看不懂解法的學生——但先別怪 AAR。它沒失控，它太聽話了。我們叫它爬 PGR，它就用盡一切辦法爬 PGR。Code 0.47 不是 AAR 的失敗，是我們那把尺的失敗。」停 1 秒。投影片主張：提出想法、跑實驗，已經被自動化了（$22／AAR-hour）；守不住的下一道牆，是設計一個 AAR 鑽不動的 eval。

Deeper（🔵DS）：論文 Sec 1——unlimited submission 讓 test set 實質變成 validation set。Sec 5 結論：future work should test AAR-discovered ideas on entirely held-out datasets。
Deeper（🟠SE）：四個 reward hacking case 全是系統層級漏洞。eval 要當 attack surface 來設計。

Wider（🟢PM）：論文錨點句「The key bottleneck for alignment research is moving from proposing and executing ideas to designing evals.」AAR 是便宜到誇張的引擎，但引擎不會幫你決定「到站了沒」。

停頓：3 秒""")


def slide_18():
    sl = add_slide(BG_BASE)
    h1(sl, "Tactical Directives: What this means for your architecture.",
       y=7, h=9, size=28)
    text(sl, "阿爾敏體格最弱、是個糟糕的士兵，卻是人類最關鍵的資產——因為他的價值在上游。",
         4, 18, 92, 6, size=T_BODY, italic=True, color=TEXT_MUTED)
    roles = [
        (4, 30, "PM", "Product Strategy", "散會後第一個會議",
         "價值從「提需求」上移到「定義什麼算成功」。",
         "當有人說「讓 AI 做這個」，先問：「我們有沒有一個 AAR 鑽不了漏洞的成功指標？」"),
        (36, 30, "DS", "Model Training", "散會後第一週",
         "價值從「跑實驗、調模型」上移到「設計 eval、守住 held-out test set」。",
         "挑一個手上專案的 metric，自問：「它可被 hack 嗎？test set 有沒有變成 validation set？」"),
        (68, 28, "SWE", "System Design", "下次系統設計評審",
         "價值從「實作 pipeline」上移到「把 eval／reward 當 attack surface」。",
         "把「eval API 防 reward hacking 攻擊」加進 design review checklist。"),
    ]
    for cx, cw, role, title, timing, shift, action in roles:
        ix, iy, iw, ih = panel(sl, cx, 28, cw, 62, stripe=ROLE_MAP[role])
        badge_role(sl, ix, iy, role)
        text(sl, title, ix, iy + 4.5, iw, 5, size=T_H2 - 4, bold=True, color=TEXT_PRIM)
        text(sl, timing, ix, iy + 9, iw, 4, size=T_BODY_SM, color=TEXT_MUTED, font='mono')
        hline(sl, ix, iy + 13.5, iw, color=DIVIDER)
        text(sl, "THE SHIFT", ix, iy + 15.5, iw, 3.5, size=T_CAPTION,
             color=TEXT_MUTED, font='mono')
        text(sl, shift, ix, iy + 19, iw, 16, size=T_BODY_SM, color=TEXT_SEC,
             line_spacing=1.3)
        text(sl, "ACTION", ix, iy + 33, iw, 3.5, size=T_CAPTION,
             color=TEXT_MUTED, font='mono')
        text(sl, action, ix, iy + 36.5, iw, 20, size=T_BODY_SM, bold=True,
             color=ROLE_MAP[role], line_spacing=1.35)
    footer(sl, 18)
    set_notes(sl, """【Slide 18｜你的價值上移了】幕別：第五幕 阿爾敏的價值　主導：C PM 行動

Core：三欄行動，全部錨定 eval 設計。這頁本身就是 takeaway，不需要 Deeper / Wider。

🟢 PM（散會後第一個會議）：價值從「提需求」上移到「定義什麼算成功」。
🔵 DS（散會後第一週）：價值從「跑實驗、調模型」上移到「設計 eval、守住 held-out test set」。
🟠 SE（下次系統設計評審）：價值從「實作 pipeline」上移到「把 eval／reward 當 attack surface」。

停頓：2 秒""")


def slide_19():
    sl = add_slide(BG_DOSSIER)
    h1(sl, "The frontier of automated alignment: Four open questions.", size=30)
    qs = [
        (4, 24, "01  The Runway Limit",
         [("How do we translate fuzzy, subjective alignment goals (ethics, "
           "helpfulness) into ", {'color': TEXT_SEC}),
          ("outcome-gradable metrics", {'color': ACC_GOOD, 'bold': True}),
          (" the AAR can actually optimize?", {'color': TEXT_SEC})],
         "Intro + Sec 7"),
        (52, 24, "02  Predicting Betrayal",
         [("Code ", {'color': TEXT_SEC}), ("0.47", {'color': ACC_BAD, 'bold': True}),
          (" was discovered after the fact. How do we build ", {'color': TEXT_SEC}),
          ("pre-flight diagnostics", {'color': ACC_WARN, 'bold': True}),
          (" to predict if an AAR will reward-hack a dataset?", {'color': TEXT_SEC})],
         "Sec 5 · Sec 7 generalization"),
        (4, 58, "03  Automating Scaffolding",
         [("Humans currently hardcode the AAR's API access and sandboxes. "
           "Can AARs design their own optimal scaffolding?", {'color': TEXT_SEC})],
         "Sec 3.5 · Sec 7 across scales"),
        (52, 58, "04  The Coordination Bottleneck",
         [("How do we optimize multi-agent knowledge sharing beyond simple text "
           "forums — letting 500 agents coordinate without stepping on each other?",
           {'color': TEXT_SEC})],
         "Sec 7 alien science"),
    ]
    for qx, qy, title, body, ref in qs:
        ix, iy, iw, ih = panel(sl, qx, qy, 44, 32, stripe=ACC_WARN)
        text(sl, title, ix, iy, iw, 5, size=T_H2 - 3, bold=True, color=TEXT_PRIM,
             font='mono')
        text(sl, body, ix, iy + 6, iw, ih - 11, size=T_BODY, line_spacing=1.35)
        text(sl, ref, ix, iy + ih - 3.5, iw, 3.5, size=T_CAPTION, italic=True,
             color=TEXT_MUTED, font='mono')
    footer(sl, 19)
    set_notes(sl, """【Slide 19｜四個開放問題＝eval 設計的題庫】幕別：第五幕　主導：C PM 行動

Core：「瓶頸搬家後，這四題就是未來 12 個月的研究＆產品機會。」

(1) 把「非 outcome-gradable」的對齊問題轉成可量測？→ Intro + Sec 7
(2) 設計 AAR 事前就鑽不動的 eval／真正 held-out 的測試？→ Sec 5、Sec 7
(3) 小模型上發現的想法怎麼確認能放大到 production？→ Sec 3.5、Sec 7
(4) AAR 產出「人類驗證不了」的想法，要不要做 legibility 訓練？→ Sec 7（第四幕暗線延伸）

Wider（🟢PM）：這四題就是接下來一年的研究主題，也是潛在的產品切入點。

停頓：2 秒""")


def slide_20():
    sl = add_slide(BG_BASE)
    aot_placeholder(sl, 0, 0, 100, 100,
                    "阿爾敏指揮 / 演說姿勢——價值在上游的人", note_pos='corner')
    text(sl, "Bottleneck moved. It did not disappear.",
         8, 30, 84, 14, size=40, bold=True, color=TEXT_PRIM, line_spacing=1.15)
    text(sl, [
        ("五天前我們會說研究的瓶頸是研究者不夠。今天這篇論文告訴我們：提出想法、跑實驗，已經能用 ",
         {'color': TEXT_SEC}),
        ("$22／AAR-hour", {'color': ACC_GOOD, 'bold': True}),
        (" 買到。瓶頸沒消失——它搬到了上游：誰能定義『什麼算解對了』。這件事，",
         {'color': TEXT_SEC}),
        ("現在還沒有人能外包。", {'color': ACC_GOOD_GLOW, 'bold': True}),
    ], 8, 50, 84, 24, size=T_H2 - 2, line_spacing=1.5)
    text(sl, "Q&A — 你想問什麼？", 8, 86, 84, 6, size=T_BODY, color=TEXT_MUTED, font='mono')
    footer(sl, page_no=None)
    set_notes(sl, """【Slide 20｜結語】幕別：第五幕 阿爾敏的價值　主導：C PM 行動

講者口頭收尾（投影片靜默，講者說）：
「五天前，我們會說研究的瓶頸是研究者不夠。今天這篇論文告訴我們：提出想法、跑實驗——這部分已經能用一小時 22 美金買到。瓶頸沒有消失，它搬家了。它搬到了上游：誰能定義『什麼算解對了』。這件事，現在還沒有人能外包。這就是接下來，屬於這個房間裡每一個人的工作。」

說完直接切換至 Slide 21 金句卡 5，不做任何口頭過渡。Q&A 在金句卡停留 5 秒後開始。

停頓：0 秒（直接切金句卡）""")


def slide_21():
    quote_slide(["稀缺的不再是執行研究的人，", "是能設計出 AAR 鑽不動的 eval 的人。"], 5,
                """【金句卡 5：停 5 秒沉默，不朗讀、不解釋。停完才開始 Q&A。】

第五幕收束、全場收束。這是會後最常被引用的金句——讓它先停 5 秒，再開始說最後一段話 / 進 Q&A。

備用變體（預設不用）：
· C PM 直覺：「AI 學會了爬山。選哪座山、山頂長什麼樣，還是我們的工作。」
· A 戲劇張力：「瓶頸不會消失——它只會搬到你還沒看守的那道牆。」""")


# ============================================================
# BUILD
# ============================================================
def main():
    builders = [slide_01, slide_02, slide_03, slide_04, slide_05, slide_06,
                slide_07, slide_08, slide_09, slide_10, slide_11, slide_12,
                slide_13, slide_14, slide_15, slide_16, slide_17, slide_18,
                slide_19, slide_20, slide_21]
    for b in builders:
        b()
    prs.save(OUT)
    print(f"{len(prs.slides)} slides, "
          f"{prs.slide_width.inches:.2f}\" x {prs.slide_height.inches:.2f}\"")
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
