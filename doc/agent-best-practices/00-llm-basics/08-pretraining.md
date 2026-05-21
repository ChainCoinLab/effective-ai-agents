# 08. 预训练：模型能力从哪里来

[返回本章](README.md)

## 核心问题

大模型为什么能从海量文本里学到能力？

## 推导线索

```text
模型参数初始是随机的
→ 输入大量文本
→ 预测下一个 token
→ 用 cross entropy 计算预测分布和真实 token 的差距
→ 反向传播计算参数该怎么改
→ optimizer 持续更新参数
→ 重复处理海量 token
→ 模型逐渐学到语言、知识和任务模式
```

## 本节要讲清楚

- pretraining 是什么
- cross entropy loss 的直觉
- 反向传播的直觉
- optimizer、batch size、learning rate 的作用
- scaling law 为什么重要
- 数据质量为什么关键

## 连接到下一节

预训练模型会续写，但不一定会按用户指令完成任务。接下来要讲：模型如何从续写模型变成指令模型。
