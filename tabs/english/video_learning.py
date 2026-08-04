"""视频学习 — 嵌入式播放器(倍速/循环) + 右侧笔记"""

import re
import streamlit as st
import streamlit.components.v1 as components


def render_content():
    from progress import save_english_note, load_english_notes
    from rag_engine import save_resource_to_kb

    YOUZACK_PRESETS = {
        "Friends 老友记": "https://www.youzack.com/Tag/Index/Friends",
        "Desperate Housewives 绝望主妇": "https://www.youzack.com/Tag/Index/DesperateHousewives",
        "Modern Family 摩登家庭": "https://www.youzack.com/Tag/Index/ModernFamily",
        "The Big Bang Theory 生活大爆炸": "https://www.youzack.com/Tag/Index/erta",
    }

    source_type = st.radio(
        "视频来源",
        ["🎬 YouTube", "📺 youzack 美剧"],
        horizontal=True,
        key="eng_video_source",
    )

    if source_type == "🎬 YouTube":
        _render_youtube_player()
    else:
        _render_youzack_player(YOUZACK_PRESETS)


def _render_youtube_player():
    from components.video_player import youtube_player_html
    from progress import save_english_note, load_english_notes
    from rag_engine import save_resource_to_kb

    url = st.text_input("YouTube 视频链接", placeholder="https://www.youtube.com/watch?v=...", key="eng_yt_url")
    video_id = _extract_youtube_id(url)

    col_speed, col_loop = st.columns([2, 1])
    with col_speed:
        speed = st.select_slider("倍速", options=[1.0, 1.25, 1.5, 2.0, 2.5], value=1.0, key="eng_speed")
    with col_loop:
        loop = st.checkbox("循环播放", key="eng_loop")

    if video_id:
        col_video, col_notes = st.columns([3, 2])
        with col_video:
            html = youtube_player_html(video_id, speed, loop)
            components.html(html, height=400, scrolling=False)
        with col_notes:
            _render_notes_panel(video_id, url)
    elif url:
        st.warning("无法识别 YouTube 链接，请粘贴完整 URL")


def _render_youzack_player(presets: dict):
    from components.video_player import youzack_player_html
    from progress import save_english_note, load_english_notes

    col_preset, col_custom = st.columns([2, 1])
    with col_preset:
        show = st.selectbox("选择美剧", ["自定义"] + list(presets.keys()), key="eng_yz_show")
    with col_custom:
        if show == "自定义":
            yz_url = st.text_input("youzack 链接", key="eng_yz_url")
        else:
            yz_url = presets[show]

    if yz_url:
        col_video, col_notes = st.columns([3, 2])
        with col_video:
            st.link_button("🔗 在 youzack.com 打开（推荐）", yz_url)
            st.caption("youzack 提供字幕对照、生词标注等功能，建议在新标签页中使用")
        with col_notes:
            source_key = yz_url.split("/")[-1] or "youzack"
            _render_notes_panel(source_key, yz_url)


def _render_notes_panel(source_key: str, source_url: str):
    from progress import save_english_note, load_english_notes
    from rag_engine import save_resource_to_kb

    st.markdown("#### 📝 学习笔记")

    note_text = st.text_area(
        "记录学习笔记",
        placeholder="记录生词、句型、听力要点...",
        height=200,
        key=f"eng_note_{source_key}",
        label_visibility="collapsed",
    )

    col_save, col_kb = st.columns(2)
    with col_save:
        if st.button("💾 保存笔记", key=f"save_note_{source_key}", use_container_width=True):
            if note_text.strip():
                save_english_note(source_key, note_text.strip(), source_url)
                st.success("已保存")
                st.rerun()
    with col_kb:
        if st.button("📚 存入知识库", key=f"kb_note_{source_key}", use_container_width=True):
            if note_text.strip():
                name = f"english_note_{source_key}"
                save_resource_to_kb(note_text.strip(), name, "english")
                st.success("已保存到 kb/english/")

    notes = load_english_notes(source_key)
    if notes:
        st.markdown("---")
        st.caption(f"历史笔记（{len(notes)} 条）")
        for n in reversed(notes[-5:]):
            with st.container(border=True):
                st.caption(n["date"][:16])
                st.markdown(n["content"])


def _extract_youtube_id(url: str) -> str:
    if not url:
        return ""
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:embed/)([a-zA-Z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return ""
