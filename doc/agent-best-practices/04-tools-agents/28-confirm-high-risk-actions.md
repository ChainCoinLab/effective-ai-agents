## Status
Recommended

Category: tools-agents

## Rule
高风险动作执行前应确认。

## Why
删除、付款、发送外部消息、修改生产数据等动作一旦执行可能难以恢复。确认步骤能降低误解、提示注入和模型误判造成的损失。

## Optimize
按风险分级定义确认策略。确认内容应包含具体动作、目标对象、影响范围和不可逆后果，不使用含糊的“是否继续”。

## Verify
测试删除、覆盖、转账、发信和生产发布路径，确认没有确认令牌或用户确认时无法执行。

## References
- OpenAI Agents SDK: human-in-the-loop
- OWASP: transaction authorization

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
