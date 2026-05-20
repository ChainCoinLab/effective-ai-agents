# 05. 主 Agent 和子 Agent 的消息分发

[返回专题首页](README.md)

本节只增加一个能力：定义主 Agent 和子 Agent 之间传递任务、消息和结果的结构。

## 本节任务

Coordinator 把用户任务分发给 Planner：

```json
{
  "task_id": "task_001",
  "target_agent": "agent_planner",
  "instruction": "为代码审查生成计划",
  "input": {
    "user_task": "请 review 这个项目的工具调用安全性"
  }
}
```

Planner 返回结构化结果：

```json
{
  "task_id": "task_001",
  "from_agent": "agent_planner",
  "status": "succeeded",
  "output": {
    "goal": "审查工具调用安全性",
    "files_to_inspect": ["main.go"],
    "acceptance_criteria": ["每个 finding 必须有文件和行号"]
  }
}
```

## 任务结构

```go
type AgentTask struct {
	TaskID      string                 `json:"task_id"`
	TargetAgent string                `json:"target_agent"`
	Instruction string                `json:"instruction"`
	Input       map[string]interface{} `json:"input"`
}
```

## 结果结构

```go
type AgentResult struct {
	TaskID    string                 `json:"task_id"`
	FromAgent string                `json:"from_agent"`
	Status    string                `json:"status"`
	Output    map[string]interface{} `json:"output,omitempty"`
	Error     string                `json:"error,omitempty"`
}
```

## 分发函数

```go
func Dispatch(agent Agent, task AgentTask) (AgentResult, error) {
	if task.TargetAgent != agent.ID {
		return AgentResult{}, fmt.Errorf("task target mismatch")
	}

	// 这里调用对应 Agent 的模型请求。
	// 输出必须解析成 AgentResult，而不是只返回一段自然语言。
	return agent.Run(task)
}
```

## 整个流程

```text
Coordinator 生成 AgentTask
  ↓
检查 target_agent
  ↓
把 task 交给对应子 Agent
  ↓
子 Agent 返回 AgentResult
  ↓
Coordinator 把 result 写入工作上下文
```

## 本节学到什么

多 Agent 协作最容易断的地方是“交接”。所以主 Agent 和子 Agent 之间不要只传自然语言，要传结构化任务和结构化结果。

[上一节：04. 创建子 Agent](04-create-sub-agent.md) · [下一节：06. 顺序调度多个 Agent](06-sequential-dispatch.md)

