# Round 1 小白学习者评审：大模型基础 01-16

## 总判断

整体学习路径是顺的：从机器学习最小结构，逐步走到神经网络、训练、泛化、向量化、token、next-token prediction、Attention、Transformer、训练对齐、推理、评测和能力边界，主线有因果关系，不是单纯堆名词。

但对初学者来说，这条路径目前有三个明显卡点：

1. 第 01 节总览和 SUMMARY 导航提前抛出太多后面才解释的工程词，容易让读者误以为一开始就要懂 Attention、Transformer、RAG、Agent、RLHF。
2. 第 06 节到第 07 节、第 08 节到第 09 节、第 12 节到第 13 节之间跨度较大，需要更强的“为什么现在换话题”的过渡。
3. 第 16 节把 RAG、工具、状态、权限、日志、Agent 闭环集中收束得很好，但 SUMMARY 里马上进入 Agent 原理时，缺少一个“从大模型边界到 Agent 工程模块”的桥接导航。

## 严重问题

### 1. 第 01 节总览对初学者信息密度过高

定位：`doc/agent-best-practices/00-llm-basics/01-llm-history.md`，`## 总览路线`、`## 2. 第二阶段：从短上下文到长距离关系` 到 `## 6. 第六阶段：长上下文、多模态、工具和 Agent`

初学者会卡在哪里：刚开始学习时，还没理解“模型、参数、训练、token、上下文”这些基础，就先看到 n-gram、词向量、Attention、Transformer、GPT、SFT、RLHF / DPO、RAG、工具、Agent。读者可能能看懂大方向，但会不知道哪些概念现在只要先记住名字，哪些必须马上理解。

为什么会卡：第 01 节是地图，但它的术语已经接近全章终点。对有经验的人这是总览，对小白则像预告片里塞了太多角色名。尤其是 `RLHF / DPO`、`RAG`、`Agent` 属于后面工程层概念，和第 02 节要回到 `f(x)=y` 的跨度很大。

建议怎么补：在第 01 节开头或总览路线后补一个“本节只需形成的三个印象”：

- 大模型不是一开始就出现的，是从“用数据学习规律”一步步发展来的。
- Attention、Transformer、RLHF、RAG、Agent 现在只需要知道是后续章节会解释的关键词。
- 下一节会暂时放下这些大词，先从最小问题 `输入 x -> 输出 y` 开始。

也可以在每个高阶术语第一次出现时加一句“先不用展开，后面第几节会讲”。

### 2. 第 06 节到第 07 节从“泛化评测”跳到“现实对象向量化”，换题感偏强

定位：`doc/agent-best-practices/00-llm-basics/06-fitting-generalization-overfitting.md`，`## 连接到下一节`；`doc/agent-best-practices/00-llm-basics/02-real-world-to-vectors.md`，`## 1. 为什么必须把现实对象变成数字`

初学者会卡在哪里：第 06 节刚学完训练集、验证集、测试集、过拟合，脑子里还在想“怎么判断模型学没学会”。第 07 节马上进入图片、文字、声音怎么变成向量，读者会问：为什么不继续讲模型评估，突然开始讲输入表示？

为什么会卡：两节之间其实有一个重要逻辑没有被充分说透：泛化好不好，不只取决于训练方法和数据划分，还取决于输入被表示成了什么。如果表示错了，模型连正确规律都看不到。这个桥现在有，但还不够显眼。

建议怎么补：在第 06 节末尾或第 07 节开头补一段过渡：

```text
前面默认 x 已经是数字，比如二维坐标。但真实世界里的 x 往往是文字、图片、声音。模型能否泛化，不只看训练过程，也看输入表示是否保留了真正有用的规律。所以下一步要先解决：现实对象怎样变成模型能学习的向量。
```

这样读者会知道第 07 节不是换主题，而是在补齐 `x` 的来源。

### 3. 第 12 节到第 13 节出现“预训练、对齐、SFT、RLHF、DPO”时，需要先区分“模型结构”和“训练阶段”

定位：`doc/agent-best-practices/00-llm-basics/07-transformer-architecture.md`，`## 通向哪里`；`doc/agent-best-practices/00-llm-basics/09-training-and-alignment.md`，`## 核心问题`、`## 6. instruction tuning 与 SFT`、`## 7. reward model、RLHF 与 DPO`

初学者会卡在哪里：第 12 节讲 Transformer block、position embedding、FFN、残差、LayerNorm、causal mask。第 13 节马上讲预训练、SFT、RLHF、DPO。读者可能分不清：Transformer 是模型本身，预训练是训练它，SFT/RLHF/DPO 是继续改变它，还是只是 Prompt 技巧？

