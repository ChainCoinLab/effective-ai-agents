# Summary

* [00. 总览：AI 工程知识结构](README.md)
* [00.1 中文速览](guide.zh.md)

## 一、大模型基础与工程边界

* [00. 本章导读：大模型开发：从原理到工程边界](00-llm-basics/README.md)

机器学习基础：

* [01. 大模型发展历史](00-llm-basics/01-llm-history.md)
* [02. 从函数到机器学习](00-llm-basics/02-function-to-machine-learning.md)
* [03. 从线性模型到神经网络](00-llm-basics/03-linear-to-neural-network.md)
* [04. 前向传播、损失函数与反向传播](00-llm-basics/04-forward-loss-backprop.md)
* [05. 梯度下降与模型训练](00-llm-basics/05-gradient-descent-training.md)
* [06. 拟合、泛化与过拟合](00-llm-basics/06-fitting-generalization-overfitting.md)

表示与架构：

* [07. 从现实世界到向量表示](00-llm-basics/07-real-world-to-vectors.md)
* [08. 从文字到 token 和 embedding](00-llm-basics/08-token-and-embedding.md)
* [09. 语言模型为什么预测下一个 token](00-llm-basics/09-next-token-prediction.md)
* [10. 为什么预测下一个 token 会产生能力](00-llm-basics/10-capability-from-prediction.md)
* [11. 从上下文问题到 Attention](00-llm-basics/11-attention-from-context.md)
* [12. Transformer 如何一步步形成](00-llm-basics/12-transformer-architecture.md)

代码实现补充：

* [代码实现：token id 到 embedding 向量矩阵](07-source-implementation/llm-from-zero/01-token-embedding-matrix.md)

训练、推理、评测和边界：

* [13. 预训练、指令微调与对齐](00-llm-basics/13-training-and-alignment.md)
* [14. 推理机制与生成参数](00-llm-basics/14-inference-and-parameters.md)
* [15. 模型评测与工程验证](00-llm-basics/15-evaluation.md)
* [16. 大模型能做什么，不能做什么](00-llm-basics/16-llm-capabilities-boundaries.md)

## 二、Agent 开发

上一部分说明了大模型擅长理解、归纳和生成，但不能独自承担事实、状态、权限、执行和审计。Agent 开发部分继续学习这些缺口如何由 Prompt、RAG、记忆、状态、工具、MCP、评测和工程流程补齐，并组织成可推进、可验证、可恢复的任务闭环。

* [01. Agent 原理](00-llm-basics/agent-principles.md)
* [02. Agent 发展历史](00-llm-basics/agent-history.md)
* [03. Prompt 与指令工程](01-prompt-instruction/README.md)
* [04. 上下文工程与 RAG](02-context-rag/README.md)
* [05. 记忆与状态管理](03-memory-state/README.md)
* [06. 工具调用与 MCP](04-tools-agents/README.md)
* [07. Agent 工程化](04-tools-agents/agent-engineering.md)
* [08. 测评与反馈闭环](05-evaluation-verification/README.md)
* [09. 生产反馈与迭代](06-feedback-iteration/README.md)

## 三、源码实现

* [00. 本模块导读](07-source-implementation/README.md)
* [01. 从零实现大模型核心组件](07-source-implementation/llm-from-zero/README.md)
  * [01. token id 如何查出 embedding 向量矩阵](07-source-implementation/llm-from-zero/01-token-embedding-matrix.md)
