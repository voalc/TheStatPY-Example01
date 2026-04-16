#!/usr/bin/env python3
"""Regression checks for thestatpy processing behavior.

This script validates:
1) Nested <thestatpy html="..."> tags are resolved recursively.
2) Reused components are served from cache in standalone processor (verbose mode).
3) Circular includes do not recurse indefinitely.
4) build.py and process_thestatpy.py produce expected output shapes.
"""

from __future__ import annotations

import io
import os
import tempfile
from contextlib import redirect_stdout

import build
from process_thestatpy import process_thestatpy as standalone_process


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _build_nested_fixture(tmp_dir: str) -> str:
    part_dir = os.path.join(tmp_dir, "part")
    os.makedirs(part_dir, exist_ok=True)

    with open(os.path.join(part_dir, "leaf.html"), "w", encoding="utf-8") as f:
        f.write("<span>LEAF</span>")

    with open(os.path.join(part_dir, "parent.html"), "w", encoding="utf-8") as f:
        f.write('<div class="parent">PARENT <thestatpy html="leaf.html"></thestatpy></div>')

    index_path = os.path.join(tmp_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(
            """<html><head><import app=\"thestatpy\"/></head><body>
<thestatpy html=\"part/parent.html\"></thestatpy>
<thestatpy html=\"part/parent.html\"></thestatpy>
</body></html>"""
        )

    return index_path


def _build_circular_fixture(tmp_dir: str) -> str:
    part_dir = os.path.join(tmp_dir, "part")
    os.makedirs(part_dir, exist_ok=True)

    with open(os.path.join(part_dir, "a.html"), "w", encoding="utf-8") as f:
        f.write('<div>A <thestatpy html="b.html"></thestatpy></div>')

    with open(os.path.join(part_dir, "b.html"), "w", encoding="utf-8") as f:
        f.write('<div>B <thestatpy html="a.html"></thestatpy></div>')

    index_path = os.path.join(tmp_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write('<html><head><import app="thestatpy"/></head><body><thestatpy html="part/a.html"></thestatpy></body></html>')

    return index_path


def test_standalone_nested_and_cache() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        index_path = _build_nested_fixture(tmp)

        with open(index_path, "r", encoding="utf-8") as f:
            src = f.read()

        stdout_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer):
            output = standalone_process(src, tmp, verbose=True)
        logs = stdout_buffer.getvalue()

        _assert("LEAF" in output, "Standalone processor did not resolve nested include content")
        _assert(output.count('<div class="parent">') == 2, "Standalone processor did not include repeated parent content twice")
        _assert(output.count("<thestatpy") == 0, "Standalone processor left unresolved thestatpy tags")
        _assert("<import" not in output, "Standalone processor did not remove thestatpy import control tag")
        _assert("Cache hit for 'part/parent.html'" in logs, "Standalone processor did not report a cache hit for repeated component")


def test_build_module_nested_resolution() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        index_path = _build_nested_fixture(tmp)

        with open(index_path, "r", encoding="utf-8") as f:
            src = f.read()

        output = build.process_thestatpy(src, tmp)

        _assert("LEAF" in output, "build.py processor did not resolve nested include content")
        _assert(output.count('<div class="parent">') == 2, "build.py processor did not include repeated parent content twice")
        _assert(output.count("<thestatpy") == 0, "build.py processor left unresolved thestatpy tags")
        _assert("<import" not in output, "build.py processor did not remove thestatpy import control tag")


def test_circular_include_guard() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        index_path = _build_circular_fixture(tmp)

        with open(index_path, "r", encoding="utf-8") as f:
            src = f.read()

        stdout_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer):
            output = standalone_process(src, tmp, verbose=True)
        logs = stdout_buffer.getvalue()

        _assert("Circular include detected" in logs, "Standalone processor did not detect circular include")
        _assert("<div>A" in output and "<div>B" in output, "Circular include fixture did not include expected partial output")
        _assert("<import" not in output, "Standalone processor did not remove thestatpy import control tag in circular case")


def main() -> int:
    tests = [
        test_standalone_nested_and_cache,
        test_build_module_nested_resolution,
        test_circular_include_guard,
    ]

    failures = []
    for test_fn in tests:
        try:
            test_fn()
            print(f"[PASS] {test_fn.__name__}")
        except Exception as exc:
            failures.append((test_fn.__name__, str(exc)))
            print(f"[FAIL] {test_fn.__name__}: {exc}")

    if failures:
        print("\nRegression checks failed:")
        for name, message in failures:
            print(f" - {name}: {message}")
        return 1

    print("\nAll thestatpy regression checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
