# Scientific Figure Skills

Reusable Codex and Agent Skills for producing, refining, and auditing publication figures. The repository separates reproducible plotting from final vector editing and paper-wide quality control.

## Included skills

| Skill | Best used for | Platform and software |
| --- | --- | --- |
| [`origin-figure`](skills/origin-figure/) | Creating or revising editable, data-bound figures in Origin/OriginPro | Windows, licensed Origin/OriginPro, and a compatible Origin MCP/Bridge |
| [`illustrator-edit`](skills/illustrator-edit/) | Refining an existing SVG, PDF, EPS, or AI file while preserving manually adjusted layouts | macOS, Adobe Illustrator, and a configured `illustrator-mcp-server` |
| [`audit-figure-suite`](skills/audit-figure-suite/) | Read-only scientific and visual consistency review across a paper's full figure set | Cross-platform for portable files; Origin is needed only for semantic OPJU checks |

## Recommended workflow

```text
data and analysis
→ Python / R / MATLAB / Origin
→ SVG or PDF
→ Illustrator vector refinement
→ final export and paper-wide audit
```

Keep data transformations, statistics, axes, scales, and data marks reproducible in analytical code or Origin. Use Illustrator for the final vector stage: typography, labels, legends, panel assembly, annotations, and export. If an exported figure was manually adjusted, `illustrator-edit` treats that vector file as the layout master and does not rerun plotting code for style-only changes.

## Install

Ask Codex to install the skill you need from its repository path:

```text
$skill-installer install the origin-figure skill from https://github.com/adjurtime/scientific-figure-skills/tree/main/skills/origin-figure

$skill-installer install the illustrator-edit skill from https://github.com/adjurtime/scientific-figure-skills/tree/main/skills/illustrator-edit

$skill-installer install the audit-figure-suite skill from https://github.com/adjurtime/scientific-figure-skills/tree/main/skills/audit-figure-suite
```

For manual installation, copy the selected directory from `skills/` into a skill location recognized by your host, such as `~/.agents/skills/<skill-name>` or `<project>/.agents/skills/<skill-name>`. Restart the host if the skill does not appear immediately.

## Use

Invoke a skill explicitly or describe the task naturally:

```text
Use $origin-figure to revise this editable Origin figure and save the OPJU before exporting.

Use $illustrator-edit to unify the typography in this manually adjusted SVG without moving labels or changing data geometry.

Use $audit-figure-suite to audit this paper's complete figure set without editing the source files.
```

### `origin-figure`

Supports XLSX, XLSM, CSV, OPJU, SVG, and image references; editable worksheet-to-graph bindings; grouped or stacked columns; multi-panel scatter and line-symbol figures; final-size typography; persistence checks; and SVG or 600 dpi PNG export on request.

See [`compatibility.md`](skills/origin-figure/references/compatibility.md) for the tested compatibility snapshot and known version-specific failures. This repository does not distribute Origin, OriginPro, the Origin Bridge, or an MCP server.

### `illustrator-edit`

Protects the source file, edits a verified working copy, freezes which objects may change, compares before-and-after previews, and verifies the saved artwork after reopening. It also handles common scientific-figure problems such as fragmented SVG text, exact PostScript font mapping, panel assembly, and publication export.

The bundled quiet launcher creates a temporary runtime copy of the cached upstream MCP package. In that copy it reduces avoidable Illustrator foreground activation, extends JSX timeouts for complex scientific SVGs, and enables character-range styling for consolidated labels. It does not modify the installed package. See [`known-limitations.md`](skills/illustrator-edit/references/known-limitations.md) for the tested behavior and recovery rules.

### `audit-figure-suite`

Establishes a shared figure specification, checks scientific and visual consistency, records justified exceptions, and returns a severity-ranked revision plan for one-figure-at-a-time execution. It does not change source files.

## Portable Origin artifact audit

The Origin skill includes a compact, environment-neutral audit script:

```powershell
python skills/origin-figure/scripts/audit_origin_artifacts.py `
  --xlsx path/to/source.xlsx `
  --svg path/to/reference.svg
```

By default it reports basenames, hashes, dimensions, counts, and SVG geometry. Optional switches expose bounded workbook previews (`--include-preview`), formula text (`--include-formulas`), or absolute paths (`--full-paths`). `openpyxl` is imported only for XLSX or XLSM input; CSV, SVG, OPJU, and generic-reference audits use the Python standard library.

A successful portable audit does not prove that an OPJU is editable or correctly bound. Formal completion requires reopening it in Origin and querying worksheet, graph, and binding state through the Origin integration.

## Update log

### 2026-08-16

- Renamed the repository from `origin-figure` to `scientific-figure-skills`.
- Added `illustrator-edit` for source-safe refinement of manually adjusted scientific vector artwork.
- Reorganized the README around the plotting, vector-editing, and figure-suite-audit workflow.
- Added `audit-figure-suite` and a reusable suite specification for scientific and visual consistency review.
- Added concise defaults for single Origin figures, including final-size typography, short outward major ticks, no minor ticks or gridlines, and restrained semantic colours.

### 2026-08-11

- Streamlined the core Origin skill and separated full create-mode audits from compact revise-mode checks.
- Added final-size English typography defaults and save-first, export-on-request delivery.
- Required small mutation batches, delta readback, and concise tool output.

## License

MIT. See [`LICENSE`](LICENSE).

Origin and OriginPro are products of OriginLab Corporation. Adobe Illustrator is a product of Adobe Inc. This independent project does not distribute or replace proprietary software from either company.
