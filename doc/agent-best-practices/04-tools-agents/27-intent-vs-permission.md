## Status
Recommended

Category: tools-agents

## Rule
模型只提出工具调用意图，应用负责权限判断和执行。

## Why
模型不应成为权限边界。真正的授权、审计、速率限制和数据访问控制应在应用层执行。

## Optimize
把工具调用拆成“模型建议”和“应用校验”。应用根据用户身份、资源权限、风险等级和策略决定是否执行、拒绝或要求确认。

## Verify
模拟越权资源、缺少权限和高风险操作，确认模型即使提出调用，应用也能阻止执行。

## References
- OpenAI Agents SDK: guardrails and tool execution
- OWASP: access control principles

---

[返回全局摘要](../README.md) · [返回本组：工具调用与多 Agent](README.md)
