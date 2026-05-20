# 10. 增加任务状态和轮询

[返回专题首页](README.md)

本节只增加一个能力：把一次同步调用，改成可查询状态的任务。

## 本节任务

用户提交一个任务：

```text
帮我总结这段长文本
```

程序立即返回：

```json
{
  "task_id": "task_001",
  "status": "running"
}
```

然后用户可以轮询：

```text
GET /tasks/task_001
```

得到：

```json
{
  "task_id": "task_001",
  "status": "succeeded",
  "result": "..."
}
```

## 和上一节相比新增什么

新增任务状态：

```go
type TaskStatus string

const (
	StatusPending   TaskStatus = "pending"
	StatusRunning   TaskStatus = "running"
	StatusSucceeded TaskStatus = "succeeded"
	StatusFailed    TaskStatus = "failed"
)
```

新增任务结构：

```go
type Task struct {
	ID     string
	Status TaskStatus
	Input  string
	Result string
	Error  string
}
```

## 整个流程

```text
用户提交任务
  ↓
Go 创建 task_id
  ↓
任务进入 running
  ↓
后台调用 Agent
  ↓
成功则 status=succeeded
  ↓
失败则 status=failed
  ↓
用户通过 task_id 轮询结果
```

## 本节学到什么

长任务不要一直阻塞 HTTP 请求。Agent 工程里常见做法是：

```text
提交任务
立即返回 task_id
后台执行
前端或调用方轮询状态
```

[上一节：09. 接入 MCP Server](09-mcp-server.md) · [下一节：11. 连接数据库](11-database-agent.md)

