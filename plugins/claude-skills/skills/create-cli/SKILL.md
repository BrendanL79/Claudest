---
name: create-cli
description: >
  This skill should be used when the user asks to "design a CLI", "help me design
  command-line flags", "what flags should my tool have", "create a CLI spec",
  "refactor my CLI interface", or wants to design command-line UX (args/flags/
  subcommands/help/output/errors/config) before implementation or audit an existing
  CLI surface for consistency and composability.
allowed-tools:
  - AskUserQuestion
  - Read
---

# Create CLI

Design CLI surface area (syntax + behavior), human-first, script-friendly.

## Phase 1 — Prepare

Read `${CLAUDE_PLUGIN_ROOT}/skills/create-cli/references/cli-guidelines.md` and apply it as the default rubric.

## Phase 2 — Clarify

Ask, then proceed with best-guess defaults if user is unsure:

- Command name + one-sentence purpose.
- Primary user: humans, scripts, or both.
- Input sources: args vs stdin; files vs URLs; secrets (never via flags).
- Output contract: human text, `--json`, `--plain`, exit codes.
- Interactivity: prompts allowed? need `--no-input`? confirmations for destructive ops?
- Config model: flags/env/config-file; precedence; XDG vs repo-local.
- Platform/runtime constraints: macOS/Linux/Windows; single binary vs runtime.

Proceed when answers are confirmed or user is unsure — use best-guess defaults.

## Phase 3 — Conventions

Apply these unless the user says otherwise:

- `-h/--help` always shows help and ignores other args.
- `--version` prints version to stdout.
- Primary data to stdout; diagnostics/errors to stderr.
- Add `--json` for machine output; consider `--plain` for stable line-based text.
- Prompts only when stdin is a TTY; `--no-input` disables prompts.
- Destructive operations: interactive confirmation + non-interactive requires `--force` or explicit `--confirm=...`.
- Respect `NO_COLOR`, `TERM=dumb`; provide `--no-color`.
- Handle Ctrl-C: exit fast; bounded cleanup; be crash-only when possible.

## Phase 4 — Deliver

Produce a compact spec the user can implement. Include all relevant sections:

- Command tree + USAGE synopsis.
- Args/flags table (types, defaults, required/optional, examples).
- Subcommand semantics (what each does; idempotence; state changes).
- Output rules: stdout vs stderr; TTY detection; `--json`/`--plain`; `--quiet`/`--verbose`.
- Error + exit code map (top failure modes).
- Safety rules: `--dry-run`, confirmations, `--force`, `--no-input`.
- Config/env rules + precedence (flags > env > project config > user config > system).
- Shell completion story (if relevant): install/discoverability; generation command or bundled scripts.
- 5–10 example invocations (common flows; include piped/stdin examples).

Use this skeleton, dropping irrelevant sections:

1. **Name**: `mycmd`
2. **One-liner**: `...`
3. **USAGE**:
   - `mycmd [global flags] <subcommand> [args]`
4. **Subcommands**:
   - `mycmd init ...`
   - `mycmd run ...`
5. **Global flags**:
   - `-h, --help`
   - `--version`
   - `-q, --quiet` / `-v, --verbose` (define exactly)
   - `--json` / `--plain` (if applicable)
6. **I/O contract**:
   - stdout:
   - stderr:
7. **Exit codes**:
   - `0` success
   - `1` generic failure
   - `2` invalid usage (parse/validation)
   - (add command-specific codes only when actually useful)
8. **Env/config**:
   - env vars:
   - config file path + precedence:
9. **Examples**:
   - …

See `${CLAUDE_PLUGIN_ROOT}/skills/create-cli/examples/example-cli-spec.md` for a complete worked example.

## Notes

- Prefer recommending a parsing library (language-specific) only when asked; otherwise keep this skill language-agnostic.
- If the request is "design parameters", do not drift into implementation.
