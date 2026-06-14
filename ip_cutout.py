# -*- coding: utf-8 -*-
"""IP 形象抠图：去纸底、边缘羽化、去除残留条带"""
from __future__ import annotations

import math
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

# 与站点宣纸色接近，用于软边缘混合
PAPER_RGB = (245, 242, 232)


def _sample_background(img: Image.Image, margin: int = 8) -> tuple[int, int, int]:
    w, h = img.size
    samples: list[tuple[int, int, int]] = []
    for x in range(min(margin, w)):
        for y in range(h):
            samples.append(img.getpixel((x, y))[:3])
            samples.append(img.getpixel((w - 1 - x, y))[:3])
    for y in range(min(margin, h)):
        for x in range(w):
            samples.append(img.getpixel((x, y))[:3])
            samples.append(img.getpixel((x, h - 1 - y))[:3])
    return tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))


def _color_dist(rgb: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb, bg)))


def _flood_background_mask(
    img: Image.Image,
    bg: tuple[int, int, int],
    tolerance: float = 36.0,
) -> list[bool]:
    w, h = img.size
    px = img.load()
    total = w * h
    mask = [False] * total
    seen = [False] * total

    def idx(x: int, y: int) -> int:
        return y * w + x

    def is_bg_pixel(x: int, y: int) -> bool:
        r, g, b = px[x, y][:3]
        if _color_dist((r, g, b), bg) <= tolerance:
            return True
        if _color_dist((r, g, b), PAPER_RGB) <= tolerance * 0.85:
            return True
        return r > 232 and g > 226 and b > 214

    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_bg_pixel(x, y):
                i = idx(x, y)
                if not seen[i]:
                    seen[i] = True
                    mask[i] = True
                    q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg_pixel(x, y):
                i = idx(x, y)
                if not seen[i]:
                    seen[i] = True
                    mask[i] = True
                    q.append((x, y))

    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h:
                i = idx(nx, ny)
                if not seen[i] and is_bg_pixel(nx, ny):
                    seen[i] = True
                    mask[i] = True
                    q.append((nx, ny))
    return mask


def _build_alpha(img: Image.Image, bg_mask: list[bool], feather: float = 22.0) -> Image.Image:
    """仅依据边缘连通背景生成透明，避免脸部浅色被误抠。"""
    w, h = img.size
    alpha = Image.new("L", (w, h), 0)
    apx = alpha.load()

    for y in range(h):
        for x in range(w):
            i = y * w + x
            if not bg_mask[i]:
                apx[x, y] = 255

    # 仅在前景边缘做轻微羽化
    for y in range(h):
        for x in range(w):
            if apx[x, y] == 0:
                continue
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < w and 0 <= ny < h:
                    j = ny * w + nx
                    if bg_mask[j]:
                        apx[x, y] = min(apx[x, y], 200)
                        break

    return alpha.filter(ImageFilter.GaussianBlur(radius=0.6))


def _trim_alpha_bbox(img: Image.Image, pad: int = 6) -> Image.Image:
    w, h = img.size
    apx = img.split()[3].load()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if apx[x, y] > 12:
                xs.append(x)
                ys.append(y)
    if not xs:
        return img
    x0 = max(0, min(xs) - pad)
    y0 = max(0, min(ys) - pad)
    x1 = min(w, max(xs) + pad + 1)
    y1 = min(h, max(ys) + pad + 1)
    return img.crop((x0, y0, x1, y1))


def remove_paper_background(src: Path | Image.Image) -> Image.Image:
    img = Image.open(src).convert("RGBA") if isinstance(src, Path) else src.convert("RGBA")
    bg = _sample_background(img)
    bg_mask = _flood_background_mask(img, bg)
    alpha = _build_alpha(img, bg_mask)
    r, g, b = img.split()[:3]
    out = Image.merge("RGBA", (r, g, b, alpha))
    return _trim_alpha_bbox(out)


def bake_cutout(src: Path, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    out = remove_paper_background(src)
    out.save(dst, format="PNG", optimize=True)
    return dst
