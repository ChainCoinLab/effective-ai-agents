# 大模型基础 01-16 高级编辑评审（Round 1）

## 总判断

作为教材章节，这组内容的主线是成立的：从机器学习最小问题逐步推到 token、embedding、Attention、Transformer、训练、推理、评测和能力边界，整体具备连续学习路径。多数章节也能稳定回到“模型只是概率生成组件，工程系统负责事实、权限、状态、执行和验证”这个落点。

编辑层面目前有中高优先级阻塞，主要不是知识是否覆盖，而是教材阅读体验：图集中堆在章首、长章节信息密度失衡、标题层级模板化、导航编号与文件名不一致，会让读者在连续阅读时出现“先被材料压住，再自己找主线”的感觉。建议先做一次结构性编辑，再进入事实校对或初学者卡点修订。

## 严重程度 P1：影响章节级可读性和导航一致性

### 1. 多数章节把图集中放在开头，图文关系没有进入讲解现场

- 定位：`doc/agent-best-practices/00-llm-basics/01-llm-history.md` 开头；`03-linear-to-neural-network.md` 开头；`04-forward-loss-backprop.md` 开头；`06-attention-from-context.md` 开头；`07-transformer-architecture.md` 开头；`09-training-and-alignment.md` 开头；`10-inference-and-parameters.md` 开头；`12-evaluation.md` 开头；`16-llm-capabilities-boundaries.md` 开头。
- 问题表现：很多章节在标题后连续放 3-4 张图，只用一句“图解导读”整体说明。例如 `06-attention-from-context.md` 开头同时出现 QKV、CNN/RNN/Transformer、Transformer block、上下文装配流水线；`10-inference-and-parameters.md` 开头同时出现 prefill/decode、Transformer block、next-token loop、context assembly。图后很快进入“核心问题”，没有逐图解释“先看哪一层、这张图解决哪个疑问、读完本段后该回看图中哪一部分”。
- 为什么影响阅读：教材里的图应该承担“降低理解门槛”的功能。现在的图更像章节素材索引，读者还没建立概念框架就看到多张跨层级图，容易把图当成装饰或被迫跳过。尤其 Attention、推理、评测这些章节，图之间横跨机制、架构、工程流程，放在同一屏会削弱焦点。
- 建议怎么改：每章保留 1 张章首总览图，其余图移动到对应小节首次讲到的位置。每张图前增加一句明确任务，例如“先看图中 Q、K、V 三列：它们回答的是一个 token 如何判断该关注谁”；图后补 2-3 句解释，例如“这张图只解释相关性计算，不解释多层堆叠；多层结构会在下一节 Transformer 中展开”。章首多图如确实保留，应改成“本章图谱”列表，并说明建议阅读顺序。

### 2. 08、09、10、13、14、15 章节明显过长，和前半章的阅读节奏失衡

- 定位：`doc/agent-best-practices/00-llm-basics/03-token-and-embedding.md`（663 行）、`04-next-token-prediction.md`（562 行）、`05-capability-from-prediction.md`（664 行）、`09-training-and-alignment.md`（566 行）、`10-inference-and-parameters.md`（473 行）、`12-evaluation.md`（463 行）。
- 问题表现：这些章节大量使用“直觉层 / 机制层 / 形式层 / 工程层”的重复小节，并叠加多段代码块、表格和误区说明。相比 01-07 多数在 176-336 行之间，后半部分突然进入长篇百科式展开。
- 为什么影响阅读：章节长度不是单纯问题，但教材连续阅读需要节奏控制。08-10 是从表示到生成能力的关键桥段，当前每个概念都完整铺四层，会让核心推导线被局部说明淹没；读者很难判断哪些是本节必须掌握，哪些是拓展材料。
- 建议怎么改：给长章节做“主线压缩 + 拓展下沉”。每章开头明确 3 个必会判断；正文只保留支撑主线的例子和表格；公式、参数细节、长任务表可放到“进阶阅读 / 工程备查”小节。尤其 `03-token-and-embedding.md` 可拆成“tokenization 与 token id”和“embedding 与语义空间”两个内部大段；`05-capability-from-prediction.md` 可把语法、事实、格式、in-context learning 合并成一个能力来源总表，再挑 2 个例子展开。

