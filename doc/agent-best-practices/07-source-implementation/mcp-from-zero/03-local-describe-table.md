# 03. 本地 MCP：查看表结构

[返回专题首页](README.md)

本节只增加一个工具：`describe_table`，用于查看某个表有哪些字段。

## 工具定义

```json
{
  "name": "describe_table",
  "description": "Describe one database table",
  "input_schema": {
    "type": "object",
    "properties": {
      "table": {
        "type": "string"
      }
    },
    "required": ["table"]
  }
}
```

## 输出示例

```json
{
  "table": "articles",
  "columns": [
    {"name": "id", "type": "integer"},
    {"name": "title", "type": "text"},
    {"name": "created_at", "type": "timestamp"}
  ]
}
```

## 权限边界

`table` 必须先和 `list_tables` 的结果做白名单匹配。不要把用户传入的表名直接拼到 SQL 字符串里。

[上一节：02. 本地 MCP：列出数据库表](02-local-list-tables.md) · [下一节：04. 本地 MCP：统计表信息](04-local-table-stats.md)

