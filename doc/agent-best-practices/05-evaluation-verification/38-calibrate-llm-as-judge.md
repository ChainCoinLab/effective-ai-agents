# 38 LLM-as-judge 需要校准

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)


## Rule
使用 LLM-as-judge 前应用人工标注集校准，并持续检查偏差、一致性和与业务标准的相关性。

## Why
Judge 模型可能偏好长答案、特定语气或表面合理性，也可能受提示词和样例顺序影响。未校准的 judge 会制造虚假的质量信号。

## Optimize
建立小规模金标集，对比人工评审和 judge 结果；对评分维度、阈值和解释格式做版本管理。

## Verify
定期计算 judge 与人工标注的一致率，并复核分歧最大的样例。

## References
- LLM-as-a-judge evaluation research
- OpenAI Evals model-graded evals
- Human preference evaluation methods

---

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)
