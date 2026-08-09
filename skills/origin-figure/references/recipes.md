# Origin-native figure recipes

Choose the simplest native structure that preserves data bindings and editability. Derive exact values and styling from the current inputs; do not bake old project values into a new figure.

## Grouped plus stacked columns

Use for a category containing multiple peer bars where one peer is itself decomposed into stacked components.

1. Import category labels and every component as separate worksheet columns.
2. Verify whether the intended reading is grouped-within-category, stacked-within-bar, or both.
3. Keep the construction in one layer when a shared axis and common category spacing are required.
4. Use the specialized column/stack tools for the native base plot. When a single typed call cannot express mixed grouping and stacking, compose plots in the same graph or use a planned, narrowly scoped LabTalk operation.
5. Set grouping, stack subgroup, overlap, gap, and column width explicitly. Do not simulate a scientific bar with rectangles.
6. Hide any structural filler series from both the graph and legend; never let it alter totals.
7. Verify each stack total and legend order against the worksheet.

## 100% stacked bars or columns

1. Decide whether normalization is already authoritative in the workbook. Prefer supplied percentages.
2. If normalization must be calculated, retain both raw and derived values in labeled worksheet columns and document the formula.
3. Plot component columns with a shared stack designation.
4. Fix the percentage axis to the intended domain, normally 0–100%, only when supported by the data definition.
5. Check that each category sums to the expected total within a stated numerical tolerance.

## Multi-panel scatter

1. Use one layer per panel and share or link axes only when the scientific comparison requires it.
2. Preserve identical scale and physical layer size for comparable panels.
3. Map point labels from an explicit worksheet label column. Label selected observations only; do not manually type data labels into the graph.
4. Keep marker size, fill, border, and transparency consistent unless the data encoding requires variation.
5. Create a graph layout, align layer rectangles, then verify panel letters and common axis titles.

## Line plus symbol with gaps

1. Map X and each Y series explicitly and sort only if the source semantics permit it.
2. Preserve authoritative blank cells as gaps. Do not convert missing values to zero or silently connect across them.
3. Use line and symbol properties as separate encodings. Avoid excessive smoothing.
4. Check axis type and units, especially date, categorical, log, or percentage axes.
5. Verify endpoints, missing runs, series order, and legend labels from worksheet values.

## General multi-panel layout

1. Build and verify each panel graph before merging.
2. Merge or create the layout with explicit rows, columns, margins, and spacing.
3. Link axes only after the intended independent/shared scale behavior is clear.
4. Apply common typography and line weights after layer geometry is stable.
5. Inspect at final export dimensions so labels, markers, and whitespace are judged at publication scale.
