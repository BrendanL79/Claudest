# Output Style Architecture

Reference for generating effective output styles. Load during Phase 1 only.

## The Persona-Anchors-Exemplars Model

Output styles work by shifting the model's generation distribution. Three layers, ordered from deepest (most effective) to shallowest:

### Layer 1: Persona (required, ~40 tokens)

A persona sentence activates a region of the model's learned style-space. "You are a tabloid journalist" compresses thousands of stylistic features (vocabulary, cadence, punctuation, sentence structure, formality, hedging patterns) into ~7 tokens. The model already knows what a tabloid journalist sounds like from training data. The persona is a pointer into that existing knowledge, not a set of rules to follow.

For character/persona styles: use the character archetype directly ("You are a Zen master", "You are a noir detective narrator").

For personal voice styles: synthesize a writing posture from samples — how they think, who they're talking to, what register they operate in. Not a character, but a description of the voice's qualities ("You write like someone explaining something at a whiteboard, mid-thought, to a smart friend who doesn't have your specific context").

For coding interaction styles: describe the collaboration mode ("You are a senior pair programmer who speaks in short, precise observations").

### Layer 2: Tonal/Thematic Anchors (recommended, ~60 tokens)

2-4 sentences that narrow within the persona's neighborhood. These constrain register, cadence, vocabulary field, and structural preferences without being explicit rules.

Good anchors: "Favor whitespace over walls of text", "One clear sentence beats three hedging ones", "Use concrete specifics, never generalize when you can point at the exact line."

Bad anchors: "Do not use em dashes" (surface-level ban), "Always write exactly 3 paragraphs" (rigid format rule). These fight the model's coherence rather than guiding it.

### Layer 3: Exemplar Phrases (optional, ~50 tokens)

2-3 short quoted phrases from the user's actual writing samples, demonstrating the target cadence and register. Only needed for personal voice matching where there's no pre-learned character archetype to activate. Character styles almost never need these because the model already has strong priors about how that character sounds.

## Why Ban Lists Fail

Banning specific tokens (em dashes, "delve", "crucial") is surface suppression. The model routes around bans by finding synonyms that carry the same rhetorical function. Banning "—" produces semicolons and parentheticals. Banning "delve" produces "explore" or "examine." The underlying distribution hasn't shifted, only the surface tokens. A well-chosen persona achieves more distribution shift in 7 tokens than a 500-word ban list.

Never include ban lists in generated styles.

## Token Budget

Empirical finding from 8 analyzed styles (2 built-in, 6 community): effective output styles range from 45-180 tokens of instruction. The most dramatic behavioral shifts come from the shortest styles (Tabloid Journalist: 45 tokens, Zen Master: 60 tokens). Longer instructions introduce conflicts the model must reconcile, reducing coherence.

Soft target: 200 tokens. Hard maximum: 400 tokens. If the generated style exceeds 400, cut from the bottom (structural constraints and surface rules first, persona and anchors last).

## keep-coding-instructions Decision

This frontmatter field controls whether the style replaces or layers on top of Claude's default engineering persona.

- `true`: Style layers on top. Default engineering behaviors preserved. Use for coding interaction styles and any style meant for use during programming.
- `false`: Style replaces defaults. Engineering persona stripped. Use for writing styles, character styles, and any style where the default concise-engineering voice would conflict.

Decision rule: if the user will primarily use this style while writing code, set `true`. If primarily for prose, creative writing, or non-coding communication, set `false`.

## Frontmatter Format

```yaml
---
name: Human-readable name (shown in /config picker)
description: One-line description of the voice (shown in /config picker)
keep-coding-instructions: true|false
---
```

The body after `---` is the style instruction. No headers needed. Write as flowing prose, not structured sections. The entire body becomes a system prompt injection.
