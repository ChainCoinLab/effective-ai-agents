# 07. 多 Agent 协同完成 Code Review

[返回专题首页](README.md)

本节把前面的能力合起来，完成一个最小多 Agent Code Review 系统。

这不是新增某一个工具，而是把调度、计划、读取、审查、验证和汇总连成一个完整工作场景。

## 本节任务

输入：

```text
请 review 当前项目的 Agent 工具调用安全性，并输出最终审查报告
```

输出：

```json
{
  "summary": "发现 2 个已验证问题",
  "findings": [
    {
      "severity": "high",
      "file": "main.go",
      "line": 87,
      "issue": "...",
      "evidence": "...",
      "suggestion": "..."
    }
  ],
  "rejected_findings": [
    {
      "issue": "...",
      "reason": "源码证据不足"
    }
  ]
}
```

## 工作场景

```text
1. Coordinator 接收用户任务
2. Planner Agent 拆计划
3. Reader Agent 按计划读取文件
4. Review Agent 输出 findings
5. Verification Agent 复查 findings
6. Reporter Agent 汇总最终报告
```

## 每个 Agent 的职责边界

| Agent | 能做什么 | 不能做什么 |
| --- | --- | --- |
| Coordinator | 调度流程、传递上下文 | 不直接审查代码 |
| Planner | 拆计划、定范围、定验收标准 | 不输出最终 finding |
| Reader | 读取文件、搜索代码 | 不评价代码质量 |
| Reviewer | 找问题、给建议 | 不确认自己的结论一定正确 |
| Verifier | 复查证据、驳回误报 | 不发明新问题 |
| Reporter | 汇总最终报告 | 不绕过验证直接采纳 finding |

## 上下文传递结构

```json
{
  "task": "用户原始任务",
  "plan": {},
  "files": [],
  "findings": [],
  "verified_findings": [],
  "rejected_findings": []
}
```

Coordinator 每一步只把下一个 Agent 需要的上下文传过去，不把全部历史无脑塞给所有 Agent。

## 整个流程

```text
用户任务
  ↓
Coordinator
  ↓
Planner: 生成计划
  ↓
Reader: 读取相关文件
  ↓
Reviewer: 输出 findings
  ↓
Verifier: confirmed / rejected
  ↓
Reporter: 输出最终报告
```

## 本节学到什么

到这里，新手应该能看懂一个多 Agent 系统怎么从简单闭环逐步长出来：

1. 先能调用模型。
2. 再能循环聊天。
3. 再能保存上下文。
4. 再能调用工具。
5. 再能读取代码。
6. 再能做 Code Review。
7. 再能计划和验证。
8. 最后才进入多 Agent 协作。

复杂度是逐层加上来的，不是一步跳到“多 Agent 框架”。

[上一节：06. 顺序调度多个 Agent](06-sequential-dispatch.md) · [下一节：08. 并行分发和结果合并](08-parallel-merge.md)
