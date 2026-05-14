#!/usr/bin/env python3
"""Batch ingest videos or transcripts into doc/video-insights.

This script is intentionally local-first: it creates a durable knowledge
directory for each video and can call tools/local_transcribe.py when a source
video is available. The extraction step is deterministic and conservative so
the generated notes are useful even before a human or LLM does a final pass.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_ROOT = REPO_ROOT / "doc" / "video-insights"
DEFAULT_WORK_ROOT = REPO_ROOT / "output" / "video-ingest"
LOCAL_TRANSCRIBE = REPO_ROOT / "tools" / "local_transcribe.py"

ACTION_TERMS = [
    "方法",
    "步骤",
    "流程",
    "工作流",
    "建议",
    "注意",
    "关键",
    "原则",
    "标准",
    "标准操作手册",
    "判断",
    "实践",
    "操作",
    "避免",
    "不要",
    "必须",
    "最好",
    "结论",
    "原因",
    "问题",
    "痛点",
    "误区",
    "先订流程",
    "example",
    "workflow",
    "process",
    "step",
    "should",
    "must",
    "avoid",
    "recommend",
]

WEAK_ACTION_TERMS = ["需要", "可以", "need", "can"]

TERM_FIXES = {
    "claudecode": "Claude Code",
    "cloud code": "Claude Code",
    "克劳德 code": "Claude Code",
    "cursor": "Cursor",
    "skill": "Skill",
    "skills": "Skills",
    "agent": "Agent",
    "agents": "Agents",
    "mcp": "MCP",
    "whisper": "Whisper",
    "git hub": "GitHub",
}


@dataclass(frozen=True)
class VideoJob:
    source: str
    slug: str
    title: str
    url: str = ""
    author: str = ""
    published_at: str = ""
    transcript: str = ""
    language: str = "zh"


@dataclass
class Segment:
    start: float | None
    end: float | None
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch process videos/transcripts into doc/video-insights."
    )
    parser.add_argument("sources", nargs="*", help="Video files, URLs, or transcript files")
    parser.add_argument(
        "--manifest",
        help="JSON/JSONL/TXT manifest. JSON items may include source, title, slug, url, author, transcript.",
    )
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT))
    parser.add_argument("--work-root", default=str(DEFAULT_WORK_ROOT))
    parser.add_argument("--jobs", type=int, default=min(4, max(1, os.cpu_count() or 1)))
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--skip-transcribe", action="store_true")
    parser.add_argument("--copy-source", action="store_true", help="Copy local video into raw/source.*")
    parser.add_argument("--whisper-model", default="small")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--force", action="store_true", help="Regenerate derived notes even if files exist")
    return parser.parse_args()


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"}


def slugify(value: str) -> str:
    lowered = value.lower().strip()
    lowered = re.sub(r"https?://", "", lowered)
    lowered = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", lowered)
    lowered = re.sub(r"-+", "-", lowered).strip("-")
    if not lowered:
        lowered = f"video-{dt.datetime.now().strftime('%Y%m%d%H%M%S')}"
    return lowered[:80]


def load_manifest(path: Path, default_language: str) -> list[VideoJob]:
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    if path.suffix.lower() == ".json":
        data = json.loads(text)
        if isinstance(data, dict):
            data = data.get("videos", [])
        return [job_from_mapping(item, default_language) for item in data]

    jobs: list[VideoJob] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("{"):
            jobs.append(job_from_mapping(json.loads(line), default_language))
            continue
        parts = [part.strip() for part in line.split("\t")]
        source = parts[0]
        title = parts[1] if len(parts) > 1 and parts[1] else infer_title(source)
        jobs.append(
            VideoJob(
                source=source,
                title=title,
                slug=slugify(title),
                url=source if is_url(source) else "",
                language=default_language,
            )
        )
    return jobs


def job_from_mapping(item: dict[str, Any], default_language: str) -> VideoJob:
    source = str(item.get("source") or item.get("url") or item.get("path") or "").strip()
    if not source and item.get("transcript"):
        source = str(item["transcript"])
    if not source:
        raise ValueError(f"manifest item is missing source: {item!r}")
    title = str(item.get("title") or infer_title(source)).strip()
    slug = str(item.get("slug") or slugify(title)).strip()
    return VideoJob(
        source=source,
        slug=slug,
        title=title,
        url=str(item.get("url") or (source if is_url(source) else "")).strip(),
        author=str(item.get("author") or "").strip(),
        published_at=str(item.get("published_at") or item.get("date") or "").strip(),
        transcript=str(item.get("transcript") or "").strip(),
        language=str(item.get("language") or default_language).strip(),
    )


def infer_title(source: str) -> str:
    if is_url(source):
        parsed = urlparse(source)
        return parsed.path.strip("/").split("/")[-1] or parsed.netloc
    return Path(source).stem


def make_job(source: str, language: str) -> VideoJob:
    title = infer_title(source)
    return VideoJob(
        source=source,
        title=title,
        slug=slugify(title),
        url=source if is_url(source) else "",
        language=language,
    )


def run_command(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def process_job(job: VideoJob, args: argparse.Namespace) -> dict[str, Any]:
    out_root = Path(args.out_root)
    work_root = Path(args.work_root)
    video_dir = out_root / job.slug
    raw_dir = video_dir / "raw"
    notes_dir = video_dir / "notes"
    assets_dir = video_dir / "assets"
    for directory in (raw_dir, notes_dir, assets_dir):
        directory.mkdir(parents=True, exist_ok=True)

    source_path = prepare_source(job, raw_dir, work_root, args)
    transcript_path = prepare_transcript(job, source_path, raw_dir, args)
    segments = load_segments(raw_dir, transcript_path)
    cleaned_text = clean_transcript("\n".join(segment.text for segment in segments))
    cleaned_path = raw_dir / "transcript.cleaned.txt"
    if args.force or not cleaned_path.exists():
        cleaned_path.write_text(cleaned_text + "\n", encoding="utf-8")

    metadata = {
        "title": job.title,
        "slug": job.slug,
        "source": job.source,
        "url": job.url,
        "author": job.author,
        "published_at": job.published_at,
        "processed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "已提炼" if segments else "待转写",
        "segment_count": len(segments),
    }
    (raw_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    write_readme(video_dir, metadata, bool(transcript_path), args.force)
    write_notes(notes_dir, job.title, metadata, segments, args.force)
    write_completion(video_dir, metadata, segments)
    return {
        "slug": job.slug,
        "title": job.title,
        "status": metadata["status"],
        "segments": len(segments),
        "dir": str(video_dir),
    }


def prepare_source(
    job: VideoJob, raw_dir: Path, work_root: Path, args: argparse.Namespace
) -> Path | None:
    if job.transcript:
        return None
    if is_url(job.source):
        if args.skip_download:
            return None
        target = raw_dir / "source.mp4"
        if target.exists() and not args.force:
            return target
        work_dir = work_root / job.slug
        work_dir.mkdir(parents=True, exist_ok=True)
        run_command(
            [
                "yt-dlp",
                "-f",
                "bv*+ba/best",
                "--merge-output-format",
                "mp4",
                "-o",
                str(target),
                job.source,
            ],
            cwd=work_dir,
        )
        return target

    source = Path(job.source).expanduser()
    if not source.exists():
        return None
    if source.suffix.lower() in {".txt", ".srt", ".json"}:
        return None
    if args.copy_source:
        target = raw_dir / f"source{source.suffix.lower() or '.mp4'}"
        if args.force or not target.exists():
            shutil.copy2(source, target)
        return target
    return source


def prepare_transcript(
    job: VideoJob, source_path: Path | None, raw_dir: Path, args: argparse.Namespace
) -> Path | None:
    explicit = Path(job.transcript).expanduser() if job.transcript else None
    if explicit and explicit.exists():
        target = raw_dir / explicit.name
        if explicit.resolve() != target.resolve() and (args.force or not target.exists()):
            shutil.copy2(explicit, target)
        normalize_transcript_file(target, raw_dir, args.force)
        return raw_dir / "transcript.txt"

    source = Path(job.source).expanduser()
    if source.exists() and source.suffix.lower() in {".txt", ".srt", ".json"}:
        target = raw_dir / source.name
        if source.resolve() != target.resolve() and (args.force or not target.exists()):
            shutil.copy2(source, target)
        normalize_transcript_file(target, raw_dir, args.force)
        return raw_dir / "transcript.txt"

    transcript = raw_dir / "transcript.txt"
    if transcript.exists() and not args.force:
        return transcript
    if args.skip_transcribe or source_path is None:
        return transcript if transcript.exists() else None
    run_command(
        [
            sys.executable,
            str(LOCAL_TRANSCRIBE),
            str(source_path),
            "--out-dir",
            str(raw_dir),
            "--model",
            args.whisper_model,
            "--language",
            job.language,
        ]
    )
    return transcript if transcript.exists() else None


def normalize_transcript_file(path: Path, raw_dir: Path, force: bool) -> None:
    transcript = raw_dir / "transcript.txt"
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        segments = data.get("segments", data if isinstance(data, list) else [])
        lines = [str(item.get("text", "")).strip() for item in segments if item.get("text")]
        if force or not transcript.exists():
            transcript.write_text("\n".join(lines) + "\n", encoding="utf-8")
        if path.name != "transcript.json":
            shutil.copy2(path, raw_dir / "transcript.json")
        return
    if path.suffix.lower() == ".srt":
        text = srt_to_text(path.read_text(encoding="utf-8"))
    else:
        text = path.read_text(encoding="utf-8")
    if force or not transcript.exists():
        transcript.write_text(text.strip() + "\n", encoding="utf-8")


def srt_to_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.isdigit() or "-->" in stripped:
            continue
        lines.append(stripped)
    return "\n".join(lines)


def load_segments(raw_dir: Path, transcript_path: Path | None) -> list[Segment]:
    json_path = raw_dir / "transcript.json"
    if json_path.exists():
        data = json.loads(json_path.read_text(encoding="utf-8"))
        raw_segments = data.get("segments", data if isinstance(data, list) else [])
        segments = []
        for item in raw_segments:
            text = clean_sentence(str(item.get("text", "")))
            if text:
                segments.append(Segment(item.get("start"), item.get("end"), text))
        if segments:
            return segments

    srt_path = raw_dir / "transcript.srt"
    if srt_path.exists():
        segments = load_srt_segments(srt_path)
        if segments:
            return segments

    if transcript_path and transcript_path.exists():
        text = transcript_path.read_text(encoding="utf-8")
        chunks = split_text_chunks(text)
        return [Segment(None, None, chunk) for chunk in chunks]
    return []


def load_srt_segments(path: Path) -> list[Segment]:
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    segments: list[Segment] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 2:
            continue
        time_line = next((line for line in lines if "-->" in line), "")
        if not time_line:
            continue
        start_text, end_text = [part.strip() for part in time_line.split("-->", 1)]
        text = " ".join(line for line in lines if line != time_line and not line.isdigit())
        text = clean_sentence(text)
        if text:
            segments.append(Segment(parse_srt_time(start_text), parse_srt_time(end_text), text))
    return segments


def parse_srt_time(value: str) -> float | None:
    match = re.match(r"(\d+):(\d+):(\d+),(\d+)", value)
    if not match:
        return None
    hours, minutes, seconds, millis = [int(part) for part in match.groups()]
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def split_text_chunks(text: str) -> list[str]:
    raw = [line.strip() for line in text.splitlines() if line.strip()]
    if len(raw) > 1:
        return [clean_sentence(line) for line in raw if clean_sentence(line)]
    sentences = re.split(r"(?<=[。！？.!?])\s+", text.strip())
    return [clean_sentence(sentence) for sentence in sentences if clean_sentence(sentence)]


def clean_transcript(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    for wrong, right in TERM_FIXES.items():
        text = re.sub(re.escape(wrong), right, text, flags=re.IGNORECASE)
    return text.strip()


def clean_sentence(text: str) -> str:
    return clean_transcript(text).replace("\n", " ").strip()


def write_readme(video_dir: Path, metadata: dict[str, Any], has_transcript: bool, force: bool) -> None:
    path = video_dir / "README.md"
    if path.exists() and not force:
        return
    status = metadata["status"]
    source = metadata["url"] or metadata["source"]
    value = "待完整转写后判断。" if not has_transcript else "已生成结构化内容、论证拆解和可复用摘录，适合后续复盘筛选。"
    content = f"""# {metadata['title']}

