# 37 不只测最终答案也测中间过程

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)


## Rule
评测应检查中间过程，包括任务分解、检索依据、工具参数、权限判断、引用来源和拒答路径。

## Why
最终答案正确不代表过程可靠。错误的工具调用、伪造依据或绕过权限可能暂时给出可用答案，却会在生产中放大风险。

## Optimize
为关键链路增加结构化 trace，并在 eval 中断言关键步骤是否发生、顺序是否正确、参数是否符合约束。

## Verify
抽查失败和成功样例的 trace，确认评测能识别“答案对但过程错”的情况。

## References
- Agent tracing practices
- Tool-use evaluation patterns
- Chain-of-thought privacy and process supervision research

---

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)
