# 08. HTTP MCP：查看结构和统计

[返回专题首页](README.md)

本节把 `describe_table` 和 `table_stats` 也迁移到 HTTP MCP。

## 查看表结构

```http
POST /tools/describe_table
content-type: application/json
authorization: Bearer <token>

{"table":"articles"}
```

## 查看统计信息

```http
POST /tools/table_stats
content-type: application/json
authorization: Bearer <token>

{"table":"articles"}
```

## 权限边界

HTTP 参数必须做同样的校验：

- `table` 必须在白名单中。
- 只能执行固定 SQL 模板。
- 不能接受任意 SQL。
- 查询结果要限制大小。

[上一节：07. HTTP MCP：列出数据库表](07-http-list-tables.md) · [下一节：09. HTTP MCP：删除清理权限校验](09-http-delete-confirm.md)

