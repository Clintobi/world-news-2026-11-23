#!/usr/bin/env python3
"""Cinematic full-bleed cover: hero image is the page, minimal elegant type."""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
CREAM = (243, 238, 228)
SOFT = (214, 219, 226)
GOLD = (232, 197, 116)
MUTE = (168, 175, 186)

LSERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
LSERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
LSERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
LSANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
LSANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def f(p, s): return ImageFont.truetype(p, s)

def cover(im, tw, th, focus_y=0.55):
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im2 = im.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
    x = (im2.size[0] - tw) // 2
    y = int((im2.size[1] - th) * focus_y)
    return im2.crop((x, y, x + tw, y + th))

def spaced(draw, cx, y, text, font, tracking, fill):
    """Draw letterspaced text centred at cx. Returns total width."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += wch + tracking
    return total

def gradient_scrim(img, top_h, bot_from):
    """Black gradient at top (for masthead) and bottom (for cover lines)."""
    ov = Image.new("L", (1, H), 0)
    px = ov.load()
    for yy in range(H):
        if yy < top_h:
            a = int(205 * (1 - yy / top_h))
        elif yy > bot_from:
            a = int(238 * ((yy - bot_from) / (H - bot_from)) ** 1.25)
        else:
            a = 0
        px[0, yy] = a
    ov = ov.resize((W, H))
    black = Image.new("RGB", (W, H), (4, 6, 10))
    img.paste(Image.composite(black, img, ov), (0, 0))
    return img

img = cover(Image.open("hero_v3.png").convert("RGB"), W, H, focus_y=0.52)
img = gradient_scrim(img, 250, 430)
d = ImageDraw.Draw(img)
cx = W // 2

# ---- Masthead ----
spaced(d, cx, 40, "THE WORLD IN ONE IMAGE", f(LSANS, 23), 7, CREAM)
d.line([cx - 150, 84, cx + 150, 84], fill=GOLD, width=2)
spaced(d, cx, 98, "MONDAY 23 NOVEMBER 2026", f(LSANS_B, 25), 5, CREAM)

# ---- Cover lines (bottom) ----
spaced(d, cx, 648, "THE STRAIT OF HORMUZ", f(LSANS_B, 24), 8, GOLD)
d.text((cx, 686), "Tankers in Flames", font=f(LSERIF_B, 96), fill=CREAM, anchor="ma")
support = "Three tankers struck; Iran says two more hit naval mines."
support2 = "Trump threatens Iranian vessels as attacks hit a wartime high."
d.text((cx, 806), support, font=f(LSERIF_I, 28), fill=SOFT, anchor="ma")
d.text((cx, 842), support2, font=f(LSERIF_I, 28), fill=SOFT, anchor="ma")

d.line([cx - 330, 902, cx + 330, 902], fill=(190, 196, 205), width=1)

def spaced_fit(draw, cx, y, text, path, size, tracking, fill, max_w=W - 72):
    s = size
    while s > 10:
        font = f(path, s)
        total = sum(draw.textlength(ch, font=font) for ch in text) + tracking * (len(text) - 1)
        if total <= max_w:
            break
        s -= 1
    spaced(draw, cx, y, text, f(path, s), tracking, fill)

spaced_fit(d, cx, 918, "COP31 COLLAPSES  ·  WARSHIP DOWN AT BENGHAZI  ·  MERCURY, AT LAST", LSANS, 20, 2, CREAM)
spaced_fit(d, cx, 948, "LAHORE: AQI 538  ·  BOY, 7, PULLED ALIVE  ·  DEMOCRATS' HOUSE SURGE  ·  AI ROUT IN ASIA", LSANS, 20, 2, CREAM)
spaced(d, cx, 986, "AP · BBC · REUTERS · AL JAZEERA · ESA · DAWN — IMAGERY IS ILLUSTRATIVE", f(LSANS, 15), 2, MUTE)

img.save("entry_cover.png", optimize=True)
img.resize((300, 300), Image.LANCZOS).save("preview_cover_300.png")
print("cover bytes:", os.path.getsize("entry_cover.png"))
