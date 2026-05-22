# 从机器学习到 Agent：AI 工程知识结构

理解 AI 不能只停留在模型 API、Prompt 技巧或单个产品功能上。更完整的知识结构应该区分两条能力线：一条是大模型开发，关注模型本体、训练、微调、推理、评测和安全；另一条是 Agent 开发，关注如何调用模型、组织上下文、连接工具、管理状态和完成任务。

这两条线相互独立，又彼此关联。大模型开发要理解外部系统会怎样调用模型，以及调用方式会带来哪些问题；Agent 开发要理解自己调用的模型、RAG、记忆、工具和 MCP 各自有什么优势、缺陷和风险，然后用工程方式规避。

English: [Agent Engineering Best Practices Guide](guide.en.md)

## 基本判断

大模型不是一个独立完成所有事情的“智能体”。它更像一个强大的概率生成组件，擅长从上下文中识别模式、生成候选、补全推理链路和组织语言。但生产级 AI 系统不能只依赖模型本身：

- 事实要由检索、数据库、工具和外部系统提供。
- 权限要由应用层控制，而不是交给模型自行判断。
- 状态要由确定性系统记录，而不是只放在对话历史里。
- 结果要能验证，过程也要能观察。
- 失败要能恢复，不能只期待下一次模型“发挥好一点”。

所以 AI 工程不是“把 Prompt 写得更神奇”，而是把模型能力拆进一个边界清晰、过程可观测、结果可验证、失败可恢复的系统。

## 知识主线

| 能力域 | 核心问题 | 需要掌握的模块 |
| --- | --- | --- |
| [大模型原理基础](00-machine-learning-basics/README.md) | 模型如何从数据中学习规律？CNN、RNN、Transformer 和大模型之间是什么演进关系？ | 梯度下降、损失函数、前向传播、反向传播、CNN、RNN、Transformer、Q/K/V、预训练 |
| [模型上下文与调用方式](00-llm-basics/context-window-basics.md) | 外部系统调用模型时，模型本轮到底能看到什么？ | 上下文窗口、token 预算、输入组织、长上下文边界 |
| [Prompt 与指令基础](00-llm-basics/prompt-instruction-basics.md) | 调用模型时如何表达任务、角色、边界和输出约束？ | system prompt、instruction、few-shot、结构化输出 |
| [大模型工程实践](01-llm-engineering/README.md) | 如何调用、调参、微调、评测和约束一个大模型？ | 推理参数、微调、模型服务、模型测评、安全边界、回归验证 |
| [Agent 原理与工程实践](04-tools-agents/README.md) | 如何让模型围绕目标调用外部能力并完成任务？ | Prompt、上下文、RAG、记忆、状态、工具调用、MCP、workflow、多 Agent |
| [源码实现](07-source-implementation/README.md) | 如何把这些概念写成可运行、可调试、可扩展的代码？ | 大模型核心组件、Go Agent、MCP Server、Skill、多 Agent 调度 |

## 第一部分：大模型开发

大模型开发可以拆成两个同级部分：原理基础和工程实践。

原理基础需要理解机器学习和深度学习的演进：传统机器学习依赖特征工程和明确任务；CNN 让模型更擅长处理局部空间特征；RNN 让模型可以处理序列状态；Transformer 通过 Q/K/V 和注意力机制提升了长距离关系建模能力，并最终成为现代大模型的核心架构。

工程实践则关注如何把模型变成可用能力：

- 调用方式：API、Prompt、上下文窗口、结构化输出。
- 推理调参：temperature、top_p、max tokens、stop、稳定性和成本。
- 微调方法：什么时候用 Prompt，什么时候用 RAG，什么时候才需要微调。
- 测评方式：能力评测、回归测试、边界样例、LLM-as-judge。
- 安全边界：幻觉、越权、敏感信息、拒答和滥用风险。

大模型开发要知道模型如何被外部系统调用，也要知道调用时可能出现的问题：上下文过长、指令冲突、输出不稳定、事实错误、格式不合规、权限边界不清。否则模型即使单次回答不错，也很难进入稳定系统。

## 第二部分：Agent 开发

Agent 开发不是训练一个模型，而是围绕模型组织任务执行。它要知道自己调用的是什么东西：模型负责理解和生成，RAG 负责补充外部知识，记忆负责跨轮连续性，工具负责访问外部系统，MCP 负责标准化连接能力，状态系统负责记录确定性进度。

更完整地看，Agent 开发是在模型外面搭建一个可执行、可观测、可恢复的任务系统：

