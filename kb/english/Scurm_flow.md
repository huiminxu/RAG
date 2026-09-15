# Engineering Meeting English Notebook

## Meeting #1 – Backlog Refinement, Q4 Planning, Technical Initiatives & Scrum Process

这场会议的信息量很大，和前面的 Daily Standup 不太一样，更接近 **Backlog Refinement + Roadmap Discussion**。最值得学习的是：**产品需求不足、技术驱动 Sprint、Q4 规划、需求拆分、技术调研、跨团队依赖、测试范围，以及“这个会议到底有没有必要”的 Scrum 流程讨论**。会议一开始就在确认下个 Sprint 是否有新的产品需求。

---

# Topic 1. Not Enough Product Requirements

## 📌 Meeting Background

The team discussed an ongoing problem: there were not enough incoming product requirements to fill the sprint. In previous sprints, product-driven work represented only a relatively small portion of the team's development capacity, so much of the upcoming sprint would again be driven by technical initiatives. 

## 💬 Original Chinese

> 我们可能这个 Team 遇到的一个问题，就是缺少足够的产品需求来支撑。

## 🇺🇸 Natural English

> One challenge we're facing as a team is that we don't have enough product requirements to fill the sprint.

### Alternative Expressions

* We don't have enough product-driven work in the pipeline.
* Most of our current backlog is technically driven.
* We're somewhat light on product requirements right now.

### ⭐ 很自然

> **We're a little light on product-driven work right now.**

这里 **light on** = 某种东西比较少。

---

# Topic 2. Technical-driven Sprint

## 💬 Original Chinese

> 这一次 Sprint 主要还是技术这边来驱动。

## 🇺🇸 Natural English

> This sprint will mainly be driven by technical initiatives. 

### Alternative Expressions

* This will be a mostly engineering-driven sprint.
* Most of the work this sprint will be technical improvements.
* The sprint is weighted more toward technical work than product features.

### 🧠 Vocabulary

**product-driven** — 产品需求驱动

**engineering-driven** — 工程/技术驱动

**technical initiative** — 技术改造/技术项目

---

# Topic 3. Existing Platforms vs. New Platforms

## 📌 Meeting Background

The team clarified the MCP strategy. Q4 would not prioritize expansion to completely new platforms such as Target or Best Buy, but MCP work for platforms already supported by the product—especially TikTok and Walmart—would continue. 

## 💬 Original Chinese

> Target、Best Buy 这种我们完全没有接入的平台先不考虑，但是 TikTok 和 Walmart 还是会继续做。

## 🇺🇸 Natural English

> For now, we're not planning to expand into completely new platforms like Target or Best Buy, but we'll continue investing in TikTok and Walmart.

### Alternative Expressions

* New platform expansion is not a priority for Q4.
* We'll focus on platforms we already support.
* TikTok and Walmart will remain key areas of investment.

### ⭐ Useful

> **X is not a priority for Q4.**

> **We'll continue investing in X.**

---

# Topic 4. Research First, Then Decide Whether to Build

## 💬 Original Chinese

> 先让 Dev 去调研它的接口，然后再看能不能做 MCP。

## 🇺🇸 Natural English

> Let's have engineering investigate the API first, and then decide whether it makes sense to build an MCP around it. 

### Alternative Expressions

* Let's validate the technical feasibility first.
* We should research the API before committing to implementation.
* Let's understand the capabilities before deciding on the solution.

### ⭐⭐⭐ 很值得背

> **Let's validate the technical feasibility first.**

**technical feasibility** = 技术可行性。

---

# Topic 5. Report Balance API Improvement

## 📌 Meeting Background

The current Report Balance API response could mislead users into thinking `balance` represented the number of reports they had remaining. The proposed improvement was to clarify what `balance` means and also return the user's actual remaining usage. 

## 💬 Original Chinese

> 用户会误以为这个 Balance 是目前剩余的 Report 数量。

## 🇺🇸 Natural English

> Users may mistakenly interpret the balance as the number of reports they have remaining.

### Alternative Expressions

* The current response is somewhat misleading.
* The meaning of `balance` isn't clear enough.
* We should make the API response more explicit.

---

## 💬 Original Chinese

> 我们可以说明这个 Balance 指的是什么，并且把用户剩余的使用次数返回给用户。

## 🇺🇸 Natural English

> We can clarify what the balance represents and return the user's remaining usage as a separate value.

### ⭐ Useful

> **make the response more explicit**

= 让返回结果表达得更明确。

---

# Topic 6. Integrating a New Search Volume Model

## 📌 Meeting Background

The Data Science team had developed a new Search Volume model with higher accuracy. The Research team needed to integrate the new dataset and update the API layer so it could read from the new table. 

## 💬 Original Chinese

> Data Science Team 做了一个 Search Volume 的新模型，准确率会更高。

## 🇺🇸 Natural English

> The Data Science team has developed a new Search Volume model with improved accuracy.

---

## 💬 Original Chinese

> 我们需要把这个新的模型接进来。

## 🇺🇸 Natural English

> We need to integrate the new model into our existing data pipeline.

### Alternative Expressions

* We need to wire the new model into our system.
* The API layer needs to consume the new dataset.
* We'll need to migrate the API to the new data source.

### 🧠 Vocabulary

**data pipeline** — 数据管道

**data source** — 数据源

**consume data** — 读取/消费数据

**integrate** — 集成

---

# Topic 7. Brand Data Normalization

## 📌 Meeting Background

Brand data currently contained inconsistent capitalization because users could enter brand names freely. For example, `abc` and `Abc` could be treated as different brands even though they represented the same brand. The solution required both new normalization logic and historical-data processing. 

## 💬 Original Chinese

> 在我们的平台里面，它是两个品牌，但实际上它是一个品牌。

## 🇺🇸 Natural English

> Our system currently treats them as two different brands even though they're actually the same brand.

---

## 💬 Original Chinese

> 我们现在需要把这个数据做处理，这涉及到新逻辑的修改，还有历史数据的处理。

## 🇺🇸 Natural English

> We need to normalize the brand data, which involves both updating the logic and cleaning up the historical data.

### ⭐ 核心词

**normalize data**

= 对数据进行标准化/归一化。

**clean up historical data**

= 清理历史数据。

---

# Topic 8. Investigating Abnormal API Usage

## 📌 Meeting Background

The team proposed using logs to identify unusual API usage patterns. For example, if most users call an API around 50 times per day but certain accounts make hundreds or thousands of calls, those accounts may require further investigation. 

## 💬 Original Chinese

> 我们可以通过日志去分析哪些用户调用 API 比较异常。

## 🇺🇸 Natural English

> We can analyze the logs to identify users with abnormal API usage patterns.

### Alternative Expressions

* We should look for suspicious usage patterns.
* We can identify outliers based on request volume.
* Let's analyze traffic patterns for unusual behavior.

### 🧠 Vocabulary

**usage pattern** — 使用模式

**outlier** — 异常值

**suspicious traffic** — 可疑流量

---

## 💬 Original Chinese

> 正常一天可能 50 次，有些用户几百次、上千次，这就明显有问题。

## 🇺🇸 Natural English

> If normal usage is around 50 calls per day but some accounts are making hundreds or thousands, that's a clear anomaly.

---

# Topic 9. Adding Protection Against Suspicious Traffic

## 💬 Original Chinese

> 如果检测到某些账号请求接口异常，可以加验证码之类的东西做防护。

## 🇺🇸 Natural English

> If we detect suspicious request patterns from certain accounts, we could introduce safeguards such as CAPTCHA challenges. 

### Alternative Expressions

* We need safeguards against abusive traffic.
* We could introduce additional verification for suspicious accounts.
* We may need application-level protection.

### ⭐ 高频

> **We need safeguards against abusive traffic.**

---

# Topic 10. Credential Scanning

## 💬 Original Chinese

> 默认分支上还是有这种漏洞，我们需要检查代码，把凭据移除掉。

## 🇺🇸 Natural English

> We still have exposed credentials on the default branch, so we need to scan the codebase and remove them. 

### Alternative Expressions

* We need to remove hard-coded credentials.
* Let's scan the repository for exposed secrets.
* Credentials shouldn't be committed to the repository.

### 🧠 Vocabulary

**credential** — 凭据

**secret** — 密钥/敏感信息

**hard-coded credential** — 写死在代码里的凭据

**exposed secret** — 已暴露的密钥

---

# Topic 11. Requirement Needs Product / UX Input

## 📌 Meeting Background

Some sponsored-brand data existed but was not displayed in the UI. Before implementation, the team needed product/design input on where the field should appear and how it should be labeled. 

## 💬 Original Chinese

> 这个地方需要 PM 进来，因为涉及到增加字段还是怎么展示这个数据。

## 🇺🇸 Natural English

> We need Product involved here because we need to decide how this data should be presented in the UI.

### Alternative Expressions

* We need UX input on this.
* The presentation still needs to be defined.
* We need Product to clarify the expected UI behavior.

---

# Topic 12. Shop Ads Commission Rate

## 📌 Meeting Background

The team discussed adding a second commission-rate field to the Messenger flow. The implementation itself appeared relatively small, but the exact placement and labeling required UX/design input, which had already been prepared. 

## 💬 Original Chinese

> 页面上再加一个 Shop Ads Commission Rate 的配置就可以了。

## 🇺🇸 Natural English

> We just need to add a Shop Ads commission-rate field to the existing form.

### Alternative Expressions

* This should be a relatively small UI change.
* We need one additional form field.
* The main question is where and how to display it.

---

## 💬 Original Chinese

> 具体加到哪里、字段怎么显示名字，还是需要设计。

## 🇺🇸 Natural English

> We still need design input on where to place the field and how to label it.

### ⭐ Useful

**label a field**

= 给字段命名/显示 Label。

---

# Topic 13. Upgrade or Remove Broken AI Models

## 💬 Original Chinese

> 能升级的升级，如果不能升级，就把它移除掉。

## 🇺🇸 Natural English

> We should upgrade the models where possible and remove the ones we can no longer support. 

### Alternative Expressions

* Upgrade what we can and deprecate the rest.
* Unsupported models should be removed.
* We shouldn't keep options that are currently broken.

---

# Topic 14. Centralizing AI Keys & Tracking Usage

## 📌 Meeting Background

AI keys were currently scattered across different tools. The proposed refactor was to consolidate them into one key while tracking which application initiated each request, which model was used, and how many input/output tokens were consumed. 

## 💬 Original Chinese

> 我们现在 Token 比较分散，每个工具调用 AI 都有一个独立的 Key。

