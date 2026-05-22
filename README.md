# AI Engineering Knowledge System

这是一个面向工程师的 AI 知识体系项目，目标是把“机器学习、大模型、RAG、Agent、MCP、工具调用、评测、源码实现”串成一条能读懂、能落地、能继续扩展的学习路径。

它不是零散笔记，也不是只教你调几个 API 参数。这个项目想解决的是一个更实际的问题：

```text
当你准备做 AI 应用、RAG 系统、Agent 工具链或大模型工程化时，
你到底应该先理解哪些原理，哪些边界必须交给工程系统，代码又该怎么一步步写出来？
```

## 这个项目要做什么

很多人学习 AI 会卡在两头：

- 只看模型 API 和 Prompt，能调出一个 demo，但不知道为什么输出不稳定、为什么会幻觉、为什么工具调用会失败。
- 只看 Transformer、Attention、训练公式，又不知道这些概念和真实的 RAG、Agent、权限、状态、评测有什么关系。

这个项目把这两头接起来：

1. 从机器学习最小问题开始，解释模型如何学习规律。
2. 继续讲 token、embedding、Attention、Transformer、训练、推理和评测。
3. 再进入 Prompt、RAG、记忆、状态、工具调用、MCP 和 Agent 工程。
4. 最后用源码小闭环把关键概念写出来，而不是停留在概念层。

读这个项目的目标不是“背 AI 术语”，而是形成工程判断：模型负责什么，RAG 补什么，工具执行什么，状态系统记录什么，权限和评测为什么不能交给模型自己决定。

## 你能从这里获得什么

如果你正在学大模型，可以从这里弄清楚：

- 一句话为什么要先变成 token，再变成 embedding 向量矩阵。
- 为什么 next-token prediction 这种看似简单的目标，会产生语言理解、代码补全和任务迁移能力。
- Attention、Q/K/V、Transformer block 到底在解决什么上下文问题。
- temperature、top_p、context window、KV cache 为什么会影响输出质量、成本和延迟。

如果你正在做 AI 应用，可以从这里找到工程答案：

- RAG 准确率低时，应该先区分“检索质量差”还是“生成阶段没用好证据”。
- Prompt 不应该只是写一大段说明，而要定义成功标准、退出路径和可机器检查的输出。
- Agent 调用工具时，模型只应该生成调用意图，真实执行、权限判断和高风险确认必须由工程系统控制。
- 评测不能只看最终答案，还要看检索结果、工具轨迹、中间状态和回归样例。

如果你想写代码实现，可以直接看源码教程：

- 用小词表和小矩阵实现 `token id -> embedding matrix`。
- 从零写一个能调用模型 API 的 Agent。
- 给 Agent 增加多轮上下文、流式输出、tool use、MCP、数据库工具和权限确认。
- 拆出 Planning、Review、Verification 等子 Agent，理解多 Agent 怎么协作。

## 例子：这个项目会怎么讲问题

### 例子 1：一句话如何进入大模型

不是直接说“embedding 是语义向量”，而是拆成：

```text
文本
→ token
→ token id
→ embedding table 查表
→ 输入矩阵 X
→ Attention / Transformer
→ 下一个 token 概率分布
```

并配套一个最小代码实现，说明：

```text
X = one_hot_matrix @ embedding_table
```

真实系统里通常不会显式构造巨大的 one-hot，而是直接查表：

```text
X = E[token_ids]
```

### 例子 2：为什么 Agent 不能只靠模型自己执行

模型可以判断“用户想删除一条记录”，但它不应该自己决定是否真的删除。

更可靠的工程分工是：

```text
模型：理解用户意图，生成候选工具调用
应用：校验参数、权限、风险等级
用户：确认高风险动作
工具：执行真实操作
日志：记录可审计轨迹
评测：验证结果和过程是否符合预期
```

这样 Agent 才能从“看起来聪明的聊天框”，变成可控制、可观察、可恢复的工程系统。

### 例子 3：RAG 不是把资料塞得越多越好

当回答不准时，不能只说“模型不行”。要拆开看：

```text
问题是否被正确理解？
检索是否召回了相关资料？
chunk 是否切得适合任务？
上下文里是否有冲突或注入内容？
生成时是否引用了证据？
答案是否能被测试集回归验证？
```

这也是项目里把 Prompt、上下文工程、RAG、评测和观测拆成独立章节的原因。

## 内容入口

- [AI 工程知识结构总览](doc/agent-best-practices/README.md)
- [大模型开发：从原理到工程边界](doc/agent-best-practices/00-llm-basics/README.md)
- [Prompt 与指令工程](doc/agent-best-practices/01-prompt-instruction/README.md)
- [上下文工程与 RAG](doc/agent-best-practices/02-context-rag/README.md)
- [记忆与状态管理](doc/agent-best-practices/03-memory-state/README.md)
- [工具调用、MCP 与多 Agent](doc/agent-best-practices/04-tools-agents/README.md)
- [测试、评测与验证](doc/agent-best-practices/05-evaluation-verification/README.md)
- [源码实现](doc/agent-best-practices/07-source-implementation/README.md)

## 适合谁读

- 想系统学习大模型和 Agent 工程的开发者。
- 已经会调用模型 API，但想理解底层原理和工程边界的人。
- 正在做 RAG、企业知识库、AI 助手、Coding Agent 或自动化工具链的团队。
- 想把 AI 知识从“经验和感觉”整理成 SOP、代码、评测和团队标准的人。

## 项目核心判断

大模型不是数据库，不是权限系统，不是状态机，也不是可靠执行器。它是一个强大的概率生成组件。

生产级 AI 系统要做的，不是期待模型永远发挥好，而是把模型放进清晰的工程结构里：

```text
模型负责理解和生成
RAG 负责补充外部知识
工具负责连接真实系统
状态系统负责记录确定性进度
权限系统负责控制动作边界
评测系统负责验证质量和风险
Agent 负责把这些模块组织成任务流程
```

这个项目就是围绕这条主线展开。
