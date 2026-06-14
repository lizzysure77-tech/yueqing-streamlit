# -*- coding: utf-8 -*-
"""
乐刻 · 乐清细纹刻纸数字化营销独立站 Streamlit 原型
品牌与 IP 来源：乐刻IP设计.docx
运行: streamlit run app.py
"""

from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).parent
CHART_PATH = BASE_DIR / "keyword_analysis.png"
IP_DIR = BASE_DIR / "assets" / "ip"

# 乐刻IP设计.docx 资源（jpeg/png 均可）
IP_ASSETS = {
    "hero": [
        "Hero_网站首屏.jpeg",
        "海报_细纹千载纸韵乐清.jpeg",
        "Hero_网站首屏.png",
    ],
    "lejian": [
        "乐笺_半身定稿.jpeg",
        "乐笺_海报用.jpeg",
        "小刻匠_半身定稿.png",
    ],
    "xiaokeling": [
        "小刻灵_Q版定稿.jpeg",
        "小刻灵_海报用.jpeg",
        "纸小仙_Q版定稿.png",
    ],
    "logo": ["LOGO_乐刻.jpeg", "LOGO_方形.png"],
    "lejian_emoji": ["乐笺_表情包.jpeg", "表情包_合集.png"],
    "xiaokeling_actions": ["小刻灵_动作延展.jpeg"],
    "lejian_spec": ["乐笺_设计规范.png"],
    "xiaokeling_spec": ["小刻灵_设计规范.png"],
    "poster_main": ["海报_细纹千载纸韵乐清.jpeg", "海报_国内版.png"],
    "poster_event": ["海报_指尖细纹.jpeg"],
    "lejian_turn": ["乐笺_三视图.jpeg"],
}

BRAND = {
    "name": "乐刻",
    "name_en": "YUE KE",
    "slogan": "乐刻，刻见东方",
    "slogan_en": "Yueke, Discover Oriental Art",
    "heritage": "乐清细纹刻纸 · 国家级非遗",
    "tagline": "细纹千载，纸韵乐清",
}

COLORS = {
    "paper": "#F5F2E8",
    "ink": "#2C3E32",
    "ink_soft": "#4A5D52",
    "accent": "#5C7A6A",
    "accent_light": "#C8D9CE",
    "line": "#D8D0C4",
    "mist": "#EDE8DF",
}


def find_ip(candidates: list[str]) -> Path | None:
    for name in candidates:
        p = IP_DIR / name
        if p.exists():
            return p
    return None


def show_ip(key: str, caption: str = "", use_container_width: bool = True) -> None:
    path = find_ip(IP_ASSETS[key])
    if path:
        st.image(str(path), caption=caption or path.stem, use_container_width=use_container_width)
    else:
        st.caption(f"（缺少素材：{key}）")


