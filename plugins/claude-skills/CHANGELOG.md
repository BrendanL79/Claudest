# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.9] - 2026-02-23

### Added
- Add `create-agent` skill with scripts, references, and examples for generating Claude Code agent definitions

## [0.1.8] - 2026-02-23

### Added
- Add language selection feature to `create-cli` skill, supporting multi-language CLI scaffolding

## [0.1.5] - 2025-12-01

### Added
- Add `create-cli` skill for designing CLI surface areas — syntax, flags, subcommands, output contracts, and error codes

### Changed
- Improve `create-cli` with agent-aware design patterns (TTY auto-detection, NDJSON streaming, structured error objects)

## [0.1.4] - 2025-11-15

### Added
- Add `improve-skill` skill for effectiveness auditing of existing skills
- Rename `skill-creator` → `create-skill` and `skill-repair` → `repair-skill` to follow verb-first convention

## [0.1.3] - 2025-11-01

### Changed
- Repair `repair-skill` per audit findings — fix frontmatter and execution modifiers

## [0.1.2] - 2025-10-15

### Changed
- Repair `create-skill` (formerly skill-creator) per audit findings

## [0.1.1] - 2025-10-01

### Fixed
- Escape dynamic syntax pattern in skill documentation to prevent frontmatter parsing errors

## [0.1.0] - 2025-09-15

### Added
- Initial release with `create-skill` and `repair-skill` skills
- Replace placeholder symlinks with real skill directories
- Add shared `references/` library: `skill-anatomy.md`, `frontmatter-options.md`, `script-patterns.md`