### 3. README 与 SUMMARY 的章节编号可读，但文件名编号不一致，后续维护和引用容易混乱

- 定位：`doc/agent-best-practices/00-llm-basics/README.md` 的“章节框架”；`doc/agent-best-practices/SUMMARY.md` 的“一、大模型开发”。
- 问题表现：导航显示 01-16，但实际文件名不是同序号：第 02 节链接到 `01-function-to-machine-learning.md`，第 07 节链接到 `02-real-world-to-vectors.md`，第 08 节链接到 `03-token-and-embedding.md`，第 13 节链接到 `09-training-and-alignment.md`，第 15 节链接到 `12-evaluation.md`。目录中还存在相近旧稿，如 `10-inference-mechanism.md`、`11-decoding-parameters.md`、`09-instruction-tuning-alignment.md`、`llm-fundamentals.md`、`transformer-principles.md`。
- 为什么影响阅读：读者从页面导航看不出问题，但编辑、审校、链接维护、交叉引用时会反复出错。尤其当正文互相引用“上一节 / 下一节”或后续 agent 并行评审时，文件名编号和章节编号错位会制造沟通成本。
- 建议怎么改：至少在 README 增加“正式章节以本表链接为准”的短说明；更理想是统一重命名正式 01-16 文件，旧稿迁入 archive 或加明确前缀。SUMMARY 与 README 应共用同一套章节名、编号和链接，不要让文件系统里同时保留多套无标记候选稿。

### 4. `SUMMARY.md` 的大模型开发导航缺少本章 README 入口，且与全局中文速览存在路径语义不一致

- 定位：`doc/agent-best-practices/SUMMARY.md` “## 一、大模型开发”；相关参考：`doc/agent-best-practices/guide.zh.md` 中 00.1-00.10 仍指向旧式概念页。
- 问题表现：SUMMARY 的“大模型开发”直接从 01 节开始，没有列出 `00-llm-basics/README.md` 作为本章导读入口。与此同时，中文速览仍有“大模型基础”“Transformer 的工作原理”等旧导航页，和这次 01-16 连续教材的组织方式并存。
- 为什么影响阅读：教材入口不稳定会削弱学习路径。读者从 SUMMARY 进入会跳过 README 里的“总主线、每节写法、讲透标准、最终落点”；从中文速览进入又会看到另一套基础页，难以判断哪个是新版主线。
- 建议怎么改：SUMMARY 在 01-16 前增加“本章导读：大模型开发：从原理到工程边界”，链接到 `00-llm-basics/README.md`。中文速览后续也应标注哪些是旧概念页、哪些是新版 01-16 主线，避免两个目录体系互相抢入口。

## 严重程度 P2：影响连贯性、表达统一和版面消化

### 5. 标题层级过于模板化，部分章节像编辑提纲而不是成稿

- 定位：`doc/agent-best-practices/00-llm-basics/04-next-token-prediction.md` 多处“直觉层 / 机制层 / 形式层 / 工程层”；`05-capability-from-prediction.md` 多处同类小标题；`09-training-and-alignment.md` 中 `### 7.1` 到 `### 7.4`；`16-llm-capabilities-boundaries.md` 的“能做什么 / 能力边界 / 工程分工 / 为什么需要 Agent”。
- 问题表现：README 规定了每节要覆盖四层，但正文在长章节里机械重复这些层级。读者看到的是模板动作，而不是自然段落推进。部分小标题还混用“从哪里来”“直觉层”“机制层”“工程层”“小结”等编辑标签。
- 为什么影响阅读：教材标题应帮助读者预测内容。过多模板标签会让章节显得像内部写作检查表，削弱叙事感，也会让重要标题和辅助标题权重相同。
- 建议怎么改：保留四层作为写作检查标准，不必都显性成为标题。将小标题改成问题式或结论式，例如把“机制层”改为“模型实际输出的是词表上的概率分布”，把“工程层”改为“为什么结构化输出还需要 schema 校验”。每章最多保留 5-8 个真正面向读者的二级标题。

