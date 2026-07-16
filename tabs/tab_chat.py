import streamlit as st
from rag_engine import query, KB_DIR


def render():
    st.title("🌸 RAG 知识库问答系统")
    st.caption("基于本地文档 + Claude 的检索增强生成问答")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if len(st.session_state.messages) > 100:
        st.session_state.messages = st.session_state.messages[-100:]

    chat_container = st.container(height=480)
    with chat_container:
        if not st.session_state.messages:
            with st.chat_message("assistant", avatar="🌿"):
                st.markdown("你好呀 🌿 我是你的知识库助手，有什么问题尽管问我～")
        for idx, msg in enumerate(st.session_state.messages):
            avatar = "🌷" if msg["role"] == "user" else "🌿"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])
                if msg.get("sources") and "非知识库内容" not in msg["content"]:
                    with st.expander("📎 参考来源"):
                        for i, src in enumerate(msg["sources"]):
                            if st.button(f"📄 {src['source']}  ({1 - src['score']:.0%})", key=f"hist_{idx}_{i}"):
                                st.session_state.preview_file = src.get("path", "")
                                st.session_state.preview_highlight = src.get("content", "")
                                st.session_state.file_edit_mode = False
                                st.rerun()

    if prompt := st.chat_input("输入你的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user", avatar="🌷"):
                st.markdown(prompt)
            with st.chat_message("assistant", avatar="🌿"):
                with st.spinner("🌸 检索中..."):
                    try:
                        result = query(prompt, chat_history=st.session_state.messages[:-1])
                        answer = result["answer"]
                        sources = result["sources"]
                        st.markdown(answer)
                        if sources and "非知识库内容" not in answer:
                            with st.expander("📎 参考来源"):
                                for i, src in enumerate(sources):
                                    if st.button(f"📄 {src['source']}  ({1 - src['score']:.0%})", key=f"src_{i}_{src['source']}"):
                                        st.session_state.preview_file = src.get("path", "")
                                        st.session_state.preview_highlight = src.get("content", "")
                                        st.session_state.file_edit_mode = False
                                        st.rerun()
                    except Exception as e:
                        answer = f"出错了: {str(e)}"
                        sources = []
                        st.error(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
        st.rerun()
