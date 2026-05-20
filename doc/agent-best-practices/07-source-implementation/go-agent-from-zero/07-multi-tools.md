# 07. 支持多个工具

[返回专题首页](README.md)

本节只增加一个能力：让 Agent 不止有一个工具，而是能在多个工具之间选择。

## 本节任务

同时提供两个工具：

- `get_time`：获取当前时间。
- `calculator`：计算简单表达式。

输入：

```text
现在几点？另外帮我算一下 12 * 8 + 5
```

输出目标：

```text
现在时间是 ...，12 * 8 + 5 的结果是 101。
```

## 和上一节相比新增什么

上一节只有一个工具。本节把 `Tools` 改成工具列表：

```go
Tools: []Tool{
	getTimeTool(),
	calculatorTool(),
}
```

执行工具时用 `switch toolUse.Name` 分发：

```go
switch toolUse.Name {
case "get_time":
	return getTime(), nil
case "calculator":
	return runCalculator(toolUse.Input)
default:
	return "", fmt.Errorf("unknown tool: %s", toolUse.Name)
}
```

## 整个流程

```text
用户输入
  ↓
Claude 看到 tools 列表
  ↓
Claude 选择 get_time 或 calculator
  ↓
Go 按 tool name 分发执行
  ↓
Go 返回一个或多个 tool_result
  ↓
Claude 汇总工具结果并回答
```

## 本节学到什么

多工具 Agent 的核心不是工具数量，而是工具边界要清楚：

- 每个工具只做一件事。
- 每个工具都有明确输入 schema。
- Go 程序只执行白名单里的工具名。
- 未知工具必须拒绝。

[上一节：06. ReAct Agent](06-react-loop.md) · [下一节：08. 给高风险工具加确认](08-tool-confirmation.md)

