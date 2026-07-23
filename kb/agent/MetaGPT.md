# MetaGPT 核心设计——一条 Message 的生命周期

学习 MetaGPT 时，很多人第一反应会去研究 **Memory**。

实际上，**Memory 并不是整个框架的核心**。

真正应该理解的是：

> **一条 Message 是如何在整个系统中流转的。**

只有理解了这条链路，才能真正理解 MetaGPT，也更容易理解 LangGraph、CrewAI、AutoGen 等 Agent 框架。

---

# 整体生命周期

```text
Message
    │
    ▼
Environment.publish_message()
    │
    ▼
Role._observe()
    │
    ▼
Memory.add()
    │
    ▼
Role._think()
    │
    ▼
Role._act()
    │
    ▼
publish_message()
```

这就是 MetaGPT 中最重要的一条运行链路。

---

# Step 1：Message（消息）

在 MetaGPT 中，Agent 之间传递的不是字符串，而是 **Message 对象**。

例如：

```text
PM：
请设计登录系统
```

会被封装成：

```python
Message(
    content="请设计登录系统",
    sent_from="PM",
    send_to="Architect",
    cause_by=WritePRD
)
```

一个 Message 不仅包含内容，还记录：

* 消息内容（content）
* 谁发送（sent_from）
* 发给谁（send_to）
* 由哪个 Action 产生（cause_by）

因此，Message 更像一条**结构化事件（Event）**。

---

# Step 2：Environment.publish_message()

所有 Message 都会发送到 **Environment**。

```text
PM
 │
 ▼
Environment
```

Environment 可以理解成：

> **整个 Agent 世界的消息总线（Message Bus）**

它负责：

* 消息广播
* 消息路由
* Agent 之间通信

Agent 不直接调用其他 Agent，而是通过 Environment 交换 Message。

---

# Step 3：Role._observe()

每个 Role 会从 Environment 中读取消息。

流程：

```text
Environment
        │
        ▼
Message Queue
        │
        ▼
Role.observe()
```

此时并不会接收所有消息。

Role 会根据自己的 **Watch List** 进行过滤。

例如：

```text
Engineer

Watch：

WriteDesign
```

那么：

```text
PM 的聊天

×

不会接收
```

而：

```text
Architect 输出的设计

√

会接收
```

Observe 的作用：

> **只接收自己真正关心的消息。**

---

# Step 4：Memory.add()

Observe 完成后：

消息才会进入 Memory。

```text
Observe

↓

Memory.add()
```

注意：

Memory 保存的是：

> **已经观察到（Observed）的消息。**

而不是：

> LLM 的全部输出。

例如：

Memory：

```text
PM：
完成需求

Architect：
完成设计

Engineer：
完成登录模块
```

Memory 的作用：

* 保存历史
* 提供上下文
* 支持后续检索

---

# Step 5：Role._think()

Think 阶段：

不会真正执行任务。

它负责：

> **决定下一步应该做什么。**

例如：

Memory：

```text
Architect：

登录接口设计完成
```

Think：

分析后决定：

```text
下一步：

WriteCode
```

因此：

Think 更像：

> 决策中心（Planner）。

---

# Step 6：Role._act()

Act：

真正开始执行。

例如：

```text
WriteCode
```

Action 内部通常会：

* 调用 LLM
* 调用工具
* 执行业务逻辑

最终生成：

```text
登录模块代码
```

---

# Step 7：再次发布 Message

Action 完成后：

不会直接结束。

而是：

再次生成新的 Message。

例如：

```text
Engineer：

登录模块开发完成
```

随后：

```text
publish_message()

↓

Environment

↓

其他 Agent Observe
```

整个流程重新开始。

因此：

整个 MetaGPT 就形成了一套持续循环的消息驱动系统。

---

# 整个生命周期示意图

```text
                Message
                    │
                    ▼
     Environment.publish_message()
                    │
                    ▼
           Message Queue
                    │
                    ▼
             Role.observe()
                    │
                    ▼
              Memory.add()
                    │
                    ▼
              Role.think()
                    │
                    ▼
               Role.act()
                    │
                    ▼
          Generate Message
                    │
                    ▼
     Environment.publish_message()
                    │
             下一轮 Observe
```

---

# 四个最核心的概念

整个 MetaGPT 都围绕四个核心对象展开。

| 核心对象                       | 职责                               |
| -------------------------- | -------------------------------- |
| **Message**                | Agent 之间的数据载体，保存内容及来源等元信息。       |
| **Environment**            | 消息总线，负责广播、路由和协调 Agent 通信。        |
| **Memory**                 | 保存已观察到的 Message，为 Think 提供历史上下文。 |
| **State / Think / Action** | 决定 Agent 当前状态、下一步计划以及具体执行逻辑。     |

---

# 一句话总结

MetaGPT 并不是多个 Agent 互相调用，而是多个 Agent **围绕 Message 进行协作**：

```text
Message
    ↓
Environment（消息总线）
    ↓
Observe（接收并过滤）
    ↓
Memory（保存上下文）
    ↓
Think（决定下一步）
    ↓
Action（执行任务）
    ↓
产生新的 Message
    ↓
再次进入 Environment
```

理解了这条消息生命周期，就理解了 MetaGPT 的设计思想。实际上，**CrewAI、AutoGen、LangGraph** 等主流多 Agent 框架也都采用了类似的理念：以 **Message** 作为通信载体，以 **State** 管理执行阶段，以 **Memory** 提供上下文，以 **Environment（或运行时）** 组织整个协作流程。不同框架的实现细节不同，但核心思想是一致的。
