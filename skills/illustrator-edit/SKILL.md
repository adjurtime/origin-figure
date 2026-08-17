---
name: illustrator-edit
description: Safely refine, assemble, and export existing vector artwork in Adobe Illustrator (.ai, .svg, .eps, or PDF), especially scientific figures exported by Python, R, MATLAB, Origin, GIS, or network software and then manually adjusted. Use when Codex must preserve manual label placement while adjusting typography, consolidating fragmented imported text, refining annotations or legends, assembling panels, editing layers or vector paths, or producing publication exports through Illustrator MCP. Do not use it to analyze raw data, choose statistical methods, or generate data-driven plots that should be reproducible in code.
---

# Illustrator Edit

Use Illustrator as the final vector-editing stage, not as the default data-plotting engine.

## Keep the Workflow Split

```text
data and analysis
→ Python / R / MATLAB / other analytical backend
→ SVG or PDF
→ Illustrator working copy
→ vector refinement and verified export
```

- Route data selection, transformations, statistics, axes, scales, uncertainty, mark generation, and repeatable plotting to `mse-figure` and the existing analytical code.
- Use this skill after the analytical figure is fixed, or for non-data vector artwork that already exists.
- Do not use Illustrator Graph tools as a default replacement for Python, R, or Origin. Use them only when the user explicitly requests a simple manually maintained chart.

## Honor a Manual Layout Master

If a figure was generated in code and then manually adjusted, treat the current SVG or AI file as the authoritative layout master.

- Do not rerun Python, R, MATLAB, or Origin merely to change fonts, spacing, labels, or other vector styling. Rerun analytical code only when data, axes, mappings, or results must change and the user authorizes it.
- Preserve manually placed label anchors, leader lines, and data geometry. A font change can alter glyph bounds; compensate only within the explicitly permitted text or legend objects.
- Never replace a manual layout with an automatically re-laid-out figure just because the code is reproducible.

## Freeze the Edit Contract

Record the exact objects and properties permitted to change before writing.

Normally permitted:

- text contents supplied by the user;
- fonts, sizes, spacing, alignment, and panel-label hierarchy;
- legend position and layout without changing category mapping;
- multi-panel assembly, margins, artboards, grouping, and layer visibility;
- non-analytical strokes, fills, paths, clipping masks, and annotations;
- PDF, SVG, EPS, AI, and raster review exports.

Require explicit authorization before changing:

- data marks, paths, bars, points, flows, or network geometry;
- axis values, limits, transformations, units, or tick labels;
- category identities or color, shape, and size mappings;
- thresholds, uncertainty, significance, exclusions, or statistical results.

For a data-backed scientific figure, keep the `mse-figure` evidence gate and visual QA requirements.

## Protect the Source

1. Resolve the exact source path and record its SHA-256 hash.
2. Copy the source to a task-specific temporary directory or approved output path.
3. Open only the copy and confirm `get_document_info.filePath` before saving or closing.
4. Prefer a one-time SVG/PDF-copy → AI-working-copy conversion. Do not repeatedly round-trip the source.
5. Call `save_document(mode="save")` only when the active path exactly equals the approved AI working copy.
6. Close the working document with `save=false` after the intended copy has been saved.
7. Re-hash the source at handoff.

If the active path is missing, ambiguous, or points to the source, stop before writing.

## Version Material Edits

- Before a substantial crop, panel rearrangement, typography hierarchy change, or label-layout pass, copy the latest verified AI file to the next sequential name: `_v1.ai`, `_v2.ai`, `_v3.ai`, and so on.
- Open and write only the new version. Never overwrite an earlier verified version during a material edit.
- Give review previews the same version stem. Keep internal moderate-resolution QA previews distinct from final publication exports.
- Record the parent version and the permitted edit contract before writing.

## Prefer the Quiet MCP

Use the registered `illustrator-silent` server when available. Its launcher in [scripts/silent_server.py](scripts/silent_server.py) copies the cached upstream package to a temporary runtime. In that copy it removes explicit foreground-activation flags, raises ordinary/heavy JSX timeouts to 90/240 seconds by default, routes native open/save/close through the heavy timeout, normalizes artboard coordinates, adds character-range text styling to `modify_object`, and registers `batch_modify_text`. It does not modify the installed package.

Check the existing setup before installing anything:

```bash
python3 scripts/silent_server.py --probe
codex mcp get illustrator-silent
```

Require the probe to report all of the following before editing:

- `runtime_activation_flags_remaining: 0`;
- the intended ordinary and heavy timeout values;
- `character_runs_enabled: true`;
- `safe_artboard_coordinates_enabled: true`;
- `batch_modify_text_enabled: true`;
- `open_uses_heavy_timeout`, `save_uses_heavy_timeout`, and `close_uses_heavy_timeout` as `true`.

Override the defaults only when justified:

```bash
python3 scripts/silent_server.py --probe --normal-timeout-ms 120000 --heavy-timeout-ms 300000
```

Do not install or upgrade Node, Python, npm packages, Illustrator, or other dependencies during an ordinary edit without approval. Use one MCP server process per task.

The launcher and registered tool set are not hot-reloaded. After changing this skill or wrapper, start a fresh MCP process before claiming that the new behavior is active.

When raw stdio diagnosis is unavoidable, use newline-delimited JSON-RPC. Do not use `Content-Length` framing or repeatedly start `npx` processes.

