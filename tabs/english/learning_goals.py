"""学习目标 — 时长统计 + 分类目标 + 计时器"""

import streamlit as st
from datetime import datetime, date, timedelta


CATEGORIES = {
    "ai_research": "🤖 AI 研究",
    "projects": "💻 项目开发",
    "presentations": "🎤 演讲表达",
    "daily_life": "🌍 日常生活",
}


def render_content():
    from progress import (
        load_english_sessions, save_english_session,
        load_english_notes, load_english_materials, load_english_recordings,
    )

    week_start = date.today() - timedelta(days=date.today().weekday())
    sessions = load_english_sessions()
    week_sessions = [s for s in sessions if s.get("date", "") >= week_start.isoformat()]

    week_minutes = 0
    cat_minutes = {k: 0 for k in CATEGORIES}
    for s in week_sessions:
        try:
            start = datetime.fromisoformat(s["start"])
            end = datetime.fromisoformat(s["end"])
            mins = (end - start).total_seconds() / 60
            week_minutes += mins
            cat = s.get("category", "")
            if cat in cat_minutes:
                cat_minutes[cat] += mins
        except (ValueError, KeyError):
            pass

    st.markdown("#### 📊 本周英语学习概况")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("⏱️ 学习时长", f"{week_minutes:.0f} 分钟")
    with col2:
        materials = load_english_materials()
        completed = len([m for m in materials if m.get("completed")])
        st.metric("📚 已完成素材", f"{completed} 个")
    with col3:
        all_notes = load_english_notes("")
        st.metric("📝 笔记", f"{all_notes} 条")
    with col4:
        recordings = load_english_recordings()
        week_recs = [r for r in recordings if r.get("date", "")[:10] >= week_start.isoformat()]
        st.metric("🎙️ 录屏", f"{len(week_recs)} 次")

    st.markdown("---")
    st.markdown("#### 🎯 分类目标")

    for key, label in CATEGORIES.items():
        mins = cat_minutes.get(key, 0)
        target = 120
        col_label, col_bar = st.columns([1, 3])
        with col_label:
            st.markdown(f"**{label}**")
        with col_bar:
            st.progress(min(mins / target, 1.0), text=f"{mins:.0f} / {target} 分钟/周")

    st.markdown("---")
    st.markdown("#### ⏱️ 学习计时器")

    col_cat, col_desc = st.columns([1, 2])
    with col_cat:
        category = st.selectbox("学习分类", list(CATEGORIES.keys()), format_func=lambda k: CATEGORIES[k], key="eng_timer_cat")
    with col_desc:
        description = st.text_input("学习内容", placeholder="如：Watching TED talk on AI", key="eng_timer_desc")

    if "eng_timer_start" not in st.session_state:
        st.session_state.eng_timer_start = None

    col_start, col_stop = st.columns(2)
    with col_start:
        if st.button("▶️ 开始计时", use_container_width=True, disabled=st.session_state.eng_timer_start is not None):
            st.session_state.eng_timer_start = datetime.now().isoformat()
            st.session_state.eng_timer_cat = category
            st.session_state.eng_timer_desc = description
            st.rerun()
    with col_stop:
        if st.button("⏹️ 停止并记录", use_container_width=True, disabled=st.session_state.eng_timer_start is None):
            start_time = st.session_state.eng_timer_start
            save_english_session(
                st.session_state.eng_timer_cat,
                "study",
                start_time,
                st.session_state.get("eng_timer_desc", ""),
            )
            st.session_state.eng_timer_start = None
            st.success("学习记录已保存")
            st.rerun()

    if st.session_state.eng_timer_start:
        start = datetime.fromisoformat(st.session_state.eng_timer_start)
        elapsed = (datetime.now() - start).total_seconds() / 60
        st.info(f"⏱️ 正在计时：{elapsed:.1f} 分钟 | 分类：{CATEGORIES.get(st.session_state.eng_timer_cat, '')} | {st.session_state.get('eng_timer_desc', '')}")

    if sessions:
        st.markdown("---")
        st.markdown("#### 📜 最近学习记录")
        for s in reversed(sessions[-10:]):
            try:
                start = datetime.fromisoformat(s["start"])
                end = datetime.fromisoformat(s["end"])
                mins = (end - start).total_seconds() / 60
                cat_label = CATEGORIES.get(s.get("category", ""), s.get("category", ""))
                st.markdown(f"- `{s['date']}` {cat_label} — {s.get('description', '')} ({mins:.0f} 分钟)")
            except (ValueError, KeyError):
                pass
