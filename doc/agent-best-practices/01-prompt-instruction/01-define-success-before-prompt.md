# 先定义成功标准再写 Prompt

[返回全局摘要](../README.md) · [返回本组：提示词与指令](README.md)


## Rule
先写清任务成功标准、失败边界和验收方式，再编写 Prompt。

![Agent 任务模型](../assets/diagrams/agent-task-model.svg)

## Why
没有成功标准的 Prompt 很难评估，只能靠主观感觉调参，容易把问题误判为模型能力不足。

对 Agent 来说，成功标准不是一句“回答要准确”。它决定后续任务模型、上下文构造、工具调用和验证方式。如果成功标准不清楚，模型可能在“看起来差不多”时提前结单，也可能为了完成任务编造证据。

以“分析 README 是否需要更新”为例，弱成功标准是：

```text
给出 README 修改建议。
```

更可执行的成功标准是：

```json
{
  "must_read_files": ["README.md"],
  "must_include_evidence": true,
  "evidence_sources": ["file", "tool_result"],
  "forbidden_without_confirmation": ["write_file"],
  "output_sections": ["问题", "证据", "建议"],
  "failure_policy": "证据不足时说明不能判断，而不是编造"
}
```

这类标准能直接指导工程实现：哪些工具必须调用，哪些动作禁止，最终答案如何校验。

## Optimize
- 把目标拆成可观察的结果、约束和禁止项。
- 为关键场景准备最小验收集。
- 明确“什么结果算失败”。
- 把成功标准拆成确定性标准和语义性标准。
- 对输出格式、证据来源、高风险动作和失败出口分别写清楚。

确定性标准优先交给程序检查：

| 标准 | 检查方式 |
| --- | --- |
| 必须读取某些文件 | trace 中存在对应 `read_file` |
| 必须引用证据 | 输出中的引用能对应 tool result |
| 禁止未确认写操作 | tool trace 中没有未授权写工具 |
| 输出必须符合 schema | JSON Schema 或结构化解析 |

语义性标准再交给人工或 LLM-as-judge 辅助判断：

- 建议是否清楚。
- 结论是否和证据匹配。
- 风险说明是否充分。
- 是否适合目标读者。

## Verify
- 用同一批输入对比 Prompt 版本。
- 检查输出是否逐条满足验收标准。
- 记录失败样例并回填到标准中。
- 检查中间 trace 是否满足“必须发生”和“禁止发生”的步骤。
- 检查证据不足时模型是否会停下、澄清或说明不确定性。

## References
- 项目需求文档
- 线上失败案例
- 评测集和回归用例

---

[返回全局摘要](../README.md) · [返回本组：提示词与指令](README.md)
