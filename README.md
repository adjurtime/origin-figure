# Origin Figure Skill

A reusable Origin and OriginPro scientific-figure skill for Codex and compatible Agent Skills hosts.


## Included skill

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

## Requirements

- Windows
- A licensed Origin or OriginPro installation
- A working Origin MCP and Bridge configuration that exposes the required `origin_*` tools
- Python 3.10 or newer to run the bundled audit script
- Optional: `openpyxl` for XLSX or XLSM audits

This repository does not distribute Origin, OriginPro, the Origin Bridge, or an MCP server. See [`compatibility.md`](skills/origin-figure/references/compatibility.md) for the tested compatibility snapshot and known version-specific failures.

## Install

### Install with Codex

Ask Codex to install the skill from:

```text
https://github.com/adjurtime/origin-figure/tree/main/skills/origin-figure
```

For example:

```text
$skill-installer install the origin-figure skill from https://github.com/adjurtime/origin-figure/tree/main/skills/origin-figure
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
