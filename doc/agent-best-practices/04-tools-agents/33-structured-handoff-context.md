# 33. Agent handoff 要传结构化上下文

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)

## Status
Recommended

Category: tools-agents

## Rule
handoff 传结构化上下文，不只传聊天记录。

## Why
聊天记录冗长且含噪声。接收方需要明确任务目标、已完成事项、关键事实、约束、未决问题和可用资源。

handoff 的目标是让接收 Agent 从正确状态继续，而不是重新读一遍完整历史再猜发生了什么。完整聊天记录里有探索、错误尝试、废弃计划、用户纠正和工具噪声。直接传历史会增加成本，也会让接收方误用过期信息。

结构化 handoff 应回答：

| 问题 | 字段 |
| --- | --- |
| 要继续完成什么 | `objective` |
| 现在做到哪里 | `state` |
| 已确认事实是什么 | `facts` |
| 证据在哪里 | `evidence_refs` |
| 有哪些约束和禁止动作 | `constraints` |
| 还有什么没解决 | `open_questions` |
| 下一步建议是什么 | `next_actions` |
| 风险和权限边界是什么 | `risks`、`permissions` |

## Optimize
定义交接 schema，包括 objective、state、decisions、evidence、open_questions、next_actions 和 risks。只传接收方完成任务所需内容。

示例 schema：

```json
{
  "objective": "验证 README 修改是否与 package.json 脚本一致",
  "state": {
    "status": "ready_for_verification",
    "completed_steps": ["read_package_json", "edit_readme"]
  },
  "facts": [
    {
      "claim": "docs:build 脚本存在",
      "source": "package.json:scripts.docs:build"
    }
  ],
  "decisions": [
    {
      "decision": "不修改部署配置",
      "reason": "用户只要求补充文档内容"
    }
  ],
  "open_questions": [],
  "next_actions": ["run docs build", "inspect changed README section"],
  "constraints": ["不要修改无关文件"],
  "risks": ["文档链接可能失效"],
  "artifacts": ["README.md", "package.json"]
}
```

handoff 内容要“够用但不过量”。接收 Agent 不需要知道所有思考过程，只需要知道可验证事实、当前状态和下一步输入。如果它需要原始证据，应通过 `evidence_refs` 去读取 artifact，而不是在 handoff 里塞满原文。

## Engineering Notes

- handoff schema 要版本化。字段变化会影响接收 Agent 行为。
- 传事实时要带来源，不要传无来源总结。
- 传决策时要说明原因和是否可撤销。
- 传风险时要写出需要接收方检查什么，而不是泛泛说“注意风险”。
- 对敏感信息使用引用，不要把密钥、个人数据或生产日志直接塞进 handoff。

## Verify
让接收 Agent 在不读取完整历史的情况下继续任务，确认它能正确执行下一步并说明依据。

还应测试：

- handoff 缺少关键字段时，接收 Agent 是否请求补充。
- 接收 Agent 是否能通过 `evidence_refs` 找回证据。
- 过期决策或被用户否定的信息是否不会进入 handoff。
- 多 Agent 连续交接后，状态是否仍能恢复和验证。
- handoff 中的约束是否被接收方遵守。

## References
- OpenAI Agents SDK: handoffs
- Structured context and task state patterns
- Handoff schema 设计
- Agent 状态交接测试

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
