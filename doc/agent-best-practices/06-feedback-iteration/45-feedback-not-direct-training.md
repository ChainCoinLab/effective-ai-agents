# 45 反馈不等于直接训练模型

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)


## Rule
用户反馈不应未经筛选就直接用于训练或微调模型，应先完成清洗、标注、授权、隐私和质量审查。

## Why
原始反馈可能包含隐私数据、恶意输入、错误偏好、噪声和版权风险。直接训练会把问题固化进模型行为。

## Optimize
先把反馈用于错误分析、eval 扩充、prompt 改进和知识库修正；只有高质量、合规、代表性数据才进入训练流程。

## Verify
检查训练数据来源是否有授权、脱敏、标注质量和采样标准记录。

## References
- Data governance for ML
- Privacy-preserving ML practices
- Feedback data quality review

---

[返回全局摘要](../README.md) · [返回本组：反馈闭环与迭代](README.md)
