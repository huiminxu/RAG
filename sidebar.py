import streamlit as st
from pathlib import Path
from rag_engine import rebuild_index, KB_DIR
from styles import load_dialog_css


def get_kb_categories():
    categories = {}
    if not KB_DIR.exists():
        return categories
    for sub in sorted(KB_DIR.iterdir()):
        if sub.is_dir():
            files = list(sub.glob("*.md"))
            if files:
                categories[sub.name] = files
    root_files = list(KB_DIR.glob("*.md"))
    if root_files:
        categories["未分类"] = root_files
    return categories


@st.dialog("📄 文档预览", width="large")
def show_file_preview(file_path: str):
    p = Path(file_path)
    if not p.exists():
        st.error("文件不存在")
        return

    load_dialog_css()

    st.markdown(f'<div class="preview-path">📂 {p.parent.name}/{p.name}</div>', unsafe_allow_html=True)
    content = p.read_text(encoding="utf-8")

    editing = st.session_state.get("file_edit_mode", False)

    if not editing:
        highlight_text = st.session_state.get("preview_highlight", "")
        with st.container(border=True, height=450):
            if highlight_text and highlight_text in content and len(highlight_text) < len(content) * 0.5:
                before, after = content.split(highlight_text, 1)
                if before.strip():
                    st.markdown(before)
                st.markdown(
                    f'<div class="source-highlight">\n\n{highlight_text}\n\n</div>',
                    unsafe_allow_html=True,
                )
                if after.strip():
                    st.markdown(after)
            else:
                st.markdown(content)
        col_edit, col_close, _ = st.columns([1, 1, 5])
        with col_edit:
            if st.button("编辑", key="preview_edit_btn"):
                st.session_state.file_edit_mode = True
                st.rerun()
        with col_close:
            if st.button("关闭", key="preview_close_btn"):
                st.session_state.pop("preview_file", None)
                st.session_state.pop("preview_highlight", None)
                st.rerun()
    else:
        edited = st.text_area("内容", value=content, height=400, key="file_editor")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("取消", use_container_width=True):
                st.session_state.file_edit_mode = False
                st.session_state.pop("preview_file", None)
                st.rerun()
        with col2:
            if st.button("确认", type="primary", use_container_width=True):
                p.write_text(edited, encoding="utf-8")
                st.session_state.file_edit_mode = False
                st.session_state.pop("preview_file", None)
                st.success("已保存！")
                st.rerun()


def render_sidebar():
    with st.sidebar:
        _tc1, _tc2 = st.columns([4, 1])
        with _tc1:
            st.markdown("")
        with _tc2:
            _label = "☀️" if st.session_state.dark_mode else "🌙"
            if st.button(_label, key="theme_toggle", help="切换主题"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()

        st.markdown('<div class="kb-header">📂 知识库文档</div>', unsafe_allow_html=True)
        categories = get_kb_categories()
        if categories:
            total_files = sum(len(fs) for fs in categories.values())
            st.caption(f"共 {len(categories)} 个分类 · {total_files} 篇文档")
            for cat, files in categories.items():
                st.markdown(f'<div class="cat-label">📁 {cat} <span class="file-count">({len(files)} 篇)</span></div>', unsafe_allow_html=True)
                for f in files:
                    if st.button(f"📄 {f.name}", key=f"kb_{cat}_{f.name}", use_container_width=True):
                        st.session_state.preview_file = str(f)
                        st.session_state.file_edit_mode = False
                        st.rerun()
        else:
            st.info("📭 kb/ 目录下没有找到 .md 文件")

        st.markdown('<div class="manage-header">🌿 分类管理</div>', unsafe_allow_html=True)
        with st.expander("操作", expanded=False, icon="🍃"):
            col_input, col_btn = st.columns([3, 1])
            with col_input:
                new_cat = st.text_input("新分类名称", placeholder="例如: docker", key="new_cat", label_visibility="collapsed")
            with col_btn:
                add_clicked = st.button("➕ 新增", key="add_cat", use_container_width=True)
            if add_clicked and new_cat.strip():
                safe_name = new_cat.strip().replace(" ", "_")
                (KB_DIR / safe_name).mkdir(parents=True, exist_ok=True)
                st.success(f"已创建分类: {safe_name}")
                st.rerun()

            existing_cats = sorted([d.name for d in KB_DIR.iterdir() if d.is_dir()])
            if existing_cats:
                selected_cat = st.selectbox("选择已有分类", existing_cats, key="manage_cat")
                col_rename, col_del = st.columns([3, 1])
                with col_rename:
                    rename_to = st.text_input("重命名为", value=selected_cat, key="rename_cat", label_visibility="collapsed")
                with col_del:
                    if st.button("✏️ 改名", key="do_rename", use_container_width=True) and rename_to.strip() and rename_to.strip() != selected_cat:
                        safe_rename = rename_to.strip().replace(" ", "_")
                        (KB_DIR / selected_cat).rename(KB_DIR / safe_rename)
                        st.success(f"{selected_cat} → {safe_rename}")
                        st.rerun()

                if st.button("🗑️ 删除该分类", key="do_delete", type="secondary", use_container_width=True):
                    st.session_state.confirm_delete_cat = selected_cat

            if st.session_state.get("confirm_delete_cat") == (selected_cat if existing_cats else None):
                file_count = len(list((KB_DIR / selected_cat).glob("*.md")))
                st.warning(f"确认删除「{selected_cat}」？（含 {file_count} 个文件，不可恢复）")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("确认删除", key="confirm_del", type="primary"):
                        import shutil
                        shutil.rmtree(KB_DIR / selected_cat)
                        st.session_state.pop("confirm_delete_cat", None)
                        st.success(f"已删除: {selected_cat}")
                        st.rerun()
                with c2:
                    if st.button("取消", key="cancel_del"):
                        st.session_state.pop("confirm_delete_cat", None)
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌸 重建索引", use_container_width=True, type="primary"):
            with st.spinner("🌱 正在重建向量索引..."):
                rebuild_index()
            st.success("索引重建完成！")