来源: {source or '未记录'}  
作者: {metadata['author'] or '未记录'}  
日期: {metadata['published_at'] or metadata['processed_at'][:10]}  
状态: {status}

## 这个视频解决什么问题

见 `notes/structured-content.md` 的“一句话概括”和“问题”部分。没有人工复核前，脚本会保守标注不确定内容。

## 最终价值

{value}

## 文件索引

- 元数据: `raw/metadata.json`
- 完整转写: `raw/transcript.txt`
- 清洗转写: `raw/transcript.cleaned.txt`
- 字幕: `raw/transcript.srt`
- 结构化内容: `notes/structured-content.md`
- 思维导图提炼: `notes/mindmap-summary.md`
- 有用摘录: `notes/useful-excerpts.md`
- 体验总结: `notes/experience-notes.md`
"""
    path.write_text(content, encoding="utf-8")


def write_notes(
    notes_dir: Path, title: str, metadata: dict[str, Any], segments: list[Segment], force: bool
) -> None:
    keywords = rank_keywords(segments)
    key_segments = select_useful_segments(segments)
    chapters = build_chapters(segments)
    write_if_needed(
        notes_dir / "structured-content.md",
        render_structured(title, metadata, segments, keywords, chapters),
        force,
    )
    write_if_needed(
        notes_dir / "mindmap-summary.md",
        render_mindmap(title, keywords, key_segments),
        force,
    )
    write_if_needed(
        notes_dir / "useful-excerpts.md",
        render_useful(title, key_segments),
        force,
    )
    write_if_needed(notes_dir / "experience-notes.md", render_experience(title), force)


def write_if_needed(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def rank_keywords(segments: list[Segment], limit: int = 12) -> list[str]:
    stopwords = {
        "这个",
        "那个",
        "就是",
        "然后",
        "所以",
        "因为",
        "如果",
        "一个",
        "我们",
        "你们",
        "他们",
        "大家",
        "可以",
        "需要",
        "视频",
        "内容",
        "the",
        "and",
        "that",
        "with",
        "this",
        "from",
        "you",
        "your",
    }
    counts: dict[str, int] = {}
    for segment in segments:
        text_lower = segment.text.lower()
        for term in ACTION_TERMS:
            if term.lower() in text_lower:
                counts[term] = counts.get(term, 0) + 2
        for word in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", segment.text):
            normalized = word.lower()
            if normalized in {"skills", "skill"}:
                normalized = "Skill"
            elif normalized in {"agents", "agent"}:
                normalized = "Agent"
            elif normalized == "claude":
                normalized = "Claude"
            if normalized in stopwords:
                continue
            counts[normalized] = counts.get(normalized, 0) + 1
    return [word for word, _count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]]


def select_useful_segments(segments: list[Segment], limit: int = 18) -> list[Segment]:
    scored: list[tuple[int, int, Segment]] = []
    seen: set[str] = set()
    for index, segment in enumerate(segments):
        text = merge_context(segments, index)
        if len(text) < 18:
            continue
        fingerprint = re.sub(r"\W+", "", text.lower())[:60]
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        strong_score = sum(3 for term in ACTION_TERMS if term.lower() in text.lower())
        weak_score = sum(1 for term in WEAK_ACTION_TERMS if term.lower() in text.lower())
        if strong_score == 0:
            continue
        score = strong_score + weak_score
        score += min(len(text) // 45, 5)
        if re.search(r"[1-9一二三四五六七八九十][\.、，:：]", text):
            score += 2
        if "?" in text or "？" in text:
            score += 1
        if score >= 3:
            scored.append(
                (
                    score,
                    -index,
                    Segment(start=segment.start, end=segment.end, text=summarize_text(text, 220)),
                )
            )
    selected = [item[2] for item in sorted(scored, key=lambda item: (-item[0], item[1]))[:limit]]
    return sorted(selected, key=lambda segment: segment.start if segment.start is not None else 10**9)


def merge_context(segments: list[Segment], index: int, max_chars: int = 260) -> str:
    start = max(0, index - 1)
    end = min(len(segments), index + 3)
    text = " ".join(segment.text for segment in segments[start:end])
    if len(text) <= max_chars:
        return text
    current = segments[index].text
    tail = " ".join(segment.text for segment in segments[index + 1 : end])
    merged = f"{current} {tail}".strip()
    return merged[:max_chars].rstrip()


def build_chapters(segments: list[Segment], max_chapters: int = 8) -> list[tuple[str, str]]:
    if not segments:
        return []
    timed = [segment for segment in segments if segment.start is not None]
    if not timed:
        sample_count = min(max_chapters, len(segments))
        step = max(1, len(segments) // sample_count)
        return [(f"片段 {index // step + 1}", summarize_text(segment.text)) for index, segment in enumerate(segments[::step][:sample_count])]
    duration = max(segment.end or segment.start or 0 for segment in timed)
    window = max(180, duration / max_chapters)
    chapters: list[tuple[str, str]] = []
    current: list[Segment] = []
    boundary = window
    for segment in timed:
        if segment.start is not None and segment.start >= boundary and current:
            chapters.append((format_time(current[0].start), summarize_text(" ".join(s.text for s in current))))
            current = []
            boundary += window
        current.append(segment)
    if current:
        chapters.append((format_time(current[0].start), summarize_text(" ".join(s.text for s in current))))
    return chapters[:max_chapters]


def summarize_text(text: str, limit: int = 110) -> str:
    text = clean_sentence(text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rstrip()
    return cut + "..."


def render_structured(
    title: str,
    metadata: dict[str, Any],
    segments: list[Segment],
    keywords: list[str],
    chapters: list[tuple[str, str]],
) -> str:
    one_line = summarize_text(segments[0].text, 140) if segments else "待转写后补充。"
    problem = infer_by_terms(segments, ["问题", "痛点", "误区", "为什么", "challenge", "problem"])
    method = infer_by_terms(segments, ["方法", "步骤", "流程", "建议", "实践", "workflow", "step", "recommend"])
    conclusion = infer_by_terms(segments, ["结论", "总结", "最终", "所以", "因此", "takeaway"])
    chapter_lines = "\n".join(f"- {time}: {summary}" for time, summary in chapters) or "- 待转写后生成。"
    keyword_text = "、".join(keywords) if keywords else "待提取"
    return f"""# {title} 结构化内容