### 6. 表格和代码块密度偏高，部分位置缺少读表前后的解释

- 定位：`04-forward-loss-backprop.md` 的损失函数表、链路节点表及多段伪公式；`05-gradient-descent-training.md` 的 batch/step/epoch 表、optimizer 表、训练日志表；`10-inference-and-parameters.md` 的性能现象表、参数表、任务参数表、故障排查表；`12-evaluation.md` 的评测方式表、任务指标表、门禁项表；`16-llm-capabilities-boundaries.md` 多个四列表。
- 问题表现：表格承担了大量正文解释，有些表格前只给一句过渡，表后没有收束判断。代码块也大量用 `text` 包伪公式和流程箭头，连续出现时会打断自然阅读。
- 为什么影响阅读：表格适合比较和查阅，不适合替代概念讲解。当前一些表格列宽很长，移动端或 GitBook 页面中会横向拥挤；读者读完表也不一定知道该带走哪条结论。
- 建议怎么改：每张表前写清“这张表只比较哪一个维度”；表后用一句话收束“所以本节要记住的是……”。超过 5 行或 4 列的表考虑拆成列表或移到“工程备查”。伪公式只保留最关键的 1-2 个，其余改成自然语言或图中说明。

### 7. 术语中英文和大小写基本可懂，但全章统一表还不够明确

- 定位：全章 01-16，尤其 `03-token-and-embedding.md`、`04-next-token-prediction.md`、`06-attention-from-context.md`、`09-training-and-alignment.md`、`10-inference-and-parameters.md`、`12-evaluation.md`。
- 问题表现：同类术语有时用英文，有时用中文解释，有时中英混排：如 token、embedding、token id、vocabulary、next-token prediction、in-context learning、logits、softmax、pretraining、SFT、RLHF、DPO、inference、prefill、decode、context window、golden dataset、LLM-as-judge、benchmark、latency、cost。当前多在局部解释，缺少全章一致的首次出现规则。
- 为什么影响阅读：中英文术语在大模型教材里不可避免，但如果没有统一规则，读者会分不清哪些是必须记住的标准英文，哪些只是作者习惯。大小写和连字符也会影响检索和后续引用。
- 建议怎么改：在 README 或附录增加“术语写法约定”：首次出现用“中文名（English term）”，后文固定一种主写法；缩写如 SFT、RLHF、DPO 首次展开；工程常用词如 token、embedding、prompt、RAG、Agent 可固定英文。对 `next-token prediction`、`context window`、`LLM-as-judge` 等保留连字符和大小写一致性。

### 8. 章节之间的过渡句有，但有些过渡只是在“引出下一节”，没有回扣上一节学到的判断

- 定位：`README.md` 的“每节写法”；各章节末尾“连接到下一节”，例如 `05-capability-from-prediction.md` 末尾、`10-inference-and-parameters.md` 末尾、`12-evaluation.md` 末尾。
- 问题表现：多数章节末尾都有“下一节讲什么”，但常见写法是从当前概念跳到下个概念，缺少“本节结论如何改变读者判断”的收束。例如从生成参数进入评测，应该强调“参数能影响输出，但不能证明质量”；从评测进入能力边界，应该强调“评测暴露的是系统边界，不只是模型分数”。
- 为什么影响阅读：教材主线依赖连续判断，而不只是连续知识点。若过渡只承担目录功能，读者容易把章节当成并列条目，而不是层层推导。
- 建议怎么改：每章结尾采用固定三句结构：本节最终判断；这个判断仍解决不了什么；所以下一节必须讨论什么。这样既保持统一，也比单纯“引出下一节”更有教材感。

