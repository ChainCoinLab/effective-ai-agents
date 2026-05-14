# 41 验证包含反例攻击样例

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)


## Rule
验证集应包含反例、诱导、越权、提示注入、数据泄露和错误工具使用等攻击样例。

## Why
Agent 面向开放输入时，用户可能无意或有意触发危险路径。只测正常路径无法证明系统在对抗输入下仍能守住边界。

## Optimize
为每个安全约束设计正例和反例，并持续把真实攻击、误用和红队发现加入验证集。

## Verify
确认高风险能力都有拒答、降级或人工审核样例，并检查这些样例在发布前全部通过。

## References
- OWASP Top 10 for LLM Applications
- Prompt injection testing
- Red teaming guidance for AI systems

---

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)
