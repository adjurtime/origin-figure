---
name: origin-figure
description: "Create, redraw, revise, audit, and export editable Origin or OriginPro scientific figures on Windows from XLSX, XLSM, CSV, OPJU, SVG, and image references. Use for Origin画图, Origin作图, 论文配图, 科研绘图, 图形重绘, publication figures, grouped or stacked columns, multi-panel scatter or line-symbol charts, source-data and formula preservation, OPJU/SVG delivery, or inspection of an existing Origin project. Require Origin-native data bindings and final Origin verification; do not use matplotlib or another renderer for the final figure."
---

# Origin Figure

Build publication-ready figures in Origin while keeping the source data, graph objects, and saved project editable. Treat a rendered preview as visual evidence, not as the final artifact.

## Choose the operating mode

1. Use **audit mode** to inspect inputs, an existing OPJU, or exported graphics without modifying them.
2. Use **create mode** to build a new worksheet, graph, OPJU, and SVG from authoritative source data.
3. Use **revise mode** to inspect an existing OPJU and save revisions separately unless overwriting is explicitly authorized.
4. Follow the current user request, project instructions, and approval policy before applying any mutation.

## Establish authority and scope

1. When authority is not specified, use XLSX, XLSM, or CSV as the quantitative authority; use SVG or an image as the visual target; use Python only as a design reference.
2. Never invent, interpolate, silently repair, or relabel scientific values. Mark missing or ambiguous facts as `unverified`.
3. Work on one figure at a time unless the user explicitly requests a batch.
4. Keep source workbooks, SVGs, images, scripts, and existing OPJU files unchanged. Save outputs separately unless replacement is explicitly authorized.

## Run the privacy-safe preflight

1. Locate the exact inputs and intended output directory.
2. Run `scripts/audit_origin_artifacts.py` with the relevant `--xlsx`, `--csv`, `--svg`, `--opju`, or `--reference` arguments. Its default output must remain privacy-safe: basenames, hashes, dimensions, counts, and geometry only.
3. Use `--include-preview`, `--include-formulas`, or `--full-paths` only when those details are necessary and permitted to appear in tool output.
4. Treat `openpyxl` as an optional XLSX/XLSM-audit dependency. If it is absent, report that limitation; do not install or alter an environment without approval. CSV, SVG, OPJU, and reference audits must remain usable without it.
5. Inspect headers, units, missing cells, category order, and formula semantics. If formula cells lack cached values, trace the upstream raw data and plan explicit derived columns in Origin instead of importing blanks or formula text as numbers.
6. State the proposed data-to-plot mapping, chart geometry, and output filenames before mutation when the current approval policy requires it.

## Confirm the Origin backend

1. Allow a pending Origin MCP server to finish initialization before deciding tools are absent.
2. Require task-visible `origin_*` tools and call `origin_doctor`, `origin_ping`, and `origin_capabilities` before mutating Origin.
3. If the tools or Bridge are unavailable, follow `references/backend.md`. Read `references/compatibility.md` only for version-specific failures.
4. If the host discovers MCP tools only at task startup, open a new task after an approved repair. Do not replace Origin control with terminal-driven mouse or keyboard automation.
5. Prefer typed Origin tools. Use `origin_run_labtalk` only for a narrow Origin-native gap that can be inspected and verified afterward.

## Build or revise in Origin

1. Open or create the project with Origin project tools.
2. Import the authoritative table without changing the source. Preserve category order, units, long names, comments, and meaningful blank cells.
3. When formula caches are missing, import upstream raw columns, rebuild derived columns with explicit Origin formulas or calculated-column tools, and verify representative rows.
4. Assign X, Y, error, and label roles explicitly. For a structurally complex figure, inspect `origin_plan_figure_spec` before executing it.
5. Choose the smallest Origin-native construction from `references/recipes.md`. Keep every scientific series and data label bound to worksheet data; never simulate data with drawing objects.
6. Match structure before cosmetics: layers, grouping, stacking, axes, scales, ticks, labels, and legends precede colors, fonts, markers, and line widths.
7. Save an editable `.opju` and export a vector `.svg`.

## Verify before claiming completion

1. Read back worksheet values, blanks, labels, and column designations.
2. Inspect graph layers, plots, data bindings, axes, legends, and text objects with Origin graph information and diagnostic tools.
3. Render the graph and inspect it at normal size and close zoom.
4. Reopen the saved OPJU and re-query it. If reopening or binding verification is blocked, mark editability as `unverified`.
5. Run `scripts/audit_origin_artifacts.py --require-outputs` on the OPJU and SVG, then apply `references/qa.md`.
6. Report exact output paths only in the final delivery context, together with verified facts, limitations, and unresolved visual judgment.

## Handle failures safely

- Treat a timeout after a mutating call as an unknown state. Inspect task status, project contents, and output files before retrying.
- Never blindly replay a non-idempotent import, plot, merge, save, or export operation.
- Preserve partial artifacts for diagnosis unless replacement or deletion is authorized.
- If the backend cannot be recovered safely, stop and report the exact failed check and shortest recovery step.

## References

- Read `references/backend.md` for discovery, connection, recovery, and tool selection.
- Read `references/compatibility.md` only for known version or environment failures.
- Read `references/recipes.md` when choosing an Origin-native chart structure.
- Read `references/qa.md` before final acceptance.
