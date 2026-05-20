# 源码实现

[返回全局摘要](../README.md)

本模块放源码级教程。目标不是讲概念，而是按小闭环逐步写代码：每一节只新增一个能力，并且能看到输入、代码、输出和下一步。

## 教程线

| 教程 | 目标 | 适合阶段 |
| --- | --- | --- |
| [从零使用 Go 语言开发一个 Agent](go-agent-from-zero/README.md) | 从一次 API 调用开始，逐步做出能用工具、能读文件、能做简单任务的单 Agent | 入门源码实现 |
| [多 Agent 交互与调度](multi-agent-interaction/README.md) | 学主 Agent、子 Agent、消息分发、任务分发、顺序调度和协同汇总 | 多 Agent 工作流 |

## 学习顺序

1. 先学 [从零使用 Go 语言开发一个 Agent](go-agent-from-zero/README.md)，把 API、上下文、tool use、权限校验、文件读取跑通。
2. 再学 [多 Agent 交互与调度](multi-agent-interaction/README.md)，把 Code Review、Planning、Verification 拆成不同 Agent，并学习主 Agent 如何分发任务。

## 本模块的约束

- 每节只加一个能力。
- 高风险动作必须有权限校验。
- 文件、数据库、命令执行都默认最小权限。
- 能用结构化 JSON 传递的中间结果，不用自然语言糊过去。
