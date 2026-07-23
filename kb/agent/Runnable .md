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