为什么会卡：这里从“房子结构”切到“怎么装修和调教房子”，抽象层级变了。第 13 节内部解释得比较完整，但初学者进入前缺少一张阶段关系图。

建议怎么补：在第 13 节前面补一个极简分层：

```text
Transformer：模型骨架，决定信息怎么流动。
Pretraining：用海量文本把随机参数训练成会续写的模型。
SFT / instruction tuning：用指令-答案样本教它按用户请求回答。
RLHF / DPO：用偏好数据让回答更符合人类偏好和安全要求。
Inference：参数固定后，实际服务用户时逐 token 生成。
```

这样后面讲 SFT、RLHF、DPO 时，读者不会把它们和架构部件混在一起。

### 4. SUMMARY 的 Agent 导航承接不够，读者会不知道“为什么从 16 跳到 Agent 原理”

定位：`doc/agent-best-practices/SUMMARY.md`，`## 一、大模型开发` 到 `## 二、Agent 开发`

初学者会卡在哪里：第 16 节说“大模型不是数据库、权限系统、状态机、可靠执行器”，然后 SUMMARY 直接进入 `Agent 原理`、`Agent 发展历史`、`Prompt 与指令工程`、`上下文工程与 RAG`、`记忆与状态管理`、`工具调用与 MCP`。读者会知道这些看起来相关，但不知道推荐阅读顺序背后的学习任务是什么。

为什么会卡：第 16 节已经把工程分工讲出来了，但 SUMMARY 只是列表，没有把“边界 -> 补位组件 -> Agent 编排”的逻辑写出来。

建议怎么补：在 SUMMARY 的 `## 二、Agent 开发` 下加 2-3 句导航说明：

```text
上一部分说明了大模型只能负责理解、归纳和生成，不能独自承担事实、状态、权限和执行。Agent 开发部分就是学习这些缺口如何由 Prompt、RAG、记忆、状态、工具、MCP、评测和工程流程补齐，并由 Agent 组织成可推进、可验证、可恢复的任务闭环。
```

## 中等问题

### 5. 第 08 节内容很扎实，但 token、embedding、text embedding、上下文化表示容易混在一起

定位：`doc/agent-best-practices/00-llm-basics/03-token-and-embedding.md`，`## embedding：把 token 放进连续向量空间`、`## 向量空间如何表达相似性`、`## 上下文含义：同一个 token 在不同句子里会变`

初学者会卡在哪里：读者会同时看到 token embedding、检索系统里的 text embedding、经过 Transformer 后的上下文化表示。三者都叫 embedding 或向量，很容易误解成“一个词固定对应一个语义向量，RAG 也是直接用这个向量”。

为什么会卡：第 08 节解释了这些差异，但因为内容长，初学者读到后半段可能忘记前面定义。

建议怎么补：在第 08 节中间或小结里加一个对照表：

| 名称 | 它表示什么 | 是否随上下文变化 | 常见用途 |
| --- | --- | --- | --- |
| token id | 词表里的编号 | 不变 | 查 embedding 表 |
| token embedding | 单个 token 的初始向量 | 通常不随句子变化 | 送入 Transformer |
| 上下文化表示 | token 在当前句子里的状态 | 会变 | 预测下一个 token |
| text embedding | 一段文本的检索向量 | 随整段文本变化 | RAG、相似度搜索 |

### 6. 第 09 节到第 10 节的“预测产生能力”需要更明确地区分“训练目标”和“产品能力”

定位：`doc/agent-best-practices/00-llm-basics/04-next-token-prediction.md`，`## 7. 通向哪里：先解释能力来源，再追问上下文关系`；`doc/agent-best-practices/00-llm-basics/05-capability-from-prediction.md`，`## 1. 从哪里来：预测压力不是背答案，而是压缩规律`

初学者会卡在哪里：第 09 节说训练目标是预测下一个 token，第 10 节说这会产生翻译、总结、写代码、推理等能力。读者可能误解成“只要会预测下一个 token，就自然可靠地会所有任务”。

为什么会卡：第 10 节有讲边界和幻觉，但建议在开头先强调“能力来源”和“可靠产品能力”不是一回事。

建议怎么补：第 10 节开头加一句强提醒：

```text
这里说的“产生能力”，指模型在参数里学到可迁移的语言和任务模式；它不等于在具体业务里稳定、可验证、可负责地完成任务。后者还需要 Prompt、RAG、工具、评测和权限系统。
```

### 7. 第 11 节 Attention 引入 RNN/LSTM，对完全小白可能需要一句“为什么要知道旧方法”

