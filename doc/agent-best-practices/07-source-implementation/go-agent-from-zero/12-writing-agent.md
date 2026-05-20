# 12. 写文章 Agent

[返回专题首页](README.md)

本节只增加一个能力：把一次性生成文章，拆成可检查的写作流程。

## 本节任务

输入：

```text
写一篇 800 字文章，主题是 Go Agent 工程入门
```

Agent 不直接一次写完，而是分三步：

1. 生成提纲。
2. 根据提纲写草稿。
3. 检查并输出最终稿。

## 和上一节相比新增什么

新增 workflow：

```go
outline := agent.Ask("先生成文章提纲：" + topic)
draft := agent.Ask("根据提纲写草稿：" + outline)
final := agent.Ask("检查草稿并输出最终稿：" + draft)
```

## 整个流程

```text
用户输入写作任务
  ↓
生成提纲
  ↓
生成草稿
  ↓
检查草稿
  ↓
输出最终稿
```

## 本节学到什么

写文章 Agent 的重点不是“调用一次模型写文章”，而是把任务拆成可观察、可重试的步骤。

这样后续才能继续加：

- 每一步保存中间结果。
- 对草稿做质量检查。
- 接入数据库保存文章。
- 接入人工审核。

如果要把写作升级成多个 Agent 协同，并且让验证结果驱动下一轮修改，继续看 [写文章多 Agent 工作流](../multi-agent-interaction/09-writing-multi-agent-workflow.md)。

[上一节：11. 连接数据库](11-database-agent.md) · [下一节：13. Coding Agent](13-coding-agent.md)
