import json
import os
import re
from datetime import datetime
from pathlib import Path

from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
KB_DIR = BASE_DIR / "kb"
RESUME_FILE = BASE_DIR / "resume_data.json"


def extract_kb_skills() -> str:
    skills = set()
    if KB_DIR.exists():
        for md_file in KB_DIR.rglob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            for line in text.split("\n"):
                line_s = line.strip()
                if line_s.startswith("# ") or line_s.startswith("## "):
                    heading = line_s.lstrip("#").strip()
                    if heading and len(heading) < 50:
                        skills.add(heading)
                elif line_s.startswith("- ") or line_s.startswith("* "):
                    item = line_s.lstrip("-* ").strip()
                    if 2 < len(item) < 30 and not item.startswith("http"):
                        skills.add(item)
    return "、".join(sorted(skills)[:50]) if skills else ""


def parse_pdf_resume(file_bytes: bytes) -> str:
    from PyPDF2 import PdfReader
    import io

    reader = PdfReader(io.BytesIO(file_bytes))
    text_parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_parts.append(text)
    return "\n\n".join(text_parts)


def save_resume(raw_text: str):
    data = load_resume()
    data["raw_text"] = raw_text
    data["uploaded_at"] = datetime.now().isoformat()
    RESUME_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_resume() -> dict:
    if RESUME_FILE.exists():
        return json.loads(RESUME_FILE.read_text(encoding="utf-8"))
    return {"raw_text": "", "uploaded_at": "", "versions": []}


def save_version(company: str, position: str, zh: str, en: str, suggestions: str):
    data = load_resume()
    data.setdefault("versions", []).append({
        "date": datetime.now().isoformat(),
        "company": company,
        "position": position,
        "zh": zh,
        "en": en,
        "suggestions": suggestions,
    })
    RESUME_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


RESUME_PROMPT = """你是一位专业的简历优化顾问。基于以下信息，生成一份针对目标职位优化的双语简历。

## 候选人现有简历
{resume_text}

## 目标公司
{company_info}

## 职位描述
{job_description}

## 候选人技能（来自知识库）
{kb_skills}

## 面试表现记录
{interview_data}

## 输出要求
1. 生成中文简历和英文简历
2. 针对 JD 关键词优化措辞
3. 突出与职位匹配的技能和经验
4. 融入面试中展现的优势
5. 用 STAR 法则描述项目经验
6. 格式专业简洁，适合 ATS 系统解析

请严格按以下格式输出（用分隔符分开）：
---CHINESE---
（完整中文简历，Markdown 格式）
---ENGLISH---
（完整英文简历，Markdown 格式）
---SUGGESTIONS---
请从以下 5 个维度给出针对性建议（每个维度 2-3 条具体可操作的建议）：

### 1. 职位匹配建议
分析候选人与目标职位的匹配度，指出需要补充或强调的方向

### 2. 面试准备建议
基于 JD 要求，给出面试中可能被问到的重点问题和准备方向

### 3. 技术提升建议
当前技术栈与目标职位的差距，推荐学习的技术/工具/框架

### 4. 项目经验包装建议
如何更好地描述现有项目经验以匹配目标职位需求

### 5. 软技能与亮点建议
沟通、协作、领导力等软技能方面的展示策略

---STRUCTURED---
请额外输出一份结构化 JSON（用于生成 PDF），严格按以下格式：
```json
{{
  "name": "姓名",
  "title": "目标职位名称",
  "info": {{
    "phone": "电话",
    "email": "邮箱",
    "age": "年龄",
    "location": "所在城市",
    "ethnicity": "民族",
    "english_level": "英语水平"
  }},
  "education": [
    {{"period": "2014.09-2018.06", "school": "学校名", "major": "专业", "degree": "学位"}}
  ],
  "skills": ["技能1", "技能2", "技能3"],
  "experience": [
    {{"company": "公司名", "role": "职位", "period": "2020.01-2024.04", "desc": "工作描述"}}
  ],
  "projects": [
    {{"name": "项目名", "role": "角色", "tech": "技术栈", "desc": ["描述1", "描述2"]}}
  ]
}}
```
注意：JSON 必须是合法的，所有字段都用中文填写（英文简历用英文填写）。"""


