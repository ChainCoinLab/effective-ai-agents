# 新手学习视角审查：大模型开发教程

审查视角：假设读者是没有大模型开发经验的新手，要按教程一步一步学习。重点检查三件事：

- 每个小节是否讲清楚。
- 知识点之间是否连贯。
- 后面章节是否依赖了前面没有铺垫的知识。

审查范围：`doc/agent-best-practices/README.md`、`SUMMARY.md`、`guide.zh.md`，以及 `00-llm-basics`、Prompt、RAG、记忆、工具/Agent、评测、反馈、源码实现、行业理解等目录。

## 总判断

这套教程的方向是对的，主线也成立：先讲大模型能力来源和边界，再讲 Prompt、RAG、记忆、工具、MCP、Agent、评测和反馈闭环，最后用源码小闭环落地。

但从“新手一步一步跟学”的角度看，当前教程分成两种完成度：

| 部分 | 新手可跟学程度 | 判断 |
| --- | --- | --- |
| `00-llm-basics` 01-16 | 较高 | 已经有阶段路线、核心问题、过渡和小白复审记录，整体能读通。 |
| `01-prompt-instruction` 到 `06-feedback-iteration` | 中低 | 很多小节像最佳实践卡片，不像教程。知道结论，但缺例子、反例、练习和前置解释。 |
| `07-source-implementation/go-agent-from-zero` | 中高 | 前几节有完整代码和运行方式，适合跟做；后几节开始变短，需要补完整实现。 |
| `07-source-implementation/mcp-from-zero` | 低 | 标题叫“从零实现”，但多数小节没有代码、运行命令和可验证结果。 |
| `07-source-implementation/skill-from-zero` | 低 | 目前是计划，不是教程。 |
| 行业理解 | 可作为扩展阅读 | 不是大模型开发主线的一部分，应明确标成选读。 |

最大问题不是大模型基础讲不通，而是后半部分从“教学章节”突然变成“工程原则清单”。新手会知道这些规则重要，但不知道怎么做，也不知道做到什么程度算通过。

## P0：会阻塞新手继续学习的问题

### 1. 入口路径不完全统一

涉及文件：

- `doc/agent-best-practices/README.md`
- `doc/agent-best-practices/SUMMARY.md`
- `doc/agent-best-practices/guide.zh.md`
- `doc/agent-best-practices/00-machine-learning-basics/README.md`
- `doc/agent-best-practices/00-llm-basics/README.md`

问题：

`README.md`、`SUMMARY.md` 和 `guide.zh.md` 都能作为入口，但它们给出的基础学习路径不完全一致。`SUMMARY.md` 推荐 01-16 的大模型基础主线；`guide.zh.md` 还保留 `llm-fundamentals.md`、`transformer-principles.md`、`context-window-basics.md` 等旧式基础页；根 README 又把 `00-machine-learning-basics` 和 `00-llm-basics` 都列为入口。

新手可能不知道自己应该先读：

- `00-machine-learning-basics/README.md`
- `00-llm-basics/README.md`
- `guide.zh.md` 里的 00.1 到 00.10
- 还是 `SUMMARY.md` 里的 01-16

建议：

明确唯一主学习路径，例如：

```text
主线：README -> SUMMARY -> 00-llm-basics/README -> 01-16
速查：guide.zh.md 只作为概念速查，不作为从零学习路径
补充：00-machine-learning-basics/README 作为 00-llm-basics 的前置导读
```

并在 `guide.zh.md` 顶部写明：这是速查表，不替代 01-16 主教程。

### 2. Prompt/RAG/记忆/工具/评测/反馈很多小节只是卡片，不是教程

涉及目录：

- `01-prompt-instruction`
- `02-context-rag`
- `03-memory-state`
- `04-tools-agents`
- `05-evaluation-verification`
- `06-feedback-iteration`

问题：

大量小节只有 `Rule / Why / Optimize / Verify / References`，篇幅约 20-30 行。它们适合工程师复习，不适合新手学习。

例如：

