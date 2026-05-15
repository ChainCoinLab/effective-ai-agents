# 面试官：如何保证 Agent 调用工具 (Function Calling) 的可靠性？

来源: https://www.bilibili.com/video/BV12rDYBcErz  
作者: 图灵AI大模型  
日期: 2026-05-15  
状态: 已提炼

## 这个视频解决什么问题

回答“如何保证 Agent 调用工具可靠”这个面试题：不能只说把 prompt 写好，而要把可靠性拆成工具定义、调用前规划、执行前校验、高风险确认、错误回传和结果反思的工程链路。

视频把工具调用可靠性概括为一套从预防、拦截到自愈的分层体系：先用 schema 和描述约束模型，再减少工具干扰，最后由应用层校验、确认、重试和观测兜底。

## 最终价值

可复用为面试回答，也可转成生产 checklist：工具 schema 要强约束，工具集要按意图裁剪，模型输出不能直接执行，失败要结构化回传，高风险动作必须进入人工确认。

## 文件索引

- 元数据: `raw/metadata.json`
- 完整转写: `raw/transcript.txt`
- 清洗转写: `raw/transcript.cleaned.txt`
- 字幕: `raw/transcript.srt`
- 结构化内容: `notes/structured-content.md`
- 思维导图提炼: `notes/mindmap-summary.md`
- 有用摘录: `notes/useful-excerpts.md`
- 体验总结: `notes/experience-notes.md`
