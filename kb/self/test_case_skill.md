重构接口测试 Skill 使用说明

1. 目标

这套 Skill 用于测试“旧接口 / 新重构接口”的响应一致性。当前实践来自 Listing Builder PHP → Java 重构测试，但流程可以复用到其他模块。

核心目标：

用真实测试环境触发接口，保留最接近用户行为的请求数据。

让 Cursor 根据固定规则生成正常、异常、边界测试用例。

对旧接口和新接口做响应对比。

自动区分：通过、需要提 Bug、按规则忽略、需要人工复核。

每次测试后更新 Excel 测试记录。

对确认的问题创建 Jira Bug，并回填到 Excel。

2. 推荐工作方式

打开测试环境页面。

按真实业务流程触发接口。

在 Chrome DevTools Network 中找到旧接口请求和新接口请求。

分别复制为 cURL。

把两个 cURL 发给 Cursor。

要求 Cursor 读取本页 Skill 文档并执行对比。

Cursor 输出对比结论、创建 Jira Bug、更新 Excel。

推荐给 Cursor 的 Prompt：

请读取 Confluence 页面：
https://pacvue-enterprise.atlassian.net/wiki/spaces/PTT/pages/1584234520/Skill

然后按照文档中的重构接口测试 Skill 流程，对我提供的旧接口和新接口 cURL 做接口一致性对比。

要求：
1. 覆盖正常场景、异常场景、边界场景。
2. 按 Skill 规则判断 Pass / Fail / 忽略。
3. 需要提 Bug 的，创建到对应父任务下并分配给研发。
4. 每个测试用例都要更新到 Excel 测试记录。
5. 最终总结哪些是 Bug，哪些按规则忽略，Excel 是否已更新。

如果当前模块不是 Listing Builder，需要补充父任务 Jira、研发负责人、Excel 文件路径、旧接口和新接口。

3. 测试用例设计原则

每个接口至少覆盖：

正常成功路径。

缺失必填参数。

参数为 null。

参数为空字符串或空数组。

参数类型错误。

数值边界，例如 0、-1、超大 ID、不存在 ID。

对写入/删除接口，需要控制有效请求次数，避免污染数据。

删除类接口默认不重复执行用户已经成功触发过的有效删除请求；可以执行不会删除真实数据的异常/边界用例；成功场景可以基于用户提供的 Network 截图或响应内容记录。

4. 对比维度

Cursor 需要对比：

HTTP Status。

响应 JSON 结构。

关键字段是否存在。

关键字段值是否一致。

错误 message 语义是否一致。

是否暴露 SQL、Mapper、MyBatis、堆栈、数据库异常等内部信息。

成功响应语义是否一致。

动态字段是否需要忽略，例如 ID、timestamp、traceId。

5. 判断结果定义

Excel 中只记录两种测试结果：

结果

含义

Pass

响应一致，或者差异命中 Skill 忽略规则

Fail

需要提 Bug，或者需要人工复核

Cursor 内部分析时可以先分为：Pass、Bug、Ignored、Need Review。其中 Ignored 在 Excel 中记为 Pass，Need Review 在 Excel 中记为 Fail。

6. 当前通用忽略规则

以下场景默认不提 Java parity Bug。

6.1 message 文案差异但语义一致

如果只是 message 文案不同，但 Java message 也表达了正确意思，可以忽略。

如果 Java message 语义错误、缺失关键信息、会误导调用方，则不能忽略。

6.2 400 vs 404 差异

400 和 404 的差异可以忽略。

但以下情况不能忽略：

一边 200，另一边错误码。

一边 4xx，另一边 5xx。

Java 返回 500 并暴露内部异常。

6.3 HKB-2215：PHP 非法参数返回 500，Java 合理返回 400/422

非法参数场景下，PHP 返回 500，但 Java 返回合理的 400 或 422 参数校验错误，这属于 PHP 既有问题，不作为 Java parity Bug。

Excel 记为 Pass，场景说明写：规则：HKB-2215。

6.4 PHP 字段为 null，Java 省略字段

如果 PHP 返回某字段且值为 null，Java 默认不返回该字段，可以忽略。

Excel 记为 Pass。

6.5 HKB-2221：布尔字段非法字符串，PHP 宽松，Java 严格校验

布尔字段传入非法字符串时，PHP 宽松处理返回 200，Java 严格校验返回合理 400，可以忽略。

Excel 记为 Pass，场景说明写：规则：HKB-2221。

6.6 HKB-2225：accountId 跨账号取数 vs x-pacvue-token 当前用户取数

PHP 通过 accountId 跨账号查询，但 Java 只通过 x-pacvue-token 获取当前用户数据，这属于 Java 更安全的设计，不作为 Bug。

Excel 记为 Pass，场景说明写：规则：HKB-2225。

