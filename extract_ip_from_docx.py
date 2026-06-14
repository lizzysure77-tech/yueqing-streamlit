# -*- coding: utf-8 -*-
"""从乐刻IP设计.docx 提取图片并按文档顺序命名到 assets/ip/"""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

BASE = Path(__file__).parent
DOCX = BASE / "乐刻IP设计.docx"
OUT = BASE / "assets" / "ip"

# 文档内图片顺序 image1..image12（见 verify_docx_images.py）
IMAGE_MAP = {
    "image1.jpeg": "LOGO_乐刻.jpeg",
    "image2.jpeg": "乐笺_海报用.jpeg",
    "image3.jpeg": "乐笺_三视图.jpeg",
    "image4.jpeg": "乐笺_半身定稿.jpeg",
    "image5.png": "乐笺_设计规范.png",
    "image6.jpeg": "小刻灵_Q版定稿.jpeg",
    "image7.jpeg": "小刻灵_动作延展.jpeg",
    "image8.png": "小刻灵_设计规范.png",
    "image9.jpeg": "海报_细纹千载纸韵乐清.jpeg",
    "image10.jpeg": "海报_指尖细纹.jpeg",
    "image11.jpeg": "乐笺_表情包.jpeg",
    "image12.jpeg": "小刻灵_海报用.jpeg",
}

ALLOWED = set(IMAGE_MAP.values()) | {"Hero_网站首屏.jpeg", "README.txt"}


def main() -> None:
    if not DOCX.exists():
        raise SystemExit(f"找不到文档: {DOCX}")

    OUT.mkdir(parents=True, exist_ok=True)

    # 移除旧占位图，避免网页误用非 docx 素材
    for item in OUT.iterdir():
        if item.name in ALLOWED:
            continue
        if item.is_dir():
            shutil.rmtree(item)
            print(f"DEL dir {item.name}")
        else:
            item.unlink()
            print(f"DEL {item.name}")

    with zipfile.ZipFile(DOCX) as z:
        for src, dst in IMAGE_MAP.items():
            data = z.read(f"word/media/{src}")
            (OUT / dst).write_bytes(data)
            print(f"OK {src} -> {dst}")

    hero_src = OUT / "海报_细纹千载纸韵乐清.jpeg"
    (OUT / "Hero_网站首屏.jpeg").write_bytes(hero_src.read_bytes())
    print("OK Hero_网站首屏.jpeg")

    readme = OUT / "README.txt"
    readme.write_text(
        "本目录图片全部来自：乐刻IP设计.docx\n"
        "更新文档后运行：python extract_ip_from_docx.py\n\n"
        + "\n".join(f"  {v}" for v in sorted(ALLOWED - {"README.txt"})),
        encoding="utf-8",
    )
    print(f"Done. {len(list(OUT.iterdir()))} files.")


if __name__ == "__main__":
    main()
