#!/usr/bin/env python3
"""Front page for Friday 20 November 2026, drawn with the stdlib only.

Produces entry.png (1024x1024 RGB) beside this file.
Run: python3 draw.py
"""
import math
import struct
import zlib
from pathlib import Path

PAGE_W, PAGE_H = 1024, 1024

# --- palette ---
PAPER_RGB = (247, 243, 232)
INK_RGB = (22, 28, 38)
NAVY_RGB = (19, 31, 56)
NAVY2_RGB = (30, 46, 82)
GOLD_RGB = (242, 193, 78)
WHITE_RGB = (255, 255, 255)
GREY_RGB = (90, 96, 110)
RED_RGB = (185, 28, 28)
BLUE_RGB = (29, 78, 216)
TEAL_RGB = (15, 118, 110)
PURPLE_RGB = (123, 47, 190)
AMBER_RGB = (180, 83, 9)
DARK_RGB = (15, 23, 42)
ORANGE_RGB = (234, 88, 12)
BODY_RGB = (40, 44, 56)

# --- canvas: one bytearray per scanline ---
rows = [bytearray(PAGE_W * 3) for _ in range(PAGE_H)]


def set_px(x, y, rgb):
    if 0 <= x < PAGE_W and 0 <= y < PAGE_H:
        row = rows[y]
        row[x * 3:x * 3 + 3] = bytes(rgb)


def fill_rect(x, y, w, h, rgb):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(PAGE_W, x + w), min(PAGE_H, y + h)
    band = bytes(rgb) * (x1 - x0)
    for yy in range(y0, y1):
        rows[yy][x0 * 3:x1 * 3] = band


def fill_disc(cx, cy, r, rgb):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                set_px(xx, yy, rgb)


def disc_ring(cx, cy, r, thick, rgb):
    lo, hi = (r - thick) * (r - thick), (r + thick) * (r + thick)
    for yy in range(cy - r - thick, cy + r + thick + 1):
        for xx in range(cx - r - thick, cx + r + thick + 1):
            d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
            if lo <= d2 <= hi:
                set_px(xx, yy, rgb)


def draw_line(x0, y0, x1, y1, rgb, w=1):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    step_x = 1 if x0 < x1 else -1
    step_y = 1 if y0 < y1 else -1
    err = dx - dy
    half = w // 2
    while True:
        for a in range(-half, half + 1):
            for b in range(-half, half + 1):
                set_px(x0 + a, y0 + b, rgb)
        if x0 == x1 and y0 == y1:
            return
        twice = 2 * err
        if twice > -dy:
            err -= dy
            x0 += step_x
        if twice < dx:
            err += dx
            y0 += step_y


def fill_poly(pts, rgb):
    top, bottom = min(p[1] for p in pts), max(p[1] for p in pts)
    count = len(pts)
    for y in range(top, bottom + 1):
        hits = []
        for i in range(count):
            ax, ay = pts[i]
            bx, by = pts[(i + 1) % count]
            if (ay <= y < by) or (by <= y < ay):
                hits.append(ax + (y - ay) * (bx - ax) / (by - ay))
        hits.sort()
        for i in range(0, len(hits) - 1, 2):
            for x in range(int(hits[i]), int(hits[i + 1]) + 1):
                set_px(x, y, rgb)


