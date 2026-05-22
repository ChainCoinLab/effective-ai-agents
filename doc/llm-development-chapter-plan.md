# 大模型开发章节计划

这份计划用于指导 `doc/agent-best-practices/00-llm-basics/` 下的大模型开发章节写作。目标不是罗列术语，而是用一条连续推导线讲清楚：机器如何从数据中学习规律，语言如何变成 token，Transformer 为什么成为大模型核心，大模型能做什么、不能做什么，以及为什么后面需要 Agent。

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

| 章节 | 核心问题 | 主要讲清楚 | 引出下一章 |
| --- | --- | --- | --- |
| [01. 大模型发展历史](agent-best-practices/00-llm-basics/01-llm-history.md) | 大模型的发展路线是什么？ | 从机器学习、语言模型、Attention、Transformer、GPT、对齐、长上下文、多模态和 Agent 做总览 | 回到机器学习最小结构 `f(x)=y` |
| [02. 从函数到机器学习](agent-best-practices/00-llm-basics/01-function-to-machine-learning.md) | 机器学习到底在学什么？ | 手写规则与学习规则、二维坐标找线、模型、参数、损失、梯度下降 | 简单函数表达能力有限，需要神经网络 |
| [03. 从线性模型到神经网络](agent-best-practices/00-llm-basics/03-linear-to-neural-network.md) | 为什么简单函数不够？ | 神经元、权重、偏置、激活函数、隐藏层、非线性、抽象表示 | 有了网络，还要知道它怎么训练 |
| [04. 前向传播、损失函数与反向传播](agent-best-practices/00-llm-basics/04-forward-loss-backprop.md) | 模型怎么知道自己错了？ | 前向传播、预测值、真实值、损失函数、反向传播、梯度 | 知道错误后，还要调整参数 |
| [05. 梯度下降与模型训练](agent-best-practices/00-llm-basics/05-gradient-descent-training.md) | 参数是怎么被优化的？ | 梯度、学习率、batch、epoch、optimizer、训练循环 | 训练变好不等于真正学会，引出泛化 |
| [06. 拟合、泛化与过拟合](agent-best-practices/00-llm-basics/06-fitting-generalization-overfitting.md) | 模型是学规律，还是背答案？ | 拟合、欠拟合、过拟合、泛化、训练集、验证集、测试集、数据泄漏 | 现实输入不是数字，需要向量化 |
| [07. 从现实世界到向量表示](agent-best-practices/00-llm-basics/02-real-world-to-vectors.md) | 机器怎么处理文字、图片、声音？ | 特征、向量、维度、表示学习、抽象化、语义空间 | 文本进入模型前要变成 token |
| [08. 从文字到 token 和 embedding](agent-best-practices/00-llm-basics/03-token-and-embedding.md) | 一句话如何变成模型能计算的输入？ | tokenizer、token、token id、vocabulary、embedding、语义向量 | 有了 token 后，语言模型开始预测下一个 token |
| [09. 语言模型为什么预测下一个 token](agent-best-practices/00-llm-basics/04-next-token-prediction.md) | 语言模型到底在学什么目标？ | next-token prediction、条件概率、logits、softmax、自回归生成 | 预测目标很小，但会施加能力压力 |
| [10. 为什么预测下一个 token 会产生能力](agent-best-practices/00-llm-basics/05-capability-from-prediction.md) | 只是续写，为什么会有理解和推理？ | 语法、语义、事实关联、任务格式、in-context learning、规模效应和边界 | 要预测好，就必须理解上下文关系 |
| [11. 从上下文问题到 Attention](agent-best-practices/00-llm-basics/06-attention-from-context.md) | 模型怎么在长上下文里找到相关信息？ | RNN/LSTM 瓶颈、Query、Key、Value、attention score、softmax、自注意力、多头注意力 | 多层 Attention 组合成 Transformer |
| [12. Transformer 如何一步步形成](agent-best-practices/00-llm-basics/07-transformer-architecture.md) | 为什么现代大模型建立在 Transformer 上？ | token embedding、position embedding、multi-head attention、FFN、残差连接、LayerNorm、decoder-only | 有了结构，还需要大规模训练 |
| [13. 预训练、指令微调与对齐](agent-best-practices/00-llm-basics/09-training-and-alignment.md) | 大模型能力从哪里来？为什么会听指令？ | pretraining、cross entropy、optimizer、scaling law、SFT、RLHF、DPO、alignment | 模型训练好后，进入推理阶段 |
| [14. 推理机制与生成参数](agent-best-practices/00-llm-basics/10-inference-and-parameters.md) | 模型是怎么生成答案的？为什么输出会变？ | inference、prefill、decode、KV cache、context window、temperature、top_p、top_k、stop、streaming | 输出有概率性，所以必须评测 |
| [15. 模型评测与工程验证](agent-best-practices/00-llm-basics/12-evaluation.md) | 怎么判断模型真的变好了？ | golden dataset、人工评估、自动评估、LLM-as-judge、benchmark、回归测试、延迟和成本 | 评测会暴露模型能力边界 |
| [16. 大模型能做什么，不能做什么](agent-best-practices/00-llm-basics/16-llm-capabilities-boundaries.md) | 大模型的边界在哪里？ | 它是什么、不是什么；事实、实时性、权限、状态、执行、审计和责任边界；工程分工 | 引出 Agent 工程 |

