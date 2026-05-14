# Agent 最佳实践写作状态

更新时间：2026-05-14

## 总体状态

Status: done

当前目标：

- 按大类生成 50 个实践点。
- 每个实践点一个 Markdown 文件。
- 每个实践文件使用统一结构：`Rule`、`Why`、`Optimize`、`Verify`、`References`。
- 每个实践点先保持短小，后续可按文章需要扩写。

当前结果：

- 50 个实践点文件已生成。
- `PRACTICES.md` 已更新为实际文件路径。
- 已生成中文 Markdown 串联版：`guide.zh.md`。
- 已生成英文 Markdown 串联版：`guide.en.md`。
- 已生成 GitBook/HonKit 静态站点：`_book/index.html`。
- HTML 串联页由 HonKit 构建生成：`_book/guide.zh.html` 和 `_book/guide.en.html`。
- 顶层状态为 `done`；公开实践页不展示内部维护状态。

## 分类状态

| 分类 | 范围 | 目录 | 状态 | 负责人 |
| --- | --- | --- | --- | --- |
| 提示词与 Instruction | 01-08 | `01-prompt-instruction/` | done | worker: prompt/context |
| 上下文工程与 RAG | 09-18 | `02-context-rag/` | done | worker: prompt/context |
| 记忆与状态管理 | 19-24 | `03-memory-state/` | done | worker: memory/tools |
| 工具调用与多 Agent | 25-34 | `04-tools-agents/` | done | worker: memory/tools |
| 测试、评测与验证 | 35-42 | `05-evaluation-verification/` | done | worker: eval/feedback |
| 反馈闭环与迭代 | 43-50 | `06-feedback-iteration/` | done | worker: eval/feedback |

## 续接规则

- 如果上下文中断，先检查 `find doc/agent-best-practices -type f | sort`。
- 对照 `PRACTICES.md` 检查是否缺文件。
- 对每个实践文件检查是否包含 `Rule`、`Why`、`Optimize`、`Verify`、`References`。
- 如果某个文件只有标题或缺少验证方式，将其状态改为 `draft`。
- 全部文件齐全并通过结构检查后，将分类状态改为 `done`。
