# Agent 能力治理

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)

本页是当前项目自己的 Agent 工程治理框架，用来把 Prompt、Skill、Memory、State、Context Builder、Tool 和 Trace 串成一条可实现、可验证、可维护的运行链路。

它不重复各章节的单点规则，而是回答一个工程问题：当 Agent 功能越来越多、Skill 越来越多、记忆越来越多时，系统如何仍然保持可控。

## 总原则

Agent 不应该靠一段越来越长的全局 Prompt 运行。更稳的做法是把任务拆成几个确定的工程层：

```text
用户目标
  -> 成功标准和失败边界
  -> 意图、领域和风险识别
  -> 能力选择：Prompt / Skill / Tool / Workflow
  -> 记忆、状态和证据筛选
  -> Context Builder 动态组装
  -> Agent / workflow 执行
  -> Verifier 验证结果和过程
  -> Trace、失败样例和回归集沉淀
```

这条链路里的每一层都要能解释“为什么这样做”，也要能在失败时定位到具体环节。

## 组件边界

| 组件 | 负责什么 | 不负责什么 |
| --- | --- | --- |
| Prompt | 当前调用的任务说明、约束、输出格式和退出路径 | 长期能力库、业务状态、权限决策 |
| Skill | 一类任务的可复用方法：触发条件、步骤、工具用法、输出标准、验证规则 | 保存用户长期事实、替代工具权限系统 |
| Memory | 跨会话可复用的稳定事实、偏好、项目背景和经验 | 任务进度、审批状态、支付状态、唯一事实来源 |
| State | 当前任务的进度、状态转移、工具结果、确认记录和恢复点 | 模糊偏好、未经确认的用户画像 |
| Tool | 对外部系统的读写动作和结构化观察结果 | 自行决定是否越权执行 |
| Trace | 记录选择、输入、输出、验证和失败原因 | 只保存最终回答 |

最重要的边界是：Memory 偏长期事实，State 偏当前任务进度，Skill 偏可复用执行方法。三者不能混用。

## Skill 管理

当系统里有多个 Skill 时，不能只把所有 Skill 全文塞进上下文。每个 Skill 应该先进入结构化注册表，再由路由器按当前任务选择。

```text
SkillSpec
  ├─ skill_id
  ├─ title
  ├─ owner
  ├─ version
  ├─ description
  ├─ trigger
  ├─ do_not_use_when
  ├─ inputs_schema
  ├─ outputs_schema
  ├─ required_tools
  ├─ required_permissions
  ├─ risk_level
  ├─ context_sections
  ├─ conflicts_with
  ├─ validators
  └─ regression_cases
```

关键规则：

- `trigger` 写清楚什么任务应该使用。
- `do_not_use_when` 写清楚什么任务不应该使用。
- `inputs_schema` 和 `outputs_schema` 固定输入输出契约。
- `required_tools` 和 `required_permissions` 明确工具依赖和权限边界。
- `risk_level` 决定是否需要人工确认、只读模式或审计。
- `context_sections` 让 Context Builder 只加载必要片段。
- `conflicts_with` 用来处理相似 Skill 的冲突。
- `validators` 和 `regression_cases` 用来验证 Skill 改动是否可靠。

运行时不要让模型“自由挑选所有能力”，而是生成内部能力计划：

```json
{
  "task": {
    "goal": "生成带证据的竞品分析报告",
    "success_criteria": ["覆盖 3 个竞品", "每个结论有证据", "输出 Markdown"],
    "risk_level": "read_only"
  },
  "selected_skills": [
    {
      "skill_id": "research.evidence-collection",
      "version": "1.2.0",
      "include_reason": "任务需要收集并筛选证据",
      "include_parts": ["steps", "source_rules", "failure_policy"]
    },
    {
      "skill_id": "writing.evidence-report",
      "version": "2.0.3",
      "include_reason": "最终产物是带证据的报告",
      "include_parts": ["output_contract", "quality_checklist"]
    }
  ],
  "rejected_skills": [
    {
      "skill_id": "marketing.landing-copy",
      "reject_reason": "用户要分析报告，不是营销文案"
    }
  ]
}
```

这个计划是内部运行数据。它约束后续上下文组装、执行和 trace，而不是展示给用户。

## Memory 管理

记忆不是“聊天历史保存得越多越好”。记忆系统要控制什么能写入、什么时候读取、怎么更新、怎么删除。

```text
MemoryRecord
  ├─ id
  ├─ subject
  ├─ content
  ├─ memory_type
  ├─ source
  ├─ scope
  ├─ confidence
  ├─ sensitivity
  ├─ status
  ├─ created_at
  ├─ updated_at
  ├─ expires_at
  └─ evidence_refs
```

写入规则：

