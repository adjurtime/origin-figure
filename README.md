# Origin Figure Skills

A pair of scientific-figure skills for Codex and compatible Agent Skills hosts: one edits a single Origin figure, and one audits a complete paper figure suite.


## Included skills

### `origin-figure`

Create, revise, audit, and save editable publication figures with Origin or OriginPro on Windows. The workflow preserves source-data authority, worksheet-to-graph bindings, editable OPJU projects, and export-on-request delivery.

The skill supports:

- XLSX, XLSM, and CSV source tables
- OPJU projects, SVG targets, and image references
- grouped and stacked columns
- multi-panel scatter and line-symbol figures
- Word-sized layouts with paper-ready typography
- formula-cache diagnostics
- compact Origin-native structural, visual, and persistence verification
- SVG or 600 dpi PNG export when requested

### `audit-figure-suite`

Audit a paper's complete figure set without changing source files. The workflow establishes a shared figure specification, checks scientific and visual consistency, records justified exceptions, and returns a severity-ranked revision plan for one-figure-at-a-time execution.

The default visual baseline uses Times New Roman at final Word size, no minor ticks or gridlines, short outward major ticks, restrained semantic colours, consistent panels and labels, and Origin binding and persistence checks when OPJU files are available.

## Requirements

- Windows
- A licensed Origin or OriginPro installation for `origin-figure` and OPJU semantic checks
- A working Origin MCP and Bridge configuration that exposes the required `origin_*` tools for editable Origin work
- Python 3.10 or newer to run the bundled audit script
- Optional: `openpyxl` for XLSX or XLSM audits

This repository does not distribute Origin, OriginPro, the Origin Bridge, or an MCP server. See [`compatibility.md`](skills/origin-figure/references/compatibility.md) for the tested compatibility snapshot and known version-specific failures.

## Install

### Install with Codex

Ask Codex to install either skill from:

```text
https://github.com/adjurtime/origin-figure/tree/main/skills/origin-figure
https://github.com/adjurtime/origin-figure/tree/main/skills/audit-figure-suite
```

For example:

```text
$skill-installer install the origin-figure skill from https://github.com/adjurtime/origin-figure/tree/main/skills/origin-figure
$skill-installer install the audit-figure-suite skill from https://github.com/adjurtime/origin-figure/tree/main/skills/audit-figure-suite
```

### Install manually

Copy `skills/origin-figure` to one of the skill locations recognized by your host:

- User scope: `~/.agents/skills/origin-figure`
- Project scope: `<project>/.agents/skills/origin-figure`

Restart the host if the skill does not appear immediately.

## Use

Invoke the skill explicitly:

```text
Use $origin-figure to create or revise an editable, Word-sized paper figure in Origin and export only when I request it.

Use $audit-figure-suite to audit this paper's complete figure set without editing the source files.
```

Or describe an Origin plotting task naturally. The skill supports three operating modes:

- **Audit:** inspect source data, OPJU, or SVG artifacts without modification.
- **Create:** build a new Origin worksheet, graph, and editable OPJU; export only when requested.
- **Revise:** inspect only the affected state in an existing OPJU, save a revision, and use delta QA unless data or structure changes.

## Portable artifact audit

The bundled script reports a compact, environment-neutral summary by default: basenames, hashes, dimensions, counts, and SVG geometry.

```powershell
python skills/origin-figure/scripts/audit_origin_artifacts.py `
  --xlsx path/to/source.xlsx `
  --svg path/to/reference.svg
```

Machine- and dataset-specific details remain fully available when needed:

- `--include-preview` includes bounded workbook headers or CSV rows.
- `--include-formulas` includes bounded formula text and coordinates.
- `--full-paths` includes resolved absolute paths.

These switches keep default logs portable across different computers; they do not remove any audit capability from the shared skill.

The script imports `openpyxl` only when `--xlsx` is used. CSV, SVG, OPJU, and generic reference audits use the Python standard library.

## Verification boundary

A successful file audit does not prove that an OPJU is editable or correctly bound. Formal completion requires reopening the project in Origin and querying its worksheet, graph objects, and data bindings through the Origin integration.

## Update log

### 2026-08-16

- Added a concise default style for single Origin figures: no minor ticks or gridlines, short outward major ticks, restrained semantic colours, and consistent final-size typography and layout.
- Added `audit-figure-suite` for read-only, paper-wide scientific and visual consistency review.
- Added a reusable suite specification template covering axes, typography, semantic encodings, layout, Origin persistence, delivery, and justified exceptions.

### 2026-08-11

- Reduced the core skill from about 860 to 536 words so routine Origin work loads less instruction context.
- Added paper defaults for English figures: Times New Roman at 10.5 pt at the final physical size and an Origin page sized to the intended Word placement.
- Changed delivery to save an editable OPJU for review first; SVG or 600 dpi PNG is exported only after feedback or an explicit request.
- Split full create-mode audits from compact revise-mode checks so visual edits do not repeatedly scan entire workbooks.
- Required small serial mutation batches, delta readback, and concise tool output instead of redundant full worksheet or diagnostic payloads.
- Updated the skill metadata and default prompt to match the streamlined workflow.

## License

MIT. See [`LICENSE`](LICENSE).

Origin and OriginPro are products of OriginLab Corporation. This project is independent and does not redistribute proprietary Origin software.
