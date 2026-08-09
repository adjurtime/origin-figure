# Origin Figure Skill

A reusable Origin and OriginPro scientific-figure skill for Codex and compatible Agent Skills hosts.

## Included skill

### `origin-figure`

Create, revise, audit, and export editable scientific figures with Origin or OriginPro on Windows. The workflow preserves source-data authority, worksheet-to-graph bindings, editable OPJU projects, and vector SVG delivery.

The skill supports:

- XLSX, XLSM, and CSV source tables
- OPJU projects, SVG targets, and image references
- grouped and stacked columns
- multi-panel scatter and line-symbol figures
- formula-cache diagnostics
- Origin-native structural, visual, and persistence verification

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
Use $origin-figure to build and verify an editable Origin figure from my workbook and SVG reference.
```

Or describe an Origin plotting task naturally. The skill supports three operating modes:

- **Audit:** inspect source data, OPJU, or SVG artifacts without modification.
- **Create:** build a new Origin worksheet, graph, OPJU, and SVG.
- **Revise:** inspect an existing OPJU and save a separately verified revision unless replacement is authorized.

## Privacy-safe artifact audit

The bundled script reports basenames, hashes, dimensions, counts, and SVG geometry by default:

```powershell
python skills/origin-figure/scripts/audit_origin_artifacts.py `
  --xlsx path/to/source.xlsx `
  --svg path/to/reference.svg
```

Potentially sensitive details are opt-in:

- `--include-preview` includes bounded workbook headers or CSV rows.
- `--include-formulas` includes bounded formula text and coordinates.
- `--full-paths` includes resolved absolute paths.

The script imports `openpyxl` only when `--xlsx` is used. CSV, SVG, OPJU, and generic reference audits use the Python standard library.

## Verification boundary

A successful file audit does not prove that an OPJU is editable or correctly bound. Formal completion requires reopening the project in Origin and querying its worksheet, graph objects, and data bindings through the Origin integration.

## License

MIT. See [`LICENSE`](LICENSE).

Origin and OriginPro are products of OriginLab Corporation. This project is independent and does not redistribute proprietary Origin software.
