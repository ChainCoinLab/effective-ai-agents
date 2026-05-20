# 09. 写文章多 Agent 工作流

[返回专题首页](README.md)

本节新增一个完整业务场景：用多个 Agent 协同完成一篇文章。

重点不是“一次调用模型写完文章”，而是展示多 Agent 如何多轮交互：先计划，再写作，再验证；验证发现问题后，不直接结束，而是把问题反馈给编辑或计划 Agent，进入下一轮。

## 本节任务

输入：

```text
写一篇 1500 字文章，主题是 Go Agent 工程入门，面向新手。
```

输出：

```json
{
  "status": "succeeded",
  "rounds": 2,
  "plan": {
    "audience": "Go 初学者",
    "outline": ["为什么需要 Agent", "最小 API 调用", "工具调用", "工程化边界"],
    "acceptance_criteria": ["结构清晰", "适合新手", "避免空泛", "包含可执行建议"]
  },
  "verification": {
    "passed": true,
    "issues": []
  },
  "final_article": "..."
}
```

## Agent 分工

| Agent | 输入 | 输出 | 不能做什么 |
| --- | --- | --- | --- |
| Coordinator | 用户任务、当前上下文 | 下一步要调用哪个 Agent | 不直接写文章 |
| Planner | 用户任务、验证反馈 | 写作计划、结构、验收标准 | 不写完整正文 |
| Writer | 写作计划 | 草稿 | 不自己判断最终通过 |
| Verifier | 写作计划、草稿 | 是否通过、问题列表、修改建议 | 不直接改稿 |
| Editor | 草稿、验证反馈 | 修改后的草稿 | 不改变用户目标 |
| Reporter | 最终草稿、验证结果 | 最终文章和过程摘要 | 不绕过验证 |

## 工作流上下文

Coordinator 维护一份结构化上下文，每一轮都更新它：

```json
{
  "task": "写一篇 1500 字文章，主题是 Go Agent 工程入门，面向新手。",
  "round": 1,
  "max_rounds": 3,
  "plan": {},
  "draft": "",
  "verification": {
    "passed": false,
    "issues": [],
    "revision_instruction": ""
  },
  "final_article": ""
}
```

不要把所有对话历史无脑塞给每个 Agent。Coordinator 只传当前 Agent 需要的上下文。

## ReAct 循环

这个写文章工作流也是 ReAct，只是 `Act` 不一定是工具调用，也可以是调用某个子 Agent。

```text
Reason: 判断当前上下文处于哪一步
  ↓
Act: 调用 Planner / Writer / Verifier / Editor / Reporter
  ↓
Observe: 读取子 Agent 返回的结构化结果
  ↓
Reason: 判断是否通过验证，是否需要下一轮
  ↓
Final: 输出最终文章
```

## 多轮流程

```text
用户任务
  ↓
Coordinator
  ↓
Planner: 生成写作计划
  ↓
Writer: 根据计划写草稿
  ↓
Verifier: 验证草稿
  ↓
如果通过
  ↓
Reporter: 输出最终文章

如果不通过，并且是小问题
  ↓
Editor: 根据反馈修改草稿
  ↓
Verifier: 再次验证

如果不通过，并且是结构性问题
  ↓
Planner: 根据反馈调整计划
  ↓
Writer: 重写草稿
  ↓
Verifier: 再次验证
```

## Go 结构体骨架

```go
type ArticleWorkflowContext struct {
	Task         string             `json:"task"`
	Round        int                `json:"round"`
	MaxRounds    int                `json:"max_rounds"`
	Plan         ArticlePlan        `json:"plan"`
	Draft        string             `json:"draft"`
	Verification VerificationResult `json:"verification"`
	FinalArticle string             `json:"final_article"`
}

type ArticlePlan struct {
	Audience           string   `json:"audience"`
	Outline            []string `json:"outline"`
	AcceptanceCriteria []string `json:"acceptance_criteria"`
}

type VerificationResult struct {
	Passed              bool     `json:"passed"`
	IssueLevel          string   `json:"issue_level"`
	Issues              []string `json:"issues"`
	RevisionInstruction string   `json:"revision_instruction"`
}

type ArticleWorkflowResult struct {
	Status       string             `json:"status"`
	Rounds       int                `json:"rounds"`
	Plan         ArticlePlan        `json:"plan"`
	Verification VerificationResult `json:"verification"`
	FinalArticle string             `json:"final_article"`
}
```