6.7 HKB-2222：Java Jackson scalar 自动转字符串

Java Jackson StringDeserializer 默认允许 scalar 强转为 String。

示例：keywords: [123] 会被反序列化为 ["123"]。

这类数组元素数字被 Java 转字符串并返回成功的差异，不作为 Java parity Bug。

Excel 记为 Pass，场景说明写：规则：HKB-2222。

6.8 HKB-2230：删除 listing 成功响应内容前端不展示

删除 listing 的成功响应内容前端不展示，因此 delete-listing 成功场景下，PHP 返回 Listing deleted successfully，Java 返回 OK 这类仅成功 message 或包装结构不同的差异，不作为 Java parity Bug。

Excel 记为 Pass，场景说明写：规则：HKB-2230。

注意：该规则仅适用于确认前端不展示/不依赖返回内容的删除成功响应。若前端依赖响应字段或数量字段，例如批量删除的 totalDeleted / data，仍需要按具体场景判断。

6.9 删除类接口成功响应体差异，前端不依赖时忽略

删除类接口成功场景下，如果前端不依赖返回体，PHP 返回刷新后的业务数据、Java 返回 OK 或空包装这类成功响应内容/结构差异不需要判断为 Bug。

示例：delete-from-keyword-bank 正常删除后，PHP 返回完整 keyword bank 数据，而 Java 返回 OK；只要两端都是成功语义，按删除成功响应规则忽略。

Excel 记为 Pass，场景说明写：规则：删除类成功响应前端不依赖返回体。

注意：如果前端依赖返回体里的业务字段、删除数量、刷新后的列表数据，或者一边成功一边失败，则不能套用该规则，需要提 Bug 或进入人工复核。

6.10 HKB-2240：calculate-metrics-data 图片/视频/coupon 字段差异

calculate-metrics-data 正常响应中，如果 Java qualityScoreResponse 不返回 PHP 中的 imageUrl、images、videos、coupon 相关字段，这类字段差异后续不作为 Java parity Bug。

Excel 记为 Pass，场景说明写：规则：HKB-2240。

6.11 HKB-2247：删除类接口空字符串/空删除项，PHP 宽松 200，Java 严格 400

删除类接口中空字符串或空删除项这类无效/空操作入参，PHP 宽松处理为 200 空结果，Java 严格校验返回合理 400，可以忽略。

示例：delete-from-keyword-bank 的空 keywords[]，PHP 返回 200 []，Java 返回 400 keywords must not be empty。

Excel 记为 Pass，场景说明写：规则：HKB-2247。

6.12 HKB-2248：删除类接口集合参数传成字符串，PHP 宽松 200，Java 严格 400

删除类接口中集合参数传成字符串等类型不匹配入参，PHP 宽松处理为 200，Java 严格校验返回合理 400，可以忽略。

示例：delete-image-preset-prompt 的 presetIds: "69"，PHP 返回 200 删除成功，Java 返回 400 presetIds is invalid。

Excel 记为 Pass，场景说明写：规则：HKB-2248。

7. 必须提 Bug 的场景

以下场景一般需要提 Bug。

7.1 成功 / 失败不一致

一边返回 200，另一边返回错误码。

如果该差异已经命中明确忽略规则，例如 HKB-2221、HKB-2247、HKB-2248，则不提 Bug，Excel 记为 Pass。

7.2 状态码类别不一致

一边 4xx，另一边 5xx。

7.3 Java 暴露内部异常

Java response 中出现 SQL、PostgreSQL、MyBatis、Mapper 路径、BatchExecutorException、stack trace 等内部实现细节时，需要提 Bug。

7.4 成功响应结构或语义不一致

成功请求都返回 200，但响应结构或成功语义不一致，需要判断前端/调用方是否依赖。

若前端不展示也不依赖，且已沉淀为明确规则，例如 HKB-2230、HKB-2240 或删除类成功响应规则，可忽略；否则仍应提 Bug 或进入人工复核。

7.5 关键业务字段值不一致

正常成功场景下，关键业务字段不同，通常需要提 Bug。

8. Excel 记录规范

每次对比完成后，必须更新 Excel。

Test Cases 固定使用以下列：

列名

说明

接口名称

使用短接口名，例如 add-note、delete-listing

用例场景（中文描述）

中文描述场景、入参、差异、命中规则

PHP结果

PHP 状态码和关键响应摘要

Java结果

Java 状态码和关键响应摘要

测试结果（Pass/Fail）

只写 Pass 或 Fail

Bug链接

如果提了 Bug，写完整 Jira 链接；否则留空

Summary 建议包含：接口名称、用例数、Pass、Fail、Bug链接。

Excel 结果规则：

完全一致：Pass。

命中忽略规则：Pass。

已提 Bug：Fail。

