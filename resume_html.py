"""Resume HTML rendering — structured data → styled HTML → optional PDF."""
import os
import base64
import json
from pathlib import Path
from jinja2 import Template
from dotenv import load_dotenv

load_dotenv()

TEMPLATES_DIR = Path(__file__).parent / "templates"


def render_resume_html(data: dict, theme: str = "default") -> str:
    """Render structured resume data to a full HTML page."""
    template_path = TEMPLATES_DIR / f"resume_{theme}.html"
    if not template_path.exists():
        template_path = TEMPLATES_DIR / "resume_default.html"

    template_str = template_path.read_text(encoding="utf-8")
    template = Template(template_str)

    context = {
        "name": data.get("name", ""),
        "title": data.get("title", "个人简历"),
        "info": data.get("info", {}),
        "education": data.get("education", []),
        "skills": data.get("skills", []),
        "experience": data.get("experience", []),
        "projects": _normalize_projects(data.get("projects", [])),
    }

    return template.render(**context)


def _normalize_projects(projects: list) -> list:
    """Ensure each project's desc is a list."""
    normalized = []
    for p in projects:
        proj = dict(p)
        if isinstance(proj.get("desc"), str):
            proj["desc"] = [proj["desc"]]
        elif not isinstance(proj.get("desc"), list):
            proj["desc"] = []
        normalized.append(proj)
    return normalized


def generate_resume_pdf_from_html(data: dict, theme: str = "default") -> bytes | None:
    """Generate PDF using WeasyPrint. Returns None if WeasyPrint unavailable."""
    try:
        from weasyprint import HTML
    except ImportError:
        return None

    html_str = render_resume_html(data, theme)
    return HTML(string=html_str).write_pdf()


TEMPLATE_GEN_PROMPT = """你是一名前端开发专家。请根据这张简历截图，生成一个完整的 HTML+CSS 模板文件。

要求：
1. 必须是完整的 HTML 文件（包含 <!DOCTYPE html>、<head>、<style>、<body>）
2. CSS 全部内嵌在 <style> 标签内（不要外部文件）
3. 使用 Jinja2 模板语法占位，变量如下：
   - {{ name }} — 姓名
   - {{ title }} — 目标职位
   - {{ info.phone }} / {{ info.email }} / {{ info.age }} / {{ info.location }} / {{ info.ethnicity }} / {{ info.english_level }}
   - {% for edu in education %} {{ edu.period }} / {{ edu.school }} / {{ edu.major }} / {{ edu.degree }} {% endfor %}
   - {% for skill in skills %} {{ skill }} {% endfor %}
   - {% for exp in experience %} {{ exp.company }} / {{ exp.role }} / {{ exp.period }} / {{ exp.desc }} {% endfor %}
   - {% for proj in projects %} {{ proj.name }} / {{ proj.role }} / {{ proj.tech }} / {% for d in proj.desc %} {{ d }} {% endfor %} {% endfor %}
4. 尽可能还原截图中的：
   - 整体布局（单栏/双栏/顶部标题栏）
   - 配色方案（背景色、标题色、文字色）
   - 字体大小层级
   - 区块间距和分隔方式
5. 使用 A4 纸尺寸（210mm x 297mm），适合打印
6. 字体栈使用：font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
7. 加上 @media print 规则确保打印效果一致
8. 加上 @page { size: A4; margin: 0; } 和 print-color-adjust: exact;

只输出完整的 HTML 代码，不要任何解释文字。"""


def generate_template_from_pdf(pdf_bytes: bytes, template_name: str = "custom") -> str | None:
    """Upload PDF → render page 1 as PNG → Claude Vision → generate HTML template."""
    import fitz

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    png_bytes = pix.tobytes("png")
    doc.close()

    img_b64 = base64.b64encode(png_bytes).decode()

    from langchain_core.messages import HumanMessage
    from rag_engine import get_llm

    llm = get_llm(max_tokens=8192)

    msg = HumanMessage(content=[
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
        {"type": "text", "text": TEMPLATE_GEN_PROMPT},
    ])

    response = llm.invoke([msg])
    html_content = response.content

    # Extract HTML if wrapped in code block
    if "```html" in html_content:
        import re
        match = re.search(r'```html\s*(.+?)```', html_content, re.DOTALL)
        if match:
            html_content = match.group(1).strip()
    elif "```" in html_content:
        import re
        match = re.search(r'```\s*(.+?)```', html_content, re.DOTALL)
        if match:
            html_content = match.group(1).strip()

    if not html_content.strip().startswith("<!DOCTYPE") and not html_content.strip().startswith("<html"):
        return None

    # Save template
    save_path = TEMPLATES_DIR / f"resume_{template_name}.html"
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    save_path.write_text(html_content, encoding="utf-8")

    return template_name


def list_templates() -> list[str]:
    """List available template themes."""
    if not TEMPLATES_DIR.exists():
        return ["default"]
    templates = []
    for f in TEMPLATES_DIR.glob("resume_*.html"):
        name = f.stem.replace("resume_", "")
        templates.append(name)
    return sorted(templates) if templates else ["default"]
