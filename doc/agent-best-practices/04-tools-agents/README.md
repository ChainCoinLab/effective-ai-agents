# MCP、工具调用与多 Agent

[返回全局摘要](../README.md)

本模块关注工具接口、权限边界、失败处理、多 Agent 分工、轨迹回放，以及 RAG、MCP、Agent、Skill 的工程化协作。目标是让 Agent 的行动具备可控性、可验证性和可恢复性。

## 实践点

- [25. 工具接口要小而清晰](25-small-clear-tool-interfaces.md)
- [26. 工具描述要写清何时不用](26-tool-description-when-not-to-use.md)
- [27. 模型只提出调用意图，应用负责权限](27-intent-vs-permission.md)
- [28. 高风险动作应确认](28-confirm-high-risk-actions.md)
- [29. 工具失败是正常路径](29-tool-failure-normal-path.md)
- [30. 优先 workflow，再升级 Agent](30-workflow-before-agent.md)
- [31. 多 Agent 要有明确职责边界](31-multi-agent-boundaries.md)
- [32. 多 Agent 的核心是测试和验证](32-multi-agent-test-verification.md)
- [33. Agent handoff 要传结构化上下文](33-structured-handoff-context.md)
- [34. Agent 轨迹要可回放](34-replayable-agent-traces.md)
