# claude-coding

Coding workflow skills for Claude Code. Six skills covering the commit loop, project maintenance, and documentation: stage and commit with conventional format, push and open a PR with smart branch handling, safely prune merged or stale branches, keep your CLAUDE.md accurate and concise, generate professional READMEs through a structured interview, and create or update a changelog from git history.

## Why

Coding sessions involve repetitive workflow decisions: which files belong in the same commit, whether to split concerns, whether you're on the right branch, what base branch to target, whether your project docs still reflect reality. These skills encode the right defaults so Claude handles those decisions consistently — and asks when it genuinely can't.

## Installation

```
/plugin marketplace add gupsammy/claudest
/plugin install claude-coding@claudest
```

Requires `git` and `gh` CLI (for push-pr). Both must be authenticated.

## Skills

### commit

Analyze and commit changes with intelligent file grouping and conventional commits. Reads `git status` and `git diff`, groups files by purpose rather than directory, validates if a linter is configured, and writes a conventional commit message (`feat`, `fix`, `docs`, etc.). Handles temporary file exclusion, multi-concern splits, and optional push in one flow.

Triggers on: "commit my changes", "commit this", "git commit", "save my work", "stage and commit", "create a commit", "commit what I've done".

### push-pr

Push commits and create or update pull requests with automatic branch management. Detects if you're on `main` with unpushed commits and cuts a feature branch before pushing. Creates new PRs or comments on existing ones. Calls the `commit` skill first if there are uncommitted changes.

Triggers on: "push this", "push my changes", "create a PR", "open a pull request", "make a PR", "submit for review", "send this up", "open PR", "pr please".

### clean-branches

Safely remove merged and stale git branches with confirmation. Finds branches already merged into main and branches with no commits in 30+ days, shows them categorized, and asks before deleting anything. Never touches protected branches. Remote deletion requires explicit confirmation.

Triggers on: "clean up branches", "delete merged branches", "prune stale branches", "git branch cleanup", "remove old branches".

### update-claudemd

Audit and optimize your project's CLAUDE.md file. Reads the current file, explores the codebase to verify accuracy, cuts anything that doesn't change how Claude acts in the next session, and rewrites for scannability. Creates a `.bak` backup before writing. Targets 150-250 lines of actionable content.

Triggers on: "update CLAUDE.md", "refresh the docs", "sync claude config", "optimize project instructions", "clean up CLAUDE.md", "improve CLAUDE.md", "fix CLAUDE.md".

### make-readme

Generate a professional `README.md` through a structured interview. Detects the project type from manifest files, then asks about depth (minimal, standard, or comprehensive), header style, sections, and badges. Minimal produces a 50-line focused doc; standard adds structured sections and shields.io badges; comprehensive adds a full Table of Contents, API reference, FAQ, and back-to-top links throughout. Writes the complete file in one pass.

Triggers on: "create a README", "generate a README", "make a readme", "write a README for my project", "add a README", "document my project", "readme with badges".

### make-changelog

Create or update `CHANGELOG.md` from git history using Keep-a-Changelog format. Detects existing changelog state and determines scope (fresh, fill, or unreleased-only). Launches one Haiku subagent per version range in parallel for token-efficient processing. Categorizes commits by user-observable impact rather than commit prefix, with present-tense imperative entries.

Triggers on: "create a changelog", "generate a changelog", "update my changelog", "fill in the changelog", "changelog from git history", "write changelog", "release notes", "my project needs a CHANGELOG".

## License

MIT
