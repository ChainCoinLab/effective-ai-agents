# 07. Transformer 如何一步步形成

[返回本章](README.md)

## 核心问题

为什么现代大模型基本建立在 Transformer 上？

## 推导线索

```text
token 需要向量表示
→ token 还需要知道自己在序列中的位置
→ token 之间需要通过 attention 建立关系
→ 单一注意力视角不够，所以引入 multi-head attention
→ 仅线性组合不够，所以加入 FFN
→ 网络变深后训练困难，所以加入 residual connection 和 normalization
→ 生成任务需要只能看过去，所以使用 causal mask
→ decoder-only 架构适合自回归生成
```

## 本节要讲清楚

- position encoding / RoPE
- multi-head attention
- FFN
- residual connection
- layer norm / RMSNorm
- causal mask
- decoder-only 架构

## 连接到下一节

结构有了，但参数一开始是随机的。接下来要问：这么大的模型是怎么从海量数据中训练出来的？
