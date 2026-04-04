#!/usr/bin/env python3
"""
SessionEnd hook (matcher: clear) — writes a handoff file so the subsequent
SessionStart hook can hard-link to this session.

Receives session_id and cwd from the SessionEnd payload.
No stdout required — SessionEnd hooks don't consume output.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent / "skills" / "recall-conversations" / "scripts"))

from memory_lib.db import get_db_path, load_settings


def main():
    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except (json.JSONDecodeError, EOFError):
        return

    # Defensive: if matcher isn't filtering, check end_reason ourselves
    end_reason = hook_input.get("end_reason", "")
    if end_reason != "clear":
        return

    session_id = hook_input.get("session_id")
    cwd = hook_input.get("cwd")
    if not session_id or not cwd:
        return

    settings = load_settings()
    db_path = get_db_path(settings)
    handoff_path = db_path.parent / "clear-handoff.json"

    handoff = {
        "session_id": session_id,
        "cwd": cwd,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    try:
        handoff_path.write_text(json.dumps(handoff))
    except OSError:
        pass


if __name__ == "__main__":
    main()
