# claude-skills

Skill and agent authoring tools for Claude Code. Five complementary skills: one generates skills from scratch, one generates agents, one audits for structural correctness, one improves for effectiveness, and one designs CLI interfaces for the scripts those skills produce. A bundled `skill-lint` agent runs structural linting automatically after skill creation or improvement.

## Why

Writing a good Claude Code skill is harder than it looks. The description has to be precise enough to route reliably while being dense enough to not waste tokens on every session it doesn't trigger. The body has to be tight enough for consistent outcomes but not so prescriptive that it suppresses the model's ability to generalize. Workflow steps that should be deterministic scripts get left as inline prose that the model re-generates differently on each run. And most skills that "work" are missing infrastructure — reference files for domain-specific data, scripts for fragile operations, examples for outputs users will adapt — that would make them substantially better.

These skills exist to close that gap: `create-skill` generates skills with these properties built in, `create-agent` generates Claude Code agents with proper description format and system prompt structure, `repair-skill` diagnoses structural violations, `improve-skill` tests effectiveness against user goals, and `create-cli` designs the CLI interfaces for the scripts that deterministic workflow steps get extracted into.

## Installation

```
/plugin marketplace add gupsammy/claudest
/plugin install claude-skills@claudest
```

No dependencies. All skills work with whatever Claude model is running.

## Skills

### create-skill

Generate a new skill or slash command from requirements. Triggers on phrases like "create a skill", "make a command", "write a slash command", "add a skill to a plugin", "improve skill description", or "write skill frontmatter".

The skill interviews you about requirements (or reads them from `$ARGUMENTS`), fetches the latest Claude Code documentation before generating, and works through a structured generation process:

Phase 1 gathers requirements: primary objective, trigger scenarios, inputs and outputs, complexity, and execution needs. Phase 2 generates the skill with correct frontmatter, description principles (third-person framing, verbatim trigger phrases, `>` scalar, density over coverage), body structure, and progressive disclosure. Before finalizing, it runs a script opportunity scan across every workflow step: five signal patterns identify steps that should be proper CLI tools — parameterized scripts designed for both Claude invocation and direct terminal use — rather than inline code blocks re-generated on each run. When a step has a clear enough interface to write `--help` text for, it delegates to the `create-cli` skill for interface design, then scaffolds the script. Phase 3 delivers the skill to the correct path and explains every design decision.

### repair-skill

Audit and improve an existing skill against a gold standard. Triggers on phrases like "repair a skill", "audit a skill", "fix my skill", "improve an existing skill", "review skill quality", "check if my skill is well-written", or "what's wrong with this skill". Accepts a path to a skill directory or SKILL.md file as an argument.

The skill loads two reference files before auditing — the skill anatomy gold standard and the frontmatter options catalog — then runs seven audit dimensions:

**D1 — Frontmatter Quality.** Description person and framing, scalar type, trigger phrase authenticity and coverage, token density. Also flags missing `argument-hint` when the skill reads positional arguments.

**D2 — Execution Modifiers.** Model selection, context isolation, tool scope. Checks for both over-configuration (unrestricted `Bash`, dead tool entries, `opus` for tasks `sonnet` handles) and under-configuration (missing `AskUserQuestion` for interactive workflows, missing `context: fork` for heavy-output skills, `@$1` injection opportunities that a `Read` tool call is currently blocking).

**D3 — Intensional vs Extensional Instruction.** Identifies instruction blocks that teach by example when a stated rule would generalize better. An example requires two reasoning hops: infer the rule, then apply it. A stated rule is one hop, and it covers edge cases the examples didn't anticipate.

**D4 — Agentic vs Deterministic Split.** Applies the five script signal patterns (repeated generation, unclear tool choice, rigid contract, dual-use potential, consistency-critical operations) to every workflow step. Also flags judgment steps with no outcome criteria, and scripts that exist but aren't actionably referenced.

