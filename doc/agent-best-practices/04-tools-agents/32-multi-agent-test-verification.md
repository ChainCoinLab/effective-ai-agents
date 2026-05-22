# 32. 多 Agent 的核心是测试和验证

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)

## Status
Recommended

Category: tools-agents

## Rule
多 Agent 的核心是测试和验证，不是数量。

## Why
增加 Agent 会增加状态、通信和错误传播路径。没有验证体系，多 Agent 只会放大不确定性。

多 Agent 系统的复杂度来自组合：一个 Agent 的小错误可能被下一个 Agent 当成事实继续放大；Planner 分错任务，Worker 可能做得很努力但方向错；Reviewer 没发现证据缺口，最终输出就会带着假确定性进入用户或生产系统。

因此，多 Agent 的价值不在“数量”，而在“分工后能否被验证”：

| 层级 | 要验证什么 |
| --- | --- |
| 单个 Agent | 输入输出契约、工具选择、拒答和边界 |
| Agent 间交接 | handoff 内容完整、无噪声、可恢复 |
| 调度流程 | 顺序、并行、超时、失败、重试和熔断 |
| 结果合并 | 冲突解决、证据保留、责任归属 |
| 端到端目标 | 最终结果是否满足用户成功标准 |

## Optimize
为每个 Agent 定义单元测试、契约测试和端到端任务测试。关键输出由独立验证器、规则或人工审核确认。

测试可以分层设计：

```text
Agent unit eval
-> Handoff contract test
-> Tool permission test
-> Orchestration integration test
-> End-to-end task eval
-> Production trace sampling
```

每个子 Agent 至少要有：

- 输入样例：正常、缺字段、冲突、恶意输入。
- 输出 schema：字段、枚举、证据、错误状态。
- 工具边界：允许工具和禁止工具。
- 成功标准：什么叫完成，什么叫 blocked。
- 失败处理：超时、低置信、权限不足、证据不足时怎么返回。

关键任务应设置独立 verifier。Verifier 不应只看最终文案，还要看 trace：哪些 Agent 参与、读了哪些证据、调了哪些工具、是否越权、是否有冲突未处理。

## Engineering Notes

- 多 Agent 的评测要保留中间轨迹，否则无法定位哪个 Agent 出错。
- 并行 Agent 的输出顺序不可依赖，要用结构化合并逻辑。
- 不要让负责生成的 Agent 自己验证自己，至少高风险场景要有独立验证。
- 测试集要包含子 Agent 失败和矛盾输出，不要只测全员成功。
- Agent 数量增加后，成本、延迟和失败概率都要进入发布门禁。

## Verify
运行包含成功、失败、冲突和恶意输入的任务集，确认系统能发现错误并给出可追踪原因。

还应检查：

- 每个 Agent 的输出都能单独重放和评测。
- handoff 缺字段时接收 Agent 不会猜测。
- 冲突结论会进入裁决流程，而不是被模型随意合并。
- 子 Agent 失败不会导致主流程编造结果。
- 多 Agent 改动后能跑相关回归集。

## References
- OpenAI Evals: evaluating model behavior
- OpenAI Agents SDK: tracing and guardrails
- 多 Agent 编排测试
- Handoff contract testing

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