- `01-prompt-instruction/01-define-success-before-prompt.md` 说“先写清成功标准”，但没有展示一个坏 Prompt 如何改成有验收标准的 Prompt。
- `03-memory-state/20-memory-write-policy.md` 说“长期记忆写入应有明确规则”，但没有给出“哪些能写、哪些不能写、如何判断”的完整样例。
- `04-tools-agents/25-small-clear-tool-interfaces.md` 说“工具接口要小而清晰”，但没有对比一个坏 schema 和一个好 schema。
- `05-evaluation-verification/35-extended-test-pyramid.md` 说 AI 系统要扩展测试金字塔，但没有给出一个最小测试集结构。
- `06-feedback-iteration/43-production-feedback-engineering-loop.md` 说生产反馈要进入工程闭环，但没有示范一次失败如何变成 eval case。

新手会出现的感受：

```text
我知道原则了，但不知道怎么落地。
我知道要 Verify，但不知道我应该写什么文件、跑什么命令、看什么结果。
```

建议：

每个实践小节至少补齐：

- 一个真实小场景。
- 一个错误做法。
- 一个改进后的做法。
- 一个最小可执行示例或伪代码。
- 一个新手练习。
- 一个验收标准。

### 3. `mcp-from-zero` 标题和内容落差大

涉及目录：`07-source-implementation/mcp-from-zero`

问题：

这个专题叫“从零实现 MCP”，但多数小节只描述工具名、请求、响应、权限边界，没有真正从零实现 server、协议消息、启动方式和客户端调用。

例如：

- `01-local-stdio-server.md` 只说明 `ping` 工具返回 `{ "ok": true }`，但没有完整代码。
- `06-http-server.md` 只列出 HTTP endpoint，没有服务端实现和调用示例。
- `07-http-list-tables.md` 到 `09-http-delete-confirm.md` 更像 API 设计草稿，不像可跟做教程。

这会直接阻塞新手，因为他无法照着教程跑出一个 MCP Server。

建议：

每一节补齐：

- 文件结构。
- 完整代码。
- 启动命令。
- 测试命令。
- 输入输出。
- 常见报错。
- 和上一节相比改了哪些代码。

### 4. `skill-from-zero` 目前还是计划，不是教程

涉及文件：`07-source-implementation/skill-from-zero/README.md`

问题：

该文件写的是“计划中的学习路径”，没有实际小节文件。新手读到这里会以为 Skill 教程还没写完。

建议：

要么改标题为“Skill 教程计划”，要么补齐 01-07 小节。不要让它在主学习路径中看起来像已完成教程。

## P1：明显影响理解但不一定阻塞

### 1. `00-llm-basics` 主线能读通，但长章节仍有负担

`00-llm-basics` 已经经过多轮小白复审，当前没有明显 P0 断层。优点是：

- 有 01-16 推荐顺序。
- 有阶段分组。
- 有“第一次读先带走三件事”。
- 能从机器学习一路推到 Agent 边界。

仍然会让新手吃力的点：

- `08-token-and-embedding.md`、`09-next-token-prediction.md`、`10-capability-from-prediction.md`、`13-training-and-alignment.md`、`14-inference-and-parameters.md`、`15-evaluation.md` 篇幅很长。
- 训练与对齐章节里 `PPO`、`GRPO`、`DPO`、reward model 等术语密集。
- Transformer 相关章节里高级变体容易干扰主干。

建议：

继续保留主线，但把高级内容明确标成“进阶阅读”。新手第一遍只要求掌握主干：

```text
token -> embedding -> next-token prediction -> attention -> transformer -> pretraining/SFT -> inference -> eval -> boundary
```

### 2. RAG 模块深度不均衡

涉及目录：`02-context-rag`

问题：

09-12、14-16、18 多数是短卡片；13 `RAG 优化要可观测` 又非常深入，直接进入动态切分、query rewrite、hybrid retrieval、rerank、Context Recall、Faithfulness、Citation Accuracy 等概念。

新手读到 13 会卡住，因为前面还没有完整建立：

- 文档如何被解析。
- chunk 是什么。
- embedding 检索如何工作。
- rerank 为什么需要。
- citation 和 faithfulness 怎么评估。
- RAG 的一次请求链路如何落到代码。

建议：

在 09 和 13 之间补一个“最小 RAG 流程”教程：

```text
原始文档 -> 切 chunk -> 生成 embedding -> 存索引 -> 用户 query -> 检索 top-k -> 拼上下文 -> 生成回答 -> 引用证据
```

