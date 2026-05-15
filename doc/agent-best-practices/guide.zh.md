# Agent 最佳工程实践指南

语言：[中文](guide.zh.md) | [English](guide.en.md)

这份指南先整理 AI 工程基础知识与原理，再串联 Agent 工程实践和专题扩展。基础页解释概念边界，实践页沉淀规则、原因、优化方向、验证方式和参考资料。

## 使用方式

- 快速浏览：阅读本文件，按模块找到相关实践点。
- 深入执行：点击单点文件，查看 `Rule`、`Why`、`Optimize`、`Verify`。

## 00. AI 大模型与 Agent 基础原理

| 主题 | 核心结论 | 文件 |
| --- | --- | --- |
| AI 大模型与 Agent 基础原理总览 | 进入实践前先理解大模型、Agent 及相关工程模块的基础原理。 | [00](00-llm-basics/README.md) |
| 大模型基础 | 解释大模型是什么、如何演变而来，以及它的能力边界。 | [00.1](00-llm-basics/llm-fundamentals.md) |
| Transformer 的工作原理 | 解释 token、向量、位置编码、Q/K/V、注意力、next-token 预测。 | [00.2](00-llm-basics/transformer-principles.md) |
| 上下文与上下文窗口 | 上下文是本轮模型实际看到的内容，窗口越大不等于效果越好。 | [00.3](00-llm-basics/context-window-basics.md) |
| 提示词与指令基础 | Prompt 提供任务和上下文，Instruction 提供规则、边界和输出约束。 | [00.4](00-llm-basics/prompt-instruction-basics.md) |
| Agent 概念与原理 | 解释 Agent 是什么、如何演进而来，以及为什么需要工具、记忆、状态和恢复机制。 | [00.5](00-llm-basics/agent-principles.md) |
| MCP 与工具调用原理 | Function calling / tool use 不是模型执行代码，而是模型生成调用意图；MCP 用标准协议暴露资源、工具和提示模板。 | [00.6](00-llm-basics/mcp-principles.md) |
| Skill 概念与原理 | Skill 把专项任务的流程、工具用法和质量标准沉淀成可复用能力包。 | [00.7](00-llm-basics/skill-principles.md) |
| RAG 概念与原理 | RAG 先检索证据，再把证据放入上下文辅助生成。 | [00.8](00-llm-basics/rag-principles.md) |
| 记忆基础 | 记忆是应用保存并重新注入的事实或偏好，不是模型天然拥有的能力。 | [00.9](00-llm-basics/memory-basics.md) |
| 状态管理基础 | 状态应由确定性系统管理，而不是只放在自然语言历史里。 | [00.10](00-llm-basics/state-management-basics.md) |

## 01. 提示词与指令实践

| 编号 | 实践点 | 核心规则 | 文件 |
| --- | --- | --- | --- |
| 01 | 先定义成功标准，再写 Prompt | 先确定验收标准，再设计指令。 | [01](01-prompt-instruction/01-define-success-before-prompt.md) |
| 02 | 把 Prompt 当作代码管理 | Prompt 需要版本、评审、回归、回滚和长期规则长度控制。 | [02](01-prompt-instruction/02-manage-prompts-as-code.md) |
| 03 | 把业务 SOP 转成可执行步骤 | 把业务流程拆成模型可执行步骤，但不要塞进全局规则。 | [03](01-prompt-instruction/03-convert-sop-to-executable-steps.md) |
| 04 | 给模型明确退出路径 | 信息不足时允许拒答、澄清或降级。 | [04](01-prompt-instruction/04-give-clear-exit-path.md) |
| 05 | 输出格式要机器可校验 | 输出应能被 schema、解析器或规则自动检查。 | [05](01-prompt-instruction/05-machine-checkable-output.md) |
| 06 | 分隔指令、上下文和用户输入 | 防止用户输入或外部上下文污染系统规则。 | [06](01-prompt-instruction/06-separate-instructions-context-input.md) |
| 07 | 少量高质量示例优于大量松散示例 | 示例要覆盖典型、边界、拒答和失败情况。 | [07](01-prompt-instruction/07-use-few-high-quality-examples.md) |
| 08 | 为不同任务拆分 Prompt | 不同任务用不同 Prompt；Prompt 只引导当前工作记忆，不改写长期认知或参数。 | [08](01-prompt-instruction/08-split-prompts.md) |

## 02. 上下文工程与 RAG