## 一句话概括

{one_line}

## 主题关键词

{keyword_text}

## 背景

来源: {metadata['url'] or metadata['source'] or '未记录'}  
处理状态: {metadata['status']}  
说明: 本文件由批处理脚本基于转写内容自动提炼，重要结论需要人工复核。

## 问题

{problem}

## 方法

{method}

## 时间线要点

{chapter_lines}

## 结论

{conclusion}
"""


def infer_by_terms(segments: list[Segment], terms: list[str]) -> str:
    matches = []
    lowered_terms = [term.lower() for term in terms]
    for segment in segments:
        text_lower = segment.text.lower()
        if any(term in text_lower for term in lowered_terms):
            matches.append(f"- {format_segment(segment)} {summarize_text(segment.text, 150)}")
        if len(matches) >= 5:
            break
    if not matches:
        return "转写中没有稳定命中的明确表达，建议人工复核后补充。"
    return "\n".join(matches)


def render_mindmap(title: str, keywords: list[str], key_segments: list[Segment]) -> str:
    branches = keywords[:4] or ["待提炼"]
    branch_text = "\n".join(
        f"├─ {word}\n│  ├─ 证据: {summarize_text(find_segment_for_word(key_segments, word), 90)}\n│  └─ 复核: 判断它是否真是主线，而不是高频口头词"
        for word in branches[:-1]
    )
    last = branches[-1]
    last_text = (
        f"└─ {last}\n   ├─ 证据: {summarize_text(find_segment_for_word(key_segments, last), 90)}\n"
        "   └─ 复核: 补充作者的论证链条"
    )
    rows = "\n".join(
        f"| {word} | {summarize_text(find_segment_for_word(key_segments, word), 70)} | 自动按关键词和行动词命中 | 待人工判断 |"
        for word in branches
    )
    return f"""# {title} 思维导图提炼

