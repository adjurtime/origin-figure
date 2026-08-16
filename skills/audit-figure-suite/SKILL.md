---
name: audit-figure-suite
description: "Audit a paper's complete figure set and each multi-panel figure for scientific, visual, typographic, geometric, and delivery consistency. Use for 整套论文图检查, 同一图内子图检查, 子图编号和横纵坐标对齐, 图1到图N统一, 投稿前图件校对, multi-panel alignment, figure suite audit, or read-only comparison of OPJU, SVG, PDF, PNG, captions, and source tables. Default to read-only reporting; hand approved single-figure Origin fixes to origin-figure."
---

# Audit Figure Suite

Audit a paper's figures as one evidence and visual system. Remain read-only unless the user separately approves a fix.

## Select the audit mode

- Use **baseline mode** to derive or confirm the suite-wide specification before figures are revised.
- Use **audit mode** to compare the current figures, captions, sources, and deliverables against that specification.
- Use **recheck mode** to verify only approved fixes and previously failed checks.

If the user asks to correct findings, finish the audit first, present the smallest per-figure fix plan, and use `$origin-figure` one figure at a time after approval.

## Establish authority and scope

1. Use supplied data and analytical outputs for values, the current manuscript and captions for terminology, and explicit user, verified journal, and approved suite rules for presentation. Prefer current evidence over memory or older figures.
2. Inventory only the figures in scope: figure and panel IDs, panel row and column, scientific role, axis and scale groups, captions, source tables, OPJU files, previews or exports, intended physical sizes, and declared exceptions.
3. Treat tables and analytical outputs as quantitative authority. Treat screenshots, PDFs, and raster images as visual evidence only.
4. Mark missing evidence as `unverified`; do not infer an editable OPJU, data binding, uncertainty definition, or current export from appearance alone.

## Run the audit

1. Read `references/figure-suite-standards.md` and freeze the explicit rules and justified exceptions. If a reusable specification is requested, copy and fill `assets/figure-suite-spec.yaml`; never edit the template itself.
2. Check scientific integrity before appearance: source identity, units, transformations, denominators, category and year order, uncertainty, and representative plotted values.
3. Audit every multi-panel figure internally before comparing figures. Verify the approved panel-label format, sequence, caption linkage, anchor, offset, and typography. Default to lowercase half-width `(a)`, `(b)`, `(c)` in row-major order and anchor labels to the plot-area top-left unless overridden.
4. Compare panel geometry: equal plot rectangles when comparable, X-axis baselines by row, Y-axis baselines by column, shared scale ranges and ticks, zero positions, axis-title offsets, gutters, outer margins, and legend or colourbar effects.
5. For Origin figures, query worksheet, layer, plot, label, binding, layer position and size, axis range, and tick state when tools are available. Require equal values for properties declared shared unless the specification defines a tolerance. A file hash or preview is not semantic evidence.
6. Inspect actual previews at final physical size, first within each multi-panel figure and then across the suite. Check visual alignment as well as typography, colours, marks, legends, labels, whitespace, accessibility, and caption terminology.
7. Verify delivery state only for requested artifacts: naming, version lineage, dimensions, freshness, clipping, parsing, and OPJU persistence.
8. Record scientific or journal reasons for legitimate differences. Do not force identical scales, geometry, palettes, or density where the evidence requires different treatment.

## Classify findings

- **Blocker:** incorrect or untraceable data, misleading scale or encoding, broken binding, wrong unit or caption linkage, clipped essential content, or persistence that remains unverified for a claimed final deliverable.
- **Major:** wrong, missing, misordered, or inconsistently placed panel labels; visibly misaligned comparable plot rectangles or axis baselines; cross-figure semantic conflict; unreadable final-size text; inconsistent comparable scales; inaccessible colour encoding; or missing required panel or legend content.
- **Minor:** small spacing, offset, tick-density, or label-hierarchy drift that remains readable and does not break the intended comparison.
- **Unverified:** evidence or tool access is insufficient; never convert this to a pass.

## Report compactly

Lead with the suite-level conclusion. Then provide:

1. the confirmed baseline and exceptions;
2. a figure-by-panel matrix for every multi-panel figure, with geometry and label checks marked `pass`, `fail`, or `unverified`;
3. a cross-figure matrix with `pass`, `fail`, or `unverified`;
4. findings ordered by severity, each with evidence and affected figures or panels;
5. the smallest revision sequence, grouped by global rule and then one figure at a time;
6. checks to rerun after correction.

Do not modify figures, captions, source data, OPJU files, exports, or external state during an audit-only request.