def generate_optimized_resume(
    resume_text: str,
    company_info: str,
    job_description: str,
    kb_skills: str = "",
    interview_data: str = "",
) -> dict:
    prompt = RESUME_PROMPT.format(
        resume_text=resume_text,
        company_info=company_info,
        job_description=job_description,
        kb_skills=kb_skills or "（暂无）",
        interview_data=interview_data or "（暂无面试记录）",
    )

    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=8192,
    )
    response = llm.invoke(prompt)
    content = response.content

    zh = ""
    en = ""
    suggestions = ""
    structured = None

    if "---STRUCTURED---" in content:
        main_part, struct_part = content.split("---STRUCTURED---", 1)
    else:
        main_part = content
        struct_part = ""

    if "---CHINESE---" in main_part and "---ENGLISH---" in main_part:
        parts = main_part.split("---ENGLISH---")
        zh = parts[0].replace("---CHINESE---", "").strip()
        rest = parts[1]
        if "---SUGGESTIONS---" in rest:
            en_parts = rest.split("---SUGGESTIONS---")
            en = en_parts[0].strip()
            suggestions = en_parts[1].strip()
        else:
            en = rest.strip()
    else:
        zh = main_part
        en = ""
        suggestions = ""

    if struct_part.strip():
        try:
            json_match = re.search(r'```json\s*(\{.+\})\s*```', struct_part, re.DOTALL)
            if json_match:
                structured = json.loads(json_match.group(1))
            else:
                brace_start = struct_part.find('{')
                brace_end = struct_part.rfind('}')
                if brace_start != -1 and brace_end > brace_start:
                    structured = json.loads(struct_part[brace_start:brace_end+1])
        except (json.JSONDecodeError, AttributeError, ValueError):
            structured = None

    if not structured and zh:
        structured = _extract_structured_from_markdown(zh)

    return {"zh": zh, "en": en, "suggestions": suggestions, "structured": structured}


STRUCTURED_PROMPT = """请将以下简历内容提取为严格的 JSON 格式（不要输出任何其他文字，只输出 JSON）：

{resume_md}

输出格式：
```json
{{
  "name": "姓名",
  "title": "职位",
  "info": {{"phone": "电话", "email": "邮箱", "age": "年龄", "location": "城市", "ethnicity": "民族", "english_level": "英语水平"}},
  "education": [{{"period": "起止时间", "school": "学校", "major": "专业", "degree": "学位"}}],
  "skills": ["技能1", "技能2"],
  "experience": [{{"company": "公司", "role": "职位", "period": "起止时间", "desc": "职责描述"}}],
  "projects": [{{"name": "项目名", "role": "角色", "tech": "技术栈", "desc": ["描述1", "描述2"]}}]
}}
```"""