st.set_page_config(
    page_title="乐刻 · 乐清细纹刻纸",
    page_icon="✂",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');
    .stApp {{ background-color: {COLORS["paper"]}; color: {COLORS["ink"]}; font-family: "Noto Serif SC", serif; }}
    [data-testid="stSidebar"] {{ background-color: {COLORS["mist"]}; border-right: 1px solid {COLORS["line"]}; }}
    .hero-wrap {{
        padding: 2.5rem 1.5rem 2rem; text-align: center;
        background: linear-gradient(180deg, {COLORS["paper"]} 0%, {COLORS["mist"]} 100%);
        border-bottom: 1px solid {COLORS["line"]}; margin: -1rem -1rem 1.2rem -1rem;
    }}
    .hero-brand {{ font-size: 2rem; font-weight: 700; letter-spacing: 0.35em; color: {COLORS["ink"]}; }}
    .hero-slogan {{ font-size: 1.35rem; font-weight: 600; color: {COLORS["accent"]}; margin: 0.6rem 0; }}
    .hero-sub {{ font-size: 0.95rem; color: {COLORS["ink_soft"]}; }}
    .section-title {{
        font-size: 1.15rem; font-weight: 600; color: {COLORS["ink"]};
        border-left: 3px solid {COLORS["accent"]}; padding-left: 0.65rem; margin-bottom: 0.75rem;
    }}
  </style>
    """,
    unsafe_allow_html=True,
)


def render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div style="font-size:0.75rem;letter-spacing:0.3em;color:{COLORS["accent"]};">
                {BRAND["heritage"]}
            </div>
            <div class="hero-brand">{BRAND["name"]} · {BRAND["name_en"]}</div>
            <div class="hero-slogan">{BRAND["slogan"]}</div>
            <p class="hero-sub">{BRAND["slogan_en"]}</p>
            <p class="hero-sub" style="margin-top:0.5rem;">{BRAND["tagline"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    show_ip("hero", "品牌形象主视觉 ·《细纹千载，纸韵乐清》")
    c1, c2, c3 = st.columns(3)
    with c1:
        show_ip("lejian", "主 IP · 乐笺")
    with c2:
        show_ip("xiaokeling", "辅 IP · 小刻灵")
    with c3:
        show_ip("logo", "乐刻 LOGO")


def tab_brand_story() -> None:
    st.markdown('<div class="section-title">品牌故事</div>', unsafe_allow_html=True)
    st.markdown(
        """
**乐刻**缘起于非遗传承人张晓朵，与乐清细纹刻纸相伴半生的坚守。

出身艺术世家，八岁执刀，与龙船花纹、细纹刻纸结缘。数十年沉心古法，复刻《清明上河图》长卷，
将公益课堂送进校园与研学营地，让刻纸纹样走进水杯、杯垫与文创日常。

- **乐**：故土乐清，以刻为乐，盼非遗重获欢喜  
- **刻**：指尖匠心，敬畏古法，接续千年文脉  

乐刻以龙船花纹为根基，萃取雁荡灵秀、瓯江温婉，坚守「细如发丝、密如蛛网」之质感，
同时让非遗走出展厅，走进年轻人的生活。
        """
    )
    c1, c2 = st.columns(2)
    with c1:
        show_ip("poster_main", "品牌主视觉海报")
    with c2:
        show_ip("poster_event", "活动海报 ·《指尖细纹》")


def tab_ip_design() -> None:
    st.markdown('<div class="section-title">IP 设计 · 乐笺 & 小刻灵</div>', unsafe_allow_html=True)

    st.markdown("### 主 IP · 乐笺")
    st.markdown(
        """
以传承人张晓朵为原型。米白旗袍、青瓷蓝镶边、细纹刻刀，温婉灵动。
**乐**取品牌名，**笺**指纸张——以纸为媒，刻见东方。
        """
    )
    show_ip("lejian_turn", "乐笺三视图")
    show_ip("lejian_emoji", "乐笺表情包")
    show_ip("lejian_spec", "乐笺设计规范")

    st.markdown("### 辅 IP · 小刻灵")
    st.markdown(
        """
纸张拟人精灵，鎏金国风衣裙与蝶翼，指尖飘散纸屑光点。
主攻抖音、小红书科普，用年轻化表达消解非遗距离感。
        """
    )
    show_ip("xiaokeling_actions", "小刻灵动作延展")
    show_ip("xiaokeling_spec", "小刻灵设计规范")


def tab_patterns() -> None:
    st.markdown('<div class="section-title">纹样数字馆</div>', unsafe_allow_html=True)
    st.caption("龙船花纹样 · 传统吉祥 / 民俗场景 / 现代创新")
    show_ip("lejian", "乐笺 · 纹样鉴赏导览")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("龙船花 · 传统吉祥纹样")
    with c2:
        st.info("节庆窗花 · 民俗场景")
    with c3:
        st.info("新中式 · 国风纹样素材")


def tab_workshop() -> None:
    st.markdown('<div class="section-title">云端工坊</div>', unsafe_allow_html=True)
    st.caption("《指尖细纹》体验日 · 研学 / DIY / 文创")

    show_ip("xiaokeling_actions", "小刻灵 · 趣味科普引导")
    st.markdown(
        """
**体验项目**（活动海报）  
壹 入门体验 · 基础纹样　贰 进阶创作 · 龙船花纹  
叁 非遗拓印 · 刻纸纹样　肆 亲子互动 · 童趣刻纸  
伍 文创 DIY · 书签明信片　陆 大师课堂 · 传承人分享
        """
    )
    show_ip("poster_event", "指尖细纹 · 活动海报")

    if st.button("预约线下研学", use_container_width=True):
        st.success("演示：预约已提交")


def tab_hometown() -> None:
    st.markdown('<div class="section-title">我的家乡 UGC</div>', unsafe_allow_html=True)
    st.text_area("写下你与乐清细纹刻纸的故事", height=100, placeholder="我爱我的家乡…")
    st.multiselect("话题", ["#乐刻", "#非遗新造", "#国潮手作", "#乐清细纹刻纸"])
    if st.button("发布到留言墙", use_container_width=True):
        st.success("投稿已收录（演示）")
    show_ip("lejian_emoji", "乐笺表情包 · 社交互动")


def tab_analytics() -> None:
    st.markdown('<div class="section-title">关键词权重分析</div>', unsafe_allow_html=True)
    if CHART_PATH.exists():
        st.image(str(CHART_PATH), use_container_width=True)
    st.caption("架构推导见 wireframe_derivation_report.txt")


def main() -> None:
    with st.sidebar:
        show_ip("logo", "乐刻")
        st.markdown(f"### {BRAND['name']}")
        st.caption(BRAND["slogan"])
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
