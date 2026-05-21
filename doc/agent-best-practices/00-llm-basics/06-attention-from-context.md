# 06. 从上下文问题到 Attention

[返回本章](README.md)

## 核心问题

模型怎么在一长串文字里找到相关信息？

## 推导线索

```text
RNN 按顺序读文本
→ 长距离信息容易衰减
→ 串行结构也不利于大规模并行训练
→ 需要让每个 token 直接参考其他 token
→ Attention 通过相关性分数决定该看谁
→ Self-attention 让同一段文本内部的 token 互相建立关系
```

## 本节要讲清楚

- RNN / LSTM 的瓶颈
- query、key、value 的直觉
- attention score 是什么
- self-attention 是什么
- 为什么 attention 适合语言建模

## 连接到下一节

Attention 解决了 token 之间互相参考的问题，但一个 attention 模块还不够。接下来要讲多头、位置、前馈网络、残差和归一化如何组合成 Transformer。