## 每节固定写法

每一节都按这条教学结构写：

```text
核心问题
→ 普通人的直觉理解
→ 这个直觉为什么不够
→ 新概念在什么问题下出现
→ 关键术语解释
→ 直观例子或图
→ 它解决了什么问题
→ 它又带来了什么新问题
→ 工程意义和常见误区
→ 引出下一节
```

这样读者不会只看到孤立名词，而是能看到知识点之间的前后因果。

## 教学深度标准

每个知识点都要按“普通人能跟上，但工程师也觉得准确”的标准写，不能只给定义。

写作时必须回答这些问题：

- **它从哪里来**：前一个方法遇到了什么问题，为什么需要引入这个概念。
- **它到底是什么**：用一句话给出核心定义，再用例子解释。
- **它怎么工作**：讲清楚最小机制，不堆公式，但保留必要公式。
- **它解决什么**：明确它比前一个方法强在哪里。
- **它解决不了什么**：说明局限，避免读者把它理解成万能答案。
- **它和后面什么有关**：每节结尾要自然引出下一个知识点。
- **它对工程有什么影响**：说明为什么这个原理会影响 Prompt、RAG、微调、推理参数、评测、工具调用或 Agent。

每节的推荐结构：

```text
1. 先用生活化或工程化例子建立直觉
2. 再给术语和必要公式
3. 然后解释机制
4. 接着讲局限
5. 最后落到工程判断
```

写作时避免三类问题：

- 不要把章节写成百科词条。
- 不要只讲“是什么”，不讲“为什么出现”。
- 不要提前展开后面章节的细节，只在当前层级讲到足够理解即可。

## 深度层级

每个核心知识点至少要写到四层，不能只停留在概念名词：

| 层级 | 要回答的问题 | 示例 |
| --- | --- | --- |
| 直觉层 | 普通人怎样先理解它？ | 训练像“猜、错、调、再猜”。 |
| 机制层 | 它内部最小工作机制是什么？ | 损失函数把错误变成数值，梯度告诉参数往哪个方向调。 |
| 形式层 | 必要的公式或结构是什么？ | 线性模型写成 `y = wx + b`，大模型核心任务写成 `P(next_token \| previous_tokens)`。 |
| 工程层 | 它对真实开发有什么影响？ | 因为模型输出是概率分布，所以要做 eval、回归测试和结构化输出校验。 |

每节至少包含：

- 一个连续例子，贯穿本节主要概念。
- 一个必要公式或结构图。
- 一个“容易误解”的提醒。
- 一个“为什么引出下一节”的过渡。

判断一节是否足够深入，看它能不能回答：

```text
如果读者只记住这一节，他能不能解释这个概念为什么存在？
如果读者要做工程，他能不能知道这个概念会影响哪些设计选择？
如果读者遇到反例，他能不能知道这个概念的边界在哪里？
```

## 发展历史的切入方式

`01. 大模型发展历史` 只做总览，不展开训练细节、特征向量细节和多模态实现细节。它先给读者一张路线图：

```text
机器从数据中学习规律
→ 语言可以被建模成序列预测问题
→ 统计语言模型根据短上下文预测下一个词
→ 神经网络语言模型把词变成向量
→ RNN / LSTM 按顺序处理文本
→ Seq2Seq 处理输入序列到输出序列
→ Attention 让模型直接关注相关位置
→ Transformer 用 self-attention 统一建模上下文关系
→ BERT / GPT 形成理解路线和生成路线
→ GPT-3 级别的大模型通过规模获得更强泛化能力
→ Instruction Tuning / RLHF / DPO 让模型更会听指令
→ 长上下文、多模态、工具调用和 Agent 扩展模型使用方式
```

`02. 从函数到机器学习` 重点用二维坐标分类建立机器学习直觉：

- **二维坐标找一条线**：解释模型、参数、误差、损失、梯度下降和训练循环。

`07. 从现实世界到向量表示` 再使用猫图识别，解释手写规则为什么失效，以及特征、向量、表示学习和神经网络抽象。

配图建议：

- `rules-vs-machine-learning.svg`：传统编程和机器学习的规则来源对比。
- `line-classifier-training.svg`：二维坐标里从错误分类线调整到更好边界。
- `training-loop-ring.svg`：猜、错、调、再猜的环形训练循环。
- `cat-feature-vector.svg`：放在 `从现实对象到特征向量`，展示像素、低层特征、高层特征、向量和类别判断。

多模态的 ViT、CLIP、projector、视觉 token 细节不放在发展历史里展开，只在历史总览中点到；后续如果单独写多模态章节，再使用 `multimodal-token-pipeline.svg` 展开。

## 最终落点

整章最后要让读者形成这个判断：

```text
大模型不是数据库
大模型不是权限系统
大模型不是状态机
大模型不是可靠执行器

大模型是一个基于上下文预测 token 的概率生成模型
它擅长理解、生成、归纳、迁移和提出候选
但事实、权限、状态、执行、验证和恢复必须交给工程系统
```

进入 Agent 工程时，顺势引出这个分工：

```text
模型负责理解和生成
RAG 负责补充外部知识
工具负责连接外部系统
状态系统负责记录确定性进度
权限系统负责控制动作边界
评测系统负责验证结果可靠性
Agent 负责把这些能力组织成任务流程
```
