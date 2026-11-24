#!/usr/bin/env python3
"""Draw the news-image-20261123 front page: 'The Daily Ledger', Monday 23 Nov 2026.
Deterministic: same input -> byte-identical PNG."""
import json
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (22, 22, 22)
RED = (163, 18, 18)
GREEN = (18, 110, 45)
GREY = (96, 90, 80)
RULE = (60, 55, 45)
DARK = (24, 24, 28)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill, max_w=None):
    if max_w is not None:
        lines = wrap(draw, text, fnt, max_w)
        for ln in lines:
            draw.text(((W - draw.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=fill)
            y += int(fnt.size * 1.12)
        return y
    draw.text(((W - draw.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.12)


def main():
    with open("stories.json") as f:
        s = json.load(f)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 4], fill=INK)
    d.text(((W - d.textlength(s["masthead"], font=font(SERIF, 62))) / 2, 18),
           s["masthead"], font=font(SERIF, 62), fill=INK)
    d.line([(28, 96), (996, 96)], fill=RULE, width=2)
    d.text((28, 104), s["date"].upper(), font=font(SANS_B, 17), fill=INK)
    right = "VOL. VIII — No. 328  ·  PRICE: ONE IMAGE"
    d.text((W - 28 - d.textlength(right, font=font(SANS_B, 17)), 104),
           right, font=font(SANS_B, 17), fill=INK)
    d.line([(28, 130), (996, 130)], fill=RULE, width=1)

    # ---- Hero ----
    y = 138
    y = draw_centered(d, y, s["hero"]["kicker"], font(SANS_B, 19), RED)
    y = draw_centered(d, y, s["hero"]["headline"], font(SERIF, 48), INK, max_w=960)
    y += 4
    deck_lines = wrap(d, s["hero"]["deck"], font(SERIF_R, 20), 920)
    for ln in deck_lines:
        d.text(((W - d.textlength(ln, font=font(SERIF_R, 20))) / 2, y), ln,
               font=font(SERIF_R, 20), fill=(52, 48, 42))
        y += 25
    y += 6
    d.line([(28, y), (996, y)], fill=RULE, width=1)
    y += 8

    # ---- Numbers band ----
    band_y = y
    bw, gap = 316, 12
    for i, n in enumerate(s["numbers"]):
        x = 28 + i * (bw + gap)
        d.rectangle([x, band_y, x + bw, band_y + 56], outline=RULE, width=1)
        d.text((x + 14, band_y + 6), n["label"], font=font(SANS_B, 14), fill=GREY)
        d.text((x + 14, band_y + 23), n["value"], font=font(SANS_B, 26), fill=GREEN)
        note = n["note"]
        d.text((x + bw - 14 - d.textlength(note, font=font(SANS, 14)), band_y + 30),
               note, font=font(SANS, 14), fill=GREY)
    y = band_y + 56 + 10
    d.line([(28, y), (996, y)], fill=RULE, width=1)
    y += 10

    # ---- 4 tiles ----
    tw, tgap = 236, 10
    tile_y = y
    tile_h = 180
    for i, t in enumerate(s["tiles"]):
        x = 28 + i * (tw + tgap)
        d.rectangle([x, tile_y, x + tw, tile_y + tile_h], outline=RULE, width=1)
        d.text((x + 10, tile_y + 9), t["tag"], font=font(SANS_B, 13), fill=RED)
        ty = tile_y + 31
        for ln in wrap(d, t["headline"], font(SERIF, 18), tw - 20):
            d.text((x + 10, ty), ln, font=font(SERIF, 18), fill=INK)
            ty += 23
        ty += 3
        for ln in wrap(d, t["body"], font(SANS, 13), tw - 20):
            d.text((x + 10, ty), ln, font=font(SANS, 13), fill=(52, 48, 42))
            ty += 17
    y = tile_y + tile_h + 10

    # ---- Wide tile ----
    wt = s["wide_tile"]
    d.rectangle([28, y, 996, y + 76], outline=RULE, width=1)
    d.text((44, y + 8), wt["tag"], font=font(SANS_B, 13), fill=RED)
    d.text((44, y + 26), wt["headline"], font=font(SERIF, 21), fill=INK)
    for ln in wrap(d, wt["body"], font(SANS, 13), 940):
        d.text((44, y + 52), ln, font=font(SANS, 13), fill=(52, 48, 42))
        break
    y += 76 + 10
    d.line([(28, y), (996, y)], fill=RULE, width=1)
    y += 8

    # ---- IN BRIEF ----
    d.text((28, y), "IN BRIEF", font=font(SANS_B, 16), fill=RED)
    y += 24
    brief_y = y
    col_w = 472
    for i, b in enumerate(s["in_brief"]):
        col = i % 2
        row = i // 2
        bx = 28 + col * (col_w + 24)
        by = brief_y + row * 48
        d.text((bx, by), "• " + b["tag"] + " — ", font=font(SANS_B, 13), fill=INK)
        tag_w = d.textlength("• " + b["tag"] + " — ", font=font(SANS_B, 13))
        lines = wrap(d, b["text"], font(SANS, 13), col_w - tag_w)
        d.text((bx + tag_w, by), lines[0], font=font(SANS, 13), fill=(52, 48, 42))
        for j, ln in enumerate(lines[1:]):
            d.text((bx, by + 17 * (j + 1)), ln, font=font(SANS, 13), fill=(52, 48, 42))
    y = brief_y + 3 * 48 + 6
    d.line([(28, y), (996, y)], fill=RULE, width=1)
    y += 8

    # ---- Markets strip ----
    d.rectangle([28, y, 996, y + 86], fill=DARK)
    d.text((44, y + 8), "MONDAY'S CLOSES — 23 NOV", font=font(SANS_B, 15), fill=(220, 214, 200))
    d.text((996 - 44 - d.textlength("NIKKEI: FRIDAY'S CLOSE (HOLIDAY)", font=font(SANS, 13)), y + 10),
           "NIKKEI: FRIDAY'S CLOSE (HOLIDAY)", font=font(SANS, 13), fill=(180, 172, 158))
    cw = (996 - 28 - 32) / 4
    for i, m in enumerate(s["markets"]):
        col, row = i % 4, i // 4
        mx = 44 + col * cw
        my = y + 31 + row * 26
        d.text((mx, my), m["label"], font=font(SANS_B, 14), fill=(220, 214, 200))
        val = f"{m['value']}  {m['chg']}"
        vx = mx + d.textlength(m["label"], font=font(SANS_B, 14)) + 10
        d.text((vx, my), val, font=font(SANS, 14),
               fill=(120, 220, 140) if m["chg"].startswith("+") else (240, 120, 110))
    y += 86 + 8

    # ---- Footer ----
    d.text((28, y + 2), s["footer"], font=font(SANS, 12), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
