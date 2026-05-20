# 02. Planning Agent

[返回专题首页](README.md)

本节只增加一个能力：在执行复杂任务前，先生成计划。

前面的 Code Review Agent 是“接到任务就开始读文件并审查”。这对小任务可以，对复杂任务容易漏文件、漏重点。Planning Agent 的作用是先把任务拆清楚。

## 本节任务

输入：

```text
请 review 这个 Agent 项目的工具调用安全性
```

Planning Agent 输出：

```json
{
  "goal": "审查工具调用安全性",
  "steps": [
    "定位 tool schema 定义",
    "定位 executeTool 分发逻辑",
    "检查高风险工具是否需要确认",
    "检查未知工具是否拒绝",
    "输出带文件行号的 findings"
  ],
  "files_to_inspect": [
    "main.go",
    "internal/tools/*.go"
  ],
  "acceptance_criteria": [
    "每个问题必须有文件和行号",
    "不能输出没有源码证据的问题",
    "高风险动作必须说明权限边界"
  ]
}
```

## 和上一节相比新增什么

新增一个单独的 Planner：

```text
用户任务 -> Planning Agent -> plan JSON -> Review Agent
```

Planner 不负责最终 review。它只负责拆任务、定义范围和验收标准。

## Planner 输出 schema

```json
{
  "goal": "string",
  "steps": ["string"],
  "files_to_inspect": ["string"],
  "acceptance_criteria": ["string"]
}
```

## 整个流程

```text
用户提交复杂任务
  ↓
Planning Agent 生成计划
  ↓
Coordinator 检查计划是否完整
  ↓
把 plan 传给 Review Agent
  ↓
Review Agent 按计划执行
```

## 本节学到什么

Planner Agent 解决的是“先做什么、看哪些文件、结果怎样算完成”。

它让后面的 Agent 不用自己猜任务边界，从而减少遗漏和跑偏。

[上一节：01. Code Review Agent](01-code-review-agent.md) · [下一节：03. Verification Agent](03-verification-agent.md)
