# Generation Standards

Reference checklist and quality standards for evaluating generated skills and commands.
Load during Phase 5 (Evaluate) before finalizing.

---

## Degrees of Freedom

Match instruction specificity to the task's fragility and variability:

| Level | When to Use | Format |
|-------|-------------|--------|
| **High freedom** | Multiple valid approaches, context-dependent decisions | Text instructions, heuristics |
| **Medium freedom** | Preferred pattern exists, some variation acceptable | Pseudocode, scripts with parameters |
| **Low freedom** | Fragile operations, consistency critical, specific sequence required | Exact scripts, few parameters |

## Quality Standards

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
