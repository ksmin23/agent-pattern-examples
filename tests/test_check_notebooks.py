"""Kernel integration tests; fixtures never call an external API."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import nbformat

from scripts import check_notebooks as checker


class NotebookChecks(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        root_patch = patch.object(checker, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        self.report = self.root / ".cache/notebook-validation.json"
        report_patch = patch.object(checker, "REPORT", self.report)
        report_patch.start()
        self.addCleanup(report_patch.stop)
        (self.root / "UPSTREAM.json").write_text('{"files": []}')

    def notebook(self, example, *sources):
        path = self.root / "patterns/demo/examples" / example / "notebooks/demo-ko.ipynb"
        path.parent.mkdir(parents=True)
        notebook = nbformat.v4.new_notebook(
            cells=[nbformat.v4.new_code_cell(s) for s in sources]
        )
        # Exercise the list-of-lines representation used by notebook editors.
        nbformat.write(notebook, path)
        return path

    def test_modes_cwd_await_and_original_bytes(self):
        for live in (False, True):
            with self.subTest(live=live):
                path = self.notebook(
                    f"mode_{live}",
                    "RUN_API = False\nimport asyncio\nfrom pathlib import Path",
                    f"assert RUN_API is {live}\n"
                    "assert Path.cwd().name == 'notebooks'\n"
                    "await asyncio.sleep(0)\n"
                    "print('output must not be saved')",
                )
                before = path.read_bytes()
                result = checker.check_notebook(path, live=live, timeout=30)
                self.assertEqual(result["status"], "passed", result)
                self.assertEqual(result["executed_cells"], 2)
                self.assertEqual(path.read_bytes(), before)
                self.assertNotIn("output must not be saved", json.dumps(result))

    def test_failure_continues_with_fresh_kernel_and_redacted_report(self):
        self.notebook("a_failure", "RUN_API = False\nleaked_state = 1", "raise RuntimeError('private error text')")
        self.notebook("b_success", "RUN_API = False\nassert 'leaked_state' not in globals()")
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(checker.main([]), 1)
        report = json.loads(self.report.read_text())
        self.assertEqual([n["status"] for n in report["notebooks"]], ["failed", "passed"])
        self.assertNotIn("private error text", self.report.read_text() + stdout.getvalue())

    def test_selection_and_invalid_example(self):
        self.notebook("selected", "RUN_API = False\nassert not RUN_API")
        self.notebook("unselected", "RUN_API = False\nraise AssertionError('must not execute')")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(checker.main(["--example", "selected"]), 0)
        report = json.loads(self.report.read_text())
        self.assertEqual([n["example"] for n in report["notebooks"]], ["selected"])
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            checker.main(["--example", "missing"])
        self.assertEqual(error.exception.code, 2)

    def test_static_failure_does_not_start_kernel(self):
        path = self.notebook("dirty", "RUN_API = False")
        notebook = nbformat.read(path, as_version=4)
        notebook.cells[0].execution_count = 1
        nbformat.write(notebook, path)
        with patch("jupyter_client.KernelManager") as manager:
            result = checker.check_notebook(path, live=False, timeout=30)
        manager.assert_not_called()
        self.assertEqual(result["status"], "failed")
        self.assertIn("clear saved outputs", result["errors"][0])


if __name__ == "__main__":
    unittest.main()
