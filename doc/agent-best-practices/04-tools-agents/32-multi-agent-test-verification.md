## Status
Recommended

Category: tools-agents

## Rule
多 Agent 的核心是测试和验证，不是数量。

## Why
增加 Agent 会增加状态、通信和错误传播路径。没有验证体系，多 Agent 只会放大不确定性。

## Optimize
为每个 Agent 定义单元测试、契约测试和端到端任务测试。关键输出由独立验证器、规则或人工审核确认。

## Verify
运行包含成功、失败、冲突和恶意输入的任务集，确认系统能发现错误并给出可追踪原因。

## References
- OpenAI Evals: evaluating model behavior
- OpenAI Agents SDK: tracing and guardrails

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
