# 09. HTTP MCP：删除清理权限校验

[返回专题首页](README.md)

本节只处理 HTTP 写入类工具的权限校验。

## 本节任务

实现一个受控删除请求：

```http
POST /tools/delete_rows
content-type: application/json
authorization: Bearer <token>

{
  "table": "articles",
  "where": "status = 'draft'",
  "confirm_token": "confirm_abc"
}
```

## 两阶段确认

第一阶段只准备，不执行：

```json
{
  "action": "delete_rows",
  "table": "articles",
  "where": "status = 'draft'"
}
```

返回：

```json
{
  "requires_confirmation": true,
  "confirm_token": "confirm_abc",
  "expires_in_seconds": 60
}
```

第二阶段带 `confirm_token` 才执行。

## 本节学到什么

HTTP MCP 的删除清理必须比本地工具更严格：

- 必须鉴权。
- 必须短期确认 token。
- 必须记录审计日志。
- 必须限制表名和条件。
- 默认拒绝 `drop`、`truncate`、无条件删除。

[上一节：08. HTTP MCP：查看结构和统计](08-http-describe-stats.md)

