# 01. 本地 stdio MCP Server

[返回专题首页](README.md)

本节只完成一个小任务：启动一个本地 MCP Server，通过 stdio 提供一个固定工具。

## 本节任务

工具名：

```text
ping
```

返回：

```json
{
  "ok": true
}
```

## 本节学到什么

本地 MCP 的核心是：

```text
Agent 进程
  ↓ stdio
MCP Server 进程
  ↓
执行工具
  ↓
返回 tool result
```

这一节先不接数据库，只确认 MCP Server 能启动、能声明工具、能返回结果。

[下一节：02. 本地 MCP：列出数据库表](02-local-list-tables.md)

