import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BASE_DIR = Path(__file__).parent
KB_DIR = BASE_DIR / "kb"
CHROMA_DIR = BASE_DIR / "chroma_db"


def load_documents():
    loader = DirectoryLoader(
        str(KB_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    return loader.load()


def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )


def get_embeddings():
    print("Loading Embeddings...")
    return FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )


def build_vectorstore():
    docs = load_documents()
    splitter = get_text_splitter()
    chunks = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )
    return vectorstore


def get_vectorstore():
    if CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir()):
        return Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=get_embeddings(),
        )
    return build_vectorstore()


def get_llm():
    return ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=1024,
    )


PROMPT_TEMPLATE = """基于以下参考文档回答用户的问题。如果文档中没有相关信息，请如实说明。

参考文档：
{context}

用户问题：{question}

请用中文回答："""


def query(question: str, k: int = 3):
    vectorstore = get_vectorstore()
    retriever = vectorstore.similarity_search_with_score(question, k=k)

    context_parts = []
    sources = []
    for doc, score in retriever:
        source = Path(doc.metadata.get("source", "unknown")).name
        context_parts.append(f"[来源: {source}]\n{doc.page_content}")
        sources.append({"source": source, "content": doc.page_content, "score": score})

    context = "\n\n---\n\n".join(context_parts)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": sources,
    }


def list_kb_files():
    return list(KB_DIR.glob("**/*.md"))


def list_kb_by_category():
    categories = {}
    for sub in sorted(KB_DIR.iterdir()):
        if sub.is_dir():
            files = list(sub.glob("*.md"))
            if files:
                categories[sub.name] = files
    root_files = list(KB_DIR.glob("*.md"))
    if root_files:
        categories["未分类"] = root_files
    return categories


def load_selected_documents(selected_files: list[str]):
    docs = []
    for rel_path in selected_files:
        file_path = KB_DIR / rel_path
        if file_path.exists():
            loader = TextLoader(str(file_path), encoding="utf-8")
            docs.extend(loader.load())
    return docs


def generate_exam(exam_type: str = "qa", selected_files: list[str] = None):
    if selected_files:
        docs = load_selected_documents(selected_files)
    else:
        docs = load_documents()
    all_content = "\n\n".join([doc.page_content for doc in docs])

    if exam_type == "qa":
        prompt = f"""基于以下知识库内容，生成 10 道面试问答题。

要求：
- 题目应覆盖知识库中的核心知识点
- 难度由浅入深，前几题基础，后几题进阶
- 每道题给出参考答案
- 格式：用 Markdown，每题包含"题目"和"参考答案"

知识库内容：
{all_content}

请生成面试问答题："""
    else:
        prompt = f"""基于以下知识库内容，生成一份笔试题（共 5 道），包含代码题和概念题。

要求：
- 2-3 道概念题（简答/判断/选择）
- 2-3 道代码题（写代码/看代码写输出/找错误）
- 每道题给出参考答案
- 格式：用 Markdown，每题包含"题目"、"题型"和"参考答案"

知识库内容：
{all_content}

请生成笔试题："""

    llm = get_llm()
    response = llm.invoke(prompt)
    return response.content


INTERVIEW_SYSTEM_TEMPLATE = """你是一位专业友好的技术面试官。基于以下知识库内容对候选人进行面试。

规则：
- 共提出 {num_questions} 个问题，覆盖知识库核心知识点
- 每次只问一个问题，等候选人回答后再继续
- 可以根据回答追问或引导，像真实面试一样自然对话
- 语气专业友好，适当鼓励
- 回复要简洁口语化（因为会被语音播报）
- 当所有问题问完后，输出评分总结：
  ## 面试评分
  | 题号 | 问题 | 得分(1-10) | 评价 |
  |------|------|-----------|------|
  最后给出总分（满分100）和整体建议
- 如果候选人说"结束面试"，立即结束并给出已完成部分的评分

知识库内容：
{content}"""


def get_interview_system_prompt(selected_files: list[str] = None, num_questions: int = 5):
    if selected_files:
        docs = load_selected_documents(selected_files)
    else:
        docs = load_documents()
    content = "\n\n".join([doc.page_content for doc in docs])
    return INTERVIEW_SYSTEM_TEMPLATE.format(num_questions=num_questions, content=content)


