# Anthropic 最新分享：Claude Code 提示词缓存的最佳实践

来源: https://www.bilibili.com/video/BV1dRRyBREPM/  
作者: code秘密花园  
发布时间: 2026-05-05  
时长: 12:18  
原文: https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything  
状态: 已下载、已转写、已提炼

## 这个视频解决什么问题

这个视频讲的是 Claude Code 这类长对话 Agent 产品，为什么必须围绕 Prompt Caching 设计系统。它不只是省钱技巧，而是影响延迟、成本、额度、上下文压缩、工具管理和模型切换的底层架构约束。

## 最终价值

这条视频值得保留，因为它把“缓存是前缀匹配”这个核心约束讲透了，并延伸出一套 Agent 系统设计原则：

```text
稳定内容放前面；
动态变化放消息里；
中途别换模型；
中途别改工具集；
工具用延迟加载；
压缩和分岔要共享主对话前缀；
缓存命中率要像在线率一样监控。
```

## 文件索引

- 原始视频: `raw/source.mp4`
- 原始音频: `raw/audio.m4a`
- 原始转写: `raw/transcript.txt`
- 清洗转写: `raw/transcript.cleaned.txt`
- 字幕: `raw/transcript.srt`
- 结构化内容: `notes/structured-content.md`
- 思维导图提炼: `notes/mindmap-summary.md`
- 有用摘录: `notes/useful-excerpts.md`
- 体验总结: `notes/experience-notes.md`
- 关键帧总览: `assets/contact_45s.jpg`

