from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from spookspade.media import MediaToolError
from spookspade.pipeline import IngestError, ingest_recording


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="spookspade",
        description="Spookspade gaming creator engine",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check local media-tool prerequisites.")
    doctor.set_defaults(handler=_doctor)

    ingest = subparsers.add_parser("ingest", help="Ingest one gameplay recording.")
    ingest.add_argument("source", type=Path)
    ingest.add_argument(
        "--runs-dir",
        type=Path,
        default=Path(".spookspade/runs"),
        help="Directory that will contain generated run artifacts.",
    )
    ingest.add_argument(
        "--skip-audio",
        action="store_true",
        help="Probe the recording but do not extract normalized audio.",
    )
    ingest.set_defaults(handler=_ingest)

    return parser


def _doctor(_args: argparse.Namespace) -> int:
    tools = {name: shutil.which(name) for name in ("ffmpeg", "ffprobe")}
    ok = all(tools.values())
    print(json.dumps({"ok": ok, "tools": tools}, indent=2))
    return 0 if ok else 1


def _ingest(args: argparse.Namespace) -> int:
    manifest_path = ingest_recording(
        args.source,
        args.runs_dir,
        extract_audio=not args.skip_audio,
    )
    print(manifest_path)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        return int(args.handler(args))
    except (IngestError, MediaToolError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("cancelled", file=sys.stderr)
        return 130