## 中心思想

待人工复核: 当前脚本先按关键词、行动词和时间线提取候选主线。

## 思维导图

```text
{title}
{branch_text}
{last_text}
```

## 论点、论据、论证

| 论点 | 论据 | 论证重点 | 我的判断 |
| --- | --- | --- | --- |
{rows or '| 待提炼 | 待提炼 | 待提炼 | 待判断 |'}
"""


def find_segment_for_word(segments: list[Segment], word: str) -> str:
    for segment in segments:
        if word.lower() in segment.text.lower():
            return segment.text
    return segments[0].text if segments else "待补充。"


def render_useful(title: str, key_segments: list[Segment]) -> str:
    reusable_points = []
    methods = []
    operations = []
    parked = []
    for segment in key_segments:
        item = f"- {format_segment(segment)} {segment.text}"
        text = segment.text.lower()
        if any(term in text for term in ["方法", "原则", "建议", "判断", "recommend", "should"]):
            reusable_points.append(item)
        elif any(term in text for term in ["步骤", "流程", "操作", "step", "workflow", "process"]):
            methods.append(item)
        elif any(term in text for term in ["需要", "必须", "可以", "不要", "避免", "must", "need", "avoid"]):
            operations.append(item)
        else:
            parked.append(item)

    def section(items: list[str]) -> str:
        return "\n".join(items[:8]) if items else "- 待人工筛选。"

    numbered = "\n".join(
        f"{index}. {strip_bullet(item)}" for index, item in enumerate(operations[:8], start=1)
    )
    return f"""# {title} 有用摘录

