#!/usr/bin/env python3
"""v3: judge-fix build. Zones: masthead 0-84 · hero 84-440 · caption 440-584 ·
panels 584-848 · breadth 848-984 · gold footer strip 990-1024."""
from PIL import Image, ImageDraw, ImageFont
import glob, os

W = H = 1024
PAPER = (242, 236, 224)
ACCENT = (255, 84, 60)
GOLD = (255, 196, 0)
MUTED = (150, 160, 175)
CARD = (22, 28, 38)
BODY = (205, 212, 222)
DARK = (10, 13, 18)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def f(p, s): return ImageFont.truetype(p, s)
_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))

def fit(path, text, max_w, start):
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

def cover(im, tw, th, focus_y=0.5):
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im2 = im.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
    x = (im2.size[0] - tw) // 2
    y = int((im2.size[1] - th) * focus_y)
    return im2.crop((x, y, x + tw, y + th))

def find(pat):
    hits = sorted(glob.glob(pat))
    assert hits, pat
    return hits[0]

img = Image.new("RGB", (W, H), DARK)
d = ImageDraw.Draw(img)

# ---------- Masthead 0-84 ----------
d.rectangle([0, 0, W, 8], fill=ACCENT)
d.text((48, 18), "THE WORLD IN ONE IMAGE", font=f(SANS_B, 24), fill=(178, 186, 198))
d.text((W - 48, 20), "WIRE & AGENCY REPORTING", font=f(SANS, 20), fill=MUTED, anchor="ra")
d.text((48, 44), "MONDAY 23 NOVEMBER 2026", font=f(SERIF_B, 40), fill=PAPER)

# ---------- Hero 84-428 ----------
hero = cover(Image.open("hero_v3.png").convert("RGB"), W, 320, focus_y=0.62)
img.paste(hero, (0, 84))
d = ImageDraw.Draw(img)

# ---------- Caption 428-584 ----------
d.rectangle([0, 404, W, 560], fill=(8, 10, 14))
d.line([48, 404, W - 48, 404], fill=ACCENT, width=4)
d.text((48, 416), "LEAD  ·  STRAIT OF HORMUZ", font=f(SANS_B, 24), fill=ACCENT)
d.text((48, 442), "TANKERS IN FLAMES", font=f(SERIF_B, 52), fill=PAPER)
d.text((48, 502), "Three tankers struck; Iran says two more hit naval mines.", font=f(SANS, 26), fill=BODY)
d.text((48, 530), "Trump threatens Iranian vessels as attacks hit a wartime high.", font=f(SANS, 26), fill=BODY)

# ---------- Panels 584-848 ----------
panels = [
    (find("media-generation-panel-warship-v3-*.webp"), "WAR AT SEA", ["RUSSIAN WARSHIP", "DOWN AT BENGHAZI"]),
    (find("media-generation-panel-mercury-v3-*.webp"), "SPACE · ESA–JAXA", ["MERCURY,", "AT LAST"]),
    (find("media-generation-panel-lahore-*.webp"), "ENVIRONMENT", ["LAHORE CHOKES:", "AQI 538"]),
]
pw, ph, gap, x0, y0 = 320, 250, 16, 32, 560
for i, (path, kicker, heads) in enumerate(panels):
    x = x0 + i * (pw + gap)
    pim = cover(Image.open(path).convert("RGB"), pw, 110)
    img.paste(pim, (x, y0))
    d.rectangle([x, y0, x + pw, y0 + 110], outline=(90, 100, 115), width=2)
    d.rectangle([x, y0 + 110, x + pw, y0 + ph], fill=CARD)
    d.text((x + 16, y0 + 120), kicker, font=f(SANS_B, 21), fill=GOLD)
    hy = y0 + 148
    for hline in heads:
        hf = fit(SERIF_B, hline, pw - 32, 40)
        d.text((x + 16, hy), hline, font=hf, fill=PAPER)
        hy += 47

# ---------- Breadth 848-984 ----------
breadth_lines = [
    "ALSO TODAY:  COP31 climate talks collapse in Turkey, no deal",
    "Boy, 7, pulled alive from Kyiv rubble  ·  AI rout shakes Asian markets",
    "Democrats win largest US House majority since 1992",
]
d.line([48, 826, W - 48, 826], fill=(70, 80, 95), width=3)
ly = 842
for ln in breadth_lines:
    lf = fit(SANS_B, ln, W - 96, 27)
    d.text((48, ly), ln, font=lf, fill=BODY)
    ly += 42

# ---------- Gold footer strip 990-1024 ----------
d.rectangle([0, 990, W, H], fill=GOLD)
d.text((48, 998), "Facts from AP · BBC · Reuters · Al Jazeera · ESA · Dawn reporting — imagery is illustrative",
       font=f(SANS_B, 19), fill=(20, 20, 20))

img.save("entry_v4.png", optimize=True)
img.resize((300, 300), Image.LANCZOS).save("preview_v4_300.png")
print("v4 bytes:", os.path.getsize("entry_v4.png"))
