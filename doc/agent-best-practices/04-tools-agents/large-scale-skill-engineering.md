# 大规模 Skill 工程实现

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)

## Status
Recommended

Category: tools-agents

## Rule
当系统有几十个或上百个 Skill 时，不要把所有 Skill 全量写进 System Prompt。应把 Skill 管理设计成可路由、可检索、可动态组装、可观测的工程系统。

## Why
少量 Skill 可以直接写入系统提示词，但 Skill 数量持续增长后，全量加载会带来系统性问题：

| 问题 | 后果 |
| --- | --- |
| Token 膨胀 | 成本和首字延迟上升，缓存命中下降 |
| 注意力稀释 | 当前任务真正需要的 Skill 被无关说明淹没 |
| Lost in the Middle | 位于长上下文中间的 Skill 更容易被忽略 |
| 工具误选 | 相似 Skill 互相干扰，模型选择错误工具或参数 |
| 难以维护 | Skill 变更难评审、难回滚、难定位线上退化 |

大规模 Skill 的核心不是继续压缩 Prompt，而是把单体 Prompt 思维改成“能力库 + 路由 + 按需装配”的架构。

## Optimize

### 1. 建 Skill Registry

每个 Skill 都应有结构化元数据，而不是只是一段自然语言说明：

| 字段 | 作用 |
| --- | --- |
| `name` | 稳定标识，用于日志、检索、灰度和回滚 |
| `description` | 用于语义检索和意图匹配 |
| `trigger` | 什么任务应该加载，什么任务不应加载 |
| `inputs` / `outputs` | 让 Prompt 组装器知道字段契约 |
| `tools` | 依赖的 MCP 工具、脚本或 API |
| `risk_level` | 决定是否需要只读、审批或人工确认 |
| `examples` | 动态 few-shot 示例来源 |
| `version` | 支持变更记录、回滚和 A/B 测试 |

### 2. 加 Intent Gateway

用户请求进入主模型前，先经过轻量意图路由：

```text
用户请求
  -> 任务类型分类
  -> 风险等级判断
  -> 候选 Skill 大类选择
  -> 是否需要多步规划 / 人工确认
```

Intent Gateway 可以用规则、小模型、分类器或 embedding 召回实现。目标是先缩小候选范围，不让主模型直接面对全部 Skill。

### 3. 用 Skill RAG 检索 Top-K

将 Skill 的描述、触发条件、参数、示例和限制文档化后建立索引。每次只召回当前任务最相关的少量 Skill，例如 Top 3-5。

```text
用户意图 + 当前任务状态
  -> 查询 Skill Registry / 向量库 / 关键词索引
  -> rerank
  -> 返回 Top-K Skill
  -> 注入 Prompt 动态上下文
```

Skill RAG 的输出应带 `skill_id`、版本、相关性分数和触发理由，便于 trace 回放和误调用分析。

### 4. 动态组装 Prompt

Prompt 由稳定前缀和动态片段组成：

```text
稳定前缀:
  - 系统角色
  - 权限边界
  - 输出约束
  - Skill 选择规则

动态片段:
  - 当前任务目标
  - Top-K Skill 摘要
  - 必要参数格式
  - 1-2 个最相关 few-shot 示例
  - 当前工具结果 / 状态
```

不要把 Skill 全文无差别塞入上下文。优先注入当前任务需要的触发条件、输入输出契约、关键步骤和失败边界。

### 5. 拆成 Manager Agent 和领域 Agent

复杂任务不要让一个 Agent 携带所有 Skill。可以拆成：

| 角色 | 职责 |
| --- | --- |
| Manager Agent | 识别目标、拆解任务、选择领域 Agent，不携带具体工具细节 |
| 领域 Agent | 只加载本领域 Skill，例如数据分析、检索、写作、代码、设计 |
| Verifier | 检查证据、格式、工具结果和风险动作 |

这样每个 Agent 的上下文更小，职责更清晰，也更容易测试和回放。

### 6. 做底层成本优化

- 对稳定系统规则、工具基础说明、固定安全边界使用 Context Caching。
- 对高频、格式稳定、变化少的工具调用模式，评估微调、模板化函数调用或确定性封装。
- 对低频 Skill 保持外部化，按需检索，不要内化到模型或全局 Prompt。

## Flow

```text
用户请求
  -> Intent Gateway 判断任务类型和风险
  -> Skill Registry / Skill RAG 召回 Top-K Skill
  -> Prompt Builder 组装稳定前缀 + 动态 Skill + 示例
  -> Agent / Workflow 执行
  -> Tool / MCP 返回结构化结果
  -> Verifier 检查结果
  -> Trace 记录 skill_id、版本、命中分数、工具调用和成本
```

## Verify

| 验证项 | 检查方式 |
| --- | --- |
| Skill 命中率 | 标注一批任务到目标 Skill，检查 Top-K 是否召回 |
| 误加载率 | 检查无关 Skill 是否被注入并影响输出 |
| 工具误调用率 | 比较全量加载和按需加载下的工具选择错误 |
| Token 和延迟 | 对比输入 token、首字延迟、总耗时和缓存命中率 |
| 分身效果 | 检查领域 Agent 是否只加载本领域 Skill |
| 可回放性 | trace 能还原为什么加载某个 Skill、为什么调用某个工具 |
| 回归能力 | Skill 描述、示例或路由规则变更后跑固定评测集 |

## References
- [02. 把 Prompt 当作代码管理](../01-prompt-instruction/02-manage-prompts-as-code.md)
- [09. 上下文不是越多越好](../02-context-rag/09-context-is-not-more-is-better.md)
- [30. 优先 workflow，再升级 Agent](30-workflow-before-agent.md)
- Skill routing and dynamic prompt assembly
- Context caching and high-frequency tool-call optimization

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
