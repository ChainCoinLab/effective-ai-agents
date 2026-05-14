## Status
Recommended

Category: memory-state

## Rule
任务状态用确定性系统管理，不依赖模型记忆。

## Why
模型会遗漏、压缩或误读历史。任务状态如果只存在自然语言上下文中，长流程会出现重复执行、漏步骤和错误恢复。

## Optimize
使用数据库、队列、状态机、检查清单或工作流引擎记录任务状态。模型只读取和建议下一步，状态变更由应用按规则提交。

## Verify
中断并恢复任务，确认系统能从持久状态继续，而不是靠模型猜测上次做到哪里。

## References
- OpenAI Agents SDK: workflows and state
- Durable execution and workflow engine design patterns

---

[返回全局摘要](../README.md) · [返回本组：记忆与状态管理](README.md)
