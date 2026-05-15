# 面试官：大模型的 function calling 是怎么实现的？ 结构化内容

## 一句话概括

Function calling 不是模型直接运行代码，而是模型基于工具定义生成受约束的结构化调用请求，应用后端负责执行真实 API、校验权限与参数，并把结果回填给模型完成回答。

## 主题关键词

Function calling、tool calling、JSON Schema、SFT、special tokens、constraint decoding、FSM/GBNF、tool retrieval、strict mode、Pydantic、observability、测试驱动观测、目标驱动观测、HITL、安全拦截

## 背景

来源: https://www.bilibili.com/video/BV1qH9YBREfD  
处理状态: 已提炼  
说明: 原始转写有 ASR 误识别，本文件已人工校正常见术语，例如 function calling、JSON Schema、约束解码、Pydantic、权限校验、HITL。

## 问题

- 面试官问这个题，不是为了考几行 SDK 调用代码，而是看候选人是否理解大模型从“对话框”变成“Agent 执行器”的机制。
- 模型本身仍然是 next token 预测器，不会天然联网、查库或运行代码。外部动作来自应用层工具执行。
- 真正要解释清楚的是：模型为什么会输出工具调用格式、为什么 JSON 结构通常稳定、后端如何安全执行并处理失败。

## 方法

把 function calling 拆成一个闭环：

1. 开发者把函数名、描述、参数结构和约束以 JSON Schema 等形式提供给模型。
2. 用户提出问题后，模型判断是否需要外部能力。如果需要，就生成工具名和参数，而不是直接编造答案。
3. 应用后端解析这段结构化调用，校验参数与权限，执行真实 API、数据库、代码解释器或业务动作。
4. 应用把工具返回结果作为 observation 回填给模型。
5. 模型基于 observation 组织最终自然语言回复，或继续下一轮工具调用。

底层能力可以从三点解释：

- SFT/指令微调：用带标签的工具调用样本教模型在特定场景下输出工具调用，而不是闲聊式回答。
- Special tokens/结构化输出模式：模型能用特殊标记进入“我要调用工具”的生成路径。
- 约束解码：推理层根据 schema、有限状态机或 GBNF 语法限制可选 token，保证输出满足 JSON 语法和字段约束。它保证的是语法形状，不等于参数语义一定正确。

这个视频还能延伸出一个更通用的工程实践：可观测性不是工具调用专属能力，而是一种观察模式设计。常见可以分成两类：

- 测试驱动观测：从测试、eval、断言和回归样例出发，先定义“应该发生什么”，再收集能证明它发生或没发生的信号。它回答的是：系统链路有没有按设计运行。
- 目标驱动观测：从用户目标、业务目标、任务成功标准或 SLO 出发，先定义“要达成什么”，再反推要观察哪些链路指标。它回答的是：这个设计有没有真正服务目标。
- 运行期 telemetry：通过 traces、metrics、logs、events 和上下文传播，把实际发生的过程暴露出来。测试驱动观测提供验证入口，目标驱动观测提供优化方向，telemetry 提供事实证据。

## 时间线要点

- `00:00` 提问意图：考察候选人是否理解 Agent 的动作机制，而不是 SDK 用法。
- `00:33` 认知纠偏：模型不会自己执行代码或联网，本质仍是概率生成器。
- `00:55` 工具定义：开发者把函数 schema 放进系统上下文，告诉模型可用能力和参数格式。
- `01:13` 调用闭环：模型输出 JSON 参数，后端执行 API，结果再回填给模型。
- `02:01` 训练来源：SFT 让模型学会在工具场景下生成指定格式的调用。
- `02:23` 结构化模式：special tokens 可以标记工具调用或结构化生成路径。
- `02:46` 约束解码：推理引擎按 schema 限制下一个 token，减少 JSON 语法错误。
- `03:26` 工程坑：参数幻觉、工具过多导致选择混乱、格式不稳定、安全越权。
- `04:19` 恢复策略：开启 strict mode，后端用强类型校验，失败后把错误反馈给模型重写。
- `04:44` 安全边界：敏感动作必须应用层硬校验，高风险操作引入 HITL 人工确认。

## 结论

- 本质：function calling 是受限的结构化参数生成，不是模型执行代码。
- 底层：它来自 SFT 学到的调用模式，加上推理层 schema/语法约束来提升 JSON 稳定性。
- 工程：生产可用性不只看模型能力，更看后端的工具检索、参数校验、错误重试、权限拦截和人工确认。

## 可复用面试回答

Function calling 的实现可以分三层讲。第一层是交互协议：开发者把工具描述和 JSON Schema 给模型，模型在需要外部能力时输出工具名和参数，应用后端执行真实 API，再把结果作为 observation 回填给模型。第二层是模型能力：模型通过 SFT/指令微调学会在特定场景下输出工具调用，推理时可能用 special tokens 标记结构化调用模式，并通过 constrained decoding、FSM 或 GBNF 约束 JSON 语法。第三层是工程落地：后端必须做工具检索、参数强校验、错误闭环、安全权限控制，高风险动作不能让模型直接执行，需要 HITL 确认。

## 延伸：可观测性的两种观测模式

| 观测模式 | 起点 | 代表意思 | 常见实践 |
| --- | --- | --- | --- |
| 测试驱动观测 | 测试、eval、断言、回归样例 | 先定义预期行为，再观察链路是否按预期发生 | 在 trace 中记录步骤、输入、输出、工具参数、权限判断和错误类型；失败样例进入回归集 |
| 目标驱动观测 | 用户目标、业务目标、任务成功标准、SLO | 先定义要达成的目标，再反推需要观察的指标和链路 | 观察任务成功率、人工接管率、拒答率、成本、延迟、工具失败率、安全拦截率、投诉率 |
| Telemetry | traces、metrics、logs、events | 提供事实证据，不直接替代目标或测试 | 把每次请求链路、模型决策、工具调用、异常恢复和用户反馈串起来 |

资料参考：

- OpenTelemetry Observability Primer: https://opentelemetry.io/docs/concepts/observability-primer/
- OpenTelemetry Signals: https://opentelemetry.io/docs/concepts/signals/
- Martin Fowler, Test-Driven Development: https://martinfowler.com/bliki/TestDrivenDevelopment.html
- Pearson, Kent Beck, Test-Driven Development: By Example: https://www.pearson.com/en-us/subject-catalog/p/test-driven-development-by-example/P200000003788/9780321146533
- SLO and observability practices
