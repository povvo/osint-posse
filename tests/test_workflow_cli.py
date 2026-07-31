from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class WorkflowCliTests(unittest.TestCase):
    def run_ospo(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys; from ospo._workflow import main; "
                    "raise SystemExit(main(sys.argv[1:], prog='ospo'))"
                ),
                *arguments,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_documented_sequence_rejects_incomplete_then_advances_once(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            manifest_path = workspace / "evidence-manifest.json"

            self.assertEqual(
                self.run_ospo("workflow", "init", "INV-release", "--workspace", str(workspace)).returncode,
                0,
            )
            self.assertEqual(
                self.run_ospo("workflow", "next", "--workspace", str(workspace)).returncode,
                0,
            )
            self.assertEqual(
                self.run_ospo(
                    "workflow",
                    "requirements",
                    "--out",
                    str(manifest_path),
                    "--workspace",
                    str(workspace),
                ).returncode,
                0,
            )

            rejected = self.run_ospo(
                "workflow",
                "done",
                "--evidence-manifest",
                str(manifest_path),
                "--workspace",
                str(workspace),
            )
            self.assertEqual(rejected.returncode, 2)

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for requirement in manifest["requirements"].values():
                requirement["evidence"] = [{"kind": "note", "value": "Verified in release fixture."}]
            for tool in manifest["tools"].values():
                tool["evidence"] = [{"kind": "record", "value": "Fixture invocation recorded."}]
            output = workspace / "case-decision-log.md"
            output.write_text("Fixture decision log\n", encoding="utf-8")
            for template in manifest["templates"].values():
                template["output_paths"] = [str(output)]
            notebook = workspace / ".green-ink" / "cases" / "INV-release" / "investigation-notebook.md"
            notebook.write_text(
                notebook.read_text(encoding="utf-8") + "\nFixture task update.\n",
                encoding="utf-8",
            )
            manifest["notebook"] = {
                "updated": True,
                "evidence": [{"kind": "note", "value": "Notebook updated for t1.1."}],
            }
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            completed = self.run_ospo(
                "workflow",
                "done",
                "--evidence-manifest",
                str(manifest_path),
                "--workspace",
                str(workspace),
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)

            status = self.run_ospo("workflow", "status", "--workspace", str(workspace))
            self.assertEqual(status.returncode, 0)
            self.assertIn("PROGRESS: 1/56 tasks", status.stdout)

    def test_supported_tool_wrapper_emits_case_bound_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            receipt = Path(temporary) / "receipt.json"
            completed = self.run_ospo(
                "tool",
                "run",
                "--standalone",
                "--receipt",
                str(receipt),
                "--investigation-id",
                "INV-release",
                "--task-id",
                "t3.1a",
                "source-grader",
                "--",
                "--help",
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(receipt.read_text())
            self.assertEqual(payload["schema_version"], "2.0")
            self.assertEqual(payload["investigation_id"], "INV-release")
            self.assertEqual(payload["task_id"], "t3.1a")


if __name__ == "__main__":
    unittest.main()
