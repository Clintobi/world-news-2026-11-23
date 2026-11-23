#!/usr/bin/env python3
"""FINAL: cinematic cover top + elegant editorial band.
Hero (full-bleed) carries craft + lead; band carries pictured stories in
large type + a breadth line. No boxes, no red slabs — hairlines and serif."""
from PIL import Image, ImageDraw, ImageFont
import glob, os

W = H = 1024
INK = (9, 12, 17)
CREAM = (243, 238, 228)
SOFT = (216, 221, 228)
GOLD = (232, 197, 116)
MUTE = (160, 167, 178)
HAIR = (86, 94, 106)

LSERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
LSERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
LSANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
LSANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def f(p, s): return ImageFont.truetype(p, s)
_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))

def cover(im, tw, th, focus_y=0.5):
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im2 = im.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
    x = (im2.size[0] - tw) // 2
    y = int((im2.size[1] - th) * focus_y)
    return im2.crop((x, y, x + tw, y + th))

def spaced(draw, cx, y, text, font, tracking, fill):
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += wch + tracking
    return total

def spaced_fit(draw, cx, y, text, path, size, tracking, fill, max_w):
    s = size
    while s > 10:
        font = f(path, s)
        if sum(draw.textlength(ch, font=font) for ch in text) + tracking * (len(text) - 1) <= max_w:
            break
        s -= 1
    return spaced(draw, cx, y, text, f(path, s), tracking, fill)

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

def find(pat):
    hits = sorted(glob.glob(pat))
    assert hits, pat
    return hits[0]

# ---------- Hero 0-606 ----------
img = cover(Image.open("hero_v3.png").convert("RGB"), W, 606, focus_y=0.58)
# scrims: top for masthead, bottom for cover lines
ov = Image.new("L", (1, 606), 0)
for yy in range(606):
    if yy < 210:
        a = int(200 * (1 - yy / 210))
    elif yy > 330:
        a = int(242 * ((yy - 330) / 276) ** 1.3)
    else:
        a = 0
    ov.putpixel((0, yy), a)
ov = ov.resize((W, 606))
black = Image.new("RGB", (W, 606), (4, 6, 10))
img = Image.composite(black, img, ov)

canvas = Image.new("RGB", (W, H), INK)
canvas.paste(img, (0, 0))
d = ImageDraw.Draw(canvas)
cx = W // 2

spaced(d, cx, 34, "THE WORLD IN ONE IMAGE", f(LSANS, 22), 7, CREAM)
d.line([cx - 140, 76, cx + 140, 76], fill=GOLD, width=2)
spaced(d, cx, 90, "MONDAY 23 NOVEMBER 2026", f(LSANS_B, 25), 5, CREAM)

spaced(d, cx, 408, "THE STRAIT OF HORMUZ", f(LSANS_B, 23), 8, GOLD)
d.text((cx, 438), "Tankers in Flames", font=f(LSERIF_B, 88), fill=CREAM, anchor="ma")
d.text((cx, 540), "Three tankers struck; Iran says two more hit naval mines.", font=f(LSERIF_I, 26), fill=SOFT, anchor="ma")
d.text((cx, 572), "Trump threatens Iranian vessels as attacks hit a wartime high.", font=f(LSERIF_I, 26), fill=SOFT, anchor="ma")

# ---------- Editorial band 606-1024 ----------
cols = [
    (find("media-generation-panel-warship-v3-*.webp"), "WAR AT SEA", ["RUSSIAN WARSHIP", "DOWN AT BENGHAZI"],
     "Suspected sea drones hit the Merkury; 10 injured."),
    (find("media-generation-panel-mercury-v3-*.webp"), "SPACE · ESA–JAXA", ["MERCURY,", "AT LAST"],
     "BepiColombo enters orbit — 2nd mission ever."),
    (find("media-generation-panel-lahore-*.webp"), "ENVIRONMENT", ["LAHORE CHOKES:", "AQI 538"],
     "World's most polluted city on Sunday morning."),
]
cw, gap, x0, y0 = 293, 24, 48, 630
for i, (path, kicker, heads, sub) in enumerate(cols):
    x = x0 + i * (cw + gap)
    if i > 0:
        d.line([x - gap // 2, y0, x - gap // 2, y0 + 268], fill=HAIR, width=1)
    canvas.paste(cover(Image.open(path).convert("RGB"), cw, 124), (x, y0))
    d = ImageDraw.Draw(canvas)
    d.text((x, y0 + 138), kicker, font=f(LSANS_B, 19), fill=GOLD)
    hy = y0 + 164
    for hline in heads:
        hf = fit(LSERIF_B, hline, cw, 33)
        d.text((x, hy), hline, font=hf, fill=CREAM)
        hy += 40
    sy = hy + 6
    sf = f(LSANS, 21)
    for ln in wrap(d, sub, sf, cw)[:2]:
        d.text((x, sy), ln, font=sf, fill=SOFT)
        sy += 28

# ---------- Breadth line ----------
d.line([48, 928, W - 48, 928], fill=HAIR, width=1)
spaced_fit(d, cx, 944,
           "ALSO TODAY  ·  COP31 COLLAPSES IN TURKEY  ·  BOY, 7, PULLED ALIVE NEAR KYIV  ·  DEMOCRATS' LARGEST HOUSE MAJORITY SINCE 1992  ·  AI ROUT IN ASIA",
           LSANS_B, 20, 1, CREAM, W - 80)
spaced(d, cx, 984, "AP · BBC · REUTERS · AL JAZEERA · ESA · DAWN — IMAGERY IS ILLUSTRATIVE", f(LSANS, 14), 2, MUTE)

canvas.save("entry_final.png", optimize=True)
canvas.resize((300, 300), Image.LANCZOS).save("preview_final_300.png")
canvas.save("entry_final.jpg", quality=88, optimize=True)
print("png bytes:", os.path.getsize("entry_final.png"), "| jpg bytes:", os.path.getsize("entry_final.jpg"))
