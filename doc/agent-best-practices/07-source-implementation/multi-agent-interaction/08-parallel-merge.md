# 08. 并行分发和结果合并

[返回专题首页](README.md)

本节只增加一个能力：主 Agent 把任务拆给多个子 Agent 并行执行，最后合并结果。

## 本节任务

Planner 判断需要审查三个文件：

```json
["main.go", "tools.go", "agent.go"]
```

Coordinator 创建三个 review 子任务：

```text
review main.go
review tools.go
review agent.go
```

三个 Reviewer 可以并行跑，最后由 Coordinator 合并 findings。

## Go 调度骨架

```go
func RunParallelReview(files []string) ([]Finding, error) {
	results := make(chan AgentResult, len(files))

	for _, file := range files {
		go func(file string) {
			task := AgentTask{
				TaskID:      "review_" + file,
				TargetAgent: "agent_reviewer",
				Instruction: "review one file",
				Input: map[string]interface{}{
					"file": file,
				},
			}
			result, _ := Dispatch(NewSubAgent(RoleReviewer), task)
			results <- result
		}(file)
	}

	var findings []Finding
	for range files {
		result := <-results
		findings = append(findings, parseFindings(result)...)
	}

	return dedupeFindings(findings), nil
}
```

## 合并规则

```text
同一 file + line + issue 视为重复 finding
高严重级别优先
没有证据的 finding 丢给 Verification Agent
多个文件的 finding 按 severity 排序
```

## 整个流程

```text
Planner 输出文件列表
  ↓
Coordinator 为每个文件创建子任务
  ↓
多个 Reviewer 并行执行
  ↓
Coordinator 收集结果
  ↓
去重、排序、交给 Verifier
```

## 本节学到什么

并行不是让多个 Agent 抢同一个任务，而是把任务切成互不冲突的小块。每个子 Agent 都要有明确输入、输出和边界。

[上一节：07. 多 Agent 协同完成 Code Review](07-collaborative-code-review.md)