## 🇺🇸 Natural English

> Our AI credentials are currently fragmented, with different tools using separate API keys.

---

## 💬 Original Chinese

> 我们想把 Key 合并成一个，但是应用自己记录每次调用用了什么模型、输入多少 Token、输出多少 Token。

## 🇺🇸 Natural English

> We'd like to consolidate the API keys while tracking the model, calling application, input tokens, and output tokens for each request.

### 🧠 Vocabulary

**consolidate** — 整合

**usage tracking** — 使用量追踪

**token consumption** — Token 消耗

---

# Topic 15. Technical Tickets Need Better Testing Details

## 📌 Meeting Background

Because many planned items were technical stories, QA could not infer the testing requirements from ticket titles alone. The team agreed that the scope and testing approach should be documented more clearly before planning. 

## 💬 Original Chinese

> 如果需要测试的话，把范围和怎么测写在 Ticket 里面。

## 🇺🇸 Natural English

> If QA needs to be involved, please document the testing scope and approach in the ticket.

### Alternative Expressions

* The ticket should clearly define what needs to be tested.
* Please include the expected regression scope.
* Technical tickets need enough context for QA to estimate the effort.

### ⭐ 很值得背

> **Please document the testing scope and approach in the ticket.**

---

# Topic 16. A Technical Migration and a Product Improvement Should Be Separate Stories

## 📌 Meeting Background

The team realized that a new TikTok API did more than support the technical OpenID migration: it also replaced an inaccurate existing method for determining creator level and quota. Because this had independent business value, the team decided to create a separate user story.  

## 💬 Original Chinese

> 这个应该拆出来，它和表结构改造是两回事。

## 🇺🇸 Natural English

> I think we should split this out into a separate story because it's independent of the underlying migration.

### Alternative Expressions

* This has standalone business value.
* Let's separate the technical migration from the product improvement.
* These are really two different pieces of work.

### ⭐⭐⭐ 非常好的项目表达

> **This has standalone business value, so it should be tracked separately.**

---

# Topic 17. Research Before Committing to MCP Implementation

## 💬 Original Chinese

> 我只是先研究一下有没有这种数据，具体怎么做还要再想，不急着实现 MCP。

## 🇺🇸 Natural English

> For now, I just want to confirm whether the data is available. We don't need to commit to an MCP implementation yet. 

### Alternative Expressions

* This is exploratory work for now.
* Let's validate the data availability first.
* We're not committing to implementation yet.

### 🧠 Vocabulary

**exploratory work** = 探索性工作

---

# Topic 18. Backlog Refinement vs. Sprint Planning

## 📌 Meeting Background

A substantial part of the meeting discussed whether Backlog Refinement and Sprint Planning were both necessary given the team's relatively small number of product requirements. The distinction was clarified: refinement is used to clarify candidate requirements, while planning considers actual team capacity and commits to the final sprint scope. 

## 💬 Original Chinese

> Planning 会议到底是在 Plan 什么？

## 🇺🇸 Natural English

> What exactly are we trying to accomplish in sprint planning?

---

## 💬 Original Chinese

> Planning 会根据现有人力，看最终能做 15 个还是 18 个，确定 Sprint 最终交付目标。

## 🇺🇸 Natural English

> During sprint planning, we look at the team's actual capacity and decide what we can realistically commit to delivering.

### ⭐⭐⭐ 必背

> **What can we realistically commit to?**

这就是 Sprint Planning 最核心的英文句型。

---

# Topic 19. Meeting Efficiency vs. Transparency

## 📌 Meeting Background

The team openly debated the value of Scrum ceremonies. One perspective was that long recurring meetings seemed inefficient; another emphasized that Scrum primarily improves transparency, predictability, and alignment rather than simply making developers work faster. 

## 💬 Original Chinese

> 我希望 Scrum 能够提高效率，如果每周都花 75 分钟开大会，我觉得不太效率。

## 🇺🇸 Natural English

> My expectation is that Scrum should help us work more efficiently. If we're spending 75 minutes in a large meeting every Monday, I'm not sure we're getting enough value from that time.

### ⭐ 这个翻译比直接说 “It's inefficient” 更成熟

> **I'm not sure we're getting enough value from that time.**

既表达质疑，又不会显得攻击性太强。

---

## 💬 Original Chinese

> Scrum 不是为了提高开发效率，而是为了提高透明度。

## 🇺🇸 Natural English

> The primary goal of Scrum isn't necessarily to make development faster; it's to improve transparency and alignment.

### Useful Vocabulary

* **transparency** — 透明度
* **alignment** — 信息/目标对齐
* **predictability** — 可预测性
* **visibility** — 可见性

---

# Topic 20. Meetings Don't Need to Use the Entire Timebox

## 💬 Original Chinese

> 如果 30 分钟能够讲清楚，没有疑问，那 30 分钟结束也没关系。

## 🇺🇸 Natural English

> If we can cover everything in 30 minutes and there are no open questions, there's no reason to use the full time slot. 

### Alternative Expressions

* We don't need to fill the entire timebox.
* We can end early if we've covered everything.
* The meeting should be as long as necessary, but no longer.

### ⭐ 推荐

> **We don't need to fill the entire timebox.**

---

# Topic 21. Prepare the Next Sprint in Advance

## 💬 Original Chinese

> 大家可以提前一个星期准备好下个 Sprint 要做的内容。

## 🇺🇸 Natural English

> We should prepare the next sprint's work at least a week in advance. 

### Alternative Expressions

* Let's prepare upcoming work ahead of time.
* We should front-load requirement clarification.
* Engineers can start reviewing documentation before the sprint begins.

---

# Topic 22. Try Combining the Meetings

## 📌 Meeting Background

Given the team's current workload and relatively low volume of product requirements, the team decided to experiment with combining Backlog Refinement and Sprint Planning for now, while leaving open the option of bringing refinement back separately if Q4 became busier. 

## 💬 Original Chinese

> 我们循序渐进地来，先把 Refinement 跟下周的 Planning 放一起试试看。

## 🇺🇸 Natural English

> Let's take an incremental approach and try combining refinement with sprint planning for now.

### Alternative Expressions

* Let's experiment with a combined meeting.
* We can try this format and see how it works.
* If it doesn't work well, we can revisit the process.

### ⭐ 很实用

> **Let's try it and see how it works.**

---

# Topic 23. Adapt the Process to the Team

## 💬 Original Chinese

> 我们根据现在 Team 的情况来调整，大家也是在探索一种新的方式。

## 🇺🇸 Natural English

> We can adapt the process to our team's current needs. We're still experimenting with what works best for us. 

### Alternative Expressions

* The process doesn't have to be one-size-fits-all.
* Let's tailor the process to the team's needs.
* We can iterate on the process as the team evolves.

### ⭐ 很自然

> **Let's iterate on the process.**

不仅代码可以 iterate，团队流程也可以。

---

# 📖 Grammar & Expression Notes

### 1. “产品需求比较少”

> **We're light on product-driven work.**

> **We don't have many product requirements in the pipeline.**

---

### 2. “先调研，不承诺开发”

> **Let's investigate this first before committing to implementation.**

---

### 3. “技术可行性”

> **technical feasibility**

> Let's validate the technical feasibility first.

---

### 4. “数据标准化”

> **normalize the data**

注意这里比 `standardize` 更贴近数据处理。

---

### 5. “这个需求拆出来”

> **split this out into a separate story**

---

### 6. “独立业务价值”

> **standalone business value**

---

### 7. “实际能承诺多少”

> **What can we realistically commit to?**

---

### 8. “会议有没有价值”

比：

> Is this meeting useful?

更成熟：

> **Are we getting enough value from this meeting?**

---

### 9. “不用开满一个小时”

> **We don't need to fill the entire timebox.**

---

### 10. “流程根据团队调整”

> **Let's tailor the process to the team's needs.**

---

# ⭐ Shadowing Practice

这场会议建议重点练 **Planning / Refinement** 英语：

> **We're a little light on product-driven work right now.**

> **This sprint will mainly be driven by technical initiatives.**

> **Let's validate the technical feasibility first.**

> **We don't need to commit to implementation yet.**

> **We need to integrate the new model into our existing data pipeline.**

> **We need to normalize the brand data.**

> **Let's analyze the logs for unusual usage patterns.**

> **We need Product involved here.**

> **Please document the testing scope and approach in the ticket.**

> **This has standalone business value, so it should be tracked separately.**

> **What can we realistically commit to?**

> **I'm not sure we're getting enough value from that time.**

> **We don't need to fill the entire timebox.**

> **Let's try combining the two meetings and see how it works.**

> **Let's tailor the process to the team's needs.**

---

# 📚 Today's Vocabulary

| Expression                    | 中文        |
| ----------------------------- | --------- |
| **product-driven**            | 产品驱动      |
| **engineering-driven**        | 技术驱动      |
| **in the pipeline**           | 已进入规划/待处理 |
| **technical initiative**      | 技术项目      |
| **technical feasibility**     | 技术可行性     |
| **data pipeline**             | 数据管道      |
| **normalize**                 | 数据标准化     |
| **historical data**           | 历史数据      |
| **usage pattern**             | 使用模式      |
| **outlier**                   | 异常值       |
| **safeguard**                 | 防护措施      |
| **exposed credential**        | 暴露的凭据     |
| **consolidate**               | 整合        |
| **standalone business value** | 独立业务价值    |
| **exploratory work**          | 探索性工作     |
| **realistically commit to**   | 实际能够承诺完成  |
| **transparency**              | 透明度       |
| **alignment**                 | 对齐        |
| **predictability**            | 可预测性      |
| **timebox**                   | 会议/任务限定时间 |
| **tailor**                    | 根据需要调整    |
| **iterate on the process**    | 持续迭代流程    |

## ⭐ 今天最值得背的 10 句

> **We're a little light on product-driven work right now.**

> **This sprint will mainly be driven by technical initiatives.**

> **Let's validate the technical feasibility first.**

> **We don't need to commit to implementation yet.**

> **Please document the testing scope and approach in the ticket.**

> **This has standalone business value, so it should be tracked separately.**

> **What can we realistically commit to?**

> **I'm not sure we're getting enough value from that time.**

> **We don't need to fill the entire timebox.**

> **Let's tailor the process to the team's needs.**

# Engineering Meeting English Notebook

## Meeting #2 – Backlog Refinement, MCP Requirement Clarification & Sprint Preparation

