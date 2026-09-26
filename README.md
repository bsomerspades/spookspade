# Spookspade Creator Engine

AI-assisted gaming content pipeline.

The first product hypothesis is deliberately small:

> **Long gameplay recording in → a short, ranked list of moments worth reviewing out.**

Spookspade is being built as a standalone specialist application first. Cortex integration is deferred until the workflow itself proves useful.

## Current slice: V0.1 ingest

The first coded slice does one boring but necessary thing well:

`gameplay file → validated media metadata + normalized audio + durable run manifest`

No clipping model, agent swarm, UI, publishing system, or Cortex dependency yet.

## Requirements

- Python 3.12+
- FFmpeg + ffprobe on PATH

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m spookspade doctor
pytest
```

Ingest a recording:

```bash
python -m spookspade ingest /path/to/gameplay.mp4
```

By default, run artifacts are written under `.spookspade/runs/`, which is gitignored.

See `docs/V0_SCOPE.md` for the bounded prototype plan.
