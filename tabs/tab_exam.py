import streamlit as st
from rag_engine import generate_exam, list_kb_files, KB_DIR


def render():
    st.title("🌼 智能出题")
    st.caption("基于知识库内容自动生成面试题")

    with st.container(border=True):
        kb_files = list_kb_files()
        file_options = [str(f.relative_to(KB_DIR)) for f in kb_files]

        selected = st.multiselect(
            "📁 选择知识范围（不选则使用全部文档）",
            options=file_options,
            default=None,
            placeholder="点击选择文档（格式: 分类/文件名）...",
        )
        selected_files = selected if selected else None

    qa_tab, code_tab = st.tabs(["🗣️ 问答题（10 道）", "✍️ 笔试题（5 道）"])

    with qa_tab:
        st.caption("适合面试官口头提问，覆盖知识库核心知识点")
        if st.button("生成问答题", key="gen_qa", use_container_width=True):
            with st.spinner("🌼 正在生成问答题..."):
                try:
                    result = generate_exam("qa", selected_files)
                    st.session_state.qa_result = result
                except Exception as e:
                    st.error(f"生成失败: {str(e)}")

        if "qa_result" in st.session_state:
            st.divider()
            st.markdown(st.session_state.qa_result)
            st.download_button(
                "⬇️ 下载问答题",
                st.session_state.qa_result,
                file_name="interview_qa.md",
                mime="text/markdown",
            )

    with code_tab:
        st.caption("包含代码题和概念题，适合书面考试")
        if st.button("生成笔试题", key="gen_code", use_container_width=True):
            with st.spinner("🌼 正在生成笔试题..."):
                try:
                    result = generate_exam("code", selected_files)
                    st.session_state.code_result = result
                except Exception as e:
                    st.error(f"生成失败: {str(e)}")

        if "code_result" in st.session_state:
            st.divider()
            st.markdown(st.session_state.code_result)
            st.download_button(
                "⬇️ 下载笔试题",
                st.session_state.code_result,
                file_name="interview_code.md",
                mime="text/markdown",
            )
