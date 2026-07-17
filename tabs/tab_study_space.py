import streamlit as st
from tabs import tab_reading, tab_studyroom
from progress import (
    load_todos, save_todo, toggle_todo, delete_todo,
    get_due_cards, review_card, get_review_stats,
)


def render():
    st.title("📖 学习空间")
    st.caption("精读、复习、计划、自习 — 集中一处高效学习")

    sub_tabs = st.tabs(["📹 自习室", "📖 精读笔记", "🧠 复习卡片", "✅ 学习计划"])

    with sub_tabs[0]:
        tab_studyroom.render_content()

    with sub_tabs[1]:
        tab_reading.render_content()

    with sub_tabs[2]:
        _render_review()

    with sub_tabs[3]:
        _render_todo()


def _render_review():
    """Spaced repetition review cards."""
    review_stats = get_review_stats()
    due_cards = get_due_cards()

    st.caption(f"总卡片 {review_stats['total_cards']} · 待复习 {review_stats['due_today']} · 已掌握 {review_stats['mastered']}")

    if review_stats["total_cards"] == 0:
        st.info('暂无复习卡片。在「精读笔记」中提炼核心概念后点击「加入复习卡片」，或完成面试后低分题会自动加入。')
        return

    if not due_cards:
        st.success("今日复习已完成！")
        return

    if "review_index" not in st.session_state:
        st.session_state.review_index = 0
    if "review_flipped" not in st.session_state:
        st.session_state.review_flipped = False

    idx = st.session_state.review_index
    total = len(due_cards)

    if idx >= total:
        st.success("今日复习全部完成！明天继续加油")
        if st.button("🔄 重新开始", key="review_restart"):
            st.session_state.review_index = 0
            st.session_state.review_flipped = False
            st.rerun()
        return

    card = due_cards[idx]
    source_label = "精读" if card["source"] == "reading" else "面试"

    st.caption(f"第 {idx + 1}/{total} 张 · 来自{source_label}")

    with st.container(border=True):
        if not st.session_state.review_flipped:
            st.markdown(f"### {card['front']}")
            st.caption(f"来源：{card.get('source_ref', '未知')}")
            if st.button("👀 翻转查看答案", use_container_width=True, key="flip_card"):
                st.session_state.review_flipped = True
                st.rerun()
        else:
            st.markdown(f"**Q：** {card['front']}")
            st.divider()
            st.markdown(card['back'])

    if st.session_state.review_flipped:
        col_forgot, col_fuzzy, col_remember = st.columns(3)
        with col_forgot:
            if st.button("😰 忘了", use_container_width=True, key="review_forgot"):
                review_card(card["id"], "forgot")
                st.session_state.review_index += 1
                st.session_state.review_flipped = False
                st.rerun()
        with col_fuzzy:
            if st.button("🤔 模糊", use_container_width=True, key="review_fuzzy"):
                review_card(card["id"], "fuzzy")
                st.session_state.review_index += 1
                st.session_state.review_flipped = False
                st.rerun()
        with col_remember:
            if st.button("✅ 记住", use_container_width=True, type="primary", key="review_remember"):
                review_card(card["id"], "remembered")
                st.session_state.review_index += 1
                st.session_state.review_flipped = False
                st.rerun()


def _render_todo():
    """Learning plan / todo list."""
    todos = load_todos()

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        new_todo = st.text_input(
            "添加计划",
            placeholder="输入学习计划...",
            key="new_todo_input",
            label_visibility="collapsed",
        )
    with col_btn:
        if st.button("➕", key="add_todo", use_container_width=True):
            if new_todo.strip():
                save_todo(new_todo.strip())
                st.rerun()

    if not todos:
        st.caption("暂无计划，添加一个开始吧")
    else:
        done_count = sum(1 for t in todos if t["done"])
        st.caption(f"完成 {done_count}/{len(todos)}")

        for t in todos:
            col_check, col_text, col_del = st.columns([1, 8, 1])
            with col_check:
                checked = st.checkbox("done", value=t["done"], key=f"todo_{t['id']}", label_visibility="collapsed")
                if checked != t["done"]:
                    toggle_todo(t["id"])
                    st.rerun()
            with col_text:
                if t["done"]:
                    st.markdown(f"~~{t['title']}~~")
                else:
                    st.markdown(t["title"])
            with col_del:
                if st.button("🗑️", key=f"del_{t['id']}"):
                    delete_todo(t["id"])
                    st.rerun()
