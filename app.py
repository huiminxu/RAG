import io
import os
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from rag_engine import (
    query, rebuild_index, generate_exam, list_kb_files, list_kb_by_category,
    get_interview_system_prompt, interview_chat, transcribe_video,
    analyze_transcript, fetch_resource, organize_content, save_resource_to_kb,
    detect_url_type, generate_learning_report, KB_DIR,
)
from progress import record_interview, record_resource, record_query, get_stats, get_progress_summary
from resume import (parse_pdf_resume, save_resume, load_resume, save_version,
                    generate_optimized_resume, extract_kb_skills)
from resume_html import (render_resume_html, generate_resume_pdf_from_html,
                         generate_template_from_pdf, list_templates)
from trends import get_all_trends

st.set_page_config(page_title="RAG 知识库问答", page_icon="📚", layout="wide")

KB_DIR.mkdir(parents=True, exist_ok=True)

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


with st.sidebar:
    st.header("📂 知识库文档")
    categories = get_kb_categories()
    if categories:
        for cat, files in categories.items():
            st.markdown(f"**{cat}/** ({len(files)} 篇)")
            for f in files:
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;`{f.name}`")
    else:
        st.warning("kb/ 目录下没有找到 .md 文件")

    st.divider()
    if st.button("🔄 重建索引"):
        with st.spinner("正在重建向量索引..."):
            rebuild_index()
        st.success("索引重建完成！")

tab_chat, tab_exam, tab_interview, tab_import, tab_resource, tab_progress, tab_resume, tab_trends = st.tabs(["💬 知识库问答", "📝 面试卷生成", "🎙️ 模拟面试", "📥 音视频导入", "📚 资源导入", "📈 学习进度", "📄 简历优化", "🔥 技术趋势"])

