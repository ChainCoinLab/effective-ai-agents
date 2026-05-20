# 07. HTTP MCP：列出数据库表

[返回专题首页](README.md)

本节只实现 HTTP 版本的 `list_tables`。

## 请求

```http
POST /tools/list_tables
content-type: application/json
authorization: Bearer <token>

{}
```

## 响应

```json
{
  "tables": ["users", "articles", "orders"]
}
```

## 本节学到什么

同一个工具能力可以有两种承载方式：

```text
stdio MCP: 本地进程调用
HTTP MCP: 网络服务调用
```

工具 schema 应该保持一致，这样上层 Agent 不需要关心工具背后是本地还是 HTTP。

[上一节：06. HTTP MCP Server](06-http-server.md) · [下一节：08. HTTP MCP：查看结构和统计](08-http-describe-stats.md)

