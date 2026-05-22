# Round 2 合并修订记录

## 已处理

- 在 `README.md` 增加 01-16 的阶段速览，把学习路径分成“地图、机器学习基础、表示与架构、训练/推理/评测/边界”四段。
- 在 `SUMMARY.md` 对大模型基础部分增加轻量阶段分组，降低 16 个条目连续铺开的目录压力。
- 在 `README.md` 的阅读约定里补充 MCP 一句话解释，避免读者只知道它和工具有关但不知道先如何理解。
- 在长章节开头增加“第一次读先带走三件事”：
  - `03-token-and-embedding.md`
  - `04-next-token-prediction.md`
  - `05-capability-from-prediction.md`
  - `09-training-and-alignment.md`
  - `10-inference-and-parameters.md`
  - `12-evaluation.md`
- 在 `12-evaluation.md` 开头回扣第 06 节的训练集、验证集、测试集，说明 golden dataset 是大模型应用里的固定测试集，但还要覆盖 prompt、RAG、工具链、成本、延迟和安全边界。
- 在 `16-llm-capabilities-boundaries.md` 给 MCP 图增加阅读范围说明，并补充工程词小抄的学习范围说明。
- 对多图压力做实际减负：`03-token-and-embedding.md`、`04-next-token-prediction.md`、`05-capability-from-prediction.md`、`09-training-and-alignment.md`、`10-inference-and-parameters.md`、`12-evaluation.md`、`16-llm-capabilities-boundaries.md` 的章首只保留最贴近本章的一张图；第 16 节的 MCP 图移动到“为什么需要 Agent”处。

## 暂未处理

- 没有统一重命名 01-16 正式文件；当前仍依赖 README / SUMMARY 的正式顺序说明。
- 没有大幅压缩长章节正文，也没有把“直觉层 / 机制层 / 形式层 / 工程层”全面改成成稿式标题。这个需要单独的结构性编辑轮。
- 没有归档旧稿文件；这会影响维护，但不阻塞当前阅读路径。

## Round 3 复审重点

- 小白学习者重点看：新增“先带走三件事”是否降低首次阅读负担，MCP 和评测回扣是否够清楚。
- 高级编辑重点看：章首多图压力是否实质缓解，新增阶段分组是否改善目录扫描，是否仍有新增表格或提示造成版面负担。
