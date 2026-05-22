# Round 2 小白学习者复审：大模型基础 01-16

## 总判断

从初学者学习路径和逻辑支撑看，Round 1 提出的主要 P0/P1 级问题已经大部分解决。当前版本已经能让读者看出一条连续主线：

```text
机器学习最小结构
→ 神经网络表达能力
→ 训练、优化、泛化
→ 输入表示与 token
→ next-token prediction
→ 能力来源
→ Attention 与 Transformer
→ 训练、对齐、推理、评测
→ 能力边界
→ 为什么需要 Agent 工程
```

对完全初学者来说，现在最大问题不再是“为什么突然换话题”，而是“关键章节信息量仍然偏大，容易知道方向但消化慢”。因此本轮建议不是推倒重写，而是进入下一轮有针对性的结构减负。

## Round 1 P0/P1 解决情况

### 已解决：01 总览提前抛出高阶术语的问题

定位：`doc/agent-best-practices/00-llm-basics/01-llm-history.md`，`## 核心问题` 前后的初学者提示。

Round 1 问题：读者刚开始就看到 RNN、Attention、Transformer、RLHF、DPO、RAG、Agent，容易误以为现在必须全部理解。

当前判断：已解决。现在明确写了“这一节只做总览”，并告诉初学者 RNN、LSTM、Attention、Transformer、RLHF、DPO、RAG、Agent 只要先知道解决什么问题，后面会逐个拆开。最后也明确下一节会回到 `输入 x -> 模型 f -> 输出 y`。

建议：无需作为阻塞继续处理。

### 已解决：06 到现实输入向量化的跳跃问题

定位：`doc/agent-best-practices/00-llm-basics/06-fitting-generalization-overfitting.md`，`## 连接到下一节`。

Round 1 问题：泛化和过拟合讲完后，突然进入“现实对象向量化”，读者会觉得换题。

当前判断：已解决。现在结尾先收束“模型表达能力 -> 预测与损失 -> 梯度与训练 -> 泛化与评测”，再指出还要回到输入端，因为文字、图片、声音不是天然数字向量。这个过渡能解释为什么下一步必须讲表示。

建议：无需作为阻塞继续处理。

### 已解决：13 进入预训练、SFT、RLHF、DPO 前缺少层级区分

定位：`doc/agent-best-practices/00-llm-basics/09-training-and-alignment.md`，`## 核心问题` 下的分层表。

Round 1 问题：读者可能分不清 Transformer 是模型结构，Pretraining、SFT、RLHF、DPO 是训练阶段，Inference 是使用阶段。

当前判断：已解决。现在用表格把 Transformer、Pretraining、SFT / instruction tuning、RLHF / DPO、Inference 放在不同层级，能有效防止初学者把架构部件、训练阶段和 Prompt 技巧混在一起。

建议：无需作为阻塞继续处理。

### 已解决：SUMMARY 从大模型边界到 Agent 开发承接不足

定位：`doc/agent-best-practices/SUMMARY.md`，`## 二、Agent 开发`。

Round 1 问题：第 16 节讲完大模型边界后，SUMMARY 直接进入 Agent 原理，缺少“为什么后面学 Prompt、RAG、状态、工具、MCP”的桥。

当前判断：已解决。现在 `## 二、Agent 开发` 下已经明确说明：大模型不能独自承担事实、状态、权限、执行和审计，后续 Agent 部分就是学习 Prompt、RAG、记忆、状态、工具、MCP、评测和工程流程如何补齐这些缺口。

建议：无需作为阻塞继续处理。

### 已解决：token embedding、上下文化表示、text embedding 容易混淆

定位：`doc/agent-best-practices/00-llm-basics/03-token-and-embedding.md`，`## 小结：token、embedding 与上下文化表示的区别`。

Round 1 问题：初学者容易把 token id、token embedding、上下文化表示、RAG 里的 text embedding 都理解成同一种“向量”。

当前判断：已解决。当前对照表清楚区分了四者的含义、是否随上下文变化和常见用途，并特别说明 RAG 里的 text embedding 不等于语言模型输入层的 token embedding。

建议：无需作为阻塞继续处理。

### 已解决：next-token prediction 的能力来源与产品可靠性混淆

定位：`doc/agent-best-practices/00-llm-basics/05-capability-from-prediction.md`，`## 核心问题`。

Round 1 问题：读者可能误解为“只要会预测下一个 token，就自然可靠地会所有任务”。

