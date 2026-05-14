# Agent 最佳工程实践

本指南整理了生产级 Agent 系统的 50 条主实践和若干专题扩展，按功能模块组织，便于从大模型基本原理进入具体规范。

English: [Agent Engineering Best Practices Guide](guide.en.md)

## 核心目标

生产级 Agent 的设计重点，是让系统在明确边界内可靠完成任务：

- 边界清晰：明确能力范围、权限范围，以及何时澄清、拒绝或转交人工。
- 过程可观测：记录 Prompt、上下文、工具调用、轨迹、成本和错误。
- 结果可验证：验证最终答案，也验证检索、工具调用和中间过程。
- 失败可恢复：提供重试、降级、回滚、人工确认和反馈闭环。

## 开篇基础

先读 [大模型与 Agent 基础](00-llm-basics/README.md)，理解大模型为什么本质上是一个概率预测机器：它根据输入和上下文计算输出概率，而不是像传统程序一样保证确定性结果。这个前提会自然引出 Agent 工程的发展路径：Prompt 优化、上下文工程、记忆与状态、工具调用、角色分工、错误恢复和长时间运行。

## 功能模块

| 模块 | 范围 | 重点 |
| --- | --- | --- |
| [大模型与 Agent 基础](00-llm-basics/README.md) | 00 | 大模型历史、Agent 历史、Transformer/QKV 原理、上下文重放、无持续记忆、能力边界、工程实践必要性 |
| [提示词与 Instruction](01-prompt-instruction/README.md) | 01-08 | 成功标准、Prompt 版本化、结构化输出、退出路径 |
| [上下文工程与 RAG](02-context-rag/README.md) | 09-18 | 检索、chunk、引用、注入防护、上下文观测 |
| [记忆与状态管理](03-memory-state/README.md) | 19-24 | 短期上下文、长期记忆、业务状态、隐私边界 |
| [工具调用与多 Agent](04-tools-agents/README.md) | 25-34A | 工具接口、权限、高风险确认、handoff、轨迹回放、长文本多轮执行 |
| [测试、评测与验证](05-evaluation-verification/README.md) | 35-42 | eval 数据、过程测试、LLM-as-judge、攻击样例 |
| [反馈闭环与迭代](06-feedback-iteration/README.md) | 43-50 | 生产反馈、失败归因、灰度发布、团队规范 |

## 阅读路径

1. 先读 [大模型与 Agent 基础](00-llm-basics/README.md)，建立“概率预测机器”的基本心智模型。
2. 从 [中文总览](guide.zh.md) 或 [English Guide](guide.en.md) 快速浏览主实践和专题扩展。
3. 进入任一功能模块，查看该模块下的实践清单。
4. 点击具体实践点，查看 `Rule`、`Why`、`Optimize`、`Verify` 和 `References`。
