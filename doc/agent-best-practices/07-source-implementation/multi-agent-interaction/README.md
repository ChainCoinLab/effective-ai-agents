# 多 Agent 交互与调度

[返回源码实现](../README.md)

这个教程从 Code Review 场景切入，讲主 Agent 和子 Agent 怎么分工、怎么传消息、怎么分发任务、怎么汇总结果。

它从单个 Review Agent 开始，再逐步加 Planning Agent、Verification Agent、子 Agent 创建、消息分发、任务分发、顺序调度和协同汇总。

## 学习路径

| 顺序 | 学习点 | 本节只解决什么问题 |
| --- | --- | --- |
| 01 | [Code Review Agent](01-code-review-agent.md) | 基于文件读取工具输出结构化代码审查结果 |
| 02 | [Planning Agent](02-planning-agent.md) | 先把复杂任务拆成步骤、文件范围和验收标准 |
| 03 | [Verification Agent](03-verification-agent.md) | 独立复查 Review 结果是否有证据、是否误报 |
| 04 | [创建子 Agent](04-create-sub-agent.md) | 主 Agent 根据任务创建不同角色的子 Agent |
| 05 | [主 Agent 和子 Agent 的消息分发](05-message-task-dispatch.md) | 定义消息结构、任务结构和结果回传结构 |
| 06 | [顺序调度多个 Agent](06-sequential-dispatch.md) | 一个任务先交给 A，再交给 B，再汇总 |
| 07 | [多 Agent 协同完成 Code Review](07-collaborative-code-review.md) | Planner、Reader、Reviewer、Verifier 协同输出最终报告 |
| 08 | [并行分发和结果合并](08-parallel-merge.md) | 多个子 Agent 同时处理不同文件，再由主 Agent 合并 |

## 最终工作场景

```text
用户提交代码审查任务
  ↓
Coordinator Agent 接收任务
  ↓
Planner Agent 拆计划
  ↓
Reader Agent 读取相关文件
  ↓
Review Agent 找问题并给出文件行号
  ↓
Verify Agent 复查结论和证据
  ↓
Reporter Agent 汇总最终报告
```

