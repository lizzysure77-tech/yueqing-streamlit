# -*- coding: utf-8 -*-
"""
乐清细纹刻纸 · 数字化营销独立站 Streamlit 原型
运行: streamlit run app.py
"""

from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).parent
CHART_PATH = BASE_DIR / "keyword_analysis.png"

# ── 东方精微美学 · 设计令牌 ──
COLORS = {
    "paper": "#F7F4ED",       # 宣纸白
    "ink": "#1C1C1C",         # 徽墨黑
    "ink_soft": "#4A4A4A",
    "cinnabar": "#C23A2B",    # 朱砂红点缀
    "cinnabar_light": "#E8D5D2",
    "line": "#D8D0C4",
    "mist": "#EDE8DF",
}

st.set_page_config(
    page_title="乐清细纹刻纸 · 数字文化馆",
    page_icon="✂",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');

    .stApp {{
        background-color: {COLORS["paper"]};
        color: {COLORS["ink"]};
        font-family: "Noto Serif SC", "SimSun", serif;
    }}

    [data-testid="stSidebar"] {{
        background-color: {COLORS["mist"]};
        border-right: 1px solid {COLORS["line"]};
    }}

    [data-testid="stSidebar"] .stMarkdown {{
        color: {COLORS["ink"]};
    }}

    .hero-wrap {{
        padding: 3.2rem 2rem 2.8rem;
        text-align: center;
        background: linear-gradient(180deg, {COLORS["paper"]} 0%, {COLORS["mist"]} 100%);
        border-bottom: 1px solid {COLORS["line"]};
        margin: -1rem -1rem 1.5rem -1rem;
    }}

    .hero-tag {{
        display: inline-block;
        font-size: 0.78rem;
        letter-spacing: 0.35em;
        color: {COLORS["cinnabar"]};
        border: 1px solid {COLORS["cinnabar_light"]};
        padding: 0.25rem 0.9rem;
        margin-bottom: 1rem;
    }}

    .hero-slogan {{
        font-size: clamp(1.8rem, 4vw, 2.6rem);
        font-weight: 700;
        color: {COLORS["ink"]};
        letter-spacing: 0.12em;
        line-height: 1.5;
        margin: 0.2rem 0 0.8rem;
    }}

    .hero-sub {{
        font-size: 1rem;
        color: {COLORS["ink_soft"]};
        letter-spacing: 0.08em;
        max-width: 36rem;
        margin: 0 auto;
    }}

    .hero-line {{
        width: 4rem;
        height: 2px;
        background: {COLORS["cinnabar"]};
        margin: 1.2rem auto 0;
    }}

    .section-card {{
        background: #FFFFFF;
        border: 1px solid {COLORS["line"]};
        border-radius: 2px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }}

    .section-title {{
        font-size: 1.15rem;
        font-weight: 600;
        color: {COLORS["ink"]};
        border-left: 3px solid {COLORS["cinnabar"]};
        padding-left: 0.65rem;
        margin-bottom: 0.75rem;
    }}

    div[data-testid="stTabs"] button {{
        font-family: "Noto Serif SC", serif;
        color: {COLORS["ink_soft"]};
    }}

    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: {COLORS["cinnabar"]} !important;
        border-bottom-color: {COLORS["cinnabar"]} !important;
    }}

    .stButton > button {{
        background-color: {COLORS["ink"]};
        color: {COLORS["paper"]};
        border: none;
        border-radius: 2px;
        letter-spacing: 0.1em;
    }}

    .stButton > button:hover {{
        background-color: {COLORS["cinnabar"]};
        color: white;
    }}

    hr {{
        border-color: {COLORS["line"]};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-tag">国家级非遗 · 乐清细纹刻纸</div>
            <div class="hero-slogan">方寸万千，纤毫传神</div>
            <p class="hero-sub">
                数字化美学叙事主阵地 · 文化背书 · 纹样典藏 · 研学体验 · 海内外传播
            </p>
            <div class="hero-line"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tab_patterns() -> None:
    st.markdown('<div class="section-title">纹样数字馆</div>', unsafe_allow_html=True)
    st.caption("美学观赏意图 → 瀑布流画廊 · 传统吉祥 / 民俗场景 / 现代创新")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**传统吉祥**")
        st.info("双喜 · 福禄 · 花鸟纹样高清库")
    with c2:
        st.markdown("**民俗场景**")
        st.info("节庆窗花 · 龙船花长卷数字展")
    with c3:
        st.markdown("**现代创新**")
        st.info("新中式美学 · 国风纹样素材下载")

    st.markdown(
        """
        <div class="section-card">
        <b>SEO 承接词</b>：新中式美学、中国传统纹样、中式窗花图案设计、国风纹样素材、东方镂空工艺
        </div>
        """,
        unsafe_allow_html=True,
    )


def tab_workshop() -> None:
    st.markdown('<div class="section-title">云端工坊</div>', unsafe_allow_html=True)
    st.caption("学习体验意图 → AIGC 纹样生成 · 研学预约 · DIY 材料包")

    left, right = st.columns([1, 1])
    with left:
        st.subheader("AIGC 纹样生成")
        prompt = st.text_input("输入意象关键词", placeholder="例如：雁荡山、龙船花、细纹镂空")
        if st.button("生成刻纸纹样预览", use_container_width=True):
            st.success("演示模式：已提交生成请求（原型占位）")
        st.markdown(
            """
            <div style="height:200px;border:1px dashed #D8D0C4;background:#F7F4ED;
            display:flex;align-items:center;justify-content:center;color:#4A4A4A;
            letter-spacing:0.2em;font-size:0.9rem;">
            AIGC 纹样预览区（原型占位）
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.subheader("研学 & 材料包")
        st.selectbox("课程类型", ["亲子非遗美育", "儿童手工非遗课程", "非遗剪纸 DIY 入门"])
        st.selectbox("材料包", ["刻纸工具套装", "刻纸材料包", "国潮文创伴手礼定制"])
        st.button("预约线下研学", use_container_width=True)

    st.markdown(
        """
        <div class="section-card">
        <b>SEO 承接词</b>：非遗剪纸DIY教程、儿童手工非遗课程、亲子非遗美育、AIGC刻纸纹样、国潮手作
        </div>
        """,
        unsafe_allow_html=True,
    )


def tab_hometown() -> None:
    st.markdown('<div class="section-title">我的家乡 UGC</div>', unsafe_allow_html=True)
    st.caption("社交种草意图 → 数字留言墙 · 家乡风物投稿")

    st.text_area("写下你与乐清细纹刻纸的故事", height=120, placeholder="我爱我的家乡…")
    c1, c2 = st.columns(2)
    with c1:
        st.file_uploader("上传风物照片 / 刻纸作品", type=["png", "jpg", "jpeg"])
    with c2:
        st.multiselect("话题标签", ["#非遗新造", "#国潮手作", "#我爱我的家乡", "#乐清细纹刻纸"])

    if st.button("发布到留言墙", use_container_width=True):
        st.balloons()
        st.success("投稿已收录（原型演示）")

    st.markdown("**热门 UGC**")
    for title, likes in [
        ("把雁荡山刻进一纸窗花里", 128),
        ("老街灯火下的细纹刻纸", 96),
        ("非遗新造 · 龙船花纹样二创", 84),
    ]:
        st.markdown(f"- {title}　❤ {likes}")


def tab_analytics() -> None:
    st.markdown('<div class="section-title">关键词权重分析</div>', unsafe_allow_html=True)
    st.caption("基于 20 个 SEO 关键词矩阵 · Weight = 搜索量 × (1 − 竞争度)")

    if CHART_PATH.exists():
        st.image(str(CHART_PATH), use_container_width=True)
    else:
        st.warning(
            f"未找到图表文件 `{CHART_PATH.name}`。请先运行：\n\n"
            "`python keyword_visualization.py`"
        )

    st.markdown(
        """
        <div class="section-card">
        <b>架构推导</b>：关键词意图聚类 → 纹样数字馆 / 云端工坊 / 我的家乡 UGC 等模块落点。
        详见 <code>wireframe_derivation_report.txt</code>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    with st.sidebar:
        st.markdown("### 乐清细纹刻纸")
        st.markdown("**数字文化馆**")
        st.divider()
        st.markdown("导航")
        nav = st.radio(
            "选择板块",
            ["首页总览", "纹样数字馆", "云端工坊", "我的家乡 UGC", "关键词分析"],
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown("**品牌色**")
        st.markdown(
            f'<span style="color:{COLORS["paper"]};background:{COLORS["ink"]};padding:2px 8px;">宣纸白</span> '
            f'<span style="color:white;background:{COLORS["cinnabar"]};padding:2px 8px;">朱砂</span>',
            unsafe_allow_html=True,
        )
        st.caption("xiwenke.cn · 原型演示")

    render_hero()

    if nav == "首页总览":
        t1, t2, t3, t4 = st.tabs(
            ["纹样数字馆", "云端工坊", "我的家乡 UGC", "关键词分析"]
        )
        with t1:
            tab_patterns()
        with t2:
            tab_workshop()
        with t3:
            tab_hometown()
        with t4:
            tab_analytics()
    elif nav == "纹样数字馆":
        tab_patterns()
    elif nav == "云端工坊":
        tab_workshop()
    elif nav == "我的家乡 UGC":
        tab_hometown()
    else:
        tab_analytics()

    st.divider()
    st.caption("数字化营销课程作业 · Streamlit 落地页原型 · 非商用演示")


if __name__ == "__main__":
    main()
