#!/usr/bin/env python3
"""Start a temporary, quiet Illustrator MCP runtime with safer text editing."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
from pathlib import Path


PACKAGE_NAME = "illustrator-mcp-server"
WRAPPER_PATCH_VERSION = 4
DEFAULT_NORMAL_TIMEOUT_MS = 90_000
DEFAULT_HEAVY_TIMEOUT_MS = 240_000


CHARACTER_RUNS_JSX = '''

      // illustrator-edit: character-runs
      if (props.character_runs) {
        try {
          for (var cri = 0; cri < props.character_runs.length; cri++) {
            var run = props.character_runs[cri];
            var startIndex = Math.max(0, Math.floor(run.start));
            var endIndex = Math.min(item.characters.length, Math.floor(run.end));
            if (endIndex <= startIndex) {
              errors.push("character_runs[" + cri + "]: empty or out-of-range interval");
              continue;
            }
            var runFont = null;
            if (run.font_name) {
              runFont = app.textFonts.getByName(run.font_name);
            }
            for (var ci = startIndex; ci < endIndex; ci++) {
              var runAttrs = item.characters[ci].characterAttributes;
              if (runFont) runAttrs.textFont = runFont;
              if (typeof run.font_size === "number") runAttrs.size = run.font_size;
              if (typeof run.baseline_shift === "number") runAttrs.baselineShift = run.baseline_shift;
            }
          }
        } catch(e) { errors.push("character_runs: " + e.message); }
      }
'''


CHARACTER_RUNS_SCHEMA = '''
                character_runs: z
                    .array(z.object({
                    start: z.number().int().min(0),
                    end: z.number().int().min(1),
                    font_name: z.string().optional(),
                    font_size: z.number().optional(),
                    baseline_shift: z.number().optional(),
                }))
                    .optional()
                    .describe('Character-range overrides. start is inclusive and end is exclusive.'),
'''


BATCH_MODIFY_TEXT_JS = r'''import { z } from 'zod';
import { executeToolJsx } from '../tool-executor.js';
import { coordinateSystemSchema } from '../session.js';
import { FONT_HELPERS_JSX, DESTRUCTIVE_ANNOTATIONS } from './shared.js';

// illustrator-edit: batch-modify-text
const jsxCode = `
var preflight = preflightChecks();
if (preflight) {
  writeResultFile(RESULT_PATH, preflight);
} else {
  try {
    var params = readParamsFile(PARAMS_PATH);
    var coordSystem = params.coordinate_system || "artboard-web";
    var abRect = (coordSystem === "artboard-web") ? getActiveArtboardRect() : null;
    ${FONT_HELPERS_JSX}

    var results = [];
    var succeeded = 0;
    var failed = 0;

    for (var bi = 0; bi < params.items.length; bi++) {
      var request = params.items[bi];
      var item = findItemByUUID(request.uuid);
      var errors = [];
      var fontCandidates = null;

      if (!item) {
        errors.push("No object found matching UUID: " + request.uuid);
      } else if (item.typename !== "TextFrame") {
        errors.push("Object is not a TextFrame: " + item.typename);
      } else {
        var props = request.properties || {};

        if (props.position) {
          try {
            item.position = webToAiPoint(
              props.position.x,
              props.position.y,
              coordSystem,
              abRect
            );
          } catch(e) { errors.push("position: " + e.message); }
        }

        if (typeof props.contents === "string") {
          try {
            item.contents = props.contents
              .split(String.fromCharCode(10))
              .join(String.fromCharCode(13));
          } catch(e) { errors.push("contents: " + e.message); }
        }

        if (typeof props.name === "string") {
          try { item.name = props.name; }
          catch(e) { errors.push("name: " + e.message); }
        }

        if (props.font_name) {
          try {
            var resolvedFont = app.textFonts.getByName(props.font_name);
            for (var tri = 0; tri < item.textRanges.length; tri++) {
              item.textRanges[tri].characterAttributes.textFont = resolvedFont;
            }
          } catch(e) {
            errors.push("font_name: Font '" + props.font_name + "' not found.");
            fontCandidates = findFontCandidates(props.font_name);
          }
        }

        if (typeof props.font_size === "number") {
          try {
            for (var tri2 = 0; tri2 < item.textRanges.length; tri2++) {
              item.textRanges[tri2].characterAttributes.size = props.font_size;
            }
          } catch(e) { errors.push("font_size: " + e.message); }
        }

        if (props.character_runs) {
          try {
            for (var cri = 0; cri < props.character_runs.length; cri++) {
              var run = props.character_runs[cri];
              var startIndex = Math.max(0, Math.floor(run.start));
              var endIndex = Math.min(item.characters.length, Math.floor(run.end));
              if (endIndex <= startIndex) {
                errors.push("character_runs[" + cri + "]: empty or out-of-range interval");
                continue;
              }
              var runFont = null;
              if (run.font_name) runFont = app.textFonts.getByName(run.font_name);
              for (var ci = startIndex; ci < endIndex; ci++) {
                var attrs = item.characters[ci].characterAttributes;
                if (runFont) attrs.textFont = runFont;
                if (typeof run.font_size === "number") attrs.size = run.font_size;
                if (typeof run.baseline_shift === "number") attrs.baselineShift = run.baseline_shift;
              }
            }
          } catch(e) { errors.push("character_runs: " + e.message); }
        }
      }

      var result = {
        uuid: request.uuid,
        success: errors.length === 0,
        errors: errors
      };
      if (item) result.verified = verifyItem(item, coordSystem, abRect);
      if (fontCandidates !== null) result.font_candidates = fontCandidates;
      results.push(result);

      if (errors.length === 0) succeeded++;
      else failed++;
    }

    writeResultFile(RESULT_PATH, {
      success: failed === 0,
      coordinateSystem: coordSystem,
      requested: params.items.length,
      succeeded: succeeded,
      failed: failed,
      results: results
    });
  } catch (e) {
    writeResultFile(RESULT_PATH, {
      error: true,
      message: "batch_modify_text failed: " + e.message,
      line: e.line
    });
  }
}
`;

const characterRunSchema = z.object({
    start: z.number().int().min(0),
    end: z.number().int().min(1),
    font_name: z.string().optional(),
    font_size: z.number().positive().optional(),
    baseline_shift: z.number().optional(),
});

const textPropertiesSchema = z.object({
    position: z.object({ x: z.number(), y: z.number() }).optional(),
    contents: z.string().optional(),
    name: z.string().optional(),
    font_name: z.string().optional(),
    font_size: z.number().positive().optional(),
    character_runs: z.array(characterRunSchema).optional(),
});

export function register(server) {
    server.registerTool('batch_modify_text', {
        title: 'Batch Modify Text',
        description: 'Modify multiple existing Illustrator text frames in one serialized JSX operation.',
        inputSchema: {
            items: z
                .array(z.object({
                    uuid: z.string(),
                    properties: textPropertiesSchema,
                }))
                .min(1)
                .max(200),
            coordinate_system: coordinateSystemSchema,
        },
        annotations: DESTRUCTIVE_ANNOTATIONS,
    }, async (params) => {
        return executeToolJsx(jsxCode, params, {
            heavy: true,
            resolveCoordinate: true,
        });
    });
}
'''


def version_key(value: str) -> tuple[int, ...]:
    parts = []
    for part in value.split("."):
        digits = "".join(character for character in part if character.isdigit())
        parts.append(int(digits or 0))
    return tuple(parts)


def package_metadata(package_dir: Path) -> dict:
    return json.loads((package_dir / "package.json").read_text(encoding="utf-8"))


def locate_package(explicit: str | None) -> Path:
    if explicit:
        package_dir = Path(explicit).expanduser().resolve()
        if not (package_dir / "package.json").is_file():
            raise SystemExit(f"Package not found: {package_dir}")
        return package_dir

    environment_path = os.environ.get("ILLUSTRATOR_MCP_PACKAGE")
    if environment_path:
        return locate_package(environment_path)

    candidates = []
    cache_root = Path.home() / ".npm" / "_npx"
    for package_json in cache_root.glob(
        f"*/node_modules/{PACKAGE_NAME}/package.json"
    ):
        try:
            metadata = json.loads(package_json.read_text(encoding="utf-8"))
            if metadata.get("name") != PACKAGE_NAME:
                continue
            candidates.append(
                (
                    version_key(str(metadata.get("version", "0"))),
                    package_json.stat().st_mtime,
                    package_json.parent.resolve(),
                )
            )
        except (OSError, ValueError, json.JSONDecodeError):
            continue
    if not candidates:
        raise SystemExit(
            "No cached illustrator-mcp-server package found. Check the existing MCP "
            "installation before installing or downloading anything."
        )
    candidates.sort()
    return candidates[-1][2]


def locate_node(explicit: str | None) -> Path:
    candidate = explicit or os.environ.get("ILLUSTRATOR_MCP_NODE")
    if candidate:
        node = Path(candidate).expanduser().resolve()
    else:
        found = shutil.which("node")
        node = Path(found).resolve() if found else Path("/opt/homebrew/bin/node")
    if not node.is_file():
        raise SystemExit(f"Node executable not found: {node}")
    return node


def count_activation_flags(package_dir: Path) -> int:
    return sum(
        javascript.read_text(encoding="utf-8").count("activate: true")
        for javascript in (package_dir / "dist").rglob("*.js")
    )


def js_integer(value: int) -> str:
    return f"{value:,}".replace(",", "_")


def patch_timeouts(package_dir: Path, normal_ms: int, heavy_ms: int) -> None:
    runner = package_dir / "dist" / "executor" / "jsx-runner.js"
    text = runner.read_text(encoding="utf-8")
    text, normal_count = re.subn(
        r"const TIMEOUT_NORMAL = [0-9_]+;",
        f"const TIMEOUT_NORMAL = {js_integer(normal_ms)};",
        text,
    )
    text, heavy_count = re.subn(
        r"const TIMEOUT_HEAVY = [0-9_]+;",
        f"const TIMEOUT_HEAVY = {js_integer(heavy_ms)};",
        text,
    )
    if normal_count != 1 or heavy_count != 1:
        raise SystemExit(
            "Could not patch illustrator-mcp-server timeouts safely; inspect "
            f"{runner} before continuing."
        )
    runner.write_text(text, encoding="utf-8")


def patch_character_runs(package_dir: Path) -> None:
    modifier = package_dir / "dist" / "tools" / "modify" / "modify-object.js"
    text = modifier.read_text(encoding="utf-8")
    if "illustrator-edit: character-runs" in text:
        return

    jsx_anchor = '''
      if (typeof props.font_size === "number") {
        try {
          for (var ri2 = 0; ri2 < item.textRanges.length; ri2++) {
            item.textRanges[ri2].characterAttributes.size = props.font_size;
          }
        } catch(e) { errors.push("font_size: " + e.message); }
      }
'''
    schema_anchor = "                font_size: z.number().optional().describe('Font size (for text frames)'),\n"
    if text.count(jsx_anchor) != 1 or text.count(schema_anchor) != 1:
        raise SystemExit(
            "Could not add character_runs safely; the upstream modify_object layout changed. "
            f"Inspect {modifier} before continuing."
        )
    text = text.replace(jsx_anchor, jsx_anchor + CHARACTER_RUNS_JSX, 1)
    text = text.replace(schema_anchor, schema_anchor + CHARACTER_RUNS_SCHEMA, 1)
    modifier.write_text(text, encoding="utf-8")


def patch_native_document_ops(package_dir: Path) -> None:
    """Route deep-document open/save/close operations through the heavy timeout."""
    for filename in ("open-document.js", "save-document.js", "close-document.js"):
        tool = package_dir / "dist" / "tools" / "modify" / filename
        text = tool.read_text(encoding="utf-8")
        if "executeJsxHeavy" in text:
            continue
        import_anchor = (
            "import { executeJsx } from '../../executor/jsx-runner.js';"
        )
        call_anchor = (
            "const result = await executeJsx(jsxCode, params, { activate: false });"
        )
        if text.count(import_anchor) != 1 or text.count(call_anchor) != 1:
            raise SystemExit(
                f"Could not route {filename} through the heavy timeout safely; "
                f"inspect {tool} before continuing."
            )
        text = text.replace(
            import_anchor,
            "import { executeJsxHeavy } from '../../executor/jsx-runner.js';",
            1,
        )
        text = text.replace(
            call_anchor,
            "const result = await executeJsxHeavy(jsxCode, params);",
            1,
        )
        tool.write_text(text, encoding="utf-8")


def patch_artboard_coordinates(package_dir: Path) -> None:
    """Make manage_artboards consume the same top-left rect contract it reports."""
    tool = package_dir / "dist" / "tools" / "modify" / "manage-artboards.js"
    text = tool.read_text(encoding="utf-8")
    if "illustrator-edit: safe-artboard-coordinates" in text:
        return

    add_anchor = '''        var r = params.rect;
        // artboardRect = [left, top, right, bottom] (document coordinates, Y-up)
        var abRect = [r.x, r.y + r.height, r.x + r.width, r.y];
'''
    add_replacement = '''        var r = params.rect;
        var coordSystem = params.coordinate_system || "document";
        // illustrator-edit: safe-artboard-coordinates
        // x/y always identify the top-left corner. artboard-web is relative to
        // the active artboard; document uses native Illustrator coordinates.
        var abRect;
        if (coordSystem === "artboard-web") {
          var activeRect = getActiveArtboardRect();
          var addLeft = activeRect[0] + r.x;
          var addTop = activeRect[1] - r.y;
          abRect = [addLeft, addTop, addLeft + r.width, addTop - r.height];
        } else {
          abRect = [r.x, r.y, r.x + r.width, r.y - r.height];
        }
'''
    resize_anchor = '''        var r2 = params.rect;
        // Artboard.artboardRect = [left, top, right, bottom] (document coordinates, Y-up)
        doc.artboards[params.index].artboardRect = [r2.x, r2.y + r2.height, r2.x + r2.width, r2.y];
        var resizedRect = doc.artboards[params.index].artboardRect;
        writeResultFile(RESULT_PATH, { success: true, index: params.index, verified: { artboardRect: resizedRect } });
'''
    resize_replacement = '''        var r2 = params.rect;
        var coordSystem2 = params.coordinate_system || "document";
        var targetRect = doc.artboards[params.index].artboardRect;
        var newRect;
        if (coordSystem2 === "artboard-web") {
          var resizeLeft = targetRect[0] + r2.x;
          var resizeTop = targetRect[1] - r2.y;
          newRect = [resizeLeft, resizeTop, resizeLeft + r2.width, resizeTop - r2.height];
        } else {
          newRect = [r2.x, r2.y, r2.x + r2.width, r2.y - r2.height];
        }
        doc.artboards[params.index].artboardRect = newRect;
        invalidateArtboardCache();
        var resizedRect = doc.artboards[params.index].artboardRect;
        writeResultFile(RESULT_PATH, {
          success: true,
          index: params.index,
          coordinateSystem: coordSystem2,
          verified: {
            artboardRect: resizedRect,
            position: { x: resizedRect[0], y: resizedRect[1] },
            size: {
              width: resizedRect[2] - resizedRect[0],
              height: resizedRect[1] - resizedRect[3]
            }
          }
        });
'''
    schema_anchor = '''                .optional()
                .describe('Position and size for add/resize (document coordinates)'),
            name: z.string().optional().describe('New name for rename action'),
'''
    schema_replacement = '''                .optional()
                .describe('Top-left position and size for add/resize'),
            coordinate_system: z
                .enum(['artboard-web', 'document'])
                .optional()
                .default('document')
                .describe('Rect coordinates. document uses native top-left x/y; artboard-web uses x/y down and right from the current artboard top-left.'),
            name: z.string().optional().describe('New name for rename action'),
'''

    replacements = (
        (add_anchor, add_replacement),
        (resize_anchor, resize_replacement),
        (schema_anchor, schema_replacement),
    )
    for anchor, replacement in replacements:
        if text.count(anchor) != 1:
            raise SystemExit(
                "Could not normalize manage_artboards coordinates safely; the "
                f"upstream layout changed. Inspect {tool} before continuing."
            )
        text = text.replace(anchor, replacement, 1)
    tool.write_text(text, encoding="utf-8")


def patch_batch_modify_text(package_dir: Path) -> None:
    """Add one heavy JSX operation for a verified set of text-frame edits."""
    tool = package_dir / "dist" / "tools" / "modify" / "batch-modify-text.js"
    tool.write_text(BATCH_MODIFY_TEXT_JS, encoding="utf-8")

    registry = package_dir / "dist" / "tools" / "registry.js"
    text = registry.read_text(encoding="utf-8")
    if "registerBatchModifyText" in text:
        return
    import_anchor = (
        "import { register as registerModifyObject } from './modify/modify-object.js';\n"
    )
    call_anchor = "    registerModifyObject(server);\n"
    if text.count(import_anchor) != 1 or text.count(call_anchor) != 1:
        raise SystemExit(
            "Could not register batch_modify_text safely; the upstream registry "
            f"layout changed. Inspect {registry} before continuing."
        )
    text = text.replace(
        import_anchor,
        import_anchor
        + "import { register as registerBatchModifyText } from './modify/batch-modify-text.js';\n",
        1,
    )
    text = text.replace(
        call_anchor,
        call_anchor + "    registerBatchModifyText(server);\n",
        1,
    )
    registry.write_text(text, encoding="utf-8")


def inspect_runtime(package_dir: Path) -> dict:
    runner = package_dir / "dist" / "executor" / "jsx-runner.js"
    modifier = package_dir / "dist" / "tools" / "modify" / "modify-object.js"
    runner_text = runner.read_text(encoding="utf-8")
    modifier_text = modifier.read_text(encoding="utf-8")
    artboards_text = (
        package_dir / "dist" / "tools" / "modify" / "manage-artboards.js"
    ).read_text(encoding="utf-8")
    registry_text = (
        package_dir / "dist" / "tools" / "registry.js"
    ).read_text(encoding="utf-8")
    document_ops = {}
    for operation in ("open", "save", "close"):
        operation_text = (
            package_dir
            / "dist"
            / "tools"
            / "modify"
            / f"{operation}-document.js"
        ).read_text(encoding="utf-8")
        document_ops[f"{operation}_uses_heavy_timeout"] = (
            "executeJsxHeavy" in operation_text
        )
    normal_match = re.search(r"const TIMEOUT_NORMAL = ([0-9_]+);", runner_text)
    heavy_match = re.search(r"const TIMEOUT_HEAVY = ([0-9_]+);", runner_text)
    if not normal_match or not heavy_match:
        raise SystemExit("Could not inspect the patched MCP timeout values.")
    return {
        "normal_timeout_ms": int(normal_match.group(1).replace("_", "")),
        "heavy_timeout_ms": int(heavy_match.group(1).replace("_", "")),
        "character_runs_enabled": "illustrator-edit: character-runs" in modifier_text,
        "safe_artboard_coordinates_enabled": (
            "illustrator-edit: safe-artboard-coordinates" in artboards_text
        ),
        "batch_modify_text_enabled": (
            "registerBatchModifyText" in registry_text
            and (
                package_dir
                / "dist"
                / "tools"
                / "modify"
                / "batch-modify-text.js"
            ).is_file()
        ),
        **document_ops,
    }


def prepare_runtime(
    source: Path,
    normal_timeout_ms: int,
    heavy_timeout_ms: int,
) -> tuple[Path, int, dict]:
    metadata = package_metadata(source)
    version = str(metadata.get("version", "unknown"))
    source_flags = count_activation_flags(source)
    if source_flags == 0:
        raise SystemExit(
            "No activation flags were found. The upstream package may have changed; "
            "inspect it before using the quiet wrapper."
        )
    runtime_root = (
        Path(tempfile.gettempdir()).resolve()
        / f"codex-illustrator-mcp-silent-{version}"
    )
    runtime_package = runtime_root / "package"
    marker = runtime_root / "source.json"
    expected_marker = {
        "source": str(source),
        "version": version,
        "source_mtime_ns": (source / "package.json").stat().st_mtime_ns,
        "source_activation_flags": source_flags,
        "wrapper_patch_version": WRAPPER_PATCH_VERSION,
        "normal_timeout_ms": normal_timeout_ms,
        "heavy_timeout_ms": heavy_timeout_ms,
    }

    rebuild = True
    if marker.is_file() and runtime_package.is_dir():
        try:
            rebuild = json.loads(marker.read_text(encoding="utf-8")) != expected_marker
        except (OSError, json.JSONDecodeError):
            rebuild = True

    if rebuild:
        if runtime_root.exists():
            shutil.rmtree(runtime_root)
        runtime_root.mkdir(parents=True)
        shutil.copytree(source, runtime_package)
        dependency_link = runtime_root / "node_modules"
        dependency_link.symlink_to(source.parent, target_is_directory=True)

        for javascript in (runtime_package / "dist").rglob("*.js"):
            text = javascript.read_text(encoding="utf-8")
            patched = text.replace("activate: true", "activate: false")
            if patched != text:
                javascript.write_text(patched, encoding="utf-8")
        patch_timeouts(runtime_package, normal_timeout_ms, heavy_timeout_ms)
        patch_character_runs(runtime_package)
        patch_native_document_ops(runtime_package)
        patch_artboard_coordinates(runtime_package)
        patch_batch_modify_text(runtime_package)
        marker.write_text(
            json.dumps(expected_marker, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    entrypoint = runtime_package / "dist" / "index.js"
    if not entrypoint.is_file():
        raise SystemExit(f"MCP entrypoint not found: {entrypoint}")
    runtime_report = inspect_runtime(runtime_package)
    if runtime_report != {
        "normal_timeout_ms": normal_timeout_ms,
        "heavy_timeout_ms": heavy_timeout_ms,
        "character_runs_enabled": True,
        "safe_artboard_coordinates_enabled": True,
        "batch_modify_text_enabled": True,
        "open_uses_heavy_timeout": True,
        "save_uses_heavy_timeout": True,
        "close_uses_heavy_timeout": True,
    }:
        raise SystemExit(f"Unexpected patched runtime state: {runtime_report}")
    return entrypoint, source_flags, runtime_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", help="Existing illustrator-mcp-server package directory")
    parser.add_argument("--node", help="Existing Node executable")
    parser.add_argument("--probe", action="store_true", help="Prepare and report without starting MCP")
    parser.add_argument(
        "--normal-timeout-ms",
        type=int,
        default=DEFAULT_NORMAL_TIMEOUT_MS,
        help=f"Timeout for ordinary JSX calls (default: {DEFAULT_NORMAL_TIMEOUT_MS})",
    )
    parser.add_argument(
        "--heavy-timeout-ms",
        type=int,
        default=DEFAULT_HEAVY_TIMEOUT_MS,
        help=f"Timeout for heavy JSX calls (default: {DEFAULT_HEAVY_TIMEOUT_MS})",
    )
    arguments = parser.parse_args()

    if arguments.normal_timeout_ms <= 0:
        parser.error("--normal-timeout-ms must be positive")
    if arguments.heavy_timeout_ms < arguments.normal_timeout_ms:
        parser.error("--heavy-timeout-ms must be greater than or equal to --normal-timeout-ms")

    source = locate_package(arguments.package)
    node = locate_node(arguments.node)
    entrypoint, source_flags, runtime_report = prepare_runtime(
        source,
        arguments.normal_timeout_ms,
        arguments.heavy_timeout_ms,
    )
    report = {
        "source_package": str(source),
        "source_version": package_metadata(source).get("version"),
        "node": str(node),
        "runtime_entrypoint": str(entrypoint),
        "source_activation_flags_removed_in_runtime": source_flags,
        "runtime_activation_flags_remaining": count_activation_flags(entrypoint.parent.parent),
        "wrapper_patch_version": WRAPPER_PATCH_VERSION,
        **runtime_report,
        "source_unchanged": True,
    }
    if arguments.probe:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    os.execv(str(node), [str(node), str(entrypoint)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
