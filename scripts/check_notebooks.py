"""Validate and execute tutorial notebooks without saving their outputs.

Install requirements-notebooks.txt and prepare .env.local as in docs/setup.md.
Run with the same Python environment that should be used by the notebook kernels.
By default, API calls are disabled. --live enables the main walkthrough only;
the additional standalone examples retain their explicit run_api=False setting.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / ".cache" / "notebook-validation.json"
API_SWITCH = re.compile(r"(?m)^RUN_API\s*=\s*(?:True|False)\b")
API_KEY = re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_snapshot() -> dict[str, str]:
    return {
        p.relative_to(ROOT).as_posix(): sha256(p)
        for p in sorted(ROOT.glob("patterns/*/examples/*/src/**/*.py"))
    }


def source_hash_errors(snapshot: dict[str, str]) -> list[str]:
    """Check recorded CLI hashes; unrelated upstream documents are out of scope."""
    errors = []
    manifest = json.loads((ROOT / "UPSTREAM.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        local = item["local"]
        if not local.endswith(".py"):
            continue
        expected = item.get("local_sha256") or item.get("sha256")
        if local not in snapshot:
            errors.append(f"Missing CLI source: {local}")
        elif not expected or snapshot[local] != expected:
            errors.append(f"CLI source hash mismatch: {local}")
    return errors


def check_notebook(path: Path, *, live: bool, timeout: int) -> dict:
    import nbformat
    from jupyter_client import KernelManager
    from nbclient import NotebookClient

    started = time.monotonic()
    before = path.read_bytes()
    result = {
        "example": path.parent.parent.name,
        "notebook": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(before).hexdigest(),
        "status": "failed",
        "code_cells": 0,
        "executed_cells": 0,
        "errors": [],
    }
    errors = result["errors"]
    current_cell = None
    stage = "static"
    try:
        # Validate the original JSON before nbformat can normalize it.
        raw = json.loads(before)
        nbformat.validate(raw)
        notebook = nbformat.reads(before.decode("utf-8"), as_version=4)
        if API_KEY.search(before.decode("utf-8")):
            errors.append("Possible embedded API key; remove it before execution.")

        switches = 0
        for index, cell in enumerate(notebook.cells, start=1):
            if cell.cell_type != "code":
                continue
            current_cell = index
            result["code_cells"] += 1
            if cell.outputs or cell.execution_count is not None:
                errors.append(f"Cell {index}: clear saved outputs and execution count.")
            # Notebook cells allow top-level await, unlike ordinary Python files.
            compile(cell.source, f"cell-{index}", "exec", ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
            switches += len(API_SWITCH.findall(cell.source))
            if re.search(r"(?m)^RUN_API\s*=\s*True\b", cell.source):
                errors.append(f"Cell {index}: the public RUN_API default must be False.")
            cell.source = API_SWITCH.sub(f"RUN_API = {live}", cell.source)
        if switches != 1:
            errors.append("Expected exactly one top-level RUN_API boolean assignment.")
        if not errors:
            stage = "execution"
            current_cell = None

            def on_cell_execute(cell, cell_index):
                nonlocal current_cell
                current_cell = cell_index + 1

            def on_cell_executed(cell, cell_index, execute_reply):
                if execute_reply["content"].get("status") == "ok":
                    result["executed_cells"] += 1

            # Select this interpreter even if a different python3 kernelspec is installed.
            manager = KernelManager(kernel_name="python3")
            manager.kernel_spec.argv = [
                sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"
            ]
            client = NotebookClient(
                notebook,
                km=manager,
                timeout=timeout,
                startup_timeout=60,
                allow_errors=False,
                force_raise_errors=True,
                skip_cells_with_tag="",
                record_timing=False,
                store_widget_state=False,
                on_cell_execute=on_cell_execute,
                on_cell_executed=on_cell_executed,
            )
            # An externally supplied manager needs explicit cleanup ownership.
            with client.setup_kernel(cwd=str(path.parent), cleanup_kc=True):
                client.execute()
            result["status"] = "passed"
    except Exception as exc:
        # CellExecutionError text includes source/output, which can contain secrets.
        # Persist only the error class and cell location, never a raw traceback.
        error_type = type(exc).__name__
        kernel_error = getattr(exc, "ename", None)
        if isinstance(kernel_error, str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", kernel_error):
            error_type += f" ({kernel_error})"
        errors.append(f"{stage}: {error_type}; cell {current_cell}")
    finally:
        if not path.is_file() or path.read_bytes() != before:
            errors.append("Notebook file changed during validation.")
        if errors:
            result["status"] = "failed"
        result["duration_seconds"] = round(time.monotonic() - started, 3)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Enable walkthrough API calls and Docker (may incur costs).")
    parser.add_argument("--example", action="append", help="Example directory name, e.g. language_routing; repeat to select several.")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout per code cell in seconds (default: 600).")
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")

    paths = sorted(ROOT.glob("patterns/*/examples/*/notebooks/*.ipynb"))
    paths = [p for p in paths if p.is_file()]
    available = {p.parent.parent.name for p in paths}
    if args.example:
        unknown = set(args.example) - available
        if unknown:
            parser.error("Unknown example(s): " + ", ".join(sorted(unknown)))
        paths = [p for p in paths if p.parent.parent.name in args.example]

    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "mode": "live" if args.live else "offline",
        "python": sys.version.split()[0],
        "packages": {},
        "timeout_seconds": args.timeout,
        "errors": [],
        "notebooks": [],
    }
    errors = report["errors"]
    for package in ("nbformat", "nbclient", "ipykernel", "openai-agents", "openai", "python-dotenv"):
        try:
            report["packages"][package] = version(package)
        except PackageNotFoundError:
            errors.append(f"Missing dependency: {package}; install requirements-notebooks.txt.")
    if not paths:
        errors.append("No notebooks found.")

    before = source_snapshot()
    try:
        errors.extend(source_hash_errors(before))
    except (OSError, ValueError, KeyError, TypeError):
        errors.append("Cannot validate CLI hashes: invalid or missing UPSTREAM.json.")

    if not any(error.startswith("Missing dependency:") for error in errors):
        for path in paths:
            print(f"Checking {path.relative_to(ROOT)} ({report['mode']})...", flush=True)
            result = check_notebook(path, live=args.live, timeout=args.timeout)
            report["notebooks"].append(result)
            print(f"  {result['status']}: {result['executed_cells']}/{result['code_cells']} code cells", flush=True)
            for error in result["errors"]:
                print(f"  {error}", flush=True)
    if source_snapshot() != before:
        errors.append("CLI source files changed during validation.")

    report["status"] = "failed" if errors or any(
        n["status"] != "passed" for n in report["notebooks"]
    ) else "passed"
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"{report['status']}: report saved to {REPORT.relative_to(ROOT)}")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
