import streamlit as st
from rag_engine import get_llm
from resume import (
    parse_pdf_resume, save_resume, load_resume, save_version,
    generate_optimized_resume, extract_kb_skills,
)
from resume_html import (
    render_resume_html, generate_resume_pdf_from_html,
    generate_template_from_pdf, list_templates,
)
from progress import get_progress_summary


def render():
    st.title("🍀 文档助手")
    st.caption("基于知识库技能 + 面试表现，AI 生成针对目标职位的双语简历")

    resume_data = load_resume()

    with st.container(border=True):
        st.subheader("📎 上传简历")
        uploaded_pdf = st.file_uploader("上传 PDF 简历（同时生成 HTML 模板）", type=["pdf"], key="resume_pdf")
    if uploaded_pdf:
        pdf_bytes = uploaded_pdf.read()
        with st.spinner("🍀 正在解析 PDF 内容..."):
            raw_text = parse_pdf_resume(pdf_bytes)
            save_resume(raw_text)
            st.session_state.resume_text = raw_text
        st.success(f"简历解析成功！提取了 {len(raw_text)} 个字符")

        if st.button("🎨 从此 PDF 生成 HTML 模板", help="AI 分析 PDF 样式，自动生成匹配的 HTML 模板"):
            with st.spinner("🍀 AI 正在分析 PDF 视觉风格并生成 HTML 模板..."):
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
        with st.spinner("🍀 AI 正在识别图片中的 JD 内容..."):
            from langchain_core.messages import HumanMessage
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
            with st.spinner("🍀 AI 正在分析并生成优化简历..."):
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