## Run One Controlled Edit Cycle

1. Open the approved working copy once.
2. Inspect path, artboards, layers, groups, text frames, fonts, and target UUIDs. Pass `coordinate_system` explicitly for every coordinate-bearing read or write.
3. Export a clean baseline PNG.
4. Apply the smallest coherent edit batch to the frozen target set. Use `batch_modify_text` for two or more text frames; use `modify_object` for a single frame or non-text object.
5. Export a moderate-resolution modified PNG and inspect the actual image.
6. Compare baseline and modified previews; require differences to be localized to permitted regions.
7. Save the AI working copy once, close it, reopen it, and export again.
8. Require the reopened preview to match the saved modified preview, or mark the discrepancy `待核验`.
9. Close without saving and verify the source hash.

Do not rely on `undo` as recovery. Close without saving and reopen the last verified AI working copy.

For `batch_modify_text`, inspect every returned item. If only some UUIDs fail, re-query those objects and retry only the failed subset; never replay a partially successful full batch blindly.

## Resize Artboards Without Guessing

The quiet runtime gives `manage_artboards` the same top-left rectangle contract used by `get_artboards`:

- `document`: `x` and `y` are the native Illustrator coordinates of the requested top-left corner; width extends right and height extends down;
- `artboard-web`: `x` and `y` are offsets right and down from the target artboard's current top-left corner.

Always call `get_artboards` with an explicit coordinate system, then call `manage_artboards` with that same coordinate system. Do not pass `rawPosition.y` into a document-coordinate resize formula. After resizing, require the verified position and size to equal the intended rectangle and export a fresh preview before moving artwork or saving.

The upstream 1.6.2 `manage_artboards` interface uses a different Y-origin convention. Do not bypass the quiet wrapper for artboard edits unless the conversion has been independently checked.

## Handle Imported Objects Carefully

- Use `list_fonts` and exact PostScript font names such as `ArialMT`; a family name such as `Arial` can fail.
- SVG imports can split formulas, subscripts, units, or rotated axis titles into single-character text frames.
- Prefer stable complete labels over fragmented text. Inspect contents, font, bounds, clipping, and layer before and after editing.
- When unifying a font family, use `list_fonts` to map existing regular, bold, italic, and bold-italic semantics to installed PostScript names in the target family. Do not flatten emphasis or hierarchy unless the user requests it. Assign the mapped font to every nonblank text frame, then require every nonblank frame to report the intended family after save and reopen. Preserve existing sizes unless the user requests a hierarchy change.
- Avoid ungrouping or outlining text unless the user explicitly accepts the loss of editability.
- Treat a whole-layout shift after SVG/PDF import as unresolved; do not correct it by eye against the source.

### Consolidate a Fragmented Logical Label

For a title or formula that should be one editable label:

1. Record the aggregate bounds or center of the visible fragments and identify the stable main text frame.
2. Put the complete logical text in that main frame.
3. Use `character_runs` for subscripts, superscripts, or mixed sizes instead of separate positioned frames. Indices are zero-based; `start` is inclusive and `end` is exclusive.
4. Recenter only the reconstructed label against its recorded aggregate bounds. Do not move country labels, data marks, axes, or leader lines.
5. Clear or remove obsolete fragments only after the reconstructed label renders correctly. If deletion is unavailable, leave them blank and report the residual blank-frame count.

Example for a final `2` that must be 7 pt inside a 10.8 pt title:

```json
{
  "uuid": "target-text-frame-uuid",
  "properties": {
    "contents": "Cross-border transfer (kt CO2)",
    "font_name": "TimesNewRomanPSMT",
    "font_size": 10.8,
    "character_runs": [
      {"start": 28, "end": 29, "font_size": 7, "baseline_shift": 0}
    ]
  }
}
```

Calculate the actual character indices from the final string; never copy example indices blindly. Verify the rendered result because baseline treatment varies by source artwork.

## Treat Foreground and Timeout Behavior Honestly

The quiet server can keep open, read, modify, and PNG export operations in the background. Illustrator may still surface itself during native save or close. Batch those operations once.

The upstream server's 30/60-second JSX limits are too short for some deeply nested scientific figures. The quiet wrapper uses 90/240 seconds by default and routes open/save/close through the heavy channel. Do not increase client timeouts while leaving shorter server timeouts unchanged.

If a tool times out after a visible action may already have occurred, do not repeat it. First inspect `get_document_info`; for a save, also compare the expected file's path, size, modification time, and hash, then reopen and render the candidate if the disk file changed. Retry only when the active path is verified and the expected disk file remained unchanged. If `open_document` times out from Illustrator's home screen, verify the UI and use an approved app-opening fallback only when needed; confirm the exact active path before any save.

`close_document(save=false)` can time out after the document has already closed. Re-probe with `get_document_info` before retrying; never close an unverified active document.

Read [references/known-limitations.md](references/known-limitations.md) when diagnosing focus changes, timeouts, font substitution, SVG fragmentation, or import/export instability.

## Handoff

Report:

- source and working-copy paths;
- parent and resulting version names for every material edit;
- permitted changes actually applied;
- source hash before and after;
- active-path verification before save;
- baseline-versus-modified difference bounds or an equivalent deterministic comparison;
- whether saved and reopened previews match;
- nonblank text-frame font counts, combined-title count, and any residual blank fragments after consolidation;
- visual QA result and any `待核验` issue.
