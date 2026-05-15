# AI 工程最佳实践文章规划

## 1. 写作目标

这篇文章的目标是系统说明 AI 工程的最佳实践，而不是停留在提示词技巧或模型调用教程。

核心论点：

> AI 工程的本质不是调用模型，而是围绕概率智能建立一套可评测、可观测、可控、可迭代、可承担责任的工程体系。

文章面向工程师、技术负责人、AI 应用开发者和正在搭建 LLM/RAG/Agent 系统的团队。重点覆盖 AI 应用工程，不深入大模型预训练、分布式训练或底层算法实现。

## 2. 调研与写作分工

### Agent 1：公开资料调研

目标：整理 OpenAI、Anthropic、Google、Microsoft、AWS、LangChain、LlamaIndex 等公开文档中提到的 AI 工程最佳实践。

重点问题：

- 各家如何定义 Prompt、RAG、Agent、Eval、Observability、Safety？
- 哪些实践是共识？
- 哪些概念适合在文章中引用？
- 哪些文档应该作为主要参考来源？

预期产出：

- 厂商实践对比表。
- 共性原则列表。
- 可引用概念清单。
- 参考链接。

### Agent 2：第一性原理大纲

目标：从 AI 系统的本质出发，推导为什么需要这些工程实践。

重点问题：

- 为什么 AI 工程不是普通软件工程的简单延伸？
- 为什么概率输出需要 eval 和风险控制？
- 为什么上下文工程比单纯模型能力更重要？
- 为什么生产 AI 系统必须有数据闭环、观测、治理和成本控制？

预期产出：

- 文章理论主线。
- 每章要讲清楚的工程原理。
- 从原理到实践的推导链路。

### Agent 3：主流大模型平台实践调研

目标：横向比较主流大模型厂商和平台在工程实践上的公开方法论。

重点问题：

- OpenAI、Anthropic、Google Vertex AI、Microsoft Azure AI、AWS Bedrock 分别如何处理工程化问题？
- 各家对 Prompt、Tool Calling、RAG、Eval、Monitoring、Safety、Cost/Latency 的建议有什么共同点和差异？
- 哪些实践已经成为事实标准？

预期产出：

- 按工程维度整理的横向对比。
- 按厂商整理的纵向总结。
- 可用于文章论证的案例和术语。

## 3. 文章主线

文章采用三层结构：

1. 公开资料层：总结主流厂商和平台的最佳实践。
2. 第一性原理层：解释这些实践为什么成立。
3. 软件工程类比层：借鉴 C++、Go 等成熟工程体系中的原则，说明 AI 工程也需要规范、接口、测试、可维护性和团队纪律。

最重要的统一解释：

- 因为输出不确定，所以需要评测、兜底、拒答、人工确认。
- 因为上下文决定输出，所以需要 Prompt、RAG、记忆和工具链工程化。
- 因为真实场景不断变化，所以需要数据闭环。
- 因为失败链路复杂，所以需要可观测性。
- 因为自然语言可被攻击，所以需要安全边界。
- 因为推理昂贵，所以需要成本和延迟优化。
- 因为用户要完成任务，所以需要产品体验设计。
- 因为模型不可完全控制，所以需要用软件架构把它包进可控系统。

## 4. 文章大纲

### 4.1 大模型发展历史与工作原理

要讲清楚：

- 大模型不是数据库，也不是严格确定性程序，而是根据输入和上下文预测输出概率的系统。
- 从 CNN、RNN 到 Transformer 的演进，本质上是在提升模型表达局部特征、序列关系、长距离依赖和全局上下文关系的能力。
- 理解这个发展脉络，才能解释为什么 AI 工程必须做评测、上下文管理、工具验证、权限控制和反馈闭环。

发展脉络：

- **统计语言模型**：n-gram 已经体现“根据前文预测下一个词”的思想，但上下文短，表达能力有限。
- **CNN**：擅长局部特征、参数共享和并行计算，适合图像和文本局部模式，但长距离依赖能力不足。
- **RNN / LSTM / GRU**：按顺序读取 token，把历史压缩进隐藏状态，适合序列数据，但难并行，长文本信息容易丢失。
- **Attention**：让模型在处理当前位置时直接关注输入中的相关位置，缓解长距离依赖问题。
- **Transformer**：用 self-attention 建模全局关系，支持并行训练和大规模预训练，成为现代大语言模型的主干。

工作原理：

- 文本先被 tokenizer 切成 token，再转成 embedding 向量。
- 模型根据系统指令、用户输入、历史消息、检索结果和工具返回组成的上下文计算概率分布。
- 核心过程可以简化为 `P(next_token | previous_tokens)`。
- 解码时通过 temperature、top-p、top-k 等策略从概率分布中选择 token。
- 模型逐 token 生成输出，所以同一输入在不同上下文和解码参数下可能产生不同答案。

引出的工程必要性：

- 因为输出是概率性的，所以需要 eval、回归测试和线上监控。
- 因为上下文会改变概率分布，所以需要 Prompt、RAG、记忆、上下文压缩和防注入。
- 因为模型会补全高概率文本，所以需要退出路径、引用、事实验证和人工审核。
- 因为模型不能负责权限和副作用，所以工具执行必须由确定性系统控制。
- 因为真实环境持续变化，所以需要反馈闭环、灰度发布和团队规范。

### 4.2 引言：AI 工程为什么不同于普通软件工程

要讲清楚：

- 传统软件工程主要面对确定性逻辑。
- AI 系统面对的是概率输出、上下文依赖、数据驱动和持续变化。
- AI 工程的目标不是消除不确定性，而是管理不确定性。

可展开的观点：

- 普通函数更像 `input -> deterministic output`。
- LLM 更像 `context -> probability distribution -> sampled output`。
- 因此，AI 系统的正确性不能只靠单元测试判断，还要靠评测集、线上反馈和风险控制。

### 4.3 第一性原理：AI 系统是概率决策系统

要讲清楚：

- 同样的问题可能有多个合理答案。
- 模型可能生成流畅但错误的内容。
- 边界条件不是有限分支，而是语义空间、用户意图空间和上下文组合空间。

推导出的实践：

- 建立任务级评测集。
- 允许模型回答不知道。
- 对高风险场景加入人工审核。
- 对关键事实要求引用来源或通过工具验证。
- 对生产输出持续监控。

### 4.4 Prompt 与 Instruction 工程

要讲清楚：

- Prompt 不是临时文本，而是运行时策略。
- Instruction 决定角色、边界、格式、流程、异常处理和输出约束。
- 生产 Prompt 应该像代码一样被版本化、测试、审查和回滚。

最佳实践：

- 先定义成功标准，再优化 Prompt。
- 指令要具体、直接、可验证。
- 使用明确的输入分隔符和输出格式。
- 将业务 SOP、客服流程、审核规则转成模型可执行的步骤。
- 为信息不足、任务超范围、工具失败设计退出路径。
- 对 Prompt 变更跑回归评测。

可引用概念：

