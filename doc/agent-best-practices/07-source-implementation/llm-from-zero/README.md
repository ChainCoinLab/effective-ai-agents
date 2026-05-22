# 从零实现大模型核心组件

[返回源码实现](../README.md)

这条教程线不训练生产级大模型，也不封装 API。它用小矩阵、小词表和可运行代码，把大模型里最容易抽象化的核心计算拆开看：token 如何变成向量矩阵、Attention 如何做加权求和、输出层如何把隐藏状态变成下一个 token 的概率。

目标是让读者能把正文里的概念和代码里的张量形状对上，而不是只记住术语。

## 教程目录

| 章节 | 本节目标 | 对应正文 |
| --- | --- | --- |
| [01. token id 如何查出 embedding 向量矩阵](01-token-embedding-matrix.md) | 用纯 Python 还原 token id、one-hot、embedding table 和输入矩阵 `X` | [08. 从文字到 token 和 embedding](../../00-llm-basics/08-token-and-embedding.md) |

## 学习顺序

1. 先看第 01 节，把 `token -> token id -> embedding matrix` 跑通。
2. 回到大模型基础第 08 节，理解 token id 只是索引，embedding 才是可训练向量。
3. 继续学习 Attention 和 Transformer 时，再把输入矩阵 `X` 接到后续 Q/K/V、softmax 和前馈网络。

## 本教程线的约束

- 每节只实现一个核心计算，不提前塞完整框架。
- 优先使用标准库，避免把学习重点转移到依赖安装。
- 每段代码都要能看到输入、矩阵形状、输出和它对应的数学式。
- 示例数值只用于解释结构，不代表真实模型已经训练好的参数。

