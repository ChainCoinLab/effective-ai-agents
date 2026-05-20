# 04. 本地 MCP：统计表信息

[返回专题首页](README.md)

本节只增加一个工具：`table_stats`，用于查看某个表的基础统计信息。

## 工具定义

```json
{
  "name": "table_stats",
  "description": "Get row count and simple stats for one table",
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
  "row_count": 1280,
  "estimated_size": "16 MB"
}
```

## 权限边界

统计工具仍然是只读工具。它只能执行固定查询模板，不能接受任意 SQL。

[上一节：03. 本地 MCP：查看表结构](03-local-describe-table.md) · [下一节：05. 本地 MCP：删除和清理前确认](05-local-delete-confirm.md)

