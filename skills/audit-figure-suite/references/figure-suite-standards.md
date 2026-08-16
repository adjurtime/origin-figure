# Figure-suite standards

Use these standards to compare a complete paper figure set. Supplied data and analytical outputs govern values, the current manuscript governs terminology, and explicit user, journal, and approved project rules govern presentation. The defaults below fill only unspecified choices.

## Scientific integrity

- Trace every figure, panel, series, label, error bar, and derived value to a source table or analytical output.
- Keep units, denominators, normalization, transformations, missing-value semantics, uncertainty definitions, and statistical annotations explicit and correct.
- Preserve category, region, sector, scenario, and year order unless an analytical reason justifies a change.
- Do not repair values from screenshots or remove observations merely to improve appearance.
- Treat wrong values, misleading baselines, invented uncertainty, and broken Origin bindings as hard failures.

## Cross-figure semantic system

- Use the same terminology, abbreviations, capitalization, and ordering in figures, captions, and manuscript text.
- Keep the same scientific meaning in the same colour, marker, line style, hatch, and label convention throughout the suite.
- Do not reuse one visual encoding for conflicting meanings without a recorded exception.
- Keep comparable panels on comparable scales and tick intervals. Allow different scales for different variables when clearly signalled and scientifically necessary.
- Give every figure and panel one defined role in the evidence chain; remove decorative or duplicative panels only with user approval.

## Within-figure multi-panel system

- Establish the intended row and column grid before judging alignment. Audit every panel separately before assigning a status to the whole figure.
- Default to lowercase half-width `(a)`, `(b)`, `(c)` in left-to-right, top-to-bottom order. Follow a verified journal or approved project rule when it differs.
- Keep panel-label text, case, punctuation, font, size, weight, colour, anchor, and relative offset identical. Anchor labels to the plot-area top-left rather than unrelated page coordinates unless specified otherwise.
- Match every panel label and sequence to the figure caption and all manuscript references.
- Compare actual plot rectangles, not only outer panel objects. Comparable panels should have equal plotting widths and heights.
- Align X-axis baselines and plot-area tops across each intended row. Align Y-axis baselines and plot-area sides across each intended column.
- Keep ranges, scale types, tick origins, intervals, and zero positions identical within declared shared-axis groups. Signal scientifically necessary differences clearly.
- Prevent long tick labels, axis titles, legends, and colourbars from shrinking or shifting only one comparable plot rectangle.
- Keep horizontal and vertical gutters, outer margins, axis-title distances, tick-label distances, and shared-title placement consistent.
- Use shared axes, legends, or colourbars only when they reduce repetition without weakening interpretation. Check that their placement does not distort one panel.
- Compare Origin layer position and size readback with the actual final-size preview. Require exact equality for declared shared geometry when no tolerance is specified.
- Record intentional asymmetry for maps, colourbars, unequal scientific scales, or structurally different panels instead of treating it as an automatic failure.

## Default visual baseline

- Use Times New Roman at about 10.5 pt at the final Word insertion size for English paper figures unless overridden.
- Disable minor ticks and gridlines by default. Use short outward major ticks and a restrained, consistent axis-line weight.
- Retain minor ticks only for log axes or a genuine fine-reading task. Retain gridlines only when they materially improve comparison.
- Use a compact number of readable major ticks; keep number formats, percentages, significant digits, and scientific notation consistent.
- Put units in axis titles. Preserve zero for magnitude-comparison bars and disclose justified non-zero baselines.
- Use a white background and avoid 3D effects, gradients, shadows, decorative frames, and other non-data ink.

## Colour, marks, and accessibility

- Use a restrained, colourblind-aware palette chosen for semantic clarity before attractiveness.
- Pair colour with position, marker, line style, shape, or direct labels when grayscale or accessibility matters.
- Keep line weights, marker sizes, marker borders, opacity, and stack or legend order consistent.
- Confirm that adjacent categories and important labels remain distinguishable at final size and in grayscale when required.
- Use black and grey labels as a deliberate readability hierarchy; do not recolour all labels mechanically.

## Typography, labels, and legends

- Keep a stable hierarchy among axis titles, tick labels, legends, annotations, direct labels, and panel letters.
- Apply the approved panel-label system consistently within each figure and across the suite.
- Define abbreviations once and use them consistently. Match terminology and units to the caption and manuscript.
- Resolve label overlap through placement, concise abbreviations, selective hierarchy, or panel design without hiding important evidence.
- Match legend order to the visual and semantic order. Remove technical filler entries and unnecessary legend borders.

## Layout and final-size reading

- Define the intended Word or journal size before judging fonts, line widths, markers, or whitespace.
- Align comparable panel rectangles, axes, baselines, margins, and gutters. Keep panel areas visually balanced.
- Avoid clipping, excessive whitespace, cramped labels, inconsistent aspect ratios, and duplicated axis information.
- Inspect the actual preview or export at final physical size; code or Origin property inspection alone is not visual QA.

## Origin editability and persistence

- Bind every scientific plot and data label to Origin worksheet columns.
- Preserve authoritative blanks, data order, source files, manual edits, and the original OPJU unless replacement is authorized.
- Save revisions under a new name, reopen the stable OPJU, and verify worksheets, layers, plots, labels, and bindings.
- Treat a save timeout as unknown state. Inspect the target file and Origin state before retrying.
- Do not claim editability from file existence, hash, SVG geometry, or a rendered preview alone.

## Delivery and version control

- Use a consistent figure, panel, and version naming scheme. Keep source, working, review, and final artifacts distinguishable.
- Save the editable OPJU for review first. Export only requested formats after approval.
- Verify dimensions, resolution, transparency, font handling, file opening, clipping, and freshness relative to the approved OPJU.
- Record all unverified checks and every exception that a reviewer could mistake for inconsistency.

## Audit status rules

- Mark a check `pass` only when the available evidence directly supports it.
- Mark a check `fail` when evidence contradicts the approved standard.
- Mark a check `unverified` when the necessary source, semantic readback, preview, caption, or journal requirement is unavailable.
- Separate global inconsistencies from figure-specific exceptions so the revision plan can fix shared rules first.