def _extract_structured_from_markdown(md_content: str) -> dict | None:
    prompt = STRUCTURED_PROMPT.format(resume_md=md_content[:3000])
    try:
        llm = ChatAnthropic(
            model="claude-sonnet-4-6",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            max_tokens=2048,
        )
        resp = llm.invoke(prompt)
        content = resp.content
        json_match = re.search(r'```json\s*(\{.+\})\s*```', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        brace_start = content.find('{')
        brace_end = content.rfind('}')
        if brace_start != -1 and brace_end > brace_start:
            return json.loads(content[brace_start:brace_end+1])
    except Exception:
        pass
    return None


TEMPLATE_CONFIG_FILE = BASE_DIR / "resume" / "template_config.json"


def analyze_template(pdf_bytes: bytes) -> list[dict]:
    """Extract all text spans from a PDF template with position/style info."""
    import fitz

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    all_spans = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if not text:
                        continue
                    bbox = span["bbox"]
                    color = span.get("color", 0)
                    if isinstance(color, int):
                        r = ((color >> 16) & 0xFF) / 255.0
                        g = ((color >> 8) & 0xFF) / 255.0
                        b = (color & 0xFF) / 255.0
                    else:
                        r, g, b = 0, 0, 0
                    all_spans.append({
                        "page": page_num,
                        "text": text,
                        "bbox": [round(bbox[0], 1), round(bbox[1], 1),
                                 round(bbox[2], 1), round(bbox[3], 1)],
                        "size": round(span.get("size", 10), 1),
                        "color": [round(r, 3), round(g, 3), round(b, 3)],
                        "font": span.get("font", ""),
                    })

    doc.close()
    return all_spans


CLASSIFY_PROMPT = """你是简历模板分析器。以下是从 PDF 模板中提取的所有文本及其位置。
请将每个文本分类为对应的简历字段。

## 文本列表（格式：[x, y, x2, y2] size=字号 "文本内容"）
{spans_text}

## 分类规则
将每个 span 分为以下类别之一：
- `name` — 姓名（通常字号最大）
- `info.ethnicity` — 民族相关
- `info.age` — 年龄相关
- `info.phone` — 电话号码
- `info.email` — 邮箱地址
- `info.location` — 所在地
- `info.english_level` — 英语水平
- `education[N].period` — 第N段教育的时间（N从0开始）
- `education[N].school` — 学校名
- `education[N].major` — 专业
- `education[N].degree` — 学位
- `skills` — 技能（可能多个span组成一段）
- `experience[N].company` — 第N段工作的公司名
- `experience[N].role` — 职位
- `experience[N].period` — 工作时间
- `projects[N].name` — 第N个项目名称
- `projects[N].role` — 项目角色
- `projects[N].tech` — 技术栈
- `projects[N].desc` — 项目描述（可能有多行）
- `section_header` — 区块标题（如"教育背景"、"工作经历"等，不替换）
- `static` — 固定文本（如页脚"感谢您的阅读"等，不替换）
- `label` — 字段标签（如"民"、"年"、"电"等前缀文字，不替换）

## 输出格式
输出严格的 JSON 数组，每个元素对应一个 span（顺序与输入一致）：
```json
[
  {{"index": 0, "field": "name"}},
  {{"index": 1, "field": "label"}},
  {{"index": 2, "field": "info.ethnicity"}},
  ...
]
```

只输出 JSON，不要其他文字。"""


def classify_template_fields(spans: list[dict]) -> dict:
    """Use Claude AI to classify each text span into a resume field."""
    spans_text = "\n".join(
        f"[{i}] [{s['bbox'][0]}, {s['bbox'][1]}, {s['bbox'][2]}, {s['bbox'][3]}] "
        f"size={s['size']} \"{s['text'][:60]}\""
        for i, s in enumerate(spans)
    )

    prompt = CLASSIFY_PROMPT.format(spans_text=spans_text)

    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=4096,
    )
    response = llm.invoke(prompt)
    content = response.content

    json_match = re.search(r'\[.+\]', content, re.DOTALL)
    if not json_match:
        return {}

    try:
        classifications = json.loads(json_match.group(0))
    except json.JSONDecodeError:
        return {}

    return _build_template_config(spans, classifications)


