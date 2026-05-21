# 01. 大模型发展历史

[返回本章](README.md)

## 核心问题

大模型为什么会走到 Transformer 和 GPT 这条路线？

## 推导线索

```text
统计语言模型
→ 神经网络语言模型
→ RNN / LSTM
→ Seq2Seq
→ Attention
→ Transformer
→ BERT / GPT
→ GPT-3 级别的大模型
→ Instruction Tuning
→ RLHF / DPO
→ 长上下文、多模态和推理模型
```

## 本节要讲清楚

- 统计语言模型解决了什么，又为什么不够
- RNN / LSTM 为什么适合序列，又为什么受限
- Attention 为什么改变了序列建模方式
- Transformer 为什么适合大规模训练
- GPT 路线为什么能扩展成通用生成模型
- 指令微调和对齐为什么会出现

## 连接到下一节

看完历史之后，下一步回到最小起点：机器学习最开始到底在学什么。也就是从一个函数开始。
