# Claude Code 接入 LiteLLM 原理解析

> 本文不是安装教程，而是帮助理解 **为什么要这样配置**、**请求是如何流转的**、**LiteLLM 在整个系统中的作用**。

---

# 一、整体架构

正常情况下，Claude Code 会直接调用 Anthropic 官方接口。

```text
Claude Code
      │
      ▼
Anthropic API
      │
      ▼
Claude 模型
```

Pacvue 内部则增加了一层 **LiteLLM Gateway**：

```text
Claude Code
      │
      ▼
LiteLLM Gateway
(llm-gateway-test.pacvue.com)
      │
      ▼
LiteLLM
      │
 ┌────┼─────┬─────┐
 ▼    ▼     ▼     ▼
Claude GPT Gemini DeepSeek ...
```

因此：

> Claude Code 并不知道自己连接的是公司网关，它仍然认为自己在访问 Anthropic API。

LiteLLM 负责接收所有请求，并转发到真正的模型。

---

# 二、LiteLLM 是什么？

LiteLLM 可以理解为：

> **AI 模型统一网关（LLM Gateway）**

作用类似于 API Gateway。

传统调用：

```text
应用
 │
 ▼
OpenAI
```

使用 LiteLLM 后：

```text
应用
 │
 ▼
LiteLLM
 │
 ├── OpenAI
 ├── Claude
 ├── Gemini
 ├── DeepSeek
 └── Azure OpenAI
```

LiteLLM 对外提供统一接口，对内管理多个模型。

---

# 三、为什么要接入 LiteLLM？

企业不会让所有开发者直接访问 Anthropic。

原因主要有以下几点。

---

## 1. 统一 API Key

开发者只需要：

```text
sk-xxxxxxxx
```

即可。

不用分别申请：

* Anthropic Key
* OpenAI Key
* Gemini Key

公司统一管理。

---

## 2. 成本统计

LiteLLM 可以记录：

```text
用户A

↓

Claude

↓

Token
↓

Cost
```

例如：

```text
张三
Claude Opus
120000 Tokens
$6.82
```

月底即可统计：

* 每个人花了多少钱
* 哪个项目成本最高
* 哪个模型最贵

---

## 3. 模型统一管理

例如：

今天：

```text
opusplan

↓

Claude Opus
```

明天：

```text
opusplan

↓

Claude Sonnet
```

或者：

```text
opusplan

↓

GPT-5
```

Claude Code 无需升级。

开发者也不用修改代码。

---

## 4. 日志与审计

所有请求都会经过 LiteLLM：

```text
Prompt

↓

LiteLLM

↓

Database
```

因此可以：

* Debug
* Audit
* 排查问题
* 查看调用历史

---

## 5. 限流

例如：

```text
每分钟

20 Requests
```

避免：

```text
死循环

↓

大量请求

↓

烧掉大量费用
```

---

## 6. Failover（故障切换）

例如：

```text
Claude

↓

异常

↓

GPT

↓

成功
```

或者：

```text
Claude

↓

Azure Claude
```

整个切换过程开发者无感知。

---

# 四、环境变量解析

Linux：

```bash
export ANTHROPIC_AUTH_TOKEN=<API_KEY>
```

Claude Code 默认读取：

```text
ANTHROPIC_AUTH_TOKEN
```

因此无需修改源码。

只是把：

Anthropic 官方 Key

替换为

公司 LiteLLM Key。

---

另一个变量：

```bash
export CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1
```

作用：

关闭 Claude Code 的实验功能。

企业环境通常希望：

* 接口稳定
* 行为一致
* 避免 Beta 功能导致兼容问题

---

# 五、为什么修改 Base URL？

配置：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL":
      "https://llm-gateway-test.pacvue.com"
  }
}
```

正常情况下：

Claude Code 请求：

```text
https://api.anthropic.com/v1/messages
```

修改后：

```text
https://llm-gateway-test.pacvue.com/v1/messages
```

也就是说：

> **只修改 Base URL，不修改 Claude Code 本身。**

所有请求都会进入 LiteLLM。

---

# 六、启动 Claude Code

启动：

```bash
claude
```

首次启动：

```text
Use Custom API Key?

Yes
```

选择：

```text
Yes
```

即可。

---

# 七、为什么选择 opusplan？

文档建议：

```text
/model

↓

opusplan
```

这里的：

```text
opusplan
```

不是 Anthropic 官方模型名称。

而是：

LiteLLM 注册的模型名称。

例如：

```text
opusplan

↓

Claude Opus
```

或者：

```text
opusplan

↓

Claude Opus Thinking
```

甚至：

```text
opusplan

↓

多个模型 Routing
```

开发者无需关心真正调用哪个模型。

---

# 八、为什么可以查询模型？

文档中：

```bash
curl https://llm-gateway-test.pacvue.com/v1/models
```

LiteLLM 会返回：

```json
{
  "data":[
    {
      "id":"opusplan"
    },
    {
      "id":"sonnet"
    },
    {
      "id":"gpt-5"
    }
  ]
}
```

Claude Code：

```text
/model
```

看到的：

就是这里注册的模型。

---

# 九、Windows 配置说明

Windows 没有：

```text
~/.bashrc
```

因此：

直接写：

```text
~/.claude/settings.json
```

例如：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL":
      "https://llm-gateway-test.pacvue.com",

    "ANTHROPIC_API_KEY":
      "YOUR_API_KEY"
  }
}
```

效果与 Linux 相同。

---

# 十、CC GUI 是什么？

CC GUI：