def _build_template_config(spans: list[dict], classifications: list[dict]) -> dict:
    """Build template_config from spans + AI classifications."""
    field_spans = {}
    for item in classifications:
        idx = item.get("index", -1)
        field = item.get("field", "")
        if idx < 0 or idx >= len(spans) or not field:
            continue
        if field in ("section_header", "static", "label"):
            continue
        field_spans.setdefault(field, []).append(spans[idx])

    fonts_used = set()
    for s in spans:
        if s.get("font"):
            fonts_used.add(s["font"])

    font_map = _build_font_map(fonts_used)

    fields = {}

    simple_fields = [k for k in field_spans if "[" not in k and k != "skills"]
    for key in simple_fields:
        span_list = field_spans[key]
        bbox = _union_bbox([s["bbox"] for s in span_list])
        first = span_list[0]
        prefix = ""
        if "." in key:
            raw_text = " ".join(s["text"] for s in span_list)
            if "：" in raw_text:
                parts = raw_text.split("：", 1)
                if len(parts[0]) <= 4:
                    prefix = parts[0] + "："

        fields[key] = {
            "bbox": [bbox[0] - 2, bbox[1] - 2, bbox[2] + 50, bbox[3] + 2],
            "font_size": first["size"],
            "color": first["color"],
            "insert_pos": [round(bbox[0], 1), round(bbox[3], 1)],
        }
        if prefix:
            fields[key]["prefix"] = prefix

    if "skills" in field_spans:
        skill_spans = field_spans["skills"]
        bbox = _union_bbox([s["bbox"] for s in skill_spans])
        fields["skills"] = {
            "type": "skills",
            "bbox_cover": [bbox[0] - 5, bbox[1] - 3, bbox[2] + 5, bbox[3] + 3],
            "start_pos": [round(bbox[0], 1), round(bbox[1] + 13, 1)],
            "font_size": skill_spans[0]["size"],
            "color": skill_spans[0]["color"],
            "line_height": 17,
        }

    repeat_groups = {}
    for key in field_spans:
        match = re.match(r'(\w+)\[(\d+)\]\.(\w+)', key)
        if match:
            group_name = match.group(1)
            idx = int(match.group(2))
            sub_field = match.group(3)
            repeat_groups.setdefault(group_name, {}).setdefault(idx, {})[sub_field] = field_spans[key]

    for group_name, items in repeat_groups.items():
        if not items:
            continue
        sorted_indices = sorted(items.keys())
        all_bboxes = []
        for idx in sorted_indices:
            for sub_field, span_list in items[idx].items():
                for s in span_list:
                    all_bboxes.append(s["bbox"])

        cover_bbox = _union_bbox(all_bboxes)

        first_idx = sorted_indices[0]
        first_items = items[first_idx]
        first_y_values = []
        for sf, slist in first_items.items():
            for s in slist:
                first_y_values.append(s["bbox"][3])
        start_y = round(min(first_y_values), 1) if first_y_values else cover_bbox[1] + 20

        step_y = 18
        if len(sorted_indices) >= 2:
            y0_list = []
            y1_list = []
            for sf, slist in items[sorted_indices[0]].items():
                for s in slist:
                    y0_list.append(s["bbox"][1])
            for sf, slist in items[sorted_indices[1]].items():
                for s in slist:
                    y1_list.append(s["bbox"][1])
            if y0_list and y1_list:
                step_y = round(min(y1_list) - min(y0_list), 1)

        columns = []
        for sub_field in sorted(first_items.keys()):
            slist = first_items[sub_field]
            first_span = slist[0]
            columns.append({
                "field": sub_field,
                "x": round(first_span["bbox"][0], 1),
                "font_size": first_span["size"],
            })
        columns.sort(key=lambda c: c["x"])

        if group_name == "projects":
            fields[group_name] = {
                "type": "freeform",
                "bbox_cover": [cover_bbox[0] - 5, cover_bbox[1] - 5,
                               cover_bbox[2] + 5, min(cover_bbox[3] + 50, 810)],
                "start_y": start_y,
                "font_size": columns[0]["font_size"] if columns else 10,
                "color": list(items[first_idx][list(first_items.keys())[0]][0]["color"]),
                "layout": _detect_project_layout(items),
            }
        else:
            fields[group_name] = {
                "type": "repeat",
                "bbox_cover": [cover_bbox[0] - 5, cover_bbox[1] - 5,
                               cover_bbox[2] + 5, cover_bbox[3] + 5],
                "start_y": start_y,
                "step_y": step_y,
                "columns": columns,
                "color": list(items[first_idx][list(first_items.keys())[0]][0]["color"]),
            }

    return {
        "fields": fields,
        "font_map": font_map,
    }