这场会议更偏 **Backlog Refinement + Requirement Clarification**。最值得学习的是：**介绍 Refinement 的目的、确认 Sprint 范围、研究型 Story、MCP Tool 边界、技术可行性、Owner 分配、分页设计，以及什么时候把讨论移到小范围会议里**。会议一开始也明确了，这次 Backlog Refinement 的目标，是把原来零散的小会集中起来，提前澄清下个 Sprint 要做的内容。

---

# Topic 1. Explaining the Purpose of Backlog Refinement

## 📌 Meeting Background

The team was just starting to adopt a more structured Scrum rhythm. Instead of having separate small meetings for every requirement, Backlog Refinement would be used to review upcoming work together, clarify open questions, identify dependencies, and prepare the team for Sprint Planning. 

## 💬 Original Chinese

> 我们希望通过这些会议，把以前很零散的东西集中在某一个会议里面解决。

## 🇺🇸 Natural English

> We want to use these meetings to consolidate the discussions that used to happen across many separate meetings.

### Alternative Expressions

* We want to centralize requirement discussions.
* Instead of scheduling multiple ad hoc meetings, we'll review the upcoming work together.
* The goal is to clarify requirements before the sprint starts.

### ⭐ 推荐

> **The goal is to clarify the upcoming work before the sprint starts.**

---

## 💬 Original Chinese

> Backlog Refining 就是提前了解一下我们下个 Sprint 要做哪些。

## 🇺🇸 Natural English

> Backlog refinement gives us a chance to review and clarify the work we're considering for the next sprint.

### ⭐ 注意

Backlog Refinement 不等于：

> decide everything for the sprint

更准确的是：

> **review and clarify candidate work**

真正最终承诺范围通常是在 Sprint Planning。

---

# Topic 2. Product Requirements Are Not Ready Yet

## 📌 Meeting Background

The PM side did not have new requirements ready for the first sprint. Some product work was still under investigation, so the team planned to fill the upcoming sprint with MCP work, technical research, and engineering improvements. 

## 💬 Original Chinese

> 产品这边正在进行的需求都还在调研中。

## 🇺🇸 Natural English

> The product requirements are still in the research phase.

### Alternative Expressions

* The product work isn't ready for implementation yet.
* Product is still validating the requirements.
* Those requirements are still being explored.

---

## 💬 Original Chinese

> MCP、技术调研、技术优化这些可以填满接下来 14 天要做的内容。

## 🇺🇸 Natural English

> We can fill the upcoming sprint with MCP work, technical research, and engineering improvements.

### 🧠 Vocabulary

* **technical research** — 技术调研
* **engineering improvement** — 技术优化
* **implementation-ready** — 已具备开发条件

---

# Topic 3. Prioritizing the High-priority Stories

## 📌 Meeting Background

There were around 20 stories and technical stories in the backlog. The plan was to focus on the high-priority items first in the next sprint. 

## 💬 Original Chinese

> 下一个 Sprint，我们先把高等级的安排起来。

## 🇺🇸 Natural English

> For the next sprint, let's start with the highest-priority items.

### Alternative Expressions

* Let's prioritize the high-priority stories first.
* We'll work through the backlog based on priority.
* The high-priority items should come first.

### ⭐ 高频

> **Let's prioritize the highest-impact items first.**

如果强调“业务影响”，`highest-impact` 比单纯 `high-priority` 更自然。

---

# Topic 4. Engineers Can Pick Work Based on Expertise or Interest

## 💬 Original Chinese

> 大家可以选择自己领域比较熟悉的，或者比较感兴趣的。

## 🇺🇸 Natural English

> Feel free to pick up work that's either in your area of expertise or something you're interested in.

### Alternative Expressions

* Pick something that aligns with your experience.
* Feel free to take ownership of something you're interested in.
* You don't have to stay strictly within your usual role.

### 🧠 Vocabulary

**area of expertise** = 擅长领域

**take ownership of** = 主动负责

---

# Topic 5. Research-heavy Story

## 📌 Meeting Background

The Amazon Seller Account Health MCP story was not a fully specified PM story. It had a stronger research component: the owner first needed to understand the Amazon report, validate whether the required data was available, and then define the MCP implementation. 

## 💬 Original Chinese

> 这个 Story 跟 PM 的 Story 不太一样，会有一点研究的特性。

## 🇺🇸 Natural English

> This story is a little different from a typical product story because it includes a significant research component.

### Alternative Expressions

* This is more exploratory than implementation-ready.
* There's still some discovery work involved.
* The owner needs to validate the feasibility first.

### ⭐ 很值得背

> **This is still somewhat exploratory.**

---

## 💬 Original Chinese

> Owner 需要先研究一下这个 Report 是什么，再看我们能不能提供这样的数据能力。

## 🇺🇸 Natural English

> The owner first needs to understand the report and then validate whether we can expose the same data through our MCP.

### ⭐ 高频

> **validate whether we can support this use case**

---

# Topic 6. On-demand Data Fetching Instead of Pulling Everything Up Front

## 💬 Original Chinese

> 用户 Call 的时候，我们再拿这个 Report，然后拿到之后存下来。

## 🇺🇸 Natural English

> Instead of pulling all the reports up front, we can fetch the report on demand when the user calls the tool and persist the result afterward. 

### Alternative Expressions

* We can fetch the data lazily.
* We don't need to pre-load everything.
* Let's retrieve the report on demand.

### 🧠 Vocabulary

**on demand** — 按需

**fetch lazily / lazy loading** — 延迟加载

**persist the result** — 持久化结果

---

# Topic 7. Clarifying the Tool's User Value

## 📌 Meeting Background

The team questioned the exact user intent behind the Account Health MCP. The conclusion was that the tool would provide a broad account-health view rather than only checking whether an Amazon account had been suspended. 

## 💬 Original Chinese

> 用户为什么会调用这个 Tool？

## 🇺🇸 Natural English

> What's the user intent behind calling this tool?

### Alternative Expressions

* What problem is this tool solving for the user?
* What's the primary use case?
* What would trigger a user to use this tool?

### ⭐⭐⭐ 产品/技术会议非常有用

> **What's the primary user intent here?**

---

# Topic 8. Requirement Should Be Clear Before Moving On

## 💬 Original Chinese

> Backlog Refining 就是确保大家对这个需求没有疑问。

## 🇺🇸 Natural English

> The goal of backlog refinement is to make sure everyone has enough clarity on the requirement before we move forward. 

### Alternative Expressions

* We should resolve the major open questions before planning.
* Everyone should understand the scope and dependencies.
* The requirement should be clear enough to estimate.

### ⭐ 推荐

> **The requirement should be clear enough to estimate and implement.**

---

# Topic 9. Assigning an Owner

## 💬 Original Chinese

> 有对这个感兴趣的吗？我可以优先安排。

## 🇺🇸 Natural English

> Is anyone interested in taking ownership of this one?

### Alternative Expressions

* Does anyone want to pick this up?
* Is anyone interested in owning this?
* If no one volunteers, I'll assign an owner later.

### ⭐ 高频

> **Does anyone want to take ownership of this?**

---

# Topic 10. Real-time Notification MCP

## 📌 Meeting Background

The team discussed integrating additional Amazon notifications into the MCP and existing Alerts system. A key open question was when subscriptions should be created and whether all seller accounts should be subscribed by default. 

## 💬 Original Chinese

> 我们现在需要对这些 Notification 做 MCP 集成。

## 🇺🇸 Natural English

> We need to integrate these Amazon notifications into the MCP workflow.

---

## 💬 Original Chinese

> 这些通知需要跟现在的 Alerts 去做集成。

## 🇺🇸 Natural English

> These notifications also need to integrate with our existing Alerts system.

### 🧠 Vocabulary

* **subscription** — 订阅
* **notification flow** — 通知流程
* **event-driven** — 事件驱动的
* **integration point** — 集成点

---

# Topic 11. Surfacing an Important Design Question

## 💬 Original Chinese

> 什么时候触发这个 Notification？

## 🇺🇸 Natural English

> What should trigger the notification subscription?

### Alternative Expressions

* When should the subscription be created?
* What's the trigger point?
* Should we subscribe all eligible accounts by default?

### ⭐ 技术设计常用

> **What's the trigger point for this flow?**

---

# Topic 12. This Needs Research, but It's Not a Blocker

## 💬 Original Chinese

> 这个我可以去调研，我可以最终给出答案，这不是什么 Block 的问题。

## 🇺🇸 Natural English

> I can investigate this and come back with an answer. I don't see it as a blocker right now. 

### Alternative Expressions

* This is an open question, but not a blocker.
* We can resolve this during implementation.
* I don't think this should prevent us from moving forward.

### ⭐ 很实用

> **It's an open question, but not a blocker.**

---

# Topic 13. Split Research into a Separate AC

## 💬 Original Chinese

> 可以先分出来一个 AC，专门去研究。

## 🇺🇸 Natural English

> We can split out a separate acceptance criterion or task specifically for the research work. 

### 更自然的工程表达

> **Let's create a separate research task for this.**

如果你们公司 AC 指具体子项，也可以说：

> Let's create a separate AC for the research portion.

---

# Topic 14. Raise Risks Early

## 💬 Original Chinese

> Sprint 前半周如果觉得有风险，及时跟我讲。

## 🇺🇸 Natural English

> If you see any risk during the first half of the sprint, please raise it early.

### Alternative Expressions

* Flag any risks as early as possible.
* Don't wait until the end of the sprint to raise concerns.
* Let me know early if the timeline starts looking risky.

### ⭐⭐⭐ 必背

> **Please flag any risks early.**

---

# Topic 15. CPC History Needs Currency

## 📌 Meeting Background

The CPC History tool could follow an existing history-tool pattern, but the team identified one important addition: currency needed to be included because CPC values differ by marketplace. 

## 💬 Original Chinese

> 我觉得这里唯一需要加的是 Currency。

## 🇺🇸 Natural English

> The only additional field we really need here is currency.

---

## 💬 Original Chinese

> 每个国家货币不一样，所以 CPC History 里面需要带 Currency。

## 🇺🇸 Natural English

> Since CPC values are marketplace-specific, the response should include the currency.

### ⭐ 更自然

> **The response should make the currency explicit.**

---

# Topic 16. Keep the First Version Small

## 📌 Meeting Background

For the "bought together" tool, the team considered multiple query directions but chose to keep the first version simple: input one ASIN and return the products that are frequently bought together with it. 

## 💬 Original Chinese

> 反过来的查询先不需要，我们先只做这一个。

## 🇺🇸 Natural English

> We don't need to support the reverse lookup in the first version. Let's keep the initial scope to one direction.

### Alternative Expressions