def interview_chat(system_prompt: str, messages: list[dict]):
    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=2048,
    )
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

    lc_messages = [SystemMessage(content=system_prompt)]
    if not messages:
        lc_messages.append(HumanMessage(content="你好，我准备好了，请开始面试。"))
    else:
        for msg in messages:
            if msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            else:
                lc_messages.append(AIMessage(content=msg["content"]))

    response = llm.invoke(lc_messages)
    return response.content


def transcribe_video(video_path: str, output_name: str = None, category: str = None) -> str:
    import io
    import speech_recognition as sr
    from pydub import AudioSegment

    audio = AudioSegment.from_file(video_path)

    chunk_length_ms = 55000
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    recognizer = sr.Recognizer()
    full_text = []

    for i, chunk in enumerate(chunks):
        wav_io = io.BytesIO()
        chunk.export(wav_io, format="wav")
        wav_io.seek(0)

        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language="en-US")
            full_text.append(text)
        except sr.UnknownValueError:
            full_text.append(f"[第{i+1}段: 未能识别]")
        except sr.RequestError as e:
            full_text.append(f"[第{i+1}段: 识别服务出错 - {e}]")

    transcript = "\n\n".join(full_text)

    if not output_name:
        output_name = Path(video_path).stem

    if category:
        target_dir = KB_DIR / category
        target_dir.mkdir(exist_ok=True)
    else:
        target_dir = KB_DIR

    output_path = target_dir / f"{output_name}.md"
    output_path.write_text(
        f"# {output_name}\n\n{transcript}",
        encoding="utf-8",
    )

    return str(output_path)


def analyze_transcript(transcript: str, category: str = None):
    existing_content = ""
    if category:
        cat_dir = KB_DIR / category
        if cat_dir.exists():
            for f in cat_dir.glob("*.md"):
                existing_content += f"\n\n--- {f.name} ---\n" + f.read_text(encoding="utf-8")
    else:
        for f in KB_DIR.glob("**/*.md"):
            existing_content += f"\n\n--- {f.name} ---\n" + f.read_text(encoding="utf-8")

    prompt = f"""你是一位学习顾问。用户刚完成一段听力/视频学习，以下是转录内容。请基于转录内容和用户已有的知识库做分析。

## 转录内容
{transcript}

## 用户已有知识库内容
{existing_content[:8000] if existing_content else "（暂无已有内容）"}

请按以下格式输出分析：

### 📌 重点整理
提炼转录内容中的核心知识点（5-10 条）

### 🔍 需要完善的点
转录内容中提到但讲解不够深入、或者用户可能没完全理解的部分

### 📝 建议补充到知识库
哪些内容值得整理成笔记加入知识库（给出具体主题和简要说明）

### 📊 薄弱点分析
对比已有知识库，分析用户在哪些方面知识比较薄弱或缺失，给出针对性学习建议

请用中文回答，分析要具体、有可操作性。"""

    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=2048,
    )
    response = llm.invoke(prompt)
    return response.content


def detect_url_type(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "ted.com" in url:
        return "ted"
    elif "github.com" in url:
        return "github"
    elif "yuque.com" in url:
        return "yuque"
    elif "pan.baidu.com" in url or "pan.quark.cn" in url or "aliyundrive.com" in url:
        return "cloud_drive"
    elif "bilibili.com" in url or "b23.tv" in url:
        return "bilibili"
    else:
        return "article"


def fetch_yuque_content(url: str) -> dict:
    import requests
    import re
    from urllib.parse import unquote
    from bs4 import BeautifulSoup

    resp = requests.get(url, timeout=15, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    resp.raise_for_status()

    match = re.search(r'decodeURIComponent\("(.+?)"\)', resp.text)
    if not match:
        raise ValueError("无法解析语雀页面数据")

    import json
    data = json.loads(unquote(match.group(1)))
    doc = data.get("doc", {})
    title = doc.get("title", "语雀文档")
    book_id = doc.get("book_id")
    slug = doc.get("slug")

    content = ""
    if book_id and slug:
        api_url = f"https://www.yuque.com/api/docs/{slug}?book_id={book_id}"
        r2 = requests.get(api_url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": url,
        })
        if r2.status_code == 200:
            doc_data = r2.json().get("data", {})
            lake_content = doc_data.get("content", "")
            if lake_content:
                soup = BeautifulSoup(lake_content, "html.parser")
                content = soup.get_text(separator="\n", strip=True)

    if not content:
        raise ValueError("无法获取语雀文档内容（可能需要登录）")

    return {"title": title, "content": content, "language": "zh", "url": url}


def fetch_youtube_transcript(url: str) -> dict:
    from youtube_transcript_api import YouTubeTranscriptApi
    import re

    match = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url)
    if not match:
        raise ValueError("无法解析 YouTube 视频 ID")
    video_id = match.group(1)

    ytt = YouTubeTranscriptApi()
    try:
        fetched = ytt.fetch(video_id, languages=["en", "zh-Hans", "zh", "zh-CN"])
        content = " ".join([entry.text for entry in fetched])
        language = "en"
    except Exception:
        transcript_list = ytt.list(video_id)
        first_transcript = next(iter(transcript_list))
        fetched = first_transcript.fetch()
        content = " ".join([entry.text for entry in fetched])
        language = first_transcript.language_code

    title = f"YouTube_{video_id}"
    try:
        import requests
        resp = requests.get(url, timeout=10)
        title_match = re.search(r"<title>(.*?)</title>", resp.text)
        if title_match:
            title = title_match.group(1).replace(" - YouTube", "").strip()
    except Exception:
        pass

    return {"title": title, "content": content, "language": language, "url": url}


