from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "launch" / "ARTIFICIAL_STUPIDITY_LINKEDIN_CARD.png"
W, H = 1600, 900
NAVY = "#13263A"
PANEL = "#1D354B"
IVORY = "#F7F4ED"
GREEN = "#43C59E"
AMBER = "#F0B35A"
MUTED = "#B9C8D4"


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def centered(draw, box, text, fnt, fill):
    x1, y1, x2, y2 = box
    b = draw.textbbox((0, 0), text, font=fnt)
    draw.text(((x1+x2-(b[2]-b[0]))/2, (y1+y2-(b[3]-b[1]))/2-b[1]), text, font=fnt, fill=fill)


img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
d.rectangle((0, 0, W, 18), fill=GREEN)
d.text((90, 62), "ARTIFICIAL STUPIDITY", font=font(64, True), fill=IVORY)
d.rectangle((92, 145, 345, 153), fill=GREEN)
d.text((90, 177), "The machine improved the score. It still could not approve itself.", font=font(30), fill=MUTED)

stages = [
    ("INTELLIGENCE", "PROPOSES"),
    ("ARTIFICIAL\nSTUPIDITY", "CHALLENGES"),
    ("EVIDENCE", "ADJUDICATES"),
    ("HUMAN", "AUTHORIZES"),
]
sx, sy, bw, bh, gap = 90, 280, 315, 130, 46
for idx, (top, bottom) in enumerate(stages):
    x = sx + idx * (bw + gap)
    d.rounded_rectangle((x, sy, x+bw, sy+bh), radius=16, fill=PANEL, outline=GREEN if idx in (1,2) else "#45637A", width=3)
    lines = top.split("\n")
    y = sy + 25 if len(lines) == 1 else sy + 12
    for line in lines:
        centered(d, (x, y, x+bw, y+34), line, font(25, True), IVORY)
        y += 29
    centered(d, (x, sy+86, x+bw, sy+119), bottom, font(17, True), GREEN)
    if idx < 3:
        ax = x+bw+8
        ay = sy+bh/2
        d.line((ax, ay, ax+28, ay), fill=AMBER, width=5)
        d.polygon([(ax+28, ay), (ax+16, ay-8), (ax+16, ay+8)], fill=AMBER)

metrics = [
    ("VALIDATION", "+0.928%"),
    ("HOLDOUT", "+0.924%"),
    ("PAIRWISE WINS", "9/9 + 9/9"),
]
my = 485
mw = 335
for idx, (label, value) in enumerate(metrics):
    x = 90 + idx * (mw + 34)
    d.rounded_rectangle((x, my, x+mw, my+165), radius=14, fill=IVORY)
    centered(d, (x, my+28, x+mw, my+72), value, font(40, True), NAVY)
    centered(d, (x, my+93, x+mw, my+128), label, font(18, True), "#4B6172")
    centered(d, (x, my+128, x+mw, my+153), "LOWER BPB IS BETTER" if idx < 2 else "NO SCORE OVERLAP", font(13), "#6F7E88")

x = 1200
d.rounded_rectangle((x, my, 1510, my+72), radius=14, fill=AMBER)
centered(d, (x, my, 1510, my+72), "MACHINE: ESCALATE", font(22, True), NAVY)
d.rounded_rectangle((x, my+92, 1510, my+165), radius=14, fill=GREEN)
centered(d, (x, my+92, 1510, my+165), "HUMAN: KEEP", font(24, True), NAVY)

d.line((90, 716, 1510, 716), fill="#45637A", width=2)
d.text((90, 748), "A MONAHINGA™ EVIDENCE PROJECT", font=font(25, True), fill=IVORY)
d.text((90, 795), "Bounded six-run H100 result - not a general AI-safety certification.", font=font(20), fill=MUTED)
d.text((1510, 817), "SEPTEMBER 2026", font=font(16, True), fill=GREEN, anchor="ra")

img.save(OUT, quality=96)
print(OUT)
