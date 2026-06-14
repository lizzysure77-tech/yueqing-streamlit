# -*- coding: utf-8 -*-
"""预生成抠图 PNG，供 Streamlit 直接加载"""
from pathlib import Path

from ip_cutout import bake_cutout

BASE = Path(__file__).parent
IP = BASE / "assets" / "ip"
OUT = IP / "cutout"

JOBS = {
    "lejian_full.png": "乐笺_海报用.jpeg",
    "lejian_turn.png": "乐笺_三视图.jpeg",
    "xiaokeling.png": "小刻灵_Q版定稿.jpeg",
    "xiaokeling_actions.png": "小刻灵_动作延展.jpeg",
    "lejian_poster.png": "乐笺_海报用.jpeg",
    "xiaokeling_poster.png": "小刻灵_海报用.jpeg",
}

if __name__ == "__main__":
    for out_name, src_name in JOBS.items():
        src = IP / src_name
        if src.exists():
            bake_cutout(src, OUT / out_name)
            print(f"OK {src_name} -> cutout/{out_name}")
        else:
            print(f"SKIP missing {src_name}")