* Let's keep the first version simple.
* We can defer the reverse lookup.
* Let's avoid expanding the scope unnecessarily.

### ⭐ 高频

> **Let's keep the initial scope small.**

---

# Topic 17. Requirement Documentation Should Be Completed Before QA

## 💬 Original Chinese

> 如果不补充的话，以后发了什么，测试怎么验证，会不太清楚。

## 🇺🇸 Natural English

> If we don't document the details, it'll be difficult later to understand exactly what was shipped and how QA should validate it. 

### Alternative Expressions

* We need enough detail for QA to know what to test.
* The implementation scope should be traceable.
* We should document the expected behavior before testing starts.

### ⭐ 推荐

> **QA needs enough context to validate the expected behavior.**

---

# Topic 18. MCP Should Be Treated as an Independent Tool

## 📌 Meeting Background

A long discussion focused on whether an MCP tool should reproduce the full Listing Builder workflow. The key clarification was that an MCP tool should expose a capability with defined inputs and outputs; the AI agent decides how to combine that capability with other tools. 

## 💬 Original Chinese

> 你又陷入整个 Listing Builder 的场景里面了，你要从那里出来。

## 🇺🇸 Natural English

> You're thinking about this too much in terms of the full Listing Builder workflow. We should treat this as an independent capability.

### ⭐ 更专业版本

> **Let's decouple the tool from the end-to-end Listing Builder workflow.**

---

## 💬 Original Chinese

> 它只是提供一个功能，具体 AI 怎么用你不要管。

## 🇺🇸 Natural English

> The MCP only needs to expose the capability. How the AI chooses to use it is a separate concern.

### Alternative Expressions

* Define the contract, not the orchestration.
* The tool should focus on inputs and outputs.
* The agent is responsible for orchestration.

### ⭐⭐⭐ 这句非常值得你学

> **The tool should focus on its contract; the agent handles the orchestration.**

---

# Topic 19. Input and Output Contract

## 💬 Original Chinese

> 你给我一堆 Keyword，我给你 Keyword Performance 就可以了。

## 🇺🇸 Natural English

> You give the tool a set of keywords, and it returns the corresponding keyword-performance data.

### 🧠 Vocabulary

**tool contract** — Tool 的输入输出约定

**input schema** — 输入 Schema

**output schema** — 输出 Schema

**orchestration** — 多工具调用与流程编排

---

# Topic 20. Pagination to Reduce Response Size

## 📌 Meeting Background

Some MCP calls were taking a very long time because large responses were difficult for different agents to handle. One example took around 26 minutes. The proposed solution was to add pagination to high-volume tools. 

## 💬 Original Chinese

> 返回数据量的大小会影响 Agent。

## 🇺🇸 Natural English

> The response size can significantly affect how well the agent handles the tool call.

### Alternative Expressions

* Large payloads can slow the agent down.
* Response size affects performance.
* We should avoid returning unnecessarily large payloads.

---

## 💬 Original Chinese

> 我们要给很多 Tool 加分页。

## 🇺🇸 Natural English

> We need to add pagination to a number of high-volume tools.

### 🧠 Vocabulary

**payload** = 请求/响应数据体

**pagination** = 分页

**high-volume tool** = 返回数据量大的工具

---

# Topic 21. Owners Should Review Their Own Tools

## 💬 Original Chinese

> 每个人 Review 一下自己做过的 Tool，看哪些需要加分页。

## 🇺🇸 Natural English

> Each owner should review the tools they've worked on and identify which ones need pagination. 

### Alternative Expressions

* Tool owners should assess pagination needs.
* Please review your own tools for large response payloads.
* Identify which tools would benefit from pagination.

---

# Topic 22. Use the UI Maximum as the Default Page Size

## 💬 Original Chinese

> 大家 Follow 页面的最大次数就可以了。

## 🇺🇸 Natural English

> We can use the UI's current maximum result count as the default page size. 

### Alternative Expressions

* Align the default page size with the existing UI limit.
* Use the current product limit as the default.
* Users can still request more or fewer results.

---

# Topic 23. Final Confirmation Before Sprint Planning

## 📌 Meeting Background

The team planned to complete missing requirement details, move the selected stories into the sprint, review story points and ACs in Sprint Planning, and then do a final confirmation of the sprint scope. 

## 💬 Original Chinese

> Planning 会议上，把今天剩下的疑问点和缺失的内容补齐。

## 🇺🇸 Natural English

> In sprint planning, we'll close the remaining gaps and confirm any open questions from today's discussion.

### Alternative Expressions

* We'll finalize the remaining details in planning.
* Planning should give us a clear, executable sprint scope.
* By the end of planning, everyone should understand the committed work.

### ⭐⭐⭐ 推荐

> **By the end of planning, we should have a clear and executable sprint scope.**

---

# Topic 24. Take Detailed Requirement Review to a Smaller Group

## 💬 Original Chinese

> Backlog Refining 不一定能全部确认，具体的事情可以私下约小范围会议。

## 🇺🇸 Natural English

> We don't need to resolve every implementation detail during backlog refinement. Detailed discussions can move to a smaller follow-up session. 

### Alternative Expressions

* Let's take the detailed discussion offline.
* We can schedule a smaller follow-up with the relevant people.
* Refinement should focus on major scope and open questions.

### ⭐ 会议效率神句

> **Let's take the detailed discussion into a smaller follow-up.**

---

# Topic 25. Don't Treat the Written Requirement as Perfect

## 💬 Original Chinese

> 不要拘泥于我写的需求，有可能是我考虑不周到。

## 🇺🇸 Natural English

> Don't treat the written requirement as fixed. If you notice missing cases or something that doesn't make sense, bring it up.

### Alternative Expressions

* The requirement isn't set in stone.
* Please challenge the requirement if something looks wrong.
* Feel free to propose changes as you learn more during implementation.

### ⭐ 很地道

> **The requirement isn't set in stone.**

= 需求不是不可修改的。

---

# 📖 Grammar & Expression Notes

### 1. “研究型需求”

> **exploratory story**

> **research-heavy story**

---

### 2. “用户为什么会调用这个 Tool？”

> **What's the user intent?**

> **What's the primary use case?**

---

### 3. “不是 Blocker”

> **It's an open question, but not a blocker.**

---

### 4. “先做第一版”

> **keep the initial scope small**

> **defer the rest**

---

### 5. “输入输出”

> **input/output contract**

> **tool contract**

---

### 6. “不要管 AI 怎么编排”

> **The agent handles the orchestration.**

---

### 7. “响应数据太大”

> **The payload is too large.**

> **The response size is too large.**

---

### 8. “完善需求”

> **flesh out the requirement**

例如：

> We still need to flesh out the requirement.

---

### 9. “需求不是写死的”

> **It's not set in stone.**

---

# ⭐ Shadowing Practice

这场建议重点练 **Refinement + MCP Design**：

> **The goal is to clarify the upcoming work before the sprint starts.**

> **This story is still somewhat exploratory.**

> **Let's validate whether we can support this use case.**

> **What's the primary user intent here?**

> **The requirement should be clear enough to estimate and implement.**

> **Does anyone want to take ownership of this?**

> **It's an open question, but not a blocker.**

> **Please flag any risks early.**

> **Let's keep the initial scope small.**

> **QA needs enough context to validate the expected behavior.**

> **Let's decouple the tool from the end-to-end workflow.**

> **The tool should focus on its contract; the agent handles the orchestration.**

> **Large payloads can slow the agent down.**

> **Each owner should review their tools for pagination needs.**

> **The requirement isn't set in stone.**

---

# 📚 Today's Vocabulary

| Expression               | 中文          |
| ------------------------ | ----------- |
| **backlog refinement**   | Backlog 梳理  |
| **candidate work**       | 候选需求        |
| **implementation-ready** | 已具备开发条件     |
| **area of expertise**    | 专长领域        |
| **exploratory story**    | 探索型需求       |
| **on demand**            | 按需          |
| **user intent**          | 用户意图        |
| **take ownership**       | 主动负责        |
| **trigger point**        | 触发点         |
| **open question**        | 待确认问题       |
| **flag a risk**          | 提前暴露风险      |
| **initial scope**        | 初始范围        |
| **tool contract**        | Tool 输入输出约定 |
| **orchestration**        | 编排          |
| **payload**              | 返回/请求数据体    |
| **pagination**           | 分页          |
| **page size**            | 每页数据量       |
| **flesh out**            | 补充完善        |
| **set in stone**         | 已固定、不可更改    |

## ⭐ 今天最值得背的 10 句

> **The goal is to clarify the upcoming work before the sprint starts.**

> **This story is still somewhat exploratory.**

> **What's the primary user intent here?**

> **The requirement should be clear enough to estimate and implement.**

> **Does anyone want to take ownership of this?**

> **It's an open question, but not a blocker.**

> **Please flag any risks early.**

> **Let's keep the initial scope small.**

> **The tool should focus on its contract; the agent handles the orchestration.**

> **The requirement isn't set in stone.**

# Engineering Meeting English Notebook

## Meeting #18 – Sprint Planning, Story Points, QA Readiness & Delivery Commitment

这场会议是一次很典型的 **Sprint Planning**。和前面的 Backlog Refinement 不同，这次重点不再是“需求是什么”，而是：**这个 Sprint 到底做哪些、有没有风险、什么时候提测、Story Point 怎么估、QA 能不能承接、哪些依赖会影响交付，以及团队最后是否愿意承诺这个 Sprint 范围**。会议一开始就明确了这些目标。

---

# Topic 1. Explaining the Purpose of Sprint Planning

## 📌 Meeting Background

The team clarified that Sprint Planning is used to define the work for the next two weeks, confirm that engineering and QA have a shared understanding of the requirements, estimate story points, and make sure the final sprint scope is within the team's capacity. 

## 💬 Original Chinese

> Planning 会议就是计划接下来两周的内容，框定我们现在要做的范围。

## 🇺🇸 Natural English

> Sprint planning is where we define the scope for the next two weeks.

### Alternative Expressions

* We use sprint planning to finalize the scope for the upcoming sprint.
* This is where we decide what we can realistically commit to.
* The goal is to make sure the planned work fits within the team's capacity.

### ⭐ 最推荐

> **This is where we decide what we can realistically commit to for the sprint.**

---

# Topic 2. Confirming Shared Understanding

## 💬 Original Chinese

> 确认研发的理解和需求是一致的。

## 🇺🇸 Natural English

> We need to make sure engineering's understanding is aligned with the requirement.

### Alternative Expressions