| 编号 | 实践点 | 核心规则 | 文件 |
| --- | --- | --- | --- |
| 09 | 上下文不是越多越好 | 控制上下文优先级、来源、长度和时效性。 | [09](02-context-rag/09-context-is-not-more-is-better.md) |
| 10 | 检索质量和生成质量分开优化 | 先评估检索命中，再评估答案质量。 | [10](02-context-rag/10-separate-retrieval-and-generation-quality.md) |
| 11 | Chunk 策略要服务任务 | 切片策略应匹配文档结构和用户任务。 | [11](02-context-rag/11-chunk-strategy-serves-task.md) |
| 12 | 检索 chunk 和生成 chunk 可以不同 | 小片段用于召回，大片段用于生成。 | [12](02-context-rag/12-retrieval-and-generation-chunks-can-differ.md) |
| 13 | RAG 优化要可观测 | 用 Context Recall、Faithfulness、首轮解决率、chunk_id 和可信度度量定位瓶颈。 | [13](02-context-rag/13-add-cited-evidence-to-rag.md) |
| 14 | 检索为空要有明确策略 | 空召回时应澄清、扩大检索、降级或拒答。 | [14](02-context-rag/14-empty-retrieval-policy.md) |
| 15 | 上下文要防注入 | 外部文档不应覆盖系统指令和权限规则。 | [15](02-context-rag/15-context-injection-defense.md) |
| 16 | 对上下文做去重和压缩 | 移除重复、低相关和模板噪声。 | [16](02-context-rag/16-deduplicate-and-compress-context.md) |
| 17 | 长上下文要有摘要层、索引层和缓存友好布局 | 长任务需要摘要、索引、稳定前缀和动态消息分层协同。 | [17](02-context-rag/17-long-context-summary-and-index-layers.md) |
| 18 | 上下文构造过程应可观测 | 记录 query、top-k、rerank、注入片段和缓存命中。 | [18](02-context-rag/18-observable-context-construction.md) |

## 03. 记忆与状态管理

| 编号 | 实践点 | 核心规则 | 文件 |
| --- | --- | --- | --- |
| 19 | 长任务的记忆管理方式 | 长任务记忆要保持上下文鲜活、旧记忆可精准检索、细节可追溯、状态可恢复。 | [19](03-memory-state/19-memory-context-state-boundaries.md) |
| 20 | 记忆应有写入规则 | 只写稳定、明确、授权的事实或偏好。 | [20](03-memory-state/20-memory-write-policy.md) |
| 21 | 记忆应可更新和删除 | 用户纠正、撤销和隐私删除应生效。 | [21](03-memory-state/21-memory-update-delete.md) |
| 22 | 记忆要带来源和时间戳 | 记忆需要来源、时间、置信度和适用范围。 | [22](03-memory-state/22-memory-source-timestamp.md) |
| 23 | 敏感信息不应默认进入长期记忆 | 隐私、密钥和商业数据默认不长期保存。 | [23](03-memory-state/23-sensitive-info-memory.md) |
| 24 | 任务状态用确定性系统管理 | 流程进度、审批和工具结果不应只放在自然语言里。 | [24](03-memory-state/24-deterministic-task-state.md) |

## 04. MCP、工具调用与多 Agent

| 编号 | 实践点 | 核心规则 | 文件 |
| --- | --- | --- | --- |
| 25 | 工具接口要小而清晰 | 每个工具只做一类动作，参数和返回稳定。 | [25](04-tools-agents/25-small-clear-tool-interfaces.md) |
| 26 | 工具描述要写清何时不用 | 工具说明应包含使用条件和禁用条件。 | [26](04-tools-agents/26-tool-description-when-not-to-use.md) |
| 27 | 模型只提出调用意图，应用负责权限 | 权限、执行和审计由确定性系统控制。 | [27](04-tools-agents/27-intent-vs-permission.md) |
| 28 | 高风险动作应确认 | 发布、付款、删除等动作需要人工确认。 | [28](04-tools-agents/28-confirm-high-risk-actions.md) |
| 29 | 工具失败是正常路径 | 超时、空结果、权限失败都要有恢复策略。 | [29](04-tools-agents/29-tool-failure-normal-path.md) |
| 30 | 优先 workflow，再升级 Agent | 固定流程、长文本多轮任务和多模块协作应先工作流化，再让 Agent 处理动态判断。 | [30](04-tools-agents/30-workflow-before-agent.md) |
| 31 | 多 Agent 要有明确职责边界 | 每个 Agent 都要有清晰输入、输出和责任范围。 | [31](04-tools-agents/31-multi-agent-boundaries.md) |
| 32 | 多 Agent 的核心是测试和验证 | 多 Agent 不是角色越多越好，关键是验证。 | [32](04-tools-agents/32-multi-agent-test-verification.md) |
| 33 | Agent handoff 要传结构化上下文 | 交接应传目标、证据、约束和待验证问题。 | [33](04-tools-agents/33-structured-handoff-context.md) |
| 34 | Agent 轨迹要可回放 | 工具输入输出和关键决策要可追踪、可复现。 | [34](04-tools-agents/34-replayable-agent-traces.md) |
| 专题 | 大规模 Skill 工程实现 | 用 Intent Gateway、小模型路由、Skill RAG、动态 Prompt 组装、分身 Agent、缓存和内化管理大量 Skill。 | [专题](04-tools-agents/large-scale-skill-engineering.md) |

