## Status
Recommended

Category: tools-agents

## Rule
优先使用 workflow，必要时再升级为 Agent。

## Why
很多业务流程有清晰步骤和条件，用确定性 workflow 更容易测试、审计和控制。Agent 适合开放式判断、动态规划和工具选择。

## Optimize
先把稳定流程建成工作流，把模型放在需要理解、生成或决策的节点。只有当路径无法提前枚举时，再引入更自主的 Agent。

## Verify
审查每个 Agent 决策点，确认它确实需要模型动态判断，而不是可以用规则、表单或状态机完成。

## References
- OpenAI Agents SDK: workflows versus agents
- Workflow engine design patterns

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
