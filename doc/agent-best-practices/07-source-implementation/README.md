# 源码实现

[返回全局摘要](../README.md)

本模块放源码级教程。它不再按泛泛的“代码实现”理解，而是把 AI 工程里最核心的几类源码小闭环拆开：从零实现大模型核心组件、从零写单 Agent、从零写 MCP、从零写 Skill，以及多 Agent 调度。

每条教程线都按小步推进：每一节只新增一个能力，并且能看到输入、代码、输出和下一步。

## 源码教程线

| 教程 | 目标 | 适合阶段 |
| --- | --- | --- |
| [从零实现大模型核心组件](llm-from-zero/README.md) | 用小词表和小矩阵还原 token、embedding、Attention 等核心计算 | 大模型原理转代码 |
| [从零使用 Go 语言开发一个 Agent](go-agent-from-zero/README.md) | 从一次 API 调用开始，逐步做出能用工具、能读文件、能做简单任务的单 Agent | 单 Agent 入门源码 |
| [从零实现 MCP](mcp-from-zero/README.md) | 分别实现本地 stdio MCP 和 HTTP MCP，并用数据库工具逐步增加能力 | 工具协议与外部系统 |
| [从零实现 Skill](skill-from-zero/README.md) | 从一个任务 SOP 开始，沉淀触发条件、执行步骤、工具依赖和质量标准 | 可复用能力包 |
| [多 Agent 交互与调度](multi-agent-interaction/README.md) | 学主 Agent、子 Agent、消息分发、任务分发、顺序调度和协同汇总 | 多 Agent 工作流 |

## 学习顺序

1. 如果正在学大模型原理，先看 [从零实现大模型核心组件](llm-from-zero/README.md)，把 token、embedding 和后续 Attention 的矩阵形状对上。
2. 再学 [从零使用 Go 语言开发一个 Agent](go-agent-from-zero/README.md)，把 API、上下文、tool use、权限校验、文件读取跑通。
3. 继续学 [从零实现 MCP](mcp-from-zero/README.md)，把工具从进程内函数拆成可复用的本地 MCP / HTTP MCP 服务。
4. 然后学 [从零实现 Skill](skill-from-zero/README.md)，把稳定流程、工具使用方法和质量标准沉淀成可复用能力包。
5. 最后学 [多 Agent 交互与调度](multi-agent-interaction/README.md)，把 Planning、Review、Verification 等职责拆成不同 Agent，并学习主 Agent 如何分发任务。

## 本模块的约束

- 每节只加一个能力。
- 高风险动作必须有权限校验。
- 文件、数据库、命令执行都默认最小权限。
- 能用结构化 JSON 传递的中间结果，不用自然语言糊过去。
- Skill、MCP、Agent 都要能被测试、观测和回归。