* [02. 从零使用 Go 语言开发一个 Agent](07-source-implementation/go-agent-from-zero/README.md)
  * [01. 调用 API 实现最小 Agent](07-source-implementation/go-agent-from-zero/01-api-call.md)
  * [02. 扩展成命令行循环](07-source-implementation/go-agent-from-zero/02-cli-loop.md)
  * [03. 保存多轮对话上下文](07-source-implementation/go-agent-from-zero/03-multi-turn-context.md)
  * [04. 把阻塞 JSON 响应改成流式输出](07-source-implementation/go-agent-from-zero/04-streaming-output.md)
  * [05. 增加 tool use](07-source-implementation/go-agent-from-zero/05-tool-use.md)
  * [06. ReAct Agent](07-source-implementation/go-agent-from-zero/06-react-loop.md)
  * [07. 支持多个工具](07-source-implementation/go-agent-from-zero/07-multi-tools.md)
  * [08. 给高风险工具加确认](07-source-implementation/go-agent-from-zero/08-tool-confirmation.md)
  * [09. 接入 MCP Server](07-source-implementation/go-agent-from-zero/09-mcp-server.md)
  * [10. 增加任务状态和轮询](07-source-implementation/go-agent-from-zero/10-task-status-polling.md)
  * [11. 连接数据库](07-source-implementation/go-agent-from-zero/11-database-agent.md)
  * [12. 写文章 Agent](07-source-implementation/go-agent-from-zero/12-writing-agent.md)
  * [13. 文件读取 Coding Agent](07-source-implementation/go-agent-from-zero/13-coding-agent.md)
* [03. 从零实现 MCP](07-source-implementation/mcp-from-zero/README.md)
  * [01. 本地 stdio MCP Server](07-source-implementation/mcp-from-zero/01-local-stdio-server.md)
  * [02. 本地 MCP：列出数据库表](07-source-implementation/mcp-from-zero/02-local-list-tables.md)
  * [03. 本地 MCP：查看表结构](07-source-implementation/mcp-from-zero/03-local-describe-table.md)
  * [04. 本地 MCP：统计表信息](07-source-implementation/mcp-from-zero/04-local-table-stats.md)
  * [05. 本地 MCP：删除和清理前确认](07-source-implementation/mcp-from-zero/05-local-delete-confirm.md)
  * [06. HTTP MCP Server](07-source-implementation/mcp-from-zero/06-http-server.md)
  * [07. HTTP MCP：列出数据库表](07-source-implementation/mcp-from-zero/07-http-list-tables.md)
  * [08. HTTP MCP：查看结构和统计](07-source-implementation/mcp-from-zero/08-http-describe-stats.md)
  * [09. HTTP MCP：删除清理权限校验](07-source-implementation/mcp-from-zero/09-http-delete-confirm.md)
* [04. 从零实现 Skill](07-source-implementation/skill-from-zero/README.md)
* [05. 多 Agent 交互与调度](07-source-implementation/multi-agent-interaction/README.md)
  * [01. Code Review Agent](07-source-implementation/multi-agent-interaction/01-code-review-agent.md)
  * [02. Planning Agent](07-source-implementation/multi-agent-interaction/02-planning-agent.md)
  * [03. Verification Agent](07-source-implementation/multi-agent-interaction/03-verification-agent.md)
  * [04. 创建子 Agent](07-source-implementation/multi-agent-interaction/04-create-sub-agent.md)
  * [05. 主 Agent 和子 Agent 的消息分发](07-source-implementation/multi-agent-interaction/05-message-task-dispatch.md)
  * [06. 顺序调度多个 Agent](07-source-implementation/multi-agent-interaction/06-sequential-dispatch.md)
  * [07. 多 Agent 协同完成 Code Review](07-source-implementation/multi-agent-interaction/07-collaborative-code-review.md)
  * [08. 并行分发和结果合并](07-source-implementation/multi-agent-interaction/08-parallel-merge.md)
  * [09. 写文章多 Agent 工作流](07-source-implementation/multi-agent-interaction/09-writing-multi-agent-workflow.md)

## 四、行业理解

* [01. 金融行业理解](08-industry-finance/README.md)
* [02. Web3 行业理解](09-industry-web3/README.md)

## 五、架构设计

* [01. 永续合约订单簿 L1 架构设计](10-architecture-design/perp-orderbook-l1-architecture.md)
  * [01A. 分阶段执行路线](10-architecture-design/perp-orderbook-l1-staged-execution.md)
  * [01B. 验证测试方案](10-architecture-design/perp-orderbook-l1-verification.md)
