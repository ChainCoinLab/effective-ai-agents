# 12. 校验评估：怎么判断模型真的更好

[返回本章](README.md)

## 核心问题

怎么判断一个模型、prompt 或参数配置是真的更好？

## 推导线索

```text
主观感觉不稳定
→ 需要固定测试集
→ 需要明确指标
→ 每次改动都跑同一批问题
→ 对比准确率、格式成功率、幻觉率、成本和延迟
→ 形成回归测试和上线监控
```

## 本节要讲清楚

- golden dataset
- 人工评估
- 自动评估
- LLM-as-judge
- benchmark
- regression test
- factuality
- hallucination rate
- format success rate
- latency / cost
- A/B test

## 收束

到这里，大模型本体形成一个闭环：

```text
目标
→ 数据
→ 模型结构
→ 训练与对齐
→ 推理
→ 调参
→ 评估
→ 再调整
```