def _detect_project_layout(items: dict) -> dict:
    """Detect internal layout of project blocks from template spans."""
    if not items or 0 not in items:
        return {"name_x": 44, "role_x": 460, "tech_x": 102, "desc_x": 102,
                "name_size": 10, "tech_size": 8, "desc_size": 9,
                "line_step": 15, "block_gap": 8}

    first = items[0]
    layout = {
        "name_x": 44, "role_x": 460, "tech_x": 102, "desc_x": 102,
        "name_size": 10, "tech_size": 8, "desc_size": 9,
        "line_step": 15, "block_gap": 8
    }

    if "name" in first:
        layout["name_x"] = round(first["name"][0]["bbox"][0], 1)
        layout["name_size"] = first["name"][0]["size"]
    if "role" in first:
        layout["role_x"] = round(first["role"][0]["bbox"][0], 1)
    if "tech" in first:
        layout["tech_x"] = round(first["tech"][0]["bbox"][0], 1)
        layout["tech_size"] = first["tech"][0]["size"]
    if "desc" in first:
        layout["desc_x"] = round(first["desc"][0]["bbox"][0], 1)
        layout["desc_size"] = first["desc"][0]["size"]
        if len(first["desc"]) >= 2:
            layout["line_step"] = round(
                first["desc"][1]["bbox"][1] - first["desc"][0]["bbox"][1], 1)

    return layout


def _union_bbox(bboxes: list) -> list:
    """Compute union bounding box."""
    x0 = min(b[0] for b in bboxes)
    y0 = min(b[1] for b in bboxes)
    x1 = max(b[2] for b in bboxes)
    y1 = max(b[3] for b in bboxes)
    return [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)]


def _build_font_map(fonts: set) -> dict:
    """Map PDF font names to system font files."""
    font_map = {}
    msyh = Path("C:/Windows/Fonts/msyh.ttc")
    noto = BASE_DIR / "fonts" / "NotoSansSC-Regular.ttf"

    for font_name in fonts:
        clean = re.sub(r'^[A-Z]{6}\+', '', font_name)
        if "PingFang" in clean or "pingfang" in clean.lower():
            if msyh.exists():
                font_map[font_name] = str(msyh)
            elif noto.exists():
                font_map[font_name] = str(noto)
        elif "Song" in clean or "song" in clean.lower():
            simsun = Path("C:/Windows/Fonts/simsun.ttc")
            if simsun.exists():
                font_map[font_name] = str(simsun)
            elif msyh.exists():
                font_map[font_name] = str(msyh)
        elif "HYQiHei" in clean or "Hei" in clean:
            if msyh.exists():
                font_map[font_name] = str(msyh)
        else:
            if msyh.exists():
                font_map[font_name] = str(msyh)
            elif noto.exists():
                font_map[font_name] = str(noto)
    return font_map


def _get_system_font() -> tuple[str | None, str]:
    """Return (font_file_path, font_ref_name) for the best available system font."""
    msyh = Path("C:/Windows/Fonts/msyh.ttc")
    noto = BASE_DIR / "fonts" / "NotoSansSC-Regular.ttf"
    if msyh.exists():
        return str(msyh), "MSYaHei"
    elif noto.exists():
        return str(noto), "NotoSans"
    return None, "china-ss"


