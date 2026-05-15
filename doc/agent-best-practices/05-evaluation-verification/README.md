# 测试、评测与验证

[返回全局摘要](../README.md)

本模块关注 Agent 的测试体系、评测数据、过程验证、风险阈值和失败分类。目标是判断每次变更是否改善了系统，而不是只依赖主观感受。

## 实践点

- [35. AI 系统需要扩展测试金字塔](35-extended-test-pyramid.md)
- [36. Eval 数据集覆盖真实分布和边界](36-eval-data-real-boundary.md)
- [37. 不只测最终答案，也测中间过程](37-test-intermediate-process.md)
- [38. LLM-as-judge 需要校准](38-calibrate-llm-as-judge.md)
- [39. 评测指标和业务风险绑定](39-metrics-bind-business-risk.md)
- [40. 影响输出的变更都要跑回归](40-run-regression-on-changes.md)
- [41. 验证要包含反例和攻击样例](41-counterexample-attack-samples.md)
- [42. 把失败分类，而不是只记录失败率](42-failure-taxonomy.md)
- [42A. 可观测性要区分测试驱动和目标驱动](42A-observability-test-goal-driven.md)
