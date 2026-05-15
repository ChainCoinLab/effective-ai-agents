# 大规模 Skill 工程实现

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)

## Status
Recommended

Category: tools-agents

## Rule
当系统有几十个或上百个 Skill 时，不要把所有 Skill 全量写进 System Prompt。应把 Skill 管理设计成可路由、可检索、可动态组装、可观测的工程系统；其中高频路由判断可以交给小模型或专用分类器完成。

## Why
少量 Skill 可以直接写入系统提示词，但 Skill 数量持续增长后，全量加载会带来系统性问题：

| 问题 | 后果 |
| --- | --- |
| Token 膨胀 | 成本和首字延迟上升，缓存命中下降 |
| 注意力稀释 | 当前任务真正需要的 Skill 被无关说明淹没 |
| Lost in the Middle | 位于长上下文中间的 Skill 更容易被忽略 |
| 工具误选 | 相似 Skill 互相干扰，模型选择错误工具或参数 |
| 难以维护 | Skill 变更难评审、难回滚、难定位线上退化 |

大规模 Skill 的核心不是继续压缩 Prompt，而是把单体 Prompt 思维改成“能力库 + 小模型路由 + 检索 + 按需装配 + 缓存 / 内化”的架构。

大规模场景可以按三个维度拆解：

| 维度 | 主要问题 | 主要手段 |
| --- | --- | --- |
| 广度 | Skill 太多，主模型不能一次面对完整能力库 | Intent Gateway、小模型 Router、Skill Registry、Skill RAG、Top-K 召回 |
| 深度 | 任务需要多步拆解、跨领域协作或证据递进 | Manager Agent、领域 Agent、Verifier、深度检索、多轮查询改写 |
| 快慢 | 高频能力反复加载和执行，成本、延迟不可控 | Prompt / Context Caching、结果缓存、工具结果缓存、确定性封装、微调或蒸馏内化 |

广度解决“该加载哪些 Skill”，深度解决“复杂任务怎么推进”，快慢解决“高频路径如何少算、快算或不再每次现算”。

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

### 3. 用小模型做 Skill Router

当 Skill 数量进入几十个或上百个后，路由本身应该产品化，而不是让主模型在完整 Skill 列表里临场判断。一个轻量小模型可以先把请求映射到候选能力域、风险等级和召回策略，再把少量候选 Skill 交给主模型或后续 workflow。

```text
用户请求 + 会话状态摘要
  -> 小模型 Router
  -> 输出 task_type / domain / risk_level / candidate_skill_ids / confidence
  -> 低置信度时扩大召回、请求澄清或交给主模型复判
```

小模型 Router 的输出应结构化，避免只返回自然语言解释：

| 字段 | 作用 |
| --- | --- |
| `task_type` | 判断是问答、检索、代码、数据分析、写作、设计、执行动作等 |
| `domain` | 缩小 Skill Registry 的命名空间或业务领域 |
| `candidate_skill_ids` | 返回少量候选 Skill，通常 3-10 个 |
| `risk_level` | 决定是否进入只读、确认、人审或禁止执行路径 |
| `confidence` | 低置信度触发 fallback，而不是硬路由 |
| `reason` | 记录简短触发依据，服务 trace 和误路由分析 |

小模型路由适合处理高频、低风险、边界清晰的分类问题；不适合独自决定高风险动作、复杂任务拆解和最终答案质量。对低置信度、相似 Skill 冲突、权限敏感或多意图请求，应进入兜底路径：扩大 Top-K、让主模型复判、拆分任务或请求用户澄清。

### 4. 用 Skill RAG 检索 Top-K

将 Skill 的描述、触发条件、参数、示例和限制文档化后建立索引。每次只召回当前任务最相关的少量 Skill，例如 Top 3-5。

```text
用户意图 + 当前任务状态
  -> 查询 Skill Registry / 向量库 / 关键词索引
  -> rerank
  -> 返回 Top-K Skill
  -> 注入 Prompt 动态上下文
```