- OpenAI 的 Agent 基础：`Model + Tools + Instructions`。
- Microsoft/OpenAI 类实践：给模型一个退出路径，例如不知道时返回 `not found` 或明确说明信息不足。
- Anthropic 强调 Prompt 优化应建立在成功标准和经验评测之上。

### 4.5 RAG 与上下文工程

要讲清楚：

- AI 系统不是“模型 + 用户输入”，而是“模型 + 上下文构造系统”。
- 上下文包括系统提示词、用户输入、会话历史、检索结果、工具结果、业务规则和安全策略。
- 上下文质量直接决定输出质量。

最佳实践：

- 对文档进行合理切片、去重、索引和更新。
- 区分检索 chunk 和生成 chunk。
- 对召回、排序、引用和最终答案分别评测。
- 事实型任务尽量使用 grounding、citation 或工具验证。
- 长上下文要有优先级，不能简单塞满。
- 检索内容不能覆盖系统安全规则，必须防御 prompt injection。

可引用概念：

- Google 将 grounding 定义为把模型响应连接到可验证信息源以提升可信度。
- LlamaIndex 将 RAG 评测拆成 response evaluation 和 retrieval evaluation。

### 4.6 Tool Calling 与 Agent 工程

要讲清楚：

- Agent 不是越自主越好，而是要按任务复杂度选择 workflow、router、multi-agent 或 autonomous agent。
- 工具调用本质上是模型提出意图，应用侧执行确定性动作。
- 权限、执行、校验和审计不能交给模型单独决定。

最佳实践：

- 工具 schema 要清晰，参数要强类型。
- 工具描述要说明何时使用、何时不用、参数含义、返回内容和限制。
- 高风险工具调用前必须用户确认。
- 工具调用前后都要做校验。
- 工具数量过多时使用 routing、handoff 或拆分职责。
- Agent 中间轨迹要可记录、可回放、可评测。

可引用概念：

- Anthropic 区分 workflow 与 autonomous agent。
- Anthropic 的经验是成功 Agent 多依赖简单、可组合模式。
- OpenAI Agents SDK 强调工具调用前后都可以设置 guardrails。

### 4.7 Eval：AI 工程的 CI/CD 核心

要讲清楚：

- 没有评测，无法判断一次 Prompt、模型、检索、工具或策略改动是优化还是退化。
- 传统测试回答“代码有没有按预期执行”，AI eval 回答“系统在一类任务上的表现是否足够好”。

评测维度：

- 正确性。
- 相关性。
- 完整性。
- 事实一致性。
- groundedness。
- 格式遵循。
- 工具调用准确性。
- 安全合规。
- 用户体验。
- 成本和延迟。

评测方法：

- 离线固定测试集。
- 线上真实流量采样。
- 人工评审。
- 代码规则。
- LLM-as-judge。
- pairwise comparison。
- A/B 测试。
- 用户反馈。

最佳实践：

- 用生产失败样例持续扩充 eval 数据集。
- Eval 应纳入发布流程。
- 对 RAG 分开评测 retrieval 和 generation。
- 对 Agent 分开评测 final response 和 trajectory/tool-use。

### 4.8 Observability：看见 AI 行为如何形成

要讲清楚：

- AI 系统的失败通常不是单点失败，而是链路失败。
- 只记录最终回答不足以定位问题。
- Trace 是理解 Agent 行为和沉淀评测样本的事实来源。

应该观测：

- 原始用户输入。
- 构造后的 Prompt。
- 检索 query。
- 命中文档。
- 工具调用参数。
- 工具返回结果。
- 模型中间决策。
- 最终输出。
- token 用量。
- 延迟分布。
- 错误类型。
- 用户反馈。

最佳实践：

- 从第一天加入 tracing。
- 将 trace 与 eval run ID、版本号、模型快照、Prompt 版本关联。
- 对敏感信息脱敏。
- 把生产失败 trace 回流为离线 eval 数据。

可引用概念：

- LangSmith 强调 Agent 行为只有运行后才显现，trace 是理解行为的核心记录。
- Microsoft Azure AI Foundry 使用 trace/span/attributes 记录 Agent 和工具链路。

### 4.9 安全、权限与治理

要讲清楚：

- 自然语言既是用户意图，也是攻击载体。
- Prompt injection、jailbreak、数据泄露、越权工具调用都是 AI 系统特有风险。
- 模型可以参与判断，但不能成为唯一安全边界。

最佳实践：

- 权限控制由确定性系统执行。
- 外部文档不能覆盖系统规则。
- 高风险动作需要用户确认或人工审批。
- 敏感数据最小化传递并脱敏。
- 输入输出加入 moderation 或 guardrails。
- 保留审计日志。
- 用红队测试和安全 eval 覆盖攻击样例。

可引用概念：

- AWS Responsible AI Lens 强调 responsible by design。
- Microsoft Responsible AI 原则包括 fairness、reliability and safety、privacy and security、transparency、accountability。

### 4.10 成本与延迟优化

要讲清楚：

- AI 推理不是普通函数调用，而是昂贵资源。
- 每次调用都有 token 成本、推理延迟、上下文构造开销、检索开销和用户等待成本。

最佳实践：

- 先满足质量，再优化成本。
- 用小模型处理简单任务，用大模型处理复杂任务。
- 使用模型路由、缓存、prompt caching、batch、streaming。
- 裁剪上下文，避免把无关材料放入 Prompt。
- 并行化检索和工具调用。
- 对成本、延迟、失败率建立监控指标。

### 4.11 产品体验与人机协作

要讲清楚：

- 用户体验中的智能不等于模型能力，而等于用户是否能稳定完成任务。
- AI 产品需要处理用户不知道怎么问、不知道系统能力边界、不知道结果是否可信的问题。

最佳实践：

- 明确能力范围和不可用范围。
- 在不确定时主动澄清。
- 对事实回答提供来源或依据。
- 支持编辑、撤销、重试。
- 把复杂任务拆成可确认步骤。
- 让用户控制自动化程度。
- 对失败结果提供可恢复路径。

### 4.12 从 C++/Go 最佳实践看 AI 工程纪律

要讲清楚：

- 成熟语言的最佳实践并不是语法偏好，而是为了降低复杂度、提高可维护性和减少团队协作成本。
- AI 工程也需要类似的工程纪律。

C++ 可借鉴点：

- 接口清晰，隐藏复杂实现。
- 资源生命周期明确。
- 错误处理不能被忽略。
- 风格统一以提高可读性。
- 避免隐式复杂度和未定义行为。

对应到 AI 工程：

- Prompt、Tool、RAG、Eval 都要有清晰接口。
- 上下文、缓存、记忆、权限都有生命周期。
- 工具失败、检索为空、模型拒答、格式错误必须显式处理。
- Prompt 和评测标准要团队统一。
- 不要把大量隐式业务规则塞进一个无法维护的 Prompt。

Go 可借鉴点：

- 简单优先。
- 显式错误处理。
- 小接口。
- 一致格式。
- 可读性优先于技巧。

对应到 AI 工程：

- 优先 workflow，再考虑复杂 Agent。
- 每个模型调用和工具调用都要有错误路径。
- 工具接口要小而清晰。
- Prompt、eval case、trace 字段要有统一规范。
- AI 系统的可读性来自可解释链路，而不是“一个神奇 Prompt”。

