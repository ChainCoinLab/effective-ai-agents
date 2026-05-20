# 09. 接入 MCP Server

[返回专题首页](README.md)

本节只增加一个能力：把本地工具从 Go 代码里的函数，拆到 MCP Server 里。

## 本节任务

实现一个最小 MCP Server，暴露一个工具：

```text
get_project_info
```

Agent 调用这个工具后，返回当前项目名称和说明。

## 和上一节相比新增什么

前面工具是 Go 进程里的函数：

```text
Claude tool_use -> Go switch -> 本地函数
```

本节改成：

```text
Claude tool_use -> Go MCP client -> MCP server -> tool result
```

## 为什么要接 MCP

MCP 的价值是把工具协议标准化：

- 工具可以由不同进程提供。
- 工具 schema 可以被统一发现。
- Agent 不需要把所有工具都写在一个文件里。
- 多个 Agent 可以复用同一个工具服务。

## 整个流程

```text
启动 MCP Server
  ↓
Go Agent 读取 MCP tools
  ↓
Claude 选择某个 MCP tool
  ↓
Go Agent 把 tool call 转发给 MCP Server
  ↓
MCP Server 返回结果
  ↓
Go Agent 把 tool_result 发回 Claude
```

## 本节学到什么

MCP 不是替代 tool use。MCP 是工具提供方式，tool use 是模型请求工具的方式。

两者关系：

```text
Claude tool_use 是“模型想调用工具”
MCP 是“工具在哪里、如何被调用”
```

[上一节：08. 给高风险工具加确认](08-tool-confirmation.md) · [下一节：10. 增加任务状态和轮询](10-task-status-polling.md)

