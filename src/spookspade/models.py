from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class MediaMetadata:
    duration_seconds: float
    has_video: bool
    has_audio: bool
    video_codec: str | None = None
    audio_codec: str | None = None
    width: int | None = None
    height: int | None = None
    fps: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
