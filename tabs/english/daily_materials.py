"""每日素材 — 浏览/搜索 → 选中直接播放 + 右侧笔记"""

import re
import os
import streamlit as st
import requests
from datetime import datetime

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

CHANNEL_CATEGORIES = {
    "🔍 全部 (自由搜索)": [],
    "A. 工程英语/技术表达": [
        {"name": "Engineering Made Easy", "id": "UCSk8Ys0LqZF8sjcOUCnFN3Q"},
        {"name": "Tech English", "id": "UCv0jq3uFevMUAzbXIn4AlVQ"},
        {"name": "Effective Technical Communication", "id": "UChU8Ii5E2VVceKwsOAZD-dg"},
        {"name": "Geeks Talk", "id": "UCiBT0nqaI8nri-W13wqDlKA"},
        {"name": "English with Lucy", "id": "UCz4tgANd4yy8Oe0iXCdSWfA"},
        {"name": "Speak English With Vanessa", "id": "UCxJGMJbjokfnr2-s4_RXPxQ"},
        {"name": "All Ears English", "id": "UCajKaiBJSwYcDFbfMICpSpA"},
        {"name": "BBC Learning English", "id": "UCHaHD477h-FICLkKas8CD3g"},
    ],
    "B. IT/编程/软件工程": [
        {"name": "freeCodeCamp.org", "id": "UC8butISFwT-Wl7EV0hUK0BQ"},
        {"name": "Fireship", "id": "UCsBjURrPoezykLs9EqgamOA"},
        {"name": "CS Dojo", "id": "UCxX9wt5FWQUAAz4UrysqK9A"},
        {"name": "The Cherno", "id": "UCQ-W1KE9EYfdxhL6S4twUNw"},
        {"name": "Academind", "id": "UCSJbGtTlrDami-tDGPUV9-w"},
        {"name": "The Coding Train", "id": "UCvjgXvBlbQiydffZU7m1_aw"},
    ],
    "C. AI/数据科学/云计算": [
        {"name": "AI Explained", "id": "UCNJ1Ymd5yFuUPtn21xtRbbw"},
        {"name": "StatQuest with Josh Starmer", "id": "UCtYLUTtgS3k1Fg4y5tAhLbw"},
        {"name": "TensorFlow", "id": "UC0rqucBdTuFTjJiefW5t-IQ"},
        {"name": "AWS", "id": "UCd6MoB9NC6uYN2grvUNT-Zg"},
        {"name": "Microsoft Developer", "id": "UCsMica-v34Irf9KVTh6xx-g"},
    ],
    "D. 真实场景/进阶听力": [
        {"name": "Google Developers", "id": "UC_x5XG1OV2P6uZZ5FSM9Ttw"},
        {"name": "MIT OpenCourseWare", "id": "UCEBb1b_L6zDS3xTUrIALZOw"},
        {"name": "Harvard Engineering", "id": "UCeOqa_ZbKo88RmL5z8Oz5Ww"},
        {"name": "Veritasium", "id": "UCHnyfMqiRRG1u-2MsSQLbXA"},
        {"name": "TED", "id": "UCAuUUnT6oDeKwE6v1NGQxug"},
        {"name": "TED-Ed", "id": "UCsooa4yRKGN_zEE8iknghZA"},
    ],
}