当前判断：已解决。现在开头明确说“产生能力”只是学到可迁移语言结构、事实关联和任务模式，不等于具体业务中稳定、可验证、可负责地完成任务，后者还需要 Prompt、RAG、工具、评测、权限和状态系统。

建议：无需作为阻塞继续处理。

### 已解决：Attention 引入 RNN/LSTM 时缺少学习范围说明

定位：`doc/agent-best-practices/00-llm-basics/06-attention-from-context.md`，`## 从哪里来：RNN / LSTM 的上下文瓶颈`。

Round 1 问题：完全小白可能以为又多了一组必须深入学习的旧架构。

当前判断：已解决。现在明确说明 RNN / LSTM 不是新的学习主线，只是用来对比旧序列处理方式的上下文瓶颈。

建议：无需作为阻塞继续处理。

### 已解决：14 推理参数与 09 采样内容重复感

定位：`doc/agent-best-practices/00-llm-basics/10-inference-and-parameters.md`，`## 核心问题`。

Round 1 问题：第 09 节讲过采样，第 14 节又讲 temperature、top_p、top_k，读者可能不知道差异。

当前判断：已解决。现在第 14 节开头明确区分：第 09 节讲采样是为了理解 next-token prediction 的基本机制，本节重新讲采样是为了放进真实推理服务，和 prefill、decode、KV cache、延迟、成本一起看。

建议：无需作为阻塞继续处理。

### 基本解决：README / SUMMARY 编号与文件名不一致

定位：`doc/agent-best-practices/00-llm-basics/README.md`，`## 章节框架` 后的说明；`doc/agent-best-practices/SUMMARY.md`，`## 一、大模型基础与工程边界`。

Round 1 问题：展示顺序是 01-16，但文件名保留旧编号，初学者从编辑器找文件会困惑。

当前判断：基本解决。README 已经明确说 01-16 是正式推荐阅读顺序，部分文件名保留早期编号，阅读、引用和复审以 README 和 SUMMARY 为准。SUMMARY 也补了本章 README 入口。

建议：对普通阅读路径已够用；如果后续要长期维护教材，仍建议单独规划文件重命名或 archive 旧稿，但这不是本轮初学者路径阻塞。

## 仍会卡住的地方

### 1. 长章节仍会让初学者“知道主线，但读到中途失焦”

定位：

- `doc/agent-best-practices/00-llm-basics/03-token-and-embedding.md`，`# 08. 从文字到 token 和 embedding`
- `doc/agent-best-practices/00-llm-basics/04-next-token-prediction.md`，`# 09. 语言模型为什么预测下一个 token`
- `doc/agent-best-practices/00-llm-basics/05-capability-from-prediction.md`，`# 10. 为什么预测下一个 token 会产生能力`
- `doc/agent-best-practices/00-llm-basics/09-training-and-alignment.md`，`# 13. 预训练、指令微调与对齐`
- `doc/agent-best-practices/00-llm-basics/10-inference-and-parameters.md`，`# 14. 推理机制与生成参数`
- `doc/agent-best-practices/00-llm-basics/12-evaluation.md`，`# 15. 模型评测与工程验证`

现在还卡在哪里：这些章节的逻辑补强了，但篇幅仍然很长。初学者读 08、09、10 连续三章时，会连续遇到 token、embedding、logits、softmax、概率分布、能力来源、in-context learning、幻觉、RAG、Agent 等概念。每个概念都有解释，但缺少“本节最低掌握线”和“可以先跳过的进阶内容”标记。

建议怎么补：每个长章节开头增加一个“初学者先带走这 3 件事”，章节中把公式、参数表、工程备查类内容标成“进阶阅读”。不一定要立即大幅删文，但要让读者知道第一次读应该抓哪几条主线。

### 2. 章首多图问题仍会增加初学者第一屏压力

定位：

- `doc/agent-best-practices/00-llm-basics/03-token-and-embedding.md`，标题下连续多张图
- `doc/agent-best-practices/00-llm-basics/04-next-token-prediction.md`，标题下连续多张图
- `doc/agent-best-practices/00-llm-basics/05-capability-from-prediction.md`，标题下连续多张图
- `doc/agent-best-practices/00-llm-basics/09-training-and-alignment.md`，标题下连续多张图
- `doc/agent-best-practices/00-llm-basics/10-inference-and-parameters.md`，标题下连续多张图
- `doc/agent-best-practices/00-llm-basics/12-evaluation.md`，标题下连续多张图
- `doc/agent-best-practices/00-llm-basics/16-llm-capabilities-boundaries.md`，标题下连续多张图