### 4.13 总结：最佳实践的统一解释

总结句：

> AI 工程的成熟度，体现在把不可控的模型能力包进可控的软件系统里。

文章结尾应回到核心论点：

- AI 工程不是模型接入工作。
- AI 工程是围绕概率智能建立工程体系。
- 真正的最佳实践不是技巧清单，而是评测、观测、治理和迭代闭环。

### 4.14 Claude Code 对 Agent 工程实践的启发

要讲清楚：

- Claude Code 的定位不是普通聊天机器人，而是能读文件、跑命令、改代码、验证结果的 agentic coding environment。
- 它的核心循环可以抽象成：收集上下文、采取行动、验证结果，然后根据反馈继续迭代。
- 这个循环可以作为 Agent 工程实践的典型参考：Agent 不是一次性回答，而是围绕任务目标持续行动、检查和纠偏。

可借鉴的实践：

- 使用 `CLAUDE.md` 或类似项目说明文件，沉淀项目约定、常用命令、测试方法、代码风格和协作规则。
- 使用 Plan Mode 先做只读分析和计划，再进入执行，降低大规模改动风险。
- 使用 hooks 在工具调用前后加入检查、测试、安全拦截或审计。
- 使用 permissions 把工具能力分级，读操作、写操作、命令执行、外部副作用分别管控。
- 使用 subagents 隔离上下文和职责，让研究、实现、评审、验证分开进行。
- 使用 git worktrees 或隔离环境运行并行 Agent，避免多条任务互相污染。
- 使用 checkpoints、git diff、测试和回滚机制，把 Agent 行动纳入可恢复流程。
- 使用 CI/GitHub 集成，让 Agent 参与 PR review、测试修复、文档更新，但最终仍要有验证门槛。

文章中要强调：

- Claude Code 官方课程和文档里最值得借鉴的不是某个工具命令，而是 agentic loop、上下文管理、权限控制、验证闭环和人类可中断控制。
- 对 Agent 工程来说，“能行动”只是第一步；真正能上线的是“行动前有边界，行动中可观测，行动后可验证，失败后可恢复”。

资料边界：

- 不使用、分析或引用非授权泄露源码。
- 可引用官方文档、官方课程页面、公开工程博客，以及公开新闻中对泄露事件的安全教训总结。
- 泄露事件只作为发布工程和供应链安全案例：发布包、source map、构建产物和内部注释都需要出包前审计。

### 4.15 大模型能力边界与 Agent 管控

要讲清楚：

- 大模型擅长语言理解、代码阅读、模式归纳、计划生成、工具选择和交互式修正。
- 大模型不擅长稳定事实记忆、精确计算、严格权限判断、长期状态一致性、不可逆操作决策和无反馈长链路执行。
- Agent 工程的核心不是让模型“更自由”，而是把模型能力放进受控执行系统。

能力边界：

- **知识边界**：模型内置知识可能过期或错误，事实型任务需要 RAG、搜索、数据库或工具验证。
- **推理边界**：长链路推理会累积错误，需要拆步、检查点、反例和 verifier。
- **上下文边界**：上下文窗口有限，长任务需要摘要、记忆、检索、subagent 隔离和压缩策略。
- **行动边界**：模型可以建议调用工具，但权限、执行、幂等、回滚应由确定性系统控制。
- **安全边界**：模型容易受 prompt injection、间接注入、越权指令和上下文污染影响。
- **经济边界**：更长上下文、更多工具、更强模型会带来成本和延迟，必须度量和优化。

管控策略：

- 权限最小化：只给当前任务需要的工具和数据。
- 分级审批：低风险自动执行，高风险人工确认。
- 结构化接口：工具 schema、输出 schema、状态机和错误码。
- 双通道验证：模型自检之外，加入代码测试、规则校验、外部事实源或独立 verifier。
- 过程可观测：记录 prompt、上下文、工具调用、结果、成本、延迟和失败类型。
- 可恢复设计：checkpoint、dry-run、事务、回滚、重试和降级路径。

### 4.16 Agent 发展历史与工程范式演进

要讲清楚：

- Agent 不是突然出现的产品概念，而是从“怎么让模型回答更好”逐步演进到“怎么让概率预测机器在工程系统里稳定工作”。
- 发展主线不是单纯产品年表，而是工程关注点不断升级：Prompt、上下文、记忆、工具、角色、恢复、长时间运行、评测和观测。
- 文章要用这条演进线解释为什么今天的 Agent 最佳实践会集中在上下文、工具、记忆、权限、评测、恢复和管控上。

建议工程演进线：

- **阶段 1：Prompt 优化，解决“怎么问”**  
  早期重点是角色设定、任务描述、输出格式、few-shot 示例、步骤拆解和拒答路径。它能提升一次性回答质量，但不能解决知识缺失、长上下文、工具执行和长期状态问题。

- **阶段 2：上下文工程，解决“给它看什么”**  
  工程重点从 Prompt 文本转向运行时上下文，包括系统指令、用户输入、历史消息、检索内容、工具返回、业务规则和安全策略。RAG、chunk、rerank、引用、上下文压缩和防注入都来自这一阶段。

- **阶段 3：记忆与状态，解决“长期任务怎么连续”**  
  当任务跨会话、跨天、跨工具执行时，不能只依赖上下文窗口。需要区分短期上下文、长期记忆和业务状态，把稳定事实、用户偏好、任务进度和工具结果放进可更新、可删除、可审计的系统。

- **阶段 4：工具调用，解决“只会说，不能做”**  
  模型提出工具调用意图，应用侧负责权限、参数校验、执行、审计、幂等和回滚。搜索、数据库、代码执行、文件读写、业务 API 等能力让 Agent 接触真实环境，也带来外部副作用风险。

- **阶段 5：角色与职责管理，解决“复杂任务怎么分工”**  
  复杂任务需要 planner、researcher、executor、reviewer、verifier 等职责分离。重点不是角色越多越好，而是每个角色有清晰输入、输出、权限和验收标准。

- **阶段 6：错误恢复，解决“失败后怎么办”**  
  Agent 执行过程中，检索为空、工具超时、参数错误、权限失败、测试不通过、目标偏航都是正常路径。工程系统需要重试、澄清、降级、回滚、人工确认、重新规划和失败报告。

- **阶段 7：长时间运行，解决“怎么稳定完成长任务”**  
  长任务需要 checkpoint、trace、状态机、预算控制、heartbeat、timeout、resume 和 verifier。目标是让 Agent 在可观测、可恢复、可验证的轨道里持续推进，而不是靠一次长上下文硬撑。

可穿插的公开历史节点：

