# 06. 顺序调度多个 Agent

[返回专题首页](README.md)

本节只增加一个能力：把多个 Agent 串起来，让一个任务按顺序交给不同 Agent。

这一步先不做并行，也不做复杂队列。先让新手理解最基本的调度方式：A 做完，把结构化结果交给 B，B 做完再交给 C。

## 本节任务

输入：

```text
请 review 这个项目的工具调用安全性
```

调度顺序：

```text
Planner Agent -> Review Agent -> Verification Agent -> Final Reporter
```

## Agent 分工

| Agent | 输入 | 输出 |
| --- | --- | --- |
| Planner | 用户任务 | `plan JSON` |
| Reviewer | `plan JSON` + 文件工具 | `findings JSON` |
| Verifier | `findings JSON` + 文件工具 | `verified JSON` |
| Reporter | `verified JSON` | 最终报告 |

## Go 里的调度骨架

```go
func RunReviewWorkflow(task string) (string, error) {
	plan, err := planner.Run(task)
	if err != nil {
		return "", err
	}

	findings, err := reviewer.Run(plan)
	if err != nil {
		return "", err
	}

	verified, err := verifier.Run(findings)
	if err != nil {
		return "", err
	}

	report, err := reporter.Run(verified)
	if err != nil {
		return "", err
	}

	return report, nil
}
```

## 整个流程

```text
用户任务
  ↓
Planner 产出计划
  ↓
Reviewer 按计划审查
  ↓
Verifier 复查证据
  ↓
Reporter 汇总报告
  ↓
返回最终结果
```

## 本节学到什么

多 Agent 调度的第一版就是函数调用链。不要一开始就上复杂框架。

关键是每个 Agent 的输出必须结构化，否则下一个 Agent 无法稳定接住。

[上一节：05. 主 Agent 和子 Agent 的消息分发](05-message-task-dispatch.md) · [下一节：07. 多 Agent 协同完成 Code Review](07-collaborative-code-review.md)