* Let's make sure we're all aligned on the requirement.
* We need to confirm there are no major gaps in understanding.
* Everyone should have the same understanding before development starts.

### ⭐ 高频

> **Let's make sure we're aligned on the requirement.**

---

# Topic 3. Story Point Estimation

## 📌 Meeting Background

The team discussed how story points should be estimated and how they relate to team capacity. The purpose was not to measure an individual developer's performance, but to help the team understand how much work it can reliably commit to in future sprints.  

## 💬 Original Chinese

> 我们会在这个会议上做 Story Point 的预估。

## 🇺🇸 Natural English

> We'll estimate story points during this meeting.

---

## 💬 Original Chinese

> 后续可以知道团队 Capacity 是什么样子的。

## 🇺🇸 Natural English

> Over time, story points will help us understand the team's capacity more accurately.

### Alternative Expressions

* This helps us calibrate our sprint capacity.
* We can use historical velocity to plan future sprints.
* The goal is to improve planning accuracy.

### 🧠 Vocabulary

| Expression        | 中文     |
| ----------------- | ------ |
| story point       | 故事点    |
| capacity          | 团队承载能力 |
| velocity          | 团队迭代速度 |
| estimate          | 估算     |
| planning accuracy | 规划准确度  |

---

# Topic 4. Large Stories May Need to Be Split

## 💬 Original Chinese

> 如果 Story Point 很多，其实意味着 User Story 很大，是可以再拆分的。

## 🇺🇸 Natural English

> If a story requires too many points, that's usually a sign that it should be broken down further. 

### Alternative Expressions

* The story may be too large.
* We should consider splitting it into smaller stories.
* A high estimate may indicate the scope is too broad.

### ⭐ 推荐

> **A large estimate is usually a signal that the story should be split.**

---

# Topic 5. Using a Consistent Estimation Standard

## 💬 Original Chinese

> 尽量用统一的标准，这样不同 Sprint 才能看到大家完成的情况。

## 🇺🇸 Natural English

> We should use a consistent estimation standard so we can compare sprint performance over time.

### Alternative Expressions

* We need a consistent baseline.
* The estimation method should stay consistent across sprints.
* Otherwise, the numbers won't be meaningful.

### ⭐ 高频

> **We need a consistent baseline for estimation.**

---

# Topic 6. Pagination as a Sprint-wide Technical Story

## 📌 Meeting Background

Pagination was one of the larger stories in the sprint because it affected many MCP tools. The team decided not every tool necessarily needed pagination—for example, one tool could only ever return 30 items due to business rules.  

## 💬 Original Chinese

> 所有的工具都要加分页吗？

## 🇺🇸 Natural English

> Do all of the tools need pagination?

---

## 💬 Original Chinese

> 这个最多只返回 30 条，业务上就是这么设计的，所以不需要。

## 🇺🇸 Natural English

> This tool only returns up to 30 items by design, so pagination isn't necessary.

### Alternative Expressions

* Pagination doesn't add much value here.
* The result set is capped at 30.
* This tool has a fixed upper limit.

### 🧠 Vocabulary

**capped at 30** = 上限 30 条

> The result set is capped at 30 items.

---

# Topic 7. Estimate by Module Instead of Individual Task

## 💬 Original Chinese

> 我们可不可以按照模块来分？

## 🇺🇸 Natural English

> Could we estimate this by module instead of by individual task?

### Alternative Expressions

* Maybe module-level estimation would be more practical.
* We can group the work by module.
* That may align better with both development and QA ownership.

### ⭐ 很实用

> **Let's group the work by module.**

---

# Topic 8. Merge Everyone's Work Into One Testing Branch

## 📌 Meeting Background

Because several people would work on different parts of the pagination story, the team agreed to merge the work into one shared branch and deploy that branch to a test environment for QA rather than using separate environments for every developer. 

## 💬 Original Chinese

> 大家统一往一个分支上合。

## 🇺🇸 Natural English

> Let's merge everyone's changes into a shared branch.

### Alternative Expressions

* We'll use one integration branch.
* Everyone should target the same testing branch.
* QA can validate the combined changes in one environment.

### 🧠 Vocabulary

**integration branch** = 集成分支

**shared branch** = 共享分支

---

# Topic 9. Defining the QA Handoff Date

## 📌 Meeting Background

QA asked whether each task should have a planned testing handoff date. The team agreed this would be useful and discussed using due dates to represent when development should be ready for QA. 

## 💬 Original Chinese

> 我们需要提前给一个提测时间吗？

## 🇺🇸 Natural English

> Should we define a target QA handoff date for each item?

### Alternative Expressions

* Should every story have a target date for QA?
* Can we add a test-ready date?
* Let's make the QA handoff date explicit.

### ⭐ 推荐

> **Let's make the QA handoff date explicit.**

---

# Topic 10. How Much Time QA Needs

## 💬 Original Chinese

> 一般一个工具给一天左右。

## 🇺🇸 Natural English

> QA typically needs about one day per tool.

### Alternative Expressions

* We should budget roughly one day of QA per tool.
* Each tool needs about a day for testing.
* We need to leave enough testing buffer.

### ⭐ 高频

> **We need to leave enough testing buffer.**

---

# Topic 11. Readiness Before Release

## 💬 Original Chinese

> 发布是 9 月 8 号，那 9 月 2 号提测应该没问题。

## 🇺🇸 Natural English

> If the release is scheduled for September 8th, a QA handoff by September 2nd should give us enough time.

### ⭐ 适合以后做 Planning

> **That should give QA enough time before the release.**

---

# Topic 12. Huimin's Two MCP Stories

这部分是你自己的任务。会议中给你安排的是：

* Keyword Sales
* ABA SFR History

其中 Keyword Sales 预计工作量更高一些，给了 **2 points**；ABA 相对简单，给了 **1 point**。两个任务当时计划一起推进，并确认 Ready for Testing 时间。

## 💬 Original Chinese

> 这两个相对来说比较类似，目前没有什么问题。

## 🇺🇸 Natural English

> These two are fairly similar, and I don't see any major issues at the moment.

---

## 💬 Original Chinese

> 什么时候可以 Ready for Testing？

## 🇺🇸 Natural English

> When do you think these will be ready for testing?

### Alternative Expressions

* What's your target QA handoff date?
* When do you expect to have these ready for QA?
* Do you have an ETA for testing readiness?

### ⭐ 你以后回答可以直接说

> **I'm targeting Monday for QA handoff.**

或者：

> **I expect both of them to be ready for testing by Monday.**

---

# Topic 13. Document Test Scope Before Development Is Done

## 💬 Original Chinese

> 提测之前，把 PR / 描述简单写一下，要测哪些点。

## 🇺🇸 Natural English

> Before handing the work over to QA, please document the main changes and what needs to be tested. 

### Alternative Expressions

* Please document the regression scope.
* QA needs enough context to understand what changed.
* Don't rely on the ticket title alone.

### ⭐ 非常值得背

> **QA needs enough context to understand what changed and what needs to be validated.**

---

# Topic 14. Large API Migration With Little Coding Effort

## 📌 Meeting Background

One Main App refactor item involved dozens of APIs, but the actual development effort was small because the work was mainly routing/configuration and regression testing.  

## 💬 Original Chinese

> 开发其实没有什么工作量，主要是配路由和测试。

## 🇺🇸 Natural English

> There's very little implementation work here. Most of the effort is in routing configuration and regression testing.

### ⭐ 很重要

Story Point 不应该只看代码量。

更完整的表达：

> **The coding effort is small, but the end-to-end delivery effort still includes configuration and QA.**

---

# Topic 15. Testing Scope Can Be Larger Than the Feature Scope

## 📌 Meeting Background

For one migrated scheduled-job flow, the actual feature change was small, but because underlying logic had moved from Main App and had not yet been fully validated, QA potentially needed to regress the broader module and related notifications. 

## 💬 Original Chinese

> 除了功能验证以外，可能整个模块都需要回归一下。

## 🇺🇸 Natural English

> In addition to validating the feature itself, we may need to run regression across the broader module.

### Alternative Expressions

* The blast radius is larger than the immediate feature.
* The underlying migration affects more than just this workflow.
* QA may need broader regression coverage.

### 🧠 Vocabulary

**blast radius** = 改动潜在影响范围

---

# Topic 16. Requirement Is Not Clear Enough Yet

## 💬 Original Chinese

> 这个字段什么意思，我现在回答不了，需要再确认。

## 🇺🇸 Natural English

> I'm not able to answer that confidently yet. I need to verify it first. 

### Alternative Expressions

* I'm not sure yet. Let me confirm.
* That's still an open question.
* I don't want to guess; I'll verify it.

### ⭐ 强烈推荐

> **I don't want to guess. Let me verify that first.**

非常适合英文技术会议。

---

# Topic 17. Remove a Field If the Source Doesn't Support It

## 💬 Original Chinese

> 如果报告里面没有这个字段，那我们就不要了。

## 🇺🇸 Natural English

> If the source report doesn't provide that field, we should leave it out.

### Alternative Expressions

* We shouldn't expose data that isn't available from the source.
* Let's remove that field from the scope.
* There's no reason to derive it unless there's a clear requirement.

---

# Topic 18. Should We Persist the Data?

## 📌 Meeting Background

The team debated whether account-health report data needed to be stored. Since the tool was mainly concerned with current account status and historical value was unclear, the initial direction was not to persist the data unless there was a clear reason.  

## 💬 Original Chinese

> 如果历史没有什么价值，我们就不用存。

## 🇺🇸 Natural English

> If there's no meaningful value in keeping the historical data, we don't need to persist it.

### Alternative Expressions

* Let's avoid persisting data unless there's a clear use case.
* We can process it on demand.
* Historical storage may be unnecessary here.

### ⭐ 高频

> **Let's avoid storing data unless there's a clear use case for it.**

---

# Topic 19. Synchronous vs. Asynchronous Report Flow

## 📌 Meeting Background

A SP-API report requires multiple steps: create the report, wait for it, download it, and parse it. That raised concerns about response time if the MCP tried to perform everything synchronously. 

## 💬 Original Chinese

> 用户拉这个报告可能会很久，因为要创建、拉取、下载、解析。

## 🇺🇸 Natural English

> The request may take quite a while because we need to create the report, wait for it to be ready, download it, and parse the result.

### 🧠 Vocabulary

* synchronous flow — 同步流程
* asynchronous process — 异步流程
* polling — 轮询
* response time — 响应时间
* long-running request — 长时间请求

### ⭐ 技术会议表达

> **This may turn into a long-running request.**

