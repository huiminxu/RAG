import os
import streamlit as st
from pathlib import Path
from rag_engine import (
    detect_url_type, fetch_resource, organize_content,
    save_resource_to_kb, transcribe_video, analyze_transcript, KB_DIR,
)
from progress import record_resource


def render():
    st.title("🌻 资源导入知识库")
    st.caption("支持 URL 抓取、音视频上传、手动编写，整理后保存到知识库")

    mode = st.radio("导入方式", ["🔗 URL 导入", "📁 文件上传", "✏️ 手动编写"], horizontal=True)

    if mode == "🔗 URL 导入":
        _render_url_import()
    elif mode == "📁 文件上传":
        _render_file_import()
    else:
        _render_manual_write()


def _render_url_import():
    with st.container(border=True):
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
                           "2. 切换到「📁 文件上传」模式上传文件\n"
                           "3. 系统会自动转录并整理内容")
            elif url_type == "bilibili":
                st.warning("⚠️ B站视频暂不支持直接抓取字幕。\n\n"
                           "**建议操作：**\n"
                           "1. 下载视频到本地（可用浏览器插件）\n"
                           "2. 切换到「📁 文件上传」模式上传文件")

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
        progress = st.progress(0, text="🌻 正在抓取内容...")

        try:
            result = fetch_resource(resource_url)
            progress.progress(30, text=f"抓取完成: {result['title'][:40]}...")

            with st.expander("📄 原始内容预览"):
                st.text(result["content"][:2000] + ("..." if len(result["content"]) > 2000 else ""))

            progress.progress(50, text="🌻 AI 正在整理内容...")
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
            if st.button("✅ 确认保存到知识库", type="primary", key="url_save"):
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
            if st.button("🗑️ 放弃", key="url_discard"):
                del st.session_state.resource_organized
                del st.session_state.resource_title
                del st.session_state.resource_category
                st.rerun()


def _render_file_import():
    with st.container(border=True):
        uploaded_file = st.file_uploader(
            "上传音视频文件",
            type=["mp4", "m4a", "mp3", "wav"],
            help="支持 MP4 视频、MP3/M4A/WAV 音频，5-30 分钟",
        )

        import_categories = [d.name for d in KB_DIR.iterdir() if d.is_dir()]
        import_category = st.selectbox(
            "📂 保存到分类",
            options=import_categories if import_categories else ["未分类"],
            index=0,
            key="import_category",
        )

        doc_name = st.text_input(
            "文档名称（可选，默认使用文件名）",
            placeholder="例如: listening_day1",
            key="import_doc_name",
        )

        auto_analyze = st.checkbox("🧠 转录后自动分析（整理重点 + 薄弱点建议）", value=True)

    if uploaded_file and st.button("🚀 开始转录", type="primary"):
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        name = doc_name.strip() if doc_name.strip() else uploaded_file.name.rsplit(".", 1)[0]
        progress = st.progress(0, text="🌷 正在提取音频并转录...")

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
            with st.spinner("🌷 AI 正在分析内容..."):
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
                target_dir = KB_DIR / st.session_state.import_category
                target_dir.mkdir(exist_ok=True)
                safe_name = st.session_state.import_name.replace(" ", "_")
                output_path = target_dir / f"{safe_name}.md"
                output_path.write_text(st.session_state.import_transcript, encoding="utf-8")
                from git_sync import auto_commit
                auto_commit([str(output_path.relative_to(KB_DIR.parent))])
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


def _render_manual_write():
    with st.container(border=True):
        manual_categories = [d.name for d in KB_DIR.iterdir() if d.is_dir()]
        manual_category = st.selectbox(
            "📂 保存到分类",
            options=manual_categories if manual_categories else ["未分类"],
            index=0,
            key="manual_category",
        )

        manual_name = st.text_input(
            "📄 文档名称",
            placeholder="例如: python_notes",
            key="manual_doc_name",
        )

        manual_content = st.text_area(
            "✏️ 内容（支持 Markdown）",
            height=300,
            placeholder="在这里编写你的笔记内容...",
            key="manual_content",
        )

    if st.session_state.get("manual_saved"):
        st.success(st.session_state.manual_saved)
        st.info('请点击侧边栏的「重建索引」按钮更新检索数据库')
        st.session_state.pop("manual_saved", None)

    if st.button("💾 保存到知识库", type="primary"):
        if not manual_name.strip() or not manual_content.strip():
            st.warning("请填写文档名称和内容后保存")
        else:
            target_dir = KB_DIR / manual_category
            target_dir.mkdir(exist_ok=True)
            safe_name = manual_name.strip().replace(" ", "_")
            if not safe_name.endswith(".md"):
                safe_name += ".md"
            output_path = target_dir / safe_name
            output_path.write_text(manual_content, encoding="utf-8")
            from git_sync import auto_commit
            auto_commit([str(output_path.relative_to(KB_DIR.parent))])
            record_resource(safe_name, manual_category, "manual")
            st.session_state.manual_saved = f"已保存: `{manual_category}/{safe_name}`"
            st.session_state["manual_doc_name"] = ""
            st.session_state["manual_content"] = ""
            st.rerun()
