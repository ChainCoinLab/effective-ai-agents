# 00.6 MCP 与工具调用原理

[返回全局摘要](../README.md) · [返回本组：AI 工程基础知识与原理](README.md)

MCP 是 Model Context Protocol，即模型上下文协议。它定义了 AI 应用或 Agent 发现、读取和调用外部资源、工具、提示模板的标准方式。

Function calling / tool use 是模型使用外部能力的机制。它的本质不是大模型在执行代码，而是模型在上下文和工具 schema 的约束下生成可解析的调用意图；Agent、应用后端或 MCP Client 负责校验、执行外部工具，并把结果再交回模型继续生成。

## 工作泳道图

![MCP 与工具调用泳道图](../assets/diagrams/mcp-tool-calling-tunnel.svg)

这张图按角色拆成六条泳道：用户、Agent/Host、大模型、MCP Client、MCP Server 和外部工具/API。一次工具调用不是模型直接执行外部动作，而是多方协作完成：

1. 用户把目标交给 Agent。
2. Agent 准备上下文，并告诉模型当前有哪些工具、工具规则是什么。
3. 模型根据用户目标和工具定义，生成结构化 tool call。
4. Agent / MCP Client 校验参数、权限和风险，再通过 MCP 调用工具。
5. MCP Server 调用真实外部系统，把工具结果返回。
6. 工具结果回到模型，模型基于结果加工成最终回答，再交给 Agent 或用户。

## 基本定义

| 概念 | 定义 | 负责什么 |
| --- | --- | --- |
| Tool | 外部系统提供的可调用能力 | 查询天气、搜索网页、读文件、执行代码、创建工单 |
| Tool call / Function call | 模型生成的结构化调用意图 | 表达要调用哪个工具，以及参数是什么 |
| MCP Server | 按 MCP 规范暴露能力的服务 | 提供 resources、tools、prompts，并执行工具适配 |
| MCP Client | Agent 或 Host 内部的协议客户端 | 发现工具、发起调用、接收返回结果 |
| Agent / Host | 编排模型、上下文和工具的应用 | 把工具定义交给模型，校验调用，处理权限、审计和回填 |

## 运行的本质

工具调用把“想做什么”和“真的去做”拆开。

```text
模型负责：根据用户目标和工具定义，生成工具名和参数
系统负责：校验参数、权限和风险，调用真实工具，返回 observation
```

这也是 function calling / tool use 最容易被误解的地方：模型吐出的不是外部工具的真实执行结果，而是一个动作请求。真实结果来自外部工具；模型拿到 observation 后，再把它加工成用户能读懂的回答。

因此，工具调用链路里至少有两次模型相关动作：第一次是模型决定要不要调用工具并生成参数；第二次是工具结果返回后，模型基于结果生成最终答复。中间真正执行查询、搜索、写入或代码运行的是外部工具，不是模型本身。

模型可能选错工具、填错参数、越过业务边界或被提示注入影响，所以不能把模型输出当成授权结果或事实结果。

真正的执行闭环是：

```text
用户目标
  -> Agent 装配上下文，告诉模型有哪些工具
  -> 模型生成 tool call
  -> Agent / MCP Client 校验参数和权限
  -> MCP Server 调用外部工具
  -> 工具返回 observation
  -> Agent 把 observation 回填给模型
  -> 模型生成最终回答或下一步 tool call
```

## 三句话总结

| 视角 | 总结 |
| --- | --- |
| 认清本质 | Function calling 不是模型执行代码，而是模型生成受约束的结构化调用意图；真正执行发生在 Agent、MCP Server 或业务后端。 |
| 点出核心 | 底层依靠工具描述、schema、工具调用样本训练和推理期结构约束，让模型更稳定地产生工具名和参数，但这只提高格式稳定性，不保证语义正确。 |
| 落地视角 | 生产环境的重点不在于模型多会“调用”，而在后端的参数校验、权限控制、错误重试、trace 回放和高风险拦截机制。 |

## 一次请求的泳道流程

以“北京今天会下雨吗”为例，完整链路可以拆成七步：

1. 用户提出目标：需要实时天气。
2. Agent 发现当前可用工具，例如天气 MCP Server 暴露了 `get_weather`。
3. Agent 把工具名称、描述、参数 schema 和使用规则放进模型上下文，告诉模型“什么情况该调用什么工具”。
4. 模型判断需要外部能力，输出结构化 tool call：`get_weather({"city":"北京","unit":"celsius"})`。
5. Agent 或 MCP Client 校验参数、用户权限、风险等级和调用策略。
6. MCP Server 执行真实天气 API，并返回结构化结果。
7. Agent 把结果作为 observation 回填给模型，模型再组织自然语言回答。

关键点是第 4 步、第 6 步和第 7 步不能混为一谈：第 4 步只是模型提出调用意图，第 6 步才是真实外部执行，第 7 步是模型把外部结果加工成最终答复。

