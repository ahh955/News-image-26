#!/usr/bin/env python3
"""Build entry.png for news-image-20261126 v2 — 36 stories, 6 regions.
Deterministic: fixed palette, fixed layout, no randomness, no timestamps.
Drawn fresh for this entry; flat detailed illustrations, no photos."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 242, 228)
INK = (26, 26, 26)
RED = (179, 32, 44)
BLUE = (28, 52, 96)
SKY = (168, 205, 226)
SEA = (178, 214, 230)
LAND = (222, 196, 148)
GREEN = (28, 110, 68)
ORANGE = (196, 96, 16)
GREY = (110, 110, 108)
LIGHT = (238, 232, 214)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


LABEL_COLORS = {
    "CONFIRMED": (28, 110, 68),
    "OFFICIAL": (28, 80, 160),
    "REPORTED": (110, 110, 108),
    "ONGOING": (196, 96, 16),
    "CLAIM": (179, 32, 44),
}

# (headline, detail, label) — all verified as reported on 26 Nov 2026.
LEADS = [
    ("MACY'S 100TH PARADE POSTPONED",
     "Nor'easter gusts of 65 mph ground the balloons; the parade moves to Saturday, 8:30 a.m. — a first in 100 years.",
     "NEW YORK", "REPORTED"),
    ("DRONES KILL TWO ITALIANS IN KUWAIT",
     "Italy and Kuwait blame Iran for the strike on an air-defence site; Tehran denies any role.",
     "KUWAIT CITY", "REPORTED"),
    ("EU SPLIT OVER BUDGET AND $49B UKRAINE LOAN",
     "Leaders end the summit without a deal as the budget fight and the loan divide the bloc.",
     "BRUSSELS", "REPORTED"),
]

# (headline, detail, label, region)
ALSO = [
    ("US proposes tariffs on 14 partners", "Duties target factory overcapacity; Taiwan up to 15%", "REPORTED", "NA"),
    ("Bears stun Lions 39\u201335", "Thanksgiving: Williams finds Odunze with 3 seconds left", "CONFIRMED", "NA"),
    ("Ford unveils GT41 hypercar", "2027 Le Mans bid shown at Ford Field", "REPORTED", "NA"),
    ("Mexico president blasts DEA", "Says US does too little on fentanyl at home", "REPORTED", "NA"),
    ("FAA halts Miami flights", "Ground stop follows FedEx jet runway overrun", "REPORTED", "NA"),
    ("MLB lockout looms over salary cap", "Owners hold firm; shutdown set for Dec 2", "REPORTED", "NA"),
    ("De Cos picked to lead ECB", "Spain's ex-central bank chief succeeds Lagarde", "OFFICIAL", "EU"),
    ("Chess Game 3: 60-move draw", "Gukesh's surprise holds; score level 1.5\u20131.5", "ONGOING", "EU"),
    ("Russia hits Kyiv mall, 7 hurt", "113 drones fired overnight; grain ships hit", "REPORTED", "EU"),
    ("Depardieu ordered to stand trial", "French star faces rape and assault charges", "REPORTED", "EU"),
    ("UK net migration falls to 77,000", "Lowest since 1997 outside the pandemic", "OFFICIAL", "EU"),
    ("Tanker capsizes off Ibiza, 1 dead", "7,000 tonnes of diesel aboard the Med Emre", "REPORTED", "EU"),
    ("Solomon Islands signs treaty", "Canberra named main security partner", "OFFICIAL", "APAC"),
    ("Kim vows more nuclear weapons", "North Korea ignores Trump's overture", "REPORTED", "APAC"),
    ("Bogor mine flood kills 13", "13 more missing 100 metres underground", "REPORTED", "APAC"),
    ("Bangkok oil blast injures 9", "Fire erupts at a major oil facility", "REPORTED", "APAC"),
    ("Taiwan jails navy spy for 6 years", "Ex-sergeant passed secrets to China", "REPORTED", "APAC"),
    ("Philippines adds 3 patrol ships", "Coast guard commissions BRP Patag", "REPORTED", "APAC"),
    ("Swiss confirm AI-agent attacks", "Autonomous hacks hit local organisations", "REPORTED", "APAC"),
    ("France honours Mumbai victims", "26/11, 18th anniversary; two French died", "REPORTED", "APAC"),
    ("Brazil blasts US Embraer tariff", "Lula calls the 10% duty unacceptable", "REPORTED", "LATAM"),
    ("Milei bank overhaul approved", "Congress backs new central bank charter", "REPORTED", "LATAM"),
    ("Venezuela debt put at $237.5B", "Regime report reveals the scale of arrears", "REPORTED", "LATAM"),
    ("Opus Dei No. 2 summoned", "Priests to testify in Argentina probe", "REPORTED", "LATAM"),
    ("Brazil budget panel cuts $370M", "Nearly a third of the cut hits health", "REPORTED", "LATAM"),
    ("Bolivia bridge falls, 500 cut off", "Floodwater destroys crossing in Cochabamba", "REPORTED", "LATAM"),
    ("Israeli strikes kill 10 in Gaza", "Hamas official Abu Nada among the dead", "REPORTED", "ME"),
    ("Judges urge dropping bribe charge", "Case 4000 is the only bribery count", "REPORTED", "ME"),
    ("Houthis strike Saudi port of Jizan", "Coalition intercepts drones near Jeddah", "REPORTED", "ME"),
    ("Settlers smash West Bank homes", "Foundations wrecked; 53 attacks a week", "REPORTED", "ME"),
    ("Congo Ebola cases pass 12,000", "Second-largest outbreak on record", "REPORTED", "AFRICA"),
    ("Guinea-Bissau vote delayed", "Vote pushed to 2028; junta stays on", "REPORTED", "AFRICA"),
    ("Cairo crash driver detained", "Tanker fire killed 31; 27 vehicles charred", "REPORTED", "AFRICA"),
]

NUMBERS = [
    ("100th", "Macy's parade"),
    ("2", "Italians killed in Kuwait"),
    ("250,000+", "without power in US storm"),
    ("$49B", "Ukraine loan on the table"),
    ("12,000", "Ebola cases in Congo"),
    ("31", "killed in Cairo crash"),
]

MAP_DOTS = [
    (1, "NEW YORK", 185, 42),
    (2, "KUWAIT CITY", 585, 62),
    (3, "BRUSSELS", 478, 26),
    (4, "GENEVA", 500, 50),
    (5, "MEXICO CITY", 140, 62),
    (6, "BUENOS AIRES", 245, 108),
    (7, "BRAS\u00cdLIA", 270, 88),
    (8, "CARACAS", 225, 72),
    (9, "BANGKOK", 720, 62),
    (10, "KINSHASA", 510, 92),
]


# ---------------------------------------------------------------- illustrations
def draw_storm_panel(d, x, y, w, h):
    """Nor'easter over the New York skyline: rain, wind, a grounded balloon."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 74, 96))
    # storm clouds
    for cx, cy, r in [(60, 22, 26), (110, 18, 30), (180, 24, 28), (250, 16, 30)]:
        d.ellipse([x + cx - r, y + cy - r // 2, x + cx + r, y + cy + r // 2], fill=(38, 50, 70))
        d.ellipse([x + cx - r // 2, y + cy - r, x + cx + r // 2, y + cy], fill=(48, 62, 84))
    # lightning bolt
    d.polygon([(x + 268, y + 8), (x + 282, y + 8), (x + 272, y + 34), (x + 284, y + 34),
               (x + 262, y + 66), (x + 270, y + 40), (x + 260, y + 40)], fill=(250, 214, 80))
    # skyline with lit windows
    base = y + h - 34
    for bx, bw, bh in [(0, 42, 58), (46, 30, 78), (80, 36, 52), (120, 28, 84),
                       (152, 40, 62), (196, 30, 74), (230, 34, 56), (268, 40, 66)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(24, 32, 48))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(bx + 6, bx + bw - 6, 12):
                if (wx + wy) % 3 == 0:
                    d.rectangle([x + wx, wy, x + wx + 5, wy + 6], fill=(250, 200, 90))
    # street
    d.rectangle([x, base, x + w, y + h], fill=(20, 26, 40))
    d.rectangle([x, base, x + w, base + 3], fill=(120, 120, 110))
    # deflated balloon on a trailer: drooping red shape + ropes + wheels
    d.polygon([(x + 96, base - 22), (x + 150, base - 30), (x + 196, base - 20),
               (x + 190, base - 8), (x + 104, base - 6)], fill=(179, 32, 44))
    d.ellipse([x + 128, base - 34, x + 168, base - 18], fill=(200, 60, 66))
    d.rectangle([x + 92, base - 6, x + 200, base], fill=(70, 70, 66))
    for wx in (104, 128, 160, 184):
        d.ellipse([x + wx, base + 2, x + wx + 12, base + 14], fill=(10, 10, 12))
        d.ellipse([x + wx + 3, base + 5, x + wx + 9, base + 11], fill=(120, 120, 116))
    # sagging power line + pole
    d.rectangle([x + 286, y + 40, x + 290, base], fill=(16, 20, 30))
    d.arc([x + 250, y + 44, x + 318, y + 84], 20, 160, fill=(16, 20, 30), width=2)
    # rain streaks
    for rx, ry in [(20, 30), (70, 55), (130, 38), (210, 60), (240, 30), (300, 55), (40, 75), (170, 80)]:
        d.line([(x + rx, y + ry), (x + rx - 6, y + ry + 14)], fill=(190, 210, 228), width=2)


def draw_kuwait_panel(d, x, y, w, h):
    """Drone over a Kuwait skyline at dusk: sun, domes, minaret, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 178, 110))
    d.ellipse([x + 252, y + 10, x + 292, y + 50], fill=(250, 214, 130))
    # distant skyline
    d.rectangle([x, y + h - 62, x + w, y + h], fill=(196, 138, 84))
    for bx, bw, bh in [(0, 46, 34), (50, 30, 48), (84, 40, 30), (128, 26, 52),
                       (158, 44, 36), (206, 30, 46), (240, 36, 30), (280, 32, 40)]:
        d.rectangle([x + bx, y + h - 62 - bh, x + bx + bw, y + h - 62], fill=(150, 100, 60))
    # dome + minaret
    d.pieslice([x + 96, y + h - 108, x + 136, y + h - 68], 180, 360, fill=(120, 84, 52))
    d.rectangle([x + 114, y + h - 116, x + 118, y + h - 104], fill=(120, 84, 52))
    d.rectangle([x + 226, y + 6, x + 234, y + h - 62], fill=(120, 84, 52))
    d.ellipse([x + 222, y + 2, x + 238, y + 14], fill=(120, 84, 52))
    # ground + road
    d.rectangle([x, y + h - 62, x + w, y + h], fill=(222, 196, 148))
    d.rectangle([x, y + h - 30, x + w, y + h - 26], fill=(90, 70, 50))
    for gx in range(8, w, 34):
        d.rectangle([x + gx, y + h - 29, x + gx + 16, y + h - 27], fill=(248, 242, 228))
    # quadcopter drone with four rotors and a hanging payload
    cx, cy = x + 160, y + 42
    d.ellipse([cx - 26, cy - 10, cx + 26, cy + 10], fill=(40, 40, 44))
    d.ellipse([cx - 8, cy - 5, cx + 8, cy + 5], fill=(120, 120, 116))
    for dx, dy in [(-34, -16), (34, -16), (-34, 16), (34, 16)]:
        d.line([(cx, cy), (cx + dx, cy + dy)], fill=(40, 40, 44), width=3)
        d.ellipse([cx + dx - 16, cy + dy - 3, cx + dx + 16, cy + dy + 3], fill=(70, 70, 72))
    d.line([(cx, cy + 10), (cx, cy + 30)], fill=(40, 40, 44), width=2)
    d.rectangle([cx - 8, cy + 30, cx + 8, cy + 40], fill=(90, 30, 30))
    # smoke plume from the struck site
    for sx, sy, r in [(60, 78, 10), (70, 66, 14), (84, 54, 18), (100, 44, 12)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(120, 112, 104))
    # birds
    for bx, by in [(220, 22), (244, 34), (206, 40)]:
        d.arc([x + bx - 8, y + by - 5, x + bx, y + by + 5], 200, 340, fill=(60, 40, 30), width=2)
        d.arc([x + bx, y + by - 5, x + bx + 8, y + by + 5], 200, 340, fill=(60, 40, 30), width=2)


def draw_eu_panel(d, x, y, w, h):
    """EU summit hall: blue field, ring of gold stars, hemicycle, flags, table."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 96))
    # ring of twelve gold stars
    import math
    for k in range(12):
        ang = math.pi * 2 * k / 12 - math.pi / 2
        sx = x + 160 + int(118 * math.cos(ang))
        sy = y + 62 + int(44 * math.sin(ang))
        d.polygon([(sx, sy - 7), (sx + 2, sy - 2), (sx + 7, sy - 2), (sx + 3, sy + 2),
                   (sx + 5, sy + 7), (sx, sy + 4), (sx - 5, sy + 7), (sx - 3, sy + 2),
                   (sx - 7, sy - 2), (sx - 2, sy - 2)], fill=(250, 204, 60))
    # hemicycle building: columns + dome
    d.rectangle([x + 70, y + 78, x + 250, y + h - 26], fill=(232, 226, 208))
    d.polygon([(x + 70, y + 78), (x + 160, y + 52), (x + 250, y + 78)], fill=(200, 192, 172))
    d.ellipse([x + 146, y + 40, x + 174, y + 62], fill=(250, 204, 60))
    for cx in range(84, 250, 24):
        d.rectangle([x + cx, y + 84, x + cx + 8, y + h - 30], fill=(180, 172, 150))
    d.rectangle([x + 70, y + h - 30, x + 250, y + h - 26], fill=(150, 142, 122))
    # long table with documents, microphones, flags
    d.rectangle([x + 30, y + h - 24, x + 290, y + h - 12], fill=(120, 60, 40))
    for tx in (44, 90, 136, 182, 228, 264):
        d.rectangle([x + tx, y + h - 34, x + tx + 22, y + h - 24], fill=(248, 242, 228))
        d.line([(x + tx + 4, y + h - 32), (x + tx + 18, y + h - 32)], fill=(120, 120, 116), width=1)
    for fx in (56, 150, 244):
        d.line([(x + fx, y + h - 24), (x + fx, y + h - 44)], fill=(60, 60, 60), width=2)
        d.polygon([(x + fx, y + h - 44), (x + fx + 16, y + h - 40), (x + fx, y + h - 36)], fill=(179, 32, 44))
    # two leader silhouettes in debate
    for px, col in [(100, (40, 40, 44)), (210, (60, 40, 40))]:
        d.ellipse([x + px - 9, y + h - 66, x + px + 9, y + h - 48], fill=col)
        d.polygon([(x + px - 14, y + h - 48), (x + px + 14, y + h - 48),
                   (x + px + 10, y + h - 24), (x + px - 10, y + h - 24)], fill=col)


# ---------------------------------------------------------------- also-on thumbnails
# One flat 23x23 pictogram per ALSO ON story, same flat style as the lead
# panels (solid shapes, no photos). The list renderer draws the red number
# badge over the thumb's bottom-right corner.
THUMB_KINDS = [
    "tariff", "football", "hypercar", "podium", "grounded_plane", "baseball",
    "bank", "chess", "rocket", "gavel", "migration", "tanker",
    "flags", "nuclear", "mine", "oil", "warship", "patrol",
    "laptop", "candle", "jet", "bank_gear", "money", "church",
    "budget", "bridge", "burst", "scales", "crane", "house_crack",
    "virus", "ballot", "truck",
]


def draw_thumb(d, x, y, kind):
    """Draw a 23x23 flat pictogram for one ALSO ON story at (x, y)."""
    if kind == "tariff":  # US proposes tariffs: shipping box with %
        d.rectangle([x, y, x + 22, y + 22], fill=(245, 222, 200), outline=INK)
        d.rectangle([x + 3, y + 8, x + 19, y + 19], fill=(176, 120, 60))
        d.line([(x + 11, y + 8), (x + 11, y + 19)], fill=(120, 80, 40), width=2)
        f = font(SANS_B, 9)
        d.text((x + 11 - d.textlength("%", font=f) / 2, y + 10), "%", font=f,
               fill=(255, 255, 255))
    elif kind == "football":  # Bears stun Lions: American football
        d.rectangle([x, y, x + 22, y + 22], fill=(222, 238, 222), outline=INK)
        d.ellipse([x + 3, y + 8, x + 20, y + 16], fill=(120, 72, 32))
        d.line([(x + 9, y + 12), (x + 15, y + 12)], fill=(255, 255, 255), width=1)
        for lx in (10, 12, 14):
            d.line([(x + lx, y + 10), (x + lx, y + 14)], fill=(255, 255, 255), width=1)
    elif kind == "hypercar":  # Ford GT41: low race car
        d.rectangle([x, y, x + 22, y + 22], fill=(214, 232, 242), outline=INK)
        d.polygon([(x + 2, y + 16), (x + 4, y + 11), (x + 8, y + 9), (x + 14, y + 9),
                   (x + 17, y + 12), (x + 21, y + 13), (x + 21, y + 16)], fill=RED)
        d.rectangle([x + 8, y + 6, x + 14, y + 9], fill=INK)
        for wx in (6, 17):
            d.ellipse([x + wx - 3, y + 14, x + wx + 3, y + 20], fill=INK)
            d.ellipse([x + wx - 1, y + 16, x + wx + 1, y + 18], fill=(255, 255, 255))
    elif kind == "podium":  # Mexico president blasts DEA: podium + mic
        d.rectangle([x, y, x + 22, y + 22], fill=(228, 224, 240), outline=INK)
        d.polygon([(x + 6, y + 20), (x + 8, y + 11), (x + 15, y + 11), (x + 17, y + 20)],
                  fill=BLUE)
        d.line([(x + 11, y + 11), (x + 11, y + 6)], fill=INK, width=2)
        d.ellipse([x + 9, y + 2, x + 13, y + 6], fill=INK)
    elif kind == "grounded_plane":  # FAA halts Miami flights: plane + red stop line
        d.rectangle([x, y, x + 22, y + 22], fill=(214, 232, 242), outline=INK)
        d.ellipse([x + 3, y + 9, x + 20, y + 13], fill=INK)
        d.polygon([(x + 9, y + 11), (x + 13, y + 4), (x + 15, y + 4), (x + 13, y + 11)],
                  fill=INK)
        d.polygon([(x + 16, y + 10), (x + 20, y + 5), (x + 21, y + 7), (x + 18, y + 11)],
                  fill=INK)
        d.line([(x + 2, y + 19), (x + 21, y + 19)], fill=RED, width=2)
    elif kind == "baseball":  # MLB lockout: stitched baseball
        d.rectangle([x, y, x + 22, y + 22], fill=(238, 232, 214), outline=INK)
        d.ellipse([x + 4, y + 4, x + 19, y + 19], fill=(255, 255, 255), outline=RED, width=1)
        d.arc([x + 6, y + 6, x + 12, y + 17], 300, 60, fill=RED, width=1)
        d.arc([x + 11, y + 6, x + 17, y + 17], 120, 240, fill=RED, width=1)
    elif kind == "bank":  # De Cos to lead ECB: bank building
        d.rectangle([x, y, x + 22, y + 22], fill=(210, 224, 240), outline=INK)
        d.polygon([(x + 3, y + 10), (x + 11, y + 4), (x + 20, y + 10)], fill=INK)
        for cx in (5, 10, 15):
            d.rectangle([x + cx, y + 11, x + cx + 2, y + 18], fill=INK)
        d.rectangle([x + 3, y + 19, x + 20, y + 21], fill=INK)
    elif kind == "chess":  # Chess Game 3 draw: checkerboard
        d.rectangle([x, y, x + 22, y + 22], fill=(238, 232, 214), outline=INK)
        d.rectangle([x + 4, y + 4, x + 11, y + 11], fill=(255, 255, 255), outline=INK)
        d.rectangle([x + 11, y + 4, x + 18, y + 11], fill=INK)
        d.rectangle([x + 4, y + 11, x + 11, y + 18], fill=INK)
        d.rectangle([x + 11, y + 11, x + 18, y + 18], fill=(255, 255, 255), outline=INK)
    elif kind == "rocket":  # Russia hits Kyiv: missile + flame
        d.rectangle([x, y, x + 22, y + 22], fill=(240, 210, 210), outline=INK)
        d.rectangle([x + 10, y + 5, x + 13, y + 14], fill=INK)
        d.polygon([(x + 10, y + 5), (x + 13, y + 5), (x + 11, y + 1)], fill=RED)
        d.polygon([(x + 10, y + 14), (x + 7, y + 18), (x + 10, y + 16)], fill=INK)
        d.polygon([(x + 13, y + 14), (x + 16, y + 18), (x + 13, y + 16)], fill=INK)
        d.polygon([(x + 10, y + 15), (x + 13, y + 15), (x + 11, y + 20)], fill=ORANGE)
    elif kind == "gavel":  # Depardieu trial: gavel + block
        d.rectangle([x, y, x + 22, y + 22], fill=(228, 224, 240), outline=INK)
        d.polygon([(x + 5, y + 8), (x + 12, y + 4), (x + 14, y + 7), (x + 7, y + 11)],
                  fill=INK)
        d.line([(x + 9, y + 10), (x + 17, y + 18)], fill=INK, width=2)
        d.rectangle([x + 13, y + 19, x + 21, y + 21], fill=(120, 80, 40))
    elif kind == "migration":  # UK net migration falls: plane + down arrow
        d.rectangle([x, y, x + 22, y + 22], fill=(214, 232, 242), outline=INK)
        d.ellipse([x + 3, y + 6, x + 18, y + 10], fill=INK)
        d.polygon([(x + 9, y + 8), (x + 12, y + 3), (x + 14, y + 3), (x + 12, y + 8)],
                  fill=INK)
        d.line([(x + 11, y + 12), (x + 11, y + 19)], fill=BLUE, width=2)
        d.polygon([(x + 8, y + 16), (x + 14, y + 16), (x + 11, y + 21)], fill=BLUE)
    elif kind == "tanker":  # Tanker capsizes off Ibiza: hull + waves
        d.rectangle([x, y, x + 22, y + 22], fill=(178, 214, 230), outline=INK)
        d.polygon([(x + 3, y + 11), (x + 19, y + 11), (x + 17, y + 16), (x + 5, y + 16)],
                  fill=(120, 60, 40))
        d.rectangle([x + 5, y + 8, x + 9, y + 11], fill=(120, 60, 40))
        d.line([(x + 2, y + 19), (x + 8, y + 19), (x + 11, y + 21), (x + 17, y + 21)],
               fill=BLUE, width=1)
        d.polygon([(x + 16, y + 8), (x + 20, y + 9), (x + 16, y + 11)], fill=RED)
    elif kind == "flags":  # Solomon Islands treaty: two crossed flags
        d.rectangle([x, y, x + 22, y + 22], fill=(238, 232, 214), outline=INK)
        d.line([(x + 7, y + 5), (x + 7, y + 20)], fill=INK, width=2)
        d.line([(x + 15, y + 5), (x + 15, y + 20)], fill=INK, width=2)
        d.polygon([(x + 7, y + 5), (x + 13, y + 7), (x + 7, y + 9)], fill=RED)
        d.polygon([(x + 15, y + 5), (x + 9, y + 7), (x + 15, y + 9)], fill=BLUE)
    elif kind == "nuclear":  # Kim vows more nuclear weapons: rocket + star
        d.rectangle([x, y, x + 22, y + 22], fill=(240, 210, 210), outline=INK)
        d.rectangle([x + 10, y + 5, x + 13, y + 15], fill=(60, 60, 64))
        d.polygon([(x + 10, y + 5), (x + 13, y + 5), (x + 11, y + 1)], fill=RED)
        d.polygon([(x + 10, y + 15), (x + 13, y + 15), (x + 11, y + 20)], fill=ORANGE)
        for sx, sy, r in [(6, 18, 3), (10, 20, 2), (15, 19, 2)]:
            d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(120, 112, 104))
        d.polygon([(x + 18, y + 2), (x + 19, y + 5), (x + 21, y + 5), (x + 19, y + 7),
                   (x + 20, y + 10), (x + 18, y + 8), (x + 16, y + 10), (x + 17, y + 7),
                   (x + 15, y + 5), (x + 17, y + 5)], fill=(250, 204, 60))
    elif kind == "mine":  # Bogor mine flood: mountain + tunnel + water
        d.rectangle([x, y, x + 22, y + 22], fill=(222, 238, 222), outline=INK)
        d.polygon([(x + 2, y + 20), (x + 11, y + 5), (x + 21, y + 20)], fill=(120, 100, 70))
        d.pieslice([x + 8, y + 13, x + 15, y + 21], 180, 360, fill=INK)
        d.line([(x + 2, y + 21), (x + 21, y + 21)], fill=(28, 80, 160), width=1)
    elif kind == "oil":  # Bangkok oil blast: derrick + flame
        d.rectangle([x, y, x + 22, y + 22], fill=(245, 222, 200), outline=INK)
        d.line([(x + 5, y + 19), (x + 9, y + 7)], fill=INK, width=2)
        d.line([(x + 13, y + 19), (x + 9, y + 7)], fill=INK, width=2)
        d.line([(x + 6, y + 15), (x + 12, y + 15)], fill=INK, width=1)
        d.polygon([(x + 16, y + 12), (x + 19, y + 5), (x + 21, y + 12), (x + 19, y + 10)],
                  fill=ORANGE)
        d.polygon([(x + 17, y + 12), (x + 19, y + 8), (x + 20, y + 12)], fill=(250, 204, 60))
    elif kind == "warship":  # Taiwan navy spy: warship + flag
        d.rectangle([x, y, x + 22, y + 22], fill=(178, 214, 230), outline=INK)
        d.polygon([(x + 2, y + 13), (x + 20, y + 13), (x + 18, y + 17), (x + 4, y + 17)],
                  fill=(60, 70, 80))
        d.rectangle([x + 9, y + 8, x + 13, y + 13], fill=(60, 70, 80))
        d.line([(x + 11, y + 8), (x + 11, y + 4)], fill=(60, 70, 80), width=2)
        d.polygon([(x + 11, y + 4), (x + 15, y + 5), (x + 11, y + 6)], fill=RED)
        d.line([(x + 3, y + 20), (x + 9, y + 20), (x + 12, y + 18), (x + 19, y + 18)],
               fill=BLUE, width=1)
    elif kind == "patrol":  # Philippines patrol ships: white boat + waves
        d.rectangle([x, y, x + 22, y + 22], fill=(178, 214, 230), outline=INK)
        d.polygon([(x + 3, y + 13), (x + 19, y + 13), (x + 17, y + 17), (x + 5, y + 17)],
                  fill=(255, 255, 255), outline=INK)
        d.rectangle([x + 9, y + 8, x + 14, y + 13], fill=BLUE)
        d.line([(x + 3, y + 20), (x + 9, y + 20), (x + 12, y + 18), (x + 19, y + 18)],
               fill=BLUE, width=1)
    elif kind == "laptop":  # Swiss AI-agent attacks: laptop + warning
        d.rectangle([x, y, x + 22, y + 22], fill=(228, 224, 240), outline=INK)
        d.rectangle([x + 4, y + 6, x + 19, y + 15], fill=INK)
        d.rectangle([x + 6, y + 8, x + 17, y + 13], fill=(168, 205, 226))
        d.polygon([(x + 3, y + 16), (x + 20, y + 16), (x + 21, y + 18), (x + 2, y + 18)],
                  fill=INK)
        d.polygon([(x + 15, y + 13), (x + 19, y + 13), (x + 17, y + 9)], fill=(250, 204, 60))
    elif kind == "candle":  # France honours Mumbai victims: memorial candle
        d.rectangle([x, y, x + 22, y + 22], fill=(238, 232, 214), outline=INK)
        d.ellipse([x + 10, y + 3, x + 14, y + 8], fill=(250, 180, 60))
        d.line([(x + 12, y + 8), (x + 12, y + 10)], fill=INK, width=1)
        d.rectangle([x + 10, y + 10, x + 13, y + 19], fill=(255, 255, 255), outline=INK)
        d.rectangle([x + 8, y + 20, x + 15, y + 21], fill=INK)
    elif kind == "jet":  # Brazil blasts Embraer tariff: passenger jet
        d.rectangle([x, y, x + 22, y + 22], fill=(214, 232, 242), outline=INK)
        d.polygon([(x + 2, y + 12), (x + 18, y + 9), (x + 21, y + 11), (x + 18, y + 13),
                   (x + 2, y + 14)], fill=INK)
        d.polygon([(x + 9, y + 11), (x + 13, y + 4), (x + 15, y + 4), (x + 12, y + 11)],
                  fill=INK)
        d.polygon([(x + 4, y + 11), (x + 6, y + 6), (x + 8, y + 6), (x + 7, y + 11)],
                  fill=INK)
        d.ellipse([x + 15, y + 10, x + 17, y + 12], fill=(255, 255, 255))
    elif kind == "bank_gear":  # Milei bank overhaul: bank + gear
        d.rectangle([x, y, x + 22, y + 22], fill=(210, 224, 240), outline=INK)
        d.polygon([(x + 2, y + 9), (x + 8, y + 4), (x + 14, y + 9)], fill=INK)
        for cx in (4, 7, 10):
            d.rectangle([x + cx, y + 10, x + cx + 2, y + 16], fill=INK)
        d.rectangle([x + 2, y + 17, x + 14, y + 19], fill=INK)
        d.ellipse([x + 15, y + 14, x + 21, y + 20], fill=(250, 204, 60))
        d.ellipse([x + 17, y + 16, x + 19, y + 18], fill=(210, 224, 240))
    elif kind == "money":  # Venezuela debt: banknote with $
        d.rectangle([x, y, x + 22, y + 22], fill=(222, 238, 222), outline=INK)
        d.rectangle([x + 3, y + 7, x + 20, y + 17], fill=(28, 110, 68))
        d.rectangle([x + 5, y + 9, x + 18, y + 15], outline=(255, 255, 255), width=1)
        f = font(SANS_B, 9)
        d.text((x + 11 - d.textlength("$", font=f) / 2, y + 8), "$", font=f,
               fill=(255, 255, 255))
    elif kind == "church":  # Opus Dei probe: church + cross
        d.rectangle([x, y, x + 22, y + 22], fill=(228, 224, 240), outline=INK)
        d.rectangle([x + 6, y + 11, x + 17, y + 20], fill=(200, 190, 170), outline=INK)
        d.polygon([(x + 5, y + 11), (x + 11, y + 5), (x + 18, y + 11)], fill=RED)
        d.line([(x + 11, y + 1), (x + 11, y + 5)], fill=INK, width=2)
        d.line([(x + 9, y + 3), (x + 13, y + 3)], fill=INK, width=2)
        d.rectangle([x + 10, y + 15, x + 13, y + 20], fill=INK)
    elif kind == "budget":  # Brazil budget cuts: bars + falling arrow
        d.rectangle([x, y, x + 22, y + 22], fill=(240, 210, 210), outline=INK)
        d.rectangle([x + 4, y + 13, x + 7, y + 20], fill=BLUE)
        d.rectangle([x + 9, y + 10, x + 12, y + 20], fill=BLUE)
        d.rectangle([x + 14, y + 7, x + 17, y + 20], fill=BLUE)
        d.line([(x + 4, y + 4), (x + 19, y + 16)], fill=RED, width=2)
        d.polygon([(x + 16, y + 16), (x + 20, y + 16), (x + 19, y + 20)], fill=RED)
    elif kind == "bridge":  # Bolivia bridge falls: broken deck + water
        d.rectangle([x, y, x + 22, y + 22], fill=(214, 232, 242), outline=INK)
        d.rectangle([x + 2, y + 9, x + 10, y + 11], fill=INK)
        d.rectangle([x + 13, y + 9, x + 21, y + 11], fill=INK)
        d.polygon([(x + 10, y + 9), (x + 12, y + 13), (x + 10, y + 15)], fill=INK)
        d.line([(x + 4, y + 11), (x + 4, y + 18)], fill=INK, width=1)
        d.line([(x + 19, y + 11), (x + 19, y + 18)], fill=INK, width=1)
        d.line([(x + 3, y + 20), (x + 9, y + 20), (x + 12, y + 18), (x + 19, y + 18)],
               fill=BLUE, width=1)
    elif kind == "burst":  # Israeli strikes in Gaza: explosion burst
        d.rectangle([x, y, x + 22, y + 22], fill=(240, 210, 210), outline=INK)
        d.rectangle([x + 3, y + 17, x + 20, y + 20], fill=(60, 60, 64))
        cx, cy = x + 11, y + 10
        d.polygon([(cx, cy - 8), (cx + 2, cy - 3), (cx + 8, cy - 5), (cx + 4, cy - 1),
                   (cx + 8, cy + 3), (cx + 3, cy + 3), (cx + 4, cy + 8), (cx, cy + 4),
                   (cx - 4, cy + 8), (cx - 3, cy + 3), (cx - 8, cy + 3), (cx - 4, cy - 1),
                   (cx - 8, cy - 5), (cx - 2, cy - 3)], fill=ORANGE)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(250, 204, 60))
    elif kind == "scales":  # Judges urge dropping bribe charge: scales
        d.rectangle([x, y, x + 22, y + 22], fill=(238, 232, 214), outline=INK)
        d.line([(x + 11, y + 4), (x + 11, y + 18)], fill=INK, width=2)
        d.line([(x + 4, y + 6), (x + 18, y + 6)], fill=INK, width=2)
        d.polygon([(x + 4, y + 6), (x + 2, y + 11), (x + 6, y + 11)], fill=INK)
        d.polygon([(x + 18, y + 6), (x + 16, y + 11), (x + 20, y + 11)], fill=INK)
        d.rectangle([x + 8, y + 18, x + 14, y + 20], fill=INK)
    elif kind == "crane":  # Houthis strike Saudi port: harbour crane
        d.rectangle([x, y, x + 22, y + 22], fill=(178, 214, 230), outline=INK)
        d.line([(x + 6, y + 4), (x + 6, y + 19)], fill=INK, width=2)
        d.line([(x + 6, y + 5), (x + 20, y + 5)], fill=INK, width=2)
        d.line([(x + 16, y + 5), (x + 16, y + 10)], fill=INK, width=1)
        d.rectangle([x + 13, y + 10, x + 19, y + 14], fill=RED)
        d.rectangle([x + 3, y + 17, x + 9, y + 20], fill=BLUE)
        d.rectangle([x + 10, y + 17, x + 16, y + 20], fill=ORANGE)
    elif kind == "house_crack":  # Settlers smash homes: cracked house
        d.rectangle([x, y, x + 22, y + 22], fill=(245, 222, 200), outline=INK)
        d.rectangle([x + 5, y + 11, x + 18, y + 20], fill=(200, 180, 150), outline=INK)
        d.polygon([(x + 4, y + 11), (x + 11, y + 5), (x + 19, y + 11)], fill=RED)
        d.line([(x + 11, y + 11), (x + 13, y + 14), (x + 10, y + 16), (x + 12, y + 19)],
               fill=INK, width=2)
        d.rectangle([x + 3, y + 20, x + 6, y + 21], fill=INK)
        d.rectangle([x + 17, y + 20, x + 20, y + 21], fill=INK)
    elif kind == "virus":  # Congo Ebola: spiky virus ball
        import math
        d.rectangle([x, y, x + 22, y + 22], fill=(240, 210, 210), outline=INK)
        cx, cy = x + 11, y + 11
        for k in range(8):
            ang = math.pi * k / 4
            x1 = cx + int(7 * math.cos(ang))
            y1 = cy + int(7 * math.sin(ang))
            x2 = cx + int(10 * math.cos(ang))
            y2 = cy + int(10 * math.sin(ang))
            d.line([(x1, y1), (x2, y2)], fill=RED, width=2)
        d.ellipse([x + 4, y + 4, x + 18, y + 18], fill=RED)
        d.ellipse([x + 8, y + 8, x + 10, y + 10], fill=(255, 255, 255))
        d.ellipse([x + 13, y + 12, x + 15, y + 14], fill=(255, 255, 255))
    elif kind == "ballot":  # Guinea-Bissau vote delayed: ballot box
        d.rectangle([x, y, x + 22, y + 22], fill=(238, 232, 214), outline=INK)
        d.polygon([(x + 9, y + 3), (x + 14, y + 3), (x + 13, y + 9), (x + 10, y + 9)],
                  fill=(255, 255, 255), outline=INK)
        d.line([(x + 10, y + 6), (x + 11, y + 8), (x + 13, y + 5)], fill=GREEN, width=1)
        d.rectangle([x + 5, y + 10, x + 18, y + 20], fill=BLUE)
        d.rectangle([x + 8, y + 10, x + 15, y + 11], fill=INK)
    elif kind == "truck":  # Cairo crash: tanker truck + flame
        d.rectangle([x, y, x + 22, y + 22], fill=(245, 222, 200), outline=INK)
        d.polygon([(x + 8, y + 8), (x + 10, y + 3), (x + 12, y + 8)], fill=ORANGE)
        d.ellipse([x + 4, y + 9, x + 16, y + 15], fill=(200, 200, 200), outline=INK)
        d.polygon([(x + 16, y + 10), (x + 20, y + 10), (x + 21, y + 15), (x + 16, y + 15)],
                  fill=RED)
        d.ellipse([x + 5, y + 15, x + 9, y + 19], fill=INK)
        d.ellipse([x + 16, y + 15, x + 20, y + 19], fill=INK)
    else:
        d.rectangle([x, y, x + 22, y + 22], fill=LIGHT, outline=INK)


# ---------------------------------------------------------------- page assembly
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_serif_b = font(SERIF_B, 56)
    f_sans_b = font(SANS_B, 13)
    f_sans_b14 = font(SANS_B, 14)
    f_sans_b15 = font(SANS_B, 15)

    # masthead
    d.text((24, 8), "THE WORLD IN ONE DAY", font=f_sans_b, fill=INK)
    d.text((W - 24 - d.textlength("THURSDAY", font=f_sans_b), 8), "THURSDAY",
           font=f_sans_b, fill=INK)
    title = "26 NOVEMBER 2026"
    d.text(((W - d.textlength(title, font=f_serif_b)) / 2, 24), title,
           font=f_serif_b, fill=INK)
    d.line([(24, 90), (W - 24, 90)], fill=INK, width=2)
    stat = "36 STORIES  \u00b7  6 REGIONS  \u00b7  3 LEADS  \u00b7  0 FROM ANOTHER DAY"
    d.text(((W - d.textlength(stat, font=f_sans_b15)) / 2, 96), stat,
           font=f_sans_b15, fill=INK)
    d.line([(24, 118), (W - 24, 118)], fill=INK, width=1)

    # red DATE CHECK bar
    d.rectangle([24, 124, W - 24, 150], fill=RED)
    check = "DATE CHECK \u2014 EVERY STORY ON THIS PAGE WAS REPORTED ON THURSDAY, 26 NOVEMBER 2026"
    d.text(((W - d.textlength(check, font=f_sans_b)) / 2, 132), check,
           font=f_sans_b, fill=(255, 255, 255))

    # three lead panels
    panel_w, panel_h, gap = 320, 240, 8
    painters = [draw_storm_panel, draw_kuwait_panel, draw_eu_panel]
    for i, (headline, context, city, label) in enumerate(LEADS):
        px = 24 + i * (panel_w + gap)
        py = 158
        d.rectangle([px, py, px + panel_w, py + panel_h], outline=INK, width=2)
        painters[i](d, px + 1, py + 1, panel_w - 2, 122)
        ty = py + 128
        f_chip = font(SANS_B, 11)
        d.rectangle([px + 8, ty, px + 8 + d.textlength(label, font=f_chip) + 10, ty + 17],
                    fill=LABEL_COLORS[label])
        d.text((px + 13, ty + 2), label, font=f_chip, fill=(255, 255, 255))
        d.text((px + panel_w - 8 - d.textlength(city, font=f_chip), ty + 2), city,
               font=f_chip, fill=GREY)
        f_head = font(SERIF_B, 19)
        lines = wrap(d, headline, f_head, panel_w - 16)
        hy = ty + 22
        for ln in lines[:2]:
            d.text((px + 8, hy), ln, font=f_head, fill=INK)
            hy += 23
        f_body = font(SANS, 12)
        for ln in wrap(d, context, f_body, panel_w - 16)[:3]:
            d.text((px + 8, hy), ln, font=f_body, fill=(60, 60, 58))
            hy += 14

    # IN NUMBERS strip
    ny = 412
    d.text((24, ny), "\u25a0  IN NUMBERS", font=f_sans_b14, fill=INK)
    d.text((W - 24 - d.textlength("only confirmed figures", font=font(SANS, 11)), ny + 2),
           "only confirmed figures", font=font(SANS, 11), fill=GREY)
    d.line([(24, ny + 20), (W - 24, ny + 20)], fill=INK, width=1)
    cell_w = 976 // 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx = 24 + i * cell_w
        f_num = font(SERIF_B, 30)
        d.text((cx + (cell_w - d.textlength(num, font=f_num)) / 2, ny + 26), num,
               font=f_num, fill=RED)
        f_cap = font(SANS, 10)
        for j, ln in enumerate(wrap(d, cap, f_cap, cell_w - 14)):
            d.text((cx + (cell_w - d.textlength(ln, font=f_cap)) / 2, ny + 62 + j * 12),
                   ln, font=f_cap, fill=(60, 60, 58))
        if i:
            d.line([(cx, ny + 26), (cx, ny + 88)], fill=(200, 194, 178), width=1)

    # WHERE IT HAPPENED map
    my = 506
    d.text((24, my), "\u25a0  WHERE IT HAPPENED", font=f_sans_b14, fill=INK)
    d.text((W - 24 - d.textlength("numbers match the story list", font=font(SANS, 11)), my + 2),
           "numbers match the story list", font=font(SANS, 11), fill=GREY)
    mx, myy, mw, mh = 24, my + 22, 976, 96
    d.rectangle([mx, myy, mx + mw, myy + mh], fill=SEA, outline=INK, width=1)
    continents = [
        [(60, 20), (150, 8), (210, 25), (190, 55), (120, 60), (70, 45)],
        [(210, 70), (260, 65), (280, 95), (240, 120), (215, 95)],
        [(460, 15), (520, 10), (540, 35), (500, 50), (465, 40)],
        [(470, 60), (540, 55), (560, 95), (520, 120), (480, 100)],
        [(560, 10), (760, 5), (820, 30), (780, 70), (650, 75), (580, 45)],
        [(760, 95), (830, 90), (850, 110), (790, 118)],
    ]
    for poly in continents:
        d.polygon([(mx + px * 0.8, myy + py * 0.8) for px, py in poly], fill=LAND,
                  outline=(180, 158, 116))
    f_dot = font(SANS_B, 10)
    for num, _name, dx, dy in MAP_DOTS:
        dx, dy = dx * 0.8, dy * 0.8
        d.ellipse([mx + dx - 9, myy + dy - 9, mx + dx + 9, myy + dy + 9],
                  fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        d.text((mx + dx - d.textlength(t, font=f_dot) / 2, myy + dy - 6), t,
               font=f_dot, fill=(255, 255, 255))
    legend = "  \u00b7  ".join(f"{n} {name}" for n, name, _, _ in MAP_DOTS)
    d.text((24, myy + mh + 4), legend, font=font(SANS_B, 11), fill=INK)

    # ALSO ON list: 3 columns x 11 rows, each row with its own thumbnail
    ly = 644
    d.text((24, ly), "\u25a0  ALSO ON 26 NOVEMBER", font=f_sans_b14, fill=INK)
    d.text((W - 24 - d.textlength("33 MORE STORIES", font=f_sans_b14), ly),
           "33 MORE STORIES", font=f_sans_b14, fill=GREY)
    d.line([(24, ly + 20), (W - 24, ly + 20)], fill=INK, width=1)
    col_w = 976 // 3
    f_item = font(SANS_B, 12)
    f_det = font(SANS, 10)
    f_lab = font(SANS_B, 9)
    f_badge = font(SANS_B, 8)
    row_h = 27
    for idx, (headline, detail, label, _region) in enumerate(ALSO):
        col, row = idx % 3, idx // 3
        ix = 24 + col * col_w
        iy = ly + 26 + row * row_h
        num = str(idx + 4)
        draw_thumb(d, ix, iy + 2, THUMB_KINDS[idx])
        bx, by = ix + 18, iy + 19
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((bx - d.textlength(num, font=f_badge) / 2, by - 4), num,
               font=f_badge, fill=(255, 255, 255))
        tx = ix + 28
        lw = d.textlength(label, font=f_lab)
        limit = col_w - 28 - lw - 6
        head = headline
        while d.textlength(head, font=f_item) > limit and " " in head:
            head = head.rsplit(" ", 1)[0]
        if head != headline:
            head = head + "\u2026"
        d.text((tx, iy), head, font=f_item, fill=INK)
        d.text((ix + col_w - 4 - lw, iy + 1), label, font=f_lab,
               fill=LABEL_COLORS[label])
        d.text((tx, iy + 13), detail, font=f_det, fill=(90, 90, 86))

    # HOW THIS PAGE WAS CHECKED + footer
    cy = ly + 26 + 11 * row_h + 6
    d.rectangle([24, cy, W - 24, cy + 30], outline=INK, width=1)
    f_check = font(SANS, 10)
    d.text((30, cy + 3),
           "HOW THIS PAGE WAS CHECKED \u2014 Each story was checked against reporting dated 26 November 2026.",
           font=f_check, fill=INK)
    d.text((30, cy + 17),
           "Claims are labelled CLAIM, official announcements OFFICIAL, ongoing events ONGOING.",
           font=f_check, fill=INK)
    f_foot = font(SANS_B, 11)
    foot = "26 NOVEMBER 2026  \u00b7  THE WORLD IN ONE DAY  \u00b7  36 STORIES, 6 REGIONS"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, cy + 36), foot,
           font=f_foot, fill=INK)
    return img


if __name__ == "__main__":
    build().save("entry.png", optimize=True)
    print("wrote entry.png")
