# 从零实现 MCP

[返回源码实现](../README.md)

这个教程用数据库工具做例子，从零实现 MCP。先做本地 stdio MCP，再做 HTTP MCP。每一节只增加一个工具或一种传输方式。

## 学习路径

| 顺序 | 学习点 | 本节只解决什么问题 |
| --- | --- | --- |
| 01 | [本地 stdio MCP Server](01-local-stdio-server.md) | 跑通一个本地 MCP server，先返回固定工具结果 |
| 02 | [本地 MCP：列出数据库表](02-local-list-tables.md) | 增加只读工具 `list_tables` |
| 03 | [本地 MCP：查看表结构](03-local-describe-table.md) | 增加只读工具 `describe_table` |
| 04 | [本地 MCP：统计表信息](04-local-table-stats.md) | 增加只读工具 `table_stats` |
| 05 | [本地 MCP：删除和清理前确认](05-local-delete-confirm.md) | 增加高风险工具权限确认 |
| 06 | [HTTP MCP Server](06-http-server.md) | 把 MCP 工具服务改成 HTTP 方式暴露 |
| 07 | [HTTP MCP：列出数据库表](07-http-list-tables.md) | 通过 HTTP 调用 `list_tables` |
| 08 | [HTTP MCP：查看结构和统计](08-http-describe-stats.md) | 通过 HTTP 调用 `describe_table` 和 `table_stats` |
| 09 | [HTTP MCP：删除清理权限校验](09-http-delete-confirm.md) | HTTP 写入类工具必须鉴权和二次确认 |

## 数据库工具顺序

```text
list_tables
  ↓
describe_table
  ↓
table_stats
  ↓
delete_rows / truncate_table
```

前三个只读，最后一个高风险。高风险工具不能默认开放，必须有权限校验和人工确认。

