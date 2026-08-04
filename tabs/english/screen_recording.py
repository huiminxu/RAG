"""录制练习 — 摄像头 + 麦克风录制，MP4 下载"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import date, timedelta


def render_content():
    from progress import load_english_recordings, save_english_recording
    from components.screen_recorder import recorder_html

    recordings = load_english_recordings()
    week_start = date.today() - timedelta(days=date.today().weekday())
    week_seconds = sum(
        r.get("duration_seconds", 0) for r in recordings
        if r.get("date", "")[:10] >= week_start.isoformat()
    )
    week_minutes = week_seconds / 60
    st.progress(min(week_minutes / 15, 1.0), text=f"本周：{week_minutes:.0f} / 15 分钟")

    components.html(recorder_html(), height=480, scrolling=False)

    col1, col2 = st.columns([1, 2])
    with col1:
        mins = st.number_input("录制时长(分钟)", min_value=1, value=5, step=1, key="eng_rec_mins")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 保存本次录制"):
            save_english_recording(mins * 60, "英语练习")
            st.success(f"已记录 {mins} 分钟")
            st.rerun()
