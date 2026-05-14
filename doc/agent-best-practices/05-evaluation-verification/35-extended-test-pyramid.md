# 35 AI 系统需要扩展测试金字塔

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)


## Rule
AI 系统测试不应只停留在单元测试，需要覆盖 prompt、检索、工具调用、模型输出、端到端任务和线上监控。

## Why
LLM 行为具有概率性，失败可能来自上下文、工具、模型版本或任务编排。传统测试金字塔不足以发现这些组合风险。

## Optimize
把测试分层：确定性代码用单元测试，Agent 流程用集成测试，关键任务用 eval，生产行为用监控和抽样复核。

## Verify
检查每个关键用户任务是否至少有一条端到端 eval，并确认工具调用、检索结果和最终输出都有可观测记录。

## References
- OpenAI Evals
- Google ML Test Score
- Martin Fowler: Test Pyramid

---

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)
