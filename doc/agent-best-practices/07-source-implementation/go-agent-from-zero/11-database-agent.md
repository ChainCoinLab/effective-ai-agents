# 11. 连接数据库

[返回专题首页](README.md)

本节只增加一个能力：让 Agent 通过受控工具查询数据库。

## 本节任务

用户输入：

```text
查询最近 5 条文章标题
```

Agent 不能直接随意执行 SQL，而是只能调用预定义工具：

```text
list_recent_articles(limit)
```

## 和上一节相比新增什么

新增一个数据库工具：

```json
{
  "name": "list_recent_articles",
  "description": "List recent article titles",
  "input_schema": {
    "type": "object",
    "properties": {
      "limit": {
        "type": "integer"
      }
    },
    "required": ["limit"]
  }
}
```

Go 程序负责执行固定查询：

```sql
SELECT id, title, created_at
FROM articles
ORDER BY created_at DESC
LIMIT $1
```

## 整个流程

```text
用户输入数据库相关问题
  ↓
Claude 选择 list_recent_articles
  ↓
Go 校验 limit
  ↓
Go 执行固定 SQL
  ↓
Go 返回查询结果
  ↓
Claude 整理成自然语言回答
```

## 本节学到什么

数据库 Agent 不应该一开始就让模型自由写 SQL。更稳的第一步是：

- 预定义只读工具。
- 参数用 schema 约束。
- SQL 写在 Go 代码里。
- 写入类操作必须走确认。

[上一节：10. 增加任务状态和轮询](10-task-status-polling.md) · [下一节：12. 写文章 Agent](12-writing-agent.md)

