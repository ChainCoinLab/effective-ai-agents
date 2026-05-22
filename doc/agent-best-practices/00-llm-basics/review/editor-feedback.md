# 00-llm-basics 编辑审查报告

## 整体编辑判断

16 节主线总体成立：从大模型历史总览进入机器学习最小闭环，再到神经网络、训练与泛化、现实对象向量化、token / embedding、next-token prediction、能力来源、Attention、Transformer、训练对齐、推理、评测，最后收束到模型边界和 Agent 工程分工。读者能看到“大模型为什么是概率生成组件，而不是万能后端”的连续论证。

主要问题不在单节是否讲清楚，而在编辑层面的节奏和一致性：开头图像过度集中，文件编号与章节编号混乱，部分承接语和总框架不一致，后半部分表格密度偏高，若干概念在第 8、10、13、14、16 节反复展开，导致阅读成本明显上升。建议本轮优先修导航、承接、图片布局和长章节压缩，再进入局部润色。

本次审查统计到 22 条问题：P0 3 条，P1 12 条，P2 7 条。

## P0 必须修

### P0-1

- 章节名：全章
- 位置/小标题：目录文件、README 章节框架、文件命名
- 编辑问题：README 中主线是 01-16，但实际文件名存在多处错位，例如第 02 节文件是 `01-function-to-machine-learning.md`，第 07 节文件是 `02-real-world-to-vectors.md`，第 15 节文件是 `12-evaluation.md`；目录中还残留 `08-pretraining.md`、`09-instruction-tuning-alignment.md`、`10-inference-mechanism.md`、`11-decoding-parameters.md` 等未进入 16 节主线的旧稿。读者按文件名排序会得到错误顺序。
- 修改建议：建立唯一 canonical 章节集，文件名改成 `01-...` 到 `16-...` 的连续编号；旧稿移入 archive 或在 README 标注“旧稿，不在本章主线”；所有章节和返回链接统一指向 canonical 文件。

### P0-2

- 章节名：02. 从函数到机器学习
- 位置/小标题：`连接到下一节`
- 编辑问题：结尾写“接下来要讲：现实对象如何变成特征向量”，实际 README 和章节顺序的下一节是“从线性模型到神经网络”。这个承接会直接打断 02 -> 03 -> 04 -> 05 -> 06 的机器学习基础链条。
- 修改建议：把第 02 节结尾改为引出“简单函数表达能力有限，需要多层非线性模型”，再进入第 03 节神经网络；“现实对象如何向量化”应放在第 06 节结尾引出第 07 节。

### P0-3

- 章节名：全章
- 位置/小标题：每节标题后 1-20 行
- 编辑问题：除第 02 节外，15 个章节都在开头 20 行集中放了 4 张图；第 02 节也在开头放了 2 张图，后文再放 2 张。读者在进入核心问题前先看到一组图墙，尤其在移动端会打断阅读。64 张主线图片中，多张图重复出现 3-5 次，容易形成“堆图”而不是“图解”。
- 修改建议：每节开头只保留 1 张核心图和 1 句导读；其余 3 张按内容插入到对应小节，或移到节末“相关图解”。图片必须服务当下段落，不作为固定模板铺在开头。

## P1 明显建议修

### P1-1

- 章节名：01. 大模型发展历史
- 位置/小标题：`总览路线`
- 编辑问题：开头连续给出路线代码块、问题代码块、三张大表，再进入六个历史阶段。总览信息完整，但前 80 行概念密度过高，读者尚未进入叙事就被多个框架同时要求记忆。
- 修改建议：保留一张“阶段接力表”作为核心总览；工程视角表和三层拆解表择一保留，另一张移到节末作为复盘。每张表前加一句明确导读：读者应该用它解决什么阅读问题。

### P1-2

- 章节名：08. 从文字到 token 和 embedding
- 位置/小标题：全节，尤其 `最朴素的办法` 到 `token 对上下文窗口、成本和截断的影响`
- 编辑问题：本节 663 行，是全章最长之一。token id 不表示语义、embedding 不是事实库、向量相似不等于正确等判断多次重复，削弱了“从文字到可计算输入”的主线推进。
- 修改建议：压缩为“tokenizer 解决切分，token id 解决索引，embedding 解决连续表示，上下文化表示解决歧义，token 预算影响工程”五段；one-hot 只保留过渡价值，不展开成独立长段。

### P1-3

- 章节名：09. 语言模型为什么预测下一个 token
- 位置/小标题：`采样与确定性的边界`
- 编辑问题：第 09 节已经较完整地讲了 temperature、top_k、top_p、贪心解码和任务选择，这与第 14 节“推理机制与生成参数”高度重叠。
- 修改建议：第 09 节只保留“输出是概率分布，因此生成不是数据库查询”的机制层解释；具体参数、推荐范围和故障诊断全部交给第 14 节。