# --- 5x7 bitmap font, one glyph per line: char + seven 5-bit rows ---
FONT_DATA = """
A 01110 10001 10001 11111 10001 10001 10001
B 11110 10001 10001 11110 10001 10001 11110
C 01110 10001 10000 10000 10000 10001 01110
D 11100 10010 10001 10001 10001 10010 11100
E 11111 10000 10000 11110 10000 10000 11111
F 11111 10000 10000 11110 10000 10000 10000
G 01110 10001 10000 10111 10001 10001 01111
H 10001 10001 10001 11111 10001 10001 10001
I 01110 00100 00100 00100 00100 00100 01110
J 00111 00010 00010 00010 00010 10010 01100
K 10001 10010 10100 11000 10100 10010 10001
L 10000 10000 10000 10000 10000 10000 11111
M 10001 11011 10101 10101 10001 10001 10001
N 10001 11001 10101 10011 10001 10001 10001
O 01110 10001 10001 10001 10001 10001 01110
P 11110 10001 10001 11110 10000 10000 10000
Q 01110 10001 10001 10001 10101 10010 01101
R 11110 10001 10001 11110 10100 10010 10001
S 01111 10000 10000 01110 00001 00001 11110
T 11111 00100 00100 00100 00100 00100 00100
U 10001 10001 10001 10001 10001 10001 01110
V 10001 10001 10001 10001 10001 01010 00100
W 10001 10001 10001 10101 10101 11011 10001
X 10001 10001 01010 00100 01010 10001 10001
Y 10001 10001 01010 00100 00100 00100 00100
Z 11111 00001 00010 00100 01000 10000 11111
0 01110 10001 10011 10101 11001 10001 01110
1 00100 01100 00100 00100 00100 00100 01110
2 01110 10001 00001 00110 01000 10000 11111
3 11111 00010 00100 00010 00001 10001 01110
4 00010 00110 01010 10010 11111 00010 00010
5 11111 10000 11110 00001 00001 10001 01110
6 00110 01000 10000 11110 10001 10001 01110
7 11111 00001 00010 00100 01000 01000 01000
8 01110 10001 10001 01110 10001 10001 01110
9 01110 10001 10001 01111 00001 00010 01100
. 00000 00000 00000 00000 00000 01100 01100
, 00000 00000 00000 00000 01100 00100 01000
- 00000 00000 00000 01110 00000 00000 00000
' 00100 00100 01000 00000 00000 00000 00000
: 00000 01100 00000 00000 00000 01100 00000
; 00000 01100 00000 01100 00100 01000 00000
( 00010 00100 01000 01000 01000 00100 00010
) 01000 00100 00010 00010 00010 00100 01000
/ 00001 00010 00010 00100 01000 01000 10000
$ 00100 01111 10100 01110 00101 11110 00100
% 11001 11010 00010 00100 01000 01011 10011
& 01100 10010 10100 01000 10101 10010 01101
+ 00000 00100 00100 11111 00100 00100 00000
= 00000 00000 11111 00000 11111 00000 00000
! 00100 00100 00100 00100 00100 00000 00100
? 01110 10001 00001 00010 00100 00000 00100
* 00000 10101 01110 10101 00000 00000 00000
"""

GLYPHS = {}
for _line in FONT_DATA.strip().splitlines():
    _parts = _line.split()
    GLYPHS[_parts[0]] = [int(_row, 2) for _row in _parts[1:]]


def glyph_w(s, scale):
    return len(s) * 6 * scale - scale


def blit_text(x, y, s, scale, rgb):
    cursor = x
    for ch in s.upper():
        if ch == " ":
            cursor += 6 * scale
            continue
        bits = GLYPHS.get(ch, GLYPHS["?"])
        for row in range(7):
            value = bits[row]
            for col in range(5):
                if value & (1 << (4 - col)):
                    fill_rect(cursor + col * scale, y + row * scale,
                              scale, scale, rgb)
        cursor += 6 * scale


