import json
from pathlib import Path

import pytest

import spookspade.pipeline as pipeline
from spookspade.models import MediaMetadata
from spookspade.pipeline import IngestError


def test_ingest_writes_manifest_and_audio_artifact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "session.mp4"
    source.write_bytes(b"not-real-video")

    metadata = MediaMetadata(
        duration_seconds=90.0,
        has_video=True,
        has_audio=True,
        video_codec="h264",
        audio_codec="aac",
        width=1920,
        height=1080,
        fps=60.0,
    )

    monkeypatch.setattr(pipeline, "probe_media", lambda _source: metadata)

    def fake_extract(_source: Path, destination: Path) -> None:
        destination.write_bytes(b"wav")

    monkeypatch.setattr(pipeline, "extract_normalized_audio", fake_extract)

    manifest_path = pipeline.ingest_recording(source, tmp_path / "runs")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["status"] == "ingested"
    assert manifest["source"]["filename"] == "session.mp4"
    assert manifest["media"]["duration_seconds"] == 90.0
    assert manifest["artifacts"]["normalized_audio"] == "audio.wav"
    assert (manifest_path.parent / "audio.wav").exists()


def test_ingest_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(IngestError, match="does not exist"):
        pipeline.ingest_recording(tmp_path / "missing.mp4", tmp_path / "runs")


def test_ingest_rejects_non_video(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "audio-only.m4a"
    source.write_bytes(b"x")

    monkeypatch.setattr(
        pipeline,
        "probe_media",
        lambda _source: MediaMetadata(
            duration_seconds=5.0,
            has_video=False,
            has_audio=True,
        ),
    )

    with pytest.raises(IngestError, match="No video stream"):
        pipeline.ingest_recording(source, tmp_path / "runs")
