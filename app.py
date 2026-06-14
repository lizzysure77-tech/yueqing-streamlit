# -*- coding: utf-8 -*-
"""
乐刻 · 乐清细纹刻纸数字化营销独立站 Streamlit 原型
品牌与 IP 来源：乐刻IP设计.docx
运行: streamlit run app.py
"""

import base64
import io
from pathlib import Path

import streamlit as st
from PIL import Image

try:
    from ip_cutout import remove_paper_background
except ImportError:
    remove_paper_background = None

BASE_DIR = Path(__file__).parent
CHART_PATH = BASE_DIR / "keyword_analysis.png"
IP_DIR = BASE_DIR / "assets" / "ip"

IP_ASSETS = {
    # 全部素材来自 乐刻IP设计.docx（运行 extract_ip_from_docx.py 同步）
    "hero_bg": ["海报_细纹千载纸韵乐清.jpeg", "Hero_网站首屏.jpeg"],
    "section_bg": ["海报_指尖细纹.jpeg", "海报_细纹千载纸韵乐清.jpeg"],
    "lejian": ["乐笺_全身定稿.jpeg", "乐笺_海报用.jpeg"],
    "xiaokeling": ["小刻灵_Q版定稿.jpeg", "小刻灵_海报用.jpeg"],
    "logo": ["LOGO_乐刻.jpeg"],
    "lejian_emoji": ["乐笺_半身定稿.jpeg", "乐笺_表情包.jpeg"],
    "xiaokeling_actions": ["小刻灵_动作延展.jpeg"],
    "lejian_spec": ["乐笺_设计规范.png"],
    "xiaokeling_spec": ["小刻灵_设计规范.png"],
    "lejian_turn": ["乐笺_三视图.jpeg"],
    "patterns_header": ["乐笺_全身定稿.jpeg"],
    "workshop_guide": ["小刻灵_Q版定稿.jpeg"],
    "poster_main": ["海报_细纹千载纸韵乐清.jpeg", "Hero_网站首屏.jpeg"],
    "poster_event": ["海报_指尖细纹.jpeg"],
}

BRAND = {
    "name": "乐刻",
    "name_en": "YUE KE",
    "slogan": "乐刻，刻见东方",
    "slogan_en": "Yueke, Discover Oriental Art",
    "heritage": "乐清细纹刻纸 · 国家级非遗",
    "tagline": "细纹千载，纸韵乐清",
    "essence": "瓯越大地上的文明之花，一针一纸承续千年文脉。",
    "hero_verse": "细线游走处，是篆刻之趣；跃然纸上时，是所思所想。",
}

# IP 设计效果 8 张（与成果展示.html 一致）
IP_SHOWCASE = [
    ("logo", "① 乐刻 LOGO", False, False, ""),
    ("lejian", "② 乐笺 · 全身定稿", True, True, "ip-cutout-lg"),
    ("lejian_turn", "③ 乐笺 · 三视图", True, True, "ip-cutout-md"),
    ("lejian_emoji", "④ 乐笺 · 表情包合图", False, False, "ip-cutout-md"),
    ("xiaokeling", "⑤ 小刻灵 · Q 版定稿", True, True, "ip-cutout-lg"),
    ("xiaokeling_actions", "⑥ 小刻灵 · 动作延展", True, True, "ip-cutout-md"),
    ("poster_main", "⑦ 海报 · 细纹千载，纸韵乐清", False, True, "ip-cutout-poster"),
    ("poster_event", "⑧ 海报 · 指尖细纹", False, True, "ip-cutout-poster"),
]

COLORS = {
    "paper": "#F5F2E8",
    "ink": "#2C3E32",
    "ink_soft": "#4A5D52",
    "accent": "#5C7A6A",
    "accent_light": "#C8D9CE",
    "line": "#D8D0C4",
    "mist": "#EDE8DF",
}


CUTOUT_DIR = IP_DIR / "cutout"
CUTOUT_FILES = {
    "lejian": "lejian_full.png",
    "lejian_turn": "lejian_turn.png",
    "xiaokeling": "xiaokeling.png",
    "xiaokeling_actions": "xiaokeling_actions.png",
    "patterns_header": "lejian_full.png",
    "workshop_guide": "xiaokeling.png",
}


def find_ip(candidates: list[str]) -> Path | None:
    for name in candidates:
        p = IP_DIR / name
        if p.exists():
            return p
    return None


