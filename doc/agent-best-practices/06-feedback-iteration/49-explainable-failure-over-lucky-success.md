# 49 可解释失败比偶然成功更有价值

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)


## Rule
调试和评估时，应优先追求可解释、可复现、可定位的失败，而不是依赖偶然成功样例证明系统可用。

## Why
偶然成功无法说明系统稳定性。可解释失败能暴露模型、上下文、工具或策略的真实短板，是持续改进的入口。

## Optimize
保留失败 trace、输入、检索结果、工具参数和输出版本；对非确定性任务记录多次运行结果和差异。

## Verify
复盘时确认关键失败能被复现并归因，且修复后对应样例进入回归集。

## References
- Reproducible debugging
- Error analysis for ML systems
- Observability for agent systems

---

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)
