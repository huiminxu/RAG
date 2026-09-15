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