- **ReAct**：把 reasoning 和 acting 交替结合，让模型在思考、行动、观察之间循环，奠定 Agent loop 的基本形态。
- **Toolformer / Tool Use**：说明模型可以通过外部工具弥补计算、搜索、事实查询等弱点。
- **AutoGPT / BabyAGI**：推动自主 Agent 热潮，也暴露目标漂移、成本不可控、缺乏验证和长链路失控问题。
- **RAG 与 LLMOps**：推动 grounding、检索评测、prompt 版本、observability 和反馈闭环成熟。
- **多 Agent 与编排框架**：让工作流、角色分工、handoff、trace 和 verifier 成为工程重点。
- **Agentic coding 和生产 Agent**：把 Agent 放进真实工程流程，进一步强调权限、工作区隔离、测试验证、PR review、CI、trace 和回滚。

文章结论：

- Agent 发展史说明，越接近生产环境，越不能只强调自主性。
- 生产 Agent 的成熟标志不是“能自己干很多事”，而是“能让概率预测机器在明确边界内、经过验证地长期完成任务”。

## 5. 厂商实践对比

| 维度 | OpenAI | Anthropic | Google Vertex AI | Microsoft Azure AI | AWS Bedrock | LangChain/LlamaIndex |
| --- | --- | --- | --- | --- | --- | --- |
| Prompt | 强调清晰指令、版本化、eval、模型快照 | 先定义成功标准，再迭代 Prompt | Prompt Optimizer 支持数据驱动优化 | 强调 specific、descriptive、给退出路径 | 提供跨模型 Prompt engineering 指南 | Prompt 与 trace/eval 结合管理 |
| Tool/Agent | `Model + Tools + Instructions`，Agents SDK，guardrails | Workflow vs Agent，简单可组合模式 | Function calling 使用 schema，重大动作确认 | Agent evaluator 覆盖意图和工具准确性 | Agents、Flows、Knowledge Bases | LangGraph/LangSmith 支持编排和追踪 |
| RAG | Vector stores、File search、metadata filtering | Citations、search result blocks | Grounding、RAG、source links | RAG evaluators 拆分 retrieval/groundedness/relevance | Knowledge Bases、RAG evaluations | LlamaIndex 强调 production RAG |
| Eval | Evals、agent evals、pairwise/scoring/classification | Console Evaluation、经验评测 | pointwise、pairwise、工具调用指标 | 内置/自定义 eval，RAG/Agent evaluators | 模型、知识库、外部 RAG 评测 | 离线 eval、在线 eval、LLM-as-judge |
| Observability | traces、usage、Agents SDK | 厂商侧偏 prompt/eval，平台补齐观测 | Vertex evaluation 和 agent monitoring | tracing、span、Azure Monitor | CloudWatch、CloudTrail、Bedrock metrics | LangSmith tracing 是核心能力 |
| Safety | moderation、guardrails、红队、HITL | 减少幻觉、引用、人工验证 | grounding、安全策略 | Responsible AI、安全评测、默认策略 | Guardrails、防 prompt attack | 依赖平台和自定义 guardrails |
| Cost/Latency | streaming、batch、prompt caching、小模型、并行 | prompt caching、batch、模型选择 | 控制工具数量和上下文 | 资源级成本估算和预算趋势 | provisioned throughput、prompt routing | 通过 trace 找瓶颈和冗余调用 |

## 6. 50 条 AI 工程经验清单

这一节作为文章正文的素材库。每条经验都应尽量写成“问题 -> 可优化点 -> 验证方式”的结构，避免只给抽象原则。

### 6.1 提示词与 Instruction

1. **先定义成功标准，再写 Prompt**  
   优化点：把“回答得好”拆成准确性、完整性、格式、语气、引用、安全等指标。验证方式：用固定 eval 集对 Prompt 版本做回归。

2. **把 Prompt 当作代码管理**  
   优化点：版本化、变更记录、评审、回滚、灰度。验证方式：每次 Prompt 变更都跑同一批样例，比较通过率和失败类型。

3. **把业务 SOP 转成可执行步骤**  
   优化点：不要只写角色设定，要写操作顺序、判断条件、异常分支。验证方式：用真实业务 case 检查模型是否按步骤行动。

4. **给模型明确退出路径**  
   优化点：信息不足时允许回答“不知道”“需要更多信息”“无法验证”。验证方式：构造缺失信息样例，检查模型是否减少幻觉。

5. **输出格式要机器可校验**  
   优化点：JSON schema、枚举值、固定字段、长度限制。验证方式：用解析器和 schema validation 自动检查输出。

6. **分隔指令、上下文和用户输入**  
   优化点：减少上下文污染和 prompt injection 风险。验证方式：加入恶意用户输入，检查是否覆盖系统规则。

7. **少量高质量示例优于大量松散示例**  
   优化点：示例覆盖典型、边界、拒答、工具失败场景。验证方式：比较 zero-shot、few-shot、错误示例修正后的指标。

8. **为不同任务拆分 Prompt，而不是一个 Prompt 包打天下**  
   优化点：意图识别、检索改写、总结、工具调用、最终回答分别设计。验证方式：逐组件 eval，定位是哪一段 Prompt 退化。

### 6.2 上下文工程与 RAG

9. **上下文是运行时数据层，不是越多越好**  
   优化点：控制上下文优先级、长度、来源和时效性。验证方式：比较不同上下文窗口下的准确率、延迟、成本。

10. **检索质量和生成质量分开优化**  
    优化点：分别评估 recall、precision、groundedness、answer relevance。验证方式：先看 top-k 文档是否命中，再看答案是否忠实。

11. **chunk 策略要服务任务，而不是固定大小切片**  
    优化点：按标题、段落、代码块、表格、业务对象切片。验证方式：观察答案引用是否跨 chunk 丢失关键信息。

12. **检索 chunk 和生成 chunk 可以不同**  
    优化点：小 chunk 用于召回，大 chunk 用于生成上下文。验证方式：比较命中率、答案完整度和 token 成本。

13. **为 RAG 加引用和证据约束**  
    优化点：要求回答绑定来源、段落或文档 ID。验证方式：抽样检查答案中的关键事实是否能在来源中找到。

14. **检索为空要有明确策略**  
    优化点：澄清问题、扩大检索、降级到通用回答、拒答。验证方式：构造知识库不存在的问题，检查是否编造。

15. **上下文要防注入**  
    优化点：外部文档内容不能覆盖系统指令和权限规则。验证方式：在文档中放置恶意指令，检查模型是否执行。

16. **对上下文做去重和压缩**  
    优化点：减少重复片段、低相关片段和模板噪声。验证方式：比较 token 成本、延迟和答案质量。

17. **长上下文要有摘要层和索引层**  
    优化点：把历史、文档、工具结果分层组织。验证方式：长任务中检查关键事实是否被保留，旧噪声是否被排除。

18. **上下文构造过程必须可观测**  
    优化点：记录 query、top-k、rerank 分数、最终注入片段。验证方式：失败 case 可以回放完整上下文链路。

### 6.3 记忆与状态管理

19. **区分短期上下文、长期记忆和业务状态**  
    优化点：会话历史、运行摘要、用户偏好、结构化记忆、任务进度、数据库状态分开存储；长时间运行 Agent 用滑动窗口、摘要、检索记忆和确定性状态分层协作。验证方式：检查跨会话任务是否既连续又不污染，长会话回放是否能控制 token、恢复任务并找回旧细节。

