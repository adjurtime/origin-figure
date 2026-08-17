# Known Limitations and Recovery

## Foreground activation

`illustrator-mcp-server` 1.6.2 passes `activate: true` to most write tools, and its heavy export helper also activates Illustrator. On macOS this inserts an AppleScript `activate` command. The quiet wrapper removes those flags only in a temporary copy.

Observed with Illustrator 30.5.1:

- quiet `open_document`, reads, `modify_object`, and PNG export can leave the current app in front;
- native `save_document` and `close_document` can still surface Illustrator even without the explicit activation flag;
- concentrate text edits into `batch_modify_text` and perform one save and one close.

The quiet wrapper also patches ordinary/heavy JSX timeouts, native document operations, artboard coordinates, `modify_object.character_runs`, and `batch_modify_text` only in its temporary runtime. It does not change the npm cache.

## Operation timeouts

Upstream 1.6.2 uses 30 seconds for ordinary JSX and 60 seconds for heavy calls. Deeply nested imported figures can exceed those limits during open, object indexing, save, or post-operation verification. The quiet wrapper defaults to 90/240 seconds, routes open/save/close through the heavy channel, and reports each patch through `--probe`.

A terminated AppleScript is ambiguous: the requested action may have completed before the response was killed. Do not retry a write from the error alone. Re-query the document path and object state. For save, compare the expected file path, size, modification time, and hash; reopen and render the changed candidate before deciding whether a retry is needed.

`open_document` can also time out from Illustrator's home screen without opening the file. Check the actual UI or document state. If needed, use an approved app-opening fallback, then require `get_document_info.filePath` to match the task copy before any write.

## Close timeouts

`close_document(save=false)` can report a timeout or terminated AppleScript even when Illustrator has already closed the document. Do not immediately retry a close against an unknown active document. Start a fresh read-only session and call `get_document_info` first. Close only after the returned path exactly matches the task copy.

## Runtime reload

The wrapper and registered MCP tools are loaded only when the MCP process starts. Editing `silent_server.py` does not alter an already running server. Run `--probe`, then start a fresh registered MCP process before testing a new patch against artwork.

## Artboard coordinates

Upstream 1.6.2 reports an artboard's document `position.y` as its top edge but interprets `manage_artboards.rect.y` as its bottom edge. In the default `artboard-web` read mode it also reports `position: (0, 0)` plus a separate `rawPosition`. Passing either result back into the upstream resize formula can move the artboard away from the artwork.

The quiet runtime normalizes `manage_artboards` to a top-left rectangle contract:

- `document`: native top-left `x/y`, width rightward, height downward;
- `artboard-web`: offsets right/down from the target artboard's current top-left.

Use the same explicit coordinate system for read and write. Verify returned position and size, render, and save only after the artwork is still inside the intended artboard.

## Batch text editing

Upstream `modify_object` accepts one UUID per call. Repeated font or size changes across dozens of labels therefore create avoidable transport overhead and transient failures.

The quiet runtime adds `batch_modify_text`, limited to text-frame position, contents, name, font, size, and character runs. It executes up to 200 requested frames in one serialized heavy JSX call and returns one result per UUID. If a subset fails, inspect and retry only that subset. It intentionally does not batch arbitrary path, fill, stroke, or data-mark edits.

## SVG imports

SVG text can be imported as many small text frames. Subscripts, formulas, units, and rotated axis titles are especially likely to be split character by character. A saved AI working copy preserves the Illustrator object model more consistently than repeated SVG opens.

When a fragmented title is reconstructed, keep its complete visible text in one Illustrator text frame and use `modify_object.character_runs` for subscript, superscript, font-size, font, or baseline-shift overrides. Preserve the original aggregate center or bounds. Clear obsolete fragments only after visual QA; report any blank remnants when removal is unavailable.

On first import, compare the rendered SVG baseline with a clean AI reopen. If the whole layout changes, treat the import state as unresolved and do not edit the source.

## Undo and byte identity

Do not trust a successful `undo` response as proof of restoration. Verify object properties or reopen the last saved copy.

Illustrator can rewrite AI file bytes during a save without a visible change. Use rendered-image comparison and object-property checks as the primary verification; use file hashes to prove source preservation and exact preview identity.

## Fonts

Use `list_fonts` before applying a font. `Arial` can fail as a PostScript font name while `ArialMT` succeeds. Treat any font warning as a failed typography check until the exported preview has been inspected.

For SVG CSS, a PostScript font name plus a Unicode subscript glyph can trigger an Illustrator substitute-glyph warning even when the font is installed. Prefer the font family name in the intermediate SVG and represent the subscript as the ordinary character with a relative size/baseline style. After import, assign the exact PostScript font in Illustrator and consolidate the character runs there.

## Raw MCP protocol

The bundled Model Context Protocol SDK uses one JSON-RPC object per line on stdio. `Content-Length` framing causes initialization timeouts. Avoid repeatedly starting `npx`; use one registered server or the quiet wrapper's direct Node process.

## Safe recovery sequence

1. Stop the MCP process, not Illustrator.
2. Start one fresh read-only MCP session.
3. Query `get_document_info`.
4. If no document is open, reopen the verified AI copy.
5. If another document is active, do not save or close it.
6. If the test copy is active and dirty, close it with `save=false`, then reopen the last verified copy.
7. If a timed-out write is visible but unsaved and cannot be verified, discard that candidate rather than relying on `undo`.