## 从文本解析到结构化调用

早期的 Agent 工具调用往往靠约定文本格式。模型吐出来的还是普通文字，应用再用正则表达式或字符串规则解析。

```text
用户：北京今天会下雨吗？
模型：我需要查询天气：北京
应用：用正则匹配 “查询天气：(.+)”，提取 “北京”，调用 get_weather("北京")
```

后来常见做法是让模型输出更明确的动作标记，例如 ReAct 风格：

```text
Thought: 用户问实时天气，需要外部查询。
Action: get_weather
Action Input: {"city": "北京", "unit": "celsius"}
```

这种方式比普通文字稳定，但本质仍然是“让模型输出一段文本，再由应用解析”。如果模型多写一句话、字段名写错、JSON 少一个括号，解析就会不稳定。

现代 function calling / tool use 把这件事做成结构化协议。开发者把工具名称、描述和参数 schema 提供给模型；模型需要工具时，不再只输出自然语言，而是输出结构化的 tool call。某些模型或 serving 层内部会用 special tokens 或协议标记表示工具调用的开始、结束和参数区域，但应用侧更应该依赖 API 返回的结构化字段，而不是裸文本 token。

```json
{
  "type": "function_call",
  "name": "get_weather",
  "arguments": {
    "city": "北京",
    "unit": "celsius"
  }
}
```

## MCP 的三类能力

| 能力 | 含义 | 示例 |
| --- | --- | --- |
| Resources | 可读取的上下文资源 | 文件、文档、数据库记录、配置、知识材料 |
| Tools | 可调用的动作能力 | 搜索、查天气、代码执行、创建工单、业务 API |
| Prompts | 可复用提示模板 | 固定分析模板、生成模板、查询模板 |

其中 Tools 最接近 function calling。MCP Server 负责声明有哪些工具、每个工具需要什么参数、返回什么结果；MCP Client 负责发现工具并发起调用。

## MCP 调用方式示例

一个天气 MCP Server 可以暴露 `get_weather` 工具。Client 先发现工具：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

Server 返回工具定义：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "description": "查询指定城市的实时天气。仅在用户需要实时天气时使用。",
        "inputSchema": {
          "type": "object",
          "properties": {
            "city": {
              "type": "string",
              "description": "城市名，例如北京、上海"
            },
            "unit": {
              "type": "string",
              "enum": ["celsius", "fahrenheit"]
            }
          },
          "required": ["city"]
        }
      }
    ]
  }
}
```

当用户问“北京今天会下雨吗”，模型如果判断需要天气工具，会产生类似这样的调用意图：

```json
{
  "name": "get_weather",
  "arguments": {
    "city": "北京",
    "unit": "celsius"
  }
}
```

然后 MCP Client 向 MCP Server 发起真正调用：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "北京",
      "unit": "celsius"
    }
  }
}
```

Server 执行外部天气 API 后返回结果：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"city\":\"北京\",\"condition\":\"小雨\",\"temperature\":18,\"unit\":\"celsius\"}"
      }
    ]
  }
}
```

Agent 再把这个 observation 回填给模型，模型才回答用户：

```text
北京今天有小雨，气温约 18 摄氏度，出门建议带伞。
```

## MCP 和 Function Calling 的关系

Function calling / tool calling 是模型 API 层的能力：告诉模型有哪些函数可用，让模型返回结构化调用。

MCP 是应用和外部能力之间的连接协议：用统一方式发现工具、读取资源、获取 prompt 模板和调用工具。

两者可以这样分工：

```text
模型 API 的 tool calling：让模型表达“我要调用哪个工具、参数是什么”
MCP 的 tools/list：让 Agent 发现“当前有哪些工具、schema 是什么”
MCP 的 tools/call：让 Agent 真正调用外部工具
应用安全层：决定这个调用能不能执行
```

所以 MCP 不是替代 function calling，而是把 function calling 背后的工具供应、发现和调用标准化。

## 工程关注点

MCP 和工具调用上线不能只关注“接通了”。真正的风险在执行边界：

- 工具描述要写清何时使用、何时不用。
- 工具参数要结构化，尽量使用必填字段、枚举和明确类型。
- 工具列表不能无限塞给模型，应按任务检索和裁剪。
- 参数必须由应用或工具服务强校验，不能信任模型输出。
- 权限、审计、速率限制和数据访问控制必须在应用层完成。
- 删除、付款、发布、发信等高风险动作必须确认。
- 工具失败要返回结构化错误，让 Agent 能重试、降级或请求补充信息。

## 参考资料

- OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling
- MCP Specification: https://modelcontextprotocol.io/specification/latest
- MCP Tools: https://modelcontextprotocol.io/specification/2025-06-18/server/tools

---

[返回全局摘要](../README.md) · [返回本组：AI 工程基础知识与原理](README.md)
