这些看起来是在整理 **LangChain 文档分割器**。可以按下面方式理解和选型：

| 分割方式        | 适用内容                  | 核心特点                             |
| ----------- | --------------------- | -------------------------------- |
| 递归字符分割器     | 普通文本、Markdown、中文文档    | 按优先级依次尝试段落、换行、句子、字符边界，直到块大小符合要求  |
| 衍生代码分割器     | Python、Java、JS、Go 等源码 | 使用对应编程语言的结构分隔符，尽量保留类、函数和代码块      |
| 中文场景分割      | 中文文章、知识库、客服资料         | 增加中文句号、问号、感叹号、逗号及零宽空格等分隔符        |
| 语义化分割       | 主题变化明显的长文本            | 基于 Embedding 判断相邻句子的语义差异，按主题边界切分 |
| HTML 分割器    | 网页、富文本                | 按标题、章节和 HTML 元素切分，并可保留层级元数据      |
| 递归 JSON 分割器 | 嵌套 JSON、API 返回结果      | 按对象和数组结构递归拆分，尽量保持 JSON 结构完整      |

### 1. 递归字符文档分割器

`RecursiveCharacterTextSplitter` 是通用场景中最常用的选择。默认会优先保留段落，其次保留句子和单词；只有前面的边界无法满足块大小时，才继续采用更细粒度的边界。([LangChain Reference Docs][1])

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
)

chunks = splitter.split_text(text)
```

### 2. 衍生代码分割器

代码分割通常仍基于 `RecursiveCharacterTextSplitter`，但通过 `from_language()` 加载特定语言的分隔规则：

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language,
)

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=1200,
    chunk_overlap=150,
)

chunks = splitter.split_text(source_code)
```

它比直接按字符切分更适合代码，因为会优先在类、函数和控制结构附近寻找边界。

### 3. 中文场景下的分割

中文没有稳定的空格边界，因此不建议只使用默认的：

```python
["\n\n", "\n", " ", ""]
```

更适合中文的配置是：

```python
chinese_separators = [
    "\n\n",
    "\n",
    "。", "！", "？",
    "；",
    "……",
    "，",
    "、",
    "\u200b",
    "",
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=chinese_separators,
    length_function=len,
)
```

实际用于 RAG 时，还可以使用模型 tokenizer 来计算块大小，避免“字符数合适，但 token 数超限”：

```python
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base",
    chunk_size=500,
    chunk_overlap=80,
    separators=chinese_separators,
)
```

### 4. 语义化分割

语义分割不是按照固定符号切分，而是：

1. 先拆成句子；
2. 为句子或句子窗口生成 Embedding；
3. 计算相邻内容的语义距离；
4. 在语义变化明显的位置切分。

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=90,
)

documents = splitter.create_documents([text])
```

适合：

* 长篇报告；
* 访谈记录；
* 主题连续变化的文章；
* 对检索召回质量要求较高的知识库。

代价是需要调用 Embedding 模型，速度和费用都高于字符分割。生产中通常采用“结构分割 + 语义分割”的组合，而不是对所有内容直接做语义分割。

### 5. HTML 分割器

LangChain 当前提供多种 HTML 分割方式：

* `HTMLHeaderTextSplitter`：按 `h1`、`h2`、`h3` 等标题切分；
* `HTMLSectionSplitter`：按页面章节切分；
* `HTMLSemanticPreservingSplitter`：尽量保留表格、列表等语义结构。([LangChain Reference Docs][2])

```python
from langchain_text_splitters import HTMLHeaderTextSplitter

headers = [
    ("h1", "一级标题"),
    ("h2", "二级标题"),
    ("h3", "三级标题"),
]

splitter = HTMLHeaderTextSplitter(
    headers_to_split_on=headers
)

documents = splitter.split_text(html_content)
```

返回的文档会携带标题层级元数据，适合网页知识库：

```python
Document(
    page_content="章节正文",
    metadata={
        "一级标题": "产品文档",
        "二级标题": "快速开始"
    }
)
```

如果标题章节仍然很大，可以再接一个递归字符分割器：

```python
header_docs = splitter.split_text(html_content)

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
)

final_docs = recursive_splitter.split_documents(header_docs)
```

### 6. 递归 JSON 分割器

`RecursiveJsonSplitter` 根据 JSON 的字典和数组结构递归拆分，不是简单地把序列化字符串截断。这样能尽量保证每个分块仍然具有可理解的键值关系。其实现位于 LangChain 的 `json.py` 模块。([GitHub][3])

```python
import json
from langchain_text_splitters import RecursiveJsonSplitter

