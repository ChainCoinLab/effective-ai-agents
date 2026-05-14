# 36 Eval 数据覆盖真实分布和边界

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)


## Rule
Eval 数据集应同时覆盖真实生产分布、高频场景、长尾边界、异常输入和高风险任务。

## Why
只用理想样例会高估系统能力。真实用户输入常包含歧义、缺失信息、噪声、冲突目标和超出预期的边界条件。

## Optimize
从生产日志、客服问题、失败案例和领域专家样例中采样，并为边界样例单独打标签，避免被平均分掩盖。

## Verify
每次评测报告都按场景类型拆分结果，确认高频样例和边界样例都有独立通过率。

## References
- OpenAI Evals dataset design
- Anthropic evaluation guidance
- ML data validation practices

---

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)
