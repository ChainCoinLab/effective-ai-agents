# Round 1 合并修订记录

## 已处理

- 修正 `01-function-to-machine-learning.md` 末尾“连接到下一节”的顺序错误，改为先引出神经网络，再回到现实对象向量化。
- 在 `01-llm-history.md` 增加初学者阅读提示，说明总览里的 RNN、Attention、Transformer、RLHF、DPO、RAG、Agent 只需先建立印象。
- 在 `README.md` 增加正式阅读顺序说明、后续工程术语先导表和图示阅读约定。
- 在 `SUMMARY.md` 增加 `00-llm-basics/README.md` 本章导读入口，并补上从大模型边界到 Agent 工程的承接说明。
- 在 `02-real-world-to-vectors.md` 补充“图片像素是数字，但不等于模型已理解图片”的提醒。
- 在 `03-token-and-embedding.md` 增加 token id、token embedding、上下文化表示、text embedding 对照表。
- 在 `04-forward-loss-backprop.md` 增加一个参数变化如何影响 loss 的直觉例子。
- 在 `05-gradient-descent-training.md` 增加初学者先掌握 learning rate、batch、epoch、optimizer 的提示。
- 在 `06-fitting-generalization-overfitting.md` 增加垃圾邮件场景下 accuracy、precision、recall 的最小例子。
- 在 `04-next-token-prediction.md` 补充 logits 到 softmax 概率的趋势解释。
- 在 `05-capability-from-prediction.md` 明确“能力来源”不等于“稳定产品能力”，并补充“涌现能力”的门槛式理解。
- 在 `06-attention-from-context.md` 补充 RNN/LSTM 只是对比材料的提示，并增加 3-token Q/K/V 权重例子。
- 在 `07-transformer-architecture.md` 增加核心组件优先级和高级变体“了解即可”的提示。
- 在 `09-training-and-alignment.md` 增加 Transformer、Pretraining、SFT、RLHF/DPO、Inference 的层级对照，并补充偏好优化小例子。
- 在 `10-inference-and-parameters.md` 补充第 09 节采样机制与本节工程化推理的差异，并增加 TTFT、tokens/s、latency 的时间线例子。
- 在 `12-evaluation.md` 增加最小 golden dataset 示例。
- 在 `16-llm-capabilities-boundaries.md` 增加工程词小抄，并用报销任务串起模型、RAG、工具、状态、权限、评测和 Agent 的分工。

## 暂未处理

- 没有批量移动每章章首多图到正文对应位置；本轮先通过 README 图示阅读约定和关键章节补充说明降低理解压力。
- 没有统一重命名正式 01-16 文件；本轮先在 README 和 SUMMARY 明确正式阅读顺序，避免破坏现有链接。
- 没有压缩 08、09、10、13、14、15 等长章节；这需要单独做结构性编辑，避免一次修改过大。

## Round 2 复审重点

- 小白学习者重点复查：顺序断层是否已消除，新增例子是否足够支撑下一节。
- 高级编辑重点复查：README / SUMMARY 的入口和说明是否清晰，新增表格是否增加负担，图文问题是否仍是阻塞。