### P1-4

- 章节名：10. 为什么预测下一个 token 会产生能力
- 位置/小标题：`幻觉和边界`、`工程决策小结`
- 编辑问题：本节 664 行，能力来源、幻觉边界、Prompt / RAG / schema / 评测补法都展开较多，和第 16 节能力边界形成重复。
- 修改建议：本节聚焦“预测压力如何逼出语法、事实关联、任务格式、in-context learning 和规模泛化”；边界只保留必要提示，系统分工、权限、状态、Agent 风险留到第 16 节。

### P1-5

- 章节名：11. 从上下文问题到 Attention
- 位置/小标题：全节结构
- 编辑问题：本节没有 `推导线索`、`本节要讲清楚`、`连接到下一节` 等与前后章节一致的导航模块，结尾使用 `通向哪里`。内容本身清楚，但章节节奏与第 08-10、12-15 节不一致。
- 修改建议：补齐统一导航：核心问题后增加推导线索，结尾统一改为“连接到下一节”。保留“从 RNN / LSTM 瓶颈到 Q/K/V”的强主线。

### P1-6

- 章节名：12. Transformer 如何一步步形成
- 位置/小标题：`Transformer block 的整体图景`、`Token embedding`
- 编辑问题：组件表很有用，但 token embedding、self-attention、causal mask 等内容与第 08、09、11 节重复较多。章节任务应是“把已学部件组装成可扩展结构”，而不是重新讲每个部件。
- 修改建议：每个部件先用一句“前文已讲过的作用”，再补“放进 Transformer block 后的新职责”。重点突出组件组合关系、训练可扩展性和 decoder-only 生成约束。

### P1-7

- 章节名：13. 预训练、指令微调与对齐
- 位置/小标题：`3. 训练闭环：数据如何推动参数变化`
- 编辑问题：tokenizer、batch、forward pass、cross entropy、backpropagation、optimizer 的解释与第 04、05、08、09 节重复。对第 13 节来说，这段过长，延迟了“预训练 -> SFT -> RLHF / DPO -> alignment”的核心。
- 修改建议：将训练闭环改为 LLM 特化复盘：数据清洗与配比、shifted tokens、全词表交叉熵、长序列训练、checkpoint。基础术语只用一句回指前文。

### P1-8

- 章节名：14. 推理机制与生成参数
- 位置/小标题：全节
- 编辑问题：本节有 17 个二级小标题，既讲 prefill / decode / KV cache，又讲 temperature / top_p / stop / seed / logprobs，还包含多张排查表。信息实用，但节奏接近参考手册，教学推进感变弱。
- 修改建议：分成三段导读：推理流程、性能成本、生成控制。参数表只保留一张总表，故障诊断表可移到节末“排查清单”。

### P1-9

- 章节名：15. 模型评测与工程验证
- 位置/小标题：`LLM-as-judge` 到 `Regression test`
- 编辑问题：评测方式表、指标表、上线门禁表连续出现，表格承载了大量判断。读者容易把本节当成清单集合，而不是理解“为什么评测暴露边界”的闭环。
- 修改建议：先用一张流程图式文字链路串起离线评测、回归、灰度、监控、样本回流，再保留指标表和门禁表；评测方式表可压缩为段落或节末对照。

### P1-10

- 章节名：16. 大模型能做什么，不能做什么
- 位置/小标题：`大模型不是什么` 到 `为什么需要 Agent`
- 编辑问题：本节表格线数达到 81 行，是全章最高。边界表、分工表、控制点表、Agent 环节表、闭环风险表、最小判断框架表连续出现，判断很完整但阅读上像架构检查表堆叠。
- 修改建议：保留两张关键表：一张“模型不是什么/应由谁承担”，一张“最小判断框架”。工程分工和 Agent 风险改成分组段落，或放到后续 Agent 章节作为展开。

### P1-11

- 章节名：全章
- 位置/小标题：章节模板与结尾命名
- 编辑问题：同类模块命名不统一：`容易误解的地方`、`常见误区`、`常见误解` 混用；`通向哪里`、`连接到下一节` 混用；`本节小结`、`工程决策小结`、`工程落点` 混用。读者会失去稳定预期。
- 修改建议：统一模板为：`核心问题`、`推导线索`、主体、`常见误区`、`工程小结`、`连接到下一节`。若某节需要变体，应有明确理由。

### P1-12

