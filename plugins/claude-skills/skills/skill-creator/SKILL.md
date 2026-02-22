---
name: skill-creator
description: >
  This skill should be used when the user asks to "create a skill", "make a command",
  "generate a prompt", "write a slash command", "build a Claude extension",
  "add a skill to a plugin", "improve skill description", "write skill frontmatter",
  or needs help crafting optimized skills and commands with proper frontmatter, trigger phrases, or progressive disclosure structure.
argument-hint: "[skill|command] [name] - or leave empty to interview"
---

# Skill & Command Generator

Generate well-structured skills or slash commands. Both are markdown files with YAML frontmatter—they share the same structure but differ in how they're triggered and described.

## Phase 0: Fetch Current Documentation

**Before generating**, retrieve the latest documentation:

```
Use Task tool with subagent_type=claude-code-guide:
"List all current frontmatter options for skills and commands, including any execution modifiers, model selection, and structural options."
```

Integrate findings into your generation process. Documentation evolves—don't assume you know all options.

## Context Engineering

Every token counts. LLM context is finite. Goal: smallest possible set of high-signal tokens that maximize outcomes

| Do | Don't |
|---|---|
| "Validate input before processing" | "You should always make sure to validate..." |
| "Use grep to search" | "You might want to consider using..." |
| Bulleted constraints | Paragraphs with buried requirements |
| Imperative voice ("Analyze") | First person ("I will analyze") |

**Progressive discovery:** Core instructions in main file, details in `references/` subdirectory. Just-in-time information > front-loaded context
**Trust Claude:** Provide direction, not dictation. Claude extrapolates well from precise nudges.
**Optimize Signal-to-Noise:** Clear, direct language over verbose explanations. High-value tokens that drive behavior

### Degrees of Freedom

Match specificity to the task's fragility and variability:

| Level | When to Use | Format |
|-------|-------------|--------|
| **High freedom** | Multiple valid approaches, context-dependent decisions | Text instructions, heuristics |
| **Medium freedom** | Preferred pattern exists, some variation acceptable | Pseudocode, scripts with parameters |
| **Low freedom** | Fragile operations, consistency critical, specific sequence required | Exact scripts, few parameters |

Think of it as path guidance: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

## Phase 1: Understand Requirements

Parse `$ARGUMENTS` for type hint.
User is often unclear and uninformed on best practices of skill development. Always pull latest claude docs before proceeding. Continue to interview and help user the using `/thinking-partner` skill, if available.

Gather requirements:
1. **Primary objective** - What should this do?
2. **Trigger scenarios** - When should it activate?
3. **Inputs/outputs** - What does it receive and produce?
4. **Complexity** - Simple, standard, or complex?
5. **Execution needs** - Isolated context? Delegated to specialized agent?

## Phase 2: Generate

Skills and commands share the same structure. The key difference is in the **description**:
- **Skills:** Trigger-rich, third-person ("This skill should be used when...")
- **Commands:** Concise, verb-first, under 60 chars

**Intensional over extensional — apply this to all generated content.** When writing instructions inside a skill body, state the rule directly with its reasoning rather than listing examples that imply the rule. An intensional rule ("quoted phrases must be verbatim user speech *because* routing matches on literal tokens") generalizes to every input the skill will encounter. An extensional approach ("here is a good example, here is a bad example") requires the reader to reverse-engineer the rule — two reasoning hops instead of one, and it only covers the shape of those specific examples. Since this skill generates instructions that will themselves guide further generation, the quality of reasoning propagates: intensional instructions produce intensional skills.

### Common Frontmatter Options

```yaml
---
name: identifier                    # Required for skills
description: >                      # How it's described/triggered
  [See description patterns below]

# Execution modifiers
model: sonnet                       # haiku (fast), sonnet (balanced), opus (complex)
context: fork                       # Run in isolated sub-agent, preserves main context
agent: Explore                      # Route to specialized agent (Explore, Plan, custom)

# Tool access
allowed-tools:                      # Restrict available tools
  - Read
  - Grep
  - Bash(git:*)

# Lifecycle hooks (optional)
hooks:
  PreToolUse:
    - command: "validation-script.sh"
  PostToolUse:
    - command: "cleanup.sh"

# Behavior modifiers
user-invocable: true                # Show in /command menu (default true)
disable-model-invocation: true      # Prevent programmatic invocation (commands only)
argument-hint: [arg1] [arg2]        # Document expected arguments (commands only)
---
```

### Description Patterns

**For Skills (auto-triggered) — principles:**

