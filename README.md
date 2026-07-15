# RAG 知识库问答 & 面试卷生成系统

基于本地 Markdown 文档 + Claude 大模型的 RAG（检索增强生成）系统，支持知识库问答和自动生成面试卷。

## 功能

| Tab | 功能 | 说明 |
|-----|------|------|
| 💬 知识库问答 | RAG 检索问答 | 从文档检索相关内容，Claude 生成回答并标注来源 |
| 📝 面试卷生成 | 自动出题 | 基于知识库生成问答题 + 笔试题，支持指定文档范围 |
| 🎙️ 模拟面试 | AI 面试官 | 逐题问答，实时评分反馈，支持语音输入 |
| 📥 音视频导入 | 内容转录 | 上传 MP4/音频，自动转录 + AI 分析重点/薄弱点 |
| 📚 资源导入 | URL 抓取整理 | 支持 YouTube/TED/GitHub/语雀/网页文章，AI 整理后存入 KB |
| 📈 学习进度 | 数据追踪 | 面试评分趋势、分类分布、AI 学习报告 |
| 📄 简历优化 | 双语简历生成 | 上传 PDF + JD → AI 生成优化简历（HTML 排版 + 浏览器打印 PDF） |
| 🔥 技术趋势 | 多渠道聚合 | GitHub/Hacker News/Dev.to/B站 热门资源，支持按领域筛选 |

## 环境要求

- Python 3.10+
- Anthropic API Key（[获取地址](https://console.anthropic.com/)）

## 快速开始

### 1. 克隆项目

```bash
git clone <仓库地址>
cd rag
```

### 2. 安装依赖

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 配置 API Key

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 Anthropic API Key：

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### 4. 添加知识库文档

将 Markdown 文件放入 `kb/` 目录：

```
kb/
├── vue3.md
├── react.md
├── your-notes.md
└── ...
```

### 5. 启动应用

```bash
python -m streamlit run app.py --server.headless true
```

浏览器访问 http://localhost:8501

## 使用说明

### 知识库问答

1. 打开 **💬 知识库问答** 标签页
2. 在输入框输入问题（如"Vue3 有哪些性能优化？"）
3. 系统自动检索相关文档片段并生成回答
4. 点击"参考来源"可查看引用的原文

### 面试卷生成

1. 打开 **📝 面试卷生成** 标签页
2. （可选）在顶部选择指定的知识库文档，不选则使用全部
3. 点击"生成问答题"或"生成笔试题"
4. 生成完成后可在线查看或下载 Markdown 文件

### 模拟面试

1. 打开 **🎙️ 模拟面试** 标签页
2. 选择面试分类和题目数量
3. AI 面试官逐题提问，你输入/语音回答
4. 每题实时评分 + 建议，结束后给出总分

### 音视频导入

1. 打开 **📥 音视频导入** 标签页
2. 上传 MP4/MP3/WAV 等文件
3. 系统自动转录内容 + AI 分析重点
4. 预览确认后保存到知识库

### 资源导入

1. 打开 **📚 资源导入** 标签页
2. 粘贴 URL（YouTube / TED / GitHub / 语雀 / 网页文章）
3. 系统自动抓取内容 + AI 整理为笔记格式
4. 预览确认后保存到知识库

### 学习进度

1. 打开 **📈 学习进度** 标签页
2. 查看面试次数、平均分、资源数等指标
3. 点击「生成 AI 学习报告」获取个性化建议

### 简历优化

1. 打开 **📄 简历优化** 标签页
2. 上传 PDF 简历（首次），可点击「从此 PDF 生成 HTML 模板」自动生成匹配风格
3. 输入目标公司简介 + 职位描述（支持图片上传识别）
4. 点击「生成优化简历」→ 预览 HTML 排版 / 中英文 Markdown
5. 下载 HTML 文件，浏览器打开后 Ctrl+P 打印为 PDF

### 技术趋势

1. 打开 **🔥 技术趋势** 标签页
2. 选择语言/领域（JavaScript、Python、AI、大模型、英语等），或选「自定义」输入任意关键词
3. 选择时间范围（今天/本周/本月）
4. 查看四大渠道聚合结果：
   - **GitHub** — 高星新项目
   - **Hacker News** — 热门技术讨论
   - **Dev.to** — 开发者社区热文
   - **B站** — 科技/数码区热门视频
5. 数据每小时自动缓存，点「刷新」强制更新

### 更新知识库

向 `kb/` 目录添加新文档后，点击侧边栏的 **🔄 重建索引** 按钮更新向量数据库。

## 项目结构

```
rag/
├── kb/                # 知识库文档目录（按分类建子目录）
│   ├── english/       # 英语学习
│   ├── frontend/      # 前端技术
│   ├── agent/         # AI Agent
│   └── backend/       # 后端技术
├── resume/            # 简历模板 PDF 存放目录
├── fonts/             # 中文字体（NotoSansSC，PDF 生成用）
├── app.py             # Streamlit Web 应用（8 个 Tab）
├── rag_engine.py      # RAG 核心逻辑 + 资源抓取 + AI 分析
├── resume.py          # 简历解析、AI 优化
├── resume_html.py     # HTML 简历渲染（Jinja2 模板 + PDF Vision 生成）
├── trends.py          # 技术趋势聚合（GitHub/HN/Dev.to/B站）
├── templates/         # HTML 简历模板目录
├── progress.py        # 学习进度追踪（面试/资源/查询记录）
├── progress.json      # 学习进度数据（自动生成）
├── resume_data.json   # 简历数据 + 历史版本（自动生成）
├── requirements.txt   # Python 依赖
├── .env.example       # 环境变量模板
└── chroma_db/         # 向量数据库（自动生成）
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 框架 | LangChain |
| LLM | Anthropic Claude (claude-sonnet-4-6) |
| Embedding | FastEmbed (ONNX Runtime) |
| 向量数据库 | ChromaDB |
| Web UI | Streamlit |
| PDF 解析 | PyPDF2 |
| HTML 简历 | Jinja2 模板 + Claude Vision（PDF→HTML 模板生成） |
| 技术趋势 | GitHub API / HN Firebase API / Dev.to API / Bilibili API |
| 视频转录 | SpeechRecognition + pydub |
| 网页抓取 | trafilatura + BeautifulSoup |
| YouTube | youtube-transcript-api |

## 常见问题

**Q: 首次启动很慢？**

首次运行会自动下载 Embedding 模型（约 50MB），之后会缓存到本地。

**Q: 报错 "team not allowed to access model"？**

检查 `.env` 中的 API Key 对应的团队是否有模型访问权限。可在 `rag_engine.py` 中修改 `model` 参数为你可用的模型。

**Q: 如何更换模型？**

编辑 `rag_engine.py` 中 `get_llm()` 函数的 `model` 参数，可选值参考你的 API Key 权限。

**Q: 知识库支持什么格式？**

目前支持 Markdown (.md) 文件。放入 `kb/` 目录即可。