data = json.loads(json_text)

splitter = RecursiveJsonSplitter(
    max_chunk_size=1000,
)

json_chunks = splitter.split_json(json_data=data)
text_chunks = splitter.split_text(json_data=data)
```

对于数组很多的 JSON，可以根据版本和数据结构考虑：

```python
splitter = RecursiveJsonSplitter(
    max_chunk_size=1000,
    min_chunk_size=300,
)

chunks = splitter.split_json(
    json_data=data,
    convert_lists=True,
)
```

### 推荐选型

普通中文知识库优先使用：

```text
中文递归字符分割
```

源码知识库优先使用：

```text
语言感知代码分割
```

网页知识库优先使用：

```text
HTML 标题分割 → 中文递归字符分割
```

结构化接口数据优先使用：

```text
递归 JSON 分割
```

高质量但成本更高的检索系统可使用：

```text
结构分割 → 语义分割 → token 长度兜底
```

[1]: https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter?utm_source=chatgpt.com "RecursiveCharacterTextSplitter | langchain_text_splitters"
[2]: https://reference.langchain.com/python/langchain-text-splitters/langchain_text_splitters?utm_source=chatgpt.com "langchain_text_splitters | LangChain Reference"
[3]: https://github.com/langchain-ai/langchain/blob/master/libs/text-splitters/langchain_text_splitters/json.py?utm_source=chatgpt.com "langchain/libs/text-splitters/langchain_text_splitters/json.py at ..."


这两个术语通常表示 **Transformer 架构在不同 NLP 任务中的应用**，区别在于它们解决的问题不同。

| 名称        | 英文                                              | 解释                                  | 输入          | 输出     | 应用场景               |
| --------- | ----------------------------------------------- | ----------------------------------- | ----------- | ------ | ------------------ |
| **问答转换器** | Question Answering Transformer (QA Transformer) | 利用 Transformer 模型理解问题和上下文，并生成或抽取答案。 | 问题 + 文档/上下文 | 答案     | 智能客服、知识问答、RAG、搜索问答 |
| **翻译转换器** | Translation Transformer                         | 利用 Transformer 模型将一种语言转换成另一种语言。     | 源语言文本       | 目标语言文本 | 机器翻译、多语言系统         |

### 1. 问答转换器（Question Answering Transformer）

**定义：**
一种基于 Transformer 的问答模型，能够理解用户提出的问题，并根据提供的上下文生成答案或从上下文中抽取答案。

**工作流程：**

```
问题：Transformer 是什么？

上下文：
Transformer 是 Google 在 2017 年提出的深度学习模型……

        ↓

模型

        ↓

答案：
Transformer 是 Google 于 2017 年提出的一种深度学习模型。
```

**典型应用：**

* ChatGPT
* RAG（检索增强生成）
* 企业知识库问答
* 智能客服
* 阅读理解（SQuAD）

---

### 2. 翻译转换器（Translation Transformer）

**定义：**
一种基于 Transformer 的机器翻译模型，将输入文本从一种语言转换为另一种语言。

**工作流程：**

```
输入：
I love artificial intelligence.

        ↓

Transformer

        ↓

输出：
我喜欢人工智能。
```

**典型应用：**

* Google Translate
* DeepL
* 百度翻译
* 多语言内容生成

---

### 两者区别

| 对比项      | 问答转换器                   | 翻译转换器                    |
| -------- | ----------------------- | ------------------------ |
| **目标**   | 回答问题                    | 翻译语言                     |
| **输入**   | 问题 + 上下文                | 源语言文本                    |
| **输出**   | 问题答案                    | 目标语言文本                   |
| **核心能力** | 理解问题、检索信息、推理            | 理解语义、跨语言映射               |
| **典型任务** | Question Answering (QA) | Machine Translation (MT) |

### 与 Transformer 的关系

需要注意的是，**Transformer 是一种模型架构，而不是具体任务**。因此：

* **问答转换器** = 用于问答任务的 Transformer 模型
* **翻译转换器** = 用于机器翻译任务的 Transformer 模型

更符合 AI 领域的专业表达通常是：

* **QA Transformer（问答 Transformer）**
* **Translation Transformer（翻译 Transformer）**
* **Transformer-based Question Answering Model（基于 Transformer 的问答模型）**
* **Transformer-based Machine Translation Model（基于 Transformer 的机器翻译模型）**

在学术论文和开源项目中，通常保留 **Transformer** 英文名称，而不是将其直译为“转换器”。