Skill RAG 的输出应带 `skill_id`、版本、相关性分数和触发理由，便于 trace 回放和误调用分析。

如果任务本身需要更深的证据链，不应只做一次 Top-K。可以先用 Skill RAG 解决能力广度，再用深度检索解决任务深度：

```text
第一层: 召回相关 Skill 和领域
第二层: 针对选中 Skill 改写查询、展开子问题、检索证据
第三层: rerank / 去重 / 交叉验证
第四层: 只把可支持当前步骤的证据和 Skill 片段注入上下文
```

这样可以避免两个极端：要么只靠一次粗召回导致证据不足，要么把所有 Skill 和资料都塞进上下文造成噪声。

### 5. 动态组装 Prompt

Prompt 由稳定前缀、动态片段和结构化组装清单组成。稳定前缀只放跨任务长期有效的规则；动态片段只放本次任务需要的 Skill 摘要、参数契约、示例和状态。

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

动态组装要做降噪，核心是把“长篇自然语言说明”压成“结构化 JSON 清单 + 少量必要正文”。Prompt Builder 可以先生成一个内部 manifest，再根据 token budget 渲染成最终 Prompt：

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
  "context_budget": {
    "max_skill_tokens": 1800,
    "max_examples": 1,
    "dedupe": true
  }
}
```

这个 JSON 不是一定要原样发给模型，而是用于约束 Prompt Builder：只装配 manifest 里声明的片段，避免把 Skill 全文、重复示例、历史无关状态和实现细节一起塞进去。需要给模型看的内容也应尽量结构化，例如用短字段表达 `why_loaded`、`must_follow`、`do_not_use_when` 和 `output_contract`，减少自然语言噪声。

一个动态组装实例：

```text
用户请求:
  帮我看这个 orders.csv，找出异常订单，最后给一份能给运营看的结论。

Router 输出:
  task_type=data_analysis
  domain=csv_order_analysis
  risk_level=read_only
  candidate_skill_ids=[
    "data-analysis.csv-anomaly",
    "reporting.evidence-based-summary"
  ]

Prompt Builder 最终注入:
  稳定前缀:
    - 只能基于用户文件和工具结果下结论
    - 不执行写入、发送、删除等动作

  当前任务:
    - 目标: 找出异常订单并输出运营可读报告
    - 输入: orders.csv
    - 输出: Markdown，包含异常类型、订单号、证据字段、建议下一步

  Skill: data-analysis.csv-anomaly
    - 触发条件: CSV / 表格数据异常检测
    - 必要步骤: 读取 schema -> 检查缺失/重复/极值 -> 按金额、频率、地区、时间分组
    - 失败边界: 文件为空、字段缺失或无法解析时先说明缺口

  Skill: reporting.evidence-based-summary
    - 输出契约: 每条结论必须带可复查证据
    - 禁止: 不把猜测写成事实

  示例:
    - 只注入 1 个最接近的异常订单报告示例
