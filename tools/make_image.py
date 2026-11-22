#!/usr/bin/env python3
"""Draw a magazine-style cover poster for 21 November 2026 world news.

No network access, no downloaded images or fonts. Everything is drawn
with PIL using system DejaVu fonts. Deterministic: same input always
produces byte-identical output.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

NAVY = (10, 30, 60)
RED = (200, 16, 46)
GOLD = (217, 164, 65)
CREAM = (251, 246, 236)
PAPER = (255, 255, 255)
INK = (17, 17, 17)
GREY = (88, 94, 102)
ROW_ALT = (244, 241, 234)
RULE = (203, 206, 211)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- Masthead band ----------
    d.rectangle([0, 0, W, 196], fill=NAVY)
    d.rectangle([0, 196, W, 202], fill=RED)
    d.rectangle([0, 202, W, 206], fill=GOLD)

    masthead = "THE WORLD TODAY"
    mf = SERIF_B(72)
    mw = d.textlength(masthead, font=mf)
    d.text(((W - mw) / 2, 26), masthead, font=mf, fill=PAPER)
    d.text((40, 138), "SATURDAY 21 NOVEMBER 2026", font=SANS_B(27), fill=GOLD)
    issue = "ISSUE No. 47  \u2022  SIX STORIES  \u2022  ONE DAY"
    iw = d.textlength(issue, font=SANS(22))
    d.text((W - 40 - iw, 140), issue, font=SANS(22), fill=(200, 210, 225))

    # ---------- Hero cover story ----------
    hx, hy, hw = 40, 224, W - 80
    hero_h = 268
    d.rectangle([hx, hy, hx + hw, hy + hero_h], fill=CREAM,
                outline=NAVY, width=2)
    d.rectangle([hx, hy, hx + 14, hy + hero_h], fill=RED)

    d.text((hx + 34, hy + 16), "COVER STORY  \u2022  MEXICO",
           font=SANS_B(24), fill=RED)
    head_f = SERIF_B(58)
    y = draw_lines(d, hx + 34, hy + 50,
                   ["MEXICO CAPTURES", "\u2018EL CHAPO ISIDRO\u2019"],
                   head_f, NAVY, 66)
    sub_f = SERIF(25)
    sub = ("Mexican forces seize Fausto Isidro Meza Flores, one of the "
           "FBI\u2019s 10 most wanted, in Guasave, Sinaloa \u2014 with help "
           "from US intelligence.")
    sub_lines = wrap(d, sub, sub_f, hw - 68)
    assert len(sub_lines) <= 2, sub_lines
    draw_lines(d, hx + 34, y + 10, sub_lines, sub_f, INK, 32)

    # ---------- Five more stories ----------
    stories = [
        ("CLIMATE", (27, 122, 77),
         "CLIMATE TALKS RUN INTO OVERTIME",
         "COP31 in Antalya drags past its deadline with no deal yet "
         "\u2014 and fossil fuels missing from the draft."),
        ("UKRAINE", (31, 78, 121),
         "MISSILES HIT ZELENSKYY\u2019S HOMETOWN",
         "Russian ballistic missiles strike Kryvyi Rih in a double-tap "
         "attack: 2 killed, 60 wounded. Missiles and a drone also crashed "
         "in Poland."),
        ("IRAN", (140, 32, 40),
         "TRUMP WEIGHS NEW STRIKES ON IRAN",
         "The US president weighs new strikes as Israel presses for "
         "action, US and Israeli officials say."),
        ("MARKETS", (91, 45, 142),
         "MARKETS PLUNGE AS NASDAQ SINKS 5.28%",
         "Friday\u2019s rout wipes out the Nasdaq\u2019s 2026 gains \u2014 down "
         "2.7% for the year. The S&P 500 falls 3.7%, the Dow 1.9%; "
         "Nvidia drops 14%."),
        ("FRANCE", (24, 52, 92),
         "FRANCE PROTESTS DRAW SMALLER CROWDS",
         "Largely peaceful cost-of-living and student protests: 82,500 "
         "people nationwide, 21,500 in Paris."),
    ]

    top = 508
    row_h = 88
    sum_f = SANS(19)
    head2_f = SANS_B(26)
    kick_f = SANS_B(20)
    for i, (kicker, color, headline, summary) in enumerate(stories):
        y0 = top + i * row_h
        if i % 2 == 1:
            d.rectangle([40, y0, W - 40, y0 + row_h - 6], fill=ROW_ALT)
        kx = 56
        d.text((kx, y0 + 6), kicker, font=kick_f, fill=color)
        kw = d.textlength(kicker, font=kick_f)
        d.text((kx + kw + 14, y0 + 6), headline, font=head2_f, fill=INK)
        sum_lines = wrap(d, summary, sum_f, W - 112)
        assert len(sum_lines) <= 2, sum_lines
        draw_lines(d, kx, y0 + 38, sum_lines, sum_f, GREY, 22)
        if i < len(stories) - 1:
            d.line([40, y0 + row_h - 6, W - 40, y0 + row_h - 6],
                   fill=RULE, width=1)

    # ---------- Footer ----------
    fy = 952
    d.rectangle([0, fy, W, H], fill=NAVY)
    d.rectangle([0, fy, W, fy + 4], fill=RED)
    foot = ("SATURDAY 21 NOVEMBER 2026  \u2022  SIX STORIES FROM "
            "AROUND THE GLOBE")
    ff = SANS_B(18)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, fy + 26), foot, font=ff, fill=PAPER)

    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