with tab_chat:
    st.title("📚 RAG 知识库问答系统")
    st.caption("基于本地文档 + Claude 的检索增强生成问答")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("输入你的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("检索中..."):
                try:
                    result = query(prompt)
                    answer = result["answer"]
                    sources = result["sources"]

                    st.markdown(answer)

                    if sources:
                        with st.expander("📎 参考来源"):
                            for src in sources:
                                st.markdown(f"**{src['source']}** (相似度: {1 - src['score']:.2f})")
                                st.markdown(f"> {src['content'][:200]}...")
                                st.divider()

                except Exception as e:
                    answer = f"出错了: {str(e)}"
                    st.error(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

with tab_exam:
    st.title("📝 面试卷生成")
    st.caption("基于知识库内容自动生成面试题")

    kb_files = list_kb_files()
    file_options = [str(f.relative_to(KB_DIR)) for f in kb_files]

    selected = st.multiselect(
        "📁 选择知识范围（不选则使用全部文档）",
        options=file_options,
        default=None,
        placeholder="点击选择文档（格式: 分类/文件名）...",
    )
    selected_files = selected if selected else None

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗣️ 问答题（10 道）")
        st.markdown("适合面试官口头提问，覆盖知识库核心知识点")
        if st.button("生成问答题", key="gen_qa"):
            with st.spinner("正在生成问答题..."):
                try:
                    result = generate_exam("qa", selected_files)
                    st.session_state.qa_result = result
                except Exception as e:
                    st.error(f"生成失败: {str(e)}")

        if "qa_result" in st.session_state:
            st.markdown(st.session_state.qa_result)
            st.download_button(
                "⬇️ 下载问答题",
                st.session_state.qa_result,
                file_name="interview_qa.md",
                mime="text/markdown",
            )

    with col2:
        st.subheader("✍️ 笔试题（5 道）")
        st.markdown("包含代码题和概念题，适合书面考试")
        if st.button("生成笔试题", key="gen_code"):
            with st.spinner("正在生成笔试题..."):
                try:
                    result = generate_exam("code", selected_files)
                    st.session_state.code_result = result
                except Exception as e:
                    st.error(f"生成失败: {str(e)}")

        if "code_result" in st.session_state:
            st.markdown(st.session_state.code_result)
            st.download_button(
                "⬇️ 下载笔试题",
                st.session_state.code_result,
                file_name="interview_code.md",
                mime="text/markdown",
            )


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


with tab_interview:
    st.title("🎙️ 模拟面试")
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

            with st.spinner("面试官准备中..."):
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
                with st.spinner("生成评分..."):
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
                    with st.spinner("面试官思考中..."):
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
                with st.spinner("识别语音中..."):
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

with tab_import:
    st.title("📥 视频导入知识库")
    st.caption("上传听力练习视频（MP4），自动转录为文字并加入知识库")

    uploaded_file = st.file_uploader(
        "上传 MP4 视频文件",
        type=["mp4", "m4a", "mp3", "wav"],
        help="支持 MP4 视频、MP3/M4A/WAV 音频，5-30 分钟",
    )

    import_categories = [d.name for d in KB_DIR.iterdir() if d.is_dir()]
    import_category = st.selectbox(
        "📂 保存到分类",
        options=import_categories if import_categories else ["未分类"],
        index=0,
    )

    doc_name = st.text_input(
        "文档名称（可选，默认使用文件名）",
        placeholder="例如: listening_day1",
    )

    auto_analyze = st.checkbox("🧠 转录后自动分析（整理重点 + 薄弱点建议）", value=True)

    if uploaded_file and st.button("🚀 开始转录", type="primary"):
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        name = doc_name.strip() if doc_name.strip() else uploaded_file.name.rsplit(".", 1)[0]
        progress = st.progress(0, text="正在提取音频并转录...")

        try:
            output_path = transcribe_video(tmp_path, name, import_category)
            progress.progress(60, text="转录完成！")

            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()

            os.unlink(output_path)

            st.session_state.import_transcript = content
            st.session_state.import_name = name
            st.session_state.import_category = import_category
            st.session_state.import_analyze = auto_analyze
            progress.progress(100, text="转录完成，请预览确认")
        except Exception as e:
            st.error(f"转录失败: {e}")
        finally:
            os.unlink(tmp_path)

    if "import_transcript" in st.session_state:
        st.divider()
        st.subheader("📄 转录结果预览")
        st.markdown(st.session_state.import_transcript)

        if st.session_state.get("import_analyze") and "import_analysis" not in st.session_state:
            with st.spinner("AI 正在分析内容..."):
                analysis = analyze_transcript(
                    st.session_state.import_transcript,
                    st.session_state.import_category,
                )
            st.session_state.import_analysis = analysis

        if "import_analysis" in st.session_state:
            st.divider()
            st.subheader("🧠 智能分析")
            st.markdown(st.session_state.import_analysis)

        st.divider()
        col_save, col_discard = st.columns(2)
        with col_save:
            if st.button("✅ 确认保存到知识库", key="import_save", type="primary"):
                from rag_engine import KB_DIR as kb_dir
                target_dir = kb_dir / st.session_state.import_category
                target_dir.mkdir(exist_ok=True)
                safe_name = st.session_state.import_name.replace(" ", "_")
                output_path = target_dir / f"{safe_name}.md"
                output_path.write_text(st.session_state.import_transcript, encoding="utf-8")
                record_resource(safe_name, st.session_state.import_category, "audio_video")
                st.success(f"已保存: `{st.session_state.import_category}/{safe_name}.md`")
                st.info('请点击侧边栏的「重建索引」按钮更新检索数据库')
                for key in ["import_transcript", "import_name", "import_category", "import_analyze", "import_analysis"]:
                    st.session_state.pop(key, None)
        with col_discard:
            if st.button("🗑️ 放弃", key="import_discard"):
                for key in ["import_transcript", "import_name", "import_category", "import_analyze", "import_analysis"]:
                    st.session_state.pop(key, None)
                st.rerun()

with tab_resource:
    st.title("📚 资源导入知识库")
    st.caption("粘贴 URL，自动抓取内容并用 AI 整理为结构化笔记")

    resource_url = st.text_input(
        "🔗 资源 URL",
        placeholder="粘贴 YouTube / TED / 网页文章链接...",
    )

    if resource_url:
        url_type = detect_url_type(resource_url)
        type_labels = {
            "youtube": "🎬 YouTube 视频",
            "ted": "🎤 TED 演讲",
            "github": "🐙 GitHub",
            "yuque": "📗 语雀文档",
            "bilibili": "📺 B站视频",
            "cloud_drive": "☁️ 网盘资源",
            "article": "📄 网页文章",
        }
        st.info(f"识别为: **{type_labels.get(url_type, '未知')}**")
        if url_type == "cloud_drive":
            st.warning("⚠️ 网盘资源需要登录才能访问，无法直接抓取。\n\n"
                       "**建议操作：**\n"
                       "1. 在网盘中下载视频到本地\n"
                       "2. 切换到「📥 音视频导入」tab 上传文件\n"
                       "3. 系统会自动转录并整理内容")
        elif url_type == "bilibili":
            st.warning("⚠️ B站视频暂不支持直接抓取字幕。\n\n"
                       "**建议操作：**\n"
                       "1. 下载视频到本地（可用浏览器插件）\n"
                       "2. 切换到「📥 音视频导入」tab 上传文件")

    res_categories = [d.name for d in KB_DIR.iterdir() if d.is_dir()]
    res_category = st.selectbox(
        "📂 保存到分类",
        options=res_categories if res_categories else ["未分类"],
        index=0,
        key="res_category",
    )

    res_doc_name = st.text_input(
        "文档名称（可选，默认使用资源标题）",
        placeholder="例如: ted_how_to_speak",
        key="res_doc_name",
    )

    if resource_url and st.button("🚀 抓取并整理", type="primary"):
        progress = st.progress(0, text="正在抓取内容...")

        try:
            result = fetch_resource(resource_url)
            progress.progress(30, text=f"抓取完成: {result['title'][:40]}...")

            with st.expander("📄 原始内容预览"):
                st.text(result["content"][:2000] + ("..." if len(result["content"]) > 2000 else ""))

            progress.progress(50, text="AI 正在整理内容...")
            organized = organize_content(
                result["content"], result["title"], result["type"], resource_url, res_category
            )
            progress.progress(90, text="整理完成！")

            st.session_state.resource_organized = organized
            st.session_state.resource_title = result["title"]
            st.session_state.resource_category = res_category
            progress.progress(100, text="完成！请预览后确认保存")

        except Exception as e:
            st.error(f"抓取失败: {e}")

    if "resource_organized" in st.session_state:
        st.divider()
        st.subheader("📝 整理结果预览")
        st.markdown(st.session_state.resource_organized)

        st.divider()
        col_save, col_discard = st.columns(2)
        with col_save:
            if st.button("✅ 确认保存到知识库", type="primary"):
                name = res_doc_name.strip() if res_doc_name.strip() else st.session_state.resource_title
                category = st.session_state.resource_category
                output_path = save_resource_to_kb(
                    st.session_state.resource_organized, name, category
                )
                record_resource(name, category, "url", resource_url)
                st.success(f"已保存: `{category}/{Path(output_path).name}`")
                st.info('请点击侧边栏的「重建索引」按钮更新检索数据库')
                del st.session_state.resource_organized
                del st.session_state.resource_title
                del st.session_state.resource_category
        with col_discard:
            if st.button("🗑️ 放弃"):
                del st.session_state.resource_organized
                del st.session_state.resource_title
                del st.session_state.resource_category
                st.rerun()

with tab_progress:
    st.title("📈 学习进度")
    st.caption("追踪学习数据，AI 生成个性化学习报告")

    stats = get_stats()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("模拟面试", f"{stats['total_interviews']} 次")
    with col2:
        st.metric("平均分", f"{stats['avg_score']}" if stats['avg_score'] else "暂无")
    with col3:
        st.metric("学习资源", f"{stats['total_resources']} 篇")
    with col4:
        st.metric("学习天数", f"{stats['total_study_days']} 天")

    if stats["recent_scores"]:
        st.subheader("📊 面试评分趋势")
        import pandas as pd
        score_df = pd.DataFrame({
            "次数": list(range(1, len(stats["recent_scores"]) + 1)),
            "分数": stats["recent_scores"],
        })
        st.line_chart(score_df, x="次数", y="分数")

    if stats["category_distribution"]:
        st.subheader("📂 分类学习分布")
        cat_df = pd.DataFrame(
            list(stats["category_distribution"].items()),
            columns=["分类", "数量"],
        )
        st.bar_chart(cat_df, x="分类", y="数量")

    st.divider()

    if st.button("🧠 生成 AI 学习报告", type="primary"):
        if stats["total_interviews"] == 0 and stats["total_resources"] == 0:
            st.warning("暂无学习数据，请先进行面试或导入资源后再生成报告")
        else:
            with st.spinner("AI 正在分析你的学习数据..."):
                summary = get_progress_summary()
                report = generate_learning_report(summary)
            st.markdown(report)

with tab_resume:
    st.title("📄 简历优化")
    st.caption("基于知识库技能 + 面试表现，AI 生成针对目标职位的双语简历")

    resume_data = load_resume()

    st.subheader("📎 上传简历")
    uploaded_pdf = st.file_uploader("上传 PDF 简历（同时生成 HTML 模板）", type=["pdf"], key="resume_pdf")
    if uploaded_pdf:
        pdf_bytes = uploaded_pdf.read()
        with st.spinner("正在解析 PDF 内容..."):
            raw_text = parse_pdf_resume(pdf_bytes)
            save_resume(raw_text)
            st.session_state.resume_text = raw_text
        st.success(f"简历解析成功！提取了 {len(raw_text)} 个字符")

        if st.button("🎨 从此 PDF 生成 HTML 模板", help="AI 分析 PDF 样式，自动生成匹配的 HTML 模板"):
            with st.spinner("AI 正在分析 PDF 视觉风格并生成 HTML 模板..."):
                try:
                    theme_name = generate_template_from_pdf(pdf_bytes, "custom")
                    if theme_name:
                        st.success(f"模板生成成功！已保存为 '{theme_name}' 主题")
                        st.session_state.resume_theme = theme_name
                    else:
                        st.error("模板生成失败，AI 未返回有效 HTML")
                except Exception as e:
                    st.error(f"模板生成出错: {e}")

        with st.expander("📄 解析内容预览"):
            st.text(raw_text[:1500] + ("..." if len(raw_text) > 1500 else ""))
    elif resume_data.get("raw_text"):
        st.session_state.resume_text = resume_data["raw_text"]
        st.info(f"已加载之前上传的简历（{resume_data.get('uploaded_at', '未知时间')}）")

    # Template theme selector
    available_themes = list_templates()
    if len(available_themes) > 1:
        selected_theme = st.selectbox(
            "选择简历模板风格",
            available_themes,
            index=available_themes.index(st.session_state.get("resume_theme", "default"))
                  if st.session_state.get("resume_theme", "default") in available_themes else 0,
        )
        st.session_state.resume_theme = selected_theme

    st.divider()
    st.subheader("🎯 目标职位信息")

    company_info = st.text_area(
        "公司简介",
        placeholder="输入目标公司的基本信息、业务方向、技术栈等...",
        height=100,
        key="resume_company",
    )

    job_description = st.text_area(
        "职位描述（JD）",
        placeholder="粘贴目标岗位的职位描述，或上传截图后由 AI 识别...",
        height=200,
        key="resume_jd",
    )

    jd_image = st.file_uploader("或上传 JD 截图（图片）", type=["png", "jpg", "jpeg"], key="jd_image")
    if jd_image:
        import base64
        st.image(jd_image, caption="JD 截图预览", use_container_width=True)
        img_bytes = jd_image.read()
        img_b64 = base64.b64encode(img_bytes).decode()
        mime = f"image/{jd_image.type.split('/')[-1]}" if "/" in (jd_image.type or "") else f"image/{jd_image.name.split('.')[-1]}"
        with st.spinner("AI 正在识别图片中的 JD 内容..."):
            from langchain_core.messages import HumanMessage
            from rag_engine import get_llm
            llm = get_llm(max_tokens=2048)
            msg = HumanMessage(content=[
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img_b64}"}},
                {"type": "text", "text": "请提取这张图片中的职位描述（JD）内容，原样输出文本，保留格式。如果有职位名称、要求、职责等信息请完整提取。"},
            ])
            resp = llm.invoke([msg])
            st.session_state.jd_from_image = resp.content
        st.success("图片识别完成！")
        st.markdown(st.session_state.jd_from_image)

    if st.button("🚀 生成优化简历", type="primary"):
        jd_text = job_description.strip() or st.session_state.get("jd_from_image", "")
        if not st.session_state.get("resume_text"):
            st.error("请先上传 PDF 简历")
        elif not company_info.strip() or not jd_text:
            st.error("请填写公司简介和职位描述")
        else:
            with st.spinner("AI 正在分析并生成优化简历..."):
                kb_skills = extract_kb_skills()
                progress_summary = get_progress_summary()
                result = generate_optimized_resume(
                    resume_text=st.session_state.resume_text,
                    company_info=company_info,
                    job_description=jd_text,
                    kb_skills=kb_skills,
                    interview_data=progress_summary,
                )
            st.session_state.resume_result = result
            save_version(company_info[:50], jd_text[:50], result["zh"], result["en"], result["suggestions"])

    if st.session_state.get("resume_result"):
        result = st.session_state.resume_result
        st.divider()

        if result.get("suggestions"):
            st.subheader("💡 改进建议")
            st.markdown(result["suggestions"])

        st.subheader("📝 简历预览")
        tab_html, tab_zh, tab_en = st.tabs(["🖨️ HTML 排版预览", "🇨🇳 中文 Markdown", "🇺🇸 English Markdown"])

        with tab_html:
            structured = result.get("structured")
            if structured:
                theme = st.session_state.get("resume_theme", "default")
                html_str = render_resume_html(structured, theme=theme)
                st.components.v1.html(html_str, height=1100, scrolling=True)
                st.caption("提示：点击上方预览区域，按 Ctrl+P 可打印为 PDF（选择「另存为 PDF」）")

                col_html, col_pdf = st.columns(2)
                with col_html:
                    st.download_button(
                        "⬇️ 下载 HTML 文件",
                        data=html_str,
                        file_name="resume.html",
                        mime="text/html",
                    )
                with col_pdf:
                    pdf_bytes = generate_resume_pdf_from_html(structured, theme=theme)
                    if pdf_bytes:
                        st.download_button(
                            "⬇️ 下载 PDF",
                            data=pdf_bytes,
                            file_name="resume.pdf",
                            mime="application/pdf",
                        )
                    else:
                        st.info("安装 weasyprint 可直接下载 PDF")
            else:
                st.warning("AI 未生成结构化数据，无法渲染 HTML 简历")
                st.markdown(result["zh"])

        with tab_zh:
            st.markdown(result["zh"])
            st.download_button(
                "⬇️ 下载 Markdown（中文）",
                data=result["zh"],
                file_name="resume_zh.md",
                mime="text/markdown",
            )

        with tab_en:
            st.markdown(result["en"])
            st.download_button(
                "⬇️ 下载 Markdown（英文）",
                data=result["en"],
                file_name="resume_en.md",
                mime="text/markdown",
            )

    if resume_data.get("versions"):
        st.divider()
        st.subheader("📋 历史版本")
        for i, ver in enumerate(reversed(resume_data["versions"][-5:])):
            with st.expander(f"版本 {len(resume_data['versions'])-i} | {ver.get('company', '')} | {ver.get('date', '')[:10]}"):
                st.markdown(f"**目标公司:** {ver.get('company', '')}")
                st.markdown(f"**目标职位:** {ver.get('position', '')}")
                if ver.get("suggestions"):
                    st.markdown(f"**改进建议:** {ver['suggestions'][:200]}")

with tab_trends:
    st.title("🔥 技术趋势")
    st.caption("聚合 GitHub / Hacker News / Dev.to / B站 热门资源，快速了解技术前沿")

    col_lang, col_custom, col_since, col_refresh = st.columns([2, 2, 2, 1])
    with col_lang:
        trend_language = st.selectbox(
            "语言/领域",
            ["", "JavaScript", "TypeScript", "Python", "Vue", "React", "Go", "Rust", "AI", "Agent", "LLM", "大模型", "英语", "__custom__"],
            format_func=lambda x: {"": "全部", "__custom__": "🔍 自定义..."}.get(x, x),
            key="trend_lang",
        )
    with col_custom:
        if trend_language == "__custom__":
            custom_kw = st.text_input("关键词", placeholder="Docker、微服务、GPT...", key="trend_custom")
        else:
            custom_kw = ""
            st.text_input("关键词", placeholder="选择「自定义」后输入", disabled=True, key="trend_custom_disabled")
    with col_since:
        trend_since = st.selectbox(
            "时间范围",
            ["daily", "weekly", "monthly"],
            index=1,
            format_func=lambda x: {"daily": "今天", "weekly": "本周", "monthly": "本月"}[x],
            key="trend_since",
        )
    with col_refresh:
        st.write("")
        st.write("")
        refresh = st.button("🔄 刷新", key="trend_refresh")

    trend_keyword = custom_kw.strip() if trend_language == "__custom__" else trend_language
    if trend_language == "__custom__" and not trend_keyword:
        st.info("请输入关键词后查看结果")
        st.stop()

    @st.cache_data(ttl=3600, show_spinner=False)
    def _cached_trends(language, since):
        return get_all_trends(language=language, since=since, limit=10)

    if refresh:
        _cached_trends.clear()

    if st.button("📡 加载趋势数据", type="primary", key="trend_load") or st.session_state.get("trends_loaded"):
        st.session_state.trends_loaded = True
        with st.spinner("正在获取最新技术趋势..."):
            trends = _cached_trends(trend_keyword, trend_since)

        st.subheader("⭐ GitHub 热门项目")
        if trends["github"]:
            for repo in trends["github"]:
                topics_str = " ".join(f"`{t}`" for t in repo["topics"]) if repo["topics"] else ""
                st.markdown(
                    f"**[{repo['name']}]({repo['url']})** — {repo['description'][:80]}\n\n"
                    f"⭐ {repo['stars']:,} | 🍴 {repo['forks']:,} | 🏷️ {repo['language']} {topics_str}"
                )
                st.divider()
        else:
            st.info("暂无数据（GitHub API 有速率限制，稍后重试）")

        st.subheader("📰 Hacker News 热门讨论")
        if trends["hackernews"]:
            for item in trends["hackernews"]:
                st.markdown(
                    f"**[{item['title']}]({item['url']})** — "
                    f"🔥 {item['score']} | 💬 {item['comments']} 评论 | {item['time']}"
                )
        else:
            st.info("暂无数据")

        st.subheader("📝 Dev.to 热门文章")
        if trends["devto"]:
            for article in trends["devto"]:
                tags_str = " ".join(f"`{t}`" for t in article["tags"][:4]) if article["tags"] else ""
                st.markdown(
                    f"**[{article['title']}]({article['url']})**\n\n"
                    f"❤️ {article['reactions']} | 💬 {article['comments']} | {tags_str} | {article['published_at']}"
                )
                st.divider()
        else:
            st.info("暂无数据")

        st.subheader("📺 B站技术视频")
        if trends["bilibili"]:
            for video in trends["bilibili"]:
                col_thumb, col_info = st.columns([1, 3])
                with col_thumb:
                    if video.get("thumbnail"):
                        st.image(video["thumbnail"], width=160)
                with col_info:
                    play_str = f"▶️ {video['play']:,}" if isinstance(video.get("play"), int) else f"▶️ {video.get('play', 0)}"
                    st.markdown(
                        f"**[{video['title']}]({video['url']})**\n\n"
                        f"👤 {video['author']} | {play_str} | 💬 {video.get('danmaku', 0)} | ⏱️ {video.get('duration', '')} | {video['published']}"
                    )
                st.divider()
        else:
            st.info("暂无 B站 数据")
