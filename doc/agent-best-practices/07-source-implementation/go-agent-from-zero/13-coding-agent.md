# 13. 文件读取 Coding Agent

[返回专题首页](README.md)

本节只增加一个能力：让 Agent 能通过工具读取项目代码。

前面 Agent 已经会调用工具，但工具还是时间、计算器、数据库这类外部能力。从这一节开始，Agent 开始面对代码任务。第一步不要改代码，也不要运行命令，只让它安全地读取文件、列文件、搜索代码。

## 本节任务

输入：

```text
读取 main.go，找出 Ask 函数做了什么
```

Agent 可以通过工具读取文件，然后基于源码回答。

## 和上一节相比新增什么

新增三个只读代码工具：

```text
list_files(root)      列出项目文件
read_file(path)       读取指定文件
search_code(query)    搜索代码文本
```

第一个闭环可以只实现 `read_file`，但页面要让新手知道 Code Review Agent 后面至少需要这三类只读能力。

## read_file 工具 schema

```json
{
  "name": "read_file",
  "description": "Read a text file from the current project",
  "input_schema": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string"
      }
    },
    "required": ["path"]
  }
}
```

## search_code 工具 schema

```json
{
  "name": "search_code",
  "description": "Search text in project files",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string"
      }
    },
    "required": ["query"]
  }
}
```

## 路径安全边界

读文件工具必须限制在项目根目录内：

```text
允许：./main.go
允许：./internal/agent/agent.go
拒绝：/etc/passwd
拒绝：../../secret.txt
```

第一步只做只读工具，不做写文件、不运行命令。

## 整个流程

```text
用户提出代码问题
  ↓
Claude 请求 read_file 或 search_code
  ↓
Go 校验路径
  ↓
Go 读取文件内容
  ↓
Go 返回 tool_result
  ↓
Claude 基于源码回答
```

## 本节学到什么

Coding Agent 不是一上来就自动改代码。更稳的顺序是：

1. 先只读文件。
2. 再允许搜索文件。
3. 再允许生成补丁。
4. 再允许运行测试。
5. 最后才允许写文件和执行命令，并且高风险动作必须确认。

到这里，Agent 已经具备 Code Review 的基础前提：能看项目文件。下一节才开始做真正的 Code Review。

[上一节：12. 写文章 Agent](12-writing-agent.md) · [继续学习：多 Agent 交互与调度](../multi-agent-interaction/README.md)
