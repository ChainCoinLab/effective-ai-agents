# 10. 推理机制：模型如何生成答案

[返回本章](README.md)

## 核心问题

模型在服务用户时到底怎么生成输出？

## 推导线索

```text
输入 prompt
→ 先处理完整上下文：prefill
→ 得到下一个 token 的概率分布
→ 按解码策略选出一个 token
→ 把新 token 接回上下文
→ 继续 decode
→ 直到遇到 stop、达到 max_tokens 或任务结束
```

## 本节要讲清楚

- prefill 阶段
- decode 阶段
- autoregressive generation
- KV cache
- streaming 输出
- context window
- 长上下文成本
- TTFT、tokens/s、throughput 和 latency

## 连接到下一节

既然输出来自概率分布，那就可以控制模型怎么选 token。下一节进入 temperature、top_p、top_k 等调参机制。