@st.cache_data(show_spinner=False)
def file_to_data_uri(path_str: str, as_png: bool = False, cutout: bool = False) -> str:
    path = Path(path_str)
    if cutout and remove_paper_background is not None:
        img = remove_paper_background(path)
    else:
        img = Image.open(path).convert("RGBA")
        if cutout:
            pixels = img.load()
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b, a = pixels[x, y]
                    if a < 20:
                        continue
                    if r > 228 and g > 222 and b > 210:
                        pixels[x, y] = (r, g, b, 0)
    buf = io.BytesIO()
    if as_png or cutout:
        img.save(buf, format="PNG")
        mime = "image/png"
    else:
        img.convert("RGB").save(buf, format="JPEG", quality=88)
        mime = "image/jpeg"
    encoded = base64.b64encode(buf.getvalue()).decode()
    return f"data:{mime};base64,{encoded}"


def asset_uri(key: str, cutout: bool = False) -> str | None:
    if cutout and key in CUTOUT_FILES:
        baked = CUTOUT_DIR / CUTOUT_FILES[key]
        if baked.exists():
            return file_to_data_uri(str(baked), as_png=True, cutout=False)
    path = find_ip(IP_ASSETS[key])
    if not path:
        return None
    is_jpeg = path.suffix.lower() in {".jpg", ".jpeg"}
    remove_bg = cutout and is_jpeg
    as_png = path.suffix.lower() == ".png" or remove_bg
    return file_to_data_uri(str(path), as_png=as_png, cutout=remove_bg)


