如果把 LangChain 的 Runnable 比作乐高积木：

数据流：|、RunnableSequence
并行：RunnableParallel
分支：RunnableBranch
转换：RunnableLambda
透传/增强：RunnablePassthrough、RunnableAssign
稳定性：with_retry、with_fallbacks
可观测性：with_listeners
配置：with_config
执行方式：invoke、batch、stream

这些基本覆盖了构建生产级 LangChain 应用时最核心的 Runnable 能力。

三者对比
方法	作用	触发时机	典型场景
with_retry()	自动重试	执行失败时	API 超时、429、网络抖动
with_fallbacks()	自动切换备用 Runnable	重试仍失败或直接失败时	多模型容灾、服务降级
with_listeners()	生命周期监听	开始、结束、异常	日志、监控、埋点、统计耗时
一个完整示例

这三个能力可以组合使用：

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

primary = ChatOpenAI()
backup = ChatAnthropic()

chain = (
    primary
    .with_retry(stop_after_attempt=3)
    .with_fallbacks([backup])
    .with_listeners(
        on_start=lambda run: print("开始"),
        on_end=lambda run: print("结束"),
        on_error=lambda run: print("发生异常")
    )
)

response = chain.invoke("什么是 RAG？")

执行流程可能是：

开始
  │
  ▼
OpenAI 调用
  │
  ├─ 失败（第 1 次）
  │
  ├─ 自动重试（第 2 次）
  │
  ├─ 自动重试（第 3 次）
  │
  ├─ 仍失败
  ▼
切换到 Claude（Fallback）
  │
  ▼
返回结果
  │
  ▼
结束

可以把它们分别理解为三个层面的增强能力：

with_retry：解决"偶发失败"，提高稳定性。
with_fallbacks：解决"主方案不可用"，提供备用方案，增强可用性。
with_listeners：解决"可观测性"，让你能够记录日志、监控性能、统计耗时或更新界面。

这也是构建生产级 LangChain 应用时非常常见的一组组合。


# LangChain｜configurable_alternatives()

## 一、什么是 configurable_alternatives？

`configurable_alternatives()` 是 LangChain Runnable 提供的一个高级能力，用于**在运行时（Runtime）根据配置动态切换不同的 Runnable 实现**。

它最大的特点是：

> **无需修改业务代码，只需修改运行配置，即可切换不同的实现。**

简单来说，就是把"选择使用哪个组件"的逻辑，从 Python 代码中抽离出来，交给运行时配置。

---

# 二、最简单的例子

假设默认使用 Claude，但有时希望切换到 GPT。

传统写法：

```python
if model == "anthropic":
    llm = ChatAnthropic(...)
else:
    llm = ChatOpenAI(...)
```

使用 `configurable_alternatives()`：

```python
from langchain_core.runnables.utils import ConfigurableField
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-3-5-sonnet"
).configurable_alternatives(
    ConfigurableField(id="llm"),
    default_key="anthropic",
    openai=ChatOpenAI(model="gpt-4o"),
)
```

默认执行：

```python
model.invoke("Hello")
```

实际调用：

```
Claude
```

如果运行时指定配置：

```python
model.with_config(
    configurable={
        "llm": "openai"
    }
).invoke("Hello")
```

实际调用：

```
GPT-4o
```

整个业务代码无需修改。

---

# 三、执行流程

默认：

```
invoke()

        │
        ▼

default_key = anthropic

        │
        ▼

ChatAnthropic
```

指定配置：

```
invoke()

        │
        ▼

configurable={
    "llm":"openai"
}

        │
        ▼

ChatOpenAI
```

整个切换发生在**运行时（Runtime）**，而不是 Python 代码层。

---

# 四、可以切换什么？

很多人认为它只能切换 LLM，其实并不是。

它可以切换**任何 Runnable**。

## ① LLM

```
Claude

↓

GPT

↓

Gemini

↓

DeepSeek
```

---

## ② Prompt

```
默认 Prompt

↓

客服 Prompt

↓

销售 Prompt

↓

技术支持 Prompt
```

---

## ③ Retriever

```
Chroma

↓

Pinecone

↓

Milvus

↓

Weaviate
```

---

## ④ Embedding

```
OpenAI

↓

FastEmbed

↓

BGE

↓

VoyageAI
```

---

## ⑤ Output Parser

```
JsonOutputParser

↓

PydanticOutputParser
```

---

## ⑥ 整个 Runnable Chain

