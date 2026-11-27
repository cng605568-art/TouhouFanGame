"""
Cuts a fumo plush out of a photo and saves a transparent, tightly cropped PNG
ready to drop into game/images/ (for example game/images/reimu_fumo.png).

    pip install opencv-python-headless pymatting pillow
    python tools/cut_fumo.py photo.jpg game/images/cirno_fumo.png
    python tools/cut_fumo.py photo.jpg game/images/eiki_fumo.png --white

Without --white the plush is separated from a plain or gradient backdrop with
GrabCut. With --white, a pure white studio backdrop is flood-filled from the
edges instead (--threshold sets how white counts as backdrop; raise it if white
fabric gets eaten, lower it if a white fringe remains). Either way, the edge is
refined with closed-form alpha matting and the backdrop colour is removed from
edge pixels, so the cutout sits cleanly on the dark courtroom.

Classical image processing only; no generative or AI models involved.
"""

import argparse

import cv2
import numpy as np
from PIL import Image
from pymatting import estimate_alpha_cf, estimate_foreground_ml


def white_backdrop_mask(img, threshold):
    near_white = (img.min(axis=2) >= threshold).astype(np.uint8)
    _n, labels = cv2.connectedComponents(near_white, connectivity=4)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    backdrop = np.isin(labels, [l for l in edge if l != 0] or [-1]) & (near_white == 1)
    return (~backdrop).astype(np.uint8)


def grabcut_mask(img, margin=6):
    h, w = img.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), mask,
                (margin, margin, w - 2 * margin, h - 2 * margin), bgd, fgd, 10, cv2.GC_INIT_WITH_RECT)
    return np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1, 0).astype(np.uint8)


def keep_subject(m):
    """Largest connected blob, with interior holes filled."""
    n, labels, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    if n > 1:
        m = (labels == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    inv = (1 - m).astype(np.uint8)
    _n, lab = cv2.connectedComponents(inv, connectivity=4)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    m[~np.isin(lab, edge) & (inv == 1)] = 1
    return cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))


def cut(src, dst, white=False, threshold=251, band=None):
    img = np.array(Image.open(src).convert("RGB"))
    if white:
        mask = white_backdrop_mask(img, threshold)
        band = band or 4
    else:
        mask = grabcut_mask(img)
        band = band or 6
    mask = keep_subject(mask)

    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * band + 1, 2 * band + 1))
    trimap = np.full(mask.shape, 0.5)
    trimap[cv2.erode(mask, k) == 1] = 1.0
    trimap[cv2.erode(1 - mask, k) == 1] = 0.0

    rgb = img.astype(np.float64) / 255.0
    alpha = np.clip(estimate_alpha_cf(rgb, trimap), 0, 1)
    alpha[alpha < 0.04] = 0
    fore = estimate_foreground_ml(rgb, alpha)

    rgba = np.dstack([np.clip(fore, 0, 1), alpha])
    out = Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), "RGBA")
    out = out.crop(out.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox())
    out.save(dst, optimize=True)
    print("%s -> %s (%dx%d)" % (src, dst, out.width, out.height))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photo")
    ap.add_argument("output")
    ap.add_argument("--white", action="store_true", help="photo has a pure white studio backdrop")
    ap.add_argument("--threshold", type=int, default=251, help="backdrop whiteness for --white (0-255)")
    args = ap.parse_args()
    cut(args.photo, args.output, args.white, args.threshold)
