# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Add `update-readme` skill to refresh existing README files against current codebase state, git history, and changelog content
- Add `make-readme` skill (renamed from `readme-maker`) for generating professional READMEs through a structured interview
- Add `make-changelog` skill for creating or updating CHANGELOG.md from git history using Keep-a-Changelog format
- Add `update-claudemd` skill to audit and optimize project CLAUDE.md files
- Add `push-pr` skill with multi-PR scope analysis, automatic branch management, and PR body generation
- Add `commit` skill for intelligent file grouping and conventional commit message generation
- Add `clean-branches` skill for safely removing merged and stale git branches with confirmation

### Changed
- Rename skills to `make-*` convention (e.g. `readme-maker` → `make-readme`, `changelog-maker` → `make-changelog`) for consistency
- Rename all skills and commands to verb-first convention
- Improve `update-claudemd` skill with more accurate codebase verification and rewrite logic
- Repair `commit` skill per audit findings and fix script paths
- Repair `clean-branches` skill YAML frontmatter and execution modifiers

### Fixed
- Fix YAML frontmatter issues across `clean-branches` and other skills
- Fix script path references in commit skill after directory restructuring