20. **记忆必须有写入规则**  
    优化点：不是所有对话都进入长期记忆，只写稳定偏好和明确事实。验证方式：抽查记忆库，计算无效、错误、过期记忆比例。

21. **记忆必须可更新和删除**  
    优化点：用户纠正、撤销授权、隐私删除要能生效。验证方式：修改记忆后重新问同类问题，检查是否使用新信息。

22. **记忆要带来源和时间戳**  
    优化点：记录由谁提供、何时产生、置信度如何。验证方式：冲突信息出现时能选择更新、更可信的记忆。

23. **敏感信息不要默认进入长期记忆**  
    优化点：对隐私、密钥、身份信息、商业数据做最小化存储。验证方式：安全测试检查敏感信息是否被记住或泄露。

24. **任务状态用确定性系统管理**  
    优化点：流程进度、审批状态、工具结果不要只放在自然语言上下文里。验证方式：中断恢复后检查状态是否一致。

### 6.4 工具调用与 Agent

25. **工具接口要小而清晰**  
    优化点：一个工具只做一类动作，参数强类型，返回结构稳定。验证方式：统计工具调用参数错误率和失败率。

26. **工具描述要写清何时不用**  
    优化点：避免模型过度调用工具或错用工具。验证方式：加入不需要工具的样例，检查无效调用比例。

27. **模型只提出调用意图，应用负责执行权限**  
    优化点：权限、审计、幂等、重试、事务由确定性代码控制。验证方式：越权样例不能被模型绕过。

28. **高风险动作必须确认**  
    优化点：发邮件、付款、删除、发布、改配置等动作加入人工确认。验证方式：模拟误触发和恶意指令，检查是否被拦截。

29. **工具失败是正常路径，不是异常边缘情况**  
    优化点：超时、空结果、权限失败、部分成功都要设计响应。验证方式：注入工具错误，检查 Agent 是否能恢复或降级。

30. **优先 workflow，再升级 Agent**  
    优化点：固定流程、长文本多轮任务、RAG/MCP/Skill/Tool 多模块协作先设计成 workflow；模型只放在需要理解、生成或动态判断的节点。验证方式：比较 workflow 与 autonomous agent 的稳定性、成本和可解释性，检查分块、状态、observation、熔断、权限和结单是否可回放。

31. **多 Agent 要有明确职责边界**  
    优化点：planner、researcher、coder、reviewer、verifier 等职责不能重叠过多。验证方式：检查任务轨迹中是否出现循环、重复劳动、互相覆盖。

32. **多 Agent 的核心是测试和验证，而不是角色数量**  
    优化点：每个 Agent 的输出都要有验收标准，下游 Agent 不盲信上游结论。验证方式：加入 verifier/reviewer，对事实、代码、工具结果做独立检查。

33. **Agent handoff 要传结构化上下文**  
    优化点：传任务目标、已完成步骤、证据、约束、待验证问题，而不是整段聊天历史。验证方式：检查接手 Agent 是否能独立复现判断。

34. **Agent 轨迹要可回放**  
    优化点：记录每一步思路摘要、工具输入输出、决策依据和版本信息。验证方式：失败任务能定位到具体错误步骤。

**专题：大规模 Skill 工程实现**
    优化点：不要把上百个 Skill 全量塞进 System Prompt；按广度、深度、快慢拆解，通过 Intent Gateway、小模型路由、Skill Registry / Skill RAG、深度检索、JSON manifest 降噪、动态 Prompt 组装、分身 Agent、结果缓存、工具结果缓存和高频 Skill 内化实现按需加载与降本提速。验证方式：检查小模型路由质量、动态组装质量、Skill Top-K 命中率、误加载率、工具误调用率、缓存有效性、内化收益、token 成本、首字延迟和 trace 可回放。

### 6.5 测试、评测与验证

35. **AI 系统需要测试金字塔的扩展版**  
    优化点：单元测试、组件 eval、端到端 eval、线上监控同时存在。验证方式：每层测试都能捕获不同类型问题。

36. **Eval 数据集要覆盖真实分布和边界样例**  
    优化点：包括典型问题、长尾问题、恶意输入、缺失信息、工具失败。验证方式：线上失败样例持续回流到 eval。

37. **不要只测最终答案，也要测中间过程**  
    优化点：RAG 测检索，Agent 测工具轨迹，Prompt 测格式遵循。验证方式：把 final response eval 和 trajectory eval 分开统计。

38. **LLM-as-judge 需要校准**  
    优化点：用人工标注样本校准 judge prompt、模型和评分标准。验证方式：计算 judge 与人工的一致性。

39. **评测指标要和业务风险绑定**  
    优化点：客服、医疗、金融、代码生成、办公自动化的错误成本不同。验证方式：按风险等级设置不同通过阈值。

40. **Prompt、模型、知识库、工具变更都要跑回归**  
    优化点：任何影响输出的变更都进入 release gate。验证方式：发布前比较 baseline 与 candidate。

41. **验证要包含反例和攻击样例**  
    优化点：测试 hallucination、prompt injection、越权、敏感信息泄露。验证方式：安全 eval 作为上线门槛。

42. **把失败分类，而不是只记录失败率**  
    优化点：区分检索失败、理解失败、工具失败、格式失败、安全失败。验证方式：每类失败都有 owner 和优化路径。

### 6.6 反馈闭环与实践迭代

43. **生产反馈要进入工程闭环**  
    优化点：用户反馈、人工审核、trace、投诉、重试都变成改进信号。验证方式：每周统计失败样例进入 eval 的比例。

44. **建立从失败到改进的闭环流程**  
    优化点：发现问题、归因、修复、回归、灰度、监控。验证方式：每个高频失败类型都有关闭记录。

45. **反馈不等于直接训练模型**  
    优化点：先判断问题应由 Prompt、RAG、工具、产品、数据还是模型解决。验证方式：每次修复记录根因和选择的优化层。

46. **人工审核要服务评测标准沉淀**  
    优化点：让审核员不只打好坏，还标注原因、证据、风险级别。验证方式：审核标签可直接转成 eval case 或 judge rubric。

47. **线上指标要同时看质量、成本、延迟和安全**  
    优化点：不要用单一满意度指标掩盖高成本或高风险。验证方式：dashboard 同时展示 pass rate、latency、token、error、安全拦截。

48. **灰度发布比一次性切换更适合 AI 系统**  
    优化点：Prompt、模型、知识库、Agent 策略逐步放量。验证方式：灰度组和对照组的质量、投诉、成本对比。

49. **可解释的失败比偶然成功更有价值**  
    优化点：宁可系统暴露不确定和原因，也不要让模型自信编造。验证方式：检查失败响应是否包含可恢复下一步。

50. **最佳实践最终要固化成团队规范**  
    优化点：Prompt 模板、工具 schema、eval 标准、trace 字段、安全规则、发布流程形成文档和检查清单。验证方式：新人能按规范独立完成一个可上线 AI 功能。

## 7. 参考来源

### AI 工程与 Agent

