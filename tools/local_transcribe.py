#!/usr/bin/env python3
"""Transcribe an audio/video file with faster-whisper and write text/json/srt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel


def srt_time(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, rem = divmod(millis, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Audio or video file to transcribe")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument("--beam-size", type=int, default=5)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=args.compute_type,
    )
    segments_iter, info = model.transcribe(
        args.input,
        language=args.language,
        vad_filter=True,
        beam_size=args.beam_size,
        word_timestamps=False,
    )

    segments = []
    for segment in segments_iter:
        item = {
            "id": segment.id,
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
        }
        segments.append(item)
        print(f"[{segment.start:8.2f} -> {segment.end:8.2f}] {item['text']}", flush=True)

    metadata = {
        "language": info.language,
        "language_probability": info.language_probability,
        "duration": info.duration,
        "model": args.model,
        "beam_size": args.beam_size,
    }

    (out_dir / "transcript.json").write_text(
        json.dumps({"metadata": metadata, "segments": segments}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "transcript.txt").write_text(
        "\n".join(item["text"] for item in segments) + "\n",
        encoding="utf-8",
    )

    srt_blocks = []
    for index, item in enumerate(segments, start=1):
        srt_blocks.append(
            f"{index}\n{srt_time(item['start'])} --> {srt_time(item['end'])}\n{item['text']}"
        )
    (out_dir / "transcript.srt").write_text("\n\n".join(srt_blocks) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
