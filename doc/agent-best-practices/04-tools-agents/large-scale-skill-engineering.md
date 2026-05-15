# 大量 Skill 共存解决方案

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)

## Status
Recommended

Category: tools-agents

## Rule
当系统里有几十个、上百个 Skill 共存时，不要把全部 Skill 全量塞进 System Prompt，也不要让主 Agent 临场猜该用哪个。应把 Skill 管理设计成“注册、路由、检索、冲突处理、动态组装、执行验证、观测回归”的工程链路。

## Why
少量 Skill 可以直接写进提示词；大量 Skill 共存时，问题会从“单个 Skill 怎么写”变成“能力库怎么治理”。

| 问题 | 典型表现 | 后果 |
| --- | --- | --- |
| Skill 太多 | Prompt 里塞入完整 Skill 列表和长说明 | token 膨胀、成本上升、首字延迟变长 |
| 注意力稀释 | 当前任务只需要 2 个 Skill，模型却看到 100 个 | 关键规则被淹没，命中率下降 |
| 相似 Skill 冲突 | 多个 Skill 都能处理“分析数据”“生成报告”“检索资料” | 误选、重复调用、输出风格漂移 |
| 触发条件不清 | Skill 只写能力，不写何时不用 | 模型过度调用或漏调用 |
| 组合顺序混乱 | 一个任务需要检索、分析、写作、验证多个 Skill | 执行顺序不稳定，handoff 信息丢失 |
| 版本不可追踪 | Skill 改了描述、示例或工具依赖 | 线上质量变化后难定位、难回滚 |
| 上下文不可控 | 每个 Skill 都带长示例和实现细节 | 超预算、缓存失效、相关信息丢失 |
| 质量不可验证 | 只看最终回答，不看 Skill 选择过程 | 不知道问题出在路由、检索、组装还是执行 |

## Optimize
大量 Skill 共存要先做收敛，再做组装，最后做验证。

| 层级 | 解决什么 | 处理措施 |
| --- | --- | --- |
| Skill Registry | 让每个 Skill 可管理 | 为 Skill 建结构化元数据：`skill_id`、`description`、`trigger`、`do_not_use_when`、`inputs`、`outputs`、`tools`、`risk_level`、`version` |
| 意图路由 | 先缩小候选范围 | 用 Intent Gateway、规则、小模型 Router 或分类器识别任务类型、领域、风险等级和候选 Skill |
| Skill 检索 | 从能力库里找相关 Skill | 用关键词、embedding、rerank 召回 Top-K Skill，并返回命中分数和触发理由 |
| 冲突处理 | 避免相似 Skill 互相干扰 | 在 Registry 中写 `conflicts_with`、优先级、排除条件和边界样例；低置信度时请求澄清或交给主模型复判 |
| 动态组装 | 只给模型当前需要的内容 | Prompt Builder 根据 manifest 注入必要片段，如触发条件、输入输出契约、关键步骤、失败边界和 1-2 个相关示例 |
| 分工执行 | 避免单 Agent 背负全部能力 | 复杂任务拆成 Manager Agent、领域 Agent 和 Verifier；每个 Agent 只加载当前阶段需要的 Skill |
| 缓存与内化 | 降低高频路径成本 | 缓存候选 Skill、检索结果、工具 observation；对稳定、低风险、高频模式再考虑微调或蒸馏内化 |
| 观测回归 | 找到错误发生在哪一层 | trace 记录 `skill_id`、版本、命中分数、include_reason、rejected_skill_ids、工具调用和验证结果 |

动态组装时，可以先生成内部 manifest，再渲染成最终 prompt：

```json
{
  "task": {
    "goal": "分析 CSV 中的异常订单并输出可复查结论",
    "risk_level": "read_only",
    "output_format": "markdown_report"
  },
  "selected_skills": [
    {
      "skill_id": "data-analysis.csv-anomaly",
      "version": "1.4.2",
      "include_reason": "用户上传 CSV 并要求识别异常订单",
      "confidence": 0.91,
      "include_parts": ["trigger", "inputs", "steps", "failure_policy"],
      "omit_parts": ["long_examples", "implementation_notes"]
    },
    {
      "skill_id": "reporting.evidence-based-summary",
      "version": "2.1.0",
      "include_reason": "最终输出需要带证据和可复查字段",
      "confidence": 0.84,
      "include_parts": ["output_contract", "citation_rules"],
      "omit_parts": ["style_variants"]
    }
  ],
  "rejected_skills": [
    {
      "skill_id": "sales.dashboard-generation",
      "reject_reason": "用户只要求分析 CSV 异常，不需要生成 BI 看板"
    }
  ],
  "context_budget": {
    "max_skill_tokens": 1800,
    "max_examples": 1,
    "dedupe": true
  }
}
```

这个 manifest 的作用不是展示给用户，而是约束 Prompt Builder：只装配本轮任务需要的 Skill 片段，避免把 Skill 全文、重复示例、无关历史状态和实现细节一起塞进上下文。

## Flow

```text
用户请求
  -> Intent Gateway 判断任务类型、领域和风险
  -> Router / Skill RAG 召回候选 Skill
  -> 冲突规则过滤相似 Skill
  -> Prompt Builder 按 manifest 动态组装少量 Skill 片段
  -> Agent / workflow 执行
  -> Verifier 检查输出、工具结果和风险动作
  -> trace 记录选择、排除、版本、执行和验证结果
  -> 失败样例进入回归集
```

## Verify
检查大量 Skill 共存系统时，不只看最终回答，还要看 Skill 选择链路：

- Top-K 召回是否覆盖真实需要的 Skill。
- 相似 Skill 是否有清楚的 `do_not_use_when` 和冲突规则。
- 低置信度、多意图或高风险请求是否会澄清、复判或人工接管。
- Prompt Builder 是否只注入 manifest 声明的片段。
- trace 是否记录 Skill ID、版本、命中分数、选择理由和排除理由。
- Skill 变更后是否触发相关回归集。
- 高频缓存是否包含用户范围、输入 hash、Skill 版本、数据版本、权限上下文和 TTL。

一句话收尾：大量 Skill 共存解决方案，不是把更多 Skill 塞给模型，而是用能力注册、路由检索、冲突裁决和动态组装，把庞大的能力库收敛成当前任务真正需要的一小组可验证能力。

## References
- Skill Registry and capability routing
- Retrieval-augmented prompt assembly
- Prompt / Context Caching
- Agent trace and regression evaluation

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
