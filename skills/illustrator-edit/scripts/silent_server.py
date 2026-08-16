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
WRAPPER_PATCH_VERSION = 3
DEFAULT_NORMAL_TIMEOUT_MS = 90_000
DEFAULT_HEAVY_TIMEOUT_MS = 150_000


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


def inspect_runtime(package_dir: Path) -> dict:
    runner = package_dir / "dist" / "executor" / "jsx-runner.js"
    modifier = package_dir / "dist" / "tools" / "modify" / "modify-object.js"
    runner_text = runner.read_text(encoding="utf-8")
    modifier_text = modifier.read_text(encoding="utf-8")
    normal_match = re.search(r"const TIMEOUT_NORMAL = ([0-9_]+);", runner_text)
    heavy_match = re.search(r"const TIMEOUT_HEAVY = ([0-9_]+);", runner_text)
    if not normal_match or not heavy_match:
        raise SystemExit("Could not inspect the patched MCP timeout values.")
    return {
        "normal_timeout_ms": int(normal_match.group(1).replace("_", "")),
        "heavy_timeout_ms": int(heavy_match.group(1).replace("_", "")),
        "character_runs_enabled": "illustrator-edit: character-runs" in modifier_text,
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
