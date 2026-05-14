# 46 人工审核沉淀评测标准

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)


## Rule
人工审核不应只给通过或不通过结论，还应沉淀可复用的评分标准、边界案例和判定理由。

## Why
人工判断若不结构化，难以规模化复用，也无法校准 LLM-as-judge 或指导后续开发。

## Optimize
让审核员按固定维度标注：事实性、完整性、安全性、合规性、语气、引用和任务完成度，并记录关键判定依据。

## Verify
定期抽查审核结果，确认标准能被不同审核员一致使用，并能转化为 eval 断言或 judge rubric。

## References
- Human evaluation rubrics
- Inter-rater agreement
- Quality review guidelines

---

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)
