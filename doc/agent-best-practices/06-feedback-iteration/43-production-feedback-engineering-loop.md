# 43 生产反馈进入工程闭环

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)


## Rule
生产反馈应进入可追踪的工程闭环，而不是停留在聊天记录、客服备注或临时讨论中。

## Why
Agent 的真实问题通常出现在生产环境。若反馈无法沉淀为样例、缺陷、指标或改进任务，团队会重复处理同类失败。

生产反馈的价值不在“有人觉得不好”，而在它携带真实分布下的失败信号：用户怎么提问、系统拿了什么上下文、调用了什么工具、哪里超时、哪个权限没拦住、最终答案为什么没解决问题。只有把这些信号转成可追踪对象，团队才能持续改进。

反馈来源通常包括：

| 来源 | 价值 |
| --- | --- |
| 用户显式反馈 | 发现答案不可用、体验不好或任务没完成 |
| 人工审核 | 发现事实、合规、安全和格式问题 |
| Trace 异常 | 发现工具失败、循环、成本超限和权限拦截 |
| 业务投诉 | 发现高影响错误和产品流程问题 |
| 指标波动 | 发现版本发布后的系统性退化 |

## Optimize
把用户反馈、人工审核、日志异常和业务投诉统一转换为工单或 eval 样例，并关联版本、trace 和处理结果。

一个生产反馈工单至少包含：

```json
{
  "feedback_id": "fb_2026_05_22_001",
  "task_type": "rag_answer",
  "severity": "P1",
  "user_impact": "用户收到错误政策答案",
  "trace_id": "trace_abc",
  "prompt_version": "rag_v4",
  "model": "model_x",
  "knowledge_version": "refund_policy_index_v3",
  "failure_category": "retrieval_error",
  "expected_behavior": "引用最新退款政策 v3",
  "regression_case_added": true
}
```

反馈闭环要关联版本，否则无法判断问题是新模型带来的、知识库更新带来的，还是旧问题一直存在。

## Engineering Notes

- 不要把用户 thumbs down 直接当训练信号；先做归因和清洗。
- 反馈要分严重度。高风险错误不能和普通体验问题排在同一队列。
- Trace 缺失的反馈价值会下降，因为难以复现和归因。
- 处理结果要回写：已修复、不可复现、产品限制、转人工策略、加入回归。
- 同类反馈要聚合，否则团队会重复处理大量相同问题。

## Verify
抽查生产失败是否能追溯到对应工单、修复记录和回归样例。

还应检查：

- 每个 P0/P1 反馈是否有 trace、版本和负责人。
- 修复后是否有回归样例。
- 同类反馈再次出现时是否能自动关联到历史问题。
- 反馈状态是否闭环，而不是长期停留在“已记录”。

## References
- Closed-loop quality management
- Incident review practices
- Continuous evaluation workflows
- Agent trace
- 生产反馈工单模板

---

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)
