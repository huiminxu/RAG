import streamlit as st
from pathlib import Path
from rag_engine import KB_DIR, extract_key_concepts, generate_deep_questions, extract_concepts_structured
from progress import save_reading_note, load_reading_notes, add_review_card


def _list_kb_files() -> list[tuple[str, Path]]:
    """Return (display_key, full_path) for all KB markdown files."""
    files = []
    if not KB_DIR.exists():
        return files
    for f in sorted(KB_DIR.rglob("*.md")):
        key = str(f.relative_to(KB_DIR)).replace("\\", "/")
        files.append((key, f))
    return files


def render():
    st.title("📖 精读笔记")
    st.caption("选择知识库文档，精读全文并记录笔记，AI 辅助提炼要点")
    render_content()


def render_content():
    kb_files = _list_kb_files()
    if not kb_files:
        st.info("知识库暂无文档，请先在「资源导入」tab 添加内容")
        return

    file_keys = [k for k, _ in kb_files]
    file_map = {k: p for k, p in kb_files}

    selected_key = st.selectbox(
        "📂 选择文档",
        options=file_keys,
        format_func=lambda k: f"📄 {k}",
        key="reading_file_select",
    )

    if not selected_key:
        return

    file_path = file_map[selected_key]
    content = file_path.read_text(encoding="utf-8")

    # --- 两列：左文档 右笔记 ---
    col_doc, col_notes = st.columns([3, 2])

    with col_doc:
        st.markdown("#### 📃 文档内容")
        with st.container(border=True, height=450):
            st.markdown(content)

    with col_notes:
        st.markdown("#### 📝 我的笔记")
        note_text = st.text_area(
            "写笔记",
            placeholder="记录阅读心得、要点、疑问...",
            height=200,
            key="reading_note_input",
            label_visibility="collapsed",
        )
        if st.button("💾 保存笔记", use_container_width=True):
            if note_text.strip():
                save_reading_note(selected_key, note_text.strip())
                st.success("笔记已保存")
                st.rerun()
            else:
                st.warning("请先写点内容")

        # 历史笔记
        notes = load_reading_notes(selected_key)
        if notes:
            with st.expander(f"📋 历史笔记（{len(notes)} 条）", expanded=False):
                for i, n in enumerate(reversed(notes[-10:])):
                    st.caption(n['date'][:10])
                    st.markdown(n["content"])
                    if st.button("📥 加入复习", key=f"note_to_review_{i}"):
                        front = n["content"][:50].replace("\n", " ")
                        if len(n["content"]) > 50:
                            front += "..."
                        add_review_card(
                            front=f"回忆笔记要点：{front}",
                            back=n["content"],
                            source="reading",
                            source_ref=selected_key,
                        )
                        st.rerun()
                    st.divider()

    # --- AI 辅助 ---
    st.divider()
    st.markdown("#### 🤖 AI 辅助精读")
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("🧠 提炼核心概念", use_container_width=True):
            with st.spinner("AI 正在分析文档..."):
                result = extract_key_concepts(content)
                st.session_state.reading_concepts = result
                structured = extract_concepts_structured(content)
                st.session_state.reading_concepts_structured = structured

    with col_btn2:
        if st.button("❓ 生成思考题", use_container_width=True):
            all_notes = "\n".join(n["content"] for n in notes) if notes else ""
            with st.spinner("AI 正在生成问题..."):
                result = generate_deep_questions(content, all_notes)
                st.session_state.reading_questions = result

    if "reading_concepts" in st.session_state:
        with st.expander("🧠 核心概念", expanded=True):
            st.markdown(st.session_state.reading_concepts)

        structured = st.session_state.get("reading_concepts_structured", [])
        if structured:
            count = len(structured)
            if st.button(f"📥 加入复习卡片（{count} 个概念）", key="add_to_review"):
                for concept in structured:
                    add_review_card(
                        front=concept.get("name", "未知概念"),
                        back=concept.get("explanation", ""),
                        source="reading",
                        source_ref=selected_key,
                    )
                st.session_state.pop("reading_concepts_structured", None)
                st.rerun()

    if "reading_questions" in st.session_state:
        with st.expander("❓ 思考题", expanded=True):
            st.markdown(st.session_state.reading_questions)
