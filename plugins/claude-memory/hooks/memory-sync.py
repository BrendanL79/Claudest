#!/usr/bin/env python3
"""Stop hook - background sync for current session."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def main():
    try:
        # Read hook input from stdin
        hook_input = sys.stdin.read()

        # Write to temp file (cross-platform stdin piping to detached process is unreliable)
        fd, tmp_path = tempfile.mkstemp(prefix="claude-memory-sync-", suffix=".json")
        with open(fd, "w") as f:
            f.write(hook_input)

        # Background the sync
        kwargs = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
        if sys.platform == "win32":
            kwargs["creationflags"] = (
                subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
            )
        else:
            kwargs["start_new_session"] = True
        subprocess.Popen(
            [sys.executable, str(SCRIPT_DIR / "sync_current.py"), "--input-file", tmp_path],
            **kwargs
        )
    except Exception:
        pass

    print(json.dumps({"continue": True}))


if __name__ == "__main__":
    main()
