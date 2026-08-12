# Repository Guidelines

## Project Structure & Module Organization

This repository is currently a documentation-first Genesis 0 project. Root documents define the project:

- `計劃書v0版.md`: strategic blueprint and development gates.
- `開發計劃.md`: ordered D0–D8 implementation backlog.
- `開發記錄.md`: append-only human-readable work log.
- `核心目標.md`: highest-level goal; expand only through the scheduled task.
- `buzz/`: Buzz platform notes, exercises, and integration references.

Planned directories such as `constitution/`, `residents/`, `missions/`, `history/`, `data/`, `src/`, and `tests/` must be created only when their corresponding development-plan step begins. Do not create residents or runtime code before the required Gate passes.

## Build, Test, and Development Commands

There is no application build or runtime yet. Use lightweight repository checks:

```powershell
rg --files                         # Inventory project files
rg -n "D[0-9]-[0-9]+" 開發計劃.md  # Locate planned work items
git diff --check                  # Detect whitespace errors
git status --short                # Review the exact change scope
```

When a runtime is introduced after Gate 2, document its setup, build, and test commands here. Buzz itself is an external platform; do not assume its Rust/React toolchain is part of this repository.

## Documentation Style & Naming Conventions

Write repository documentation in Traditional Chinese, using UTF-8, ATX headings, short paragraphs, and fenced blocks for schemas or flows. Preserve established machine-readable names such as `resident_001`, `mission_001.yaml`, `constitution_v0.1.md`, and `event_ledger.jsonl`. Use two-space indentation in YAML and valid JSON/JSONL. Keep Buzz platform concerns separate from Genesis Core rules.

## Testing Guidelines

For documentation changes, verify links, paths, terminology, and consistency with `計劃書v0版.md`. Record completed work and evidence in `開發記錄.md`. Future automated tests should cover event immutability, state reconstruction, lifecycle transitions, permissions, cost limits, and Buzz-event idempotency. No coverage threshold or test framework has been selected yet.

## Commit & Pull Request Guidelines

History uses concise Traditional Chinese commits, typically `新增 …`, `更新 …`, or `修正 …`. Keep each commit focused. Pull requests should state the development task ID, affected Gate, changed files, validation performed, and any unresolved risks. Include screenshots only for Buzz UI changes and link relevant issues or decisions.

## Security & Agent Instructions

Never commit Buzz `nsec` private keys, API keys, tokens, credentials, or `.env` files. Use minimum permissions and human approval for external actions. Follow the first unfinished item in `開發計劃.md`; do not silently skip stages or rewrite historical records.
