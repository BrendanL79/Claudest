# Example CLI Spec: `snapr`

A complete worked example covering all deliverable sections. Use as a reference for
output format and level of detail.

---

## 1. Name

`snapr`

## 2. One-liner

Take and restore filesystem snapshots.

## 3. USAGE

```
snapr [global flags] <subcommand> [args]

snapr snapshot <path> [--name <name>] [--tag <tag>]
snapr restore  <snapshot-id> <target-path> [--force] [--dry-run]
snapr list     [--json] [--tag <tag>]
snapr delete   <snapshot-id> [--force]
```

## 4. Subcommands

| Subcommand | Description | Idempotent? |
|-----------|-------------|-------------|
| `snapshot <path>` | Capture a versioned archive of `<path>`. | Yes — creates a new snapshot each time |
| `restore <id> <target>` | Restore snapshot to `<target>`. Fails if target non-empty without `--force`. | No — overwrites data |
| `list` | List all snapshots; filter by tag. | Yes |
| `delete <id>` | Delete a snapshot. Prompts for confirmation unless `--force`. | No |

## 5. Global flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-h, --help` | bool | — | Show help; ignore all other args |
| `--version` | bool | — | Print version to stdout, exit 0 |
| `-q, --quiet` | bool | false | Suppress progress output; errors still go to stderr |
| `-v, --verbose` | bool | false | Emit debug output to stderr |
| `--json` | bool | false | Machine-readable JSON on stdout |
| `--no-color` | bool | false | Disable ANSI color; also respected via `NO_COLOR` env var |
| `--config <path>` | string | `~/.snapr/config.toml` | Path to config file |

Subcommand-specific flags:

| Flag | Applies to | Description |
|------|-----------|-------------|
| `--name <name>` | `snapshot` | Human label; defaults to ISO8601 timestamp |
| `--tag <tag>` | `snapshot`, `list` | Group/filter snapshots |
| `--dry-run` | `restore` | Show what would be overwritten without writing |
| `--force` | `restore`, `delete` | Skip confirmation; required for non-interactive use |

## 6. I/O contract

**stdout:** Snapshot IDs, list output, version string. `--json` converts all stdout to
JSON objects. `--quiet` suppresses everything except the final ID on `snapshot`.

**stderr:** Progress messages, verbose debug, warnings, errors. Never emitted in `--json` mode.

**stdin:** `restore` accepts `-` as `<target>` to pipe restored content to stdout
(single-file snapshots only).

## 7. Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Runtime error (snapshot not found, I/O failure, permission denied) |
| `2` | Invalid usage (unknown flag, missing required arg, bad type) |
| `3` | Target conflict — restore target is non-empty and `--force` not passed |

## 8. Env/config

**Environment variables:**

| Variable | Overrides | Notes |
|----------|-----------|-------|
| `SNAPR_DIR` | default snapshot dir (`~/.snapr/snapshots/`) | Set in CI to a shared volume |
| `SNAPR_CONFIG` | `--config` flag | Lower precedence than the flag |
| `NO_COLOR` | `--no-color` | Standard; respected automatically |

**Config file** (`~/.snapr/config.toml`; project-local `.snapr.toml` in CWD also checked):

```toml
snapshot_dir   = "~/.snapr/snapshots"
default_tag    = ""
retention_days = 30
```

**Precedence (high → low):** flags > env vars > project config (`.snapr.toml`) > user
config (`~/.snapr/config.toml`) > built-in defaults.

## 9. Examples

```bash
# Take a snapshot with a label
snapr snapshot ./src --name "before-refactor" --tag "dev"

# List all snapshots, machine-readable
snapr list --json | jq '.[] | select(.tag == "dev")'

# Preview a restore without writing
snapr restore abc123 ./src --dry-run

# Restore non-interactively in CI
snapr restore abc123 ./src --force --quiet

# Delete a snapshot
snapr delete abc123

# Pipe single-file snapshot to stdout
snapr restore def456 -

# Quiet snapshot in a pre-commit hook
SNAPR_DIR=/tmp/hooks snapr snapshot . --quiet
```