- 章节名：全章
- 位置/小标题：图片复用
- 编辑问题：`training-alignment-pipeline.svg` 和 `next-token-loop.svg` 各出现 5 次，`transformer-block-stack.svg`、`gradient-descent-landscape.svg`、`forward-backprop-flow.svg`、`context-assembly-pipeline.svg` 各出现 4 次。重复图没有总是带来新解释，容易让读者误以为章节内容重复。
- 修改建议：同一张图第一次完整解释，后续只在需要回指时以内联小图或文字链接出现；复用时必须给出“这次看图关注哪个局部”的导读。

## P2 润色项

### P2-1

- 章节名：01. 大模型发展历史
- 位置/小标题：标题与 `总览路线`
- 编辑问题：标题叫“发展历史”，但正文更像技术路线总览，基本没有年份、关键论文或产品节点。标题和内容预期略有偏差。
- 修改建议：二选一：要么改成“发展路线总览”，要么补少量年份锚点，例如 n-gram、RNN/LSTM、Attention、Transformer、GPT、RLHF、Agent 的代表节点。

### P2-2

- 章节名：02. 从函数到机器学习
- 位置/小标题：图解导读
- 编辑问题：开头写“这一节已经用规则对比、二维分类线和训练循环解释机器学习”，读者刚进入本节时还没有读到这些内容，语气像事后总结。
- 修改建议：改成“本节将用规则对比、二维分类线和训练循环解释机器学习”，或放到节末作为图解回顾。

### P2-3

- 章节名：04. 前向传播、损失函数与反向传播；05. 梯度下降与模型训练
- 位置/小标题：`机制层`、`工程层`
- 编辑问题：`真实答案`、`标签`、`y`、`target` 的关系没有形成统一说法；`loss`、`损失`、`损失函数` 也在不同语境中交替出现。
- 修改建议：建立小型术语约定：第一次出现用“中文名（英文名，常见符号）”，之后固定用中文名或固定英文名，不在同一节内随意切换。

### P2-4

- 章节名：全章
- 位置/小标题：术语大小写
- 编辑问题：Prompt / prompt、Attention / attention、Self-attention / self-attention、Context window / context window、next-token prediction / 预测下一个 token 混用。技术读者能理解，但教学材料需要更稳定。
- 修改建议：制定术语表：章节标题中保留规范英文大小写，正文第一次出现给中英对照，后续优先用中文，必要英文保持同一写法。

### P2-5

- 章节名：13. 预训练、指令微调与对齐
- 位置/小标题：`7.2 RLHF：用奖励模型继续优化助手`
- 编辑问题：`reward hacking（奖励黑客）` 这个译法不够自然，容易被理解成某类人而不是训练中的目标投机现象。
- 修改建议：改为“reward hacking（奖励劫持/奖励投机）”，并用一句话说明“模型优化了奖励分数，但偏离真实质量目标”。

### P2-6

- 章节名：16. 大模型能做什么，不能做什么
- 位置/小标题：返回链接
- 编辑问题：第 16 节开头和结尾各有一个 `[返回本章](README.md)`，其他主线章节只有开头一个。虽然不影响理解，但导航形式不一致。
- 修改建议：统一返回链接策略：要么每节都首尾都有，要么每节都只在开头保留一个。

### P2-7

- 章节名：README
- 位置/小标题：`最终落点`、`能力边界`
- 编辑问题：README 的最终判断已经较完整地写了“大模型不是数据库/权限系统/状态机/执行器”，第 16 节又大篇幅展开相同判断。作为目录页，README 的结论可以更短，把解释空间留给正文。
- 修改建议：README 保留一段高度浓缩结论和章节地图；完整分工和边界表放在第 16 节，避免目录页提前消耗正文高潮。

## 图文混排建议

总原则：每节开头保留一张“核心图”，用于建立本节问题；辅助图放到第一次需要它的小标题下。不要让四张图在标题后连续出现。每张复用图都要说明“这次看图关注什么”。

