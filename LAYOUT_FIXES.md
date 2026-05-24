# Layout Fixes — AAR_Appendix_v1.pptx

All fixes are in `code/build_appendix.py`.

**Rebuild:** `poetry run python code/build_appendix.py`
**Verify:** open `ppt/AAR_Appendix_v1.pptx`, check the slides listed under each fix.

---

## Coordinate reference

All layout coordinates are percentages of the slide dimensions (13.333" × 7.5").

| Constant | % value | In inches |
|----------|---------|-----------|
| `STRIPE_H` | 0.833% | 0.0625" |
| `PAD_Y` | 2.593% | 0.194" — applied to **top and bottom** of content area |
| `PAD_X` | 1.875% | 0.250" |
| `panel()` total Y overhead | 6.019% | 0.451" — = `STRIPE_H + 2×PAD_Y` (stripe at top + padding above and below text) |
| `ax_footer()` top | 94.6% | 7.095" |
| Slide bottom | 100% | 7.500" |

`card()` adds a further `pt_h(title_size × 1.6)` on top of the `panel()` overhead for the title row.

---

## Fix 1 — Divider slide list overflow (dividers A, B, C, D, F)

**Function:** `_divider()` — search `def _divider`
**Slides:** 2 (A), 8 (B), 13 (C), 19 (D), 28 (F)

### Visual symptom
On 5-item dividers (A, C, F), the last row in the slide index is invisible — it renders below the slide boundary. On 4-item dividers (B, D), the last row's bottom edge touches or overlaps the footer label.

### Problem & fix
The loop used fixed `sy=56, sh=8, gap=2`, stepping 10% per item. Five items need 56 + 48 = **104%** — the 5th panel is entirely off-slide. Four items reach 94%, leaving only 0.045" before the footer.

The minimum safe `sh` is ~7.1%, because `panel()` overhead (6.019%) plus one line of rendered text (~3.6% from `iy`) requires the panel background to be at least `3.426 + 3.6 = 7.026%` tall.

```python
# Before:
sy, sh, gap = 56.0, 8.0, 2.0

# After:
n = len(slide_list)
if n == 5:
    sy, sh, gap = 49.0, 7.5, 1.0   # 49 + 5×7.5 + 4×1.0 = 90.5%
elif n == 4:
    sy, sh, gap = 54.0, 8.0, 2.0   # 54 + 4×8.0 + 3×2.0 = 92.0%
else:
    sy, sh, gap = 56.0, 8.0, 2.0   # 56 + 3×8.0 + 2×2.0 = 84.0%
```

### Result
Last panel bottom: 5-item → 6.593", 4-item → 6.706", 3-item → 6.106". All clear the footer (7.095") by ≥ 0.39". Verified by python-pptx geometry scan.

---

## Fix 2 — A2 card body height effectively zero (ih = 0.04")

**Function:** `slide_A2()` — search `def slide_A2`
**Slide:** 4 (A2)

### Visual symptom
The "關鍵設計決策 + 引用原句" card shows no body text, or text renders outside the card background rect and into the footer zone.

### Root cause
The card was positioned at `y=80, h=11`. The `card()` overhead alone (title at `T_H2=22pt` → `STRIPE_H + PAD_Y + pt_h(22×1.6) = 0.833 + 2.593 + 4.444 = 7.870%`) left only `11 − 7.870 = 3.13%` for the body `panel()`, whose own overhead (6.019%) exceeded it — body `ih ≈ 0.04"`. Three testbed panels above the card each had `sh=16`, so reducing them by 2% each freed `3 × 2 = 6%` of vertical space to reallocate.

### Fix
```python
# Before:
sy, sh, gap = 26.0, 16.0, 2.0          # three testbed panels, sh=16 each
...
card(sl, 4, 80, 92, 11, title="關鍵設計決策 + 引用原句", ...)

# After:
sy, sh, gap = 26.0, 14.0, 2.0          # each panel 2% shorter → 3×2 = 6% freed
...
card(sl, 4, 74, 92, 20, title="關鍵設計決策 + 引用原句", ...)   # moved up 6%, height 11→20
```

### Result
Card body frame: `top=6.14" h=0.72" bot=6.86"` — 0.23" clearance before footer. Verified by python-pptx geometry scan.

---

## Fix 3 — F3 OOD quote panel too short

**Function:** `slide_F3()` — search `def slide_F3`
**Slide:** 31 (F3)

### Visual symptom
The red OOD warning block's quote text renders below the panel's colored background rect, appearing to float on the slide background.

### Root cause
Panel had `h=26`. After `panel()` overhead (6.019%), the usable `ih = 19.981%`. The `text_lines()` call passed `ih − 15 = 4.981% = 0.374"` as its height, but the two-line quote plus one-line conclusion needed ~0.731" — text overflowed the panel background by ~0.36".

### Fix
```python
# Before:
ix, iy, iw, ih = panel(sl, 4, 64, 92, 26, stripe=ACC_BAD, fill=PANEL_BAD)

# After:
ix, iy, iw, ih = panel(sl, 4, 64, 92, 28, stripe=ACC_BAD, fill=PANEL_BAD)
```

### Result
Panel bottom moves from 6.75" to 6.90" (Y=92%). Text ends at ~6.763", 0.14" inside the panel. Verified by python-pptx geometry scan.

---

## Shared root cause — body text-box extends below panel background (Fixes 4–6)

**Applies to:** `slide_A4` (slide 6), `_method_slide` (slides 15–17), `slide_F5` (slide 33)