### 3. 记忆与状态模块前后落差大

涉及目录：`03-memory-state`

问题：

`19-memory-context-state-boundaries.md` 很完整，讲了长任务记忆、上下文窗口、向量库、结构化记忆、确定性状态库、trace 等。但 20-24 又变成 24 行左右的规则卡片。

新手会知道“记忆要治理”，但不知道怎么设计记忆记录结构。例如：

- 一条长期记忆长什么样？
- 来源、时间戳、置信度放在哪里？
- 用户删除记忆时系统怎么处理？
- 任务状态和长期记忆的数据库表如何区分？

建议：

补一个统一示例贯穿 19-24：比如“写文章 Agent 记住用户偏好，但任务进度放状态表”。每节都只扩展这个例子的一部分。

### 4. 工具与 Agent 模块有多个小节缺少一级标题

涉及文件：

- `04-tools-agents/25-small-clear-tool-interfaces.md`
- `04-tools-agents/26-tool-description-when-not-to-use.md`
- `04-tools-agents/27-intent-vs-permission.md`
- `04-tools-agents/28-confirm-high-risk-actions.md`
- `04-tools-agents/31-multi-agent-boundaries.md`
- `04-tools-agents/32-multi-agent-test-verification.md`
- `04-tools-agents/33-structured-handoff-context.md`
- `04-tools-agents/34-replayable-agent-traces.md`

问题：

这些文件第一行是 `## Status`，没有 `# 标题`。从目录点进去时，新手看不到当前章节名，只看到状态字段，阅读体验像打开了一张元数据卡片。

建议：

补上和目录一致的 H1 标题，然后再放 Status。

### 5. 多 Agent 概念跳得偏快

涉及：

- `04-tools-agents/31-multi-agent-boundaries.md`
- `04-tools-agents/32-multi-agent-test-verification.md`
- `04-tools-agents/33-structured-handoff-context.md`
- `07-source-implementation/multi-agent-interaction`

问题：

多 Agent 章节默认读者已经理解：

- 主 Agent / 子 Agent。
- handoff。
- structured context。
- verification agent。
- trace replay。
- merge strategy。

但前面没有一个“为什么单 Agent 不够，什么时候才拆多 Agent”的小白故事。

建议：

先用一个小任务解释：

```text
代码审查任务太复杂
-> Planner 决定看哪些文件
-> Reader 只负责读文件
-> Reviewer 提出问题
-> Verifier 检查证据
-> Reporter 汇总
```

然后再讲职责边界、handoff 和 trace。

### 6. 评测模块需要更多可操作样例

涉及目录：`05-evaluation-verification`

问题：

README 的分类清楚，但单点小节太短。新手会知道要 eval、golden dataset、LLM-as-judge、反例攻击样例、回归测试，但不知道怎么创建第一份评测文件。

建议：

补一个最小 eval 样例：

```json
{
  "id": "refund-policy-001",
  "input": "会员过期后还能退款吗？",
  "expected_behavior": "基于制度回答，不确定时要求补充购买时间",
  "must_cite": ["refund_policy_v3#section_2"],
  "must_not": ["编造退款比例", "直接承诺退款"],
  "rubric": {
    "grounded": 2,
    "complete": 2,
    "safe": 2
  }
}
```

### 7. 反馈闭环模块缺少从失败到修复的完整故事

涉及目录：`06-feedback-iteration`

问题：

43-50 都是正确原则，但新手读完不容易形成闭环感。比如“反馈不等于直接训练模型”很重要，但需要一个案例说明同一个失败可能分别该改 Prompt、RAG、工具、产品流程或模型。

建议：

补一个贯穿案例：

```text
用户投诉回答了过期政策
-> 查看 trace
-> 发现检索命中了旧文档
-> 标成 RAG 数据更新问题
-> 增加 eval case
-> 更新索引
-> 回归测试
-> 灰度发布
-> 线上监控
```

## P2：发布态和学习体验优化

### 1. 给每章加“前置知识”和“学完能做什么”

建议每个 README 都加：

- 读本章前要懂什么。
- 本章不讲什么。
- 学完后能做什么。
- 推荐练习。