现在还卡在哪里：README 已经补了“章首图用于建立地图，正文图用于解释当前概念”的阅读约定，这能缓解压力。但读者进入具体章节时，仍会在理解核心问题前先看到多张跨层级图。例如第 14 节同时出现 prefill/decode、Transformer block、next-token loop、context assembly，对新手来说会先形成“这章很复杂”的心理负担。

建议怎么补：每章章首最多保留一张总览图，其余图移动到首次讲到对应概念的小节。如果暂时不移动，至少在每张图前加一句“第一次读只看哪一部分”，不要只用一段总的图解导读覆盖所有图。

### 3. `MCP` 在学习路径里出现了，但初学者入口解释还不够

定位：

- `doc/agent-best-practices/00-llm-basics/README.md`，`## 阅读约定`
- `doc/agent-best-practices/SUMMARY.md`，`## 二、Agent 开发`
- `doc/agent-best-practices/00-llm-basics/16-llm-capabilities-boundaries.md`，章首图 `MCP 与工具调用泳道图`

现在还卡在哪里：README 说本章会提前出现 Prompt、RAG、工具调用、MCP、Agent 等词，但术语表里没有单独解释 MCP。SUMMARY 的 Agent 承接也提到 MCP。第 16 节章首图名直接出现“MCP 与工具调用泳道图”。初学者会知道 MCP 和工具有关，但还不知道它在这条学习路径里到底先理解成什么。

建议怎么补：在 README 的“阅读约定”表里补一行 MCP，例如“工具和模型之间的标准化连接协议，先理解成让 Agent 以统一方式发现和调用外部能力”。第 16 节章首如果保留 MCP 图，也建议在图前或图后加一句“这里先不用理解协议细节，只看模型请求、工具执行、结果返回的分工”。

### 4. 第 16 节工程边界收束清楚，但工程词集中出现时仍偏重

定位：`doc/agent-best-practices/00-llm-basics/16-llm-capabilities-boundaries.md`，`## 大模型不是什么`、`## 最小判断框架`。

现在还卡在哪里：第 16 节已经加了工程词小抄，也用“模型不是数据库、权限系统、状态机、执行器”建立了边界。但对小白来说，IAM、ACL、RBAC、ABAC、workflow、状态机、幂等、事务、回滚、trace 会在短时间内集中出现。它们是必要工程词，但容易让读者从“大模型边界”跳到“后端系统术语速成”。

建议怎么补：保留小抄，但在表前加一句学习范围说明：这些词现在只用来理解“哪些职责不能交给模型”，不要求掌握实现。也可以在表后增加一个最小例子，把一个动作分成“模型生成建议、权限系统判断、工具执行、日志记录”，让术语落到同一个场景里。

### 5. `12-evaluation.md` 已经承接推理，但评测与前面机器学习评估的关系可以再回扣一次

定位：`doc/agent-best-practices/00-llm-basics/12-evaluation.md`，`## 核心问题`、`## 2. Golden dataset：固定测试集是评测的地基`。

现在还卡在哪里：第 06 节已经讲训练集、验证集、测试集、accuracy、precision、recall；第 15 节又讲 golden dataset、LLM-as-judge、benchmark、回归测试。现在两处各自成立，但初学者可能会问：golden dataset 和前面的测试集是什么关系？LLM 应用评测是不是机器学习评估的另一个名字？

建议怎么补：在第 15 节开头补一段回扣：“第 06 节讲的是机器学习训练时如何避免只适配训练集；本节讲的是模型、prompt、RAG、参数和工具链作为一个应用系统时如何持续回归测试。Golden dataset 可以理解成大模型应用里的固定测试集，但样本里还要包含期望行为、评分规则、成本和安全边界。”

## 是否建议进入下一轮修订

建议进入下一轮修订，但不建议大改主线。

本轮 Round 1 的初学者 P0/P1 逻辑断层已经基本修复，章节顺序可以成立。下一轮重点应放在“降低首次阅读负担”：

- 给长章节加最低掌握线和进阶阅读标记。
- 处理章首多图造成的第一屏压力。
- 补齐 MCP 等提前出现工程词的一句话解释。
- 在第 15 节回扣第 06 节，让“机器学习评估”和“大模型应用评测”关系更清楚。

完成这些后，就可以进入更细的事实校对、术语统一和版面编辑阶段。
