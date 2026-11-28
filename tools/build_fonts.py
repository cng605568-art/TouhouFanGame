"""
Builds the subset fonts shipped in game/fonts/ from the full Shippori Mincho
B1 release and, for Simplified Chinese, Noto Serif SC (both SIL Open Font
License 1.1).

    python tools/build_fonts.py path/to/ShipporiMinchoB1-Bold.ttf path/to/ShipporiMinchoB1-ExtraBold.ttf [path/to/NotoSerifSC[wght].ttf]

Full fonts: https://github.com/google/fonts/tree/main/ofl/shipporiminchob1
and https://github.com/google/fonts/tree/main/ofl/notoserifsc (the variable
font; SemiBold and Black instances are cut from it).

Both subsets keep Latin, punctuation, kana and every character used in
game/*.rpy. The dialogue font also keeps the JIS level-1 kanji, so new
Japanese lines render without rebuilding; re-run this after adding kanji to
headings. The source font
has no U+2260 (not-equal sign); one is drawn from its own "=" so it matches.
"""

import os
import re
import sys

from fontTools import subset
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "game", "fonts")

RANGES = [
    (0x0020, 0x007E), (0x00A0, 0x017F), (0x2010, 0x2027), (0x2030, 0x203A),
    (0x2190, 0x2193), (0x25A0, 0x25CF), (0x2605, 0x2606), (0x266A, 0x266A),
    (0x3000, 0x303F), (0x3041, 0x30FF), (0xFF01, 0xFF5E),
]


def jis_level1():
    out = set()
    for hi in range(0x88, 0x99):
        for lo in list(range(0x40, 0x7F)) + list(range(0x80, 0xFD)):
            try:
                out.add(bytes([hi, lo]).decode("shift_jis"))
            except UnicodeDecodeError:
                pass
    return out


def script_chars(skip=()):
    out = set()
    game = os.path.join(ROOT, "game")
    for dirpath, _dirs, files in os.walk(game):
        if any(os.path.join(game, s) in dirpath for s in skip):
            continue
        for fn in files:
            if fn.endswith(".rpy"):
                with open(os.path.join(dirpath, fn), encoding="utf-8") as f:
                    out.update(f.read())
    return out


def add_not_equal(font):
    """Draws U+2260 from the font's own '=' plus a slanted bar."""
    cmap = font.getBestCmap()
    if 0x2260 in cmap:
        return
    glyf = font["glyf"]
    eq_name = cmap[ord("=")]
    eq = glyf[eq_name]

    rec = RecordingPen()
    eq.draw(rec, glyf)

    # Bar thickness of '=' is the height of its first contour.
    first = []
    for op, pts in rec.value:
        if op == "closePath":
            break
        first.extend(p[1] for p in pts)
    bar = max(first) - min(first)

    pen = TTGlyphPen(glyf)
    rec.replay(pen)

    cx = (eq.xMin + eq.xMax) / 2.0
    cy = (eq.yMin + eq.yMax) / 2.0
    half_h = (eq.yMax - eq.yMin) / 2.0 + bar * 1.3
    lean = half_h * 0.36
    w = bar * 0.5
    # Clockwise, like the '=' bars, so the overlap stays filled.
    pts = [
        (cx - lean - w, cy - half_h), (cx + lean - w, cy + half_h),
        (cx + lean + w, cy + half_h), (cx - lean + w, cy - half_h),
    ]
    pen.moveTo(pts[0])
    for p in pts[1:]:
        pen.lineTo(p)
    pen.closePath()

    name = "uni2260"
    glyf[name] = pen.glyph()
    font["hmtx"][name] = font["hmtx"][eq_name]
    if "vmtx" in font:
        font["vmtx"][name] = font["vmtx"][eq_name]
    if name not in font.getGlyphOrder():
        font.setGlyphOrder(font.getGlyphOrder() + [name])
    for table in font["cmap"].tables:
        if table.isUnicode():
            table.cmap[0x2260] = name


def build(src, dst, kanji, weight=None, skip=()):
    font = TTFont(src)
    if weight is not None:
        from fontTools.varLib import instancer
        font = instancer.instantiateVariableFont(font, {"wght": weight})
    if "glyf" in font:
        add_not_equal(font)

    codepoints = set()
    for a, b in RANGES:
        codepoints.update(range(a, b + 1))
    if kanji:
        codepoints.update(ord(c) for c in jis_level1())
    codepoints.update(ord(c) for c in script_chars(skip) if ord(c) >= 0x20)
    codepoints.add(0x2260)

    opts = subset.Options()
    opts.layout_features = ["kern", "palt", "liga"]
    opts.name_IDs = ["*"]
    opts.name_languages = ["*"]
    opts.notdef_outline = True
    opts.drop_tables += ["DSIG", "vhea", "vmtx"]
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=sorted(codepoints))
    sub.subset(font)
    font.save(dst)
    print("%s: %d glyphs, %.0f KB" % (os.path.basename(dst), len(font.getGlyphOrder()), os.path.getsize(dst) / 1024.0))


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    os.makedirs(OUT, exist_ok=True)
    # Dialogue font: keeps common kanji so new Japanese lines just work.
    build(sys.argv[1], os.path.join(OUT, "ShipporiMinchoB1-Bold-sub.ttf"), True)
    # Heading font: Latin, kana and the kanji the script actually uses.
    build(sys.argv[2], os.path.join(OUT, "ShipporiMinchoB1-ExtraBold-sub.ttf"), False)
    # Simplified Chinese: every character in the game except the Japanese
    # translation, at the weights of the two Shippori fonts.
    if len(sys.argv) == 4:
        skip = (os.path.join("tl", "japanese"),)
        build(sys.argv[3], os.path.join(OUT, "NotoSerifSC-SemiBold-sub.ttf"), False, 600, skip)
        build(sys.argv[3], os.path.join(OUT, "NotoSerifSC-Black-sub.ttf"), False, 900, skip)
