# 25. 工具接口要小而清晰

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)

## Status
Recommended

Category: tools-agents

## Rule
工具接口要小而清晰。

## Why
模型选择和填参依赖工具描述。接口过大、参数含糊或副作用太多，会增加误调用和难以验证的行为。

工具接口对 Agent 来说就是行动空间。接口越模糊，模型越容易误解；接口越大，参数组合越多，错误面越大；副作用越隐藏，执行风险越难控制。

坏工具通常长这样：

```json
{
  "name": "manage_user",
  "description": "管理用户",
  "parameters": {
    "action": "string",
    "data": "string"
  }
}
```

这个工具的问题是：它同时承担查询、创建、修改、删除等多种动作；`action` 和 `data` 都是自由字符串；风险等级不清；下游无法做精确权限控制。模型只要填出看似合理的字符串，执行器就很难判断是否安全。

更好的方式是拆成小工具：

```text
get_user_profile(user_id)
list_user_orders(user_id, limit)
update_user_email(user_id, new_email)
deactivate_user(user_id, reason, confirmation_token)
```

每个工具的动作、参数、风险和返回值都清楚，应用层才能分别控制权限、确认和审计。

## Optimize
一个工具只做一个明确动作。参数使用结构化类型、枚举、必填约束和清楚的错误返回，避免万能字符串和隐藏副作用。

工具设计时至少检查：

| 维度 | 要求 |
| --- | --- |
| 名称 | 动词 + 对象，表达具体动作 |
| 描述 | 写清用途、前置条件、副作用、何时不用 |
| 参数 | 类型明确，必填/可选清楚，枚举和范围有限 |
| 返回 | 结构化，包含成功、失败、错误类型和可重试性 |
| 权限 | 可按资源、租户、动作和风险等级校验 |
| 幂等 | 写操作有幂等键或重复执行保护 |
| 审计 | 能记录调用者、参数、结果和确认信息 |

参数要避免“万能字符串”。如果用户只能选择 `draft | published | archived`，就不要让模型填任意 `status: string`。如果金额必须是正数且单位为分，就在 schema 里写清 `amount_cents`、最小值和货币字段。

错误返回也要结构化：

```json
{
  "ok": false,
  "error_type": "permission_denied",
  "message": "current user cannot update this resource",
  "retryable": false,
  "user_action_required": "request_permission"
}
```

这样 Agent 才能基于错误选择澄清、换工具、请求权限或停止，而不是反复重试。

## Engineering Notes

- 只读工具和写工具分开。不要让一个工具既查询又修改。
- 高风险工具单独命名和分级，避免隐藏在普通工具里。
- 工具返回不要是大段不可解析文本；必要时提供摘要和 artifact 引用。
- 工具 schema 改动要版本化，并跑工具选择和参数回归测试。
- 工具少不等于功能弱。清晰的小工具更容易组合、授权和验证。

## Verify
让模型仅凭工具名、描述和 schema 选择调用，检查是否能稳定选对工具并填对参数。

还应测试：

- 相似工具能否稳定区分。
- 缺字段时是否请求澄清，而不是乱填。
- 非法枚举、越界数值、路径逃逸能否被 schema 或执行器拒绝。
- 写工具是否有确认、幂等和审计记录。
- 工具失败是否返回结构化 observation。

## References
- OpenAI Function Calling: tool schema design
- OpenAI Agents SDK: tools
- JSON Schema / typed DTO
- 工具调用 trace

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
