"""
Builds game/gui/vfx/: the sprites and overlays for Mokou's fight in Case 09.

    python tools/make_vfx.py path/to/kenney-particle-pack

Two kinds of file:

  * Particle sprites from Kenney's Particle Pack (CC0, kenney.nl; the GitHub
    mirror github.com/Calinou/kenney-particle-pack has the same files). They
    are white on transparent, so the game tints them. Copied at a smaller
    size to keep the download light.
  * Anime overlays drawn here as SVG: focus lines (the radial lines that
    close in on a hit), horizontal speed streaks, the cut-in band, and the
    masks that split the screen for the face-off.

Needs Pillow.
"""

import math
import os
import random
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "game", "gui", "vfx")

# Kenney sprite -> (name in the game, size in px).
SPRITES = {
    "star_08": ("flare_cross", 320),     # four-point hit flare
    "star_06": ("flare_star", 256),
    "spark_05": ("bolt_a", 384),         # lightning
    "spark_06": ("bolt_b", 384),
    "spark_01": ("crackle", 320),
    "fire_01": ("fireball_a", 384),
    "fire_02": ("fireball_b", 384),
    "muzzle_01": ("flame_jet", 320),
    "muzzle_03": ("flame_lick", 256),
    "circle_03": ("ring", 512),          # shockwave
    "circle_05": ("glow", 256),
    "smoke_07": ("smoke_a", 384),
    "smoke_03": ("smoke_b", 256),
    "dirt_02": ("debris", 320),
    "slash_03": ("slash", 320),
    "scratch_01": ("streak", 256),
    "scorch_02": ("scorch", 256),
    "twirl_02": ("swirl", 256),
}


def find(folder, name):
    for dirpath, _dirs, files in os.walk(folder):
        if name + ".png" in files:
            return os.path.join(dirpath, name + ".png")
    raise SystemExit("missing %s.png in %s" % (name, folder))


def svg(w, h, body, comment):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">\n'
            '<!-- %s (tools/make_vfx.py) -->\n%s\n</svg>\n' % (w, h, w, h, comment, body))


def write(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(text)


def p(x, y):
    return "%.1f %.1f" % (x, y)


def focus_lines(seed, colour="#000000", opacity=0.9):
    """Manga focus lines: thin wedges from the edges toward a clear centre."""
    W, H = 1920, 1080
    cx, cy = 1080, 430
    rnd = random.Random(seed)
    wedges = []
    a = rnd.uniform(0, 0.05)
    while a < 2 * math.pi:
        width = rnd.uniform(0.004, 0.016)
        r0 = rnd.uniform(380, 620)
        r1 = 1800
        wedges.append("M%s L%s L%s Z" % (
            p(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
            p(cx + r1 * math.cos(a - width), cy + r1 * math.sin(a - width)),
            p(cx + r1 * math.cos(a + width), cy + r1 * math.sin(a + width))))
        a += rnd.uniform(0.025, 0.07)
    return svg(W, H, '<path d="%s" fill="%s" fill-opacity="%.2f"/>' % (" ".join(wedges), colour, opacity),
               "focus lines %d" % seed)


def speed_streaks(seed):
    """White horizontal streaks for a dash."""
    W, H = 1920, 1080
    rnd = random.Random(seed)
    lines = []
    for _ in range(70):
        y = rnd.uniform(0, H)
        x = rnd.uniform(-400, W)
        ln = rnd.uniform(300, 1100)
        th = rnd.uniform(2, 9)
        lines.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.1f" rx="%.1f" fill="#FFFFFF" fill-opacity="%.2f"/>'
                     % (x, y, ln, th, th / 2, rnd.uniform(0.25, 0.8)))
    return svg(W, H, "\n".join(lines), "speed streaks %d" % seed)


def cutin_band():
    """The slanted band a character's close-up slides in on."""
    W, H = 2400, 420
    body = "\n".join([
        '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#2A0A10"/><stop offset="0.5" stop-color="#7A1420"/>'
        '<stop offset="1" stop-color="#2A0A10"/></linearGradient></defs>',
        '<path d="M120 0 L2400 0 L2280 420 L0 420 Z" fill="url(#g)"/>',
        '<path d="M120 0 L2400 0 L2396 14 L116 14 Z" fill="#E8C060"/>',
        '<path d="M4 406 L2284 406 L2280 420 L0 420 Z" fill="#E8C060"/>',
    ])
    return svg(W, H, body, "cut-in band")


def split_mask(side):
    """Face-off halves, split on a diagonal (white = shown)."""
    W, H = 1920, 1080
    if side == "left":
        d = "M0 0 L1110 0 L810 1080 L0 1080 Z"
    else:
        d = "M1110 0 L1920 0 L1920 1080 L810 1080 Z"
    return svg(W, H, '<path d="%s" fill="#FFFFFF"/>' % d, "face-off mask, " + side)


def split_edge():
    """The bright seam between the two halves."""
    W, H = 1920, 1080
    return svg(W, H, '<path d="M1104 0 L1118 0 L818 1080 L804 1080 Z" fill="#FFF6D8"/>', "face-off seam")


def main(kenney):
    os.makedirs(OUT, exist_ok=True)
    for src, (name, size) in SPRITES.items():
        im = Image.open(find(kenney, src)).convert("RGBA")
        im = im.resize((size, size), Image.LANCZOS)
        im.save(os.path.join(OUT, name + ".png"), optimize=True)
    for i in range(3):
        write("focus_%d.svg" % i, focus_lines(11 + i))
        write("focus_red_%d.svg" % i, focus_lines(21 + i, "#FFFFFF", 0.75))
    for i in range(2):
        write("streaks_%d.svg" % i, speed_streaks(31 + i))
    write("cutin_band.svg", cutin_band())
    write("split_left.svg", split_mask("left"))
    write("split_right.svg", split_mask("right"))
    write("split_edge.svg", split_edge())
    with open(os.path.join(OUT, "CREDITS.txt"), "w", encoding="utf-8") as f:
        f.write("Particle sprites (the .png files) from Particle Pack by Kenney (kenney.nl),\n"
                "Creative Commons CC0 1.0. https://kenney.nl/assets/particle-pack\n"
                "Resized and renamed by tools/make_vfx.py. The .svg overlays are drawn by that script.\n")
    print("wrote", len(os.listdir(OUT)), "files to", OUT)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
