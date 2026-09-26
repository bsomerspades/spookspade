# Spookspade Agent Guide

## Product invariant

The current proof is:

> **Long gameplay recording in → ranked moments worth reviewing out.**

Do not expand the project into a full social platform, editor, Cortex module, multi-agent framework, or publishing system before that loop works.

## Current implementation slice

V0.1 owns only:

`source media → probe → optional normalized audio → run manifest`

A change outside that slice must explain the dependency before implementation.

## Architecture rules

- Standalone first. Do not import Cortex code or depend on unfinished Cortex services.
- Prefer boring local files and pure functions before durable infrastructure.
- FFmpeg/ffprobe are external tools, not hidden magic. Surface missing-tool and invalid-media errors clearly.
- Keep provider/model choices behind later boundaries; do not hard-wire the product to one AI vendor.
- Generated artifacts belong under the run directory, never beside the user's source recording.
- Do not modify or delete the original media.
- Every stage should leave inspectable outputs so a human can understand what happened.
- Public/publishing actions are out of scope for V0.

## Collaboration rules

- Work in bounded branches and PRs.
- Keep commits focused enough that another developer can review them.
- Add or update tests for deterministic logic.
- Do not silently refactor unrelated code.
- Do not add a dependency unless the current slice needs it.
- Never commit recordings, credentials, API keys, model weights, or generated run artifacts.

## Definition of done for a slice

- happy path works from the CLI;
- failure states are understandable;
- deterministic logic has tests;
- source recordings are untouched;
- README/docs match the actual behavior;
- no speculative infrastructure was added.