- OpenAI: A practical guide to building agents  
  https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- OpenAI: Agents SDK  
  https://platform.openai.com/docs/guides/agents-sdk/
- Anthropic: Building effective agents  
  https://www.anthropic.com/research/building-effective-agents
- Google Cloud: Choose your agentic AI architecture components  
  https://cloud.google.com/architecture/choose-agentic-ai-architecture-components

### Prompt Engineering

- OpenAI: Prompt engineering  
  https://platform.openai.com/docs/guides/prompt-engineering/
- Anthropic: Prompt engineering overview  
  https://docs.anthropic.com/en/docs/prompt-engineering
- Microsoft Azure OpenAI: Prompt engineering  
  https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/prompt-engineering
- AWS Bedrock: Prompt engineering guidelines  
  https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering-guidelines.html

### Eval

- OpenAI: Evaluation best practices  
  https://platform.openai.com/docs/guides/evaluation-best-practices
- OpenAI: Agent evals  
  https://platform.openai.com/docs/guides/agent-evals
- Anthropic: Evaluation tool  
  https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool
- Google Vertex AI: Gen AI evaluation overview  
  https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview
- Google Vertex AI: Evaluate Gen AI agents  
  https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents
- AWS Bedrock: Model evaluation  
  https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html
- LangSmith: Evaluation concepts  
  https://docs.langchain.com/langsmith/evaluation-concepts

### RAG 与上下文

- Google Vertex AI: Grounding overview  
  https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview
- Google Vertex AI: Ground responses using RAG  
  https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/ground-responses-using-rag
- LlamaIndex: Production RAG  
  https://docs.llamaindex.ai/en/stable/optimizing/production_rag/
- LlamaIndex: Evaluating  
  https://docs.llamaindex.ai/en/stable/module_guides/evaluating/

### Observability

- Microsoft Azure AI Foundry: Observability  
  https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/observability
- Microsoft Azure AI Foundry: Trace and observe AI Agents  
  https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/tracing
- LangSmith: Observability  
  https://docs.langchain.com/langsmith/observability
- LlamaIndex: Observability  
  https://docs.llamaindex.ai/en/stable/module_guides/observability/

### Safety 与 Responsible AI

- Microsoft: Responsible AI principles  
  https://www.microsoft.com/en-us/ai/principles-and-approach/
- AWS Well-Architected: Responsible AI Lens design principles  
  https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/design-principles.html
- AWS Bedrock: Guardrails  
  https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-how.html
- AWS Bedrock: Prompt attack detection  
  https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html

### 成本与延迟

- OpenAI: Latency optimization  
  https://platform.openai.com/docs/guides/latency-optimization
- OpenAI: Cost optimization  
  https://platform.openai.com/docs/guides/cost-optimization
- OpenAI: Prompt caching  
  https://platform.openai.com/docs/guides/prompt-caching
- Anthropic: Reducing latency  
  https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-latency
- AWS Bedrock: Agent performance optimization  
  https://docs.aws.amazon.com/bedrock/latest/userguide/agents-optimize-performance.html

### 软件工程最佳实践类比

- C++ Core Guidelines  
  https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines
- Google C++ Style Guide  
  https://google.github.io/styleguide/cppguide.html
- Effective Go  
  https://go.dev/doc/effective_go
- Go Code Review Comments  
  https://go.dev/wiki/CodeReviewComments

## 8. 后续写作任务拆分

### 第一阶段：完成文章初稿

- 按第 4 节大纲写完整正文。
- 每章保持结构一致：问题、原理、实践、例子。
- 每个关键观点至少关联一个公开资料来源或工程类比。

### 第二阶段：补充工程案例

建议加入 3 类案例：

- RAG 问答系统：如何从“能回答”演进到“可信、可测、可观测”。
- Agent 工具调用：如何处理权限、确认、失败、审计。
- Prompt 变更回归：为什么 Prompt 改动也要进入 CI/eval。

### 第三阶段：形成最佳实践清单

文章末尾可以附一份 checklist：

- 是否定义成功标准？
- 是否有离线 eval？
- 是否记录 trace？
- 是否对 Prompt 和工具版本化？
- 是否有 RAG 检索评测？
- 是否有上下文构造记录和回放能力？
- 是否区分短期上下文、长期记忆和业务状态？
- 是否有安全 guardrails？
- 是否有多 Agent 的独立 verifier/reviewer？
- 是否对 Agent 轨迹和工具调用做验证？
- 是否有成本和延迟指标？
- 是否有失败样例回流机制？

### 第四阶段：审稿与收敛

- 检查是否过度依赖厂商术语。
- 确保每个实践都能从原理推导出来。
- 删除无法落地的抽象表述。
- 给每章加一个可执行结论。

## 9. 默认写作风格

- 使用工程师能接受的实用语气。
- 少写口号，多写因果关系。
- 原理讲清楚，实践要能落地。
- 避免把 AI 工程写成“提示词技巧合集”。
- 避免把厂商文档堆砌成资料汇总。
- 重点突出工程闭环：定义目标、构建系统、评测、观测、安全、迭代。

## 10. 附录：AI 工程与 Agent 最佳实践链接索引

本附录用于集中存放现有公开资料链接。后续写正文时，正文只保留必要引用，完整材料索引放在这里。链接按资料类型分组，优先收录官方文档、平台方法论、工程实践文章和 GitHub 仓库。

### 10.1 官方与平台方法论

