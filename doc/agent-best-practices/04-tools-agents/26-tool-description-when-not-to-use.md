## Status
Recommended

Category: tools-agents

## Rule
工具描述要写清楚何时使用，也要写清楚何时不用。

## Why
只描述能力会让模型过度调用工具。明确排除条件能减少无意义调用、权限请求和错误路径。

## Optimize
在描述中加入适用场景、禁止场景、前置条件和替代方式。例如“仅在需要实时数据时使用；不应用于用户已经提供完整数据的情况”。

## Verify
用不需要工具的样例提示测试，确认模型不会为了确认常识、重复已有信息或执行低价值操作而调用工具。

## References
- OpenAI Function Calling: tool descriptions
- OpenAI Prompt Engineering: instruction clarity

---

[返回全局摘要](../README.md) · [返回本组：工具调用与多 Agent](README.md)
