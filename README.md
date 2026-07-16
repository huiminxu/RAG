# RAG 知识库问答 & 学习辅助系统

基于本地 Markdown 文档 + Claude 大模型的 RAG（检索增强生成）系统，支持知识库问答、面试练习、资源聚合等一站式学习辅助功能。

## 功能概览

| Tab | 功能 | 说明 |
|-----|------|------|
| 🌸 知识问答 | RAG 检索问答 | 从文档检索相关内容，Claude 生成回答，来源高亮定位 |
| 🌺 技术趋势 | 多渠道聚合 | GitHub/Hacker News/Dev.to/B站 热门资源，按领域筛选 |
| 🌻 资源导入 | 三合一导入 | URL 抓取 / 音视频上传转录 / 手动编写，统一保存到知识库 |
| 🌼 智能出题 | 自动出题 | 基于知识库生成问答题 + 笔试题，支持指定文档范围 |
| 🌹 AI 对练 | 模拟面试 | AI 面试官逐题问答，实时评分反馈，支持语音输入 |
| 🍀 文档助手 | 简历优化 | 上传 PDF + JD → AI 生成优化简历（HTML 排版 + PDF 打印） |
| 🌱 学习进度 | 数据追踪 | 面试评分趋势、分类分布、AI 学习报告 |

## 知识问答功能详情

- **RAG 检索问答**：输入问题，系统自动检索知识库相关片段 + Claude 生成回答
- **参考来源展示**：每次回答标注匹配的文档来源（文件名 + 相似度百分比）
- **来源高亮定位**：点击来源按钮打开文档预览，匹配段落自动高亮（粉色左边框）
- **智能过滤**：同一文件只显示最高相似度的一条，低于 20% 的不相关结果自动过滤
- **通用知识兜底**：知识库无相关内容时用 AI 通用知识回答，并标注来源类型
- **对话上下文**：保留最近 100 条消息，支持连续多轮对话

## 资源导入功能详情

三种导入方式统一在一个 Tab 中：

| 方式 | 说明 |
|------|------|
| 🔗 URL 导入 | 支持 YouTube/TED/GitHub/语雀/网页文章，自动抓取 + AI 整理为结构化笔记 |
| 📁 文件上传 | 上传 MP4/MP3/M4A/WAV，自动转录 + AI 分析重点/薄弱点 |
| ✏️ 手动编写 | 直接编写 Markdown 内容，选择分类后保存到知识库 |

## 界面主题

系统支持双主题切换（侧边栏切换按钮）：

| 主题 | 风格 |
|------|------|
| 浅色（默认） | 粉蓝碎花渐变，柔和花园风 |
| 深色 | 深紫花园，紫粉霓虹感 |

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

将 Markdown 文件放入 `kb/` 目录（支持按分类建子目录）：

```
kb/
├── english/
│   ├── interview.md
│   └── introduction.md
├── frontend/
│   └── vue2.md
└── your-notes.md
```

### 5. 启动应用

```bash
python -m streamlit run app.py --server.headless true
```

浏览器访问 http://localhost:8501

## 使用说明

### 知识问答

1. 打开 **🌸 知识问答** 标签页
2. 在输入框输入问题（如"Vue3 有哪些性能优化？"）
3. 系统自动检索相关文档片段并生成回答
4. 点击「参考来源」展开查看引用的文档来源
5. 点击来源按钮打开文档预览，匹配段落自动高亮
6. 知识库无相关内容时用通用知识回答并标注

### 资源导入

1. 打开 **🌻 资源导入** 标签页
2. 选择导入方式：
   - **URL 导入**：粘贴链接，自动识别类型（YouTube/TED/GitHub/语雀/网页），AI 整理为笔记
   - **文件上传**：上传音视频文件，自动转录 + AI 分析重点与薄弱点
   - **手动编写**：直接编写 Markdown 内容，选择分类保存
3. 预览确认后保存到对应分类
4. 保存后点击侧边栏「重建索引」更新向量数据库

### 智能出题

1. 打开 **🌼 智能出题** 标签页
2. （可选）选择指定的知识库文档，不选则使用全部
3. 点击「生成问答题」或「生成笔试题」
4. 生成完成后可在线查看或下载 Markdown 文件

### AI 对练（模拟面试）

1. 打开 **🌹 AI 对练** 标签页
2. 选择面试分类和题目数量
3. AI 面试官逐题提问，你输入/语音回答
4. 每题实时评分 + 建议，结束后给出总分

