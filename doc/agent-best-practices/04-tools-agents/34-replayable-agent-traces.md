## Status
Recommended

Category: tools-agents

## Rule
Agent 轨迹应可回放。

## Why
Agent 系统的问题常发生在长链路中。没有可回放轨迹，就难以定位是提示、上下文、工具、权限还是外部系统导致错误。

## Optimize
记录输入、模型输出、工具调用意图、实际执行结果、权限决策、错误和最终响应。对敏感字段做脱敏或引用化处理。

## Verify
选择失败案例重放，确认能复现关键决策路径，并能定位需要修改的提示、工具或策略。

## References
- OpenAI Agents SDK: tracing
- Observability best practices for distributed systems

---

[返回全局摘要](../README.md) · [返回本组：工具调用与多 Agent](README.md)
