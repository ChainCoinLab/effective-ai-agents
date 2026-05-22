# 【软核】循环神经网络 RNN：从遗忘到记忆

来源: https://www.bilibili.com/video/BV1FXduBNERM?vd_source=c85d4e6e0005b8d780998fba348f7bdf  
作者: 过拟合青年  
日期: 2026-05-08  
状态: 已提炼

## 这个视频解决什么问题

这个视频用“同一个词在不同语境下含义不同”切入，解释 RNN 为什么需要状态、状态如何沿时间更新、普通 RNN 为什么会遗忘，以及 LSTM / GRU 为什么要给状态更新加门控。

## 最终价值

它适合放在“大模型发展历史 / 从 RNN 到 Attention / Transformer”这一段之前，作为理解序列建模的底层铺垫：RNN 的核心不是公式，而是“读一个 token，改一次状态”；它的强项和弱点都来自这条状态链。

## 文件索引

- 元数据: `raw/metadata.json`
- 完整转写: `raw/transcript.txt`
- 清洗转写: `raw/transcript.cleaned.txt`
- 字幕: `raw/transcript.srt`
- 结构化内容: `notes/structured-content.md`
- 思维导图提炼: `notes/mindmap-summary.md`
- 有用摘录: `notes/useful-excerpts.md`
- 体验总结: `notes/experience-notes.md`
