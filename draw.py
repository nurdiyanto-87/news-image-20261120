#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page, pure stdlib.

Writes entry.png (1024x1024, RGB PNG) next to this script.
Run: python3 draw.py
"""
import math
import struct
import zlib
from pathlib import Path

W, H = 1024, 1024

# ---------- palette ----------
PAPER = (247, 243, 232)
INK = (22, 28, 38)
NAVY = (19, 31, 56)
NAVY2 = (30, 46, 82)
GOLD = (242, 193, 78)
WHITE = (255, 255, 255)
GREY = (90, 96, 110)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (15, 118, 110)
PURPLE = (123, 47, 190)
AMBER = (180, 83, 9)
DARK = (15, 23, 42)
ORANGE = (234, 88, 12)

# ---------- canvas ----------
buf = bytearray(W * H * 3)


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = c


def rect(x, y, w, h, c):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            buf[i], buf[i + 1], buf[i + 2] = c


def disc(cx, cy, r, c):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                px(xx, yy, c)


def ring(cx, cy, r, t, c):
    for yy in range(cy - r - t, cy + r + t + 1):
        for xx in range(cx - r - t, cx + r + t + 1):
            d2 = (xx - cx) ** 2 + (yy - cy) ** 2
            if (r - t) ** 2 <= d2 <= (r + t) ** 2:
                px(xx, yy, c)


def line(x0, y0, x1, y1, c, w=1):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        for a in range(-(w // 2), w // 2 + 1):
            for b in range(-(w // 2), w // 2 + 1):
                px(x0 + a, y0 + b, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def poly(points, c):
    """Scanline fill of a simple polygon."""
    ys = [p[1] for p in points]
    for y in range(min(ys), max(ys) + 1):
        xs = []
        n = len(points)
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(int(xs[i]), int(xs[i + 1]) + 1):
                px(x, y, c)


# ---------- 5x7 bitmap font (own patterns, uppercase + digits + punctuation) ----------
F = {}


def _g(ch, rows):
    F[ch] = [sum((1 if b == "1" else 0) << (4 - j) for j, b in enumerate(r)) for r in rows]


_g("A", ["01110", "10001", "10001", "11111", "10001", "10001", "10001"])
_g("B", ["11110", "10001", "10001", "11110", "10001", "10001", "11110"])
_g("C", ["01110", "10001", "10000", "10000", "10000", "10001", "01110"])
_g("D", ["11100", "10010", "10001", "10001", "10001", "10010", "11100"])
_g("E", ["11111", "10000", "10000", "11110", "10000", "10000", "11111"])
_g("F", ["11111", "10000", "10000", "11110", "10000", "10000", "10000"])
_g("G", ["01110", "10001", "10000", "10111", "10001", "10001", "01111"])
_g("H", ["10001", "10001", "10001", "11111", "10001", "10001", "10001"])
_g("I", ["01110", "00100", "00100", "00100", "00100", "00100", "01110"])
_g("J", ["00111", "00010", "00010", "00010", "00010", "10010", "01100"])
_g("K", ["10001", "10010", "10100", "11000", "10100", "10010", "10001"])
_g("L", ["10000", "10000", "10000", "10000", "10000", "10000", "11111"])
_g("M", ["10001", "11011", "10101", "10101", "10001", "10001", "10001"])
_g("N", ["10001", "11001", "10101", "10011", "10001", "10001", "10001"])
_g("O", ["01110", "10001", "10001", "10001", "10001", "10001", "01110"])
_g("P", ["11110", "10001", "10001", "11110", "10000", "10000", "10000"])
_g("Q", ["01110", "10001", "10001", "10001", "10101", "10010", "01101"])
_g("R", ["11110", "10001", "10001", "11110", "10100", "10010", "10001"])
_g("S", ["01111", "10000", "10000", "01110", "00001", "00001", "11110"])
_g("T", ["11111", "00100", "00100", "00100", "00100", "00100", "00100"])
_g("U", ["10001", "10001", "10001", "10001", "10001", "10001", "01110"])
_g("V", ["10001", "10001", "10001", "10001", "10001", "01010", "00100"])
_g("W", ["10001", "10001", "10001", "10101", "10101", "11011", "10001"])
_g("X", ["10001", "10001", "01010", "00100", "01010", "10001", "10001"])
_g("Y", ["10001", "10001", "01010", "00100", "00100", "00100", "00100"])
_g("Z", ["11111", "00001", "00010", "00100", "01000", "10000", "11111"])
_g("0", ["01110", "10001", "10011", "10101", "11001", "10001", "01110"])
_g("1", ["00100", "01100", "00100", "00100", "00100", "00100", "01110"])
_g("2", ["01110", "10001", "00001", "00110", "01000", "10000", "11111"])
_g("3", ["11111", "00010", "00100", "00010", "00001", "10001", "01110"])
_g("4", ["00010", "00110", "01010", "10010", "11111", "00010", "00010"])
_g("5", ["11111", "10000", "11110", "00001", "00001", "10001", "01110"])
_g("6", ["00110", "01000", "10000", "11110", "10001", "10001", "01110"])
_g("7", ["11111", "00001", "00010", "00100", "01000", "01000", "01000"])
_g("8", ["01110", "10001", "10001", "01110", "10001", "10001", "01110"])
_g("9", ["01110", "10001", "10001", "01111", "00001", "00010", "01100"])
_g(" ", ["00000"] * 7)
_g(".", ["00000", "00000", "00000", "00000", "00000", "01100", "01100"])
_g(",", ["00000", "00000", "00000", "00000", "01100", "00100", "01000"])
_g("-", ["00000", "00000", "00000", "01110", "00000", "00000", "00000"])
_g("'", ["00100", "00100", "01000", "00000", "00000", "00000", "00000"])
_g(":", ["00000", "01100", "00000", "00000", "00000", "01100", "00000"])
_g(";", ["00000", "01100", "00000", "01100", "00100", "01000", "00000"])
_g("(", ["00010", "00100", "01000", "01000", "01000", "00100", "00010"])
_g(")", ["01000", "00100", "00010", "00010", "00010", "00100", "01000"])
_g("/", ["00001", "00010", "00010", "00100", "01000", "01000", "10000"])
_g("$", ["00100", "01111", "10100", "01110", "00101", "11110", "00100"])
_g("%", ["11001", "11010", "00010", "00100", "01000", "01011", "10011"])
_g("&", ["01100", "10010", "10100", "01000", "10101", "10010", "01101"])
_g("+", ["00000", "00100", "00100", "11111", "00100", "00100", "00000"])
_g("=", ["00000", "00000", "11111", "00000", "11111", "00000", "00000"])
_g("!", ["00100", "00100", "00100", "00100", "00100", "00000", "00100"])
_g("?", ["01110", "10001", "00001", "00010", "00100", "00000", "00100"])
_g("*", ["00000", "10101", "01110", "10101", "00000", "00000", "00000"])


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, c):
    s = s.upper()
    cx = x
    for ch in s:
        glyph = F.get(ch, F["?"])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits & (1 << (4 - col)):
                    rect(cx + col * scale, y + row * scale, scale, scale, c)
        cx += 6 * scale


def text_center(cx, y, s, scale, c):
    draw_text(cx - text_w(s, scale) // 2, y, s, scale, c)


def wrap(s, width, scale):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, scale) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------- icons (each drawn in a 110x140 box at bx, by) ----------
def icon_cyclone(bx, by):
    rect(bx, by, 110, 140, (204, 251, 241))
    for r in (34, 26, 18, 10):
        ring(bx + 55, by + 62, r, 3, TEAL)
    disc(bx + 55, by + 62, 6, TEAL)
    for dx in (-38, -14, 12, 36):
        line(bx + 55 + dx, by + 108, bx + 51 + dx, by + 124, (14, 116, 144), 3)
    line(bx + 55, by + 62, bx + 92, by + 40, (13, 148, 136), 3)
    draw_text(bx + 34, by + 8, "AKVAN", 2, TEAL)


def icon_clock(bx, by):
    rect(bx, by, 110, 140, (254, 242, 242))
    disc(bx + 55, by + 62, 40, WHITE)                    # clock face
    ring(bx + 55, by + 62, 40, 3, RED)
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx = bx + 55 + int(34 * math.cos(a))
        sy = by + 62 + int(34 * math.sin(a))
        disc(sx, sy, 2, INK)
    line(bx + 55, by + 62, bx + 55, by + 34, INK, 3)     # minute hand
    line(bx + 55, by + 62, bx + 76, by + 74, INK, 3)     # hour hand
    disc(bx + 55, by + 62, 4, RED)
    draw_text(bx + 31, by + 112, "2027", 2, RED)


def icon_scales(bx, by):
    rect(bx, by, 110, 140, (219, 234, 254))
    rect(bx + 52, by + 18, 6, 84, NAVY)                  # post
    rect(bx + 20, by + 24, 70, 6, NAVY)                  # beam
    disc(bx + 55, by + 16, 5, GOLD)                      # finial
    line(bx + 24, by + 30, bx + 12, by + 58, NAVY, 2)    # left strings
    line(bx + 24, by + 30, bx + 36, by + 58, NAVY, 2)
    poly([(bx + 8, by + 58), (bx + 40, by + 58), (bx + 24, by + 74)], GOLD)
    line(bx + 86, by + 30, bx + 74, by + 58, NAVY, 2)    # right strings
    line(bx + 86, by + 30, bx + 98, by + 58, NAVY, 2)
    poly([(bx + 70, by + 58), (bx + 102, by + 58), (bx + 86, by + 74)], GOLD)
    rect(bx + 34, by + 102, 42, 8, NAVY)                 # base
    rect(bx + 28, by + 110, 54, 8, NAVY)
    draw_text(bx + 38, by + 122, "ICJ", 2, BLUE)


def icon_shield(bx, by):
    rect(bx, by, 110, 140, (255, 251, 235))
    poly([(bx + 15, by + 14), (bx + 95, by + 14), (bx + 95, by + 66),
          (bx + 55, by + 118), (bx + 15, by + 66)], (30, 58, 138))
    poly([(bx + 25, by + 24), (bx + 85, by + 24), (bx + 85, by + 62),
          (bx + 55, by + 104), (bx + 25, by + 62)], GOLD)
    poly([(bx + 55, by + 36), (bx + 62, by + 52), (bx + 79, by + 52),
          (bx + 66, by + 63), (bx + 70, by + 80), (bx + 55, by + 71),
          (bx + 40, by + 80), (bx + 44, by + 63), (bx + 31, by + 52),
          (bx + 48, by + 52)], NAVY)
    draw_text(bx + 35, by + 124, "HAITI", 2, NAVY)


def icon_ball(bx, by):
    rect(bx, by, 110, 140, (243, 232, 255))
    disc(bx + 55, by + 62, 42, ORANGE)                   # ball
    ring(bx + 55, by + 62, 42, 2, (124, 45, 18))
    line(bx + 13, by + 62, bx + 97, by + 62, (124, 45, 18), 3)
    line(bx + 55, by + 20, bx + 55, by + 104, (124, 45, 18), 3)
    for sx, sy, ex, ey in [(18, 34, 46, 78), (92, 34, 64, 78),
                           (18, 90, 46, 46), (92, 90, 64, 46)]:
        line(bx + sx, by + sy, bx + ex, by + ey, (124, 45, 18), 2)
    draw_text(bx + 31, by + 116, "$750M", 2, PURPLE)


def icon_court(bx, by):
    rect(bx, by, 110, 140, (226, 232, 240))
    poly([(bx + 10, by + 34), (bx + 100, by + 34), (bx + 55, by + 12)], NAVY2)
    disc(bx + 55, by + 26, 5, GOLD)
    for i in range(5):
        rect(bx + 20 + i * 14, by + 40, 7, 52, WHITE)    # columns
    rect(bx + 14, by + 92, 82, 8, WHITE)                 # entablature
    rect(bx + 10, by + 100, 90, 8, NAVY2)                # steps
    rect(bx + 6, by + 108, 98, 8, NAVY2)
    draw_text(bx + 33, by + 122, "SEOUL", 2, NAVY2)


# ---------- stories ----------
STORIES = [
    ("WEATHER * INDIA", TEAL, icon_cyclone,
     "CYCLONE AKVAN", "HITS ODISHA COAST",
     "Landfall near Gopalpur at noon, winds to 110 km/h. Odisha moves 300,000 people to shelters."),
    ("USA * IRAN", RED, icon_clock,
     "TRUMP PUSHES IRAN", "DECISION TO 2027",
     "The US will 'see what happens' after 1 January, Trump says, putting off any war decision."),
    ("WORLD * JUSTICE", BLUE, icon_scales,
     "COURT FINDS MYANMAR", "COMMITTED GENOCIDE",
     "The ICJ rules Myanmar guilty of genocide against the Rohingya, a first for any state."),
    ("AMERICAS * HAITI", AMBER, icon_shield,
     "HAITI POLICE KILL", "34 IN GANG SWEEP",
     "Officers and a task force fight gangs in the Martissant corridor of Port-au-Prince."),
    ("SPORT * BUSINESS", PURPLE, icon_ball,
     "SPARKS NEAR RECORD", "$750M SALE",
     "The LA Sparks are close to a $750m sale, a record price for a WNBA team."),
    ("ASIA * KOREA", DARK, icon_court,
     "SEOUL COURT OVERTURNS", "EX-PM HAN SENTENCE",
     "South Korea's top court quashes Han Duck-soo's 15-year term and orders a retrial."),
]


def panel(x, y, tag, accent, icon, h1, h2, caption):
    rect(x, y, 497, 256, WHITE)
    # border
    rect(x, y, 497, 2, accent)
    rect(x, y + 254, 497, 2, accent)
    rect(x, y, 2, 256, accent)
    rect(x + 495, y, 2, 256, accent)
    # tag strip
    rect(x + 2, y + 2, 493, 30, accent)
    draw_text(x + 12, y + 10, tag, 2, WHITE)
    draw_text(x + 497 - 12 - text_w("20 NOV", 2), y + 10, "20 NOV", 2, WHITE)
    # headlines
    draw_text(x + 12, y + 42, h1, 3, INK)
    draw_text(x + 12, y + 66, h2, 3, INK)
    # icon box
    icon(x + 12, y + 100)
    # caption
    lines = wrap(caption, 497 - 134 - 12, 2)
    cy = y + 104
    for ln in lines[:6]:
        draw_text(x + 134, cy, ln, 2, (40, 44, 56))
        cy += 20


def main():
    rect(0, 0, W, H, PAPER)
    # masthead
    rect(0, 0, W, 116, NAVY)
    text_center(W // 2, 14, "THE WORLD TODAY", 5, WHITE)
    text_center(W // 2, 66, "FRIDAY 20 NOVEMBER 2026", 3, GOLD)
    rect(0, 112, W, 4, GOLD)
    # kicker
    text_center(W // 2, 128, "SIX STORIES THAT DEFINED THE DAY", 2, GREY)
    rect(10, 152, W - 20, 2, (200, 192, 170))
    # grid
    xs = [10, 517]
    ys = [160, 426, 692]
    for i, st in enumerate(STORIES):
        panel(xs[i % 2], ys[i // 2], *st)
    # footer
    rect(0, 958, W, 66, NAVY)
    draw_text(14, 966, "ALSO TODAY:", 2, GOLD)
    foot1 = "US-VENEZUELA SIGN MILITARY PACT  *  DENMARK APPROVES GREENLAND DEAL"
    foot2 = "VOYAGER 1 DATA FLOW STOPS  *  PEW: MUSLIMS LARGEST FAITH BY 2035"
    draw_text(14, 986, foot1, 2, WHITE)
    draw_text(14, 1004, foot2, 2, WHITE)
    # write PNG
    out = Path(__file__).resolve().parent / "entry.png"
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(buf[y * W * 3:(y + 1) * W * 3])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    out.write_bytes(png)
    print(f"wrote {out} {len(png)} bytes")


if __name__ == "__main__":
    main()