def fetch_ted_transcript(url: str) -> dict:
    import requests
    from bs4 import BeautifulSoup

    if "/transcript" not in url:
        url = url.rstrip("/") + "/transcript"

    resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    paragraphs = soup.select("p[data-testid='paragraph']")
    if not paragraphs:
        paragraphs = soup.select(".Grid--with-gutter p")
    if not paragraphs:
        paragraphs = soup.select("section.Talk__transcript p, div.talk-transcript__paragraph")

    content = " ".join([p.get_text(strip=True) for p in paragraphs])
    if not content:
        all_p = soup.find_all("p")
        content = " ".join([p.get_text(strip=True) for p in all_p if len(p.get_text(strip=True)) > 20])

    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "TED Talk"

    return {"title": title, "content": content, "language": "en", "url": url}


def fetch_github_content(url: str) -> dict:
    import requests
    import re

    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}
    title = "GitHub"

    name_match = re.search(r"github\.com/([\w\.\-]+)/([\w\.\-]+)", url)
    if not name_match:
        raise ValueError("无法解析 GitHub URL")

    owner, repo = name_match.group(1), name_match.group(2)
    title = f"{owner}/{repo}"

    if "/blob/" in url:
        raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        resp = requests.get(raw_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        content = resp.text
    else:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        resp = requests.get(api_url, timeout=15, headers={**headers, "Accept": "application/vnd.github.v3.raw"})
        if resp.status_code == 200:
            content = resp.text
        else:
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            resp = requests.get(api_url, timeout=15, headers=headers)
            if resp.status_code == 200:
                repo_info = resp.json()
                desc = repo_info.get("description", "") or ""
                topics = repo_info.get("topics", [])
                content = f"# {repo_info.get('full_name', title)}\n\n"
                content += f"{desc}\n\n"
                content += f"- Language: {repo_info.get('language', 'N/A')}\n"
                content += f"- Stars: {repo_info.get('stargazers_count', 0)}\n"
                content += f"- Topics: {', '.join(topics)}\n"
            else:
                import trafilatura
                downloaded = trafilatura.fetch_url(url)
                content = trafilatura.extract(downloaded) if downloaded else ""
                if not content:
                    raise ValueError(f"无法获取 GitHub 仓库内容: {url}")

    heading_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if heading_match:
        title = heading_match.group(1).strip()

    return {"title": title, "content": content, "language": "unknown", "url": url}


def fetch_web_article(url: str) -> dict:
    import trafilatura
    import requests
    from bs4 import BeautifulSoup

    downloaded = trafilatura.fetch_url(url)
    content = None
    title = "Web Article"

    if downloaded:
        content = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
        metadata = trafilatura.extract(downloaded, output_format="json", include_comments=False)
        if metadata:
            import json
            meta = json.loads(metadata)
            title = meta.get("title", title)

    if not content:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)

        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()

        article = (
            soup.find("article")
            or soup.find("div", class_=lambda c: c and ("content" in c or "article" in c or "doc" in c))
            or soup.find("main")
        )
        if article:
            content = article.get_text(separator="\n", strip=True)
        else:
            body = soup.find("body")
            content = body.get_text(separator="\n", strip=True) if body else ""

        content = "\n".join(line for line in content.split("\n") if line.strip())

    if not content:
        raise ValueError("无法提取网页正文内容")

    return {"title": title, "content": content, "language": "unknown", "url": url}