---

# Topic 20. Investigate Before Finalizing the Design

## 💬 Original Chinese

> 你可以先试一下，整个流程大概要多久。

## 🇺🇸 Natural English

> Let's prototype the flow first and measure how long the full request takes.

### Alternative Expressions

* Let's validate the latency before finalizing the design.
* We need some real measurements.
* Let's test the end-to-end timing first.

### ⭐ 很工程化

> **Let's get some real measurements before we decide.**

---

# Topic 21. Keep Tool Definition Explicit

## 📌 Meeting Background

The team noticed the requirement document still lacked concrete MCP tool names, input parameters, and output definitions. That made it difficult to communicate exactly how many tools would ship and what their contracts were. 

## 💬 Original Chinese

> Tool Name、入参、出参这些东西要补一下。

## 🇺🇸 Natural English

> We need to define the tool name, input parameters, and output schema.

### Alternative Expressions

* The tool contract still needs to be finalized.
* We need a clear input/output definition.
* The requirement isn't implementation-ready yet.

### ⭐ 推荐

> **The tool contract still needs to be finalized.**

---

# Topic 22. External Dependency Creates Schedule Risk

## 💬 Original Chinese

> 这个得看他们什么时候提供接口。

## 🇺🇸 Natural English

> This depends on when they can provide the API.

### Alternative Expressions

* We're blocked by an external dependency.
* The timeline depends on the upstream team.
* We can't give a firm date until the dependency is ready.

### ⭐ 高频

> **The timeline depends on the upstream dependency.**

---

# Topic 23. Some Notifications Are Not Technically Feasible

## 📌 Meeting Background

During the Amazon notification discussion, research showed that some notifications were vendor-only and some SQS subscriptions were already owned by another service, so not every originally planned notification could be supported. 

## 💬 Original Chinese

> 有一部分是做不了的。

## 🇺🇸 Natural English

> Some of these notification types aren't technically feasible for us.

### Alternative Expressions

* We can't support all of them.
* Some are out of scope due to platform limitations.
* Certain notifications aren't available to our account type.

---

## 💬 Original Chinese

> 把能做的找出来，不能做的备注原因。

## 🇺🇸 Natural English

> Let's identify the ones we can support and document why the others aren't feasible.

### ⭐ 很适合需求调研

> **Document the feasibility and the reason for any limitations.**

---

# Topic 24. Integration May Be More Expensive Than Expected

## 💬 Original Chinese

> 跟现有 Alerts 集成的话，成本可能比较高。

## 🇺🇸 Natural English

> Integrating this into the existing Alerts system may require significantly more effort than expected. 

### Alternative Expressions

* The integration cost is higher than we expected.
* This isn't just a simple event mapping.
* We'd need changes to templates, notifications, and downstream flows.

### ⭐ 推荐

> **The integration is more involved than we initially expected.**

---

# Topic 25. Pull a Risky Story Out of the Sprint

## 📌 Meeting Background

Because the Notification story still had unresolved design questions and feasibility concerns, the team decided not to include it in the current delivery batch yet. 

## 💬 Original Chinese

> 这个有点风险了，先不放这一批。

## 🇺🇸 Natural English

> This looks too risky to commit to right now, so let's leave it out of this release batch for now.

### Alternative Expressions

* Let's take it out of the sprint for now.
* We shouldn't commit to this until the design is clearer.
* Let's defer it until we've resolved the open questions.

### ⭐⭐⭐ Planning 高频

> **We shouldn't commit to this until the design is clearer.**

---

# Topic 26. Finding the Root Cause of an AI Model Failure

## 💬 Original Chinese

> 我们需要定位 AI Image 为什么生成不了。

## 🇺🇸 Natural English

> We need to identify the root cause of why the AI image generation is failing. 

### Alternative Expressions

* We need to investigate why the model stopped working.
* The old model ID may no longer be supported.
* Let's trace when the failure first started.

### ⭐ 高价值表达

> **Let's trace this back to when it first started failing.**

---

# Topic 27. Going Back Through Historical Failures

## 💬 Original Chinese

> 需要再往前回溯，看之前失败的原因是什么。

## 🇺🇸 Natural English

> We need to go back through the earlier failures and identify what originally caused the issue.

### Useful Expressions

* trace it back
* inspect historical failures
* identify when the regression started
* narrow down the root cause

---

# Topic 28. MCP Calculation Has Hidden Dependencies

## 📌 Meeting Background

The Listing Builder MCP discussion revealed that some values such as KPS depend not only on keywords, but also on competitors, search volume, CPS, and keyword source. This meant the supposedly standalone tool had more contextual dependencies than originally expected. 

## 💬 Original Chinese

> KPS 不是只看 Keyword，还依赖竞品、SV、CPS 和 Keyword Source。

## 🇺🇸 Natural English

> KPS isn't derived from the keyword alone. It also depends on competitor data, search volume, CPS, and keyword source.

### Alternative Expressions

* The calculation has several upstream dependencies.
* This isn't a standalone metric.
* The input contract needs to carry more context.

### ⭐ 很适合 MCP 设计

> **The tool needs more context than we initially expected.**

---

# Topic 29. Make Optional Context Explicit

## 💬 Original Chinese

> Keyword Source 可以做成 Optional，如果没填，就认为是用户自己加的。

## 🇺🇸 Natural English

> We can make `keywordSource` optional. If it's missing, we can treat the keyword as user-provided. 

### 🧠 Vocabulary

**optional field** — 可选字段

**user-provided** — 用户提供的

**default behavior** — 默认行为

---

# Topic 30. Could Two Tools Be Combined?

## 💬 Original Chinese

> 这两个是不是可以合成一个 Tool？

## 🇺🇸 Natural English

> Could these two capabilities be combined into a single tool? 

### Alternative Expressions

* Do these really need to be separate tools?
* Could we consolidate them?
* Are the input/output contracts similar enough to merge?

### ⭐ MCP 设计很实用

> **Are these capabilities distinct enough to justify separate tools?**

---

# Topic 31. Final Sprint Risk Check

## 📌 Meeting Background

At the end of planning, the team explicitly checked for delivery risks and delays. If new product requirements entered the sprint later, they would need to be reviewed against the existing commitment and potentially replace lower-priority work rather than simply being added on top. 

## 💬 Original Chinese

> 大家看一下自己手上的风险，有 Delay 风险就提前讲。

## 🇺🇸 Natural English

> Please review your own items and raise any delivery risks or potential delays early.

### ⭐ 必背

> **Please flag any delivery risks early.**

---

## 💬 Original Chinese

> 如果产品中途加新需求，要看会不会影响当前 Sprint 的交付，要不要置换。

## 🇺🇸 Natural English

> If new product work comes in mid-sprint, we need to assess the impact on the current commitment and decide whether something else should be deprioritized.

### ⭐ 高级项目表达

> **New work shouldn't simply be added on top of the existing commitment.**

---

# Topic 32. Planning Is Done Once the Team Commits

## 💬 Original Chinese

> 如果没有问题，整个 Sprint 范围也就确认了。

## 🇺🇸 Natural English

> If there are no further concerns, we can consider the sprint scope finalized.

### Alternative Expressions

* We're comfortable committing to this scope.
* This will be our committed sprint scope.
* The sprint plan is finalized.

### ⭐ Sprint Planning 收尾

> **Are we all comfortable committing to this scope?**

---

# 📖 Grammar & Expression Notes

### 1. “框定 Sprint 范围”

> **define the sprint scope**

> **finalize the sprint scope**

---

### 2. “提测时间”

> **QA handoff date**

> **test-ready date**

---

### 3. “Story 很大，需要拆”

> **The story is too large and should be broken down further.**

---

### 4. “测试范围比需求范围大”

> **The regression scope is broader than the feature scope.**

---

### 5. “我现在不确定，不想乱猜”

> **I don't want to guess. Let me verify that first.**

---

### 6. “数据要不要存”

> **Do we need to persist this data?**

---

### 7. “整个请求可能很慢”

> **This may turn into a long-running request.**

---

### 8. “这个需求还没 Ready”

> **The requirement isn't implementation-ready yet.**

---

### 9. “有外部依赖”

> **We're blocked by an upstream dependency.**

---

### 10. “先不承诺”

> **We shouldn't commit to this yet.**

---

# ⭐ Shadowing Practice – Sprint Planning Edition

建议你重点练这一组：

> **This is where we decide what we can realistically commit to for the sprint.**

> **Let's make sure we're aligned on the requirement.**

> **We need a consistent baseline for estimation.**

> **A large estimate is usually a signal that the story should be split.**

> **Let's make the QA handoff date explicit.**

> **That should give QA enough time before the release.**

> **QA needs enough context to understand what changed and what needs to be validated.**

> **I don't want to guess. Let me verify that first.**

> **Let's avoid storing data unless there's a clear use case for it.**

> **This may turn into a long-running request.**

> **Let's get some real measurements before we decide.**

> **The tool contract still needs to be finalized.**

> **The timeline depends on the upstream dependency.**

> **The integration is more involved than we initially expected.**

> **We shouldn't commit to this until the design is clearer.**

> **Please flag any delivery risks early.**

> **Are we all comfortable committing to this scope?**

---

# 📚 Today's Vocabulary

| Expression               | 中文        |
| ------------------------ | --------- |
| **sprint scope**         | Sprint 范围 |
| **commit to**            | 承诺交付      |
| **capacity**             | 团队容量      |
| **velocity**             | 团队速度      |
| **baseline**             | 基准        |
| **QA handoff date**      | 提测日期      |
| **testing buffer**       | 测试缓冲      |
| **integration branch**   | 集成分支      |
| **blast radius**         | 改动影响范围    |
| **persist data**         | 持久化数据     |
| **long-running request** | 长耗时请求     |
| **implementation-ready** | 可进入开发     |
| **upstream dependency**  | 上游依赖      |
| **technically feasible** | 技术可行      |
| **defer**                | 延后        |
| **trace back**           | 回溯        |
| **optional field**       | 可选字段      |
| **tool contract**        | 工具输入输出契约  |
| **delivery risk**        | 交付风险      |
| **deprioritize**         | 降低优先级     |

## ⭐ 今天最值得你背的 10 句

> **This is where we decide what we can realistically commit to for the sprint.**

> **Let's make sure we're aligned on the requirement.**

> **A large estimate is usually a signal that the story should be split.**

> **Let's make the QA handoff date explicit.**

> **QA needs enough context to understand what changed and what needs to be validated.**

> **I don't want to guess. Let me verify that first.**

