# 检索质量和生成质量分开

[返回全局摘要](../README.md) · [返回本组：上下文工程与 RAG](README.md)

## Rule
分别评估检索是否找对材料，以及生成是否正确使用材料。

## Why
RAG 失败可能来自检索召回不足，也可能来自模型忽略证据。混在一起评估会误导优化方向。

只看最终答案，会把不同问题混在一起：

| 失败现象 | 真实原因可能是 | 应该优化 |
| --- | --- | --- |
| 答案编造 | 检索没找到证据，也可能是生成忽略证据 | 先看证据是否进上下文 |
| 答案过时 | 旧文档排在前面 | 索引版本、时间权重、权限过滤 |
| 答非所问 | 查询改写偏移或召回路径错误 | query rewrite、混合检索、rerank |
| 引用不支持结论 | 生成阶段证据绑定失败 | 引用约束、faithfulness 评测 |
| 找到材料但没回答完整 | 上下文扩展不足或生成覆盖率不足 | chunk 扩展、答案结构和 verifier |

检索层的目标是“正确证据进入候选和上下文”；生成层的目标是“输出严格受证据支持”。两者要分开看，否则会出现错误优化：明明是 chunk 切分导致召回不到，却去换更大模型；明明证据已经在上下文里，模型却胡编，却去调 embedding。

## Optimize
- 为检索建立独立的召回率、准确率和排序指标。
- 为生成建立基于证据的一致性指标。
- 在日志中保存查询、候选文档和最终上下文。

检索评估至少关注：

- `context_recall`：标准答案所需证据是否出现在 top-k 或最终上下文中。
- `precision@k`：top-k 里有多少是真相关材料。
- `mrr / ndcg`：正确材料排得是否足够靠前。
- 权限正确性：不该被当前用户看到的资料是否被过滤。
- 新鲜度：是否优先使用最新版本和有效时间内的资料。

生成评估至少关注：

- faithfulness：关键结论是否被上下文支持。
- citation accuracy：引用是否真实支持对应句子。
- coverage：答案是否覆盖用户问题的关键子问题。
- abstention：证据不足时是否拒答或澄清。
- format validity：输出是否符合 schema 或产品要求。

工程上可以把一次 RAG 请求拆成两段日志：

```text
Retrieval Trace:
query -> rewritten_query -> candidates -> reranked -> selected_context

Generation Trace:
selected_context -> answer -> citations -> verifier_result
```

当失败发生时，先问一个问题：正确证据有没有进入 `selected_context`。如果没有，优先查检索；如果有，优先查生成、引用和验证。

## Engineering Notes

- 不要用用户满意度替代检索指标。用户觉得不满意时，链路上可能有多个原因。
- 检索评估需要人工或领域专家标注“应该命中的证据”，否则无法算召回。
- 生成评估不能只看答案像不像标准答案，还要看证据是否支持。
- RAG 系统的版本要包含索引版本、文档版本、chunk 策略、embedding 模型、reranker、Prompt 和生成模型。
- 当知识库更新时，检索回归和生成回归都要跑。

## Verify
- 人工标注查询应命中的文档。
- 检查答案中的关键结论是否被上下文支持。
- 分别统计 retrieval miss 和 generation miss。
- 对同一失败样例记录“正确证据是否被召回”“是否进入最终上下文”“模型是否正确引用”。
- 每次优化后分别报告检索指标和生成指标，避免整体分数掩盖退化。
- 抽查权限过滤和旧版本文档是否影响检索结果。

## References
- 检索评测集
- 生成评测集
- RAG 调试日志
- Context recall / faithfulness 指标
- RAG trace 面板

---

[返回全局摘要](../README.md) · [返回本组：上下文工程与 RAG](README.md)
