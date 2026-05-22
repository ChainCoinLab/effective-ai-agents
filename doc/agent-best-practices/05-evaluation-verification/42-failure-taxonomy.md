# 42 失败分类

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)

## Rule
所有评测失败都应归入稳定分类，例如理解错误、检索错误、工具错误、事实错误、安全错误、格式错误和体验错误。

## Why
没有分类的失败只能形成零散 bug。稳定分类能帮助团队识别系统性弱点，决定是改 prompt、数据、工具、模型还是产品约束。

失败分类的价值在于指导修复。如果所有问题都叫“模型回答不准确”，团队会反复调 Prompt；但真实根因可能是检索没召回、工具报错、权限策略错误、状态丢失、知识库过期或评测标准不清。

建议最小分类：

| 类别 | 表现 | 常见修复方向 |
| --- | --- | --- |
| 意图理解错误 | 误解用户目标或风险等级 | Prompt、示例、澄清策略 |
| 检索错误 | 没召回正确证据、排序错误 | chunk、query、索引、rerank |
| 生成错误 | 证据在上下文里但回答不忠实 | 输出约束、引用验证、模型 |
| 工具错误 | 选错工具、参数错、工具失败 | schema、描述、错误处理 |
| 权限安全错误 | 越权、泄露、跳过确认 | 应用层权限、确认、红队样例 |
| 状态错误 | 重复执行、漏步骤、中断不可恢复 | 状态机、checkpoint、幂等 |
| 格式错误 | JSON/schema 不合法 | 结构化输出、解析修复 |
| 体验错误 | 过度冗长、拒答不清、下一步不明确 | UX 文案、任务出口 |

## Optimize
维护轻量失败 taxonomy，并允许样例有主因和次因。分类口径变化时记录版本，避免历史趋势不可比。

失败记录建议包含：

```json
{
  "case_id": "eval_2026_05_22_001",
  "primary_category": "retrieval_error",
  "secondary_categories": ["generation_error"],
  "severity": "P1",
  "risk_type": "wrong_policy_answer",
  "root_cause": "refund policy v3 chunk not indexed",
  "fix_owner": "rag",
  "regression_added": true
}
```

主因和次因要分开。比如答案幻觉可能是生成错误，但如果正确证据根本没进上下文，主因就是检索错误。分类错误会导致修错层。

## Engineering Notes

- 分类不要过细。过细会增加标注成本，过粗会失去诊断价值。
- 严重程度和失败类型分开。格式错误可能是低风险，也可能在工具参数中造成高风险。
- Taxonomy 版本要记录。分类口径变化后，历史趋势不能直接比较。
- 每类高频失败要有负责人，不然分类只是报表。
- 失败样例要进入回归集，修复后用同类样例验证趋势是否下降。

## Verify
查看评测报告是否按失败类别聚合，并确认每类高频失败都有负责人和后续处理状态。

还应检查：

- 是否能从分类直接推导修复方向。
- 是否存在大量“其他”类别，说明 taxonomy 不够清楚。
- 同一个失败是否被不同评审者稳定归类。
- 修复后对应类别失败率是否下降，而不是总分偶然上涨。

## References
- Defect taxonomy
- Error analysis in ML systems
- Incident categorization practices
- Agent failure analysis
- Eval 报告模板

---

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)