| 章节 | 开头核心图 | 正文中按需插入的辅助图 |
| --- | --- | --- |
| 01. 大模型发展历史 | `model-evolution.svg` | `rules-vs-machine-learning.svg` 放“从规则到学习”；`cnn-rnn-transformer-comparison.svg` 放“从短上下文到长距离关系”；`training-alignment-pipeline.svg` 放“从会续写到会按指令协作”。 |
| 02. 从函数到机器学习 | `rules-vs-machine-learning.svg` | `line-classifier-training.svg` 放“二维坐标里的第一条线”；`training-loop-ring.svg` 放“训练循环”；`cat-feature-vector.svg` 移到第 07 节或只在本节末作为“为什么规则会失效”的预告。 |
| 03. 从线性模型到神经网络 | `neural-network-depth.svg` | `line-classifier-training.svg` 放“线性模型的边界”；`cat-feature-vector.svg` 放“逐层抽象”；`forward-backprop-flow.svg` 放结尾，作为下一节预告。 |
| 04. 前向传播、损失函数与反向传播 | `forward-backprop-flow.svg` | `training-loop-ring.svg` 放开头复盘；`gradient-descent-landscape.svg` 放结尾引出优化器；`training-alignment-pipeline.svg` 移到第 13 节。 |
| 05. 梯度下降与模型训练 | `gradient-descent-landscape.svg` | `training-loop-ring.svg` 放“机制层”；`forward-backprop-flow.svg` 只作一句回指；`overfitting-generalization.svg` 放结尾引出第 06 节。 |
| 06. 拟合、泛化与过拟合 | `overfitting-generalization.svg` | `line-classifier-training.svg` 放“欠拟合/过拟合”例子；`llm-evaluation-loop.svg` 放“工程层：如何做可靠评测”；`gradient-descent-landscape.svg` 可删除或只作前文链接。 |
| 07. 从现实世界到向量表示 | `cat-feature-vector.svg` | `token-embedding-pipeline.svg` 放“为什么文字比图片更麻烦”；`multimodal-token-pipeline.svg` 放表示学习或多模态补充；`rules-vs-machine-learning.svg` 可删除，避免回到第 02 节。 |
| 08. 从文字到 token 和 embedding | `token-embedding-pipeline.svg` | `next-token-loop.svg` 放“回到主线”；`transformer-block-stack.svg` 移到第 12 节；`context-assembly-pipeline.svg` 移到第 14 或 16 节。 |
| 09. 语言模型为什么预测下一个 token | `next-token-loop.svg` | `token-embedding-pipeline.svg` 只在开头一句回指，不必放图；`prediction-capability-stack.svg` 放结尾引出第 10 节；`inference-prefill-decode.svg` 移到第 14 节。 |
| 10. 为什么预测下一个 token 会产生能力 | `prediction-capability-stack.svg` | `next-token-loop.svg` 放第一节复盘；`llm-capability-boundary.svg` 放“幻觉和边界”；`training-alignment-pipeline.svg` 移到第 13 节。 |
| 11. 从上下文问题到 Attention | `qkv-apple-example.svg` | `cnn-rnn-transformer-comparison.svg` 放“RNN / LSTM 的上下文瓶颈”；`transformer-block-stack.svg` 放结尾引出第 12 节；`context-assembly-pipeline.svg` 移到工程影响小节或后续章节。 |
| 12. Transformer 如何一步步形成 | `transformer-block-stack.svg` | `qkv-apple-example.svg` 放 self-attention 小节；`next-token-loop.svg` 放 decoder-only 小节；`cnn-rnn-transformer-comparison.svg` 只在“为什么支撑大规模训练”处短引用。 |
| 13. 预训练、指令微调与对齐 | `training-alignment-pipeline.svg` | `forward-backprop-flow.svg` 和 `gradient-descent-landscape.svg` 合并为训练闭环回顾，不要分散到开头；`llm-evaluation-loop.svg` 放“为什么必须保留评测集”。 |
| 14. 推理机制与生成参数 | `inference-prefill-decode.svg` | `next-token-loop.svg` 放 decode 小节；`context-assembly-pipeline.svg` 放 context window 小节；`transformer-block-stack.svg` 只保留文字回指或移除。 |
| 15. 模型评测与工程验证 | `llm-evaluation-loop.svg` | `inference-prefill-decode.svg` 放 latency / cost；`llm-capability-boundary.svg` 放收束；`training-alignment-pipeline.svg` 移除或放第 13 节回指。 |
| 16. 大模型能做什么，不能做什么 | `llm-agent-foundation.svg` | `llm-capability-boundary.svg` 放“先给结论”；`context-assembly-pipeline.svg` 放“上下文边界”；`mcp-tool-calling-tunnel.svg` 放“为什么需要 Agent”或后续工具章节，不放开头。 |

## 建议本轮优先执行的修订清单

1. 先修 P0：统一 16 节文件编号和 README 主线；修正第 02 节结尾承接；把每节开头 4 图改为“1 张核心图 + 正文插图”。
2. 压缩第 08、10、13 节，重点删减重复解释，把每节控制在更接近 250-400 行的教学节奏。
3. 调整第 14、15、16 节表格密度，只保留真正承担决策作用的表格，其余改为段落或节末清单。
4. 统一章节模板：核心问题、推导线索、主体、常见误区、工程小结、连接到下一节。
5. 制作术语表，统一 Prompt、Attention、Self-attention、Context window、next-token prediction、SFT、RLHF、DPO 等写法。
6. 给复用图片增加“本次看图重点”，避免同一图在多节中承担相同解释。
7. 让 README 更像导航页，减少提前展开第 16 节边界结论。
8. 最后一轮再做语气润色：删掉“已经”“不是万能”等重复句式，把章节之间的过渡写得更短、更准。