定位：`doc/agent-best-practices/00-llm-basics/06-attention-from-context.md`，`## 从哪里来：RNN / LSTM 的上下文瓶颈`

初学者会卡在哪里：读者刚从 next-token prediction 过来，可能会问：我还没学过 RNN/LSTM，为什么突然要学旧架构？

为什么会卡：RNN/LSTM 是为了衬托 Attention 的必要性，但如果不先声明“只作为对比，不要求掌握细节”，读者会以为又多了一组必须深入理解的概念。

建议怎么补：在该节开头加一句：

```text
RNN/LSTM 在这里不是新的学习主线，只是用来说明旧的序列处理方式为什么难以支撑长上下文和大规模并行训练。
```

### 8. 第 14 节推理参数很好用，但和第 09 节采样内容有重复感，需要说明“这里是工程化展开”

定位：`doc/agent-best-practices/00-llm-basics/04-next-token-prediction.md`，`## 4. 采样与确定性的边界`；`doc/agent-best-practices/00-llm-basics/10-inference-and-parameters.md`，`## 8. 从 logits 到采样` 到 `## 15. 参数如何按任务选择`

初学者会卡在哪里：第 09 节已经看到 temperature、采样、确定性，第 14 节又看到 temperature、top_p、top_k、stop、seed、logprobs。读者可能觉得重复，或不知道两节侧重点有什么不同。

为什么会卡：第 09 节是在解释“语言模型为什么按概率生成”，第 14 节是在解释“上线时如何控制生成行为和成本”。这个差异值得明说。

建议怎么补：第 14 节开头加一个回扣：

```text
第 09 节讲采样，是为了理解 next-token prediction 的基本机制；本节重新讲采样，是为了把它放进真实推理服务里，理解延迟、成本、上下文、KV cache 和参数选择。
```

## 轻微问题

### 9. README 和 SUMMARY 的展示编号清楚，但文件名编号不连续，可能让初学者找文件时困惑

定位：`doc/agent-best-practices/00-llm-basics/README.md`，`## 章节框架`；`doc/agent-best-practices/SUMMARY.md`，`## 一、大模型开发`

初学者会卡在哪里：目录展示是 01-16，但文件名里有 `01-function-to-machine-learning.md`、`02-real-world-to-vectors.md`、`03-token-and-embedding.md`、`04-next-token-prediction.md` 等复用旧编号。读者如果在文件系统里找“第 07 节”，会发现文件叫 `02-real-world-to-vectors.md`。

为什么会卡：阅读网页时不明显，但本仓库学习者可能直接在编辑器里打开文件。

建议怎么补：不一定要改文件名。可以在 README 的章节框架后加一句：

```text
说明：表格中的章节序号是推荐阅读顺序，部分文件名保留了早期编号，以表格和 SUMMARY 的顺序为准。
```

### 10. 工程词提前出现较多，建议统一加“后面会讲”的小标记

定位：`doc/agent-best-practices/00-llm-basics/02-real-world-to-vectors.md`，`## 4. 表示学习：让模型自己学特征`、`## 6. 工程意义：表示决定模型能看到什么`；`doc/agent-best-practices/00-llm-basics/03-token-and-embedding.md` 多处 RAG、Agent；`doc/agent-best-practices/00-llm-basics/04-next-token-prediction.md` 多处 RAG、Agent

初学者会卡在哪里：RAG、Agent、工具调用、Prompt 工程在基础章节中多次提前出现。虽然这些工程关联有价值，但小白可能会停下来查这些词，打断主线。

为什么会卡：基础章既想讲原理，又想连接工程意义。对初学者，工程词如果没有“先知道用途即可”的提示，会变成额外负担。

建议怎么补：第一次出现 RAG、Agent、工具调用时加短括号：

```text
RAG（后面会讲，先理解成“把外部资料检索出来放进上下文”）
Agent（后面会讲，先理解成“把模型、工具、状态和评测组织成任务流程”）
```

## 下一轮复审重点

1. 重点复查第 01 节是否降低了总览门槛：读者是否知道哪些词现在只需有印象。
2. 重点复查第 06 -> 07、第 12 -> 13、第 16 -> Agent 导航三处过渡是否补强。
3. 重点复查第 08 节是否清楚区分 token embedding、上下文化表示和 text embedding。
4. 重点复查 SUMMARY 是否从“大模型边界”自然导向 Prompt、RAG、记忆、状态、工具、MCP 和 Agent。
5. 让一个完全没学过机器学习的读者只读 README + SUMMARY，检查他能否说出：为什么要按 01-16 顺序学，以及每节是在解决前一节留下的什么问题。