- **Third-person framing is a routing signal, not a stylistic choice.** The routing model evaluates the description as a triggering condition. First-person ("Use this skill when...") reads as an instruction to execute. Third-person ("This skill should be used when...") reads as a condition to test. The framing changes how the model interprets the field.
- **Quoted phrases must be verbatim user speech.** Routing matches on literal token patterns. Write the exact words a user would type, not paraphrases: `"create a hook"` triggers correctly; `"hook creation workflows"` may not.
- **The description is always in context, even when the skill isn't active.** Every session pays the token cost of every skill's description. Density matters: cover more trigger patterns in fewer words. Avoid restating the skill name or explaining what skills are.
- **Cover the naive phrasing.** A user who doesn't know this skill exists won't search for it by name — they'll describe their problem in plain language. Include the phrasing someone would use who has never heard of this skill.
- **3–5 trigger phrases minimum.** Single-phrase descriptions have high miss rates. Varied phrases improve routing coverage across synonym space.
- **Use `>` scalar, not `|`.** Folded scalar (`>`) collapses newlines to spaces, producing a single continuous string — correct for descriptions. Literal scalar (`|`) preserves newlines, which can create unexpected whitespace when parsed.

```yaml
# Correct — third-person, verbatim phrases, folded scalar
description: >
  This skill should be used when the user asks to "create a hook",
  "add validation", "implement lifecycle automation", or mentions
  pre/post tool events.

# Wrong — vague, no trigger phrases, not third-person
description: Provides guidance for hooks.
```

**For Commands (user-invoked) — principles:**

- **Verb-first, under 60 chars.** The description appears as a single scannable line in the `/` menu — treat it as a menu label, not a sentence.
- **Describe the action, not the tool.** "Fix GitHub issue by number" orients by outcome. "GitHub issue fixer" orients by tool name. Users scan for what they want to accomplish.

```yaml
description: Fix GitHub issue by number
description: Review code for security issues
description: Deploy to staging environment
```

### Body Structure

Both skills and commands follow the same body pattern:

```markdown
# Name

Brief overview (1-2 sentences).

## Process
1. Step one (imperative voice)
2. Step two
3. Step three
```

**Key principle**
- Commands are instructions FOR Claude, not TO the user.

**Construction Rules:**
- State objective explicitly in first sentence
- Use imperative voice ("Analyze", "Generate", "Identify")
- No first-person narrative ("I will", "I am")
- Context only when necessary for understanding
- XML tags only for complex structured data
- Examples only when they clarify expectations — prefer stating the rule directly (intensional) over relying on examples to imply it (extensional); a stated rule generalizes, an example only covers its own shape
- Every word must earn its place
- No "When to Use This Skill" section in the body — the body loads only after triggering, so routing guidance placed there is never read by the routing decision
- Avoid headers deeper than H3 — deep nesting signals content that belongs in `references/`, not `SKILL.md`
- Use `` !`command` `` for dynamic context injection when real-time data (git status, file list, env vars) improves the skill without requiring a tool call

### Dynamic Content

| Syntax | Purpose |
|--------|---------|
| `$ARGUMENTS` | All arguments as string |
| `$1`, `$2`, `$3` | Positional arguments |
| `@path/file` | Load file contents |
| `@$1` | Load file from argument |
| Exclamation + backticks | Execute bash command, include output |

### Progressive Disclosure

For complex skills, organize into subdirectories:

```
skill-name/
├── SKILL.md          # Core instructions (keep under 500 lines)
├── scripts/          # Executable code (Python/Bash)
├── references/       # Docs loaded into context as needed
├── examples/         # Working code examples users can copy directly
└── assets/           # Files used in output (templates, icons, fonts)
```