def centred_text(cx, y, s, scale, rgb):
    blit_text(cx - glyph_w(s, scale) // 2, y, s, scale, rgb)


def wrap_text(s, width, scale):
    out, current = [], ""
    for word in s.split():
        trial = (current + " " + word).strip()
        if glyph_w(trial, scale) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


# --- icons, each in a 110x140 box with its top-left at (bx, by) ---
def icon_cyclone(bx, by):
    fill_rect(bx, by, 110, 140, (204, 251, 241))
    for radius in (36, 27, 18, 9):
        disc_ring(bx + 55, by + 60, radius, 3, TEAL_RGB)
    fill_disc(bx + 55, by + 60, 6, TEAL_RGB)
    for dx in (-40, -14, 12, 38):
        draw_line(bx + 55 + dx, by + 106, bx + 51 + dx, by + 124,
                  (14, 116, 144), 3)
    draw_line(bx + 55, by + 60, bx + 94, by + 38, (13, 148, 136), 3)
    blit_text(bx + 34, by + 8, "AKVAN", 2, TEAL_RGB)


def icon_clock(bx, by):
    fill_rect(bx, by, 110, 140, (254, 242, 242))
    fill_disc(bx + 55, by + 60, 38, WHITE_RGB)
    disc_ring(bx + 55, by + 60, 38, 3, RED_RGB)
    for k in range(12):
        angle = math.pi * 2 * k / 12 - math.pi / 2
        tx = bx + 55 + int(32 * math.cos(angle))
        ty = by + 60 + int(32 * math.sin(angle))
        fill_disc(tx, ty, 2, INK_RGB)
    draw_line(bx + 55, by + 60, bx + 55, by + 32, INK_RGB, 3)
    draw_line(bx + 55, by + 60, bx + 74, by + 72, INK_RGB, 3)
    fill_disc(bx + 55, by + 60, 4, RED_RGB)
    blit_text(bx + 31, by + 112, "2027", 2, RED_RGB)


def icon_scales(bx, by):
    fill_rect(bx, by, 110, 140, (219, 234, 254))
    fill_rect(bx + 52, by + 18, 6, 84, NAVY_RGB)
    fill_rect(bx + 20, by + 24, 70, 6, NAVY_RGB)
    fill_disc(bx + 55, by + 16, 5, GOLD_RGB)
    draw_line(bx + 24, by + 30, bx + 12, by + 58, NAVY_RGB, 2)
    draw_line(bx + 24, by + 30, bx + 36, by + 58, NAVY_RGB, 2)
    fill_poly([(bx + 8, by + 58), (bx + 40, by + 58), (bx + 24, by + 74)],
              GOLD_RGB)
    draw_line(bx + 86, by + 30, bx + 74, by + 58, NAVY_RGB, 2)
    draw_line(bx + 86, by + 30, bx + 98, by + 58, NAVY_RGB, 2)
    fill_poly([(bx + 70, by + 58), (bx + 102, by + 58), (bx + 86, by + 74)],
              GOLD_RGB)
    fill_rect(bx + 34, by + 102, 42, 8, NAVY_RGB)
    fill_rect(bx + 28, by + 110, 54, 8, NAVY_RGB)
    blit_text(bx + 38, by + 122, "ICJ", 2, BLUE_RGB)


def icon_shield(bx, by):
    fill_rect(bx, by, 110, 140, (255, 251, 235))
    fill_poly([(bx + 15, by + 14), (bx + 95, by + 14), (bx + 95, by + 66),
               (bx + 55, by + 118), (bx + 15, by + 66)], (30, 58, 138))
    fill_poly([(bx + 25, by + 24), (bx + 85, by + 24), (bx + 85, by + 62),
               (bx + 55, by + 104), (bx + 25, by + 62)], GOLD_RGB)
    fill_poly([(bx + 55, by + 36), (bx + 62, by + 52), (bx + 79, by + 52),
               (bx + 66, by + 63), (bx + 70, by + 80), (bx + 55, by + 71),
               (bx + 40, by + 80), (bx + 44, by + 63), (bx + 31, by + 52),
               (bx + 48, by + 52)], NAVY_RGB)
    blit_text(bx + 35, by + 124, "HAITI", 2, NAVY_RGB)


def icon_ball(bx, by):
    fill_rect(bx, by, 110, 140, (243, 232, 255))
    fill_disc(bx + 55, by + 60, 40, ORANGE_RGB)
    disc_ring(bx + 55, by + 60, 40, 2, (124, 45, 18))
    draw_line(bx + 15, by + 60, bx + 95, by + 60, (124, 45, 18), 3)
    draw_line(bx + 55, by + 20, bx + 55, by + 100, (124, 45, 18), 3)
    for sx, sy, ex, ey in [(20, 34, 46, 76), (90, 34, 64, 76),
                           (20, 86, 46, 44), (90, 86, 64, 44)]:
        draw_line(bx + sx, by + sy, bx + ex, by + ey, (124, 45, 18), 2)
    blit_text(bx + 31, by + 116, "$750M", 2, PURPLE_RGB)


def icon_court(bx, by):
    fill_rect(bx, by, 110, 140, (226, 232, 240))
    fill_poly([(bx + 10, by + 34), (bx + 100, by + 34), (bx + 55, by + 12)],
              NAVY2_RGB)
    fill_disc(bx + 55, by + 26, 5, GOLD_RGB)
    for i in range(5):
        fill_rect(bx + 20 + i * 14, by + 40, 7, 52, WHITE_RGB)
    fill_rect(bx + 14, by + 92, 82, 8, WHITE_RGB)
    fill_rect(bx + 10, by + 100, 90, 8, NAVY2_RGB)
    fill_rect(bx + 6, by + 108, 98, 8, NAVY2_RGB)
    blit_text(bx + 33, by + 122, "SEOUL", 2, NAVY2_RGB)


# --- the six stories of the day ---
STORIES = [
    ("WEATHER * INDIA", TEAL_RGB, icon_cyclone,
     "CYCLONE AKVAN", "HITS ODISHA COAST",
     "Landfall near Gopalpur at noon, winds to 110 km/h. Odisha moves "
     "300,000 people to shelters."),
    ("USA * IRAN", RED_RGB, icon_clock,
     "TRUMP PUSHES IRAN", "DECISION TO 2027",
     "The US will 'see what happens' after 1 January, Trump says, "
     "putting off any war decision."),
    ("WORLD * JUSTICE", BLUE_RGB, icon_scales,
     "COURT FINDS MYANMAR", "COMMITTED GENOCIDE",
     "The ICJ rules Myanmar guilty of genocide against the Rohingya, "
     "a first for any state."),
    ("AMERICAS * HAITI", AMBER_RGB, icon_shield,
     "HAITI POLICE KILL", "34 IN GANG SWEEP",
     "Officers and a task force fight gangs in the Martissant corridor "
     "of Port-au-Prince."),
    ("SPORT * BUSINESS", PURPLE_RGB, icon_ball,
     "SPARKS NEAR RECORD", "$750M SALE",
     "The LA Sparks are close to a $750m sale, a record price for a "
     "WNBA team."),
    ("ASIA * KOREA", DARK_RGB, icon_court,
     "SEOUL COURT OVERTURNS", "EX-PM HAN SENTENCE",
     "South Korea's top court quashes Han Duck-soo's 15-year term and "
     "orders a retrial."),
]


def card(x, y, tag, accent, draw_icon, head1, head2, blurb):
    fill_rect(x, y, 497, 256, WHITE_RGB)
    fill_rect(x, y, 497, 2, accent)
    fill_rect(x, y + 254, 497, 2, accent)
    fill_rect(x, y, 2, 256, accent)
    fill_rect(x + 495, y, 2, 256, accent)
    fill_rect(x + 2, y + 2, 493, 30, accent)
    blit_text(x + 12, y + 10, tag, 2, WHITE_RGB)
    blit_text(x + 497 - 12 - glyph_w("20 NOV", 2), y + 10, "20 NOV", 2,
              WHITE_RGB)
    blit_text(x + 12, y + 42, head1, 3, INK_RGB)
    blit_text(x + 12, y + 66, head2, 3, INK_RGB)
    draw_icon(x + 12, y + 100)
    cy = y + 104
    for ln in wrap_text(blurb, 497 - 134 - 12, 2)[:6]:
        blit_text(x + 134, cy, ln, 2, BODY_RGB)
        cy += 20


def build_page():
    fill_rect(0, 0, PAGE_W, PAGE_H, PAPER_RGB)
    fill_rect(0, 0, PAGE_W, 116, NAVY_RGB)
    centred_text(PAGE_W // 2, 14, "THE WORLD TODAY", 5, WHITE_RGB)
    centred_text(PAGE_W // 2, 66, "FRIDAY 20 NOVEMBER 2026", 3, GOLD_RGB)
    fill_rect(0, 112, PAGE_W, 4, GOLD_RGB)
    centred_text(PAGE_W // 2, 128, "SIX STORIES THAT DEFINED THE DAY", 2,
                 GREY_RGB)
    fill_rect(PAGE_W // 2 - 100, 146, 200, 3, GOLD_RGB)
    fill_rect(10, 152, PAGE_W - 20, 2, (200, 192, 170))
    xs, ys = [10, 517], [160, 426, 692]
    for i, story in enumerate(STORIES):
        card(xs[i % 2], ys[i // 2], *story)
    fill_rect(0, 958, PAGE_W, 66, NAVY_RGB)
    blit_text(14, 966, "ALSO TODAY:", 2, GOLD_RGB)
    blit_text(14, 986,
              "US-VENEZUELA SIGN MILITARY PACT  *  DENMARK APPROVES GREENLAND DEAL",
              2, WHITE_RGB)
    blit_text(14, 1004,
              "VOYAGER 1 DATA FLOW STOPS  *  PEW: MUSLIMS LARGEST FAITH BY 2035",
              2, WHITE_RGB)


def write_png():
    build_page()
    raw = bytearray()
    for row in rows:
        raw.append(0)
        raw.extend(row)
    payload = zlib.compress(bytes(raw), 9)

    def add_chunk(kind, data):
        piece = struct.pack(">I", len(data)) + kind + data
        return piece + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += add_chunk(b"IHDR",
                      struct.pack(">IIBBBBB", PAGE_W, PAGE_H, 8, 2, 0, 0, 0))
    png += add_chunk(b"IDAT", payload)
    png += add_chunk(b"IEND", b"")
    target = Path(__file__).resolve().parent / "entry.png"
    target.write_bytes(png)
    print(f"wrote {target} {len(png)} bytes")


if __name__ == "__main__":
    write_png()
