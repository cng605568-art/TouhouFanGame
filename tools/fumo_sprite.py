"""
Turns a photo of a fumo plush into a courtroom-ready sprite.

    python tools/fumo_sprite.py art_src/cirno_fumo.jpg game/images/cirno_fumo.png

Steps:
  1. Background removal with the BiRefNet segmentation model (via rembg).
     The model only decides which pixels belong to the plush; it does not
     draw or change anything. `--model classic` uses GrabCut / white-backdrop
     flood fill instead, with no AI at all.
  2. Edge refinement: closed-form alpha matting on the soft edge band, then
     the backdrop colour is removed from edge pixels, so nothing grey or white
     fringes the plush on the dark crimson courtroom.
  3. Relighting to match the courtroom: lantern-lit highlights, a crimson
     white balance, red bounce light from the lacquer walls, a gold rim light
     from the mirror halo behind the stand, and ambient occlusion toward the
     cushion. `--no-relight` skips this.
  4. Crop to the plush, save a transparent PNG.

Needs:  pip install "rembg[cpu]" pymatting opencv-python-headless pillow
BiRefNet needs roughly 8 GB of free RAM; the "Make fumo sprites" GitHub
workflow runs this for you on GitHub's machines.
"""

import argparse
import os

import cv2
import numpy as np
from PIL import Image

# Relighting, tuned against bg_courtroom.svg.
LIGHT = dict(
    exposure=0.86,               # studio photo -> lantern-lit room
    shoulder=0.55,               # rolls off blown-out white fabric
    wb=(1.08, 0.95, 0.93),       # warm, leaning crimson rather than amber
    bounce_col="#6E1A28",        # red bounce light from the lacquer walls
    bounce=0.05,
    top=1.04,                    # overhead key light...
    bottom=0.78,                 # ...falling off toward the cushion
    sat=0.95,
    rim_col="#F2C46A",           # gold backlight from the mirror halo
    rim=1.15,
    rim_width=3.0,
)


# ---------------------------------------------------------------------------
# Masks
# ---------------------------------------------------------------------------

def ai_alpha(img, model):
    import onnxruntime as ort
    from rembg import new_session, remove

    opts = ort.SessionOptions()
    opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
    session = new_session(model, sess_opts=opts)
    mask = remove(Image.fromarray(img), session=session, only_mask=True)
    return np.asarray(mask, dtype=np.float64) / 255.0


def classic_alpha(img):
    h, w = img.shape[:2]
    border = np.concatenate([img[0], img[-1], img[:, 0], img[:, -1]])
    if (border.min(axis=1) >= 245).mean() > 0.9:
        # Pure white studio backdrop: flood-fill near-white from the edges.
        near_white = (img.min(axis=2) >= 251).astype(np.uint8)
        _n, labels = cv2.connectedComponents(near_white, connectivity=4)
        edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
        backdrop = np.isin(labels, [l for l in edge if l != 0] or [-1]) & (near_white == 1)
        return (~backdrop).astype(np.float64)
    mask = np.zeros((h, w), np.uint8)
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), mask, (6, 6, w - 12, h - 12), bgd, fgd, 10, cv2.GC_INIT_WITH_RECT)
    return np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1.0, 0.0)


