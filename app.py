import streamlit as st
from rag_engine import KB_DIR

st.set_page_config(page_title="RAG 知识库问答", page_icon="📚", layout="wide")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

KB_DIR.mkdir(parents=True, exist_ok=True)

# 加载主题 CSS
from styles import load_theme_css
load_theme_css()

# 侧边栏
from sidebar import render_sidebar, show_file_preview
render_sidebar()

# 文档预览触发
if st.session_state.get("preview_file"):
    show_file_preview(st.session_state["preview_file"])

# Tabs
from tabs import tab_chat, tab_exam, tab_interview
from tabs import tab_resource, tab_progress, tab_resume, tab_trends, tab_study_space

tab_objs = st.tabs([
    "🌸 知识问答",
    "🌺 技术趋势",
    "📖 学习空间",
    "🌻 资源导入",
    "🌼 智能出题",
    "🌹 AI 对练",
    "🍀 文档助手",
    "📈 学习进度",
])

with tab_objs[0]:
    tab_chat.render()
with tab_objs[1]:
    tab_trends.render()
with tab_objs[2]:
    tab_study_space.render()
with tab_objs[3]:
    tab_resource.render()
with tab_objs[4]:
    tab_exam.render()
with tab_objs[5]:
    tab_interview.render()
with tab_objs[6]:
    tab_resume.render()
with tab_objs[7]:
    tab_progress.render()
