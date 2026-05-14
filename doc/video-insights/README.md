# Video Insights

这个目录用于存放每个视频提炼出来的结果。

目标不是简单保存字幕或摘要，而是把一个视频转化成可以复用的知识资产：

```text
完整获取内容 -> 提炼中心思想 -> 拆出论点/论据/论证 -> 摘录有用方法 -> 写下自己的体验总结
```

## 目录规则

每个视频一个独立子目录：

```text
doc/video-insights/
  video-slug/
    README.md
    raw/
      transcript.txt
      transcript.cleaned.txt
      transcript.srt
    notes/
      structured-content.md
      mindmap-summary.md
      useful-excerpts.md
      experience-notes.md
    assets/
      contact_60s.jpg
```

批量处理时会额外维护一个入口索引：

```text
doc/video-insights/_index.md
```

## 已处理视频

| 视频 | 目录 | 状态 |
| --- | --- | --- |
| Claude Code: 从零搭建你的 AI 工作团队（Skills + Agents） | `claude-code-skills-agents-axton/` | 已转写，已做结构化和思维导图提炼 |
| Anthropic 最新分享：Claude Code 提示词缓存的最佳实践 | `claude-code-prompt-caching-best-practices/` | 已转写，已做结构化、思维导图、摘录和体验总结 |

## 每类文件的用途

| 文件 | 用途 |
| --- | --- |
| `README.md` | 单个视频的入口，说明来源、主题、最终价值和文件索引 |
| `raw/transcript.txt` | 原始转写，尽量保留完整内容 |
| `raw/transcript.cleaned.txt` | 修正术语后的转写，便于阅读和引用 |
| `raw/transcript.srt` | 带时间轴的字幕文件 |
| `notes/structured-content.md` | 按章节整理出的结构化内容 |
| `notes/mindmap-summary.md` | 中心思想、论点、论据、论证的思维导图式提炼 |
| `notes/useful-excerpts.md` | 可直接复用的观点、方法、句子和操作清单 |
| `notes/experience-notes.md` | 你自己的体验、判断、疑问和行动计划 |
| `assets/` | 关键帧、截图、封面等辅助材料 |
| `.completed.json` | 单个视频处理完成标记，记录状态、片段数和关键文件是否生成 |
| `_index.md` | 多视频处理索引，方便查看状态和进入单个视频目录 |

## 批量处理工具

使用 `tools/video_insights_batch.py` 可以一次处理多个视频或已有转写，并发生成归档目录：

```bash
python3 tools/video_insights_batch.py \
  --manifest videos.json \
  --jobs 4 \
  --whisper-model small
```

也可以直接把已有转写导入，适合先验证提炼格式：

```bash
python3 tools/video_insights_batch.py doc/video-insights/example/raw/transcript.srt --skip-transcribe
```

Manifest 支持 JSON、JSONL 或纯文本。JSON 推荐格式：

```json
{
  "videos": [
    {
      "source": "https://www.bilibili.com/video/BVxxxx",
      "title": "视频标题",
      "slug": "video-title",
      "author": "作者",
      "published_at": "2026-05-14"
    },
    {
      "source": "/path/to/local.mp4",
      "title": "本地视频",
      "transcript": "/path/to/transcript.srt"
    }
  ]
}
```

常用参数：

| 参数 | 用途 |
| --- | --- |
| `--jobs 4` | 并行处理多个视频，默认最多 4 个任务 |
| `--skip-download` | 只建目录和记录来源，不下载 URL 视频 |
| `--skip-transcribe` | 不调用本地 Whisper，只用已有转写 |
| `--copy-source` | 把本地视频复制到 `raw/source.*`，否则只读取原路径 |
| `--force` | 重新生成清洗转写和笔记 |

这个脚本复用 `tools/local_transcribe.py` 做本地转写；URL 下载依赖 `yt-dlp`，转写依赖 `faster-whisper`。

## GitHub skill 调研结论

2026-05-14 查到的相关方案里，有三类值得借鉴：

1. `kennyzheng-builds/seek-and-analyze-video` 强调把视频索引成可长期查询的知识层，适合借鉴“跨视频检索”和“视频库记忆”的方向。
2. `browser-use/video-use` 的 `transcribe_batch.py` 明确采用 4-worker 批量转写，适合借鉴“多视频并行处理”和“转写缓存”。
3. `msadig` 的 video-input gist 强调每一步校验、帧与字幕按时间对齐、完成标记，适合借鉴“不中断、不漏步骤”的处理记录。

当前仓库先补齐本地批处理和归档能力；如果后续视频规模变大，再考虑接入持久向量索引或 VideoDB/Memories.ai 这类外部视频记忆服务。

## 提炼标准

处理每个视频时，按这个顺序走：

1. 完整获取：先拿到完整转写，不只看标题或关键帧。
2. 纠正常见术语：把专有名词、产品名、命令名修正清楚。
3. 结构化：按“背景 -> 问题 -> 方法 -> 案例 -> 结论”拆开。
4. 论证分析：明确作者的中心思想、主要论点、论据和论证方式。
5. 有用摘录：只摘能复用、能启发行动、能形成方法论的内容。
6. 体验总结：记录你看完后的判断，区分“作者观点”和“我的结论”。

## 有用内容筛选标准

进入 `notes/useful-excerpts.md` 的内容必须至少满足一条：

1. 能直接指导行动：包含步骤、流程、操作、建议、注意事项。
2. 能解释判断：包含原则、标准、原因、误区、取舍。
3. 能复用到写作或工作流：包含清晰表达、案例、模板、命令、工具组合。
4. 能暴露风险：包含限制条件、失败原因、不适用场景。

不收录纯寒暄、重复铺垫、没有上下文就无法判断的口号式表达。自动提取结果只作为第一轮候选，最终仍要人工复核。

## 命名建议

视频目录名使用英文小写短横线：

```text
claude-code-skills-agents-axton
```

如果同一作者同一系列有多期，可以加日期或编号：

```text
axton-ai-workflow-2026-04-07
```
