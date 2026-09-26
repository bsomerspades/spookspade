from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from spookspade.media import extract_normalized_audio, probe_media


class IngestError(RuntimeError):
    """Raised when a source recording cannot be admitted to a run."""


def ingest_recording(
    source: Path,
    runs_dir: Path,
    *,
    extract_audio: bool = True,
) -> Path:
    source = source.expanduser().resolve()

    if not source.exists():
        raise IngestError(f"Recording does not exist: {source}")
    if not source.is_file():
        raise IngestError(f"Recording is not a file: {source}")

    metadata = probe_media(source)
    if not metadata.has_video:
        raise IngestError(f"No video stream was found in {source.name}.")
    if metadata.duration_seconds <= 0:
        raise IngestError(f"Could not determine a positive duration for {source.name}.")

    run_id = f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"
    run_dir = runs_dir.expanduser().resolve() / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    audio_relative: str | None = None
    if extract_audio and metadata.has_audio:
        audio_path = run_dir / "audio.wav"
        extract_normalized_audio(source, audio_path)
        audio_relative = audio_path.name

    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "status": "ingested",
        "source": {
            "path": str(source),
            "filename": source.name,
            "size_bytes": source.stat().st_size,
        },
        "media": metadata.to_dict(),
        "artifacts": {
            "normalized_audio": audio_relative,
        },
    }

    manifest_path = run_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest_path