### 2. 加统一术语表

后半部分高频出现但对新手不友好的词：

- schema
- trace
- eval
- golden dataset
- rubric
- rerank
- chunk
- grounding
- faithfulness
- workflow
- handoff
- idempotency / 幂等
- RBAC / ABAC
- observability

建议放一个 `glossary.md`，每个术语一句话解释，再链接到深入章节。

### 3. 区分“主线必读”和“工程备查”

当前很多内容都很有价值，但并不都适合第一遍学习。建议标注：

- 必读：形成主线判断。
- 实操：跟着写代码。
- 进阶：先知道名字，后面再细学。
- 备查：做项目时查规则。

### 4. 源码教程需要统一环境说明

建议在 `07-source-implementation/README.md` 前面补：

- 需要的 Go 版本。
- API key 如何设置。
- 模型名如何替换。
- 每节代码放在哪个目录。
- 是否每节都是独立 `main.go`。
- 如何处理网络/API 报错。
- 如何确认本节跑通。

### 5. 行业理解应明确为选读

`08-industry-finance` 和 `09-industry-web3` 写得清楚，但不是大模型开发主线的必需前置知识。建议在 `SUMMARY.md` 或 README 里标注“完成工程主线后选读”。

## 按模块的具体学习连贯性判断

| 模块 | 清楚吗 | 连贯吗 | 主要问题 |
| --- | --- | --- | --- |
| 全局 README / SUMMARY | 基本清楚 | 基本连贯 | 多入口路径并存，`guide.zh.md` 和 01-16 主线关系需说明。 |
| `00-machine-learning-basics` | 清楚 | 和 00-llm 有重叠 | 适合作导读，但要说明不是替代 01-16。 |
| `00-llm-basics` 01-16 | 较清楚 | 较连贯 | 长章节仍重，高级术语需标进阶。 |
| `01-llm-engineering` | 清楚但太概览 | 承接合理 | 只有 README，没有展开小节。 |
| Prompt 实践 | 原则清楚 | 顺序合理 | 缺完整 Prompt 改造案例。 |
| RAG 实践 | 局部清楚 | 深度不均 | 13 太深，前面缺最小 RAG 实操铺垫。 |
| 记忆与状态 | 19 很清楚，20-24 太短 | 思路合理 | 缺贯穿样例和数据结构。 |
| 工具/MCP/多 Agent | 方向清楚 | 概念跳跃 | 多个文件缺 H1；工具 schema、权限、handoff 缺对照案例。 |
| 评测与验证 | 分类清楚 | 顺序合理 | 缺 eval 文件、rubric、judge 校准示例。 |
| 反馈迭代 | 原则清楚 | 闭环感不足 | 缺一次生产失败到修复发布的完整故事。 |
| Go Agent 源码 | 前半清楚 | 小步推进好 | 后半节奏变快；需要环境页和完整项目结构。 |
| MCP 源码 | 不够清楚 | 路径有但内容不足 | 缺真正可运行代码。 |
| Skill 源码 | 不够清楚 | 只是计划 | 不应作为已完成教程放在主线。 |
| 多 Agent 源码 | 场景清楚 | 概念顺序合理 | 缺可运行 coordinator 和消息循环。 |
| 行业理解 | 清楚 | 与主线关系明确 | 应标选读。 |

## 建议的修订顺序

1. 统一入口路径，明确 `SUMMARY.md` 的 01-16 是主线，`guide.zh.md` 是速查。
2. 把 `mcp-from-zero` 和 `skill-from-zero` 从“计划/草稿”补成可运行教程，或先标注未完成。
3. 给 01-06 最佳实践短卡片补最小案例，优先补 Prompt、RAG、工具、评测四组。
4. 给所有短卡片加 H1 标题、前置知识、练习和验收标准。
5. 给源码教程加统一环境准备页。
6. 增加术语表，降低后半工程词密度。
7. 最后再做版面和标题统一。

## 一句话结论

如果目标是“理解大模型和 Agent 工程为什么这样设计”，当前教程已经有比较好的骨架；如果目标是“新手小白跟着每一节一步一步学会大模型开发”，后半部分还需要从原则卡片升级成带例子、代码、练习和验收的教程。
