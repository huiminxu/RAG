十六、现代 RAG 已经不是"检索+生成"

真正企业级 RAG 更像一个流水线：

                   User Question
                          │
                          ▼
                  Query Rewrite
                          │
                          ▼
                    Retriever
                          │
                          ▼
                     Reranker
                          │
                          ▼
                   Context Builder
                          │
                          ▼
                         LLM
                          │
                          ▼
                Faithfulness Check
                          │
                          ▼
                     Citation
                          │
                          ▼
                    Final Answer

这里：

每增加一层，

都在减少某一种幻觉。

十七、RAG 能缓解哪些幻觉？
幻觉类型	RAG 是否有效	原因
事实幻觉	✅ 非常有效	提供可信知识来源
时间幻觉	✅ 非常有效	可以检索最新资料
企业知识幻觉	✅ 非常有效	检索内部知识库
引用幻觉	✅ 较有效	可以返回真实文档来源
摘要幻觉	⚠️ 有帮助	仍取决于模型是否忠实于原文
推理幻觉	❌ 效果有限	推理能力仍依赖 LLM
数学计算幻觉	❌ 基本无效	应交给计算工具处理
工具调用幻觉	❌ 无效	属于 Agent 调度问题
Memory 幻觉	❌ 无效	属于记忆系统问题
多 Agent 幻觉	❌ 无效	属于协作流程问题
十八、一句话总结

RAG 的本质不是让模型更聪明，而是让模型回答前先"查资料"。

它主要解决的是知识来源不足导致的幻觉，尤其适用于企业知识库、产品文档、内部 Wiki、API 文档等场景。

但如果问题来自推理、计算、工具调用、记忆或多 Agent 协作，仅靠 RAG 并不能解决。这也是为什么现代 AI 系统越来越倾向于把 RAG、Tool Calling、Memory、Agent、Reviewer 组合起来，而不是把 RAG 当成唯一的解决方案。
