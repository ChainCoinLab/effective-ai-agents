# 05. 本地 MCP：删除和清理前确认

[返回专题首页](README.md)

本节只增加一个高风险能力：删除或清理数据前必须确认。

## 工具示例

```json
{
  "name": "delete_rows",
  "description": "Delete rows from one table with a restricted condition",
  "input_schema": {
    "type": "object",
    "properties": {
      "table": {"type": "string"},
      "where": {"type": "string"},
      "confirm": {"type": "boolean"}
    },
    "required": ["table", "where", "confirm"]
  }
}
```

## 执行规则

```text
confirm != true    拒绝执行
table 不在白名单   拒绝执行
where 为空         拒绝执行
truncate/drop      默认拒绝
```

## 整个流程

```text
Agent 请求 delete_rows
  ↓
MCP Server 返回需要确认
  ↓
用户确认
  ↓
Agent 再次请求并带 confirm=true
  ↓
MCP Server 执行受限删除
```

## 本节学到什么

删除、清理、写入都不是普通工具调用。模型可以提出意图，但权限由 MCP Server 和应用共同控制。

[上一节：04. 本地 MCP：统计表信息](04-local-table-stats.md) · [下一节：06. HTTP MCP Server](06-http-server.md)