def inject_styles(page_bg_uri: str | None) -> None:
    bg_rule = ""
    if page_bg_uri:
        bg_rule = (
            f"background-image: linear-gradient(180deg, "
            f"rgba(245,242,232,0.94) 0%, rgba(245,242,232,0.88) 100%), "
            f"url('{page_bg_uri}');"
            "background-size: cover; background-position: center top; "
            "background-attachment: fixed;"
        )
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');
        .stApp {{
            background-color: {COLORS["paper"]};
            color: {COLORS["ink"]};
            font-family: "Noto Serif SC", serif;
            {bg_rule}
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(237, 232, 223, 0.96);
            border-right: 1px solid {COLORS["line"]};
        }}
        [data-testid="stImage"] img {{
            max-height: 320px !important;
            width: auto !important;
            object-fit: contain !important;
            margin: 0 auto;
        }}
        .hero-panel {{
            position: relative;
            border-radius: 14px;
            overflow: hidden;
            margin: -0.5rem 0 1rem 0;
            border: 1px solid {COLORS["line"]};
        }}
        .hero-panel .hero-bg {{
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center;
            opacity: 0.22;
            filter: blur(1px);
        }}
        .hero-panel .hero-veil {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
                105deg,
                rgba(245,242,232,0.92) 0%,
                rgba(245,242,232,0.78) 45%,
                rgba(245,242,232,0.72) 100%
            );
        }}
        .hero-panel .hero-body {{
            position: relative;
            z-index: 2;
            display: grid;
            grid-template-columns: minmax(120px, 1fr) minmax(220px, 1.4fr) minmax(120px, 1fr);
            gap: 0.5rem;
            align-items: end;
            padding: 1.5rem 1rem 1rem;
        }}
        .hero-text {{
            text-align: center;
            padding: 0.5rem 0 1rem;
        }}
        .hero-brand {{
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: 0.35em;
            color: {COLORS["ink"]};
        }}
        .hero-slogan {{
            font-size: 1.25rem;
            font-weight: 600;
            color: {COLORS["accent"]};
            margin: 0.5rem 0;
        }}
        .hero-sub {{
            font-size: 0.9rem;
            color: {COLORS["ink_soft"]};
            margin: 0.15rem 0;
        }}
        .cutout-wrap {{
            text-align: center;
            padding: 0.25rem;
        }}
        .ip-cutout {{
            max-height: 260px;
            width: auto;
            max-width: 100%;
            object-fit: contain;
            display: block;
            margin: 0 auto;
            filter: drop-shadow(0 6px 18px rgba(44, 62, 50, 0.1));
        }}
        .ip-cutout-soft {{
            opacity: 0.72;
            filter: drop-shadow(0 4px 14px rgba(44, 62, 50, 0.08));
        }}
        .ip-cutout-sm {{
            max-height: 88px;
            filter: drop-shadow(0 4px 12px rgba(44, 62, 50, 0.12));
        }}
        .ip-cutout-md {{
            max-height: 200px;
        }}
        .ip-cutout-lg {{
            max-height: 300px;
        }}
        .ip-cutout-poster {{
            max-height: 200px;
            opacity: 0.82;
        }}
        .brand-verse {{
            background: rgba(255, 255, 255, 0.68);
            border: 1px solid {COLORS["line"]};
            border-radius: 10px;
            padding: 1.1rem 1.25rem;
            margin: 0.5rem 0 1.2rem;
            text-align: center;
            color: {COLORS["ink_soft"]};
            font-size: 0.95rem;
            line-height: 1.85;
        }}
        .brand-verse strong {{
            color: {COLORS["accent"]};
        }}
        .wordplay-card {{
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid {COLORS["line"]};
            border-radius: 8px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.85rem;
        }}
        .wordplay-card h4 {{
            margin: 0 0 0.45rem;
            color: {COLORS["accent"]};
            font-size: 0.95rem;
        }}
        .cutout-label {{
            font-size: 0.75rem;
            color: {COLORS["ink_soft"]};
            margin-top: 0.35rem;
        }}
        .section-panel {{
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            margin: 0.75rem 0 1rem;
            border: 1px solid {COLORS["line"]};
        }}
        .section-panel .section-bg {{
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center;
            opacity: 0.14;
        }}
        .section-panel .section-veil {{
            position: absolute;
            inset: 0;
            background: rgba(245, 242, 232, 0.9);
        }}
        .section-panel .section-inner {{
            position: relative;
            z-index: 2;
            padding: 1.25rem 1.1rem;
        }}
        .section-title {{
            font-size: 1.15rem;
            font-weight: 600;
            color: {COLORS["ink"]};
            border-left: 3px solid {COLORS["accent"]};
            padding-left: 0.65rem;
            margin-bottom: 0.75rem;
        }}
        .ip-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
            align-items: flex-end;
            margin: 0.5rem 0;
        }}
        .ip-row .cutout-wrap {{
            flex: 0 1 auto;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_cutout(
    key: str,
    label: str = "",
    size: str = "",
    cutout: bool = True,
    soft: bool = False,
) -> None:
    uri = asset_uri(key, cutout=cutout)
    if not uri:
        st.caption(f"（缺少素材：{key}）")
        return
    cls = f"ip-cutout {size}".strip()
    if soft:
        cls += " ip-cutout-soft"
    label_html = f'<div class="cutout-label">{label}</div>' if label else ""
    st.markdown(
        f'<div class="cutout-wrap"><img src="{uri}" class="{cls}" alt="{label or key}"/>{label_html}</div>',
        unsafe_allow_html=True,
    )


def render_brand_essence() -> None:
    st.markdown(
        f"""
        <div class="brand-verse">
            <p><strong>{BRAND["essence"]}</strong></p>
            <p>{BRAND["hero_verse"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def brand_wordplay_markdown() -> str:
    return """
### 乐刻 · 同音不同字，同字不同音

| 字 | 读音与意象 | 品牌内涵 |
|:---|:---|:---|
| **乐** | 乐清故土；以刻为**乐**（lè） | 地域根脉与手艺之乐、观纹之乐 |
| **刻** | 刀尖**刻**画；时光**刻**印 | 工艺之本、匠心之痕 |
| **乐刻** | 乐在其中，**刻**下时光 | 双关：乐土印记 × 以刻为乐 |

在瓯越山水之间，细纹刻纸如一朵静放的**文明之花**——不喧哗，却在方寸纸面开满纹样。

---

### 乐笺 · 纸上有情，跃然纸上

| 字 | 含义 | IP 内涵 |
|:---|:---|:---|
| **乐** | 与品牌同脉 | 乐刻精神的拟人化身 |
| **笺** | 信笺、纸笺 | 以纸为媒，承托心绪与纹样 |

**篆刻之趣**分两层：一是**过程**——刀尖游走、细线层叠时的专注与沉浸；二是**成品**——纹饰成形的惊艳与圆满。  
所思所想，不必多言，皆能**跃然纸上**；一纸细纹，既是技艺，也是情感。
"""


def render_ip_showcase_grid() -> None:
    for row_start in (0, 4):
        cols = st.columns(4)
        for col, item in zip(cols, IP_SHOWCASE[row_start:row_start + 4]):
            with col:
                key, label, use_cutout, soft, size = item
                show_cutout(key, label, size, cutout=use_cutout, soft=soft)
    bg_uri = asset_uri(bg_key, cutout=False)
    bg_style = f"background-image: url('{bg_uri}');" if bg_uri else ""
    st.markdown(
        f"""
        <div class="section-panel">
            <div class="section-bg" style="{bg_style} opacity:{opacity_style};"></div>
            <div class="section-veil"></div>
            <div class="section-inner">{inner_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    bg_uri = asset_uri("hero_bg", cutout=False)
    lejian_uri = asset_uri("lejian", cutout=True)
    logo_uri = asset_uri("logo", cutout=False)
    xkl_uri = asset_uri("xiaokeling", cutout=True)
    soft_cls = " ip-cutout-soft"
    lejian_img = (
        f'<div class="cutout-wrap"><img src="{lejian_uri}" class="ip-cutout{soft_cls}" alt="乐笺"/></div>'
        if lejian_uri
        else ""
    )
    logo_img = (
        f'<div class="cutout-wrap"><img src="{logo_uri}" class="ip-cutout ip-cutout-sm" alt="乐刻"/></div>'
        if logo_uri
        else ""
    )
    xkl_img = (
        f'<div class="cutout-wrap"><img src="{xkl_uri}" class="ip-cutout{soft_cls}" alt="小刻灵"/></div>'
        if xkl_uri
        else ""
    )
    bg_div = f'<div class="hero-bg" style="background-image:url(\'{bg_uri}\');"></div>' if bg_uri else ""
    st.markdown(
        f"""
        <div class="hero-panel">
            {bg_div}
            <div class="hero-veil"></div>
            <div class="hero-body">
                <div>{lejian_img}<div class="cutout-label">主 IP · 乐笺</div></div>
                <div class="hero-text">
                    <div style="font-size:0.72rem;letter-spacing:0.28em;color:{COLORS["accent"]};">
                        {BRAND["heritage"]}
                    </div>
                    <div class="hero-brand">{BRAND["name"]} · {BRAND["name_en"]}</div>
                    <div class="hero-slogan">{BRAND["slogan"]}</div>
                    <p class="hero-sub">{BRAND["slogan_en"]}</p>
                    <p class="hero-sub">{BRAND["tagline"]}</p>
                    <p class="hero-sub" style="font-size:0.82rem;margin-top:0.45rem;">
                        {BRAND["essence"]}
                    </p>
                    {logo_img}
                </div>
                <div>{xkl_img}<div class="cutout-label">辅 IP · 小刻灵</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tab_brand_story() -> None:
    inner = """
        <div class="section-title">品牌故事</div>
        <p>雁荡山下，瓯江之畔，<strong>乐刻</strong>缘起于非遗传承人张晓朵与乐清细纹刻纸相伴半生的坚守。
        这里是瓯越大地上的文明之花——一纸细纹，承载山水灵秀与千年手艺人文。</p>
        <p>出身艺术世家，八岁执刀，与龙船花纹结缘。数十年沉心古法，复刻《清明上河图》长卷；
        将公益课堂送进校园与研学营地，让刻纸纹样走进水杯、杯垫与文创日常。</p>
        <div class="wordplay-card">
            <h4>乐刻 · 一字多义</h4>
            <p><strong>乐</strong>：乐清故土；以刻为<strong>乐</strong>；愿人阅纹而生喜悦。<br>
            <strong>刻</strong>：刀尖刻画；时光刻印；一笔一刻见匠心。<br>
            同音不同字、同字不同音——<strong>乐刻</strong>，既是乐土印记，也是以刻为乐。</p>
        </div>
        <div class="wordplay-card">
            <h4>乐笺 · 跃然纸上</h4>
            <p><strong>笺</strong>者，信笺、纸笺；纸为媒，情为墨。细线游走是<strong>篆刻之趣</strong>（过程），
            纹饰成形是<strong>成品之悦</strong>；所思所想，皆可跃然纸上，凝于细纹。</p>
        </div>
        <p>乐刻以龙船花纹为根基，萃取雁荡灵秀、瓯江温婉，坚守「细如发丝、密如蛛网」之质感，
        让非遗走出展厅，走进年轻人的生活。</p>
    """
    section_with_bg("section_bg", inner)
    st.markdown(brand_wordplay_markdown())


def tab_ip_design() -> None:
    st.markdown('<div class="section-title">IP 设计 · 乐笺 & 小刻灵</div>', unsafe_allow_html=True)
    st.markdown(
        """
**乐笺**是乐刻主 IP，以传承人张晓朵为原型：米白旗袍、青瓷蓝镶边、手持刻刀，温婉灵动。  
**小刻灵**是辅 IP，纸张精灵，负责年轻化科普与工坊引导。  
一字一笺、一笔一刻——同音不同字，同字不同音，让瓯越文明之花跃然纸上。
        """
    )
    st.markdown(brand_wordplay_markdown())

    st.markdown("#### IP 设计效果（8 张定稿 · 与成果展示一致）")
    render_ip_showcase_grid()

    with st.expander("乐笺 / 小刻灵 设计规范（参考大图）"):
        c1, c2 = st.columns(2)
        with c1:
            show_cutout("lejian_spec", "乐笺设计规范", "ip-cutout-md", cutout=False)
        with c2:
            show_cutout("xiaokeling_spec", "小刻灵设计规范", "ip-cutout-md", cutout=False)


def tab_patterns() -> None:
    section_with_bg(
        "hero_bg",
        '<div class="section-title">纹样数字馆</div>'
        '<p style="color:#4A5D52;">龙船花纹样 · 传统吉祥 / 民俗场景 / 现代创新</p>',
        opacity_style="0.12",
    )
    show_cutout("patterns_header", "纹样导览", "ip-cutout-md")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("龙船花 · 传统吉祥纹样")
    with c2:
        st.info("节庆窗花 · 民俗场景")
    with c3:
        st.info("新中式 · 国风纹样素材")


def tab_workshop() -> None:
    section_with_bg(
        "section_bg",
        '<div class="section-title">云端工坊</div>'
        '<p style="color:#4A5D52;">《指尖细纹》体验日 · 研学 / DIY / 文创</p>',
    )
    show_cutout("workshop_guide", "小刻灵 · 工坊引导", "ip-cutout-md")
    st.markdown(
        """
**体验项目**  
壹 入门体验 · 基础纹样　贰 进阶创作 · 龙船花纹  
叁 非遗拓印 · 刻纸纹样　肆 亲子互动 · 童趣刻纸  
伍 文创 DIY · 书签明信片　陆 大师课堂 · 传承人分享
        """
    )
    if st.button("预约线下研学", use_container_width=True):
        st.success("演示：预约已提交")


def tab_hometown() -> None:
    st.markdown('<div class="section-title">我的家乡 UGC</div>', unsafe_allow_html=True)
    show_cutout("lejian_emoji", "", "ip-cutout-sm", cutout=False)
    st.text_area("写下你与乐清细纹刻纸的故事", height=100, placeholder="我爱我的家乡…")
    st.multiselect("话题", ["#乐刻", "#非遗新造", "#国潮手作", "#乐清细纹刻纸"])
    if st.button("发布到留言墙", use_container_width=True):
        st.success("投稿已收录（演示）")


def tab_analytics() -> None:
    st.markdown('<div class="section-title">关键词权重分析</div>', unsafe_allow_html=True)
    if CHART_PATH.exists():
        st.image(str(CHART_PATH), use_container_width=True)
    st.caption("架构推导见 wireframe_derivation_report.txt")


def main() -> None:
    st.set_page_config(
        page_title="乐刻 · 乐清细纹刻纸",
        page_icon="✂",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    page_bg = asset_uri("hero_bg", cutout=False)
    inject_styles(page_bg)

    with st.sidebar:
        show_cutout("logo", "乐刻", "ip-cutout-sm", cutout=False)
        st.markdown(f"### {BRAND['name']}")
        st.caption(f"{BRAND['slogan']} · {BRAND['essence']}")
        st.divider()
        nav = st.radio(
            "导航",
            [
                "首页总览",
                "品牌故事",
                "IP 设计",
                "纹样数字馆",
                "云端工坊",
                "我的家乡 UGC",
                "关键词分析",
            ],
            label_visibility="collapsed",
        )
        st.divider()
        st.caption("乐清细纹刻纸数字文化馆 · 原型")

    render_hero()
    render_brand_essence()

    pages = {
        "首页总览": lambda: None,
        "品牌故事": tab_brand_story,
        "IP 设计": tab_ip_design,
        "纹样数字馆": tab_patterns,
        "云端工坊": tab_workshop,
        "我的家乡 UGC": tab_hometown,
        "关键词分析": tab_analytics,
    }

    if nav == "首页总览":
        t1, t2, t3, t4, t5 = st.tabs(
            ["品牌故事", "IP 设计", "纹样数字馆", "云端工坊", "关键词分析"]
        )
        with t1:
            tab_brand_story()
        with t2:
            tab_ip_design()
        with t3:
            tab_patterns()
        with t4:
            tab_workshop()
        with t5:
            tab_analytics()
    else:
        pages[nav]()

    st.divider()
    st.caption("数字化营销课程作业 · 乐刻品牌 IP · Streamlit 原型")


if __name__ == "__main__":
    main()