def fetch_resource(url: str) -> dict:
    url_type = detect_url_type(url)
    if url_type == "youtube":
        result = fetch_youtube_transcript(url)
    elif url_type == "ted":
        result = fetch_ted_transcript(url)
    elif url_type == "github":
        result = fetch_github_content(url)
    elif url_type == "yuque":
        result = fetch_yuque_content(url)
    elif url_type in ("cloud_drive", "bilibili"):
        raise ValueError(f"该资源类型不支持直接抓取，请下载后使用「音视频导入」")
    else:
        result = fetch_web_article(url)
    result["type"] = url_type
    return result


def organize_content(raw_content: str, title: str, source_type: str, url: str, category: str) -> str:
    existing_content = ""
    cat_dir = KB_DIR / category
    if cat_dir.exists():
        for f in cat_dir.glob("*.md"):
            existing_content += f"\n\n--- {f.name} ---\n" + f.read_text(encoding="utf-8")

    type_labels = {"youtube": "YouTube", "ted": "TED", "article": "Article"}

    prompt = f"""你是一位学习内容整理专家。请将以下原始内容整理为结构化的学习笔记。

## 原始内容
标题: {title}
来源: {url}
类型: {type_labels.get(source_type, source_type)}

内容:
{raw_content[:12000]}

## 用户已有知识库（{category} 分类）
{existing_content[:4000] if existing_content else "（暂无）"}

## 输出要求

请按以下格式整理：

# {title}

> 来源: {url}
> 类型: {type_labels.get(source_type, source_type)}

## 核心要点
- （提炼 5-10 个核心知识点）

## 详细笔记
（按主题组织内容，用二级/三级标题分层）

## 关键词汇/术语
| 词汇 | 含义 | 例句 |
|------|------|------|
（如果是英语内容，提取重要词汇；中文内容提取专业术语）

## 学习建议
（基于内容和已有知识库，给出后续学习方向建议）

请用中文输出（术语保留英文原文）。内容要精炼有价值，不要水。"""

    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=4096,
    )
    response = llm.invoke(prompt)
    return response.content


def save_resource_to_kb(content: str, name: str, category: str) -> str:
    target_dir = KB_DIR / category
    target_dir.mkdir(exist_ok=True)
    safe_name = "".join(c for c in name if c.isalnum() or c in " _-").strip().replace(" ", "_")
    if not safe_name:
        safe_name = "resource"
    output_path = target_dir / f"{safe_name}.md"
    output_path.write_text(content, encoding="utf-8")
    return str(output_path)


def generate_learning_report(progress_summary: str) -> str:
    prompt = f"""你是一位专业的学习顾问。基于以下学习数据，生成一份个性化学习报告。

{progress_summary}

请按以下格式输出：

## 📊 学习概况
简要总结学习情况（频率、覆盖面、投入程度）

## 📈 进步与亮点
哪些方面有明显进步，值得肯定的地方

## ⚠️ 薄弱点分析
哪些分类/领域投入不足或分数偏低，需要加强

## 🎯 下周学习建议
给出具体的、可执行的学习计划建议（3-5 条）

## 💡 学习策略建议
基于数据模式，给出学习方法上的建议

请用中文回答，分析要基于数据，建议要具体可操作。"""

    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=2048,
    )
    response = llm.invoke(prompt)
    return response.content


def extract_kb_skills() -> str:
    skills = set()
    if KB_DIR.exists():
        for md_file in KB_DIR.rglob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            for line in text.split("\n"):
                line = line.strip()
                if line.startswith("# ") or line.startswith("## "):
                    heading = line.lstrip("#").strip()
                    if heading and len(heading) < 50:
                        skills.add(heading)
                elif line.startswith("- ") or line.startswith("* "):
                    item = line.lstrip("-* ").strip()
                    if 2 < len(item) < 30 and not item.startswith("http"):
                        skills.add(item)
    return "、".join(sorted(skills)[:50]) if skills else ""


def rebuild_index():
    import shutil

    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    return build_vectorstore()
