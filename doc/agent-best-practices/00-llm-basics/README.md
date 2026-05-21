# 大模型本体：由浅入深

[返回全局摘要](../README.md)

这一章只讲大模型本体，暂时不展开 Agent、RAG、工具调用和上层应用。写法采用“从一个最小问题出发，然后一层一层推导”的方式：每一节都解释前一个问题为什么不够、下一个概念为什么会被引入，以及它又会带来什么新问题。

## 总主线

```text
大模型为什么会发展到今天这条路线
→ 我们想让机器学会一个函数
→ 简单函数不够
→ 现实对象要变成向量
→ 文字要变成 token 和 embedding
→ 语言模型变成预测下一个 token
→ 为了理解上下文，引出 Attention
→ 为了大规模训练，引出 Transformer
→ 为了让模型有能力并会听指令，引出预训练、SFT、RLHF / DPO
→ 为了让模型跑起来并可控，引出推理机制、KV Cache 和采样参数
→ 为了判断是否变好，引出评估体系
```

## 章节框架

| 章节 | 核心问题 | 推导重点 |
| --- | --- | --- |
| [01. 大模型发展历史](01-llm-history.md) | 大模型为什么会走到 Transformer 和 GPT 这条路线？ | 从统计语言模型、RNN、Attention 推到 Transformer、GPT、指令微调和对齐。 |
| [02. 从函数到机器学习](01-function-to-machine-learning.md) | 机器学习最开始到底在学什么？ | 从 `f(x)=y` 推到参数、损失函数、梯度下降和训练。 |
| [03. 从现实对象到特征向量](02-real-world-to-vectors.md) | 机器怎么处理图片、声音、文字这些现实对象？ | 从“机器只能算数字”推到特征、向量和表示学习。 |
| [04. 从文字到 token 和 embedding](03-token-and-embedding.md) | 文字怎么变成模型能计算的东西？ | 从编号、one-hot 的不足推到 token、tokenizer 和 embedding。 |
| [05. 语言模型为什么预测下一个 token](04-next-token-prediction.md) | 为什么大模型的核心任务是 next-token prediction？ | 从语言序列推到条件概率、logits、概率分布和自回归生成。 |
| [06. 为什么预测下一个 token 会产生能力](05-capability-from-prediction.md) | 只是续写文本，为什么会出现理解、知识和推理？ | 从预测压力推到语法、事实、任务格式和 in-context learning。 |
| [07. 从上下文问题到 Attention](06-attention-from-context.md) | 模型怎么在长文本里找到相关信息？ | 从 RNN 长距离依赖问题推到 self-attention。 |
| [08. Transformer 如何一步步形成](07-transformer-architecture.md) | 为什么现代大模型基本建立在 Transformer 上？ | 从 attention 推到多头、位置编码、FFN、残差、归一化和 decoder-only。 |
| [09. 训练与对齐：模型能力从哪里来](09-training-and-alignment.md) | 模型怎么获得能力，又怎么从“会续写”变成“会听话”？ | 从预训练推到 SFT、RLHF、DPO、数据质量和 scaling law。 |
| [10. 推理机制与调参](10-inference-and-parameters.md) | 模型怎么生成答案，又如何控制输出？ | 从 prefill、decode、KV cache 推到 temperature、top_p、stop、logprobs。 |
| [11. 校验评估：怎么判断模型真的更好](12-evaluation.md) | 怎么判断模型、prompt 或参数配置是真的提升？ | 从主观体感不足推到 golden dataset、指标、回归测试和线上监控。 |

## 每节写法

每一节固定按这条链路展开：

```text
这一节从什么问题开始
→ 最朴素的办法是什么
→ 它为什么不够
→ 新概念为什么被引入
→ 这个概念解决了什么
→ 它又引出下一个什么问题
```

这样读者不会只看到一个个孤立名词，而是能看到知识点之间的前后因果。