需要人工复核：Fail。

复测已创建的 Jira Bug 时，也必须更新同一个 Excel 测试记录：按复测用例追加或更新记录，写明复测日期/场景、Java 当前结果、是否修复。

复测通过记为 Pass，并保留对应 Jira 链接；复测未通过仍记为 Fail，并保留对应 Jira 链接。

如果复测通过并把 Jira 状态改为 Done，Excel 中也必须能看出该 Bug 对应场景已复测通过，不能只改 Jira 状态而不更新测试用例。

9. Jira Bug 创建规范

默认创建为父任务下的 Dev Bug (Sub-task)。

Jira 描述必须包含：测试接口、PHP URL、Java URL、失败用例、请求参数、PHP 实际响应、Java 实际响应、期望行为、影响、已按 Skill 规则过滤的差异。如果来自截图，需要说明“由用户提供的 Network 截图确认”。

Jira Summary 建议格式：

Java <接口名> <场景>，未对齐 PHP <结果>

10. Cursor 执行清单

读取本 Confluence Skill 文档。

解析用户提供的 PHP 和 Java cURL。

判断接口是否会写入或删除数据。

对危险成功请求谨慎执行，必要时只使用用户已提供的 Network 响应。

设计正常、异常、边界测试用例。

调用 PHP 和 Java 接口。

对比 status、body、message、关键字段和内部异常。

按 Skill 规则判断 Pass / Fail。

对 Fail 且确认是 Java parity 问题的场景创建 Jira。

更新 Excel Test Cases 和 Summary。

如果是复测 Jira Bug，先更新 Excel 复测记录，再按结果推进 Jira 状态。

最终回复用户：测试范围、Bug 列表、忽略列表、Excel 是否已更新。

11. 推荐最终回复格式

已完成 <接口名> 对比，并已更新 Excel。

覆盖用例：正常 / 异常 / 边界，共 X 条。

创建 Bug：
- HKB-xxxx：问题摘要
- HKB-yyyy：问题摘要

按 Skill 规则忽略：
- xxx 场景，命中 HKB-2215
- xxx 场景，命中 400/404 忽略规则

Excel 当前统计：Pass X，Fail Y。

12. 如何新增忽略规则

当研发在 Jira comment 中确认某类差异无需处理时，需要把该场景沉淀到本 Skill 文档。

新增规则时必须记录：Jira Key、场景描述、为什么可以忽略、后续 Excel 如何记录。

13. 当前已沉淀规则索引

规则

说明

Excel

message 语义一致

仅文案不同，但 Java 语义正确

Pass

400/404 忽略

400 vs 404 可忽略

Pass

HKB-2215

PHP 非法参数 500，Java 合理 400/422

Pass

PHP null Java omitted

PHP 字段为 null，Java 省略字段

Pass

HKB-2221

布尔字段非法字符串，PHP 宽松，Java 严格校验

Pass

HKB-2225

PHP accountId 跨账号，Java x-pacvue-token 当前用户

Pass

HKB-2222

Java Jackson scalar 自动转 String

Pass

HKB-2230

删除 listing 成功响应前端不展示，成功 message/包装差异忽略

Pass

删除类成功响应前端不依赖返回体

PHP 返回刷新数据，Java 返回 OK / 空包装，只要成功语义一致且前端不依赖返回体即可忽略

Pass

HKB-2240

calculate-metrics-data 的图片、视频、coupon 字段差异不再作为错误判断

Pass

HKB-2247

删除类接口空字符串/空删除项入参，PHP 宽松 200、Java 合理 400 不再作为错误判断

Pass

HKB-2248

删除类接口集合参数传字符串等类型不匹配入参，PHP 宽松 200、Java 合理 400 不再作为错误判断

Pass

Jira Bug 复测记录

每次复测已创建 Bug 后，Excel 必须记录复测结果；Done 前也必须能在 Excel 中看出复测通过

Pass 或 Fail，保留 Bug 链接

14. 注意事项

不要把所有差异都机械地提 Bug，必须先套用 Skill 规则。

不要因为 Java message 文案不同就提 Bug，除非语义错误。

删除和写入接口不要重复跑有效成功请求，除非用户明确允许。

如果响应中有 SQL / MyBatis / Mapper / PostgreSQL 等内部信息，即使状态码同为 500，也需要考虑提安全/异常泄露 Bug。

Excel 是团队交付物，必须保持中文场景描述清楚，方便非执行人复盘。

如果 Skill 规则变化，要回填更新历史 Excel 中受影响的用例结果。

复测 Bug 后不要只更新 Jira 状态；必须同步更新 Excel 测试用例记录。

HKB-2240、HKB-2247、HKB-2248 已确认不需要作为错误判断，后续遇到相同场景按对应规则记录为 Pass。