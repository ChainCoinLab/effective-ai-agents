# 38 LLM-as-judge 需要校准

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)

## Rule
使用 LLM-as-judge 前应用人工标注集校准，并持续检查偏差、一致性和与业务标准的相关性。

## Why
Judge 模型可能偏好长答案、特定语气或表面合理性，也可能受提示词和样例顺序影响。未校准的 judge 会制造虚假的质量信号。

LLM-as-judge 适合评估开放文本，但它本身也是模型，也会犯错。常见偏差包括：偏好更长的答案、偏好自信语气、忽略事实依据、被答案顺序影响、对某些写作风格更宽容、对安全边界判断不稳定。

Judge 不能替代人工标准，它只能在被校准后作为规模化辅助。没有金标集校准的 judge 分数，只能说明“某个模型觉得它好”，不能说明业务上真的好。

## Optimize
建立小规模金标集，对比人工评审和 judge 结果；对评分维度、阈值和解释格式做版本管理。

校准流程：

```text
定义 rubric
-> 人工标注金标集
-> 运行 judge
-> 比较一致率和分歧样例
-> 调整 judge prompt、评分维度和阈值
-> 固定版本
-> 定期复核
```

Rubric 要按任务拆开，不要只给一个总体分。例如 RAG 问答可拆成：

| 维度 | 判断 |
| --- | --- |
| 事实性 | 结论是否正确 |
| 忠实性 | 是否被上下文证据支持 |
| 引用准确性 | 引用是否对应到具体结论 |
| 完整性 | 是否覆盖用户问题 |
| 安全性 | 是否拒绝越权或无证据请求 |
| 格式 | 是否符合输出 schema |

Judge 输出也应结构化：

```json
{
  "score": 4,
  "passed": true,
  "dimensions": {
    "faithfulness": "pass",
    "citation_accuracy": "fail"
  },
  "reason": "第二条引用不能支持对应结论"
}
```

## Engineering Notes

- Judge 不适合检查确定性规则。JSON schema、权限、工具参数、路径范围应由程序检查。
- Judge prompt 和 judge 模型版本要记录，否则历史分数不可比。
- Pairwise judge 和绝对打分各有偏差，关键任务可以组合使用。
- 高风险样例不能完全交给 judge 自动放行，应保留人工复核或规则红线。
- 分歧样例比平均分更有价值，能暴露 rubric 不清或 judge 偏差。

## Verify
定期计算 judge 与人工标注的一致率，并复核分歧最大的样例。

还应检查：

- Judge 是否偏好长答案或固定风格。
- 样例顺序调换后结果是否稳定。
- 不同 judge 版本的评分是否可比较。
- 低分原因是否能指导修复，而不是只给主观评价。

## References
- LLM-as-a-judge evaluation research
- OpenAI Evals model-graded evals
- Human preference evaluation methods
- Rubric 设计
- 人工金标集

---

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)
