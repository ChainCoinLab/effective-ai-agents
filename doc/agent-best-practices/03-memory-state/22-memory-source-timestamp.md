## Status
Recommended

Category: memory-state

## Rule
长期记忆应带来源和时间戳。

## Why
记忆不是事实本身，而是某次交互中记录下来的信息。来源和时间能帮助判断可信度、时效性和冲突处理方式。

## Optimize
记录创建时间、更新时间、来源会话或来源系统，以及是否由用户明确确认。展示或使用高影响记忆时优先引用这些元数据。

## Verify
随机读取记忆条目，确认能追溯到来源，并能判断是否需要刷新或废弃。

## References
- OpenAI Agents SDK: tracing and state metadata
- OpenAI Model Spec: transparency and reliability

---

[返回全局摘要](../README.md) · [返回本组：记忆与状态管理](README.md)
