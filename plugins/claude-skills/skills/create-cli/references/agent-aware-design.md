# Agent-Aware CLI Design — Spec

## Overview

CLI tools built in this workflow are invoked by both AI agents and humans, with agents as the
primary runtime caller. The goal is not to redesign CLI calling conventions — agents are
trained on `--help`, standard flags, and POSIX norms and will use them — but to make every
surface of the existing contract work better when the caller is an LLM. The three pillars are:
token-efficient output, fewer tool calls through good UX, and structured errors that enable
programmatic recovery.

## Key Themes

### Agent-Aware, Not Agent-First

Agents don't need a new interface — they're already fluent with `--help`, flag tables, and
exit codes. What they need is for those surfaces to be precise and low-noise. The skill should
not teach a different CLI paradigm; it should teach authors to be rigorous about the conventions
they already know, and to treat the agent as a peer consumer alongside the human.

### Explicit Output Modes

Explicit is better than implicit. The output default is human-readable text. `--json` gives
structured JSON. No TTY sniffing, no surprises. Agents pass `--json` — one extra token, zero
ambiguity. This avoids the PTY trap (some agent runners allocate pseudo-terminals, fooling
`isatty()`) and works identically across platforms, CI environments, and terminal emulators.
List commands in `--json` mode use NDJSON (one object per line) for streaming. For paginated
results with metadata, a JSON object with an `items` array is acceptable.

### Reduce Tool Calls Through CLI Design

Three patterns reduce the number of Bash invocations an agent needs:

- **Compound output:** Operations return enough data to avoid a follow-up call. `create`
  returns the created resource's ID and key fields on stdout. `delete` echoes what was deleted.
  `list` returns full objects, not just IDs, in JSON mode.

- **Rich defaults:** In `--json` mode, include enough context in a single response that the
  agent rarely needs to call again. Avoid outputs that are "half the answer."

- **Predictable behavior:** Idempotent commands, clear preconditions, consistent flag behavior
  across subcommands. If the agent can predict the outcome, it may skip a verification call
  entirely.

### Consistent Surface for Fast Discovery

Agents scan a CLI's surface area from `--help` output and flag tables. Consistency across
subcommands is what makes that scan cheap:

- Verb-noun subcommand naming, applied uniformly (`create`, `list`, `delete`, `get`).
- Same flag names for the same concepts across all subcommands (`--id`, `--json`, `--force`).
- Same output shape for similar operations (all create-type commands return the same fields).

A compact top-level `--help` that fits in a single screen is the agent's map. It should be
tight enough that the agent reads it once and knows the full surface area.

### Structured Errors with Executable Hints

Error output in non-TTY mode should follow a standard JSON schema on stderr:

```json
{"error": "not_found", "message": "Snapshot 'abc123' does not exist.", "hint": "snapr list --json"}
```

The `hint` field should be an exact command the agent can execute, not prose. This eliminates
a reasoning step — the agent doesn't need to infer what to do, it can run the hint directly.
The three fields are: `error` (machine-readable code, snake_case), `message` (human-readable
sentence), `hint` (optional; exact CLI invocation or `null`).

### Agent Piping Principles (brief)

- Stdout should be stable across versions in non-TTY mode (agents pipe into other tools).
- When a command produces a list, emit one JSON object per line (NDJSON) rather than a
  JSON array — this enables streaming and `jq` piping without buffering the full output.
- Support `-` as stdin/stdout for single-resource commands where it makes sense.
- Never emit ANSI codes, progress spinners, or interactive prompts when stdout is not a TTY.

### Spec Lives in a Skill

The CLI spec produced by this skill typically lives inside a skill body or as an embedded
reference block, not as a standalone file in the user's repo. This means the spec must be
compact enough to fit in an agent's context budget. Redundant sections should be omitted
(not just marked optional), and examples should be dense — demonstrate multiple patterns
in a single invocation rather than one-pattern-per-line.

## Decisions & Positions

- Explicit output modes: human-readable by default, `--json` for structured output. No TTY
  auto-detection — explicit is better than implicit.
- Phase 3 of the skill should be rewritten from scratch as unified "CLI Conventions" — not
  "human norms + agent add-on."
- `cli-guidelines.md` should be extended with an "Agent Ergonomics" section (our opinionated
  fork of clig.dev, not a replacement of it).
- The snapr example should demonstrate all agent-aware patterns: explicit `--json` output,
  structured errors with executable hints, compound output, NDJSON for list commands.
- Flag design stays natural language — no formal schemas. Consistency and precision in the
  spec is sufficient; agents infer well from well-written docs.

## Resolved Decisions

- NDJSON is the default list format in `--json` mode. It's strictly more useful for agents
  and `jq` piping. Exception: paginated results with top-level metadata use a JSON object
  with an `items` array.
- The error schema requires `hint` to be a fully executable command (strict). An agent can
  run the hint directly without a reasoning step. `null` when no recovery action applies.

## Constraints & Boundaries

- This is not about new CLI calling conventions. Agents use `--help`, flags, and exit codes
  as-is. The improvements are in output format, error structure, and design discipline.
- Not a formal schema spec (no OpenAPI/JSON Schema for CLI interfaces). Principles and
  strong conventions, not machine-readable contracts.
- Not a token-minimization guide. The goal is fewer tool calls, not shortest possible output.
  Rich compound output often uses *more* tokens per call but fewer calls total.