## 筛选标准

只保留能复用、能指导行动、能解释判断标准，或能作为后续写作素材的片段；单纯寒暄、重复铺垫和无法验证的泛泛表达不进入核心摘录。

## 可复用观点

{section(reusable_points)}

## 可复用方法

{section(methods)}

## 可复用操作步骤

{numbered or '1. 待人工筛选。'}

## 值得保留的表达

{section(parked[:5])}

## 暂不采纳的内容

- 自动提取置信度不足的片段先不采纳，复盘时再根据完整上下文补充。
"""


def render_experience(title: str) -> str:
    return f"""# {title} 体验总结

## 我认可的部分

- 待人工复盘。

## 我存疑的部分

- 待人工复盘。

## 可以马上实践的动作

1. 从 `notes/useful-excerpts.md` 里挑出 1-3 条可执行步骤。
2. 把 `notes/mindmap-summary.md` 中的候选论点改成自己的判断。
3. 将不确定结论回到 `raw/transcript.cleaned.txt` 查上下文。

## 后续要验证的问题

- 哪些观点只是作者经验，哪些可以迁移到自己的场景？
- 哪些步骤有前置条件、成本或风险？

## 我的结论

待人工补充这个视频对自己的实际价值。
"""


def strip_bullet(value: str) -> str:
    return re.sub(r"^- ", "", value).strip()


def format_segment(segment: Segment) -> str:
    if segment.start is None:
        return ""
    return f"`{format_time(segment.start)}`"


def format_time(seconds: float | None) -> str:
    if seconds is None:
        return "无时间轴"
    total = int(seconds)
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours:02}:{minutes:02}:{secs:02}"
    return f"{minutes:02}:{secs:02}"


def write_completion(video_dir: Path, metadata: dict[str, Any], segments: list[Segment]) -> None:
    completion = {
        "completed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": metadata["status"],
        "segment_count": len(segments),
        "required_files": {
            "readme": (video_dir / "README.md").exists(),
            "structured": (video_dir / "notes" / "structured-content.md").exists(),
            "mindmap": (video_dir / "notes" / "mindmap-summary.md").exists(),
            "useful": (video_dir / "notes" / "useful-excerpts.md").exists(),
            "experience": (video_dir / "notes" / "experience-notes.md").exists(),
        },
    }
    (video_dir / ".completed.json").write_text(
        json.dumps(completion, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_library_index(out_root: Path, results: list[dict[str, Any]]) -> None:
    out_root.mkdir(parents=True, exist_ok=True)
    entries: dict[str, dict[str, Any]] = {}
    for child in out_root.iterdir():
        if not child.is_dir() or child.name.startswith("_"):
            continue
        entry = read_existing_entry(child)
        if entry:
            entries[child.name] = entry
    for result in results:
        entries[result["slug"]] = result

    lines = [
        "# Video Insights Index",
        "",
        "这个索引由 `tools/video_insights_batch.py` 生成，用来查看多视频处理状态和入口。",
        "",
        "| 视频 | 状态 | 片段数 | 目录 |",
        "| --- | --- | ---: | --- |",
    ]
    for result in sorted(entries.values(), key=lambda item: item["slug"]):
        lines.append(
            f"| {result['title']} | {result['status']} | {result['segments']} | `{result['slug']}/` |"
        )
    (out_root / "_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_existing_entry(video_dir: Path) -> dict[str, Any] | None:
    metadata_path = video_dir / "raw" / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        return {
            "slug": video_dir.name,
            "title": metadata.get("title") or video_dir.name,
            "status": metadata.get("status") or "未知",
            "segments": metadata.get("segment_count") or "?",
            "dir": str(video_dir),
        }

    readme_path = video_dir / "README.md"
    if not readme_path.exists():
        return None
    title = video_dir.name
    status = "未知"
    for line in readme_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("状态:"):
            status = line.split(":", 1)[1].strip()
    segment_count = count_existing_segments(video_dir)
    return {
        "slug": video_dir.name,
        "title": title,
        "status": status,
        "segments": segment_count if segment_count else "?",
        "dir": str(video_dir),
    }


def count_existing_segments(video_dir: Path) -> int:
    transcript_json = video_dir / "raw" / "transcript.json"
    if transcript_json.exists():
        data = json.loads(transcript_json.read_text(encoding="utf-8"))
        segments = data.get("segments", data if isinstance(data, list) else [])
        return len(segments)
    transcript_srt = video_dir / "raw" / "transcript.srt"
    if transcript_srt.exists():
        return len(load_srt_segments(transcript_srt))
    return 0


def main() -> int:
    args = parse_args()
    jobs = [make_job(source, args.language) for source in args.sources]
    if args.manifest:
        jobs.extend(load_manifest(Path(args.manifest), args.language))
    if not jobs:
        print("No videos provided. Pass sources or --manifest.", file=sys.stderr)
        return 2

    results: list[dict[str, Any]] = []
    failures: list[tuple[VideoJob, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as executor:
        future_to_job = {executor.submit(process_job, job, args): job for job in jobs}
        for future in concurrent.futures.as_completed(future_to_job):
            job = future_to_job[future]
            try:
                result = future.result()
                results.append(result)
                print(f"[ok] {result['slug']} ({result['status']}, {result['segments']} segments)")
            except Exception as exc:  # noqa: BLE001 - CLI reports per-job failures.
                failures.append((job, str(exc)))
                print(f"[failed] {job.slug}: {exc}", file=sys.stderr)

    write_library_index(Path(args.out_root), results)
    if failures:
        print("\nFailures:", file=sys.stderr)
        for job, reason in failures:
            print(f"- {job.slug}: {reason}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
