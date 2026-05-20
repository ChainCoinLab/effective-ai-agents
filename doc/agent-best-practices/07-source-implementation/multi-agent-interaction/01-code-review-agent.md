# 01. Code Review Agent

[返回专题首页](README.md)

本节只增加一个能力：基于上一节的文件读取工具，做一个 Code Review Agent。

它不是泛泛地评价代码，而是输出结构化审查结果：问题、文件、行号、原因、建议和严重级别。

## 本节任务

输入：

```text
请 review main.go，重点看错误处理和工具调用边界
```

输出：

```json
{
  "findings": [
    {
      "severity": "high",
      "file": "main.go",
      "line": 87,
      "issue": "工具名没有白名单校验",
      "reason": "模型返回的 tool_use 不能直接执行，否则可能触发未授权工具",
      "suggestion": "在 executeTool 中只允许显式注册的工具名"
    }
  ],
  "summary": "发现 1 个高风险问题"
}
```

## 和上一节相比新增什么

上一节解决的是“Agent 能读代码”。本节增加的是“读完代码后按 review 标准输出结果”。

新增 system prompt：

```text
你是 Code Review Agent。你必须先读取相关文件，再给出审查结论。
输出必须是 JSON。每个 finding 必须包含 severity、file、line、issue、reason、suggestion。
没有证据的问题不要输出。
```

## Review Agent 可用工具

```text
list_files
read_file
search_code
```

第一版不要给它写文件权限，也不要给它执行 shell 的权限。

## 输出 JSON schema

```json
{
  "findings": [
    {
      "severity": "low | medium | high",
      "file": "string",
      "line": 1,
      "issue": "string",
      "reason": "string",
      "suggestion": "string"
    }
  ],
  "summary": "string"
}
```

## 整个流程

```text
用户提交 review 任务
  ↓
Review Agent 判断需要看哪些文件
  ↓
调用 search_code 或 read_file
  ↓
读取源码
  ↓
按 review 标准分析
  ↓
输出结构化 findings
```

## 本节学到什么

Code Review Agent 的关键不是“让模型看看代码”，而是给它三层约束：

1. 只能用只读代码工具。
2. 必须引用文件和行号。
3. 必须输出机器可解析的 JSON。

下一节继续加一个角色：Planning Agent。复杂任务不直接 review，先让 Planner 拆计划。

[前置教程：文件读取 Coding Agent](../go-agent-from-zero/13-coding-agent.md) · [下一节：02. Planning Agent](02-planning-agent.md)