def _fetch_channel_videos(channel_id: str, keyword: str = "", max_results: int = 6) -> list:
    if not YOUTUBE_API_KEY:
        return []
    try:
        params = {
            "part": "snippet",
            "order": "date",
            "type": "video",
            "maxResults": max_results,
            "key": YOUTUBE_API_KEY,
        }
        if channel_id:
            params["channelId"] = channel_id
        if keyword:
            params["q"] = keyword
        if not channel_id:
            params["relevanceLanguage"] = "en"
        resp = requests.get("https://www.googleapis.com/youtube/v3/search", params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        results = []
        for item in items:
            vid = item["id"].get("videoId", "")
            snippet = item.get("snippet", {})
            if vid:
                results.append({
                    "title": snippet.get("title", ""),
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "video_id": vid,
                    "channel": snippet.get("channelTitle", ""),
                    "published": snippet.get("publishedAt", "")[:10],
                })
        return results
    except Exception:
        return []


def render_content():

    _render_video_search()

    # 播放区：选中视频后显示
    if st.session_state.get("eng_playing"):
        st.markdown("---")
        _render_player_with_notes()


def _render_video_search():
    if not YOUTUBE_API_KEY:
        st.info("需要配置 YOUTUBE_API_KEY 环境变量")
        return
    col_cat, col_kw = st.columns([1, 2])
    with col_cat:
        category = st.selectbox("分类", list(CHANNEL_CATEGORIES.keys()), key="eng_category")
    with col_kw:
        keyword = st.text_input("关键词", value="", placeholder="输入搜索关键词...", key="yt_eng_kw")
    if st.button("🔍 搜索", key="yt_eng_search"):
        channels = CHANNEL_CATEGORIES[category]
        with st.spinner("搜索中..."):
            if channels:
                all_videos = []
                for ch in channels:
                    all_videos.extend(_fetch_channel_videos(ch["id"], keyword, 4))
                st.session_state["yt_eng_results"] = all_videos
            else:
                q = keyword if keyword.strip() else "English learning"
                params = {
                    "part": "snippet", "q": q, "type": "video",
                    "order": "relevance", "maxResults": 8,
                    "relevanceLanguage": "en", "key": YOUTUBE_API_KEY,
                }
                try:
                    resp = requests.get("https://www.googleapis.com/youtube/v3/search", params=params, timeout=10)
                    items = resp.json().get("items", [])
                    st.session_state["yt_eng_results"] = [{
                        "title": i["snippet"]["title"],
                        "url": f"https://www.youtube.com/watch?v={i['id']['videoId']}",
                        "video_id": i["id"]["videoId"],
                        "channel": i["snippet"].get("channelTitle", ""),
                        "published": i["snippet"].get("publishedAt", "")[:10],
                    } for i in items if i["id"].get("videoId")]
                except Exception:
                    st.error("搜索失败，请检查网络或 API Key")
    _render_video_list(st.session_state.get("yt_eng_results", []), "youtube")




def _render_video_list(videos: list, source: str):
    if not videos:
        return
    for i, v in enumerate(videos):
        with st.container(border=True):
            col_info, col_actions = st.columns([4, 2])
            with col_info:
                st.markdown(f"**[{v['title']}]({v['url']})**")
                st.caption(f"{v.get('channel', '')} · {v.get('published', '')}")
            with col_actions:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("▶️ 播放", key=f"play_{source}_{i}", use_container_width=True):
                        st.session_state["eng_playing"] = {
                            "video_id": v.get("video_id", ""),
                            "title": v["title"],
                            "url": v["url"],
                        }
                        st.rerun()
                with c2:
                    st.link_button("🔗 跳转", v["url"])


def _render_player_with_notes():
    from progress import save_english_note, load_english_notes
    from rag_engine import save_resource_to_kb

    playing = st.session_state["eng_playing"]
    video_id = playing.get("video_id", "")
    title = playing.get("title", "")
    url = playing.get("url", "")

    st.markdown(f"### ▶️ 正在播放：{title}")

    if st.button("✖️ 关闭播放器"):
        st.session_state.pop("eng_playing", None)
        st.rerun()

    col_video, col_notes = st.columns([3, 2])
    with col_video:
        if video_id:
            embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&rel=0"
            st.markdown(
                f'<iframe width="100%" height="360" src="{embed_url}" '
                f'frameborder="0" allow="accelerometer; autoplay; clipboard-write; '
                f'encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                unsafe_allow_html=True,
            )
            st.caption("💡 点击视频 ⚙️ 设置可调整倍速 | 有暂停/全屏按钮")
        elif url:
            st.video(url)
        else:
            st.link_button("🔗 在浏览器中打开", url)
    with col_notes:
        _render_notes_panel(video_id or title, title)



def _render_notes_panel(source_key: str, source_title: str):
    from progress import save_english_note, load_english_notes
    from rag_engine import save_resource_to_kb

    st.markdown("#### 📝 学习笔记")
    note_text = st.text_area(
        "记录笔记",
        placeholder="记录生词、句型、听力要点...",
        height=180,
        key=f"eng_note_{source_key}",
        label_visibility="collapsed",
    )

    col_save, col_kb = st.columns(2)
    with col_save:
        if st.button("💾 保存", key=f"save_{source_key}", use_container_width=True):
            if note_text.strip():
                save_english_note(source_key, note_text.strip(), source_title)
                st.success("已保存")
                st.rerun()
    with col_kb:
        if st.button("📚 存入KB", key=f"kb_{source_key}", use_container_width=True):
            if note_text.strip():
                name = f"english_{source_key}"
                save_resource_to_kb(note_text.strip(), name, "english")
                st.success("已存入 kb/english/")

    notes = load_english_notes(source_key)
    if notes:
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