```text
业务目标
→ Task / 成功标准
→ Context Builder / 上下文构造
→ Model Decision / 模型决策
→ Tool、Workflow、MCP / 外部执行
→ Observation / 结构化观察
→ State / 状态更新
→ Verifier / 结果验证
→ Trace、Eval、Feedback / 观测和迭代
```

因此 Agent 开发要同时回答两类问题。第一类是“模型要看什么、输出什么、什么时候继续或停止”；第二类是“系统如何控制权限、保存状态、执行工具、记录证据、评估质量和处理失败”。前者是智能交互能力，后者是工程可靠性。缺少后者，Agent 只能停留在演示。

Agent 工程实践更适合按几个核心模块理解：

| 模块 | 解决的问题 | 需要规避的风险 |
| --- | --- | --- |
| [Prompt 与指令工程](01-prompt-instruction/README.md) | 定义目标、边界、输出格式和退出路径 | 指令冲突、格式漂移、任务边界不清 |
| [上下文工程与 RAG](02-context-rag/README.md) | 组织证据、约束、检索结果和用户输入 | 上下文污染、证据不相关、检索为空、引用不支撑结论 |
| [记忆与状态管理](03-memory-state/README.md) | 区分长期记忆、短期上下文和业务状态 | 把状态放进自然语言、敏感信息进入记忆、任务进度不可恢复 |
| [工具调用、MCP 与多 Agent](04-tools-agents/README.md) | 连接外部系统并组织多步骤任务 | 工具接口过大、权限越界、高风险动作无确认、多 Agent 边界不清 |
| [安全、调优与测评](05-evaluation-verification/README.md) | 验证任务过程和最终结果是否可靠 | 只测最终答案、不测工具轨迹、不做攻击样例和回归测试 |

Agent 开发要理解被调用模块的优势和缺陷。模型擅长生成但不负责权限，RAG 能补知识但会检索错，记忆能保持连续但会污染上下文，工具能执行动作但需要审计和确认。Agent 的价值就在于把这些能力组织成可控流程。

## 源码实现

源码实现部分用于把上面的概念落到可运行的小闭环里。它下面包含五条线：从零实现大模型核心组件、从零使用 Go 语言开发一个 Agent、从零实现 MCP、从零实现 Skill，以及多 Agent 交互与调度。

这部分先保持独立演进，后续可以继续补充更多完整项目和案例。

## 行业理解

行业知识先作为单独层保留。不同业务场景对 AI 的要求不一样：有的重效率，有的重安全，有的重合规，有的重资产控制。行业理解决定了 AI 系统的边界该怎么设、数据该怎么组织、风险该怎么评估。

| 行业 | 核心问题 | 细节入口 |
| --- | --- | --- |
| [金融行业理解](08-industry-finance/README.md) | 金融系统如何围绕资金、风险、信用、时间和信任运行？AI 如何在高监管、高风险场景里落地？ | 风控、合规、投研、支付清算、审计、人机协同 |
| [Web3 行业理解](09-industry-web3/README.md) | Web3 如何用链上状态、智能合约、钱包和 token 机制重构资产与协作？AI 如何参与但不越过安全边界？ | 钱包、合约、DeFi、链上数据、安全、治理 |

## 推荐阅读路径

1. 先读 [机器学习与大模型](00-machine-learning-basics/README.md)，建立训练、模型结构和能力来源的底层视角。
2. 再读 [大模型原理与工程边界](00-llm-basics/README.md) 和 [大模型工程实践](01-llm-engineering/README.md)，理解模型本体、调用方式、调优方法和测评边界。
3. 进入 Agent 开发，按 [Prompt 与指令工程](01-prompt-instruction/README.md)、[上下文工程与 RAG](02-context-rag/README.md)、[记忆与状态管理](03-memory-state/README.md)、[工具调用、MCP 与多 Agent](04-tools-agents/README.md) 逐步展开；Skill、记忆、状态、动态上下文组装和 trace 回归已经合并到工具调用与 MCP 小节中。
4. 阅读 [安全、调优与测评](05-evaluation-verification/README.md) 和 [反馈闭环与迭代](06-feedback-iteration/README.md)，理解如何让 AI 系统可回归、可观测、可改进。
5. 最后进入源码实现部分，先看 [大模型核心组件](07-source-implementation/llm-from-zero/README.md) 如何把 token 和 embedding 落成矩阵代码，再分别看 [Go Agent](07-source-implementation/go-agent-from-zero/README.md)、[MCP](07-source-implementation/mcp-from-zero/README.md)、[Skill](07-source-implementation/skill-from-zero/README.md) 和 [多 Agent](07-source-implementation/multi-agent-interaction/README.md) 这些小闭环。
