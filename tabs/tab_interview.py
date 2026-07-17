import io
import streamlit as st
import streamlit.components.v1 as components
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from rag_engine import list_kb_files, get_interview_system_prompt, interview_chat, KB_DIR
from progress import record_interview, add_review_card


def tts_speak(text: str):
    clean_text = text.replace('"', '\\"').replace('\n', ' ').replace('\r', '')
    js = f"""
    <script>
    const utterance = new SpeechSynthesisUtterance("{clean_text}");
    utterance.lang = 'zh-CN';
    utterance.rate = 1.0;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
    </script>
    """
    components.html(js, height=0)


def stt_recognize(audio_bytes: bytes) -> str:
    recognizer = sr.Recognizer()
    audio_file = io.BytesIO(audio_bytes)
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data, language="zh-CN")


def render():
    st.title("🌹 AI 对练")
    st.caption("语音对话式面试模拟 — AI 面试官提问，你用语音回答")

    if "interview_active" not in st.session_state:
        st.session_state.interview_active = False
        st.session_state.interview_completed = False
        st.session_state.interview_messages = []
        st.session_state.interview_system_prompt = ""
        st.session_state.pending_answer = None

    if st.session_state.get("interview_completed"):
        st.subheader("✅ 面试结束")
        for msg in st.session_state.interview_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        st.divider()
        if st.button("🔄 重新开始面试"):
            st.session_state.interview_completed = False
            st.session_state.interview_active = False
            st.session_state.interview_messages = []
            st.session_state.pending_answer = None
            st.rerun()

    elif not st.session_state.interview_active:
        st.subheader("面试设置")
        iv_kb_files = list_kb_files()
        iv_file_options = [str(f.relative_to(KB_DIR)) for f in iv_kb_files]

        iv_selected = st.multiselect(
            "📁 选择知识范围（不选则使用全部）",
            options=iv_file_options,
            default=None,
            placeholder="点击选择文档（格式: 分类/文件名）...",
            key="iv_files",
        )
        iv_num = st.select_slider("题目数量", options=[3, 5, 8, 10], value=5)

        if st.button("🎬 开始面试", type="primary"):
            selected = iv_selected if iv_selected else None
            st.session_state.interview_system_prompt = get_interview_system_prompt(
                selected, iv_num
            )
            st.session_state.interview_messages = []
            st.session_state.interview_active = True
            st.session_state.pending_answer = None

            with st.spinner("🌹 面试官准备中..."):
                first_reply = interview_chat(
                    st.session_state.interview_system_prompt,
                    [],
                )
            st.session_state.interview_messages.append(
                {"role": "assistant", "content": first_reply}
            )
            st.rerun()
    else:
        col_end, col_tts = st.columns([1, 4])
        with col_end:
            if st.button("⏹️ 结束面试"):
                st.session_state.interview_messages.append(
                    {"role": "user", "content": "结束面试"}
                )
                with st.spinner("🌹 生成评分..."):
                    final_reply = interview_chat(
                        st.session_state.interview_system_prompt,
                        st.session_state.interview_messages,
                    )
                st.session_state.interview_messages.append(
                    {"role": "assistant", "content": final_reply}
                )
                st.session_state.interview_active = False
                st.session_state.interview_completed = True
                st.session_state.pending_answer = None
                import re
                score_match = re.search(r"总分[：:]\s*(\d+)", final_reply)
                score = int(score_match.group(1)) if score_match else 0
                iv_cats = st.session_state.get("iv_selected_cats", [])
                record_interview(score, 5, iv_cats, final_reply[-200:])
                _add_low_score_to_review(final_reply)
                st.rerun()

        for msg in st.session_state.interview_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        last_msg = st.session_state.interview_messages[-1] if st.session_state.interview_messages else None
        if last_msg and last_msg["role"] == "assistant":
            if st.button("🔊 播放面试官语音", key="tts_play"):
                tts_speak(last_msg["content"])

        st.divider()

        if st.session_state.pending_answer:
            st.markdown(f"**你的回答：** {st.session_state.pending_answer}")
            col_confirm, col_redo = st.columns(2)
            with col_confirm:
                if st.button("✅ 确认发送", type="primary"):
                    user_text = st.session_state.pending_answer
                    st.session_state.pending_answer = None
                    st.session_state.interview_messages.append(
                        {"role": "user", "content": user_text}
                    )
                    with st.spinner("🌹 面试官思考中..."):
                        ai_reply = interview_chat(
                            st.session_state.interview_system_prompt,
                            st.session_state.interview_messages,
                        )
                    st.session_state.interview_messages.append(
                        {"role": "assistant", "content": ai_reply}
                    )
                    st.rerun()
            with col_redo:
                if st.button("🔄 重新录音"):
                    st.session_state.pending_answer = None
                    st.rerun()
        else:
            st.markdown("**🎤 点击录音按钮回答（录完后可确认或重录）：**")
            audio_bytes = audio_recorder(
                text="",
                recording_color="#e74c3c",
                neutral_color="#95a5a6",
                pause_threshold=3.0,
            )

            if audio_bytes:
                with st.spinner("🌹 识别语音中..."):
                    try:
                        user_text = stt_recognize(audio_bytes)
                        st.session_state.pending_answer = user_text
                        st.rerun()
                    except sr.UnknownValueError:
                        st.warning("未能识别语音，请重新录音")
                    except sr.RequestError as e:
                        st.error(f"语音识别服务出错: {e}")
                    except Exception as e:
                        st.error(f"出错了: {e}")


def _add_low_score_to_review(final_reply: str):
    """Parse interview score table and add low-scoring questions to review."""
    import re
    rows = re.findall(
        r"\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|",
        final_reply,
    )
    added = 0
    for question, score_str, feedback in rows:
        try:
            s = int(score_str)
        except ValueError:
            continue
        if s <= 6:
            add_review_card(
                front=question.strip(),
                back=feedback.strip(),
                source="interview",
                source_ref=f"面试 {__import__('datetime').date.today().isoformat()}",
            )
            added += 1
    if added > 0:
        st.toast(f"已将 {added} 道低分题加入复习队列")
