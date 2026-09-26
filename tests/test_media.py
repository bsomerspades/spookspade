from spookspade.media import parse_ffprobe_json


def test_parse_ffprobe_json_extracts_expected_metadata() -> None:
    payload = {
        "streams": [
            {
                "codec_type": "video",
                "codec_name": "h264",
                "width": 1920,
                "height": 1080,
                "avg_frame_rate": "60000/1001",
            },
            {
                "codec_type": "audio",
                "codec_name": "aac",
            },
        ],
        "format": {"duration": "123.456"},
    }

    metadata = parse_ffprobe_json(payload)

    assert metadata.duration_seconds == 123.456
    assert metadata.has_video is True
    assert metadata.has_audio is True
    assert metadata.video_codec == "h264"
    assert metadata.audio_codec == "aac"
    assert metadata.width == 1920
    assert metadata.height == 1080
    assert metadata.fps is not None
    assert round(metadata.fps, 2) == 59.94


def test_parse_ffprobe_json_handles_missing_audio() -> None:
    payload = {
        "streams": [
            {
                "codec_type": "video",
                "codec_name": "hevc",
                "width": 2560,
                "height": 1440,
                "avg_frame_rate": "60/1",
            }
        ],
        "format": {"duration": "10"},
    }

    metadata = parse_ffprobe_json(payload)

    assert metadata.has_video is True
    assert metadata.has_audio is False
    assert metadata.audio_codec is None
    assert metadata.fps == 60.0
