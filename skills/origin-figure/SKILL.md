---
name: origin-figure
description: "Create, revise, audit, and save editable publication figures in Origin or OriginPro on Windows from tabular data, OPJU, SVG, and image references. Use for Origin画图, 论文配图, existing-OPJU revisions, Word-sized layouts, typography, labels, multi-panel figures, and requested vector or raster exports. Require Origin-native worksheet bindings and persistence verification; do not use another renderer for the final graph."
---

# Origin Figure

Make paper-ready Origin figures with authoritative data, worksheet bindings, and editability. Work on one figure at a time.

## Use the publication defaults

- Treat tabular inputs as quantitative authority and images as visual references. Never invent or silently repair scientific values.
- For English paper figures, default to Times New Roman at 10.5 pt at the final physical size. Set the Origin page to the intended Word insertion size so later scaling does not change the effective font size. Explicit user, journal, or project requirements override these defaults.
- Reuse an accepted project style for typography, axes, palette, legends, panel labels, and spacing.
- Save an editable `.opju` when the graph is ready for review. Do not export by default. After user feedback, export only the requested formats; prefer SVG for vector delivery and use 600 dpi PNG when raster output is requested.
- Protect source files and existing OPJU files. Preserve manual Origin edits and save revisions separately unless replacement is authorized.

## Match the work to the request

1. Use **audit mode** for read-only inspection.
2. Use **create mode** for new data, formulas, or graph structure. Audit headers, units, order, blanks, and formula caches.
3. Use **revise mode** for visual changes to an existing OPJU. Read only the current graph and affected objects; skip full-workbook audits unless data or structure changes.

## Execute compactly in Origin

1. Confirm the backend once per task with `origin_doctor`, `origin_ping`, and `origin_capabilities`; repeat only after failure. If tools are pending or unavailable, read `references/backend.md`.
2. Prefer typed `origin_*` tools. Use narrow LabTalk only for an Origin-native gap that can be checked afterward.
3. Bind every scientific series and data label to worksheet columns. Preserve blanks and rebuild uncached derived values from authoritative columns.
4. Apply structure before styling. Submit small serial mutation batches and read back only changed state. Treat timeouts as unknown state and inspect before retrying.
5. Request counts, roles, limits, changed properties, and representative values instead of full worksheets or redundant JSON.

## Verify proportionately

- For an intermediate visual revision, render a preview and perform delta QA on the changed properties and bindings.
- At a stable OPJU handoff, save, reopen, and verify the expected worksheets, layers, plots, and bindings. Mark blocked checks as `unverified`.
- When export is requested, inspect only the requested files for size, dimensions, parsing, clipping, overlap, and freshness relative to the OPJU.
- Do not claim completion from a successful save, file hash, preview, or stale export alone.

## Load details only when needed

- Read `references/recipes.md` only when the native graph construction is uncertain.
- Read `references/qa.md` only for stable handoff or final export acceptance.
- Read `references/compatibility.md` only for a matching version or dependency failure.
- Run `scripts/audit_origin_artifacts.py` for new or changed inputs and final artifact checks, not for routine style-only revisions.
