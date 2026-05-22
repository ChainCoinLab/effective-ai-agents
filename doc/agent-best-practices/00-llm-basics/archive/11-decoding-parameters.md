# 11. 调参：如何控制模型输出

[返回本章](README.md)

## 核心问题

为什么同一个 prompt，每次输出可能不同？

## 推导线索

```text
模型输出的是概率分布
→ 可以永远选概率最高的 token
→ 也可以在候选 token 中采样
→ 随机性、候选范围和惩罚规则不同，输出就不同
→ 解码参数就是控制采样行为和输出边界
```

## 本节要讲清楚

- temperature
- top_p
- top_k
- max_tokens
- stop
- repetition penalty
- frequency penalty / presence penalty
- seed
- logprobs
- 不同任务的参数选择

## 连接到下一节

调参后感觉变好了不够。必须验证模型、prompt 或参数配置是不是真的变好了。