### 技术趋势

1. 打开 **🌺 技术趋势** 标签页
2. 选择语言/领域（JavaScript、Python、AI、大模型、英语等），或选「自定义」输入关键词
3. 选择时间范围（今天/本周/本月）
4. 查看四大渠道聚合结果：
   - **GitHub** — 高星新项目
   - **Hacker News** — 热门技术讨论
   - **Dev.to** — 开发者社区热文
   - **B站** — 科技/数码区热门视频
5. 数据每小时自动缓存，点「刷新」强制更新

### 文档助手（简历优化）

1. 打开 **🍀 文档助手** 标签页
2. 上传 PDF 简历，可点击「从此 PDF 生成 HTML 模板」自动生成匹配风格
3. 输入目标公司简介 + 职位描述（支持图片上传识别）
4. 点击「生成优化简历」→ 预览 HTML 排版 / 中英文 Markdown
5. 下载 HTML 文件，浏览器打开后 Ctrl+P 打印为 PDF

### 学习进度

1. 打开 **🌱 学习进度** 标签页
2. 查看面试次数、平均分、资源数等指标
3. 点击「生成 AI 学习报告」获取个性化建议

### 知识库管理

- **侧边栏文件浏览**：按分类查看所有知识库文档，点击可预览/编辑
- **分类管理**：新增/重命名/删除分类
- **重建索引**：添加新文档后点击侧边栏「重建索引」按钮更新向量数据库

## 项目结构

```
rag/
├── kb/                # 知识库文档目录（按分类建子目录）
├── resume/            # 简历模板 PDF 存放目录
├── fonts/             # 中文字体（NotoSansSC，PDF 生成用）
├── templates/         # HTML 简历模板目录
├── styles/            # CSS 主题样式
│   ├── __init__.py    # load_theme_css() / load_dialog_css()
│   ├── light.css      # 浅色主题
│   ├── dark.css       # 深色主题
│   ├── dialog_light.css  # 浅色对话框样式
│   └── dialog.css     # 深色对话框样式
├── tabs/              # Tab 模块（每个 Tab 一个文件）
│   ├── tab_chat.py    # 知识问答
│   ├── tab_trends.py  # 技术趋势
│   ├── tab_resource.py # 资源导入（URL/文件/手动）
│   ├── tab_exam.py    # 智能出题
│   ├── tab_interview.py # AI 对练
│   ├── tab_resume.py  # 文档助手
│   └── tab_progress.py # 学习进度
├── app.py             # Streamlit 应用入口（7 个 Tab + 双主题）
├── sidebar.py         # 侧边栏（KB 管理 + 文档预览）
├── rag_engine.py      # RAG 核心：向量检索、文档加载、资源抓取、AI 分析
├── resume.py          # 简历解析、版本管理、AI 优化生成
├── resume_html.py     # HTML 简历渲染（Jinja2 模板 + PDF Vision 模板生成）
├── trends.py          # 技术趋势聚合（GitHub/HN/Dev.to/B站 API）
├── progress.py        # 学习进度追踪（面试/资源/查询记录 + 统计）
├── requirements.txt   # Python 依赖
├── .env.example       # 环境变量模板
└── chroma_db/         # ChromaDB 向量数据库（自动生成）
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 框架 | LangChain |
| LLM | Anthropic Claude (claude-sonnet-4-6) |
| Embedding | FastEmbed (ONNX Runtime) |
| 向量数据库 | ChromaDB（chunk_size=200, overlap=30） |
| Web UI | Streamlit |
| PDF 解析 | PyPDF2 + PyMuPDF |
| HTML 简历 | Jinja2 + WeasyPrint + Claude Vision |
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

目前支持 Markdown (.md) 文件。放入 `kb/` 目录即可，支持按子目录分类。

**Q: ChromaDB 报错 "no such table: tenants"？**

向量数据库文件损坏。系统已内置自动检测修复：启动时验证数据库完整性，异常时自动删除并重建索引。也可手动删除 `chroma_db/` 目录后重启。

**Q: 如何切换主题？**

点击侧边栏右上角的 🌙/☀️ 按钮即可在浅色碎花与深紫花园主题之间切换。

**Q: 搜索不到知识库内容？**

添加/修改文档后需点击侧边栏「重建索引」按钮更新向量数据库。若知识库确实无相关内容，系统会用通用知识回答并标注。
