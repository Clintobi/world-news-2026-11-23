#!/usr/bin/env python3
"""
make.fun bounty entry: "Sum up 23 November's world news in one image."
This program writes ONE image summarising the day's world news.
Headlines gathered 23 Nov 2026 (WAT) from AP, BBC, Reuters, Al Jazeera,
NYT, The Guardian, Dawn/IQAir, ESA reporting and USGS data.
Output: world_news_2026-11-23.png (1600 x 1600)
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1600
BG = (13, 17, 23)          # near-black blue
PAPER = (240, 234, 222)    # warm off-white
ACCENT = (255, 84, 60)     # signal red-orange
GOLD = (255, 196, 0)
MUTED = (150, 160, 175)
CARD = (24, 30, 40)
LINE = (70, 80, 95)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- Masthead ----
d.rectangle([0, 0, W, 12], fill=ACCENT)
d.text((80, 48), "THE WORLD IN ONE IMAGE", font=f(SERIF_B, 92), fill=PAPER)
d.text((82, 160), "MONDAY 23 NOVEMBER 2026  ·  THE DAY AT A GLANCE", font=f(SANS_B, 34), fill=GOLD)
d.line([80, 224, W - 80, 224], fill=LINE, width=3)

# ---- Lead story ----
d.rectangle([80, 252, W - 80, 560], fill=CARD)
d.rectangle([80, 252, 96, 560], fill=ACCENT)
d.text((130, 276), "LEAD  ·  STRAIT OF HORMUZ", font=f(SANS_B, 30), fill=ACCENT)
d.text((130, 318), "TANKERS IN FLAMES", font=f(SERIF_B, 74), fill=PAPER)
lead = [
    "At least three oil tankers struck in and near the strait;",
    "two more caught fire after hitting naval mines, Iran says.",
    "Attacks on shipping at their highest since the war began.",
]
y = 412
for line in lead:
    d.text((130, y), line, font=f(SANS, 33), fill=(205, 212, 222))
    y += 46
d.text((W - 130, 280), "AP · CNN-UKMTO · IRNA", font=f(SANS, 24), fill=MUTED, anchor="ra")

# ---- Story grid (2 columns x 3 rows) ----
stories = [
    ("CLIMATE", "COP31 TALKS COLLAPSE",
     "Longest-ever UN climate talks end in Turkey with no deal, as fossil-fuel divisions split the summit.", "BBC · NYT"),
    ("WAR AT SEA", "RUSSIAN WARSHIP SUNK",
     "Suspected Ukrainian sea drones hit the corvette Merkury at Benghazi; the ship capsized, 10 injured.", "AP · REUTERS"),
    ("UKRAINE", "BOY, 7, PULLED ALIVE",
     "Rescuers free a child from rubble hours after a Russian strike flattened a block near Kyiv.", "BBC · AL JAZEERA"),
    ("US POLITICS", "DEMOCRATS' HOUSE SURGE",
     "Flipping a North Carolina seat gives Democrats their largest House majority since 1992.", "BBC"),
    ("SPACE", "MERCURY, AT LAST",
     "Europe & Japan's BepiColombo enters Mercury orbit after an 8-year voyage - only the 2nd mission ever.", "ESA"),
    ("ENVIRONMENT", "LAHORE CHOKES: AQI 538",
     "Pakistan's Lahore is again the world's most polluted major city on Sunday morning.", "IQAir · DAWN"),
]
gx, gy = 80, 592
cw, ch = 712, 218
for i, (kicker, head, body, src) in enumerate(stories):
    x = gx + (i % 2) * (cw + 16)
    yy = gy + (i // 2) * (ch + 16)
    d.rectangle([x, yy, x + cw, yy + ch], fill=CARD)
    d.text((x + 24, yy + 18), kicker, font=f(SANS_B, 24), fill=GOLD)
    d.text((x + 24, yy + 52), head, font=f(SERIF_B, 37), fill=PAPER)
    # wrap body manually at ~38 chars
    words, lines, cur = body.split(), [], ""
    for w_ in words:
        if len(cur) + len(w_) + 1 > 40:
            lines.append(cur); cur = w_
        else:
            cur = (cur + " " + w_).strip()
    if cur: lines.append(cur)
    ly = yy + 104
    for ln in lines[:3]:
        d.text((x + 24, ly), ln, font=f(SANS, 26), fill=(198, 206, 216))
        ly += 34
    d.text((x + cw - 24, yy + ch - 36), src, font=f(SANS, 20), fill=MUTED, anchor="ra")

# ---- Ticker ----
ty = 592 + 3 * (218 + 16) + 8
d.line([80, ty, W - 80, ty], fill=LINE, width=3)
ticker = ("ALSO TODAY:  Drone strikes damage a UN facility in Khartoum  ·  Japan's restored Shuri Castle "
          "reopens, 7 years after fire  ·  M6.5 deep quake near Vanuatu, no damage reported  ·  "
          "NHS launches world's largest AI breast-cancer screening trial")
words, lines, cur = ticker.split(), [], ""
for w_ in words:
    if len(cur) + len(w_) + 1 > 96:
        lines.append(cur); cur = w_
    else:
        cur = (cur + " " + w_).strip()
if cur: lines.append(cur)
ly = ty + 22
for ln in lines[:3]:
    d.text((80, ly), ln, font=f(SANS, 27), fill=(190, 198, 210))
    ly += 40

d.text((80, H - 64), "Compiled from wire & public reporting, 23 Nov 2026 (WAT) · One day. One image.",
       font=f(SANS, 24), fill=MUTED)
d.rectangle([0, H - 12, W, H], fill=GOLD)

out = "world_news_2026-11-23.png"
img.save(out)
print("wrote", out, img.size)