def load_template_config() -> dict | None:
    """Load saved template configuration."""
    if TEMPLATE_CONFIG_FILE.exists():
        try:
            return json.loads(TEMPLATE_CONFIG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return None


def save_template_config(config: dict):
    """Save template configuration to JSON."""
    TEMPLATE_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    TEMPLATE_CONFIG_FILE.write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")


def analyze_and_save_template_config(pdf_bytes: bytes, template_filename: str = ""):
    """Full pipeline: extract spans → AI classify → save config."""
    spans = analyze_template(pdf_bytes)
    if not spans:
        return None

    # Only classify page 1 spans (template uses page 1 only)
    page1_spans = [s for s in spans if s["page"] == 0]
    if not page1_spans:
        page1_spans = spans

    config = classify_template_fields(page1_spans)
    if not config or not config.get("fields"):
        return None

    template_dir = BASE_DIR / "resume"
    if template_filename:
        config["template_file"] = str(template_dir / template_filename)
    else:
        templates = list(template_dir.glob("*.pdf"))
        templates = [t for t in templates if "test_output" not in t.name]
        if templates:
            config["template_file"] = str(templates[0])

    save_template_config(config)
    return config


def generate_resume_pdf(content, language: str = "zh") -> bytes:
    if isinstance(content, dict) and content.get("structured"):
        return _generate_template_pdf(content["structured"], language)
    elif isinstance(content, dict):
        markdown = content.get("zh" if language == "zh" else "en", "")
        return _generate_simple_pdf(markdown, language)
    else:
        return _generate_simple_pdf(content, language)


def _generate_template_pdf(data: dict, language: str = "zh") -> bytes:
    """Generate PDF using dynamic template config. Falls back to simple PDF if no config."""
    import fitz

    config = load_template_config()
    if not config or not config.get("fields"):
        return _generate_simple_pdf(json.dumps(data, ensure_ascii=False), language)

    template_path = config.get("template_file", "")
    if not template_path or not Path(template_path).exists():
        template_dir = BASE_DIR / "resume"
        templates = list(template_dir.glob("*.pdf"))
        templates = [t for t in templates if "test_output" not in t.name]
        if not templates:
            return _generate_simple_pdf(json.dumps(data, ensure_ascii=False), language)
        template_path = str(templates[0])

    doc = fitz.open(template_path)
    while doc.page_count > 1:
        doc.delete_page(1)
    page = doc[0]

    font_file, font_ref = _get_system_font()

    def cover(rect):
        shape = page.new_shape()
        shape.draw_rect(rect)
        shape.finish(color=None, fill=(1, 1, 1))
        shape.commit()

    def put(pos, text, size=10, color=(0.12, 0.12, 0.12)):
        if not text:
            return
        if font_file:
            page.insert_text(pos, str(text), fontsize=size, color=color,
                           fontname=font_ref, fontfile=font_file)
        else:
            page.insert_text(pos, str(text), fontsize=size, color=color,
                           fontname=font_ref)

    fields = config["fields"]

    for field_key, cfg in fields.items():
        field_type = cfg.get("type", "single")

        if field_type == "repeat":
            _render_repeat(cover, put, cfg, data, field_key)
        elif field_type == "freeform":
            _render_freeform(cover, put, cfg, data, field_key)
        elif field_type == "skills":
            _render_skills(cover, put, cfg, data)
        else:
            _render_single(cover, put, cfg, data, field_key)

    try:
        doc.subset_fonts()
    except Exception:
        pass
    pdf_bytes = doc.tobytes(garbage=4, deflate=True)
    doc.close()
    return pdf_bytes


def _render_single(cover, put, cfg: dict, data: dict, field_key: str):
    """Render a single-value field (name, info.phone, etc.)."""
    import fitz

    keys = field_key.split(".")
    value = data
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, "")
        else:
            value = ""
            break

    if not value:
        return

    bbox = cfg["bbox"]
    cover(fitz.Rect(*bbox))

    prefix = cfg.get("prefix", "")
    text = f"{prefix}{value}" if prefix else str(value)
    pos = tuple(cfg["insert_pos"])
    size = cfg.get("font_size", 10)
    color = tuple(cfg.get("color", [0.12, 0.12, 0.12]))

    put(pos, text, size=size, color=color)


def _render_repeat(cover, put, cfg: dict, data: dict, field_key: str):
    """Render a repeating section (experience, education)."""
    import fitz

    items = data.get(field_key, [])
    if not items:
        return

    bbox_cover = cfg["bbox_cover"]
    cover(fitz.Rect(*bbox_cover))

    start_y = cfg["start_y"]
    step_y = cfg.get("step_y", 18)
    columns = cfg.get("columns", [])
    color = tuple(cfg.get("color", [0.12, 0.12, 0.12]))

    for i, item in enumerate(items):
        y = start_y + i * step_y
        for col in columns:
            sub_field = col["field"]
            x = col["x"]
            size = col.get("font_size", 10)
            val = item.get(sub_field, "")
            if val:
                put((x, y), str(val), size=size, color=color)


