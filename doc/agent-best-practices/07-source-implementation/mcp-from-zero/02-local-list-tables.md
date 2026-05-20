# 02. 本地 MCP：列出数据库表

[返回专题首页](README.md)

本节只增加一个只读数据库工具：`list_tables`。

## 工具定义

```json
{
  "name": "list_tables",
  "description": "List database tables",
  "input_schema": {
    "type": "object",
    "properties": {},
    "required": []
  }
}
```

## 输出示例

```json
{
  "tables": ["users", "articles", "orders"]
}
```

## 权限边界

`list_tables` 只能读数据库元信息，不能拼接用户输入 SQL，不能执行写入语句。

[上一节：01. 本地 stdio MCP Server](01-local-stdio-server.md) · [下一节：03. 本地 MCP：查看表结构](03-local-describe-table.md)

