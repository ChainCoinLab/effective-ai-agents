# 04. 创建子 Agent

[返回专题首页](README.md)

本节只增加一个能力：主 Agent 根据任务创建子 Agent。

## 本节任务

用户提交：

```text
请 review 这个项目的工具调用安全性
```

Coordinator 创建三个子 Agent：

```text
planner
reviewer
verifier
```

## Agent 定义

```go
type AgentRole string

const (
	RolePlanner  AgentRole = "planner"
	RoleReviewer AgentRole = "reviewer"
	RoleVerifier AgentRole = "verifier"
)

type Agent struct {
	ID     string
	Role   AgentRole
	System string
	Tools  []Tool
}
```

## 创建子 Agent

```go
func NewSubAgent(role AgentRole) Agent {
	switch role {
	case RolePlanner:
		return Agent{ID: "agent_planner", Role: role, System: "You create review plans."}
	case RoleReviewer:
		return Agent{ID: "agent_reviewer", Role: role, System: "You review code with evidence.", Tools: codeReadTools()}
	case RoleVerifier:
		return Agent{ID: "agent_verifier", Role: role, System: "You verify findings with evidence.", Tools: codeReadTools()}
	default:
		panic("unknown role")
	}
}
```

## 整个流程

```text
Coordinator 接收任务
  ↓
根据任务类型选择 Agent 角色
  ↓
创建 Planner / Reviewer / Verifier
  ↓
为每个 Agent 绑定 system prompt 和工具权限
```

## 本节学到什么

子 Agent 不是另一个魔法模型，而是一组配置：

- role
- system prompt
- tools
- 输入输出 schema
- 权限边界

[上一节：03. Verification Agent](03-verification-agent.md) · [下一节：05. 主 Agent 和子 Agent 的消息分发](05-message-task-dispatch.md)

