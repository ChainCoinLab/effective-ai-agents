# 大模型开发：从原理到工程边界

[返回全局摘要](../README.md)

这一章聚焦大模型本体，但不是孤立讲算法名词。它要从机器学习的最小问题开始，一层一层推导到 token、embedding、Attention、Transformer、训练、推理和评测，最后明确大模型是什么、不是什么、边界在哪里，并为后面的 Agent 工程打基础。

这里的“大模型开发”不是 API 调用实操，而是开发者理解模型能力来源、调用边界和工程分工所需的基础。Prompt、RAG、工具、状态和 Agent 会在后续章节展开；本章只在必要时提前点名，用来说明这些工程模块为什么会出现。

读完本章，你不需要成为训练算法专家，但要能回答四个工程问题：

1. 模型能力从哪里来？
2. 一段文本如何变成模型可计算的 token 和向量？
3. 推理参数、上下文和评测为什么会影响输出可靠性？
4. 哪些职责必须交给 RAG、工具、状态、权限和评测系统？

## 总主线

```text
机器如何学习规律
→ 神经网络如何拟合复杂关系
→ 模型如何训练、优化和泛化
→ 现实对象如何表示成向量
→ 文本如何变成 token 和 embedding
→ 语言模型为什么预测下一个 token
→ 预测压力如何产生语言能力
→ Attention 如何解决上下文关系
→ Transformer 为什么成为大模型核心
→ 预训练、微调、对齐如何塑造能力
→ 推理参数如何影响输出
→ 评测如何判断模型是否可靠
→ 大模型能做什么、不能做什么
→ 为什么后面需要 Agent
```

## 章节框架

可以先按四个阶段理解这 16 节：

| 阶段 | 章节 | 学习任务 |
| --- | --- | --- |
| 地图 | 01 | 先知道大模型路线从哪里来，不要求吃透所有术语 |
| 机器学习基础 | 02-06 | 建立模型、参数、训练、优化、泛化的底层框架 |
| 表示与架构 | 07-12 | 理解现实输入如何变成 token / embedding，以及 Attention / Transformer 如何处理上下文 |
| 训练、推理、评测和边界 | 13-16 | 理解模型能力如何被训练出来，如何被调用、评测和放进工程边界 |

| 章节 | 核心问题 | 主要讲清楚 | 引出下一章 |
| --- | --- | --- | --- |
| [01. 大模型发展历史](01-llm-history.md) | 大模型的发展路线是什么？ | 从机器学习、语言模型、Attention、Transformer、GPT、对齐、长上下文、多模态和 Agent 做总览 | 回到机器学习最小结构 `f(x)=y` |
| [02. 从函数到机器学习](02-function-to-machine-learning.md) | 机器学习到底在学什么？ | 手写规则与学习规则、二维坐标找线、模型、参数、损失、梯度下降 | 简单函数表达能力有限，需要神经网络 |
| [03. 从线性模型到神经网络](03-linear-to-neural-network.md) | 为什么简单函数不够？ | 神经元、权重、偏置、激活函数、隐藏层、非线性、抽象表示 | 有了网络，还要知道它怎么训练 |
| [04. 前向传播、损失函数与反向传播](04-forward-loss-backprop.md) | 模型怎么知道自己错了？ | 前向传播、预测值、真实值、损失函数、反向传播、梯度 | 知道错误后，还要调整参数 |
| [05. 梯度下降与模型训练](05-gradient-descent-training.md) | 参数是怎么被优化的？ | 梯度、学习率、batch、epoch、optimizer、训练循环 | 训练变好不等于真正学会，引出泛化 |
| [06. 拟合、泛化与过拟合](06-fitting-generalization-overfitting.md) | 模型是学规律，还是背答案？ | 拟合、欠拟合、过拟合、泛化、训练集、验证集、测试集、数据泄漏 | 现实输入不是数字，需要向量化 |
| [07. 从现实世界到向量表示](07-real-world-to-vectors.md) | 机器怎么处理文字、图片、声音？ | 特征、向量、维度、表示学习、抽象化、语义空间 | 文本进入模型前要变成 token |
| [08. 从文字到 token 和 embedding](08-token-and-embedding.md) | 一句话如何变成模型能计算的输入？ | tokenizer、token、token id、vocabulary、embedding、语义向量 | 有了 token 后，语言模型开始预测下一个 token |
| [09. 语言模型为什么预测下一个 token](09-next-token-prediction.md) | 语言模型到底在学什么目标？ | next-token prediction、条件概率、logits、softmax、自回归生成 | 预测目标很小，但会施加能力压力 |
| [10. 为什么预测下一个 token 会产生能力](10-capability-from-prediction.md) | 只是续写，为什么会有理解和推理？ | 语法、语义、事实关联、任务格式、in-context learning、规模效应和边界 | 要预测好，就必须理解上下文关系 |
| [11. 从上下文问题到 Attention](11-attention-from-context.md) | 模型怎么在长上下文里找到相关信息？ | RNN/LSTM 瓶颈、Query、Key、Value、attention score、softmax、自注意力、多头注意力 | 多层 Attention 组合成 Transformer |
| [12. Transformer 如何一步步形成](12-transformer-architecture.md) | 为什么现代大模型建立在 Transformer 上？ | token embedding、position embedding、multi-head attention、FFN、残差连接、LayerNorm、decoder-only | 有了结构，还需要大规模训练 |
| [13. 预训练、指令微调与对齐](13-training-and-alignment.md) | 大模型能力从哪里来？为什么会听指令？ | pretraining、cross entropy、optimizer、scaling law、SFT、RLHF、PPO、GRPO、DPO、alignment | 模型训练好后，进入推理阶段 |
| [14. 推理机制与生成参数](14-inference-and-parameters.md) | 模型是怎么生成答案的？为什么输出会变？ | inference、prefill、decode、KV cache、context window、temperature、top_p、top_k、stop、streaming | 输出有概率性，所以必须评测 |
| [15. 模型评测与工程验证](15-evaluation.md) | 怎么判断模型真的变好了？ | golden dataset、人工评估、自动评估、LLM-as-judge、benchmark、回归测试、延迟和成本 | 评测会暴露模型能力边界 |
| [16. 大模型能做什么，不能做什么](16-llm-capabilities-boundaries.md) | 大模型的边界在哪里？ | 它是什么、不是什么；事实、实时性、权限、状态、执行、审计和责任边界；工程分工 | 引出 Agent 工程 |