| 主题 | 链接 | 可用于文章的重点 |
| --- | --- | --- |
| OpenAI Agent 构建指南 | https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/ | Agent 的核心组成、指令、工具、流程拆分 |
| OpenAI Evaluation Best Practices | https://platform.openai.com/docs/guides/evaluation-best-practices | 非确定性系统如何做 eval、数据集和指标 |
| OpenAI Agent Evals | https://platform.openai.com/docs/guides/agent-evals | Agent 质量、trace grading、datasets |
| OpenAI Prompt Engineering | https://platform.openai.com/docs/guides/prompt-engineering/ | Prompt 可靠性、结构化输出、约束 |
| OpenAI Function Calling | https://platform.openai.com/docs/guides/function-calling | 工具调用 schema、strict mode、应用侧执行 |
| OpenAI Retrieval / File Search | https://platform.openai.com/docs/guides/retrieval | 托管检索、向量库、RAG 实现 |
| OpenAI Latency Optimization | https://platform.openai.com/docs/guides/latency-optimization | 延迟优化、并行、streaming |
| OpenAI Cost Optimization | https://platform.openai.com/docs/guides/cost-optimization | 成本优化、模型选择、token 控制 |
| Anthropic Building Effective Agents | https://www.anthropic.com/research/building-effective-agents | workflow vs agent、简单可组合模式 |
| Anthropic Claude Code Overview | https://docs.anthropic.com/en/docs/claude-code/overview | agentic coding tool、终端工作流、MCP、CI |
| Claude Code Best Practices | https://code.claude.com/docs/en/best-practices | 上下文窗口、Plan Mode、并行会话、验证 |
| Claude Code: Best practices for agentic coding | https://www.anthropic.com/engineering/claude-code-best-practices | `CLAUDE.md`、探索-计划-编码-提交、测试验证 |
| Claude Code: How Claude Code works | https://code.claude.com/docs/en/how-claude-code-works | agentic loop、工具、上下文、权限、checkpoint |
| Claude Code Common Workflows | https://code.claude.com/docs/en/common-workflows | 探索代码、修 bug、测试、PR、worktrees、CI |
| Claude Code Memory | https://code.claude.com/docs/en/memory | `CLAUDE.md`、auto memory、规则作用域 |
| Claude Code Permissions | https://code.claude.com/docs/en/permissions | 权限模式、allow/deny、组织策略 |
| Claude Code Hooks | https://code.claude.com/docs/en/hooks | PreToolUse、PostToolUse、agent hooks、自动化检查 |
| Claude Code Subagents | https://code.claude.com/docs/en/sub-agents | context isolation、工具限制、并行任务、专用 agent |
| Anthropic Prompt Engineering | https://docs.anthropic.com/en/docs/prompt-engineering | 成功标准、经验评测、Prompt 迭代 |
| Anthropic Tool Use | https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use | 工具描述、参数、何时使用工具 |
| Anthropic Reduce Hallucinations | https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | 拒答、引用、事实验证 |
| Anthropic Evaluation Tool | https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool | 测试集、版本对比、质量评分 |
| Google Agentic Architecture Components | https://cloud.google.com/architecture/choose-agentic-ai-architecture-components | Agent 架构组件、迭代选型 |
| Google Vertex AI Evaluation Overview | https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview | pointwise/pairwise、自定义指标 |
| Google Vertex AI Agent Evaluation | https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents | final response 与 trajectory 评测 |
| Google Vertex AI Function Calling | https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling | 工具 schema、低温、工具数量控制 |
| Google Vertex AI Grounding | https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview | grounding、source links、可信输出 |
| Microsoft AI Agents in Production | https://microsoft.github.io/ai-agents-for-beginners/10-ai-agents-production/ | 生产 Agent 的 observability、eval、成本 |
| Microsoft Azure AI Observability | https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/observability | 评测、监控、tracing 的统一框架 |
| Microsoft Azure AI Agent Tracing | https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/tracing | trace/span/attributes、Agent 链路 |
| Microsoft RAG Evaluators | https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/rag-evaluators | retrieval、groundedness、relevance |
| Microsoft Agent Evaluators | https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators | intent、tool call、task adherence |
| Microsoft Responsible AI | https://www.microsoft.com/en-us/ai/principles-and-approach/ | fairness、safety、privacy、transparency、accountability |
| AWS Well-Architected Generative AI Lens | https://aws.amazon.com/blogs/architecture/announcing-the-aws-well-architected-generative-ai-lens/ | GenAI 工作负载六大支柱和生命周期 |
| AWS Bedrock Prompt Engineering | https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering-guidelines.html | 跨模型 Prompt 工程建议 |
| AWS Bedrock Evaluation | https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html | 模型、知识库、RAG 评测 |
| AWS Bedrock Guardrails | https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-how.html | 输入输出安全策略 |
| AWS Bedrock Prompt Attack Detection | https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html | prompt injection、jailbreak、prompt leakage |
| AWS Bedrock Monitoring | https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring.html | CloudWatch、token、latency、error、throttle |
| LangChain Agent Observability Powers Evaluation | https://www.langchain.com/conceptual-guides/agent-observability-powers-agent-evaluation | trace 如何驱动 Agent 评测 |
| LangChain Production Monitoring | https://www.langchain.com/blog/production-monitoring | 生产 Agent 监控、质量、成本、trace |
| LangSmith Evaluation | https://docs.langchain.com/langsmith/evaluation | 离线 eval、在线 eval、human/LLM/code evaluator |
| LangSmith Observability | https://docs.langchain.com/langsmith/observability | tracing、datasets、monitoring |
| LlamaIndex Production RAG | https://docs.llamaindex.ai/en/stable/optimizing/production_rag/ | 生产 RAG 的鲁棒性、性能、规模 |
| LlamaIndex Evaluating | https://docs.llamaindex.ai/en/stable/module_guides/evaluating/ | response evaluation、retrieval evaluation |
| LlamaIndex Observability | https://docs.llamaindex.ai/en/stable/module_guides/observability/ | LLM/prompt、index/query trace |

### 10.2 工程实践文章与课程

| 主题 | 链接 | 可用于文章的重点 |
| --- | --- | --- |
| Coursera: Claude Code in Action | https://www.coursera.org/learn/claude-code-in-action | 官方课程，context management、tool calling、MCP、GitHub、hooks |
| Class Central: Claude Code in Action | https://www.classcentral.com/course/anthropic-academy-claude-code-in-action-536160 | 课程概要、模块结构、免费证书信息 |
| USC Career Center: Claude Code in Action by Anthropic | https://careers.usc.edu/classes/claude-code-in-action-by-anthropic/ | 课程覆盖架构、上下文管理、MCP、GitHub、planning modes |
| Braintrust: LLM Observability Guide | https://www.braintrust.dev/articles/llm-observability-guide | LLM observability、tracing、eval、monitoring |
| Hugging Face: AI Agent Observability and Evaluation | https://huggingface.co/learn/agents-course/bonus-unit2/what-is-agent-observability-and-evaluation | Agent 观测、离线/在线评测、质量指标 |
| Microsoft: AI Agents in Production | https://microsoft.github.io/ai-agents-for-beginners/10-ai-agents-production/ | 从黑盒 Agent 到可管理系统 |
| LangChain: Production Monitoring | https://www.langchain.com/blog/production-monitoring | 生产 Agent 如何监控质量和行为 |
| LangChain: Agent Observability Powers Agent Evaluation | https://www.langchain.com/conceptual-guides/agent-observability-powers-agent-evaluation | Agent trace 是 eval 的基础 |
| Agent Patterns: Observability for AI Agents | https://www.agentpatterns.tech/en/observability-monitoring/observability-overview | tracing、logging、metrics、常见错误 |
| Hugging Face Blog: Observability in Agentic AI | https://huggingface.co/blog/royswastik/evaluating-agentic-ai-systems-part-3-observability | Agentic AI 可观测栈、OpenTelemetry |
| Maxim AI: Agent Observability Guide | https://www.getmaxim.ai/articles/agent-observability-the-definitive-guide-to-monitoring-evaluating-and-perfecting-production-grade-ai-agents/ | prompts、tool calls、model outputs、human feedback |
| N-iX: AI Agent Observability | https://www.n-ix.com/ai-agent-observability/ | 企业 AI Agent 观测纪律 |
| Zylos: AI Agent Deployment Strategies | https://zylos.ai/research/2026-03-05-ai-agent-deployment-strategies-containerization-scaling | 容器化、扩缩容、零停机、生产指标 |
| Agentmelt: AI Agent Observability | https://agentmelt.com/blog/ai-agent-observability-monitoring/ | 生产 Agent latency、cost、hallucination、prompt drift |
| Mezmo: AI Agent Observability Standards | https://www.mezmo.com/learn-observability/ai-agent-observability-standards-best-practices | 调试、准确性、成本维度的观测 |
| The Verge: Claude Code leak reporting | https://www.theverge.com/ai-artificial-intelligence/904776/anthropic-claude-source-code-leak | 只作为发布安全和构建产物审计案例，不引用泄露代码 |
| The Guardian: Claude Code leak reporting | https://www.theguardian.com/technology/2026/apr/01/anthropic-claudes-code-leaks-ai | 只作为供应链/发布流程风险案例 |

