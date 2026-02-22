---
name: youtube-research
description: >
  This skill should be used when the user asks to "search YouTube", "find videos about",
  "get a transcript", "download subtitles", "extract audio from YouTube", "scan a channel",
  "research a topic on YouTube", "get video metadata", "what videos exist about",
  "download YouTube audio", "YouTube research", or provides a YouTube/Vimeo/video URL
  and wants to extract information from it. Also triggers on "batch download transcripts",
  "analyze a channel", or any multi-video research workflow.
argument-hint: "<url-or-query>"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(python3:*)
  - Bash(yt-dlp:*)
  - Bash(jq:*)
  - Bash(cat:*)
  - AskUserQuestion
  - WebSearch
  - Task
---

# YouTube Research

Multi-platform video research toolkit. Operates in two modes: toolkit (individual operations)
and research (autonomous search-to-synthesis pipeline). All operations use a single CLI at
`${CLAUDE_PLUGIN_ROOT}/skills/youtube-research/scripts/yt_research.py`.

## Toolkit Mode

Invoke individual subcommands for targeted operations. Default mode when the user requests
a specific action (transcript, search, metadata, audio, channel scan).

### Search

Find videos matching a query. Returns structured results with metadata.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-research/scripts/yt_research.py search "<query>" --count 10
```

Add filters to narrow results: `--min-duration 600` (seconds), `--after 20250101` (YYYYMMDD),
`--min-views 50000`. Filters are applied client-side after fetching, so the tool over-fetches
automatically to compensate. Output is JSON by default; add `-f text` for human-readable.

### Transcript

Download and clean subtitles to LLM-ready text.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-research/scripts/yt_research.py transcript "<url>"
```

Outputs clean prose to stdout by default. Add `--timestamps` for SRT with timing cues.
Add `--save -t <topic>` to persist to `~/youtube-research/<topic>/`. Use `--lang all` to
list available subtitle languages before downloading. Fallback chain: manual subs then
auto-generated. Exit 4 if no subtitles exist in the requested language.

After extracting a transcript, read the output and summarize key points for the user
unless they asked for raw output only.

### Metadata

Extract full video information without downloading.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-research/scripts/yt_research.py metadata "<url>"
```

Returns: title, description, channel, duration, chapters, view/like counts, tags, available
subtitle languages, thumbnail URL. Add `--playlist` for playlist entry listings.

### Audio

Download audio in the requested format.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-research/scripts/yt_research.py audio "<url>" --audio-format mp3 -t <topic>
```

Saves to `~/youtube-research/<topic>/audio/`. Supported formats: mp3, m4a, opus, wav.
Always saves to disk (audio cannot go to stdout). Prints the file path on success.

### Channel

Scan a channel's content.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-research/scripts/yt_research.py channel "<url-or-@handle>" --limit 20
```

Supports tabs: `--tab videos` (default), `shorts`, `streams`, `playlists`. Filter with
`--after`/`--before` (YYYYMMDD). Sort with `--sort views` for most-viewed-first.

### Batch Processing

Any subcommand except `search` accepts `--batch <file>` (or `--batch -` for stdin) to
process multiple URLs. One URL per line; lines starting with `#` or `;` are skipped.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-research/scripts/yt_research.py transcript --batch urls.txt --save -t <topic>
```

### Global Flags

| Flag | Purpose |
|------|---------|
| `-f json/text` | Output format (default: json for search/metadata/channel, text for transcript) |
| `-t <topic>` | Topic subdirectory for saved files |
| `-d <path>` | Override base dir (default: ~/youtube-research) |
| `--cookies <browser>` | Browser cookie auth for age-restricted content |
| `-q` | Suppress progress messages |
| `--dry-run` | Show yt-dlp command without executing |

## Research Mode

Activate when the user asks to "research", "investigate", or "find out about" a topic
using YouTube as a source. This is an autonomous multi-step pipeline:

1. Search for the topic with broad terms, request 15-20 results
2. Evaluate results: read titles, channels, view counts, durations. Select the 3-5
   most relevant based on: authority of channel, view count as quality signal,
   duration appropriate to depth needed, recency
3. Extract metadata for selected videos to confirm relevance (check descriptions, chapters)
4. Download transcripts for the final selection
5. Read each transcript and synthesize findings into a structured report covering:
   key takeaways across videos, points of agreement/disagreement between sources,
   unique insights from specific videos, and gaps in coverage

Present the report with source attribution (video title + timestamp if available).
Save all transcripts under the topic directory for future reference.

### Research Mode Composability

Chain operations for complex queries:

```bash
# Search, filter, extract transcripts
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-research/scripts/yt_research.py search "topic" --count 20 \
  | jq -r '.[].url' \
  | python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-research/scripts/yt_research.py transcript --batch - --save -t topic
```

## Platform Notes

YouTube is the primary platform, but any yt-dlp-supported URL works. See
`references/platforms.md` for platform-specific behavior and limitations.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Usage error |
| 2 | yt-dlp not found |
| 3 | Network/download error |
| 4 | No results or no subtitles |
