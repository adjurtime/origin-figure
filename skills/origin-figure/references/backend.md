# Origin backend

## Prerequisites

Require all of the following before figure execution:

- Windows with a licensed Origin or OriginPro installation.
- A configured Origin MCP server that exposes the required `origin_*` tools.
- The companion Origin Bridge running on a loopback endpoint.
- A task or session that has completed MCP tool discovery.

The skill does not distribute Origin, the Bridge, or the MCP server. Do not expose the Bridge endpoint to another host.

## Discover the active runtime

1. Inspect the current Codex MCP configuration and resolve the configured Origin server command without publishing user-profile paths, tokens, or status-file contents.
2. Resolve executables from configuration and the active project environment. Do not assume a drive letter, user directory, package manager location, port, or Origin version.
3. If the server belongs to a Python or uv project, inspect its `pyproject.toml`, lock file, virtual environment, and installed package versions before proposing a repair.
4. Keep the MCP server environment separate from Origin's embedded Python. Do not install packages into the Origin application directory or the system Python.
5. If Origin's embedded Python lacks a required data package, diagnose that environment separately. State the exact impact and rollback scope and obtain approval before installing or copying packages.

## Connection sequence

1. If the optional Origin MCP server is pending, wait for initialization to settle before deciding tools are missing.
2. Run the configured server's read-only status and doctor commands when available.
3. Confirm that `origin_*` tools are visible in the current task.
4. Call `origin_doctor`, then start Origin and the installed Bridge if necessary.
5. Call `origin_ping`, followed by `origin_capabilities`.
6. Use task-list or task-status tools after an ambiguous timeout.

If a repair succeeds but the host loads MCP tools only at task startup, keep Origin and the Bridge running and open a new task. Do not emulate missing Origin tools with terminal-driven GUI automation.

## Tool selection

Prefer task-visible typed tools in this order:

- Environment: `origin_doctor`, `origin_ping`, `origin_capabilities`
- Knowledge and planning: `origin_browse_knowledge`, `origin_query_knowledge`, `origin_plan_figure_spec`, `origin_execute_figure_spec`
- Data: `origin_import_table`, `origin_read_worksheet`, `origin_write_worksheet`, `origin_diagnose_worksheet`
- Plotting: `origin_recommend_chart`, `origin_plot`, `origin_plot_auto`, and specialized `origin_plot_*` tools
- Structure: `origin_add_plot_to_graph`, `origin_merge_graphs`, `origin_create_graph_layout`, `origin_link_graph_layers`
- Formatting: `origin_set_axis`, `origin_set_plot_style`, `origin_format_graph`, `origin_format_legend`
- QA and export: `origin_get_graph_info`, `origin_diagnose_graph`, `origin_view_graph`, `origin_export_graph`
- Project lifecycle: `origin_new_project`, `origin_open_project`, `origin_save_project`

Use `origin_run_labtalk` only for a narrowly scoped Origin-native gap. Explain what it changes, avoid filesystem wildcards, and verify the result afterward.

## Recovery boundaries

- Bridge not running: start Origin and the installed Bridge once, then repeat read-only diagnostics.
- Authentication or stale-token failure: restart the Bridge once, then rerun the doctor check.
- Timeout after mutation: inspect task and project state before retrying.
- Missing tools while startup is pending: wait for discovery to finish.
- Missing tools after a confirmed repair: open a new task when required by the host.
- Dependency or import failure: consult `compatibility.md`, then repair only the owning project environment after approval.
- Permission failure reading a status file: distinguish sandbox access from an actual Bridge failure; prefer task-visible diagnostics.