`IssueLevel` 用来决定下一步走向：

```text
none        通过，进入 Reporter
minor       小问题，交给 Editor 修改
structural 结构性问题，回到 Planner 调整计划
```

## 子 Agent 调用骨架

```go
func runPlan(ctx ArticleWorkflowContext) (ArticlePlan, error) {
	// 调用 Planner Agent。
	// 输入：task + 上一轮 verification issues。
	// 输出：ArticlePlan JSON。
	return ArticlePlan{}, nil
}

func runWrite(ctx ArticleWorkflowContext) (string, error) {
	// 调用 Writer Agent。
	// 输入：task + plan。
	// 输出：draft。
	return "", nil
}

func runVerify(ctx ArticleWorkflowContext) (VerificationResult, error) {
	// 调用 Verifier Agent。
	// 输入：task + plan + draft。
	// 输出：VerificationResult JSON。
	return VerificationResult{}, nil
}

func runEdit(ctx ArticleWorkflowContext) (string, error) {
	// 调用 Editor Agent。
	// 输入：draft + verification.revision_instruction。
	// 输出：revised draft。
	return "", nil
}

func runReport(ctx ArticleWorkflowContext) (ArticleWorkflowResult, error) {
	// 调用 Reporter Agent，或由 Go 直接组装最终结果。
	return ArticleWorkflowResult{
		Status:       "succeeded",
		Rounds:       ctx.Round,
		Plan:         ctx.Plan,
		Verification: ctx.Verification,
		FinalArticle: ctx.Draft,
	}, nil
}
```

## Coordinator 调度循环

```go
func RunWritingWorkflow(task string) (ArticleWorkflowResult, error) {
	ctx := ArticleWorkflowContext{
		Task:      task,
		MaxRounds: 3,
	}

	for round := 1; round <= ctx.MaxRounds; round++ {
		ctx.Round = round

		if round == 1 || ctx.Verification.IssueLevel == "structural" {
			plan, err := runPlan(ctx)
			if err != nil {
				return ArticleWorkflowResult{}, err
			}
			ctx.Plan = plan

			draft, err := runWrite(ctx)
			if err != nil {
				return ArticleWorkflowResult{}, err
			}
			ctx.Draft = draft
		} else {
			draft, err := runEdit(ctx)
			if err != nil {
				return ArticleWorkflowResult{}, err
			}
			ctx.Draft = draft
		}

		verification, err := runVerify(ctx)
		if err != nil {
			return ArticleWorkflowResult{}, err
		}
		ctx.Verification = verification

		if verification.Passed {
			return runReport(ctx)
		}
	}

	return ArticleWorkflowResult{
		Status:       "needs_human_review",
		Rounds:       ctx.MaxRounds,
		Plan:         ctx.Plan,
		Verification: ctx.Verification,
		FinalArticle: ctx.Draft,
	}, nil
}
```

## 一次失败后的上下文变化

第一轮验证失败：

```json
{
  "passed": false,
  "issue_level": "minor",
  "issues": [
    "第 2 节只讲概念，没有给出 Go 代码示例",
    "文章结尾缺少新手下一步行动建议"
  ],
  "revision_instruction": "补充一个 Go API 调用示例，并在结尾增加学习路径。"
}
```

Coordinator 观察到 `issue_level = minor`，所以第二轮不重新规划，直接调用 Editor。

第二轮验证通过：

```json
{
  "passed": true,
  "issue_level": "none",
  "issues": [],
  "revision_instruction": ""
}
```

Coordinator 进入 Reporter，输出最终文章。

## 本节学到什么

写文章多 Agent 工作流的关键是“验证驱动下一步”：

- 不是固定执行一轮。
- Verifier 的结果决定是否进入下一轮。
- 小问题走 Editor。
- 结构性问题回 Planner。
- 超过最大轮次进入人工审核。

这个模式也能迁移到代码生成、报告生成、数据分析和运营内容生产。

[上一节：08. 并行分发和结果合并](08-parallel-merge.md)

