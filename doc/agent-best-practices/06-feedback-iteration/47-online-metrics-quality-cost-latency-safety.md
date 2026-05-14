# 47 线上指标同时看质量成本延迟安全

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)


## Rule
线上监控应同时覆盖质量、成本、延迟和安全，不应只看调用成功率或用户满意度。

## Why
Agent 改进常存在权衡：质量提高可能带来成本和延迟上升，工具更多可能增加安全风险。单一指标会误导决策。

## Optimize
建立发布看板，包含任务成功率、人工接管率、拒答率、成本、P95 延迟、首 token 延迟、缓存命中率、工具失败率、安全拦截和投诉率。

## Verify
每次发布后比较新旧版本指标，确认没有在成本、延迟、缓存命中或安全上换取不可接受的质量提升。

## References
- SLO and observability practices
- AI product monitoring
- Cost and latency optimization for LLM systems

---

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)
