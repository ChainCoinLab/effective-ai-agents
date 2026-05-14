## Status
Recommended

Category: tools-agents

## Rule
多 Agent 应有清晰职责边界。

## Why
多个 Agent 如果职责重叠，会互相重复、争夺控制权或产生相互矛盾的结论。边界不清会让系统更难调试。

## Optimize
为每个 Agent 定义输入、输出、可用工具、禁止事项和交接条件。避免多个 Agent 同时拥有同一高风险写入权限。

## Verify
用同一任务追踪每个 Agent 的贡献，确认没有重复调用、职责漂移或无人负责的步骤。

## References
- OpenAI Agents SDK: multi-agent orchestration
- Distributed systems: ownership and interface boundaries

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
