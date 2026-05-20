# 08. 给高风险工具加确认

[返回专题首页](README.md)

本节只增加一个能力：高风险工具不能直接执行，必须先让用户确认。

## 本节任务

新增一个写文件工具：

```text
write_file(path, content)
```

当 Claude 请求写文件时，Go 程序不立刻执行，而是先打印：

```text
Claude 请求写入文件：
path: demo.txt
content: ...

是否执行？输入 yes 确认：
```

只有用户输入 `yes`，Go 才真正写文件。

## 和上一节相比新增什么

工具分成两类：

```go
type ToolRisk string

const (
	RiskLow  ToolRisk = "low"
	RiskHigh ToolRisk = "high"
)
```

执行前判断：

```go
if risk == RiskHigh {
	ok := askUserConfirmation(toolUse)
	if !ok {
		return "user rejected this tool call", nil
	}
}
```

## 整个流程

```text
Claude 返回 write_file tool_use
  ↓
Go 识别这是高风险工具
  ↓
Go 打印将要执行的操作
  ↓
用户输入 yes
  ↓
Go 执行写文件
  ↓
Go 返回 tool_result
```

## 本节学到什么

模型只负责提出调用意图，应用负责权限和执行。

这是 Agent 工程里很重要的一条边界：

```text
intent by model
permission by application
execution by application
```

[上一节：07. 支持多个工具](07-multi-tools.md) · [下一节：09. 接入 MCP Server](09-mcp-server.md)

