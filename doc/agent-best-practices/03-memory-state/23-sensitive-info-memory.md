## Status
Recommended

Category: memory-state

## Rule
敏感信息不默认进入长期记忆。

## Why
敏感信息跨会话保留会扩大泄露、误用和合规风险。即使用户在一次任务中提供，也不代表同意长期保存。

## Optimize
默认排除密钥、凭据、身份标识、健康、财务、未公开业务信息等内容。确需保存时，要求明确目的、最小字段、权限边界和删除路径。

## Verify
用包含密码、Token、身份证明和私人偏好的样例测试写入逻辑，确认敏感内容被拒绝或需要显式确认。

## References
- OpenAI Model Spec: privacy and sensitive information
- OWASP: secrets management principles

---

[返回全局摘要](../README.md) · [返回本组：记忆与状态管理](README.md)
