## Status
Recommended

Category: tools-agents

## Rule
handoff 传结构化上下文，不只传聊天记录。

## Why
聊天记录冗长且含噪声。接收方需要明确任务目标、已完成事项、关键事实、约束、未决问题和可用资源。

## Optimize
定义交接 schema，包括 objective、state、decisions、evidence、open_questions、next_actions 和 risks。只传接收方完成任务所需内容。

## Verify
让接收 Agent 在不读取完整历史的情况下继续任务，确认它能正确执行下一步并说明依据。

## References
- OpenAI Agents SDK: handoffs
- Structured context and task state patterns

---

[返回全局摘要](../README.md) · [返回本组：工具调用与多 Agent](README.md)
