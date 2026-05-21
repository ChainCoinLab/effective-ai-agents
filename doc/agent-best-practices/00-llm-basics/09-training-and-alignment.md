# 09. 训练与对齐：模型能力从哪里来

[返回本章](README.md)

## 核心问题

大模型为什么能从海量文本里学到能力，又怎么从“会续写”变成“会听话”？

## 推导线索

```text
模型参数初始是随机的
→ 用海量文本预测下一个 token
→ loss 告诉模型预测错在哪里
→ 反向传播和 optimizer 更新参数
→ 预训练让模型获得语言、知识和模式能力
→ 但预训练模型只是在续写
→ SFT 让模型学习指令和回答格式
→ RLHF / DPO 让模型更符合人类偏好
```

## 本节要讲清楚

- pretraining
- cross entropy loss
- 反向传播和 optimizer 的直觉
- 数据质量和 scaling law
- instruction tuning
- SFT
- RLHF
- DPO
- 对齐和能力的区别

## 连接到下一节

模型训练好了，下一步就是运行。运行时模型不是一次性生成整段答案，而是一个 token 一个 token 地推理和采样。
