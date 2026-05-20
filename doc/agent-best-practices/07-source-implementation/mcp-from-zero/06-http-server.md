# 06. HTTP MCP Server

[返回专题首页](README.md)

本节只增加一种传输方式：把 MCP 工具服务通过 HTTP 暴露。

## 本节任务

启动 HTTP 服务：

```text
POST /tools/list_tables
POST /tools/describe_table
POST /tools/table_stats
```

## 和本地 stdio 的区别

```text
本地 stdio：Agent 启动 MCP Server 子进程，通过 stdin/stdout 通信
HTTP：Agent 通过 HTTP 请求调用远程工具服务
```

## 权限边界

HTTP MCP 必须额外考虑：

- API key 或内部鉴权。
- 请求来源校验。
- 超时。
- 速率限制。
- 写入类工具的二次确认。

[上一节：05. 本地 MCP：删除和清理前确认](05-local-delete-confirm.md) · [下一节：07. HTTP MCP：列出数据库表](07-http-list-tables.md)

