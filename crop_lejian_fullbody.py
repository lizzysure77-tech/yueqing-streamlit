# -*- coding: utf-8 -*-
"""从乐笺海报单图生成全身定稿（避免合图裁切杂色）"""
from pathlib import Path

from PIL import Image

BASE = Path(__file__).parent
SRC = BASE / "assets" / "ip" / "乐笺_海报用.jpeg"
OUT = BASE / "assets" / "ip" / "乐笺_全身定稿.jpeg"


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"缺少 {SRC}")
    im = Image.open(SRC).convert("RGB")
    im.save(OUT, format="JPEG", quality=94)
    print(f"Saved {OUT.name} from 海报用 {im.size}")


if __name__ == "__main__":
    main()
