# 向量数据库学习笔记：FAISS、Pinecone、TCVectorDB

## 一、什么是向量数据库（Vector Database）

大语言模型（LLM）本身无法直接搜索文档，因此通常会将文本转换成 **Embedding（向量）**，再存入向量数据库，通过相似度搜索找到最相关的内容，这就是 **RAG（Retrieval-Augmented Generation）** 的核心流程。

```
文档
  │
Chunk（切分）
  │
Embedding Model
  │
向量（Embedding）
  │
Vector Database
  │
Similarity Search（相似度搜索）
  │
Top K 文档
  │
LLM
```

常见的向量存储方案有：

* FAISS（Meta 开源）
* Chroma
* Pinecone
* Milvus
* Qdrant
* Weaviate
* TCVectorDB（腾讯云）

---

# 二、FAISS

> Facebook AI Similarity Search

官网：[https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)

## 定位

FAISS **不是数据库**，而是一个**向量检索库（Library）**。

它只负责：

> 已经有一堆向量，如何最快找到最相似的几个？

例如：

```
Embedding

↓

FAISS Index

↓

Top K
```

它不负责：

* 数据存储
* 用户管理
* API
* 权限
* 元数据
* 高可用
* 集群

所以它更像：

```
NumPy

或者

Scikit-Learn
```

只是一个 Python/C++ 库。

---

## 示例

```python
from langchain_community.vectorstores import FAISS

db = FAISS.from_documents(docs, embedding)

db.similarity_search("What is LangChain?")
```

底层其实就是：

```python
index.add(vectors)

index.search(query, k=5)
```

---

## 持久化

默认：

```
内存

↓

程序结束

↓

数据消失
```

如果要保存：

```python
db.save_local("faiss_index")
```

再次加载：

```python
db = FAISS.load_local(...)
```

---

## 优点

✅ 免费

✅ 开源

✅ 检索速度快

✅ GPU 加速

✅ 教程最多

---

## 缺点

所有数据库能力都需要自己实现：

* CRUD
* Metadata
* API
* 集群
* 权限
* 自动扩容
* 高可用

---

# 三、Pinecone

官网：[https://www.pinecone.io/](https://www.pinecone.io/)

## 定位

Pinecone 是真正意义上的 **Vector Database（向量数据库）**。

可以理解成：

```
MySQL
↓

存文本

-------------------

Pinecone
↓

存向量
```

它不仅能存储向量，还提供：

```
Embedding

Metadata

Namespace

Collection

Filter

Delete

Update

REST API
```

是一套完整的数据库服务。

---

## 示例

写入：

```python
index.upsert([
    {
        "id": "1",
        "values": [...],
        "metadata": {
            "title": "LangChain"
        }
    }
])
```

查询：

```python
index.query(
    vector=query,
    top_k=5,
    filter={
        "title": "LangChain"
    }
)
```

---

## 特点

无需自己维护服务器：

```
你的程序

↓

Pinecone Cloud

↓

自动扩容

自动备份

自动高可用
```

---

## 优点

* 托管服务
* 高可用
* 自动扩容
* Metadata Filter
* REST API
* SDK 完善
* LangChain 官方支持

---

## 缺点

* 收费
* 海外服务为主
* 国内访问速度一般

---

# 四、TCVectorDB（腾讯云向量数据库）

官网：[https://cloud.tencent.com/product/vdb](https://cloud.tencent.com/product/vdb)

## 定位

腾讯云推出的企业级向量数据库。

本质上可以理解为：

```
腾讯云版 Pinecone
```

适合：

* 腾讯云生态
* 国内部署
* 企业级应用

---

## 支持能力

* Collection
* Namespace
* Metadata
* Filter
* ANN
* REST API
* SDK
* 自动扩容
* 高可用

---

## 优势

如果业务部署在腾讯云：

```
COS

CVM

TKE

CLS

SCF
```

使用 TCVectorDB 会更加方便。

---

# 五、三者对比

| 对比项             | FAISS  | Pinecone | TCVectorDB   |
| --------------- | ------ | -------- | ------------ |
| 类型              | 开源库    | 托管向量数据库  | 腾讯云向量数据库     |
| 是否需要部署          | ✅ 自己部署 | ❌ 不需要    | ❌ 不需要        |
| 是否存储数据          | 自己实现   | ✅        | ✅            |
| Metadata Filter | 基本没有   | ✅        | ✅            |
| CRUD            | 较弱     | 完整支持     | 完整支持         |
| REST API        | ❌      | ✅        | ✅            |
| 自动扩容            | ❌      | ✅        | ✅            |
| 高可用             | ❌      | ✅        | ✅            |
| GPU             | ✅      | 云端支持     | 云端支持         |
| 成本              | 免费     | 收费       | 收费（国内通常更有优势） |

---

# 六、LangChain 集成

三者都可以作为 LangChain 的 Vector Store。

### FAISS

```python
from langchain_community.vectorstores import FAISS
```

### Pinecone

```python
from langchain_pinecone import PineconeVectorStore
```

### TCVectorDB

```python
from langchain_community.vectorstores import TencentVectorDB
```

常见接口基本一致：

```python
add_documents()

similarity_search()

delete()

as_retriever()
```

这也是 LangChain 的优势：**统一接口，不同底层实现可以方便替换。**

---

# 七、如何选择

| 场景        | 推荐                   |
| --------- | -------------------- |
| 学习 RAG 原理 | ⭐⭐⭐⭐⭐ FAISS          |
| 本地 Demo   | ⭐⭐⭐⭐⭐ FAISS / Chroma |
| 中小型项目     | ⭐⭐⭐⭐ Chroma / Qdrant |
| 海外生产环境    | ⭐⭐⭐⭐⭐ Pinecone       |
| 国内生产环境    | ⭐⭐⭐⭐⭐ TCVectorDB     |
| 超大规模企业    | ⭐⭐⭐⭐⭐ Milvus         |

---

# 八、学习路线

```
Embedding
        │
        ▼
FAISS（理解向量检索）
        │
        ▼
Chroma（本地向量数据库）
        │
        ▼
Pinecone（云端向量数据库）
        │
        ▼
Milvus / Qdrant / TCVectorDB
（企业级生产环境）
```

建议顺序：

1. **Embedding 原理**：理解文本如何转换为向量。
2. **FAISS**：掌握向量索引、相似度搜索和 RAG 基础流程。
3. **Chroma**：学习本地持久化、Metadata、Retriever 等概念。
4. **Pinecone / TCVectorDB**：了解托管向量数据库、云端部署、扩缩容等生产能力。
5. **Milvus / Qdrant**：深入学习企业级向量数据库的架构和高性能检索。

---

# 九、一句话总结

> **FAISS 是向量检索库，Pinecone 和 TCVectorDB 是完整的向量数据库。**

学习阶段推荐：

> **FAISS → Chroma → Pinecone → TCVectorDB（或 Milvus/Qdrant）**

这个顺序既能帮助理解底层原理，又能逐步过渡到企业级 AI/RAG 应用开发。