> **The tool contract still needs to be finalized.**

> **The timeline depends on the upstream dependency.**

> **We shouldn't commit to this until the design is clearer.**

> **Please flag any delivery risks early.**
>
# Engineering Meeting English Notebook

## Meeting #19 – Backlog Refinement, Technical Stories, API Migration & Product Requirement Clarification

这场会议属于比较典型的 **Backlog Refinement + Requirement Clarification**。和 Sprint Planning 不同，这次更关注：**下个 Sprint 可能做什么、需求是否足够清楚、技术故事怎么描述、依赖项是什么、哪些工作需要 UX、哪些需求只是先调研，以及新加入的产品需求怎么进入 Sprint 流程**。会议一开始就明确这是一次“需求澄清会”。

---

# Topic 1. Explaining the Backlog Refinement Process

## 📌 Meeting Background

Keisha was unfamiliar with the process, so the team explained how requirements move from the backlog into a sprint. A requirement can first stay in the backlog as a candidate item, and once the team decides to work on it, it can be moved into the upcoming sprint. 

## 💬 Original Chinese

> 当前不一定要做的需求可以先放到 Backlog，确定要做的话再放到下一个 Sprint。

## 🇺🇸 Natural English

> If a requirement isn't ready to be committed yet, we can keep it in the backlog and move it into the sprint once we're ready to work on it.

### Alternative Expressions

* Keep it in the backlog for now.
* Move it into the sprint once the scope is clear.
* Treat it as candidate work until we're ready to commit.

### ⭐ 推荐

> **We can keep it in the backlog until we're ready to commit to it.**

---

# Topic 2. Reviewing Work by Priority

## 💬 Original Chinese

> 我从高优先级到低优先级来讲。

## 🇺🇸 Natural English

> I'll go through the items from highest to lowest priority. 

### Alternative Expressions

* Let's review these in priority order.
* We'll start with the highest-priority items.
* I'll walk through the backlog from high to low priority.

### ⭐ 高频

> **Let's review these in priority order.**

---

# Topic 3. Migrating From Static Credentials to Role-based Access

## 📌 Meeting Background

One technical story involved changing how the system accesses S3 and SQS. The current implementation used credentials, while the target design was to switch to role-based access in the next sprint. 

## 💬 Original Chinese

> 现在调用 S3、SQS 都是用密码形式，下一 Sprint 要改成 Role 的方式。

## 🇺🇸 Natural English

> We're currently using static credentials to access S3 and SQS, and we want to migrate to role-based access in the next sprint.

### Alternative Expressions

* We want to move away from static credentials.
* We should switch to role-based authentication.
* This is mainly a security and maintainability improvement.

### 🧠 Vocabulary

| Expression          | 中文      |
| ------------------- | ------- |
| static credentials  | 静态凭据    |
| role-based access   | 基于角色的访问 |
| authentication      | 认证      |
| credential rotation | 凭据轮换    |
| maintainability     | 可维护性    |

---

# Topic 4. Listing Builder Skill Is Built but Not Released

## 📌 Meeting Background

The Listing Builder Skill had already been developed, but the team still did not know how or where it should be published. The remaining work was mostly coordination and release-process clarification rather than implementation. 

## 💬 Original Chinese

> Listing Builder Skill 已经做好了，但是一直不知道怎么 Release。

## 🇺🇸 Natural English

> The Listing Builder Skill is already built, but we still haven't finalized how it should be released.

### Alternative Expressions

* The implementation is done; the release path is still unclear.
* We're blocked on the publishing process rather than development.
* The remaining work is mostly coordination.

### ⭐ 推荐

> **The implementation is complete, but the release path is still unclear.**

---

# Topic 5. Replace Brand With Shop

## 📌 Meeting Background

In TikTok Product Finder, the existing Brand field had become unreliable because the source data could no longer be crawled consistently. Shop data was still available, so the team planned to replace Brand with Shop in both the web experience and MCP filtering. 

## 💬 Original Chinese

> Brand 现在拿不到了，但是 Shop 是可以的，所以我们准备把 Brand 替换成 Shop。

## 🇺🇸 Natural English

> Brand data is no longer reliably available, but Shop data is, so we're planning to replace Brand with Shop.

### Alternative Expressions

* The current Brand filter is no longer reliable.
* Shop is a more stable data source.
* We'll need to update both the web flow and the MCP filter.

### ⭐ Useful

> **The current data source is no longer reliable.**

---

# Topic 6. Assigning Work Based on Capacity

## 💬 Original Chinese

> 下个 Sprint 暂时没有计划的话，这个可以先给你。

## 🇺🇸 Natural English

> If you don't have anything else planned for the next sprint, I can assign this to you.

### Alternative Expressions

* Do you have capacity to take this on?
* If you have bandwidth, I'll assign this to you.
* You can pick this up if your current sprint work is wrapping up.

### ⭐ 高频

> **Do you have capacity to take this on?**

---

# Topic 7. Sales History & GMV History MCP

## 📌 Meeting Background

The team proposed building Sales History and GMV History MCP tools by following the pattern of an existing Search Volume History tool. Because the structure was already familiar, the work was considered relatively straightforward. 

## 💬 Original Chinese

> Sales 跟 GMV History 可以参照 Search Volume History 来做 MCP。

## 🇺🇸 Natural English

> We can model the Sales History and GMV History MCPs after the existing Search Volume History tool.

### Alternative Expressions

* We can reuse the same pattern.
* The implementation should be fairly straightforward.
* We already have a similar reference implementation.

### 🧠 Vocabulary

**reference implementation** = 参考实现

---

# Topic 8. API Deprecation Creates a Hard Deadline

## 📌 Meeting Background

A TikTok API was scheduled to be shut down in October, so the team needed to migrate to the new OpenID-based API before the end of September. 

## 💬 Original Chinese

> 现在的 API 10 月份就会下线，所以 9 月底之前必须替换完。

## 🇺🇸 Natural English

> The current API will be deprecated in October, so we need to complete the migration by the end of September.

### Alternative Expressions

* We have a hard migration deadline.
* The legacy API is being sunset.
* We need to complete the cutover before the old API is retired.

### 🧠 Vocabulary

**deprecate** = 弃用

**sunset an API** = 正式停止一个 API

**cutover** = 从旧系统切换到新系统

### ⭐ 推荐

> **We have a hard deadline because the legacy API is being sunset.**

---

# Topic 9. Dependency Between Product Work and API Migration

## 💬 Original Chinese

> 我要做的需求是以 OpenID 为前提，所以这个做完以后才能做我的需求。

## 🇺🇸 Natural English

> My requirement depends on the OpenID migration, so we can't start it until that work is complete.

### Alternative Expressions

* This is a prerequisite for my work.
* My story is blocked by the OpenID migration.
* We need the migration in place first.

### ⭐ 高频

> **This is a prerequisite for the next piece of work.**

---

# Topic 10. Why the API Is Changing

## 📌 Meeting Background

The team explained that TikTok was moving away from exposing internal user IDs and introducing OpenID instead, mainly for security reasons. The migration might also require compatibility handling for historical data. 

## 💬 Original Chinese

> 主要是为了安全，原来的 User ID 不能再用了，要切成 OpenID。

## 🇺🇸 Natural English

> The main reason is security. The old user ID can no longer be used, so we need to migrate to OpenID.

### Alternative Expressions

* This is primarily a security-driven migration.
* The identifier model is changing.
* We may also need backward compatibility for historical data.

### 🧠 Vocabulary

**backward compatibility** = 向后兼容

---

# Topic 11. Google Trends as a Research Task

## 📌 Meeting Background

The Google Keyword Trends item was lower priority and still somewhat exploratory. The team planned to investigate whether existing code could be reused and wrap the capability as an MCP rather than build an entirely new data flow. 

## 💬 Original Chinese

> 你先研究一下吧。

## 🇺🇸 Natural English

> Please investigate this first and see what we can reuse.

### Alternative Expressions

* Start with a technical spike.
* Let's validate what already exists before building anything new.
* This is exploratory for now.

### ⭐ 高频

> **Let's see what we can reuse before building anything new.**

---

# Topic 12. Reuse Existing Functionality

## 💬 Original Chinese

> Amazon 已经开发过了，所以对应功能照搬，Spec 保持一致就可以。

## 🇺🇸 Natural English

> We already have the Amazon version, so we can reuse the same behavior and keep the spec consistent. 

### Alternative Expressions

* We don't need to reinvent the behavior.
* Let's keep the cross-platform behavior consistent.
* We can mirror the existing Amazon implementation.

### ⭐ 推荐

> **Let's mirror the existing implementation and keep the spec consistent.**

---

# Topic 13. Centralizing AI API Keys

## 📌 Meeting Background

The team currently had separate LiteLLM keys across multiple features. The proposed improvement was to use a shared key and track AI usage by feature in the database or logs, making maintenance and cost visibility easier. 

## 💬 Original Chinese

> 每加一个功能都申请一个 Key，可维护性太差。

## 🇺🇸 Natural English

> Creating a separate key for every new feature isn't maintainable.

### Alternative Expressions

* The current key-management model doesn't scale well.
* We should centralize key management.
* We need better usage tracking by feature.

---

## 💬 Original Chinese

> 最终希望统一一个 Key，然后按工具记录每天的 AI 使用量。

## 🇺🇸 Natural English

> Ideally, we'd use a shared key and track AI usage by feature or tool.

### 🧠 Vocabulary

* centralized key management
* usage tracking
* token consumption
* feature-level metrics

---

# Topic 14. Legacy Navigation Still Exists

## 📌 Meeting Background

Some navigation flows still pointed users to legacy PHP pages after refactoring. The team wanted to audit cross-tool navigation and identify any paths that had not yet been migrated. 

## 💬 Original Chinese

> 有些页面跳转的时候还是会调到旧的 PHP 页面。

## 🇺🇸 Natural English

> Some navigation paths still point to the legacy PHP pages.

### Alternative Expressions

* We still have a few legacy navigation paths.
* Some cross-tool links haven't been migrated.
* We need to audit the remaining legacy routes.

### 🧠 Vocabulary

**audit** = 系统性检查

**legacy route** = 遗留路由

---

# Topic 15. Standardizing Service Discovery

## 💬 Original Chinese

> 现在代码里有的用 Eureka，有的用 K8s Service，我们想统一掉。

## 🇺🇸 Natural English

> Some services still use Eureka while others use Kubernetes service discovery. We want to standardize on one approach. 

### Alternative Expressions

* We need to standardize service discovery.
* The current setup is inconsistent.
* Let's converge on a single approach.