## 代码实现入口

本章正文先讲概念和边界；如果想把关键概念落到代码，可以从源码实现里的 [从零实现大模型核心组件](../07-source-implementation/llm-from-zero/README.md) 开始。

当前已补充的最小闭环是 [token id 如何查出 embedding 向量矩阵](../07-source-implementation/llm-from-zero/01-token-embedding-matrix.md)：用小词表、小 embedding table 和纯 Python 代码说明 `one_hot_matrix @ embedding_table` 如何得到输入矩阵 `X`。

## 阅读约定

本章会提前出现一些后续工程词，例如 Prompt、RAG、工具调用、MCP、Agent、状态系统和权限系统。第一次遇到时，只需要先理解它们补的是哪类模型边界，不需要立刻掌握实现细节：

| 术语 | 本章先这样理解 | 后面展开位置 |
| --- | --- | --- |
| Prompt | 放进上下文里的任务说明、约束和示例 | Prompt 与指令工程 |
| RAG | 把外部资料检索出来，再放进模型上下文 | 上下文工程与 RAG |
| 工具调用 | 模型提出调用意图，工程系统执行真实动作 | 工具调用与 MCP |
| MCP | 工具和模型之间的标准化连接方式，先理解成让 Agent 统一发现和调用外部能力 | 工具调用与 MCP |
| 状态系统 | 用确定性数据记录任务进度，而不是只靠聊天历史 | 记忆与状态管理 |
| 权限系统 | 由应用层判断身份、资源和动作边界 | 工具调用与 Agent 工程 |
| Agent | 把模型、上下文、工具、状态、权限和评测组织成任务流程 | Agent 原理与工程实践 |

图示的读法也遵循同一个原则：章首图用于建立地图，正文图用于解释当前概念。遇到提前出现的图，不需要一次看完所有细节，只抓住图前导语指定的那一层关系即可。

## 最终落点

读完这一章，读者需要形成一个稳定判断：大模型是一个强大的概率生成组件，能把上下文里的语言、知识、模式和任务要求压缩成下一个 token 的概率分布，再逐 token 生成答案。

```text
大模型是一个基于上下文预测 token 的概率生成模型
它擅长理解、生成、归纳、迁移和提出候选
但事实、权限、状态、执行、验证和恢复必须交给工程系统
```

能力边界在第 16 节集中展开。这里只先记住工程分工：

```text
模型负责理解和生成
RAG 负责补充外部知识
工具负责连接外部系统
状态系统负责记录确定性进度
权限系统负责控制动作边界
评测系统负责验证结果可靠性
Agent 负责把这些能力组织成任务流程
```