## 05. 测试、评测与验证

| 编号 | 实践点 | 核心规则 | 文件 |
| --- | --- | --- | --- |
| 35 | AI 系统需要扩展测试金字塔 | 单元测试、组件 eval、端到端 eval 和线上监控都要有。 | [35](05-evaluation-verification/35-extended-test-pyramid.md) |
| 36 | Eval 数据集覆盖真实分布和边界 | 评测集要包含典型、长尾、失败和攻击样例。 | [36](05-evaluation-verification/36-eval-data-real-boundary.md) |
| 37 | 不只测最终答案，也测中间过程 | RAG 测检索，Agent 测轨迹，Prompt 测格式。 | [37](05-evaluation-verification/37-test-intermediate-process.md) |
| 38 | LLM-as-judge 需要校准 | Judge 要和人工标准对齐，不应直接盲用。 | [38](05-evaluation-verification/38-calibrate-llm-as-judge.md) |
| 39 | 评测指标和业务风险绑定 | 风险越高，通过阈值和人工审核越严格。 | [39](05-evaluation-verification/39-metrics-bind-business-risk.md) |
| 40 | 影响输出的变更都要跑回归 | Prompt、模型、知识库、工具变更都要回归。 | [40](05-evaluation-verification/40-run-regression-on-changes.md) |
| 41 | 验证要包含反例和攻击样例 | 应覆盖幻觉、注入、越权和泄露风险。 | [41](05-evaluation-verification/41-counterexample-attack-samples.md) |
| 42 | 把失败分类，而不是只记录失败率 | 失败要按根因分类，才能形成改进路径。 | [42](05-evaluation-verification/42-failure-taxonomy.md) |
| 42A | 可观测性要区分测试驱动和目标驱动 | 测试驱动看链路是否按设计运行，目标驱动看设计是否真正服务目标。 | [42A](05-evaluation-verification/42A-observability-test-goal-driven.md) |

## 06. 反馈闭环与迭代

| 编号 | 实践点 | 核心规则 | 文件 |
| --- | --- | --- | --- |
| 43 | 生产反馈要进入工程闭环 | 用户反馈、trace、投诉和重试都应回流。 | [43](06-feedback-iteration/43-production-feedback-engineering-loop.md) |
| 44 | 建立从失败到改进的闭环流程 | 失败要经过归因、修复、回归、灰度和监控。 | [44](06-feedback-iteration/44-failure-to-improvement-loop.md) |
| 45 | 反馈不等于直接训练模型 | 先判断该改 Prompt、RAG、工具、产品还是模型。 | [45](06-feedback-iteration/45-feedback-not-direct-training.md) |
| 46 | 人工审核要服务评测标准沉淀 | 审核标签要能转成 eval case 或 rubric。 | [46](06-feedback-iteration/46-human-review-to-eval-standards.md) |
| 47 | 线上指标同时看质量、成本、延迟和安全 | 不应用单一满意度掩盖成本、缓存命中、延迟和风险。 | [47](06-feedback-iteration/47-online-metrics-quality-cost-latency-safety.md) |
| 48 | 灰度发布比一次性切换更适合 AI 系统 | Prompt、模型和 Agent 策略应逐步放量。 | [48](06-feedback-iteration/48-gradual-rollout.md) |
| 49 | 可解释的失败比偶然成功更有价值 | 系统应暴露不确定性和可恢复下一步。 | [49](06-feedback-iteration/49-explainable-failure-over-lucky-success.md) |
| 50 | 最佳实践最终要固化成团队规范 | 规范要覆盖 Prompt、工具、eval、trace、安全和发布流程。 | [50](06-feedback-iteration/50-team-standards.md) |