### Root cause
`panel()` returns `(ix, iy, iw, ih)`. The visual bottom of the colored background rect sits at `y + sh`, but `iy` is offset inward by `STRIPE_H + PAD_Y = 3.426%`. Any text element placed at `iy + offset` must stay within `(y + sh) - iy = sh - 3.426%` to remain inside the panel's colored rect.

All three affected functions computed body text-box height as `sh - constant` (e.g., `sh-6`, `sh-4.5`) without accounting for this 3.426% y-overhead. With the original `sh` values (9.5–10.5%), the resulting text boxes extended 2.4–3.1% below the panel background — text appeared to float on the dark slide background.

### Fix formula
For a text element starting at `iy + offset_y`, the maximum safe height is:
```
max_h = sh - 3.426 - offset_y - safety_margin
```
Where `safety_margin ≥ 0.2%` (≈ 1pt) is recommended.
To give meaningful body text space at the corrected heights, `sh` must also be increased.

---

## Fix 4 — A4 desc text overflow (slide 6)

**Function:** `slide_A4()` — search `def slide_A4`
**Slide:** 6 (A4)

### Visual symptom
The `desc` line in each of the 5 method panels renders below the panel's colored background rect, floating on the slide background.

### Root cause
`sh=10.0`. Panel visual area from `iy` = `10.0 − 3.426 = 6.574%`. The desc text was placed at `iy+5.2, h=4.5` → bottom at `iy+9.7` — **3.126% overflow**.

### Fix
```python
# Before:
sy, sh, gap = 28.0, 10.0, 1.5
text(sl, name, ix+6, iy+0.5, iw-6, 5,   ...)
text(sl, desc, ix+6, iy+5.2, iw-6, 4.5, ...)
ix, iy, iw, ih = panel(sl, 63, 28, 33, 56, ...)   # right panel y=28, h=56 → 84%

# After:
sy, sh, gap = 26.0, 13.0, 0.5   # 26 + 5×13 + 4×0.5 = 93%
# panel visual area from iy = 13 − 3.426 = 9.574%
text(sl, name, ix+6, iy+0.3, iw-6, 4.5, ...)      # bottom at iy+4.8 ✓
text(sl, desc, ix+6, iy+5.0, iw-6, 4.4, ...)      # bottom at iy+9.4 ≤ 9.574 ✓
ix, iy, iw, ih = panel(sl, 63, 26, 33, 67, ...)   # right panel aligned y=26, h=67 → 93%
```

### Result
All panel bottoms at 93.0%, desc text at iy+9.4. Clear of footer (94.6%) by 1.6%. Verified by python-pptx geometry scan.

---

## Fix 5 — _method_slide body text overflow (slides 15, 16, 17)

**Function:** `_method_slide()` — search `def _method_slide`
**Slides:** 15 (C2), 16 (C3), 17 (C4) — all use `len(steps) == 5`

### Visual symptom
The body text in each step panel renders below the panel's colored background rect.

### Root cause
`n=5`: `sh = (60.0/5) − 1.5 = 10.5`. Panel visual area from `iy` = `10.5 − 3.426 = 7.074%`. Body was placed at `iy+5, h=sh-6=4.5` → bottom at `iy+9.5` — **2.426% overflow**.

### Fix
```python
# Before:
sy, sh, gap = 22.0, (60.0 / max(len(steps), 1)) - 1.5, 1.5
# ...in loop:
text(sl, body, ix+6, iy+5, iw-6, sh-6, ...)      # sh-6=4.5, bottom at iy+9.5

# After:
n = max(len(steps), 1)
sh = 13.0 if n == 5 else (60.0 / n) - 1.5
sy, gap = 22.0, 1.5
# n=5: total = 22 + 5×13 + 4×1.5 = 93%
# panel visual area from iy = 13 − 3.426 = 9.574%
# ...in loop:
text(sl, body, ix+6, iy+5, iw-6, sh-8.6, ...)    # sh-8.6=4.4, bottom at iy+9.4 ≤ 9.574 ✓
```

### Result
All step panel bottoms at 93.0%, body text at iy+9.4. Clear of footer by 1.6%. Verified by python-pptx geometry scan.

---

## Fix 6 — F5 caveat body text overflow (slide 33)

**Function:** `slide_F5()` — search `def slide_F5`
**Slide:** 33 (F5)

### Visual symptom
Body text in each of the 6 caveat panels renders below the panel's colored background rect.

### Root cause
`sh=9.5`. Panel visual area from `iy` = `9.5 − 3.426 = 6.074%`. Body was placed at `iy+4.2, h=sh-4.5=5.0` → bottom at `iy+9.2` — **3.126% overflow**.

### Fix
```python
# Before:
sy, sh, gap = 30.0, 9.5, 1.0
text(sl, body, ix, iy+4.2, iw, sh-4.5, ...)      # sh-4.5=5.0, bottom at iy+9.2

# After:
sy, sh, gap = 25.0, 11.0, 0.5   # 25 + 6×11 + 5×0.5 = 93.5%
# panel visual area from iy = 11 − 3.426 = 7.574%
text(sl, body, ix, iy+4.2, iw, sh-7.9, ...)      # sh-7.9=3.1, bottom at iy+7.3 ≤ 7.574 ✓
```

### Result
All caveat panel bottoms at 93.5%, body text at iy+7.3. Clear of footer by 1.1%. Verified by python-pptx geometry scan.

⚠ **Note:** With `sh=11`, body height = 3.1% ≈ 0.23" ≈ 1.2 lines of 11pt text. Caveats with multi-sentence bodies (caveats 1, 5, 6) will be clipped after ~1 line. To show full text: shorten those bodies to one punchy sentence each, or reduce body font from `T_BODY_SM-1 = 11pt` to `T_CAPTION = 10pt`.