不是新的 AI。

只是：

Claude Code 的 GUI。

结构：

```text
IDEA

↓

CC GUI

↓

Claude Code SDK

↓

LiteLLM

↓

Claude
```

因此：

GUI 只是方便：

* 上传图片
* 上传文件
* 查看聊天记录

底层仍然调用 Claude Code。

---

# 十一、完整调用流程

```text
                Claude Code
                     │
                     │ 读取环境变量
                     ▼
      ANTHROPIC_AUTH_TOKEN
      ANTHROPIC_BASE_URL
                     │
                     ▼
       https://llm-gateway-test.pacvue.com
                     │
                     ▼
              LiteLLM Gateway
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 Claude Opus      Claude Sonnet     GPT / Gemini ...
      │
      ▼
   返回结果
      │
      ▼
  Claude Code CLI
```

---

# 十二、核心知识总结

| 配置项                                      | 作用                                    |
| ---------------------------------------- | ------------------------------------- |
| `ANTHROPIC_AUTH_TOKEN`                   | Claude Code 使用的认证 Token（公司发放）         |
| `ANTHROPIC_BASE_URL`                     | 将 Claude Code 的请求重定向到 LiteLLM Gateway |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | 关闭实验功能，保证企业环境稳定                       |
| `opusplan`                               | 公司在 LiteLLM 中注册的模型名称，由网关决定最终调用的底层模型   |

---

# 十三、一句话理解整个流程

```text
Claude Code
      │
      ▼
读取 API Key
      │
      ▼
读取 Base URL
      │
      ▼
请求发送到 LiteLLM Gateway
      │
      ▼
LiteLLM 选择实际模型
      │
      ▼
Claude / GPT / Gemini 等模型执行
      │
      ▼
返回结果给 Claude Code
```

**总结：** Claude Code 本身并没有被修改，真正发生变化的是它连接的目标地址。通过将 `ANTHROPIC_BASE_URL` 指向 Pacvue 的 LiteLLM Gateway，并使用公司统一的 API Key，所有模型调用都经过企业网关，从而实现统一认证、成本统计、模型路由、日志审计、限流以及故障切换等企业级能力。














第三步：启动
1
claude
​
首次启动会提示是否使用自定义 API Key，选择 Yes。

设置模型为opusplan
image-20260402-095353.png


然后可以使用

故障排查
每次启动都要求登录
确认环境变量是否生效：

1
  env | grep ANTHROPIC
​
应输出二行。如果缺失，检查 ~/.bashrc 是否正确写入，然后 source ~/.bashrc。

模型不存在
确认 settings.json 中的 model 和 smallModel 名称与上方可用模型一致。或查询网关已注册模型：

1
2
curl -s https://llm-gateway-test.pacvue.com/v1/models \
  -H "Authorization: Bearer <你的API Key>" | python3 -m json.tool
​




Windows
green apple 

1. 安装 Claude Code（在User目录下安装）
1
PowerShell执行：
​
irm https://claude.ai/install.ps1 | iex

image-20260324-023508.png
如果这里显示claude启动不了

把下面这个路径加入到你的用户 PATH：

C:\Users\XXXXX\.local\bin

image-20260401-091937.png


2. 创建配置文件
在 C:\\Users\\<用户名>\\.claude\\settings.json 中写入以下内容：

1
2
3
4
5
6


{
  "env": {
    "ANTHROPIC_BASE_URL": "https://llm-gateway-test.pacvue.com",
    "ANTHROPIC_API_KEY": "YOUR_API_KEY"
  }
}
​
💡 配置文件路径即 ~/.claude/settings.json，可通过 $PROFILE 查看当前用户目录。

image-20260324-023636.png
3.写入 PowerShell Profile 永久环境变量
查看 Profile 路径：

echo $PROFILE



追加环境变量到 Profile：

1
2
3
4
5
6
Add-Content -Path $PROFILE -Value @"

# Claude Code 环境变量
`$env:ANTHROPIC_BASE_URL="https://llm-gateway-test.pacvue.com"
`$env:CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1"
"@
​
3.1 如果 power shell 路径走不通，可以尝试 git bash 的方式，启动 Claude 之前先通过 export 的方式把配置修改为公司的配置


1
2
3

export ANTHROPIC_BASE_URL=https://llm-gateway-test.pacvue.com
export CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1
​
c6dd8d82-e1c2-40ec-88f5-c0538376b4f5-20260401-100503.png




4. 启动 Claude Code
1
claude
​
image-20260324-024655.png
设置模型为opusplan
image-20260402-095353.png


然后可以使用



IntelliJ IDEA 插件
idea 有一个 Claude Code CLI 套壳插件叫做 CC GUI，它能够提供一套 UI 让你方便的上传图片、文件等附件，要比纯 CLI 更方便。

在 idea 的插件市场搜索并安装 CC GUI

image-20260407-022853.png
安装 Claude Code SDK 

image-20260409-083402.png
添加一个自定义 provider 

image-20260409-084009.png
自定义 provider 的设置中配置公司的 URL key 等作为参数

05ceda58-45c2-4c22-9446-e4bea579c0e9.png
image-20260409-083702.png
启用这个自定义的 provider 

image-20260409-083900.png


测试是否有反应，然后开始使用

image-20260407-023314.png


Related content

Claude Code 安装
Mengchen Wang
LiteLLM项目调研报告
Zack Shang
LiteLLM 对接指南
Zack Shang
raising hands
Cursor接入LiteLLM
Zack Shang

Add a comment


5
