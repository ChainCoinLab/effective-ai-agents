# 31. 多 Agent 要有明确职责边界

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)

## Status
Recommended

Category: tools-agents

## Rule
多 Agent 应有清晰职责边界。

## Why
多个 Agent 如果职责重叠，会互相重复、争夺控制权或产生相互矛盾的结论。边界不清会让系统更难调试。

多 Agent 不是把任务分给更多“聪明人”就一定更好。它会引入通信成本、状态同步、权限边界、结果合并和责任归属问题。只有当任务天然存在不同职责、不同上下文或不同验证视角时，多 Agent 才有价值。

常见职责可以这样拆：

| Agent | 负责 | 不负责 |
| --- | --- | --- |
| Planner | 分解任务、定义步骤、分派子任务 | 直接执行高风险工具 |
| Researcher | 检索资料、整理证据 | 做最终业务决策 |
| Coder | 修改代码、运行测试 | 审批上线 |
| Reviewer | 找风险、检查证据和质量 | 直接重写所有实现 |
| Verifier | 验证输出是否满足标准 | 为了通过而放宽标准 |

## Optimize
为每个 Agent 定义输入、输出、可用工具、禁止事项和交接条件。避免多个 Agent 同时拥有同一高风险写入权限。

多 Agent 设计应先写职责契约：

```json
{
  "agent_id": "verification_agent",
  "purpose": "验证实现是否满足成功标准",
  "inputs": ["task_spec", "changed_files", "test_results", "trace"],
  "outputs": ["findings", "pass_fail", "blocking_risks"],
  "tools": ["read_file", "run_tests"],
  "forbidden": ["write_file", "deploy", "change_requirements"],
  "handoff_condition": "verification_complete_or_blocked"
}
```

职责边界要覆盖四件事：

- 信息边界：它能看到哪些上下文，哪些不需要给它。
- 工具边界：它能调用哪些工具，哪些工具禁止。
- 决策边界：它能建议什么，什么必须交给主流程或人类。
- 输出边界：它必须产出什么结构，谁消费这个输出。

多 Agent 系统最好保留一个明确的 owner。可以是主 Agent、workflow 或应用调度器。不要让多个 Agent 同时决定任务是否完成、是否发布、是否写入生产。

## Engineering Notes

- 不要为了“多 Agent”而多 Agent。一个 workflow 加少量模型节点往往更稳定。
- 写权限要集中控制。多个 Agent 同时写同一资源会带来冲突和难以审计的副作用。
- 交接内容要结构化，不能只传聊天记录。
- Agent 输出要可比较、可合并。否则主流程只能让另一个模型凭感觉总结。
- 每个 Agent 的 prompt、工具集和评测集都要独立版本化。

## Verify
用同一任务追踪每个 Agent 的贡献，确认没有重复调用、职责漂移或无人负责的步骤。

还应测试：

- 两个 Agent 给出冲突结论时，系统如何裁决。
- 子 Agent 失败或超时时，主流程是否能降级或转人工。
- 子 Agent 是否尝试调用不属于自己的工具。
- handoff 后接收方能否在不读完整历史的情况下继续。
- 最终结果能否追溯到每个 Agent 的输入和输出。

## References
- OpenAI Agents SDK: multi-agent orchestration
- Distributed systems: ownership and interface boundaries
- Agent handoff schema
- 多 Agent trace

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
