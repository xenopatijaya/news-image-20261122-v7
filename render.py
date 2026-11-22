#!/usr/bin/env python3
"""Sunday 22 November 2026 - the world in one day, drawn as one page.

Original drawing program for the make.fun news-image-20261122 entry (v7).
Every story printed was reported on Sunday 22 November 2026; the page is
drawn entirely in code with PIL primitives - night skies, a summit table,
a Gulf shoreline, and fifteen small scenes for the drawn stories.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
CARD = (253, 250, 242)
INK = (26, 25, 23)
SOFT = (84, 79, 70)
NAVY = (17, 41, 66)
NAVY2 = (30, 62, 94)
RED = (166, 34, 24)
GOLD = (186, 132, 40)
TEAL = (36, 100, 94)
GREEN = (58, 110, 62)
SAND = (233, 223, 197)
LINE = (196, 186, 164)
NIGHT = (13, 24, 43)
NIGHT2 = (24, 42, 68)

FD = "/usr/share/fonts/truetype/liberation/"
FDV = "/usr/share/fonts/truetype/dejavu/"


def font(path, size):
    return ImageFont.truetype(path, size)


def serif_b(size):
    return font(FD + "LiberationSerif-Bold.ttf", size)


def serif_i(size):
    return font(FD + "LiberationSerif-Italic.ttf", size)


def sans(size):
    return font(FD + "LiberationSans-Regular.ttf", size)


def sans_b(size):
    return font(FD + "LiberationSans-Bold.ttf", size)


def serif_num(size):
    return font(FDV + "DejaVuSerif-Bold.ttf", size)


# ---------------------------------------------------------------- stories
# (number, region, place, beat, headline, deck, source, tag)
LEADS = [
    (1, "EUROPE", "KYIV, UKRAINE", "WAR",
     "Russia fires 186 drones in a single night",
     "Air defences downed or suppressed 161 of the 186 drones by 08:00 Kyiv "
     "time - 56 of the 72 jet-powered Shaheds among them. Strikes were "
     "recorded at 18 locations, with debris at six more; the Air Force "
     "called its figures preliminary.",
     "Ukrainian Air Force", "REPORTED"),
    (2, "WORLD", "ANTALYA, TURKIYE", "CLIMATE SUMMIT",
     "COP31 final text names no fossil fuels",
     "The ten-page text recalls the Dubai pact and keeps the goal of 35% "
     "clean electricity by 2035; a $120bn adaptation target was dropped. "
     "Objections closed at 03:00 GMT and the approval session opened at "
     "06:00 - no gavel had fallen.",
     "Reuters", "REPORTED"),
    (3, "MIDDLE EAST", "MANAMA, BAHRAIN", "GULF CLAIM",
     "Iran claims two US Patriot radars were hit",
     "Tehran says its Saturday-night strike hit two US Patriot radars. "
     "Bahrain denies it: a civilian industrial site caught fire and nobody "
     "was hurt. The claim is printed as a claim, beside the denial.",
     "IRGC claim - Bahrain denial", "CLAIM - DENIED"),
]

# (number, region, place, headline, deck, source)
CARDS = [
    (4, "ASIA-PACIFIC", "IMPHAL, INDIA",
     "Toxic-liquor toll climbs to 19",
     "More than 600 people hospitalised since 20 Nov; 13 are in intensive care.",
     "XINHUA"),
    (5, "EUROPE", "GULF OF FINLAND",
     "Tanker Sparta II still burning",
     "The vessel's fire burned on through Sunday; all 16 crew are safe.",
     "WIRES"),
    (6, "ASIA-PACIFIC", "HONG KONG",
     "Election Committee picks the legislature",
     "856 candidates for 723 seats; 5,700 voters; polls 09:00-18:00; turnout 93.55%.",
     "SCMP"),
    (7, "AMERICAS", "LAS VEGAS, USA",
     "Verstappen wins the Las Vegas Grand Prix",
     "Norris finished second and Piastri third under the lights.",
     "FORMULA 1"),
    (8, "OCEANIA", "WELLINGTON, N.Z.",
     "India pile up 720 for 9",
     "Rahul made 136, Pant 128 and Gill 98 in the huge Wellington total.",
     "ESPNCRICINFO"),
    (9, "AMERICAS", "NEW ORLEANS, USA",
     "Wembanyama: 50 points, 19 rebounds",
     "Five blocks too, as the Spurs beat the Pelicans 114-91.",
     "NBA"),
    (10, "MIDDLE EAST", "TEHRAN, IRAN",
     "Electricity rationing begins",
     "Households face power cuts of up to two hours a day.",
     "IRANIAN MEDIA"),
    (11, "ASIA-PACIFIC", "CIKANDE, INDONESIA",
     "Candy-factory fire: 3 dead, 36 missing",
     "The blaze tore through a sweets plant in Banten on Sunday.",
     "INDONESIAN MEDIA"),
    (12, "EUROPE", "COPENHAGEN, DENMARK",
     "Russian attache expelled",
     "Denmark ordered the Russian military attache out of the country.",
     "OFFICIALS"),
    (13, "OCEANIA", "CANBERRA, AUSTRALIA",
     "Marles rejects the US AUKUS report",
     "The defence minister dismissed Washington's review findings.",
     "AUSTRALIAN MEDIA"),
    (14, "MIDDLE EAST", "BEIRUT, LEBANON",
     "Aoun: the state alone bears arms",
     "The president restated the state's monopoly on weapons.",
     "LEBANESE MEDIA"),
    (15, "OCEANIA", "MELBOURNE, AUSTRALIA",
     "1956 Olympians reunite at the MCG",
     "30 athletes walked the ground again, 70 years to the day of the opening ceremony.",
     "ATHLETICS AUSTRALIA"),
]

# (number, region, place, fact, source)
BRIEFS = [
    (16, "MIDDLE EAST", "GAZA", "Hamas seeks fresh talks through mediators", "Anadolu"),
    (17, "MIDDLE EAST", "RIYADH", "Saudi defences down three Houthi missiles", "Anadolu"),
    (18, "MIDDLE EAST", "HORMUZ", "Tanker Torleif still burning in the strait", "UKMTO"),
    (19, "MIDDLE EAST", "TEHRAN", "Iran says it downed two US drones", "Al Jazeera"),
    (20, "MIDDLE EAST", "JERUSALEM", "Eisenkot invites Likud into a unity bloc", "Reports"),
    (21, "AMERICAS", "WASHINGTON", "Nvidia faces an SEC accounting probe", "Reports"),
    (22, "EUROPE", "TALLINN", "Estonia shuts five Russia crossings from 1 Dec", "Reuters"),
    (23, "ASIA-PACIFIC", "TAIPEI", "Kinmen holds a live-fire drill", "CNA"),
    (24, "ASIA-PACIFIC", "MANILA", "Chinese bomber turns back 170 km from the capital", "Reports"),
    (25, "ASIA-PACIFIC", "NEW DELHI", "Japan holds its first live-fire drills in India", "Reports"),
    (26, "ASIA-PACIFIC", "KATHMANDU", "PM Shah pays a first state visit to Delhi", "IANS"),
    (27, "EUROPE", "MADRID", "Spain widens its bank tax to fund housing", "AP"),
    (28, "AFRICA", "KINSHASA", "Attack kills 40 civilians in DR Congo", "Officials"),
    (29, "ASIA-PACIFIC", "DHAKA", "30 Awami League homes torched overnight", "TOI"),
    (30, "AMERICAS", "WASHINGTON", "900,000 AI chips cleared for export to China", "Reuters"),
    (31, "MIDDLE EAST", "DOHA", "Iran opens talks with Qatari mediators", "Al Jazeera"),
    (32, "EUROPE", "VATICAN", "Pope Leo lunches with 1,300 poor guests", "Vatican News"),
    (33, "ASIA-PACIFIC", "LEH", "Ladakh votes 70% in first polls since 2019", "Daily World"),
    (34, "AFRICA", "EL FASHER", "Thousands who fled the city still missing", "MSF"),
    (35, "EUROPE", "TURIN", "Zverev meets Alcaraz in the final, 17:00 GMT", "ATP"),
    (36, "WORLD", "ANTALYA", "Road to COP32: Addis Ababa, November 2027", "Reuters"),
    (37, "WORLD", "NEW YORK", "US open to a Latin American UN chief", "Reports"),
    (38, "AMERICAS", "WASHINGTON", "FBI probes a hack of its crime database", "AP"),
    (39, "AFRICA", "MOGADISHU", "Somalia expels the UAE ambassador", "Wires"),
    (40, "AFRICA", "KHARTOUM", "Army retakes some 30 towns in Kordofan", "FT"),
    (41, "ASIA-PACIFIC", "BANGKOK", "Myanmar mine chemical exports barred", "Reuters"),
    (42, "WORLD", "MARKETS", "Bitcoin back above $60,000 after a $55,130 low", "Markets"),
    (43, "ASIA-PACIFIC", "BEIJING", "China 'firmly opposes' the FCC carrier ban", "Reuters"),
]

REGION_ORDER = ["ASIA-PACIFIC", "MIDDLE EAST", "EUROPE", "AMERICAS",
                "AFRICA", "WORLD", "OCEANIA"]
REGION_COLORS = {
    "ASIA-PACIFIC": (166, 62, 38),
    "MIDDLE EAST": (186, 132, 40),
    "EUROPE": (43, 88, 134),
    "AMERICAS": (44, 118, 84),
    "AFRICA": (122, 84, 148),
    "WORLD": (96, 96, 92),
    "OCEANIA": (36, 100, 94),
}


def tally():
    counts = {r: 0 for r in REGION_ORDER}
    for s in LEADS:
        counts[s[1]] += 1
    for s in CARDS:
        counts[s[1]] += 1
    for s in BRIEFS:
        counts[s[1]] += 1
    return counts


COUNTS = tally()
assert COUNTS == {"ASIA-PACIFIC": 11, "MIDDLE EAST": 9, "EUROPE": 7,
                  "AMERICAS": 5, "AFRICA": 4, "WORLD": 4, "OCEANIA": 3}, COUNTS
assert len(LEADS) + len(CARDS) + len(BRIEFS) == 43


# ---------------------------------------------------------------- helpers
def wrap(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, width, lh, max_lines=None):
    lines = wrap(d, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


def sky(d, x, y, w, h, top, bottom):
    steps = 24
    for i in range(steps):
        t = i / (steps - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.rectangle([x, y + h * i // steps, x + w, y + h * (i + 1) // steps + 1], fill=c)


def dotted(d, x0, y0, x1, y1, fill, n=16, r=1.4):
    for i in range(n + 1):
        t = i / n
        cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def dashed_arc(d, cx, cy, rx, ry, a0, a1, fill, dash=7, gap=5, wd=2):
    import math
    total = a1 - a0
    steps = 90
    on = True
    run = 0
    prev = None
    for i in range(steps + 1):
        a = math.radians(a0 + total * i / steps)
        p = (cx + rx * math.cos(a), cy + ry * math.sin(a))
        run += 1
        if on and prev:
            d.line([prev, p], fill=fill, width=wd)
        if on and run >= dash:
            on, run = False, 0
        elif not on and run >= gap:
            on, run = True, 0
        prev = p


def burst(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flame(d, cx, by, s, outer=(232, 110, 30), inner=(246, 196, 84)):
    d.polygon([(cx - 0.42 * s, by), (cx, by - s), (cx + 0.42 * s, by)], fill=outer)
    d.polygon([(cx - 0.2 * s, by), (cx, by - 0.55 * s), (cx + 0.2 * s, by)], fill=inner)


def smoke(d, cx, cy, s, col=(120, 118, 112)):
    for dx, dy, r in [(0, 0, 0.5), (0.5, -0.3, 0.65), (1.1, -0.55, 0.85), (1.8, -0.75, 1.05)]:
        d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s,
                   cx + dx * s + r * s, cy + dy * s + r * s], fill=col)


def drone(d, cx, cy, s, col=(10, 12, 18)):
    d.rectangle([cx - s, cy - 0.28 * s, cx + s, cy + 0.28 * s], fill=col)
    for dx in (-1, 1):
        for dy in (-1, 1):
            px, py = cx + dx * s * 1.25, cy + dy * s * 0.75
            d.line([cx, cy, px, py], fill=col, width=2)
            d.ellipse([px - 3.4, py - 1.4, px + 3.4, py + 1.4], fill=col)
    d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=(230, 60, 40))


# ---------------------------------------------------------------- lead scenes
def scene_kyiv(d, x, y, w, h):
    sky(d, x, y, w, h, NIGHT, NIGHT2)
    d.ellipse([x + w - 52, y + 10, x + w - 26, y + 36], fill=(238, 232, 205))
    d.ellipse([x + w - 60, y + 6, x + w - 36, y + 30], fill=NIGHT2)
    base = y + h
    # searchlight beam sweeping up from the rooftops
    d.polygon([(x + 0.47 * w, base), (x + 0.19 * w, y + 4), (x + 0.34 * w, y + 1)],
              fill=(84, 92, 96))
    # skyline of apartment blocks with lit windows
    blocks = [(0.02, 0.42), (0.16, 0.58), (0.31, 0.36), (0.44, 0.64),
              (0.60, 0.44), (0.73, 0.56), (0.87, 0.40)]
    for fx, fh in blocks:
        bx, bw = x + fx * w, 0.115 * w
        by = base - fh * h
        d.rectangle([bx, by, bx + bw, base], fill=(8, 13, 24))
        for r in range(4):
            for c in range(2):
                if (int(fx * 97) + r * 3 + c * 7) % 3 != 0:
                    wx, wy = bx + 5 + c * (bw - 12), by + 6 + r * (fh * h - 12) / 4
                    d.rectangle([wx, wy, wx + 4.4, wy + 3.4], fill=(240, 196, 96))
    # drones on dotted paths + bursts
    drone(d, x + 0.16 * w, y + 0.24 * h, 7)
    drone(d, x + 0.38 * w, y + 0.16 * h, 6)
    drone(d, x + 0.66 * w, y + 0.30 * h, 7)
    dotted(d, x + 0.16 * w, y + 0.30 * h, x + 0.30 * w, base - 8, (200, 90, 60), 9)
    dotted(d, x + 0.66 * w, y + 0.36 * h, x + 0.78 * w, base - 6, (200, 90, 60), 9)
    burst(d, x + 0.31 * w, base - 12, 10, (246, 178, 64))
    burst(d, x + 0.79 * w, base - 9, 8, (240, 140, 52))


def scene_cop31(d, x, y, w, h):
    sky(d, x, y, w, h, (246, 208, 150), (250, 232, 196))
    d.ellipse([x + 0.06 * w, y + 0.10 * h, x + 0.06 * w + 30, y + 0.10 * h + 30],
              fill=(244, 178, 74))
    # hall back wall + window band
    d.rectangle([x, y + 0.52 * h, x + w, y + h], fill=(214, 196, 164))
    # long summit table with delegates
    ty = y + 0.60 * h
    d.rectangle([x + 0.05 * w, ty + 14, x + 0.60 * w, ty + 20], fill=(122, 84, 50))
    for i in range(6):
        hx = x + (0.09 + i * 0.088) * w
        d.ellipse([hx - 6, ty - 8, hx + 6, ty + 4], fill=(70, 52, 40))
        d.pieslice([hx - 8, ty + 2, hx + 8, ty + 18], 180, 360, fill=(52, 66, 92))
        d.rectangle([hx - 5, ty + 10, hx + 5, ty + 13], fill=(238, 234, 222))
    # the text itself: a document panel, one line struck through in red
    px, py, pw, ph = x + 0.66 * w, y + 0.10 * h, 0.30 * w, 0.80 * h
    d.rectangle([px, py, px + pw, py + ph], fill=(253, 250, 240), outline=(150, 138, 112))
    for i in range(5):
        ly = py + 10 + i * 11
        d.rectangle([px + 8, ly, px + pw - 8 - (i % 3) * 9, ly + 3.4], fill=(150, 146, 134))
    d.text((px + 8, py + ph - 20), "FOSSIL FUELS", font=sans_b(8), fill=RED)
    d.line([px + 6, py + ph - 15, px + 62, py + ph - 15], fill=RED, width=2)
    # clock at 03:00
    cx, cy, r = x + 0.60 * w, y + 0.26 * h, 11
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(253, 250, 240), outline=INK, width=2)
    d.line([cx, cy, cx, cy - r + 4], fill=INK, width=2)
    d.line([cx, cy, cx + r - 5, cy], fill=INK, width=2)


def scene_bahrain(d, x, y, w, h):
    sky(d, x, y, w, h, (216, 178, 128), (240, 214, 178))
    d.rectangle([x, y + 0.68 * h, x + w, y + h], fill=(44, 96, 110))
    for i in range(5):
        wy = y + (0.74 + i * 0.05) * h
        d.line([x + (i % 2) * 14, wy, x + w - ((i + 1) % 2) * 14, wy],
               fill=(90, 140, 148), width=1)
    shore = y + 0.68 * h
    d.rectangle([x, shore - 4, x + w, shore], fill=(120, 96, 70))
    # two radar domes on the shore
    for fx in (0.16, 0.40):
        bx = x + fx * w
        d.rectangle([bx - 16, shore - 12, bx + 16, shore - 4], fill=(96, 92, 86))
        d.pieslice([bx - 13, shore - 34, bx + 13, shore - 8], 180, 360, fill=(238, 234, 224))
        d.line([bx, shore - 32, bx, shore - 40], fill=INK, width=2)
    flame(d, x + 0.40 * w, shore - 30, 15)
    smoke(d, x + 0.43 * w, shore - 44, 7)
    # Patriot-style launcher, right side
    lx, ly = x + 0.74 * w, shore - 6
    d.rectangle([lx - 20, ly - 8, lx + 22, ly], fill=(60, 64, 58))
    d.ellipse([lx - 14, ly - 3, lx - 5, ly + 4], fill=(30, 30, 28))
    d.ellipse([lx + 8, ly - 3, lx + 17, ly + 4], fill=(30, 30, 28))
    import math
    ex, ey = lx + 26, ly - 34
    d.line([lx + 4, ly - 8, ex, ey], fill=(60, 64, 58), width=6)
    d.rectangle([ex - 13, ey - 5, ex + 13, ey + 5], fill=(74, 78, 70))
    # incoming dashed arcs - a claim, drawn dashed
    dashed_arc(d, x + 0.30 * w, y + 0.62 * h, 0.34 * w, 0.52 * h, 200, 305, RED, wd=2)
    dashed_arc(d, x + 0.52 * w, y + 0.60 * h, 0.30 * w, 0.46 * h, 205, 300, RED, wd=2)


# ---------------------------------------------------------------- card scenes
def sc_manipur(d, x, y, w, h):
    sky(d, x, y, w, h, (52, 44, 48), (84, 66, 66))
    for i, fx in enumerate((0.16, 0.34, 0.52)):
        bx = x + fx * w
        d.rectangle([bx - 6, y + 0.34 * h, bx + 6, y + 0.92 * h], fill=(30, 30, 30))
        d.rectangle([bx - 2.4, y + 0.14 * h, bx + 2.4, y + 0.34 * h], fill=(30, 30, 30))
        d.rectangle([bx - 6, y + 0.52 * h, bx + 6, y + 0.62 * h], fill=(214, 178, 92))
        d.line([bx - 4, y + 0.40 * h, bx + 4, y + 0.48 * h], fill=RED, width=2)
        d.line([bx - 4, y + 0.48 * h, bx + 4, y + 0.40 * h], fill=RED, width=2)
    cx, cy = x + 0.80 * w, y + 0.52 * h
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(240, 236, 226))
    d.rectangle([cx - 3, cy - 9, cx + 3, cy + 9], fill=RED)
    d.rectangle([cx - 9, cy - 3, cx + 9, cy + 3], fill=RED)


def sc_sparta(d, x, y, w, h):
    sky(d, x, y, w, h, (196, 150, 110), (226, 190, 150))
    d.rectangle([x, y + 0.66 * h, x + w, y + h], fill=(52, 88, 102))
    hx, hy = x + 0.16 * w, y + 0.60 * h
    d.polygon([(hx, hy), (hx + 0.62 * w, hy), (hx + 0.55 * w, hy + 0.16 * h),
               (hx + 0.07 * w, hy + 0.16 * h)], fill=(38, 40, 44))
    d.rectangle([hx + 0.40 * w, hy - 0.22 * h, hx + 0.52 * w, hy], fill=(70, 72, 76))
    d.rectangle([hx + 0.10 * w, hy - 0.12 * h, hx + 0.34 * w, hy], fill=(96, 88, 80))
    flame(d, hx + 0.24 * w, hy - 0.10 * h, 13)
    flame(d, hx + 0.46 * w, hy - 0.20 * h, 10)
    smoke(d, hx + 0.30 * w, hy - 0.34 * h, 6, (96, 92, 88))


def sc_hongkong(d, x, y, w, h):
    sky(d, x, y, w, h, (198, 214, 226), (232, 236, 226))
    for fx, fh in ((0.04, 0.55), (0.17, 0.75), (0.30, 0.45), (0.42, 0.65)):
        bx = x + fx * w
        d.rectangle([bx, y + h - fh * h, bx + 0.10 * w, y + h], fill=(90, 104, 122))
    bx, by = x + 0.60 * w, y + 0.30 * h
    d.rectangle([bx, by, bx + 0.32 * w, by + 0.58 * h], fill=(240, 236, 226), outline=INK)
    d.rectangle([bx + 5, by + 6, bx + 0.32 * w - 5, by + 10], fill=INK)
    px, py = bx + 0.10 * w, by - 0.20 * h
    d.rectangle([px, py, px + 0.13 * w, py + 0.30 * h], fill=(250, 248, 240), outline=SOFT)
    d.line([px + 3, py + 8, px + 6, py + 12], fill=GREEN, width=2)
    d.line([px + 6, py + 12, px + 12, py + 3], fill=GREEN, width=2)


def sc_vegas(d, x, y, w, h):
    sky(d, x, y, w, h, NIGHT, (40, 34, 64))
    for i in range(14):
        sx = x + (i * 37 % 150)
        sy = y + (i * 23 % 16)
        d.ellipse([sx, sy, sx + 1.8, sy + 1.8], fill=(240, 236, 210))
    d.rectangle([x, y + 0.78 * h, x + w, y + h], fill=(30, 28, 36))
    d.line([x, y + 0.78 * h, x + w, y + 0.78 * h], fill=(240, 196, 96), width=2)
    cx, cy = x + 0.30 * w, y + 0.52 * h
    d.polygon([(cx, cy), (cx + 0.16 * w, cy - 0.16 * h), (cx + 0.34 * w, cy - 0.10 * h),
               (cx + 0.42 * w, cy)], fill=(178, 30, 30))
    d.rectangle([cx - 0.05 * w, cy - 0.05 * h, cx + 0.01 * w, cy], fill=(24, 24, 26))
    d.rectangle([cx + 0.36 * w, cy - 0.20 * h, cx + 0.44 * w, cy], fill=(24, 24, 26))
    for fx in (0.06, 0.34):
        d.ellipse([cx + fx * w - 6, cy - 1, cx + fx * w + 6, cy + 9], fill=(12, 12, 14))
        d.ellipse([cx + fx * w - 2.4, cy + 2, cx + fx * w + 2.4, cy + 6], fill=(150, 150, 150))
    for i in range(5):
        lx = x + (0.60 + i * 0.075) * w
        d.line([lx, y + 0.78 * h, lx, y + 0.40 * h], fill=(200, 200, 200), width=1)
        d.ellipse([lx - 2.4, y + 0.34 * h, lx + 2.4, y + 0.42 * h], fill=(250, 220, 130))


def sc_cricket(d, x, y, w, h):
    sky(d, x, y, w, h, (168, 204, 168), (216, 232, 196))
    d.rectangle([x, y + 0.55 * h, x + w, y + h], fill=(86, 140, 74))
    d.rectangle([x + 0.40 * w, y + 0.55 * h, x + 0.62 * w, y + h], fill=(206, 188, 150))
    for i in range(3):
        sx = x + (0.455 + i * 0.045) * w
        d.rectangle([sx, y + 0.30 * h, sx + 3, y + 0.72 * h], fill=(238, 230, 200))
    d.rectangle([x + 0.455 * w, y + 0.28 * h, x + 0.565 * w, y + 0.33 * h], fill=(238, 230, 200))
    d.line([x + 0.78 * w, y + 0.86 * h, x + 0.66 * w, y + 0.34 * h], fill=(150, 110, 60), width=3)
    dotted(d, x + 0.16 * w, y + 0.20 * h, x + 0.44 * w, y + 0.30 * h, (178, 30, 30), 7, 1.8)
    d.ellipse([x + 0.13 * w, y + 0.14 * h, x + 0.13 * w + 7, y + 0.14 * h + 7], fill=(178, 30, 30))


def sc_nba(d, x, y, w, h):
    sky(d, x, y, w, h, (70, 60, 84), (110, 96, 118))
    d.rectangle([x, y + 0.72 * h, x + w, y + h], fill=(168, 118, 74))
    d.line([x, y + 0.72 * h, x + w, y + 0.72 * h], fill=(240, 236, 226), width=2)
    bx, by = x + 0.58 * w, y + 0.16 * h
    d.rectangle([bx, by, bx + 0.30 * w, by + 0.30 * h], fill=(240, 236, 226), outline=INK)
    d.rectangle([bx + 0.09 * w, by + 0.20 * h, bx + 0.21 * w, by + 0.30 * h],
                outline=(200, 90, 30), width=2)
    for i in range(4):
        d.line([bx + (0.10 + i * 0.033) * w, by + 0.30 * h,
                bx + 0.15 * w, by + 0.52 * h], fill=(240, 236, 226), width=1)
    d.ellipse([x + 0.20 * w, y + 0.30 * h, x + 0.20 * w + 17, y + 0.30 * h + 17],
              fill=(216, 110, 40))
    d.arc([x + 0.20 * w, y + 0.30 * h, x + 0.20 * w + 17, y + 0.30 * h + 17],
          90, 270, fill=(120, 56, 20), width=1)
    dotted(d, x + 0.28 * w, y + 0.52 * h, bx + 0.13 * w, by + 0.26 * h, (250, 220, 190), 8)


def sc_tehran(d, x, y, w, h):
    sky(d, x, y, w, h, (36, 38, 52), (70, 70, 84))
    for fx, fh in ((0.05, 0.4), (0.25, 0.55), (0.48, 0.35), (0.66, 0.5)):
        bx = x + fx * w
        d.rectangle([bx, y + h - fh * h, bx + 0.15 * w, y + h], fill=(16, 17, 24))
    px = x + 0.86 * w
    d.line([px, y + 0.10 * h, px, y + h], fill=(10, 10, 12), width=3)
    d.line([px - 0.09 * w, y + 0.16 * h, px + 0.09 * w, y + 0.16 * h], fill=(10, 10, 12), width=2)
    import math
    for fx in (0.06, 0.30, 0.54):
        x0 = x + fx * w
        pts = [(x0 + t * 0.20 * w, y + 0.14 * h + math.sin(t * 3.1) * 2.6) for t in
               (0, 0.25, 0.5, 0.75, 1.0)]
        d.line(pts, fill=(10, 10, 12), width=1)
    bx, by = x + 0.80 * w, y + 0.34 * h
    d.ellipse([bx - 6, by - 7, bx + 6, by + 5], fill=(90, 88, 80))
    d.rectangle([bx - 2, by + 5, bx + 2, by + 8], fill=(60, 58, 52))
    d.line([bx - 8, by + 10, bx + 8, by - 12], fill=RED, width=2)


def sc_cikande(d, x, y, w, h):
    sky(d, x, y, w, h, (226, 176, 138), (240, 210, 176))
    fx, fy = x + 0.14 * w, y + 0.34 * h
    d.rectangle([fx, fy, fx + 0.56 * w, y + h], fill=(120, 104, 96))
    d.rectangle([fx + 0.44 * w, fy - 0.24 * h, fx + 0.52 * w, fy], fill=(100, 88, 82))
    for i in range(4):
        wx = fx + (0.06 + i * 0.12) * w
        d.rectangle([wx, fy + 0.16 * h, wx + 0.07 * w, fy + 0.34 * h], fill=(250, 214, 140))
    flame(d, fx + 0.16 * w, fy + 0.02 * h, 15)
    flame(d, fx + 0.30 * w, fy + 0.02 * h, 11)
    smoke(d, fx + 0.48 * w, fy - 0.30 * h, 6, (104, 98, 92))
    d.rectangle([x + 0.78 * w, y + 0.62 * h, x + 0.94 * w, y + 0.92 * h], fill=(178, 30, 30))
    d.rectangle([x + 0.845 * w, y + 0.68 * h, x + 0.875 * w, y + 0.86 * h], fill=(250, 246, 238))
    d.rectangle([x + 0.795 * w, y + 0.735 * h, x + 0.925 * w, y + 0.765 * h], fill=(250, 246, 238))


def sc_copenhagen(d, x, y, w, h):
    sky(d, x, y, w, h, (188, 204, 218), (226, 230, 220))
    d.rectangle([x, y + 0.80 * h, x + w, y + h], fill=(120, 128, 118))
    gx = x + 0.08 * w
    for fx in (0.0, 0.22, 0.44, 0.66, 0.88):
        bx = gx + fx * 0.72 * w
        d.rectangle([bx, y + 0.30 * h, bx + 4, y + 0.82 * h], fill=(52, 54, 56))
    d.line([gx, y + 0.34 * h, gx + 0.76 * w, y + 0.34 * h], fill=(52, 54, 56), width=2)
    d.line([gx, y + 0.56 * h, gx + 0.76 * w, y + 0.56 * h], fill=(52, 54, 56), width=2)
    px = x + 0.84 * w
    d.line([px, y + 0.06 * h, px, y + 0.84 * h], fill=(40, 40, 42), width=2)
    d.rectangle([px, y + 0.06 * h, px + 0.13 * w, y + 0.30 * h], fill=(196, 40, 44))
    d.rectangle([px, y + 0.155 * h, px + 0.13 * w, y + 0.185 * h], fill=(246, 244, 238))
    d.rectangle([px + 0.038 * w, y + 0.06 * h, px + 0.062 * w, y + 0.30 * h], fill=(246, 244, 238))


def sc_canberra(d, x, y, w, h):
    sky(d, x, y, w, h, (170, 200, 220), (228, 234, 220))
    d.ellipse([x + 0.78 * w, y + 0.08 * h, x + 0.78 * w + 15, y + 0.08 * h + 15],
              fill=(246, 200, 92))
    d.rectangle([x, y + 0.58 * h, x + w, y + h], fill=(52, 96, 118))
    sy = y + 0.60 * h
    d.ellipse([x + 0.14 * w, sy - 6, x + 0.80 * w, sy + 7], fill=(30, 34, 40))
    d.rectangle([x + 0.40 * w, sy - 13, x + 0.54 * w, sy - 4], fill=(30, 34, 40))
    d.rectangle([x + 0.455 * w, sy - 19, x + 0.475 * w, sy - 12], fill=(30, 34, 40))
    d.polygon([(x + 0.80 * w, sy - 2), (x + 0.90 * w, sy - 10), (x + 0.90 * w, sy + 2)],
              fill=(30, 34, 40))
    for i in range(4):
        wx = x + (0.08 + i * 0.22) * w
        d.arc([wx, sy + 6, wx + 16, sy + 13], 180, 360, fill=(210, 228, 232), width=1)


def sc_beirut(d, x, y, w, h):
    sky(d, x, y, w, h, (214, 200, 168), (238, 228, 198))
    bx, by = x + 0.10 * w, y + 0.30 * h
    d.rectangle([bx, by, bx + 0.52 * w, y + h], fill=(206, 188, 156))
    d.pieslice([bx + 0.16 * w, by - 0.26 * h, bx + 0.36 * w, by + 0.10 * h], 180, 360,
               fill=(150, 120, 84))
    for i in range(3):
        wx = bx + (0.07 + i * 0.16) * w
        d.rectangle([wx, by + 0.20 * h, wx + 0.08 * w, by + 0.44 * h], fill=(96, 84, 66))
    tx = x + 0.80 * w
    d.rectangle([tx - 1.6, y + 0.52 * h, tx + 1.6, y + 0.94 * h], fill=(110, 80, 52))
    for i, (dy, wd) in enumerate(((0.30, 0.13), (0.44, 0.105), (0.57, 0.08))):
        d.polygon([(tx - wd * w, y + dy * h + 8), (tx, y + dy * h), (tx + wd * w, y + dy * h + 8)],
                  fill=(44, 104, 60))


def sc_melbourne(d, x, y, w, h):
    sky(d, x, y, w, h, (206, 190, 150), (236, 226, 196))
    for fx in (0.08, 0.34, 0.62, 0.88):
        mx = x + fx * w
        d.line([mx, y + h, mx, y + 0.16 * h], fill=(70, 66, 60), width=2)
        for r in range(2):
            for c in range(3):
                d.ellipse([mx - 5 + c * 5, y + 0.10 * h + r * 5, mx - 3 + c * 5,
                           y + 0.10 * h + r * 5 + 3], fill=(250, 240, 200))
    d.ellipse([x + 0.16 * w, y + 0.58 * h, x + 0.84 * w, y + 1.06 * h], fill=(96, 140, 78))
    d.ellipse([x + 0.24 * w, y + 0.66 * h, x + 0.76 * w, y + 1.02 * h], fill=(178, 120, 84))
    d.ellipse([x + 0.315 * w, y + 0.715 * h, x + 0.685 * w, y + 0.965 * h], fill=(96, 140, 78))
    for fx in (0.40, 0.52, 0.63):
        rx, ry = x + fx * w, y + 0.80 * h
        d.ellipse([rx - 2.4, ry - 8, rx + 2.4, ry - 3.4], fill=(40, 36, 32))
        d.line([rx, ry - 3, rx + 3, ry + 3], fill=(40, 36, 32), width=2)
        d.line([rx, ry + 3, rx - 4, ry + 8], fill=(40, 36, 32), width=2)


CARD_SCENES = {4: sc_manipur, 5: sc_sparta, 6: sc_hongkong, 7: sc_vegas,
               8: sc_cricket, 9: sc_nba, 10: sc_tehran, 11: sc_cikande,
               12: sc_copenhagen, 13: sc_canberra, 14: sc_beirut, 15: sc_melbourne}


# ---------------------------------------------------------------- world map
LAND_SPANS = [
    (0, 7, 9), (0, 12, 14), (0, 40, 44), (0, 48, 53),
    (1, 5, 17), (1, 30, 36), (1, 37, 57),
    (2, 4, 18), (2, 29, 37), (2, 38, 58),
    (3, 5, 17), (3, 29, 38), (3, 39, 57),
    (4, 6, 16), (4, 28, 34), (4, 35, 56),
    (5, 7, 15), (5, 28, 38), (5, 39, 54), (5, 46, 49),
    (6, 9, 14), (6, 16, 18), (6, 29, 37), (6, 40, 53),
    (7, 16, 19), (7, 29, 37), (7, 44, 47), (7, 48, 51),
    (8, 15, 19), (8, 30, 36), (8, 47, 50), (8, 52, 55),
    (9, 15, 18), (9, 30, 35),
    (10, 15, 18), (10, 30, 34),
    (11, 15, 17), (11, 30, 33), (11, 48, 53),
    (12, 14, 17), (12, 31, 33), (12, 50, 57),
    (13, 14, 16), (13, 50, 56),
    (14, 14, 16), (14, 51, 56),
    (15, 13, 15), (15, 60, 60),
    (16, 13, 14),
]
# story number -> (col, row) on the grid above
PINS = {1: (36, 3), 2: (36, 5), 3: (40, 7), 4: (47, 7), 5: (35, 2),
        6: (51, 7), 7: (11, 5), 8: (60, 15), 9: (15, 6), 10: (40, 5),
        11: (49, 11), 12: (33, 3), 13: (57, 14), 14: (37, 6), 15: (55, 15)}


def draw_map(d, x, y, w, h):
    cols, rows = 62, 17
    px, py = w / cols, h / rows
    land = set()
    for r, c0, c1 in LAND_SPANS:
        for c in range(c0, c1 + 1):
            land.add((c, r))
    for r in range(rows):
        for c in range(cols):
            cx, cy = x + (c + 0.5) * px, y + (r + 0.5) * py
            if (c, r) in land:
                d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=NAVY2)
            else:
                d.ellipse([cx - 0.8, cy - 0.8, cx + 0.8, cy + 0.8], fill=(224, 214, 190))
    for n, (c, r) in PINS.items():
        cx, cy = x + (c + 0.5) * px, y + (r + 0.5) * py
        d.ellipse([cx - 5.6, cy - 5.6, cx + 5.6, cy + 5.6], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        f = sans_b(7)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 3.6), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- assembly
MX, MW = 20, 984


def centered(d, cx, y, s, fnt, fill):
    d.text((cx - d.textlength(s, font=fnt) / 2, y), s, font=fnt, fill=fill)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # kicker band
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((MX, 7), "THE WORLD IN ONE DAY", font=sans_b(11), fill=(246, 242, 230))
    rt = "A ONE-PAGE BRIEF OF ONE DAY'S NEWS"
    d.text((W - MX - d.textlength(rt, font=sans_b(11)), 7), rt,
           font=sans_b(11), fill=(246, 242, 230))

    # masthead
    d.line([MX, 32, W - MX, 32], fill=INK, width=2)
    d.line([MX, 35, W - MX, 35], fill=INK, width=1)
    centered(d, W / 2, 42, "Sunday 22 November 2026", serif_b(62), INK)
    centered(d, W / 2, 110,
             "43 dated stories \u00b7 7 regions \u00b7 every story dated "
             "Sunday 22 November 2026 at its source", sans(12), SOFT)
    d.line([MX, 130, W - MX, 130], fill=LINE, width=1)
    centered(d, W / 2, 136,
             "186 drones over Ukraine in one night \u00b7 COP31's final text "
             "names no fossil fuels \u00b7 Iran's radar claim, denied in Manama",
             serif_i(17), RED)

    # big numbers
    nums = [("186", "DRONES LAUNCHED AT UKRAINE OVERNIGHT", RED),
            ("161", "DOWNED OR SUPPRESSED BY 08:00 KYIV", NAVY),
            ("19", "DEAD IN MANIPUR'S TOXIC-LIQUOR TOLL", NAVY),
            ("723", "HONG KONG SEATS CONTESTED SUNDAY", NAVY),
            ("720/9", "INDIA'S TOTAL AT WELLINGTON", NAVY),
            ("50", "POINTS FOR WEMBANYAMA IN NEW ORLEANS", NAVY)]
    ny, cw = 158, MW / 6
    d.line([MX, 154, W - MX, 154], fill=INK, width=1)
    for i, (n, lab, col) in enumerate(nums):
        cx = MX + cw * i + cw / 2
        centered(d, cx, ny, n, serif_num(33), col)
        for j, ln in enumerate(wrap(d, lab, sans_b(8), cw - 10)):
            centered(d, cx, ny + 39 + j * 9.5, ln, sans_b(8), SOFT)
        if i:
            d.line([MX + cw * i, 158, MX + cw * i, 210], fill=LINE, width=1)
    d.line([MX, 214, W - MX, 214], fill=INK, width=1)

    # region tally
    by = 222
    xcur = MX
    for r in REGION_ORDER:
        seg = MW * COUNTS[r] / 43
        d.rectangle([xcur, by, xcur + seg - 1.5, by + 13], fill=REGION_COLORS[r])
        xcur += seg
    lx = MX
    d.text((lx, by + 17), "WHERE THE DAY HAPPENED", font=sans_b(10), fill=INK)
    lx += d.textlength("WHERE THE DAY HAPPENED  ", font=sans_b(10))
    for r in REGION_ORDER:
        d.rectangle([lx, by + 18, lx + 8, by + 26], fill=REGION_COLORS[r])
        s = "%s %d" % (r, COUNTS[r])
        d.text((lx + 12, by + 17), s, font=sans(10), fill=INK)
        lx += 12 + d.textlength(s, font=sans(10)) + 12

    # UTC timeline
    ty = 256
    d.rectangle([MX, ty, W - MX, ty + 19], fill=NAVY)
    d.text((MX + 9, ty + 4), "THE DAY IN UTC", font=sans_b(10), fill=(246, 242, 230))
    d.text((MX + 118, ty + 4),
           "01:42 Houthi missile downed \u00b7 03:00 COP31 objections close "
           "\u00b7 06:00 approval session opens \u00b7 09:00-18:00 Hong Kong "
           "polls \u00b7 17:00 ATP final, Turin",
           font=sans(10.5), fill=(226, 232, 240))

    # leads
    ly = 283
    scenes = {1: scene_kyiv, 2: scene_cop31, 3: scene_bahrain}
    for i, s in enumerate(LEADS):
        n, reg, place, beat, head, deck, src, tag = s
        x = MX + i * 332
        w = 320
        scenes[n](d, x, ly, w, 100)
        d.rectangle([x, ly, x + w, ly + 100], outline=LINE)
        d.text((x, ly + 106), "%d \u00b7 %s \u2014 %s" % (n, place, beat),
               font=sans_b(10), fill=RED)
        hend = text_block(d, x, ly + 122, head, serif_b(20), INK, w, 24, 3)
        dend = text_block(d, x, hend + 3, deck, sans(10.5), (40, 39, 36), w, 13.5, 5)
        tagw = d.textlength(tag, font=sans_b(8)) + 10
        tcol = GREEN if tag == "REPORTED" else RED
        d.rectangle([x, 524, x + tagw, 538], fill=tcol)
        d.text((x + 5, 527), tag, font=sans_b(8), fill=(255, 255, 255))
        d.text((x + tagw + 7, 526.5), src, font=sans(9), fill=SOFT)
        if i:
            d.line([x - 6, ly, x - 6, 540], fill=LINE, width=1)

    # cards
    cy0 = 548
    for idx, c in enumerate(CARDS):
        n, reg, place, head, deck, src = c
        row, col = divmod(idx, 6)
        x = MX + col * (156 + 9.6)
        y = cy0 + row * (116 + 6)
        w, h = 156, 116
        d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE)
        CARD_SCENES[n](d, x + 1, y + 1, w - 2, 40)
        # source as a small credit chip over the scene's lower-right corner
        sw = d.textlength(src, font=sans(6.8))
        d.rectangle([x + w - 4 - sw - 6, y + 28, x + w - 4, y + 39],
                    fill=CARD, outline=LINE)
        d.text((x + w - 7 - sw, y + 30), src, font=sans(6.8), fill=SOFT)
        d.text((x + 6, y + 45), "%d \u00b7 %s" % (n, place), font=sans_b(7.8), fill=RED)
        text_block(d, x + 6, y + 57, head, serif_b(12), INK, w - 12, 14.5, 2)
        text_block(d, x + 6, y + 86, deck, sans(8.8), (40, 39, 36), w - 12, 10.8, 3)

    # briefs
    byy = 792
    d.text((MX, byy), "THE REST OF THE DAY", font=serif_b(13), fill=INK)
    d.text((MX + 168, byy + 2), "\u2014 28 briefs, numbered 16-43, each with its source",
           font=sans(10.5), fill=SOFT)
    d.line([MX, byy + 19, W - MX, byy + 19], fill=LINE, width=1)
    cols = [BRIEFS[0:10], BRIEFS[10:19], BRIEFS[19:28]]
    for ci, colset in enumerate(cols):
        x = MX + ci * 332
        for ri, b in enumerate(colset):
            n, reg, place, fact, src = b
            y = byy + 26 + ri * 12.8
            head = "%d %s \u2014 " % (n, place)
            d.text((x, y), head, font=sans_b(8.8), fill=INK)
            hw = d.textlength(head, font=sans_b(8.8))
            d.text((x + hw, y), "%s (%s)" % (fact, src), font=sans(8.8),
                   fill=(40, 39, 36))

    # bottom: map + date check
    gy = 946
    d.text((MX, gy), "WHERE IT HAPPENED \u2014 PINS MATCH STORY NUMBERS",
           font=sans_b(8.5), fill=INK)
    draw_map(d, MX, gy + 13, 452, 52)
    bx = 492
    d.rectangle([bx, gy - 2, W - MX, 1008], outline=RED, width=2)
    d.text((bx + 10, gy + 4), "DATE CHECK", font=sans_b(10), fill=RED)
    text_block(d, bx + 10, gy + 19,
               "Left off on purpose: the EU-Indonesia deal (signed Saturday) "
               "\u00b7 Kenya's last Ebola patient (home 11 Nov) \u00b7 Peru's "
               "Junin quake (Friday; update Saturday) \u00b7 Belgium's flight "
               "shutdown (announced Saturday) \u00b7 El Chapo Isidro, Bayelsa "
               "boat, Gaza food-van strike (Fri-Sat).",
               sans(8.8), (40, 39, 36), W - MX - bx - 20, 11.5)

    # footer
    centered(d, W / 2, 1012,
             "Sources are named on the page \u00b7 Compiled Sunday 22 "
             "November 2026 \u00b7 REPORTED = carried by the day's wires "
             "\u00b7 CLAIM - DENIED = one side's claim, printed beside the denial",
             sans(7.5), SOFT)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    draw_page().save(out)
    print("wrote", out)
