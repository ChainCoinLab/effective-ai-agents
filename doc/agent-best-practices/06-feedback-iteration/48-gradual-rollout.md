# 48 灰度发布

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)


## Rule
Agent 能力、模型、prompt、工具和知识库更新应优先灰度发布，逐步扩大流量。

## Why
离线评测无法覆盖所有真实输入。灰度发布能在影响范围受控的情况下发现质量、成本、延迟和安全问题。

## Optimize
按用户、任务类型、风险等级或流量比例分阶段放量，并设置自动回滚条件和人工停止开关。

## Verify
灰度期间检查关键指标和抽样 trace，确认达到放量标准后再进入下一阶段。

## References
- Canary release
- Feature flags
- Progressive delivery

---

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)
