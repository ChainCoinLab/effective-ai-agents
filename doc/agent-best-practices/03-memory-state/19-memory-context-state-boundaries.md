## Status
Recommended

Category: memory-state

## Rule
区分短期上下文、长期记忆和业务状态，不把三者混用。

## Why
短期上下文服务当前对话，长期记忆服务跨会话偏好，业务状态服务产品事实。混用会导致过期信息、隐私风险和不可预测行为。

## Optimize
为三类数据定义独立存储、生命周期和读写入口。业务状态优先来自权威系统，长期记忆只存稳定偏好和用户明确希望保留的信息。

## Verify
检查同一条信息是否能回答：来源在哪里、何时失效、由谁更新、是否允许跨会话使用。

## References
- OpenAI Agents SDK: Context management
- OpenAI Model Spec: memory and personalization principles

---

[返回全局摘要](../README.md) · [返回本组：记忆与状态管理](README.md)