**scripts/** - Deterministic, token-efficient. May be executed without loading into context. Use when the same code is rewritten repeatedly or reliability is critical.

**references/** - Documentation Claude reads while working. Keeps SKILL.md lean. For files >100 lines, include a table of contents. Only load when needed.

**examples/** - Working code examples: complete, runnable scripts, configuration files, template files, real-world usage examples. Users can copy and adapt these directly. Distinct from references (docs) and scripts (utilities).

**assets/** - Files NOT loaded into context. Used in output: templates, images, fonts, boilerplate. Example: `assets/hello-world/` for a React template.

#### Progressive Disclosure Patterns

**Pattern 1: High-level guide with references**

```markdown
# PDF Processing

## Quick start
Extract text with pdfplumber:
[code example]

## Advanced features
- **Form filling**: See references/forms.md
- **API reference**: See references/api.md
```

Claude loads references only when needed.

**Pattern 2: Domain-specific organization**

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (revenue, billing)
    ├── sales.md (pipeline, opportunities)
    └── product.md (API usage, features)
```

When user asks about sales, Claude only reads sales.md.

**Pattern 3: Variant-based organization**

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

User chooses AWS → Claude only reads aws.md.

### Execution Modifiers

Use these when the default behavior isn't sufficient:

- **`context: fork`** — Run in isolated sub-agent. Use for heavy workflows that would pollute main context, or when you need clean separation.

- **`agent: [type]`** — Route to a specialized agent. Examples: `Explore` for codebase search, `Plan` for architecture decisions, or custom agents you've defined. Requires `context: fork`.

- **`model: [level]`** — Override the model. Valid values: `haiku` (fast, cheap, simple tasks), `sonnet` (balanced default), `opus` (complex reasoning). Omit to inherit from the current conversation (`inherit` is the implicit default).

- **`hooks`** — Run scripts before/after tool use, scoped to this skill's lifecycle. Useful for validation, logging, or side effects.

- **`disable-model-invocation: true`** — Prevent Claude from auto-loading this skill. Use for skills you want to invoke manually only (commands only).

- **`user-invocable: false`** — Hide from the `/` command menu. Use for background-knowledge skills that should trigger automatically but not appear as slash commands.

### Tool Selection

Default generous, restrict only when needed. The principle: restrict tools that have destructive or side-effect potential, not tools that are read-only or purely generative.

| Tier | Tools | Why |
|------|-------|-----|
| **Always allow** | Read, Grep, Glob | Read-only, no side effects |
| **Usually allow** | Edit, Write, WebSearch, WebFetch, Task | Core work tools; restrict if skill is deliberately read-only |
| **Scope Bash** | `Bash(git:*)`, `Bash(npm:*)`, `Bash(pytest:*)` | Bash is the highest blast-radius tool — scope to known commands |
| **If interactive** | AskUserQuestion | Required any time the skill needs user decisions mid-workflow |
| **If delegating** | Skill | Required to invoke other skills programmatically |
| **If notebooks** | NotebookEdit | Jupyter-specific; omit unless skill touches `.ipynb` files |
| **If plan-gated** | ExitPlanMode, EnterPlanMode | For workflows requiring explicit user approval before execution |

### Before Finalizing

Scan for existing resources:
- Does a skill/command already handle part of this?
- Can this delegate to existing workflows?
- Is there redundancy with other features?

#### Delegation & Modularization

Before finalizing, scan for delegation opportunities:

```
Review available: skills, commands, agents, MCPs
For each workflow step, ask: "Do we already have this?"
```

**Common delegation patterns:**
- Git commits → `SlashCommand: /commit`
- Code review → `skill: /code-review`

**Always use fully qualified names:**
- `Skill: plugin-dev:hook-development` (not just "hook-development")
- `SlashCommand: /plugin-dev:create-plugin` (not just "create-plugin")
- `Task: subagent_type=plugin-dev:agent-creator`

### Script Opportunity Scan

**Load `references/script-patterns.md` before this step.** Apply the five signal
patterns to every workflow step in the skill being generated:

| Signal | Question | If yes → |
|--------|----------|----------|
| **Repeated Generation** | Does any step produce the same structure with different params across invocations? | Parameterized script in `scripts/` |
| **Unclear Tool Choice** | Does any step combine multiple tools in a fragile sequence to do something naturally expressible as one function? | Script the procedure |
| **Rigid Contract** | Can you write `--help` text for this step right now without ambiguity? | CLI candidate — delegate design to `create-cli` |
| **Dual-Use Potential** | Would a user want to run this step from the terminal, outside the skill workflow? | Design as proper CLI from the start |
| **Consistency Critical** | Must this step produce bit-for-bit identical output for identical inputs? | Script — never LLM generation |

For each identified script candidate:
1. Choose the archetype from `script-patterns.md` (init/validate/transform/package/query)
2. If the interface is non-trivial, delegate to `create-cli` skill to design it
3. Scaffold the script in `scripts/` using the Python template from `script-patterns.md`
4. Wire it into SKILL.md with: trigger condition, exact invocation, output interpretation

**Wiring rule:** A script reference must state *when* to invoke (trigger condition),
*how* to invoke (exact command with flags), and *what to do* with the result (exit code
handling, which output fields matter). Vague references ("run the script if needed") are
invisible to the skill workflow in practice.

### Explain Your Choices

When presenting the generated skill/command to the user, briefly explain:
- **What you set and why** — "Added `context: fork` because this workflow generates heavy output"
- **What you excluded and why** — "Left `model` unset (inherits default), `hooks` omitted (no validation needed)"
- **What they might want to change** — "You may want to add more trigger phrases if this doesn't activate reliably"

This transparency helps users understand the design and provide feedback.

### Bundled Scripts

This skill includes helper scripts to accelerate skill creation.

**Initialize a new skill:**
```bash
~/.claude/skills/skill-creator/scripts/init_skill.py <name> --path <dir> [--resources scripts,references,assets] [--examples]
```

Creates a skill directory with templated SKILL.md and optional resource directories.

**Validate a skill:**
```bash
~/.claude/skills/skill-creator/scripts/validate_skill.py <skill-directory>
```

Checks frontmatter format, naming conventions, description completeness, and body content.

**Package for distribution:**
```bash
~/.claude/skills/skill-creator/scripts/package_skill.py <skill-directory> [output-dir]
```

Creates a `.skill` file (zip format) after validation passes.

## Phase 3: Deliver

### Output Paths

| Type | Location |
|------|----------|
| User skill | `~/.claude/skills/<name>/SKILL.md` |
| User command | `~/.claude/commands/<name>.md` |
| Project skill | `.claude/skills/<name>/SKILL.md` |
| Project command | `.claude/commands/<name>.md` |

### Write and Confirm

Before writing:
```
Writing to: [path]
This will [create new / overwrite existing] file.
Proceed?
```

### After Creation

Summarize what was created:
- Name and type
- Path
- How to invoke/trigger
- Suggested test scenario

## Evaluation

**Evaluate the generated/optimized prompt:**

| Dimension | Criteria |
|-----------|----------|
| **Clarity (0-10)** | Instructions unambiguous, objective clear |
| **Precision (0-10)** | Appropriate specificity without over-constraint |
| **Efficiency (0-10)** | Token economy—maximum value per token |
| **Completeness (0-10)** | Covers requirements without gaps or excess |
| **Usability (0-10)** | Practical, actionable, appropriate for target use |

**Target: 9.0/10.0**

Present evaluation, then:
- If < 9.0: Refine addressing weakness, re-evaluate once
- If ≥ 9.0: Proceed to delivery


## Quality Standards

Apply Context Engineering Principles (see above). Additionally:

**Format Economy:**
- Simple task → direct instruction, no sections
- Moderate task → light organization with headers
- Complex task → full semantic structure

**Balance Flexibility with Precision:**
- Loose enough for creative exploration
- Tight enough to prevent ambiguity

**Remove ruthlessly:** Filler phrases, obvious implications, redundant framing, excessive politeness

## Validation Checklist

Before finalizing a skill or command:

**Structure:**
- [ ] SKILL.md file exists with valid YAML frontmatter
- [ ] Frontmatter has `name` and `description` fields
- [ ] Markdown body is present and substantial
- [ ] Referenced files actually exist

**Description Quality:**
- [ ] Uses third person ("This skill should be used when...")
- [ ] Includes specific trigger phrases users would say
- [ ] Lists concrete scenarios ("create X", "configure Y")
- [ ] Not vague or generic

**Content Quality:**
- [ ] Body uses imperative/infinitive form, not second person
- [ ] Body is focused and lean (1,500–2,000 words ideal, <5k max)
- [ ] Detailed content moved to references/
- [ ] Examples are complete and working
- [ ] Scripts are executable and documented
- [ ] Script opportunities identified via five signal patterns (references/script-patterns.md)
- [ ] Script references in SKILL.md include trigger condition, invocation, output handling
- [ ] Consistency-critical steps are scripted, not left to LLM re-generation

**Progressive Disclosure:**
- [ ] Core concepts in SKILL.md
- [ ] Detailed docs in references/
- [ ] Working code in examples/
- [ ] Utilities in scripts/
- [ ] SKILL.md references these resources

**Testing:**
- [ ] Skill triggers on expected user queries
- [ ] Content is helpful for intended tasks
- [ ] No duplicated information across files
- [ ] References load when needed

## Error Handling

| Issue | Action |
|-------|--------|
| Unclear requirements | Ask clarifying questions |
| Missing context | Request examples or constraints |
| Path issues | Verify directory exists, create with confirmation |
| Type unclear | Default to skill if auto-triggering desired |

---

Execute phases sequentially. Always fetch current documentation first.