- 只写稳定、明确、可复用的信息。
- 用户偏好、项目背景、长期约束可以写。
- 临时选择、模型猜测、一次性中间结论不自动写。
- 密钥、密码、身份敏感信息和隐私数据默认不写。
- 有冲突、低置信度或影响较大的记忆，需要确认或进入待确认状态。

读取规则：

- 先按用户、项目、组织和权限过滤。
- 再按当前任务相关性筛选。
- 排除过期、敏感、冲突或未确认的记忆。
- 注入上下文时使用短摘要，并保留来源、时间和适用范围。
- trace 记录读取了哪些 memory id，以及为什么读取。

## State 管理

任务进度不能只写在自然语言历史里。长任务、工具调用、多 Agent 协作都需要确定性状态。

```text
TaskState
  ├─ task_id
  ├─ status
  ├─ goal
  ├─ success_criteria
  ├─ current_step
  ├─ completed_steps
  ├─ pending_questions
  ├─ pending_confirmations
  ├─ artifacts
  ├─ tool_results
  ├─ retry_counts
  ├─ budget
  ├─ version
  └─ updated_at
```

状态系统负责：

- 限制合法状态转移。
- 保存 checkpoint，支持中断恢复。
- 记录工具结果和副作用。
- 保存待确认事项。
- 控制取消、失败、重试和完成。
- 给多 Agent 协作提供一致的任务视图。

## Context Builder

Context Builder 的任务是把庞大的规则、Skill、记忆、状态和证据压缩成本轮需要的最小有效上下文。

建议组装顺序：

```text
1. 稳定系统规则和安全边界
2. 当前任务目标、成功标准和失败边界
3. 当前 TaskState 摘要
4. 选中的 Skill 片段
5. 相关 Memory 摘要
6. RAG 证据和工具 observation
7. 输出格式、验证规则和退出路径
```

注入规则：

| 内容 | 注入方式 |
| --- | --- |
| Skill | 只注入触发条件、关键步骤、输出契约、失败策略和少量必要示例 |
| Memory | 只注入本轮相关摘要，带来源、时间和适用范围 |
| State | 注入当前决策需要的状态快照，完整状态仍由数据库或工作流系统保存 |
| Evidence | 注入可引用、可验证的片段，保留来源 id |
| Tool result | 注入结构化 observation，不直接塞完整工具日志 |

## Verifier 与 Trace

Agent 不能自己说“完成了”就算完成。Verifier 应该检查成功标准、输出格式、工具结果、状态转移和风险动作。

Trace 至少记录：

- 输入目标和成功标准。
- 候选 Skill、选中 Skill、排除 Skill 和原因。
- 读取的 Memory id、来源和注入摘要。
- TaskState 版本和状态转移。
- 工具调用参数、权限校验、执行结果和错误。
- Verifier 检查项、通过项、失败项。
- 最终输出和失败样例归档位置。

这些 trace 不是为了堆日志，而是为了能回答：一次失败到底发生在路由、记忆、上下文、工具、执行还是验证。

## 上线检查

- 是否先定义了成功标准、失败边界和验收方式。
- Skill 是否都有触发条件、禁用条件、输入输出契约和版本。
- 相似 Skill 是否有冲突规则。
- Context Builder 是否只注入当前任务需要的片段。
- Memory 是否有写入、读取、更新、删除和过期策略。
- 敏感信息是否默认不进入长期记忆。
- TaskState 是否由确定性系统管理。
- 高风险工具是否有确认、幂等、审计和回滚策略。
- Trace 是否能回放能力选择、记忆读取、上下文组装、工具调用和验证结果。
- Prompt、Skill、Memory policy、工具 schema 改动后是否触发相关回归。

## 反模式

| 反模式 | 风险 | 改法 |
| --- | --- | --- |
| 把所有 Skill 全文塞进 System Prompt | 成本高、注意力稀释、冲突难定位 | Skill registry + router + 动态组装 |
| Skill 只写能做什么，不写何时不用 | 误触发、重复调用 | 增加 `do_not_use_when` 和边界样例 |
| 把聊天历史当长期记忆 | 旧信息污染、无法审计、无法删除 | Memory store + 来源、时间、权限和过期策略 |
| 把任务进度写进自然语言记忆 | 中断后无法可靠恢复 | TaskState + 状态机 + checkpoint |
| 让模型自行判断权限 | 越权和审计缺失 | 应用层权限、确认和工具执行器控制 |
| 只看最终回答质量 | 不知道问题出在哪一层 | 分别评估路由、记忆、上下文、工具和验证 |

## 一句话原则

Prompt 负责当前调用，Skill 负责可复用方法，Memory 负责长期事实，State 负责任务进度，Tool 负责外部动作，Trace 负责复盘验证。Agent 工程的核心不是堆更多上下文，而是把这些组件按边界组织起来。

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
