# Summary

* [00. 总览：AI 工程知识结构](README.md)
* [00.1 中文速览](guide.zh.md)

## 一、大模型开发

* [01. 大模型本体：由浅入深](00-llm-basics/README.md)
  * [01. 大模型发展历史](00-llm-basics/01-llm-history.md)
  * [02. 从函数到机器学习](00-llm-basics/01-function-to-machine-learning.md)
  * [03. 从现实对象到特征向量](00-llm-basics/02-real-world-to-vectors.md)
  * [04. 从文字到 token 和 embedding](00-llm-basics/03-token-and-embedding.md)
  * [05. 语言模型为什么预测下一个 token](00-llm-basics/04-next-token-prediction.md)
  * [06. 为什么预测下一个 token 会产生能力](00-llm-basics/05-capability-from-prediction.md)
  * [07. 从上下文问题到 Attention](00-llm-basics/06-attention-from-context.md)
  * [08. Transformer 如何一步步形成](00-llm-basics/07-transformer-architecture.md)
  * [09. 训练与对齐：模型能力从哪里来](00-llm-basics/09-training-and-alignment.md)
  * [10. 推理机制与调参](00-llm-basics/10-inference-and-parameters.md)
  * [11. 校验评估：怎么判断模型真的更好](00-llm-basics/12-evaluation.md)

## 二、Agent 开发

* [01. Agent 原理](00-llm-basics/agent-principles.md)
* [02. Agent 发展历史](00-llm-basics/agent-history.md)
* [03. Prompt 与指令工程](01-prompt-instruction/README.md)
* [04. 上下文工程与 RAG](02-context-rag/README.md)
* [05. 记忆与状态管理](03-memory-state/README.md)
* [06. 工具调用与 MCP](04-tools-agents/README.md)
* [07. Agent 工程化](04-tools-agents/agent-engineering.md)
* [08. 测评与反馈闭环](05-evaluation-verification/README.md)

## 三、源码实现

* [01. 源码实现](07-source-implementation/README.md)
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