### 10.3 Agent 发展历史与论文

| 主题 | 链接 | 可用于文章的重点 |
| --- | --- | --- |
| ReAct: Synergizing Reasoning and Acting in Language Models | https://huggingface.co/papers/2210.03629 | reasoning + acting 交替循环，Agent loop 早期范式 |
| Toolformer: Language Models Can Teach Themselves to Use Tools | https://ai.meta.com/research/publications/toolformer-language-models-can-teach-themselves-to-use-tools/ | 模型使用外部 API 弥补能力边界 |
| AutoGPT | https://github.com/Significant-Gravitas/AutoGPT | 早期自主 Agent 热潮，暴露长期自主执行和成本问题 |
| BabyAGI | https://github.com/yoheinakajima/babyagi | 任务拆解、任务队列、简单自主循环 |
| Voyager | https://voyager.minedojo.org/ | 具身/环境反馈式 Agent，持续技能学习 |
| Generative Agents | https://arxiv.org/abs/2304.03442 | 记忆、反思、计划对 Agent 行为的影响 |

### 10.4 GitHub：官方示例、Cookbook 与课程

| 仓库 | 链接 | 可用于文章的重点 |
| --- | --- | --- |
| OpenAI Cookbook | https://github.com/openai/openai-cookbook | OpenAI API、agents、evals、RAG、实践 notebook |
| Anthropic Claude Cookbooks | https://github.com/anthropics/anthropic-cookbook | Claude tool use、agent SDK、提示词与能力示例 |
| Google ADK Python | https://github.com/google/adk-python | code-first Agent 框架、eval、debug、deploy |
| Google ADK Samples | https://github.com/google/adk-samples | 多语言 ADK 示例、multi-agent 工作流 |
| Google ADK Docs | https://github.com/google/adk-docs | ADK 文档源码、Agent 工程化说明 |
| Google ADK Go | https://github.com/google/adk-go | Go 版本 ADK，适合对比 Go 工程实践 |
| Google ADK Java | https://github.com/google/adk-java | Java 版本 ADK，强调强类型和部署 |
| Microsoft AI Agents for Beginners | https://github.com/microsoft/ai-agents-for-beginners | Agent 课程、生产观测、评测、trustworthy agents |
| AWS Open Source Bedrock Agent Evaluation | https://github.com/aws-samples/open-source-bedrock-agent-evaluation | Bedrock Agent 评测、Langfuse observability、RAG/Text2SQL |
| AWS Amazon Bedrock RAG | https://github.com/aws-samples/amazon-bedrock-rag | Bedrock Knowledge Bases RAG 示例 |
| AWS RAG Evaluation | https://github.com/aws-samples/rag-evaluation | RAGAS、chunk 策略、模型对比实验 |
| LangChain | https://github.com/langchain-ai/langchain | LLM 应用与 Agent 编排基础库 |
| LangGraph | https://github.com/langchain-ai/langgraph | 状态化、多步骤、可恢复 Agent 工作流 |
| LangSmith SDK | https://github.com/langchain-ai/langsmith-sdk | tracing、eval、datasets、monitoring 接入 |
| LlamaIndex | https://github.com/run-llama/llama_index | RAG、数据连接、检索、评测与观测 |

### 10.5 GitHub：评测、观测与 AgentOps 工具

| 仓库 | 链接 | 可用于文章的重点 |
| --- | --- | --- |
| Arize Phoenix | https://github.com/Arize-ai/phoenix | AI observability、eval、RAG/Agent trace |
| TruLens | https://github.com/truera/trulens | LLM/Agent evaluation and tracking |
| Langfuse | https://github.com/langfuse/langfuse | 开源 LLM observability、tracing、eval、prompt management |
| Helicone | https://github.com/Helicone/helicone | LLM observability、cost tracking、caching |
| Giskard OSS | https://github.com/Giskard-AI/giskard | LLM/Agent 测试、安全、红队、RAG eval |
| Ragas | https://github.com/explodinggradients/ragas | RAG evaluation 指标和测试集 |
| DeepEval | https://github.com/confident-ai/deepeval | LLM evaluation、unit test 风格 eval |
| Promptfoo | https://github.com/promptfoo/promptfoo | Prompt / model / RAG 测试和红队 |
| OpenLLMetry | https://github.com/traceloop/openllmetry | OpenTelemetry instrumentation for LLM apps |
| agentevals | https://github.com/agentevals-dev/agentevals | 基于 OpenTelemetry trace 的 Agent 评测 |
| Coze Loop | https://github.com/coze-dev/coze-loop | Agent 开发、调试、评测、监控全生命周期 |
| Laminar | https://github.com/lmnr-ai/lmnr | 开源 AI observability、eval、datasets |

### 10.6 GitHub：Awesome Lists 与资料合集

| 仓库 | 链接 | 可用于文章的重点 |
| --- | --- | --- |
| Awesome AI Agents 2026 | https://github.com/Supersynergy/awesome-ai-agents-2025 | Agent 框架、memory、observability、security、RAG |
| Awesome Agents | https://github.com/kyrolabs/awesome-agents | Agent 工具、测试、评测、observability |
| Awesome AI Agents | https://github.com/Deep-Insight-Labs/awesome-ai-agents | Agent 框架、observability、tracing |
| Awesome List of AI Agents | https://github.com/slavakurilyak/awesome-ai-agents | Agent 项目与资源集合 |
| Awesome AI Eval | https://github.com/Vvkmnn/awesome-ai-eval | AI 可靠性、RAG、Agent eval、red teaming |
| Awesome Context Engineering | https://github.com/yzfly/awesome-context-engineering | 上下文工程、Agent context、MCP、最佳实践 |
| Awesome RAG Production | https://github.com/Yigtwxx/Awesome-RAG-Production | 生产级 RAG 工具、评测、观测、安全 |
| Awesome RAG | https://github.com/coree/awesome-rag | RAG 论文、教程、工具集合 |
| LLM Engineer's Handbook | https://github.com/PacktPublishing/LLM-Engineers-Handbook | LLMOps、RAG、部署、监控、测试评测 |

### 10.7 后续筛选规则

- 正文优先引用官方文档和平台方法论。
- 工程实践文章用于补充“为什么生产环境需要观测、评测和反馈闭环”。
- GitHub 仓库优先选有代码、示例、评测或观测能力的项目。
- Awesome List 只作为资料入口，不直接作为核心论据。
- 不使用、复述、分析或链接非授权泄露源码；泄露事件最多作为发布安全和供应链风险案例。
- 对具体工具的 star 数、版本、维护状态不要写死在正文里，除非写作当天重新核验。