def main_subject(alpha):
    """Drops stray specks: keeps the largest solid blob and its soft edge."""
    solid = (alpha > 0.5).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(solid, connectivity=8)
    if n <= 1:
        return alpha
    keep = (labels == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    # Fill enclosed holes in the solid region.
    inv = 1 - keep
    _n, lab = cv2.connectedComponents(inv, connectivity=4)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    keep[~np.isin(lab, edge) & (inv == 1)] = 1
    near = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    out = alpha * near
    out[keep == 1] = np.maximum(out[keep == 1], alpha[keep == 1])
    return out


def refine(img, alpha):
    """Closed-form matting on the uncertain band, then colour decontamination."""
    from pymatting import estimate_alpha_cf, estimate_foreground_ml

    rgb = img.astype(np.float64) / 255.0
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg = cv2.erode((alpha > 0.95).astype(np.uint8), k)
    bg = cv2.erode((alpha < 0.05).astype(np.uint8), k)
    trimap = np.full(alpha.shape, 0.5)
    trimap[fg == 1] = 1.0
    trimap[bg == 1] = 0.0
    matted = np.clip(estimate_alpha_cf(rgb, trimap), 0, 1)
    # Trust the model where it was certain; use matting only in the band.
    band = (trimap == 0.5)
    out = alpha.copy()
    out[band] = 0.5 * matted[band] + 0.5 * alpha[band]
    out[out < 0.03] = 0
    fore = estimate_foreground_ml(rgb, out)
    return np.clip(fore, 0, 1), out


# ---------------------------------------------------------------------------
# Relighting
# ---------------------------------------------------------------------------

def _to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def _hex_lin(h):
    return _to_lin(np.array([int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]))


def _smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def relight(rgb, alpha, L=LIGHT):
    h, w = alpha.shape
    luma = np.array([0.2126, 0.7152, 0.0722])
    lin = _to_lin(rgb) * L["exposure"]
    lin = lin / (1 + lin * L["shoulder"]) * (1 + L["shoulder"])
    lin = lin * np.array(L["wb"])

    lum = (lin * luma).sum(-1, keepdims=True)
    lin = lin + _hex_lin(L["bounce_col"]) * L["bounce"] * (1 - np.clip(lum * 2.2, 0, 1))

    y = np.linspace(0, 1, h)[:, None, None]
    lin = lin * (L["top"] + (L["bottom"] - L["top"]) * _smoothstep(0.45, 1.0, y))

    lum = (lin * luma).sum(-1, keepdims=True)
    lin = lum + (lin - lum) * L["sat"]

    # Rim light: strongest on upward- and sideways-facing edges of the upper
    # body, fading out toward the feet (the halo sits behind the head).
    solid = (alpha > 0.5).astype(np.uint8)
    dist = cv2.distanceTransform(solid, cv2.DIST_L2, 5)
    soft = cv2.GaussianBlur(alpha.astype(np.float32), (0, 0), 3)
    gy, gx = np.gradient(soft)
    norm = np.sqrt(gx * gx + gy * gy) + 1e-6
    nx, ny = -gx / norm, -gy / norm
    facing = np.clip(0.35 + 0.65 * (-ny * 0.7 + np.abs(nx) * 0.5), 0, 1)
    fade = 1 - _smoothstep(0.55, 0.85, y[..., 0])
    rim = (np.exp(-dist / L["rim_width"]) * facing * fade * alpha)[..., None] * L["rim"]
    lin = 1 - (1 - np.clip(lin, 0, 1)) * (1 - rim * _hex_lin(L["rim_col"]))

    return _to_srgb(lin)


# ---------------------------------------------------------------------------

def preview(cutout, lit, path):
    """Before / after over the courtroom crimson, for reviewing on GitHub."""
    w, h = lit.size
    sheet = Image.new("RGB", (w * 2 + 30, h + 20), (43, 7, 13))
    for i, im in enumerate((cutout, lit)):
        top, bot = np.array([94, 21, 34]), np.array([43, 7, 13])
        grad = (top + (bot - top) * np.linspace(0, 1, h)[:, None]).astype(np.uint8)
        bg = Image.fromarray(np.dstack([np.repeat(grad[:, None, :], w, axis=1), np.full((h, w), 255, np.uint8)]), "RGBA")
        bg.alpha_composite(im)
        sheet.paste(bg.convert("RGB"), (10 + i * (w + 10), 10))
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    sheet.save(path, quality=90)


def make_sprite(src, dst, model="birefnet-general", do_refine=True, do_relight=True, preview_path=None):
    img = np.array(Image.open(src).convert("RGB"))

    alpha = classic_alpha(img) if model == "classic" else ai_alpha(img, model)
    alpha = main_subject(alpha)

    if do_refine:
        rgb, alpha = refine(img, alpha)
    else:
        rgb = img.astype(np.float64) / 255.0

    def to_image(colour):
        arr = np.dstack([colour, alpha])
        return Image.fromarray((arr * 255 + 0.5).astype(np.uint8), "RGBA")

    cutout = to_image(rgb)
    out = to_image(relight(rgb, alpha)) if do_relight else cutout

    box = out.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    box = (max(0, box[0] - 2), max(0, box[1] - 2), min(out.width, box[2] + 2), min(out.height, box[3] + 2))
    out = out.crop(box)
    cutout = cutout.crop(box)

    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    out.save(dst, optimize=True)
    if preview_path:
        preview(cutout, out, preview_path)
    print("%s -> %s (%dx%d, %s)" % (src, dst, out.width, out.height, model))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photo")
    ap.add_argument("output")
    ap.add_argument("--model", default="birefnet-general",
                    help="rembg model (birefnet-general, birefnet-general-lite, isnet-general-use) or 'classic'")
    ap.add_argument("--no-refine", action="store_true", help="use the model's alpha as-is")
    ap.add_argument("--no-relight", action="store_true", help="keep the photo's original lighting")
    ap.add_argument("--preview", help="also save a before/after JPEG here")
    a = ap.parse_args()
    make_sprite(a.photo, a.output, a.model, not a.no_refine, not a.no_relight, a.preview)