甚至整个 LCEL 链都可以作为不同实现进行切换。

---

# 五、为什么需要它？

传统项目：

```python
if use_openai:
    ...
elif use_claude:
    ...
elif use_gemini:
    ...
```

随着模型越来越多：

```
if...
else...
elif...
```

会越来越难维护。

使用 `configurable_alternatives()` 后：

```
业务代码

↓

保持不变

↓

运行配置决定使用哪个 Runnable
```

这样：

* 更容易维护
* 更方便扩展
* 更容易做实验
* 更适合生产部署

---

# 六、和 LCEL 的关系

LCEL（LangChain Expression Language）负责把多个 Runnable 组合成一条执行链。

例如：

```
Prompt

↓

LLM

↓

OutputParser
```

如果 LLM 使用了 `configurable_alternatives()`：

```
Prompt
    │
    ▼
configurable_alternatives
    │
┌───┴─────────────┐
│                 │
Claude         GPT-4o
│                 │
└──────┬──────────┘
       ▼
OutputParser
```

整个 LCEL 结构无需修改。

---

# 七、典型应用场景

## 场景一：开发 / 测试 / 生产环境

开发：

```python
configurable={
    "llm":"openai"
}
```

生产：

```python
configurable={
    "llm":"anthropic"
}
```

无需修改任何业务代码。

---

## 场景二：SaaS 多租户

不同客户使用不同模型。

```
A 公司

↓

Claude

--------------------

B 公司

↓

GPT

--------------------

C 公司

↓

Gemini
```

业务逻辑完全一致，仅配置不同。

---

## 场景三：A/B 测试

同一条 LCEL：

```
Prompt

↓

LLM

↓

Parser
```

一部分用户：

```
Claude
```

另一部分：

```
GPT
```

方便比较不同模型的效果。

---

## 场景四：统一部署

只部署一套代码。

不同环境：

```
Dev

↓

OpenAI

--------------------

Prod

↓

Claude

--------------------

Enterprise

↓

Azure OpenAI
```

通过配置完成切换。

---

# 八、与其他 Runnable 能力的区别

## configurable_alternatives()

**根据配置决定使用哪个 Runnable。**

```
configurable

↓

GPT
```

配置指定什么，就执行什么。

---

## with_fallbacks()

**主 Runnable 失败后自动切换备用 Runnable。**

```
Claude

↓

失败

↓

GPT
```

属于自动容灾。

---

## RunnableBranch

**根据输入数据决定执行哪个 Runnable。**

```
score > 80

↓

GPT

否则

↓

Claude
```

属于数据驱动。

---

## with_retry()

**同一个 Runnable 自动重试。**

```
Claude

↓

失败

↓

Claude

↓

失败

↓

Claude
```

不会切换到其他 Runnable。

---

# 九、能力对比

| 能力                            | 解决的问题             | 谁决定  | 是否自动 |
| ----------------------------- | ----------------- | ---- | ---- |
| `with_retry()`                | 临时失败重试            | 程序   | ✅    |
| `with_fallbacks()`            | 主方案失败后切换备用方案      | 程序   | ✅    |
| `RunnableBranch`              | 根据输入选择不同流程        | 输入数据 | ✅    |
| `configurable_alternatives()` | 根据配置选择不同 Runnable | 运行配置 | ❌    |
| `with_listeners()`            | 生命周期监听            | 程序   | ✅    |

---

# 十、核心总结

可以把这些能力理解为不同维度的增强：

| 能力                            | 一句话理解                  |
| ----------------------------- | ---------------------- |
| `with_retry()`                | **再试一次**（同一个 Runnable） |
| `with_fallbacks()`            | **换备用方案**（失败后自动切换）     |
| `RunnableBranch`              | **根据输入选择方案**           |
| `configurable_alternatives()` | **根据配置选择方案**           |
| `with_listeners()`            | **观察整个执行过程**           |

其中，`configurable_alternatives()` 的核心价值在于：

> **将"使用哪个组件"的决策从业务代码中抽离出来，交给运行时配置，实现同一套 LCEL 链路支持多种 Runnable，实现更好的扩展性、可维护性和部署灵活性。**

《LangChain Runnable 全景图》，把 invoke、batch、stream、RunnableSequence、RunnableParallel、RunnableBranch、RunnableLambda、RunnablePassthrough、RunnableAssign、with_retry、with_fallbacks、with_listeners、configurable_alternatives 等能力放在一张思维导图里，看完基本就能建立完整的 Runnable 知识体系。
