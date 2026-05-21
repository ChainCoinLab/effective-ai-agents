# 10. 推理机制与调参

[返回本章](README.md)

## 核心问题

模型服务用户时怎么生成答案，又为什么同一个 prompt 可能得到不同输出？

## 推导线索

```text
输入 prompt
→ prefill 处理完整上下文
→ 得到下一个 token 的概率分布
→ decode 阶段一个 token 一个 token 生成
→ KV cache 复用历史计算
→ 采样参数决定如何从概率分布里选 token
→ 参数变化会影响稳定性、创造性、成本和延迟
```

## 本节要讲清楚

- prefill
- decode
- autoregressive generation
- KV cache
- context window
- streaming
- TTFT、tokens/s、latency
- temperature
- top_p / top_k
- max_tokens / stop
- repetition penalty
- logprobs

## 连接到下一节

调参后不能只靠感觉判断好坏。下一节要讲怎么用固定测试集和指标验证模型是否真的变好。
