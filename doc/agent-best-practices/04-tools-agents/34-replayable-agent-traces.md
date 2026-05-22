# 34. Agent 轨迹要可回放

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)

## Status
Recommended

Category: tools-agents

## Rule
Agent 轨迹应可回放。

## Why
Agent 系统的问题常发生在长链路中。没有可回放轨迹，就难以定位是提示、上下文、工具、权限还是外部系统导致错误。

Agent 失败很少只是“最终回答不好”。真实失败可能发生在任意一步：上下文没召回、工具选错、参数错、权限误判、工具超时、错误被模型忽略、状态没更新、verifier 没拦住。没有 trace，团队只能看最终输出猜原因。

可回放 trace 要能回答：

- 当时用户目标是什么。
- 系统给模型装配了哪些上下文。
- 模型提出了什么工具调用意图。
- 应用层做了哪些校验和权限判断。
- 工具真实执行了什么，返回了什么。
- 状态如何更新。
- 最终结果为什么被接受或拒绝。

## Optimize
记录输入、模型输出、工具调用意图、实际执行结果、权限决策、错误和最终响应。对敏感字段做脱敏或引用化处理。

最小 trace 结构：

```json
{
  "trace_id": "task_123",
  "step_id": "step_4",
  "event_type": "tool_execution",
  "model_input_ref": "prompt_snapshot_abc",
  "model_output": {
    "type": "tool_call",
    "tool": "read_file",
    "arguments": {"path": "README.md"}
  },
  "policy_decision": "allowed",
  "tool_result_ref": "artifact_tool_result_789",
  "state_patch": {"read_files": ["README.md"]},
  "timestamp": "2026-05-22T10:20:00+09:00"
}
```

Trace 不一定要永久保存完整 Prompt 原文。对敏感内容可以保存引用、hash、脱敏快照和 artifact ID。但必须足够还原关键决策路径，否则无法做评测和审计。

建议记录的事件类型：

| 事件 | 内容 |
| --- | --- |
| `context_built` | 输入来源、token 预算、被裁剪内容 |
| `model_decision` | final、tool_call、clarify、handoff、stop |
| `policy_check` | schema、权限、风险、确认判断 |
| `tool_execution` | 参数、结果、错误、耗时 |
| `state_update` | checkpoint、事实、任务状态变化 |
| `verification` | 验收标准、通过/失败、原因 |
| `handoff` | 发送方、接收方、结构化上下文 |

## Engineering Notes

- Trace 要和版本绑定：Prompt、模型、工具 schema、知识库、代码版本都要能追溯。
- Trace 要支持重放，但重放不应重复执行高风险副作用；写工具要 mock、dry-run 或 require confirmation。
- 日志不是越多越好。要记录可解释决策的结构化字段，而不是只堆文本。
- 敏感字段要脱敏或引用化，并遵守保留期限。
- Trace 应进入 eval 样例和失败分类，而不只是排障日志。

## Verify
选择失败案例重放，确认能复现关键决策路径，并能定位需要修改的提示、工具或策略。

还应测试：

- 给定 trace，能否判断失败发生在检索、生成、工具、权限、状态还是验证。
- 版本变更后，旧 trace 是否仍能解释当时行为。
- 敏感字段是否被脱敏，同时不影响调试。
- 重放时不会重复执行真实删除、付款、发送等副作用。
- 成功样例也能回放，避免只在失败时才有日志。

## References
- OpenAI Agents SDK: tracing
- Observability best practices for distributed systems
- Agent trace schema
- 回放和离线评测流程

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
