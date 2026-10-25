"""Build the title/loading screen art from branding/strata.png.

Writes into config/fancymenu/assets/strata/:
  logo.png        the STRATA letters cut out of the art (GrabCut), with a soft shadow
  background.png  the same art with the letters painted out, cropped to 16:9, softly blurred

Run: python tools/make_menu_art.py   (needs opencv-python-headless and numpy)
"""
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "branding" / "strata.png"
OUT = ROOT / "config" / "fancymenu" / "assets" / "strata"

LETTERS = (0.11, 0.385, 0.955, 0.70)  # box around the letters, as fractions of the art's size
# Areas GrabCut gets wrong on its own (gold ore under the T, the S's middle): always letter
SURE_LETTER = [(0.318, 0.50, 0.37, 0.65), (0.205, 0.50, 0.255, 0.57)]
LOGO_WIDTH = 1024
BG_SIZE = (1600, 900)


def px(box, w, h):
    return int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)


def letter_mask(img: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    x0, y0, x1, y1 = px(LETTERS, w, h)
    mask = np.zeros((h, w), np.uint8)
    bgd, fgd = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.setRNGSeed(1)
    cv2.grabCut(img, mask, (x0, y0, x1 - x0, y1 - y0), bgd, fgd, 6, cv2.GC_INIT_WITH_RECT)
    for box in SURE_LETTER:
        bx0, by0, bx1, by1 = px(box, w, h)
        mask[by0:by1, bx0:bx1] = cv2.GC_FGD
    cv2.grabCut(img, mask, None, bgd, fgd, 4, cv2.GC_INIT_WITH_MASK)
    fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    # Keep the big pieces that sit on the letters' middle line; drops floating dirt and the gears above
    keep = np.zeros_like(fg)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(fg)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] > 4000 and y0 + (y1 - y0) * 0.3 < cent[i][1] < y1:
            keep[lab == i] = 255
    # Fill small holes (ore sparkles) but keep the letters' counters open
    n, lab, stats, _ = cv2.connectedComponentsWithStats(255 - keep)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] < 1500:
            keep[lab == i] = 255
    return cv2.morphologyEx(keep, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))


def logo(img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    x0, y0, x1, y1 = px(LETTERS, w, h)
    pad = 24
    crop = img[y0 - pad:y1 + pad, x0 - pad:x1 + pad]
    alpha = cv2.GaussianBlur(mask[y0 - pad:y1 + pad, x0 - pad:x1 + pad], (3, 3), 0).astype(np.float32) / 255
    # Soft dark shadow, offset down, so the letters read on any background
    shadow = cv2.GaussianBlur(np.roll(alpha, 6, axis=0), (0, 0), 7) * 0.75
    out_a = alpha + shadow * (1 - alpha)
    rgb = crop.astype(np.float32) * alpha[..., None] / np.maximum(out_a, 1e-6)[..., None]
    out = np.dstack([rgb, out_a * 255]).clip(0, 255).astype(np.uint8)
    scale = LOGO_WIDTH / out.shape[1]
    return cv2.resize(out, (LOGO_WIDTH, round(out.shape[0] * scale)), interpolation=cv2.INTER_AREA)


def background(img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    hole = cv2.dilate(mask, np.ones((15, 15), np.uint8))
    small = cv2.resize(img, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
    clean = cv2.inpaint(small, cv2.resize(hole, (w // 2, h // 2)), 12, cv2.INPAINT_TELEA)
    bw, bh = BG_SIZE
    scaled = cv2.resize(clean, (bw, bw), interpolation=cv2.INTER_CUBIC)
    top = int(bw * 0.52) - bh // 2
    bg = cv2.GaussianBlur(scaled[top:top + bh], (0, 0), 9).astype(np.float32)
    # Vignette and a darker middle band so the buttons stay readable
    yy, xx = np.mgrid[0:bh, 0:bw].astype(np.float32)
    r = np.sqrt(((xx - bw / 2) / (bw * 0.62)) ** 2 + ((yy - bh * 0.45) / (bh * 0.75)) ** 2)
    shade = np.clip(1.05 - 0.55 * r ** 2, 0.35, 1.0) * 0.78
    return (bg * shade[..., None]).clip(0, 255).astype(np.uint8)


def main() -> None:
    img = cv2.imread(str(SRC))
    mask = letter_mask(img)
    OUT.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT / "logo.png"), logo(img, mask), [cv2.IMWRITE_PNG_COMPRESSION, 9])
    cv2.imwrite(str(OUT / "background.png"), background(img, mask), [cv2.IMWRITE_PNG_COMPRESSION, 9])
    for f in sorted(OUT.glob("*.png")):
        im = cv2.imread(str(f), cv2.IMREAD_UNCHANGED)
        print(f.relative_to(ROOT), im.shape[1::-1], f.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
