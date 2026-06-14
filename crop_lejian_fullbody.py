# -*- coding: utf-8 -*-
"""从乐笺合图裁出全身像（首屏用）"""
from pathlib import Path

from PIL import Image

BASE = Path(__file__).parent
SRC = BASE / "assets" / "ip" / "乐笺_半身定稿.jpeg"
OUT = BASE / "assets" / "ip" / "乐笺_全身定稿.jpeg"


def trim_content(img: Image.Image, pad: int = 12) -> Image.Image:
    rgb = img.convert("RGB")
    w, h = rgb.size
    bg = rgb.getpixel((2, 2))
    mask = []
    for y in range(h):
        for x in range(w):
            r, g, b = rgb.getpixel((x, y))
            if abs(r - bg[0]) < 28 and abs(g - bg[1]) < 28 and abs(b - bg[2]) < 28:
                mask.append(0)
            else:
                mask.append(1)
    xs = [i % w for i, v in enumerate(mask) if v]
    ys = [i // w for i, v in enumerate(mask) if v]
    if not xs:
        return img
    x0, x1 = max(0, min(xs) - pad), min(w, max(xs) + pad + 1)
    y0, y1 = max(0, min(ys) - pad), min(h, max(ys) + pad + 1)
    return img.crop((x0, y0, x1, y1))


def main() -> None:
    im = Image.open(SRC)
    w, h = im.size
    # 合图右上为全身站姿（文档 image4 多姿势板）
    crop = im.crop((int(w * 0.46), int(h * 0.02), w - 4, int(h * 0.58)))
    crop = trim_content(crop)
    crop.save(OUT, format="JPEG", quality=92)
    print(f"Saved {OUT.name} {crop.size}")


if __name__ == "__main__":
    main()