## 严重程度 P3：局部编辑一致性和表达精修

### 9. “大模型开发”这个栏目名和章节实际内容存在轻微偏差

- 定位：`doc/agent-best-practices/SUMMARY.md` 的“## 一、大模型开发”；`doc/agent-best-practices/00-llm-basics/README.md` 标题“大模型开发：从原理到工程边界”。
- 问题表现：01-16 主要是“大模型基础原理与工程边界”，不是狭义“开发”。真正的 Prompt、RAG、工具、状态、评测工程在后续栏目展开。
- 为什么影响阅读：栏目名会设定期待。“大模型开发”容易让读者期待 API 调用、模型服务、微调实操和工程配置；实际内容更偏基础教材和工程判断框架。
- 建议怎么改：SUMMARY 栏目可改为“大模型基础与工程边界”或“大模型原理基础”。如果必须保留“大模型开发”，建议在 README 开头补一句：“这里的开发不是 API 实操，而是开发者理解模型能力和边界所需的基础。”

### 10. 局部标题编号和标题文本可再做一次全章校准

- 定位：`doc/agent-best-practices/00-llm-basics/README.md` 章节框架；各正文 `# 01` 到 `# 16`；`doc/agent-best-practices/SUMMARY.md`。
- 问题表现：显示编号目前一致，但正文文件名和旧稿并存已经增加误读风险；部分标题偏口语化，如“为什么预测下一个 token 会产生能力”“大模型能做什么，不能做什么”，适合读者，但和“模型评测与工程验证”“预训练、指令微调与对齐”这类名词型标题混在一起，风格略不统一。
- 为什么影响阅读：标题风格不一致本身不是大问题，但教材目录需要稳定的识别感。问题式标题和名词式标题混用时，应有明确节奏，而不是偶然混用。
- 建议怎么改：保留问题式标题的亲和力，但统一目录风格。可采用“问题式主标题 + 名词式副标题”或反过来，例如“10. 预测下一个 token 为什么会产生能力：能力来源与边界”。

### 11. 部分术语和语气可减少绝对化表达

- 定位：`16-llm-capabilities-boundaries.md` “大模型不是什么”“能力边界”；`README.md` “大模型不是数据库 / 权限系统 / 状态机 / 可靠执行器”；`10-inference-and-parameters.md` 参数建议表。
- 问题表现：当前边界表达清晰有力，但有些句式连续使用“不是”“不能”“必须”，在教材中容易显得像结论口号。参数建议表中“推荐倾向”也需要提醒“随模型、任务、评测集变化”。
- 为什么影响阅读：边界章节需要坚定，但教材还要避免把工程判断写成过度绝对的规则。读者后续遇到例外场景时，可能误以为正文与现实冲突。
- 建议怎么改：保留结论句，但在首次出现时增加适用条件，例如“在没有外部数据源、权限系统和执行确认的应用里，大模型不应承担……”。参数表后补“这些是起点，不是上线配置；最终以评测集和线上指标为准”。

## 下一轮复审重点

1. 先复审目录入口：`README.md`、`SUMMARY.md`、中文速览和正式 01-16 文件名是否形成唯一、稳定的导航体系。
2. 再复审图文混排：每张图是否移动到对应概念首次讲解处，是否具备图前导语和图后解释，章首是否只保留必要总览图。
3. 重点抽查长章节：`03-token-and-embedding.md`、`04-next-token-prediction.md`、`05-capability-from-prediction.md`、`09-training-and-alignment.md`、`10-inference-and-parameters.md`、`12-evaluation.md` 是否压缩主线、下沉备查材料。
4. 统一术语表和标题风格：检查 token、embedding、Attention、Transformer、SFT、RLHF、DPO、prefill、decode、LLM-as-judge 等术语首次出现、大小写、连字符和中英文对应。
5. 最后做版面密度复核：表格是否过宽、代码块是否过多、每章结尾是否用“本节判断 → 未解决问题 → 下一节必要性”完成过渡。