### ⭐ 工程高频

> **We should standardize on one approach.**

---

# Topic 16. Don't Pull Everything Into One Sprint

## 💬 Original Chinese

> 这个不会完整放到下一个 Sprint，有空的话再拆新的 Technical Story。

## 🇺🇸 Natural English

> We won't pull the entire initiative into the next sprint. If we have capacity, we'll split off smaller technical stories.

### Alternative Expressions

* We'll tackle this incrementally.
* We'll only pull in the parts we have capacity for.
* Let's avoid overloading the sprint.

### ⭐ 推荐

> **We'll tackle this incrementally based on available capacity.**

---

# Topic 17. Confirming Whether UX Is Needed

## 💬 Original Chinese

> 这些需求需要 UX 参与吗？

## 🇺🇸 Natural English

> Do any of these items require UX involvement? 

### Alternative Expressions

* Do we need design support for any of these?
* Is there any UX work involved?
* Can engineering handle these without additional design?

---

# Topic 18. Refinement Doesn't Require Every Detail to Be Final

## 📌 Meeting Background

The team clarified that not every requirement needs a fully complete PRD during refinement. If some research is still needed, a user story can be created first, and the detailed requirement document can be attached later before Sprint Planning. 

## 💬 Original Chinese

> Backlog Refining 的时候不一定能确认所有细节。

## 🇺🇸 Natural English

> We don't need every detail finalized during backlog refinement.

### Alternative Expressions

* The story can still be exploratory at this stage.
* We just need enough clarity to understand the intended work.
* The detailed PRD can follow later.

### ⭐ 推荐

> **We just need enough clarity to understand the intended scope.**

---

# Topic 19. New Product Requirement – Two Commission Rates

## 📌 Meeting Background

A new TikTok Influencer Messenger requirement was introduced. Today the flow supports one commission rate, but the business now needs two: a standard commission rate and a Shop Ads commission rate, because orders generated through paid promotion may use a lower commission. 

## 💬 Original Chinese

> 现在实际上有两个佣金，一个是 Standard Commission Rate，一个是 Shop Ads Commission Rate。

## 🇺🇸 Natural English

> In practice, there are now two commission rates: the Standard Commission Rate and the Shop Ads Commission Rate.

### Alternative Expressions

* Organic and ad-driven orders may use different commission rates.
* We need to support both rates in the same workflow.
* The user should be able to configure both values during invitation setup.

### ⭐ 推荐

> **We need to support both commission rates in the same workflow.**

---

# Topic 20. Why the Second Commission Rate Is Needed

## 💬 Original Chinese

> 如果卖家额外花钱推广达人视频，就不会再按原来的 10% 给佣金。

## 🇺🇸 Natural English

> If the seller pays to promote the creator's video, they may use a lower commission rate for orders generated by that paid traffic.

### Alternative Expressions

* Paid traffic follows a different commission model.
* The seller is already paying for the ad spend.
* Ad-generated orders may have a separate commission rate.

---

# Topic 21. Don't Over-constrain the Relationship Between the Two Fields

## 💬 Original Chinese

> 理论上新比例应该更低，但不做强校验，只要在合法范围内就可以。

## 🇺🇸 Natural English

> In theory, the Shop Ads rate would usually be lower, but we don't want to enforce a strict relationship between the two values. As long as the input is valid, we should accept it. 

### Alternative Expressions

* We shouldn't hard-code a dependency between the two fields.
* Keep validation limited to the allowed range.
* Let the user decide the actual values.

### ⭐ 高频

> **We shouldn't enforce a strict relationship between the two fields.**

---

# Topic 22. Optional Field With Platform Default

## 💬 Original Chinese

> 新加的字段可以不填，TikTok 会有默认规则。

## 🇺🇸 Natural English

> The new field can remain optional, and TikTok will apply its own default behavior if it's not provided. 

### Alternative Expressions

* The field is optional.
* We can rely on TikTok's fallback behavior.
* We don't need to force a value in every case.

### 🧠 Vocabulary

**fallback behavior** = 兜底行为

---

# Topic 23. One Story vs. Multiple Stories

## 💬 Original Chinese

> 如果需求比较小，一个 Sprint 内能做完，就作为一个 Story；大的需求跨多个迭代才拆多个 Story。

## 🇺🇸 Natural English

> If the requirement is small enough to complete within one sprint, keep it as a single story. Only split it into multiple stories if it spans multiple iterations. 

### ⭐ 推荐

> **Keep it as one story if it can be delivered within a single sprint.**

---

# Topic 24. Avoid Process Overhead

## 📌 Meeting Background

Keisha questioned whether maintaining both idea-level tracking and internal Jira stories created unnecessary duplication. The response was that the detailed Jira board gives engineering and QA more granular visibility, but the team also agreed to keep the process lightweight where possible. 

## 💬 Original Chinese

> 我们不要用太多时间在这种 Paperwork 上。

## 🇺🇸 Natural English

> Let's make sure we don't spend too much time on process overhead.

### Alternative Expressions

* Let's keep the process lightweight.
* We should minimize duplicate administrative work.
* The tracking process shouldn't become a burden.

### ⭐ 非常实用

> **Let's keep the process lightweight.**

---

# Topic 25. Upstream API Changes Need Impact Analysis

## 📌 Meeting Background

Another team had changed several APIs and asked the Research team to re-integrate against the new versions. Before creating work, Dongming wanted to understand exactly what changed, which dependencies were affected, and what regression testing would be needed. 

## 💬 Original Chinese

> 首先我们得知道它改了哪些东西，我们的依赖是什么，我们要怎么改。

## 🇺🇸 Natural English

> First, we need to understand what changed, which dependencies are affected, and what changes we need to make on our side.

### ⭐ 很标准

> **We need to understand the impact before we commit to the work.**

---

# Topic 26. API Rename May Be Small, Regression Isn't

## 💬 Original Chinese

> 接口本身改动不大，但是我们这边改完以后还是要做回归。

## 🇺🇸 Natural English

> The API change itself may be small, but we'll still need regression testing after updating our integration.

### Alternative Expressions

* The implementation looks straightforward, but the regression scope is broader.
* We still need to validate all affected consumers.
* A small API change can still have a larger downstream impact.

---

# Topic 27. Main App Refactor – Production Rollout

## 📌 Meeting Background

The team reviewed the remaining Main App refactor rollout. CE regression was around 90% complete, and the next steps included releasing backend pieces to production, running production regression, and coordinating Audience validation. 

## 💬 Original Chinese

> 测试回归到 90% 了，这周先把后端发上去，然后再在线上回归一次。

## 🇺🇸 Natural English

> Regression is about 90% complete. The plan is to deploy the backend this week and then run another round of validation in production.

### Alternative Expressions

* We'll do a staged production rollout.
* Backend goes first, followed by production regression.
* We'll validate the production path before moving on.

---

# Topic 28. Long-running Scheduled-job Migration

## 💬 Original Chinese

> 定时任务比较复杂，测试要专门排时间，所以整个周期会比较长。

## 🇺🇸 Natural English

> The scheduled-job migration is more complex and requires dedicated QA time, so the overall timeline will be longer. 

### Alternative Expressions

* This needs dedicated regression coverage.
* The testing effort is the main driver of the timeline.
* This is not something we can rush.

### ⭐ 高频

> **The testing effort is the main driver of the timeline.**

---

# 📖 Grammar & Expression Notes

### 1. “放进 Backlog”

> **keep it in the backlog**

---

### 2. “从高优先级讲到低优先级”

> **go through the items in priority order**

---

### 3. “旧 API 下线”

> **the legacy API is being sunset**

---

### 4. “前置依赖”

> **prerequisite**

> This is a prerequisite for the next story.

---

### 5. “调研型任务”

> **technical spike**

> **exploratory task**

---

### 6. “尽量复用已有实现”

> **reuse the existing implementation**

> **mirror the existing behavior**

---

### 7. “流程不要太重”

> **keep the process lightweight**

---

### 8. “影响分析”

> **impact analysis**

> We need an impact analysis before we proceed.

---

### 9. “默认兜底”

> **fallback behavior**

---

### 10. “一个 Sprint 内做得完”

> **deliverable within a single sprint**

---

# ⭐ Shadowing Practice

这场建议重点练 **Refinement + Requirement Clarification**：

> **We can keep it in the backlog until we're ready to commit to it.**

> **Let's review these in priority order.**

> **We want to migrate from static credentials to role-based access.**

> **The implementation is complete, but the release path is still unclear.**

> **The current data source is no longer reliable.**

> **Do you have capacity to take this on?**

> **We can reuse the existing implementation.**

> **We have a hard deadline because the legacy API is being sunset.**

> **This is a prerequisite for the next piece of work.**

> **Let's see what we can reuse before building anything new.**

> **We just need enough clarity to understand the intended scope.**

> **We need to support both commission rates in the same workflow.**

> **We shouldn't enforce a strict relationship between the two fields.**

> **Let's keep the process lightweight.**

> **We need to understand the impact before we commit to the work.**

---

# 📚 Today's Vocabulary

| Expression                     | 中文         |
| ------------------------------ | ---------- |
| **candidate work**             | 候选工作       |
| **priority order**             | 优先级顺序      |
| **static credentials**         | 静态凭据       |
| **role-based access**          | 基于角色访问     |
| **release path**               | 发布路径       |
| **reference implementation**   | 参考实现       |
| **sunset an API**              | 停止旧 API    |
| **cutover**                    | 切换         |
| **prerequisite**               | 前置依赖       |
| **technical spike**            | 技术调研任务     |
| **mirror the implementation**  | 复用/对齐已有实现  |
| **centralized key management** | 集中式 Key 管理 |
| **legacy route**               | 遗留路由       |
| **standardize on**             | 统一采用       |
| **fallback behavior**          | 默认兜底行为     |
| **process overhead**           | 流程成本       |
| **impact analysis**            | 影响分析       |
| **regression scope**           | 回归范围       |
| **staged rollout**             | 分阶段发布      |

## ⭐ 今天最值得背的 10 句

> **We can keep it in the backlog until we're ready to commit to it.**

> **Let's review these in priority order.**

> **The implementation is complete, but the release path is still unclear.**

> **The current data source is no longer reliable.**

> **We have a hard deadline because the legacy API is being sunset.**

> **This is a prerequisite for the next piece of work.**

> **We just need enough clarity to understand the intended scope.**

> **We need to support both commission rates in the same workflow.**

> **Let's keep the process lightweight.**

> **We need to understand the impact before we commit to the work.**