**D5 — Verbosity and Context Efficiency.** Redundant prose, hedging language, code blocks that collapse to one intensional rule, routing guidance in the body (dead tokens on every invocation since the body only loads post-trigger), headers deeper than H3, body exceeding 500 lines, extraneous documentation files.

**D6 — Workflow Clarity.** Phase structure, entry and exit conditions, half-thought steps, missing delivery format.

**D7 — Anatomy Completeness.** Compares the skill's directory structure against the correct tier (simple/standard/complex) and identifies absent infrastructure: missing `scripts/` for deterministic operations, missing `references/` when SKILL.md is too large, missing `examples/` for skills that produce user-adaptable output, unreferenced resource files that Claude won't load.

The output separates violations (something wrong) from gaps (something absent), each with the specific fix or addition needed. Confirmed repairs are applied in severity order with explicit reasoning for each change.

### improve-skill

Increase the effectiveness of an existing skill. Where `repair-skill` checks structural correctness against fixed rules, `improve-skill` asks whether the skill accomplishes what users actually need. Triggers on phrases like "improve a skill", "make this skill better", "add features to a skill", "what's missing from this skill", "the skill doesn't do X", or "improve how the skill works step by step".

The skill starts by understanding user intent via AskUserQuestion — establishing the specific complaint or running a full effectiveness audit if the user is unsure. It then runs four sub-analyses: mental simulation (walk through the skill as Claude with a real request, documenting stuck points, divergence points, dead ends, and friction), live doc validation (verify every factual claim — frontmatter field names, tool behavior, API parameters — against current documentation), feature adjacency scan (identify capabilities that are absent but adjacent, complementary, or needed to close end-to-end gaps), and UX flow review (check whether user interaction is placed at optimal points and consequential decisions are surfaced rather than made silently).

Findings are presented grouped by outcome type — new features, UX improvements, accuracy fixes, efficiency gains — and the user selects which to apply before any edits are made.

### create-cli

Design a CLI's surface area — syntax, flags, subcommands, output contracts, error codes, and configuration — before writing implementation code. Triggers on phrases like "design a CLI", "help me design command-line flags", "what flags should my tool have", "create a CLI spec", "refactor my CLI interface", or "design a CLI my agent can call".

