# V0 — Ranked Moments Prototype

## Goal

Prove one useful behavior before building the larger creator engine:

> **A long gameplay recording can be reduced to a small review queue containing moments the creator actually considers worth keeping.**

The prototype is not judged by how many AI features it has. It is judged by whether it meaningfully reduces the amount of raw footage a human has to scrub through.

## Standalone-first rule

Spookspade is a standalone specialist application during V0.

Cortex may later provide shared capabilities such as identity, approvals, files, resumption, connectors, or analytics, but V0 must not depend on unfinished Cortex infrastructure.

## Bounded sequence

### V0.1 — Ingest ← current

Input:
- one local gameplay recording.

Output:
- validated media metadata;
- normalized 16 kHz mono WAV when audio exists;
- a durable JSON run manifest.

Why first:
- every later transcript, event detector, clipper, and reviewer needs a reliable common media representation;
- this can be tested without choosing an AI provider.

### V0.2 — Transcript + timeline

Add:
- speech transcription with timestamps;
- speaker/channel information only if it proves reliable enough to help;
- transcript artifact attached to the run.

Prefer a local transcription path first where practical. Provider abstraction can wait until a second provider is actually useful.

### V0.3 — Candidate signals

Generate candidate time ranges from multiple weak signals rather than pretending one detector understands comedy:
- transcript/language cues;
- audio energy/change;
- scene/cut/change information;
- game/session metadata when available;
- later, model-based semantic review if it materially improves results.

Signals are evidence, not clips.

### V0.4 — Ranked review queue

Combine candidate signals into an inspectable ranked list:
- start/end time;
- why the candidate was surfaced;
- confidence/score inputs;
- nearby transcript/context;
- optional preview clip.

The creator can keep, reject, or adjust each candidate. That feedback becomes later training/evaluation data; it does not immediately justify self-modifying production logic.

## Out of scope for V0

- automatic publishing;
- comment/DM automation;
- cross-platform analytics;
- retention-driven re-editing;
- thumbnails;
- long-form automatic assembly;
- trend/patch-note research;
- generic multi-agent orchestration;
- Cortex integration;
- cloud infrastructure;
- custom hardware;
- a polished dashboard.

Those remain valid later ideas. None are required to prove the first loop.

## First proof questions

After using V0 on real recordings:

1. Does it reduce manual scrubbing enough to feel useful?
2. Does it surface moments the creator would otherwise have kept?
3. Are the reasons/timestamps good enough to trust as a review queue?
4. Which signal types contribute useful candidates versus noise?
5. What part of the process still consumes the most human time?

The next slice is chosen from observed failure, not from the grand roadmap.
