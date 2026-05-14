# Agent 最佳实践索引

状态说明：

- `done`：文件已生成，包含统一结构，可作为初稿继续扩写。
- `draft`：文件存在但需要补结构或补验证方式。
- `todo`：尚未创建。

## 01. 提示词与 Instruction

| 编号 | 实践点 | 文件 | 状态 |
| --- | --- | --- | --- |
| 01 | 先定义成功标准，再写 Prompt | `01-prompt-instruction/01-define-success-before-prompt.md` | done |
| 02 | 把 Prompt 当作代码管理 | `01-prompt-instruction/02-manage-prompts-as-code.md` | done |
| 03 | 把业务 SOP 转成可执行步骤 | `01-prompt-instruction/03-convert-sop-to-executable-steps.md` | done |
| 04 | 给模型明确退出路径 | `01-prompt-instruction/04-give-clear-exit-path.md` | done |
| 05 | 输出格式要机器可校验 | `01-prompt-instruction/05-machine-checkable-output.md` | done |
| 06 | 分隔指令、上下文和用户输入 | `01-prompt-instruction/06-separate-instructions-context-input.md` | done |
| 07 | 少量高质量示例优于大量松散示例 | `01-prompt-instruction/07-use-few-high-quality-examples.md` | done |
| 08 | 为不同任务拆分 Prompt | `01-prompt-instruction/08-split-prompts.md` | done |

## 02. 上下文工程与 RAG

| 编号 | 实践点 | 文件 | 状态 |
| --- | --- | --- | --- |
| 09 | 上下文不是越多越好 | `02-context-rag/09-context-is-not-more-is-better.md` | done |
| 10 | 检索质量和生成质量分开优化 | `02-context-rag/10-separate-retrieval-and-generation-quality.md` | done |
| 11 | Chunk 策略要服务任务 | `02-context-rag/11-chunk-strategy-serves-task.md` | done |
| 12 | 检索 chunk 和生成 chunk 可以不同 | `02-context-rag/12-retrieval-and-generation-chunks-can-differ.md` | done |
| 13 | 为 RAG 加引用和证据约束 | `02-context-rag/13-add-cited-evidence-to-rag.md` | done |
| 14 | 检索为空要有明确策略 | `02-context-rag/14-empty-retrieval-policy.md` | done |
| 15 | 上下文要防注入 | `02-context-rag/15-context-injection-defense.md` | done |
| 16 | 对上下文做去重和压缩 | `02-context-rag/16-deduplicate-and-compress-context.md` | done |
| 17 | 长上下文要有摘要层、索引层和缓存友好布局 | `02-context-rag/17-long-context-summary-and-index-layers.md` | done |
| 18 | 上下文构造过程应可观测 | `02-context-rag/18-observable-context-construction.md` | done |

## 03. 记忆与状态管理

| 编号 | 实践点 | 文件 | 状态 |
| --- | --- | --- | --- |
| 19 | 区分短期上下文、长期记忆和业务状态 | `03-memory-state/19-memory-context-state-boundaries.md` | done |
| 20 | 记忆应有写入规则 | `03-memory-state/20-memory-write-policy.md` | done |
| 21 | 记忆应可更新和删除 | `03-memory-state/21-memory-update-delete.md` | done |
| 22 | 记忆要带来源和时间戳 | `03-memory-state/22-memory-source-timestamp.md` | done |
| 23 | 敏感信息不应默认进入长期记忆 | `03-memory-state/23-sensitive-info-memory.md` | done |
| 24 | 任务状态用确定性系统管理 | `03-memory-state/24-deterministic-task-state.md` | done |

## 04. 工具调用与多 Agent

| 编号 | 实践点 | 文件 | 状态 |
| --- | --- | --- | --- |
| 25 | 工具接口要小而清晰 | `04-tools-agents/25-small-clear-tool-interfaces.md` | done |
| 26 | 工具描述要写清何时不用 | `04-tools-agents/26-tool-description-when-not-to-use.md` | done |
| 27 | 模型只提出调用意图，应用负责权限 | `04-tools-agents/27-intent-vs-permission.md` | done |
| 28 | 高风险动作应确认 | `04-tools-agents/28-confirm-high-risk-actions.md` | done |
| 29 | 工具失败是正常路径 | `04-tools-agents/29-tool-failure-normal-path.md` | done |
| 30 | 优先 workflow，再升级 Agent | `04-tools-agents/30-workflow-before-agent.md` | done |
| 31 | 多 Agent 要有明确职责边界 | `04-tools-agents/31-multi-agent-boundaries.md` | done |
| 32 | 多 Agent 的核心是测试和验证 | `04-tools-agents/32-multi-agent-test-verification.md` | done |
| 33 | Agent handoff 要传结构化上下文 | `04-tools-agents/33-structured-handoff-context.md` | done |
| 34 | Agent 轨迹要可回放 | `04-tools-agents/34-replayable-agent-traces.md` | done |

## 05. 测试、评测与验证

| 编号 | 实践点 | 文件 | 状态 |
| --- | --- | --- | --- |
| 35 | AI 系统需要扩展测试金字塔 | `05-evaluation-verification/35-extended-test-pyramid.md` | done |
| 36 | Eval 数据集覆盖真实分布和边界 | `05-evaluation-verification/36-eval-data-real-boundary.md` | done |
| 37 | 不只测最终答案，也测中间过程 | `05-evaluation-verification/37-test-intermediate-process.md` | done |
| 38 | LLM-as-judge 需要校准 | `05-evaluation-verification/38-calibrate-llm-as-judge.md` | done |
| 39 | 评测指标和业务风险绑定 | `05-evaluation-verification/39-metrics-bind-business-risk.md` | done |
| 40 | 影响输出的变更都要跑回归 | `05-evaluation-verification/40-run-regression-on-changes.md` | done |
| 41 | 验证要包含反例和攻击样例 | `05-evaluation-verification/41-counterexample-attack-samples.md` | done |
| 42 | 把失败分类，而不是只记录失败率 | `05-evaluation-verification/42-failure-taxonomy.md` | done |

## 06. 反馈闭环与迭代

| 编号 | 实践点 | 文件 | 状态 |
| --- | --- | --- | --- |
| 43 | 生产反馈要进入工程闭环 | `06-feedback-iteration/43-production-feedback-engineering-loop.md` | done |
| 44 | 建立从失败到改进的闭环流程 | `06-feedback-iteration/44-failure-to-improvement-loop.md` | done |
| 45 | 反馈不等于直接训练模型 | `06-feedback-iteration/45-feedback-not-direct-training.md` | done |
| 46 | 人工审核要服务评测标准沉淀 | `06-feedback-iteration/46-human-review-to-eval-standards.md` | done |
| 47 | 线上指标同时看质量、成本、延迟和安全 | `06-feedback-iteration/47-online-metrics-quality-cost-latency-safety.md` | done |
| 48 | 灰度发布比一次性切换更适合 AI 系统 | `06-feedback-iteration/48-gradual-rollout.md` | done |
| 49 | 可解释的失败比偶然成功更有价值 | `06-feedback-iteration/49-explainable-failure-over-lucky-success.md` | done |
| 50 | 最佳实践最终要固化成团队规范 | `06-feedback-iteration/50-team-standards.md` | done |
