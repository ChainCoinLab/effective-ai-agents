# 40 Prompt/模型/知识库/工具变更跑回归

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)


## Rule
任何 prompt、模型、知识库、工具 schema、权限策略或编排逻辑变更，都应触发相关回归评测。

## Why
AI 系统依赖多个可变部件，小改动可能改变推理路径、检索命中、工具选择或输出风格。没有回归评测会让质量退化隐性进入生产。

## Optimize
按变更类型维护 eval 子集：prompt 变更跑核心任务，知识库变更跑检索和引用，工具变更跑参数和权限。

## Verify
CI 或发布流程中检查评测记录，确认变更对应的回归集已通过并可追溯到版本。

## References
- Continuous evaluation
- Regression testing
- Prompt and model versioning practices

---

[返回全局摘要](../README.md) · [返回本组：测试、评测与验证](README.md)
