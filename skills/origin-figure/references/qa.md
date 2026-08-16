# Acceptance checklist

Apply every relevant check. A plausible preview or successful file-level audit is not sufficient.

## Environment and input integrity

- The audit used portable summary defaults unless full paths, previews, or formulas were necessary for the task.
- Tool output contains no unintended user-profile path, token, private data value, formula, or workbook header.
- Source hashes were recorded before mutation without changing the source files.
- Original workbooks, SVGs, images, scripts, and OPJU files remain unchanged.
- The current request, not prior memory or a stale handoff note, determines authority.
- Resource limits were sufficient for the intended inputs; any skipped or bounded inspection is disclosed.

## Data and mapping

- Sheet, header, unit, category order, and column roles match the source.
- Representative values were read back from Origin and checked against the source.
- Formula-derived values were checked against source rows; missing cached results are reported.
- Blank and missing cells retain their intended semantics.
- Every plotted series and data label remains bound to worksheet data.
- Stack totals, percentages, error bars, and transformations are numerically verified when applicable.

## Graph structure

- Chart type, layer count, plot count, grouping, stacking, and panel arrangement match the specification.
- Axis type, range, scale, ticks, units, and shared or independent behavior are correct.
- Legends contain exactly the intended entries in the intended order.
- Panel labels and annotations are present, positioned correctly, and not used to fake data.

## Visual design

- Final dimensions and aspect ratio match the target or stated journal requirement.
- Typography, palette, line widths, markers, column widths, gaps, and transparency are consistent.
- Major ticks are short and outward; minor ticks and gridlines are absent unless the approved style or scientific reading task requires them.
- The same scientific meaning retains the same colour, marker, line style, terminology, and ordering across the figure or approved suite specification.
- No clipping, unresolved overlap, unintended gridline, default placeholder, decorative effect, or excessive whitespace remains.
- The figure is legible at final export size and in grayscale when required.

## Three evidence layers

1. **File evidence:** OPJU and SVG exist, are non-empty, have hashes, and the SVG parses with genuine geometry.
2. **Origin semantic evidence:** worksheet values, graph objects, layer structure, legends, axes, and data bindings were queried through Origin.
3. **Persistence evidence:** the saved OPJU was reopened and the expected worksheet, graph, and bindings still exist.

File evidence alone does not prove editability. A rendered graph alone does not prove data binding. A successful save call alone does not prove persistence.

## Delivery

- Output files are outside protected input locations unless replacement was explicitly authorized.
- Exact output paths are reported in the final delivery context.
- Every `unverified` item and inspection limitation is reported.
- Tool availability, a successful preflight, or a passed figure-spec plan is not evidence that plotting, export, and final QA were completed.
