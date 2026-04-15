---
name: context-pack-builder
description: Build narrow, high-signal context packs for complex engineering tasks by selecting only the relevant code, tests, recent changes, docs, and risks. Use when a task spans multiple files or subsystems and the execution agent would otherwise be harmed by too much or too little context.
---

# Context Pack Builder

Build a narrow context pack that makes the next agent faster and safer.

## Workflow

1. Start from the task brief, not from the whole repository.
2. Separate implementation files, test files, and documentation files.
3. Include only recent changes that can realistically collide with this task.
4. Add reproduction paths, verification targets, and known risks.
5. Exclude noisy or merely adjacent material.

## Rules

- Justify why each file is included.
- Prefer small packs over broad packs.
- Include the minimum docs needed to avoid hallucinated assumptions.
- If a missing file is genuinely blocking, say so explicitly instead of padding the pack.

## Output Contract

Mirror `../../docs/templates/CONTEXT_PACK_TEMPLATE.md`.

## Read These References

- `references/context-selection-rules.md` for inclusion and exclusion rules

## Failure Modes To Avoid

- Dumping a broad directory listing
- Missing the key regression test file
- Omitting recent changes that directly affect the task
- Treating UI filtering as equivalent to backend enforcement
