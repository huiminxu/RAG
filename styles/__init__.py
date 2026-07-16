import streamlit as st
from pathlib import Path


def load_theme_css():
    """加载主题 CSS，根据 dark_mode 状态选择浅色或深色主题"""
    base = Path(__file__).parent
    dark_mode = st.session_state.get("dark_mode", False)

    if dark_mode:
        css = (base / "dark.css").read_text(encoding="utf-8")
    else:
        css = (base / "light.css").read_text(encoding="utf-8")

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_dialog_css():
    """加载文档预览对话框 CSS"""
    base = Path(__file__).parent
    dark_mode = st.session_state.get("dark_mode", False)

    if dark_mode:
        css = (base / "dialog.css").read_text(encoding="utf-8")
    else:
        css = (base / "dialog_light.css").read_text(encoding="utf-8")

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
