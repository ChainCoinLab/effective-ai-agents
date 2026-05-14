## Status
Recommended

Category: tools-agents

## Rule
工具接口要小而清晰。

## Why
模型选择和填参依赖工具描述。接口过大、参数含糊或副作用太多，会增加误调用和难以验证的行为。

## Optimize
一个工具只做一个明确动作。参数使用结构化类型、枚举、必填约束和清楚的错误返回，避免万能字符串和隐藏副作用。

## Verify
让模型仅凭工具名、描述和 schema 选择调用，检查是否能稳定选对工具并填对参数。

## References
- OpenAI Function Calling: tool schema design
- OpenAI Agents SDK: tools

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
