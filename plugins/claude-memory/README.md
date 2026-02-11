# claude-memory

Searchable conversation memory for Claude Code. Auto-syncs your sessions to a SQLite database with full-text search.

## Requirements

- Python 3.7+ (uses stdlib only, no pip packages needed)

## Installation

Add the Claudest marketplace to Claude Code, then install the plugin:

**Slash command (inside Claude Code):**
```
/plugin marketplace add gupsammy/claudest
/plugin install claude-memory@claudest
```

**CLI:**
```bash
claude plugin marketplace add gupsammy/claudest
claude plugin install claude-memory@claudest
```

## Features

- **Auto-sync**: Sessions automatically sync to database on session end
- **Auto-setup**: Database created on first session if missing
- **Full-text search**: FTS5 with Porter stemming and BM25 ranking (falls back to FTS4 or LIKE on systems without FTS5)
- **Context injection**: Previous session context automatically injected on startup
- **Branch-aware storage**: Tracks conversation rewinds as separate branches
- **Cross-platform**: Works on macOS, Linux, and Windows

## How It Works

On session start, the plugin injects context from your most recent session so Claude knows where you left off. On session end, it syncs the current conversation to the database in the background.

The `past-conversations` skill triggers automatically on phrases like:
- "what did we discuss"
- "remember when we worked on..."
- "continue where we left off"
- "as I mentioned before"

## Database

Location: `~/.claude-memory/conversations.db`

### Schema (v3)

- **projects**: Project metadata derived from directory structure
- **sessions**: One row per conversation session (UUID, timestamps, git branch)
- **branches**: Tracks conversation branches from rewinds, with aggregated content for FTS
- **messages**: User/assistant messages stored once per session, deduped by UUID
- **branch_messages**: Many-to-many mapping between branches and messages
- **messages_fts / branches_fts**: Full-text search indexes (FTS5, FTS4, or absent depending on platform)

## Hooks

| Event | Hook | Action |
|-------|------|--------|
| SessionStart | memory-setup.py | Creates `~/.claude-memory/` directory, triggers initial import if DB missing |
| SessionStart | memory-context.py | Injects previous session context (on `startup` and `clear` events) |
| Stop | memory-sync.py | Background syncs current session to database |

All hooks run without blocking Claude.

## Manual Usage

```bash
# Import all conversations
python3 plugins/claude-memory/hooks/import_conversations.py

# Import with stats
python3 plugins/claude-memory/hooks/import_conversations.py --stats

# Search conversations
python3 plugins/claude-memory/skills/past-conversations/scripts/search_conversations.py --query "authentication OAuth"

# Recent sessions
python3 plugins/claude-memory/skills/past-conversations/scripts/recent_chats.py --n 5
```

## License

MIT