def _render_skills(cover, put, cfg: dict, data: dict):
    """Render skills section."""
    import fitz

    skills = data.get("skills", [])
    if not skills:
        return

    bbox_cover = cfg["bbox_cover"]
    cover(fitz.Rect(*bbox_cover))

    start_pos = cfg["start_pos"]
    size = cfg.get("font_size", 10)
    color = tuple(cfg.get("color", [0.12, 0.12, 0.12]))
    line_height = cfg.get("line_height", 17)

    lines = []
    current = ""
    for s in skills:
        addition = f" | {s}" if current else s
        if len(current + addition) > 80:
            lines.append(current)
            current = s
        else:
            current += addition
    if current:
        lines.append(current)

    y = start_pos[1]
    for line in lines:
        put((start_pos[0], y), line, size=size, color=color)
        y += line_height


def _render_freeform(cover, put, cfg: dict, data: dict, field_key: str):
    """Render freeform section (projects with variable content)."""
    import fitz

    items = data.get(field_key, [])
    if not items:
        return

    bbox_cover = cfg["bbox_cover"]
    cover(fitz.Rect(*bbox_cover))

    layout = cfg.get("layout", {})
    if isinstance(layout, str):
        layout = {}

    start_y = cfg["start_y"]
    color = tuple(cfg.get("color", [0.12, 0.12, 0.12]))

    name_x = layout.get("name_x", 44)
    role_x = layout.get("role_x", 460)
    tech_x = layout.get("tech_x", 102)
    desc_x = layout.get("desc_x", 102)
    name_size = layout.get("name_size", 10)
    tech_size = layout.get("tech_size", 8)
    desc_size = layout.get("desc_size", 9)
    line_step = layout.get("line_step", 15)
    block_gap = layout.get("block_gap", 8)

    CLR_GRAY = (0.396, 0.396, 0.396)
    CLR_BLUE = (0.204, 0.478, 0.706)

    y = start_y
    for proj in items:
        proj_name = proj.get("name", "")
        proj_role = proj.get("role", "")
        tech = proj.get("tech", "")
        descs = proj.get("desc", [])
        if isinstance(descs, str):
            descs = [descs]

        put((name_x, y), proj_name, size=name_size, color=color)
        if proj_role:
            put((role_x, y), f"参与角色：{proj_role}", size=name_size, color=CLR_GRAY)
        y += 18

        if tech:
            put((tech_x, y), f"技术栈：{tech}", size=tech_size, color=CLR_BLUE)
            y += line_step

        for d in descs:
            put((desc_x, y), f"■  {d}", size=desc_size, color=color)
            y += line_step
        y += block_gap


def _generate_simple_pdf(markdown_content: str, language: str = "zh") -> bytes:
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_dir = BASE_DIR / "fonts"
    font_path = font_dir / "NotoSansSC-Regular.ttf"

    if font_path.exists():
        pdf.add_font("NotoSans", "", str(font_path))
        pdf.set_font("NotoSans", size=10)
    else:
        pdf.set_font("Helvetica", size=10)

    content = markdown_content.replace("**", "").replace("*", "")
    content = re.sub(r'[\U00010000-\U0010ffff]', '', content)
    lines = content.split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            pdf.ln(3)
            continue
        try:
            if stripped.startswith("# "):
                pdf.set_font_size(16)
                pdf.multi_cell(0, 10, stripped[2:].strip())
                pdf.ln(2)
                pdf.set_font_size(10)
            elif stripped.startswith("## "):
                pdf.set_font_size(13)
                pdf.multi_cell(0, 8, stripped[3:].strip())
                pdf.ln(1)
                pdf.set_font_size(10)
            elif stripped.startswith("### "):
                pdf.set_font_size(11)
                pdf.multi_cell(0, 7, stripped[4:].strip())
                pdf.set_font_size(10)
            elif stripped.startswith("- ") or stripped.startswith("* "):
                item = stripped[2:].strip()
                pdf.multi_cell(0, 6, f"  • {item}")
            else:
                pdf.multi_cell(0, 6, stripped)
        except Exception:
            continue

    return bytes(pdf.output())
