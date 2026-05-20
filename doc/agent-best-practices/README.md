# Agent 最佳工程实践

本指南整理生产级 AI / Agent 系统的基础原理和工程实践。基础部分先解释关键概念，实践部分再沉淀规则、流程、验证和协作方式。

English: [Agent Engineering Best Practices Guide](guide.en.md)

## 核心目标

生产级 Agent 的设计重点，是让系统在明确边界内可靠完成任务：

- 边界清晰：明确能力范围、权限范围，以及何时澄清、拒绝或转交人工。
- 过程可观测：记录 Prompt、上下文、工具调用、轨迹、成本和错误。
- 结果可验证：验证最终答案，也验证检索、工具调用和中间过程。
- 失败可恢复：提供重试、降级、回滚、人工确认和反馈闭环。

## 开篇基础

先读 [AI 大模型与 Agent 基础原理](00-llm-basics/README.md)，理解大模型、Transformer、上下文、提示词、Agent、MCP/工具调用、Skill、RAG、记忆和状态这些基础模块。再进入后面的实践章节，学习如何把这些模块工程化协作起来。

## 功能模块

| 模块 | 范围 | 重点 |
| --- | --- | --- |
| [AI 大模型与 Agent 基础原理](00-llm-basics/README.md) | 00 | 大模型、Transformer、上下文、提示词与指令、Agent、MCP/工具调用、Skill、RAG、记忆、状态 |
| [提示词与指令实践](01-prompt-instruction/README.md) | 01-08 | 成功标准、Prompt 版本化、结构化输出、退出路径、工作记忆边界 |
| [上下文工程与 RAG](02-context-rag/README.md) | 09-18 | 检索、chunk、引用、注入防护、上下文观测 |
| [记忆与状态管理](03-memory-state/README.md) | 19-24 | 短期上下文、长期记忆、混合记忆架构、业务状态、隐私边界、长任务记忆管理 |
| [MCP、工具调用与多 Agent](04-tools-agents/README.md) | 25-34 + 专题 | 工具接口、权限、高风险确认、workflow 编排、Agent 调用工具的可靠性、大量 Skill 共存、handoff、轨迹回放 |
| [测试、评测与验证](05-evaluation-verification/README.md) | 35-42 | eval 数据、过程测试、LLM-as-judge、攻击样例 |
| [反馈闭环与迭代](06-feedback-iteration/README.md) | 43-50 | 生产反馈、失败归因、灰度发布、团队规范 |
| [源码实现](07-source-implementation/README.md) | 07 | Go Agent 源码实现、多 Agent 交互与调度、工具调用、权限校验和文件读取 |

## 阅读路径

1. 先读 [AI 大模型与 Agent 基础原理](00-llm-basics/README.md)，建立基础概念和模块边界。
2. 从 [中文总览](guide.zh.md) 或 [English Guide](guide.en.md) 快速浏览主实践。
3. 进入任一功能模块，查看该模块下的实践清单。
4. 点击具体实践点，查看 `Rule`、`Why`、`Optimize`、`Verify` 和 `References`。
