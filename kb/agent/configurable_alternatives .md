configurable_alternatives 是 LangChain Runnable 提供的一个高级能力，用来让同一个 Runnable 可以根据配置切换不同实现。

简单理解就是：

不用改代码，只改配置，就能切换不同的大模型、Prompt、Retriever、工具等。

举个最简单的例子

假设你默认使用 Claude，但有时候想换成 GPT。

不用写：

if model == "claude":
    llm = ChatAnthropic(...)
else:
    llm = ChatOpenAI(...)

而是：

from langchain_core.runnables.utils import ConfigurableField

model = ChatAnthropic(
    model="claude-3-5-sonnet"
).configurable_alternatives(
    ConfigurableField(id="llm"),
    default_key="anthropic",
    openai=ChatOpenAI(model="gpt-4o"),
)

这样：

默认执行：

model.invoke("Hello")

实际上使用的是

Claude

如果运行时指定：

model.with_config(
    configurable={"llm": "openai"}
).invoke("Hello")

就变成：

GPT-4o

代码完全不用改。

它的作用

可以切换很多东西。

例如：

① 切换 LLM
Claude

↓

GPT

↓

Gemini

↓

DeepSeek
② 切换 Prompt

例如：

默认 Prompt

你是客服

配置后

configurable={"prompt":"sales"}

变成

你是销售顾问
③ 切换 Retriever

例如：

Chroma

↓

Pinecone

↓

Milvus

一个配置即可切换。

④ 切换 Embedding
OpenAI

↓

FastEmbed

↓

BGE

↓

VoyageAI
⑤ 切换 Agent

例如：

Simple Agent

↓

ReAct Agent

↓

Tool Calling Agent
官方示意图
             configurable_alternatives

                   llm
                    │
      ┌─────────────┼─────────────┐
      │             │             │
 Claude          GPT-4o       Gemini
      │             │             │
      └─────────────┴─────────────┘

运行时：

configurable={"llm":"gpt"}

即可切换。

为什么需要它？

传统方式：

if xxx:
    use GPT
else:
    use Claude

项目越来越大后，会有很多 if/else，代码难维护。

用了 configurable_alternatives 后：

代码

↓

保持固定

↓

配置决定运行哪个组件

这样更容易维护，也更方便做实验和部署。

和 LCEL 的关系

LCEL（LangChain Expression Language）负责把多个 Runnable 组合成一条执行链：

Prompt
   │
   ▼
LLM
   │
   ▼
Parser

configurable_alternatives 则是让其中某个节点可以动态替换：

Prompt
   │
   ▼
      configurable_alternatives
             │
      ┌──────┴──────┐
      ▼             ▼
   Claude        GPT-4o
      │             │
      └──────┬──────┘
             ▼
          Parser
在实际项目中的典型场景

例如做一个 RAG 知识库：

用户问题
      │
      ▼
 Prompt
      │
      ▼
 configurable_alternatives
      │
 ┌────┴──────────────┐
 │                   │
Claude            GPT-4o
 │                   │
 └────────┬──────────┘
          ▼
 OutputParser
          ▼
     最终回答

测试环境：

configurable={"llm": "gpt"}

生产环境：

configurable={"llm": "claude"}

无需改动链路代码。

总结

configurable_alternatives 的核心价值是把“选择哪个组件”的逻辑从代码中抽离出来，交给运行时配置。

它特别适合：

在 Claude、GPT、Gemini、DeepSeek 等模型之间切换。
在不同 Prompt 模板之间切换。
在不同向量数据库（Chroma、Pinecone、Milvus 等）之间切换。
在不同 Embedding 模型之间切换。
在同一套 LCEL 链路中，根据环境、用户或配置动态选择不同实现，而不需要修改业务代码。
