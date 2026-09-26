from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from spookspade.models import MediaMetadata


class MediaToolError(RuntimeError):
    """Raised when ffmpeg/ffprobe cannot inspect or transform media."""


def _require_tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise MediaToolError(
            f"{name} is required but was not found on PATH. "
            "Install FFmpeg and make sure both ffmpeg and ffprobe are available."
        )
    return path


def _fraction_to_float(value: str | None) -> float | None:
    if not value or value == "0/0":
        return None
    try:
        numerator, denominator = value.split("/", 1)
        denominator_value = float(denominator)
        if denominator_value == 0:
            return None
        return float(numerator) / denominator_value
    except (ValueError, ZeroDivisionError):
        return None


def parse_ffprobe_json(payload: dict[str, Any]) -> MediaMetadata:
    streams = payload.get("streams") or []
    format_info = payload.get("format") or {}

    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    duration_raw = format_info.get("duration")
    if duration_raw is None:
        durations = [
            float(s["duration"])
            for s in streams
            if s.get("duration") not in (None, "N/A")
        ]
        duration = max(durations, default=0.0)
    else:
        try:
            duration = float(duration_raw)
        except (TypeError, ValueError):
            duration = 0.0

    return MediaMetadata(
        duration_seconds=max(duration, 0.0),
        has_video=video_stream is not None,
        has_audio=audio_stream is not None,
        video_codec=video_stream.get("codec_name") if video_stream else None,
        audio_codec=audio_stream.get("codec_name") if audio_stream else None,
        width=int(video_stream["width"]) if video_stream and video_stream.get("width") else None,
        height=int(video_stream["height"]) if video_stream and video_stream.get("height") else None,
        fps=_fraction_to_float(video_stream.get("avg_frame_rate")) if video_stream else None,
    )


def probe_media(source: Path) -> MediaMetadata:
    ffprobe = _require_tool("ffprobe")
    command = [
        ffprobe,
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        str(source),
    ]

    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip()
        raise MediaToolError(
            f"ffprobe could not inspect {source.name}"
            + (f": {detail}" if detail else ".")
        ) from exc

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise MediaToolError("ffprobe returned invalid JSON.") from exc

    return parse_ffprobe_json(payload)


def extract_normalized_audio(source: Path, destination: Path) -> None:
    ffmpeg = _require_tool("ffmpeg")
    destination.parent.mkdir(parents=True, exist_ok=True)

    command = [
        ffmpeg,
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(source),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(destination),
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip()
        raise MediaToolError(
            f"ffmpeg could not extract audio from {source.name}"
            + (f": {detail}" if detail else ".")
        ) from exc
