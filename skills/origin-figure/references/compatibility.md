# Compatibility and known failures

Treat every entry here as a dated compatibility record, not as a universal installation requirement. Discover and verify the current runtime before applying it.

## Known compatible snapshot

The following combination was verified on Windows with Origin 2026b in August 2026:

- `origin-mcp==0.1.4`
- `mcp==1.29.0`
- project constraint `mcp>=1.8,<2`
- Origin embedded Python 3.11

Other versions may work. Prefer current tool capabilities and the owning project's lock file over this snapshot.

## `mcp.server.fastmcp` import failure

`origin-mcp==0.1.4` imports `mcp.server.fastmcp`, which is absent from `mcp==2`. When the exact failure is `ModuleNotFoundError: No module named 'mcp.server.fastmcp'`:

1. Inspect the MCP server's owning Python or uv project and lock file.
2. Confirm the installed `origin-mcp` and `mcp` versions.
3. Propose the narrow project constraint `mcp>=1.8,<2` only for the affected `origin-mcp==0.1.4` environment.
4. State the lock-file and virtual-environment impact and obtain approval.
5. Verify both `import mcp.server.fastmcp` and `import origin_mcp.server` after synchronization.

Do not apply this constraint to unrelated projects, Origin's embedded Python, or the system Python.

## Task-start discovery

Some Codex hosts discover MCP tools when a task starts and cannot add repaired tools to an already running task. After a confirmed repair, keep Origin and the Bridge running and open a new task if the current task still lacks `origin_*` tools.

Do not treat a temporarily pending optional server as a permanent registration failure. Wait for initialization to settle and verify the final tool list.

## Optional spreadsheet audit dependency

`scripts/audit_origin_artifacts.py` requires `openpyxl` only when `--xlsx` is used. CSV, SVG, OPJU, and generic reference inspection use the Python standard library. If `openpyxl` is missing, report the optional dependency and follow the current environment-approval policy; never install it automatically.

## Unicode staging paths

Some package-target operations can stall on lock files under non-ASCII paths. If a binary-compatible target must be built after approval, use an ASCII-only staging directory, verify it, and copy only the approved packages to the intended environment.
