# Claudest

A curated Claude Code plugin marketplace. Everything here is something I personally use, build, and iterate on across real projects. If it's in this marketplace, it works.

## Installation

Add the marketplace, then install any plugin:

```
/plugin marketplace add gupsammy/claudest
/plugin install claude-memory@claudest
```

To enable auto-updates, run `/plugin`, go to the Marketplaces tab, and toggle auto-update for Claudest.

## Plugins

### claude-memory

Conversation memory for Claude Code. Recall what happened yesterday, last week, or three weeks ago.

LLMs don't carry anything forward between sessions. Every conversation starts blank. Claude Code gives agents core memory (CLAUDE.md files loaded every session), procedural memory (skills and tool definitions), and archival memory (auto memory notes the agent writes for itself). What was missing: recall memory. The ability to search and retrieve actual past conversations.

That's what claude-memory provides. It stores every session in a SQLite database with full-text search (FTS5, BM25 ranking, zero external dependencies) and makes past conversations available to the agent in two ways.

First, automatic context injection. On every session start, a hook queries recent sessions and injects the most recent meaningful one into context. The agent already knows what you worked on last time before you say a word. This is what makes the plan-in-one-session, implement-in-the-next workflow possible.

Second, on-demand search. A past-conversations skill lets the agent (or you) search conversation history by keywords, browse recent sessions, or run structured analyses like retrospectives and gap-finding. Ask "what did we decide about the API design?" and the agent searches your history.

The search works because the agent constructs the queries, not you. When you ask about "the database migration," the agent extracts the right keywords, sends them to FTS5, and iterates if the first results aren't good enough. The agent compensates for the simplicity of the storage layer. No vector database, no embedding pipeline, no external dependencies. Just SQLite and Python's standard library.

The plugin also includes an extract-learnings skill, a route from recall into archival memory. It reads past conversations, identifies non-obvious insights and gotchas worth preserving, and proposes placing them at the right layer in the memory hierarchy (CLAUDE.md, MEMORY.md, or topic files) with diffs and rationale. Learnings that would otherwise evaporate when context resets get distilled into persistent knowledge.

For the full story behind the architecture, I wrote about the design decisions and what I learned about how agents actually use memory: [What I Learned Building a Memory System for My Coding Agent](https://www.reddit.com/r/ClaudeCode/comments/1r1w397/comment/o5294lk/).

```
/plugin install claude-memory@claudest
```

---

### claude-utilities

Useful tools that don't fit in a specific plugin.

Currently includes **web-to-markdown**, which converts any webpage to clean markdown, stripping ads, navigation, popups, and cookie banners. Uses [ezycopy](https://github.com/gupsammy/EzyCopy) under the hood.

```bash
# Prerequisite
curl -sSL https://raw.githubusercontent.com/gupsammy/EzyCopy/main/install.sh | sh
```

Triggers on "convert this page to markdown", "extract this webpage", "save this article", "grab content from URL", "scrape this page".

```
/plugin install claude-utilities@claudest
```

---

## Contributing

This is a curated set of tools I personally maintain, not an open-submission marketplace. If you find bugs or have suggestions, open an issue. If you want to run your own marketplace with your own battle-tested tools, fork this and make it yours.

## License

MIT