Based on a design by [steipete](https://github.com/steipete); this is a modified version adapted for agent-aware CLI workflows.

The skill is built around a key distinction: a CLI consumed by an agent has different requirements than one designed only for human terminal use. Agents are always non-TTY, cannot tolerate ambiguous exit codes, parse stderr as structured data, and need compound output that reduces follow-up tool calls. The skill applies that lens throughout.

Phase 1 loads `cli-guidelines.md` as the default rubric and `language-selection.md` for implementation language guidance. Phase 2 clarifies command name, primary consumer (agent, human, scripted automation, or mixed), input sources, output contract, interactivity needs, config model, and implementation language — using best-guess defaults if the user is unsure or provides an existing spec. Language selection covers Go, Python, Node.js, Rust, and shell, with recommendations based on distribution requirements, runtime constraints, and agent-use patterns. Phase 3 applies a unified set of agent-first conventions: TTY auto-detection (pretty output when stdout is a TTY; structured JSON when piped or non-TTY), NDJSON for list commands to enable streaming, structured error objects on stderr with an `error` code and an executable `hint` field, consistent flag naming across subcommands so agent callers can learn patterns once, and compound output on mutating commands to avoid follow-up calls. For deeper context on these conventions, the skill can load `references/agent-aware-design.md`. Phase 4 delivers either a full CLI spec (new designs) or a gap report (audits of existing CLIs), including a command tree, args/flags table, output rules, error and exit code map, safety rules, config/env precedence, and worked examples.

`create-cli` is also called internally by `create-skill` and `repair-skill` when they identify a workflow step with a rigid enough interface to warrant a proper CLI tool rather than an inline code block.

### create-agent

Generate a well-structured Claude Code agent from requirements. Triggers on phrases like "create an agent", "make an agent", "write an agent", "build a subagent", "add an agent to a plugin", "design an autonomous agent", "generate an agent file", "write a system prompt for an agent", or "what frontmatter does an agent need".

Agents and skills are distinct constructs with different authoring requirements. An agent runs in an isolated context window, is written in second-person ("You are..."), uses `<example>` XML blocks in its description for routing, and is spawned via the Task tool. A skill injects inline into the current conversation, uses imperative instructions for Claude to follow, and routes via trigger phrase matching. `create-agent` enforces this distinction throughout.

The skill fetches current agent documentation before generating, then works through a structured generation process. Phase 1 gathers requirements: domain, expert persona, trigger conditions, proactive vs reactive firing behavior, tool access, and context isolation needs. Phase 2 generates the agent — it applies naming validation rules (3–50 characters, lowercase alphanumeric with hyphens, no generic names like `helper` or `assistant`), writes frontmatter with minimum necessary tools on the least-privilege principle, constructs a description with 2–4 `<example>` blocks covering synonym trigger coverage, and writes the system prompt body in second person with persona, process steps, output format, and edge cases. A script opportunity scan applies the five signal patterns to every step in the system prompt. Phase 3 delivers the agent to the correct path (`~/.claude/agents/`, `.claude/agents/`, or `<plugin-root>/agents/`), explains every design decision, and scores the result across five quality dimensions (Clarity, Trigger Precision, Efficiency, Completeness, Safety) targeting 9.0/10.0.

Two helper scripts are included: `validate_agent.py` checks naming rules and required frontmatter fields, returning a structured JSON error list with severity levels; `init_agent.py` scaffolds a new agent file with placeholders at the target path.

## Agents

### skill-lint

A bundled agent that runs structural linting after skill creation or improvement. Fires proactively when `create-skill` or `improve-skill` finishes generating output, and also on explicit user requests like "lint this skill".

`skill-lint` loads the two repair-skill audit reference files and runs all seven structural dimensions (D1–D7) against the skill. It auto-applies all critical and major fixes without asking, then presents minor findings for user decision. This separates structural correctness (skill-lint's domain) from effectiveness analysis (improve-skill's domain) — the two concerns that most often get conflated in manual skill review.

The agent is scoped to `Read`, `Glob`, `Grep`, `Edit`, `Write`, and `AskUserQuestion` only. It explicitly declines to lint agent files (AGENT.md), which have a different structural contract.

## Reference Library

The skills share a `references/` library that they load during their workflows.

`skill-anatomy.md` defines the gold standard at each complexity tier, the three-level loading model (metadata always loaded, SKILL.md on trigger, resources on demand), directory type definitions with when-to-use criteria, the Degrees of Freedom table mapping task fragility to instruction specificity, and a Gap Analysis Checklist for identifying what a skill would benefit from adding.

`frontmatter-options.md` is the complete catalog of valid frontmatter fields, all valid values per field, the full tool list with blast-radius notes, and a tool selection framework with tier table and rationale. Loaded before any frontmatter or execution modifier audit.

`script-patterns.md` covers the five signal patterns for recognizing script and CLI candidates, CLI design conventions for skill context (argument structure, output format, exit codes, help text), five script archetypes (init/validate/transform/package/query) with canonical argument patterns, the Python script template, wiring rules for referencing scripts from SKILL.md, and the delegation pattern to `create-cli` for non-trivial interface design.

`agent-frontmatter.md` (in `create-agent/references/`) is the complete catalog of valid agent frontmatter fields — tools, disallowedTools, model, color, permissionMode, isolation, background, maxTurns, skills, memory — with color semantics and tool selection guidance specific to agents. Loaded by `create-agent` before generating frontmatter.

`language-selection.md` (in `create-cli/references/`) covers implementation language selection for CLI tools: Go, Python, Node.js, Rust, and shell, with recommendations based on distribution model, runtime dependency tolerance, parsing library options, and agent-use suitability. Loaded by `create-cli` during Phase 2 clarification.

## Architecture Note

The skills in this plugin are regular directories shipped with the plugin. No symlinks or external sync needed — updates are delivered through the plugin version.

## License

MIT