```

动态实例的重点不是“拼得越多越好”，而是每个进入上下文的片段都能回答三个问题：为什么加载、模型必须遵守什么、什么时候不能用。

### 6. 拆成 Manager Agent 和领域 Agent

复杂任务不要让一个 Agent 携带所有 Skill。可以拆成：

| 角色 | 职责 |
| --- | --- |
| Manager Agent | 识别目标、拆解任务、选择领域 Agent，不携带具体工具细节 |
| 领域 Agent | 只加载本领域 Skill，例如数据分析、检索、写作、代码、设计 |
| Verifier | 检查证据、格式、工具结果和风险动作 |

这样每个 Agent 的上下文更小，职责更清晰，也更容易测试和回放。

### 7. 用缓存和内化优化快慢

- 对稳定系统规则、工具基础说明、固定安全边界使用 Context Caching。
- 对高频 Skill 路由使用小模型、专用分类器或规则，避免每次都让主模型读取完整能力目录。
- 对高频、格式稳定、变化少的工具调用模式，评估微调、模板化函数调用或确定性封装。
- 对低频 Skill 保持外部化，按需检索，不要内化到模型或全局 Prompt。

缓存和内化解决的是快慢问题，但要分层处理：

| 手段 | 适用对象 | 注意事项 |
| --- | --- | --- |
| Prompt / Context Caching | 稳定系统规则、工具 manifest、安全边界、常用 Skill 摘要 | 保持前缀稳定，避免频繁改顺序、改模型或插入动态内容 |
| 结果缓存 | 高频、低风险、输入可规范化、结果可复用的问答或分析 | cache key 必须包含用户范围、输入 hash、Skill 版本、数据版本和权限上下文 |
| 工具结果缓存 | 慢查询、外部 API、只读数据库查询、静态配置读取 | 设置 TTL 和失效策略，避免把过期数据当实时事实 |
| 确定性封装 | 格式转换、字段校验、模板化生成、固定业务规则 | 能用代码稳定完成的不要每次交给模型推理 |
| 模型内化 | 高频、稳定、低风险、边界清楚的 Skill 判断或输出模式 | 通过微调、蒸馏或小模型专用化实现，变更频繁和高风险规则仍应外部化 |

结果缓存不是简单缓存最终文本，而是缓存“可复用的中间结果”。例如候选 Skill 列表、规范化查询、检索结果、工具 observation、结构化分析结论都可以缓存；最终回答如果包含用户上下文、实时数据或权限差异，则应谨慎缓存。

内化也不是把所有 Skill 写进模型。适合内化的是生产中反复出现、定义稳定、验证集覆盖充分的高频技能，例如固定格式分类、常见工具参数生成、标准报告骨架、低风险数据清洗步骤。仍在快速变化的业务规则、长尾领域知识、高风险审批逻辑和需要引用证据的内容，应继续放在 Skill Registry、RAG、工具或 workflow 中按需加载。

## Flow

```text
用户请求
  -> Intent Gateway 判断任务类型和风险
  -> 小模型 Router 输出候选能力域、风险等级和置信度
  -> Skill Registry / Skill RAG 召回 Top-K Skill
  -> Prompt Builder 组装稳定前缀 + 动态 Skill + 示例
  -> Agent / Workflow 执行
  -> Tool / MCP 返回结构化结果
  -> 缓存可复用的路由、检索、工具结果或结构化中间结论
  -> Verifier 检查结果
  -> Trace 记录 skill_id、版本、命中分数、工具调用和成本
```

## Verify

| 验证项 | 检查方式 |
| --- | --- |
| Skill 命中率 | 标注一批任务到目标 Skill，检查 Top-K 是否召回 |
| 小模型路由质量 | 检查 task_type、domain、risk_level、candidate_skill_ids 的准确率和低置信度兜底 |
| 动态组装质量 | 检查 manifest 是否只包含必要 Skill 片段，是否去重、限量、记录 include_reason |
| 误加载率 | 检查无关 Skill 是否被注入并影响输出 |
| 工具误调用率 | 比较全量加载和按需加载下的工具选择错误 |
| Token 和延迟 | 对比输入 token、首字延迟、总耗时和缓存命中率 |
| 缓存有效性 | 检查 cache key 是否包含输入 hash、Skill 版本、数据版本、权限上下文和 TTL |
| 内化收益 | 对比内化前后的质量、延迟、成本、回滚难度和长尾失败率 |
| 分身效果 | 检查领域 Agent 是否只加载本领域 Skill |
| 可回放性 | trace 能还原为什么加载某个 Skill、为什么调用某个工具 |
| 回归能力 | Skill 描述、示例或路由规则变更后跑固定评测集 |

## References
- [02. 把 Prompt 当作代码管理](../01-prompt-instruction/02-manage-prompts-as-code.md)
- [09. 上下文不是越多越好](../02-context-rag/09-context-is-not-more-is-better.md)
- [30. 优先 workflow，再升级 Agent](30-workflow-before-agent.md)
- Small-model routing, Skill routing, JSON manifest and dynamic prompt assembly
- Result caching, tool-result caching and high-frequency Skill internalization

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
