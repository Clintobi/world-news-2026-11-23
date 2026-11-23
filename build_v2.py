#!/usr/bin/env python3
"""v2 poster: hero visual + 3 pictured panels + breadth bar. Native 1024x1024."""
from PIL import Image, ImageDraw, ImageFont
import glob

W = H = 1024
BG = (10, 13, 18)
PAPER = (242, 236, 224)
ACCENT = (255, 84, 60)
GOLD = (255, 196, 0)
MUTED = (150, 160, 175)
CARD = (22, 28, 38)
BODY = (198, 206, 216)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def f(p, s): return ImageFont.truetype(p, s)

_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))

def fit(path, text, max_w, start):
    """Largest font size <= start that fits text in max_w."""
    s = start
    while s > 10:
        if _probe.textlength(text, font=f(path, s)) <= max_w:
            return f(path, s)
        s -= 1
    return f(path, s)

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def cover(im, tw, th):
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im2 = im.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
    x = (im2.size[0] - tw) // 2
    y = (im2.size[1] - th) // 2
    return im2.crop((x, y, x + tw, y + th))

def find(pat):
    hits = sorted(glob.glob(pat))
    assert hits, pat
    return hits[0]

img = Image.new("RGB", (W, H), BG)

# ---------- Masthead (0-116) ----------
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 8], fill=ACCENT)
d.text((48, 22), "THE WORLD IN ONE IMAGE", font=f(SANS_B, 27), fill=MUTED)
d.text((48, 52), "MONDAY 23 NOVEMBER 2026", font=f(SERIF_B, 47), fill=PAPER)
d.line([48, 112, W - 48, 112], fill=ACCENT, width=4)

# ---------- Hero (120-566) ----------
hero = cover(Image.open("hero_hormuz.png").convert("RGB"), W, 446)
img.paste(hero, (0, 120))
img.paste(Image.new("RGB", (W, 158), (8, 10, 14)), (0, 408))
d = ImageDraw.Draw(img)
d.rectangle([0, 408, 10, 566], fill=ACCENT)
d.text((44, 418), "LEAD  ·  STRAIT OF HORMUZ", font=f(SANS_B, 25), fill=ACCENT)
d.text((44, 446), "TANKERS IN FLAMES", font=f(SERIF_B, 54), fill=PAPER)
d.text((44, 510), "Three tankers struck; Iran says two more hit naval mines.", font=f(SANS, 24), fill=(205, 212, 222))
d.text((44, 538), "Attacks on shipping at their highest since the war began.", font=f(SANS, 24), fill=(205, 212, 222))

# ---------- Panels (582-884) ----------
panels = [
    (find("media-generation-panel-warship-*.webp"), "WAR AT SEA", ["RUSSIAN WARSHIP", "SUNK AT BENGHAZI"],
     "Suspected Ukrainian sea drones hit the Merkury."),
    (find("media-generation-panel-mercury-*.webp"), "SPACE", ["MERCURY,", "AT LAST"],
     "BepiColombo arrives after an 8-year voyage."),
    (find("media-generation-panel-lahore-*.webp"), "ENVIRONMENT", ["LAHORE CHOKES:", "AQI 538"],
     "World's most polluted major city Sunday morning."),
]
pw, ph, gap, x0, y0 = 320, 292, 16, 32, 582
for i, (path, kicker, heads, body) in enumerate(panels):
    x = x0 + i * (pw + gap)
    img.paste(cover(Image.open(path).convert("RGB"), pw, 140), (x, y0))
    d.rectangle([x, y0 + 140, x + pw, y0 + ph], fill=CARD)
    d.text((x + 16, y0 + 150), kicker, font=f(SANS_B, 20), fill=GOLD)
    hy = y0 + 178
    for hline in heads:
        hf = fit(SERIF_B, hline, pw - 32, 31)
        d.text((x + 16, hy), hline, font=hf, fill=PAPER)
        hy += 38
    by = hy + 6
    bf = f(SANS, 20)
    for ln in wrap(d, body, bf, pw - 32)[:2]:
        d.text((x + 16, by), ln, font=bf, fill=BODY)
        by += 26

# ---------- Breadth bar (898-980) ----------
d.line([48, 902, W - 48, 902], fill=(70, 80, 95), width=3)
breadth = ("ALSO TODAY:  COP31 collapses, no deal  ·  Boy, 7, pulled alive near Kyiv  ·  "
           "Democrats win biggest US House majority since 1992  ·  Drones hit UN in Khartoum")
bf = f(SANS_B, 22)
ly = 914
for ln in wrap(d, breadth, bf, W - 96)[:3]:
    d.text((48, ly), ln, font=bf, fill=(205, 212, 222))
    ly += 30

# ---------- Footer ----------
d.text((W - 48, 26), "AP · BBC · REUTERS · AL JAZEERA · NYT", font=f(SANS, 19), fill=MUTED, anchor="ra")
d.text((48, 994), "Imagery is illustrative · Facts from wire reporting, 23 Nov 2026",
       font=f(SANS, 17), fill=MUTED)
d.rectangle([0, H - 8, W, H], fill=GOLD)

img.save("entry_v2.png", optimize=True)
img.resize((300, 300), Image.LANCZOS).save("preview_v2_300.png")
import os
print("v2 bytes:", os.path.getsize("entry_v2.png"))
