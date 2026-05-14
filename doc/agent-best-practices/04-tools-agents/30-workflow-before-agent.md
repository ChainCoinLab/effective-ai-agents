## Status
Recommended

Category: tools-agents

## Rule
优先使用 workflow，必要时再升级为 Agent。固定流程、长文本多轮任务，以及 RAG、MCP、Skill、Tool 多模块协作，都应先设计成可观察、可恢复、可验证的工作流。

## Why
很多业务流程有清晰步骤和条件，用确定性 workflow 更容易测试、审计和控制。Agent 适合开放式判断、动态规划和工具选择。

很多 AI 应用失败，不是因为缺少 Agent，而是因为把本该由 workflow 管理的职责交给了模型自由发挥：

| 场景 | 直接交给自主 Agent 的风险 | workflow 应承担的职责 |
| --- | --- | --- |
| 固定业务流程 | 越权、漏步骤、难审计 | 状态机、权限、审批、幂等和回滚 |
| 长文本多轮任务 | 上下文爆炸、死循环、幻觉修复、无法结单 | 分块、状态表、验证、熔断和结单 |
| RAG + Tool 协作 | 分不清查知识还是执行动作 | 检索、证据引用、工具权限和任务状态分层 |
| MCP 暴露多系统 | 统一接口变成统一风险入口 | 资源、只读工具、写工具和高风险工具分级控制 |
| Skill 复用流程 | Skill 只剩角色设定，Agent 临场猜 | 触发条件、前置检查、执行步骤和质量标准 |

## Optimize
先把稳定流程建成工作流，把模型放在需要理解、生成或决策的节点。只有当路径无法提前枚举时，再引入更自主的 Agent。

工作流设计时先明确模块职责：

- Agent 负责规划、路由和整合，但不能绕过权限和状态机。
- Skill 负责流程、模板、检查清单和经验复用。
- MCP 负责标准化连接资源和工具，并暴露清晰的能力边界。
- RAG 负责提供可引用的知识证据，不负责执行动作。
- Tool 负责执行动作并返回结构化结果。
- Workflow、权限、审计和人审负责控制风险。

长文本或长链路任务要拆成可执行单元，并用状态表管理进度：

| 字段 | 作用 |
| --- | --- |
| `unit_id` | 当前文本块、文件、日志段或子任务 |
| `status` | pending、running、passed、failed、needs_review、skipped |
| `attempts` | 已尝试次数 |
| `last_observation` | 最近一次工具结果、错误摘要或验证反馈 |
| `evidence_refs` | 本轮结论依赖的原文位置、chunk、行号或工具输出 |
| `open_issues` | 未解决问题和阻塞点 |
| `next_action` | 下一轮要执行的动作 |

工具失败时，把错误转成结构化 observation，而不是把完整日志堆进上下文：

```json
{
  "unit_id": "file:src/report.py",
  "tool": "python_interpreter",
  "status": "failed",
  "error_type": "ZeroDivisionError",
  "traceback_excerpt": [
    "File \"report.py\", line 42",
    "rate = total / count",
    "ZeroDivisionError: division by zero"
  ],
  "attempt": 2,
  "max_attempts": 3,
  "suggested_next_action": "检查 count 为 0 的分支，不要重写无关逻辑。"
}
```

为多轮任务设置熔断条件：同一单元超过最大尝试次数、错误类型连续相同、修复没有改变根因、新错误数量增加、成本或时间超限时，停止自动推进并标记 `needs_review`。

典型协作流：

```text
用户提出目标
  -> workflow 识别任务类型和风险等级
  -> Agent 只在需要动态判断的节点规划或路由
  -> Skill 提供流程、检查项和输出标准
  -> MCP 暴露资源和工具
  -> 需要知识时调用 RAG 并记录证据
  -> 需要动作时调用 Tool 并记录结构化结果
  -> 高风险动作进入人工确认
  -> workflow 更新状态、验证结果、决定继续/熔断/结单
```

## Verify
审查每个 Agent 决策点，确认它确实需要模型动态判断，而不是可以用规则、表单或状态机完成。

验证长链路 workflow 时，不只看最终回答，还要检查：

- 分块是否完整，`unit_id` 是否覆盖所有输入。
- 状态是否可恢复，中断后不会重复或跳过单元。
- RAG 结论是否能回查到 `chunk_id` 或来源。
- 工具参数是否经过校验，错误 observation 是否清晰。
- 高风险动作是否触发确认，越权调用是否被应用层拒绝。
- 熔断是否生效，失败任务是否能结单并说明剩余风险。

## References
- OpenAI Agents SDK: workflows versus agents
- Workflow engine design patterns
- Long-context task orchestration
- RAG evidence-bound generation
- MCP resources, tools and prompts
- Skill-based task reuse

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
