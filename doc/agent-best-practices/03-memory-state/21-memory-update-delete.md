## Status
Recommended

Category: memory-state

## Rule
记忆应支持更新和删除，不应只追加。

## Why
用户偏好、身份信息和项目背景会变化。旧记忆如果无法修正，会让 Agent 持续使用错误前提。

## Optimize
为记忆设置稳定标识、版本或合并策略。允许用户显式更正、删除，也允许系统在发现冲突时标记旧记忆失效。

## Verify
测试“用户改变偏好”和“用户要求忘记”两类路径，确认后续回答不再使用旧内容。

## References
- OpenAI Model Spec: correction and user control
- OpenAI Agents SDK: persistent state

---

[返回全局摘要](../README.md) · [返回本组：记忆与状态管理](README.md)
