下面是这一页关于 **RAG 文档组件与文档加载器（Document & Loaders）** 的完整笔记，按照学习顺序整理。

---

# RAG 文档组件与文档加载器

## 一、整体流程

RAG 中，所有文档都会经历下面的流程：

```text
文件
    │
    ▼
Document Loader（文档加载器）
    │
    ▼
Document（统一数据结构）
    │
    ▼
Text Splitter（文本切分）
    │
    ▼
Embedding（向量化）
    │
    ▼
Vector Store（向量数据库）
    │
    ▼
Retriever（检索）
    │
    ▼
LLM（生成答案）
```

> **Loader 的作用：把各种格式的文件转换成统一的 `Document` 对象。**

---

# 二、Document（最重要）

## 什么是 Document？

Document 是 LangChain 中统一的文档对象。

无论文件来自：

* txt
* pdf
* docx
* html
* markdown

最终都会转换成：

```python
Document(
    page_content="真正的文本内容",
    metadata={
        "source": "...",
        "page": 1
    }
)
```

---

## Document 包含两个核心字段

### ① page_content

真正用于 RAG 检索的文本。

例如：

```text
ChatGPT is an AI assistant...
```

---

### ② metadata

文档的元数据。

例如：

```python
{
    "source": "book.pdf",
    "page": 5
}
```

可以保存：

* 文件路径
* 页码
* 作者
* URL
* 创建时间

等等。

---

# 三、Document Loader（文档加载器）

Loader 的作用：

> **读取各种格式的文件，并生成 Document。**

不同文件对应不同 Loader。

---

## 1）TextLoader

适用于：

* txt
* md
* log

示例：

```python
loader = TextLoader("README.md")
docs = loader.load()
```

流程：

```text
README.md
    │
    ▼
TextLoader
    │
    ▼
Document
```

特点：

* 最简单
* 最轻量
* 适合纯文本

---

## 2）UnstructuredFileLoader

万能 Loader。

支持：

* PDF
* Word
* PPT
* HTML
* Markdown
* txt
* Email
* CSV
* 图片 OCR

示例：

```python
loader = UnstructuredFileLoader("report.pdf")
docs = loader.load()
```

流程：

```text
PDF
    │
    ▼
Unstructured
    │
    ▼
Document
```

特点：

✅ 支持格式最多

缺点：

* 安装依赖较多
* 速度较慢

---

# 四、Blob（新版概念）

新版 LangChain 引入了 Blob。

很多人第一次都会觉得抽象。

实际上：

> Blob 就是**文件对象**。

可以理解成：

```text
文件

↓

Blob

↓

Document
```

Blob 里面保存的是：

```text
文件路径

或者

文件二进制(bytes)
```

例如：

```text
Blob

path="book.pdf"
```

它还没有解析。

只是：

> 我知道这个文件在哪里。

---

# 五、BlobLoader

BlobLoader 的职责只有一个：

> **找到文件。**

例如：

```text
docs/

A.pdf
B.pdf
C.docx
```

BlobLoader：

```text
↓

Blob(A.pdf)

Blob(B.pdf)

Blob(C.docx)
```

注意：

它不会：

* 打开 PDF
* 提取文字
* OCR

只是扫描文件。

---

## FileSystemBlobLoader

最常见的 BlobLoader。

负责：

扫描本地文件夹。

例如：

```python
loader = FileSystemBlobLoader("./docs")
```

流程：

```text
docs/

↓

Blob

Blob

Blob
```

---

# 六、Parser（解析器）

Parser 才是真正读取文件内容。

例如：

```text
Blob(pdf)

↓

PyPDFParser

↓

Document
```

Parser 的职责：

```text
打开文件

↓

提取文字

↓

生成 Document
```

不同 Parser：

* PyPDFParser
* DocxParser
* HTMLParser
* OCR Parser

---

# 七、GenericLoader（新版 Loader）

GenericLoader 不负责解析。

它只是：

**把 BlobLoader 和 Parser 组合起来。**

示例：

```python
loader = GenericLoader(
    blob_loader=FileSystemBlobLoader("./docs"),
    blob_parser=PyPDFParser()
)
```

内部流程：

```text
扫描文件
      │
      ▼
BlobLoader

↓

Blob

↓

Parser

↓

Document
```

可以理解成：

```python
blobs = blob_loader.load()

docs = []

for blob in blobs:
    docs.append(parser.parse(blob))
```

GenericLoader 只是负责组织整个流程。

---

# 八、新旧 Loader 对比

## 旧版

一个 Loader 全部完成。

```text
PDF

↓

PyPDFLoader

↓

Document
```

或者：

```text
txt

↓

TextLoader

↓

Document
```

---

## 新版

拆成三个角色。

```text
文件

↓

BlobLoader
（找到文件）

↓

Blob

↓

Parser
（解析文件）

↓

Document
```

最后：

```text
GenericLoader

=

BlobLoader

+

Parser
```

---

# 九、为什么新版要拆？

因为：

**扫描文件** 和 **解析文件** 是两件不同的事情。

例如：

今天：

```text
本地磁盘

↓

PDF
```

以后：

```text
S3

↓

PDF
```

只需要换：

BlobLoader。

Parser 完全不用改。

---

或者：

今天：

```text
PDF
```

以后：

```text
Word
```

只需要换：

Parser。

BlobLoader 不变。

因此：

新版更加灵活。

---

# 十、所有组件关系

```text
                 Document
                    ▲
                    │
                Parser
                    ▲
                    │
                  Blob
                    ▲
                    │
             BlobLoader
                    ▲
                    │
       FileSystemBlobLoader
```

传统 Loader：

```text
TextLoader
PyPDFLoader
UnstructuredLoader

↓

Document
```

新版 Loader：

```text
BlobLoader

+

Parser

↓

GenericLoader

↓

Document
```

---

# 十一、学习建议（按重要程度）

⭐⭐⭐⭐⭐ **必须掌握**

1. Document
2. TextLoader
3. PyPDFLoader
4. UnstructuredFileLoader

⭐⭐⭐⭐ **理解即可**

5. Blob
6. BlobLoader
7. FileSystemBlobLoader
8. Parser
9. GenericLoader

> **对于大多数 RAG 项目，前四项已经足够使用。**
> BlobLoader、Parser、GenericLoader 是 LangChain 新架构中的扩展设计，更适合处理大量、多来源、多格式文档的企业级场景。掌握它们的职责划分即可，不必一开始就深究内部实现。
