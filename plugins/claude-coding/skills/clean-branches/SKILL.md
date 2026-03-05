---
name: clean-branches
description: >
  This skill should be used when the user says "clean up branches", "delete merged
  branches", "prune stale branches", "git branch cleanup", "remove old branches",
  or wants to tidy up or purge old branches.
argument-hint: "[branch-pattern] - optional pattern to filter branches"
allowed-tools:
  - Bash(git:*)
  - Bash(bash:*)
  - AskUserQuestion
---

# Clean Git Branches

Safely remove merged and stale git branches with confirmation.

## Process

**0. Parse arguments**
If `$ARGUMENTS` provided, treat it as a glob pattern to filter branch candidates (e.g., `feature/*` shows only feature branches). Pass it to the candidate script in Step 2.

**1. Fetch latest state**
```bash
git fetch --all --prune
```
If fetch fails (no remotes configured), note remote data is unavailable and continue with local analysis only.

**2. Identify candidates**

Run the candidate detection script, passing the optional pattern filter:
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/clean-branches/scripts/find-candidates.sh "$PATTERN"
```
The script outputs two labeled sections (`=== MERGED ===` and `=== STALE ===`), one branch per line. Parse each section into its own list.

**3. Present results**

Display branches in three groups: merged (safe to delete), stale (no recent commits), and protected (never touch). If both candidate lists are empty, report "No branches to clean" and stop — do not proceed to Step 4.

**4. Confirm before deletion**

Use AskUserQuestion with concrete options derived from the candidates found. Structure:
- Header: "Branch cleanup"
- For merged branches: ask "Delete these merged branches?" with options like "Delete all N merged branches" (label) / "Removes: branch-a, branch-b, ..." (description), and "Keep all merged branches"
- For stale branches with multiple candidates: use multiSelect:true so the user can pick individual branches. Each option: label = branch name, description = age (e.g., "3 months ago")
- Always include a "Skip — keep all" option

Never proceed to deletion without explicit user confirmation through AskUserQuestion.

**5. Execute deletion**

Delete only what the user confirmed:
```bash
git branch -d <branch-name>
```
Use `-d` (not `-D`) because `-d` refuses to delete branches with unmerged commits — git itself enforces the safety check.

If the user explicitly requests remote cleanup:
```bash
git push origin --delete <branch-name>
```
Remote deletion requires explicit user request — never delete remotes unless the user says so directly.

## Safety Rules

- Never delete: main, master, develop, release/*
- Use `-d` not `-D` to preserve git's unmerged-commit safety check
- Remote deletion only on explicit user request

## Output

Summary of actions taken:
- Branches deleted (local)
- Branches deleted (remote, if requested)
- Branches kept
- Any errors encountered
