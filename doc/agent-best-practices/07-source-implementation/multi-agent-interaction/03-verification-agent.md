# 03. Verification Agent

[返回专题首页](README.md)

本节只增加一个能力：让另一个 Agent 独立复查 review 结果。

Review Agent 可能误报、漏报，或者给出没有证据的结论。Verification Agent 不负责找新问题，它负责检查已有结果是否成立。

## 本节任务

输入：

```json
{
  "plan": "...",
  "review_findings": [
    {
      "severity": "high",
      "file": "main.go",
      "line": 87,
      "issue": "工具名没有白名单校验"
    }
  ]
}
```

Verification Agent 输出：

```json
{
  "verified_findings": [
    {
      "status": "confirmed",
      "file": "main.go",
      "line": 87,
      "reason": "源码中 executeTool 直接按模型返回的 name 分发"
    }
  ],
  "rejected_findings": [],
  "missing_evidence": []
}
```

## 和上一节相比新增什么

新增独立验证角色：

```text
Review Agent 输出 findings
  ↓
Verification Agent 读取同一份源码证据
  ↓
确认、驳回或标记证据不足
```

## Verification Agent 的规则

```text
你是 Verification Agent。
你不负责提出新需求。
你只检查 review finding 是否被源码证据支持。
没有文件和行号的 finding 必须标记为 missing_evidence。
无法从源码确认的问题必须标记为 rejected 或 needs_more_context。
```

## 整个流程

```text
Review Agent 产出 findings
  ↓
Verifier 读取 finding 指向的文件和行号
  ↓
检查 issue 是否真的成立
  ↓
输出 confirmed / rejected / missing_evidence
  ↓
Coordinator 只保留 verified findings
```

## 本节学到什么

多 Agent 不是为了热闹，而是为了分离职责：

- Review Agent 负责发现问题。
- Verification Agent 负责检查问题是否有证据。

这一步能明显降低误报。

[上一节：02. Planning Agent](02-planning-agent.md) · [下一节：04. 创建子 Agent](04-create-sub-agent.md)
