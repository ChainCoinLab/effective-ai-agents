## Status
Recommended

Category: tools-agents

## Rule
工具失败是正常路径，不是异常边角。

## Why
网络、权限、配额、输入、依赖服务和用户取消都会导致失败。Agent 如果没有失败策略，会编造结果或卡在循环重试。

## Optimize
为工具返回结构化错误、可重试标志、用户可操作信息和安全降级方案。限制自动重试次数，失败后明确说明已知和未知内容。

## Verify
注入超时、403、404、限流和无效参数错误，确认 Agent 能停止、解释或请求补充，而不是假装成功。

## References
- OpenAI Agents SDK: error handling
- Resilience engineering: retries, timeouts, fallbacks

---

[返回全局摘要](../README.md) · [返回本组：MCP、工具调用与多 Agent](README.md)
