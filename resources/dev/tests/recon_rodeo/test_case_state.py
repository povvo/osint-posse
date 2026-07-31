from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[4] / "src" / "skills" / "recon-rodeo" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from case_state import (  # noqa: E402
    CaseStateError,
    initialise_case,
    load_progress,
    resolve_workspace,
    save_progress,
    select_case,
    validate_case_id,
)


class CaseStateTests(unittest.TestCase):
    def workspace(self, root: Path, name: str = "project") -> Path:
        path = root / name
        path.mkdir()
        return path

    def test_two_cases_are_isolated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.workspace(Path(tmp))
            first, _ = initialise_case(workspace, "INV-one")
            second, _ = initialise_case(workspace, "INV-two")

            save_progress(first, {"completed": ["t1.1"], "current_index": 1})
            first.notebook_path.write_text("first notebook\n", encoding="utf-8")

            self.assertEqual(
                load_progress(second),
                {"completed": [], "current_index": 0, "completion_records": {}},
            )
            self.assertNotEqual(first.progress_file, second.progress_file)
            self.assertNotEqual(first.notebook_path, second.notebook_path)
            self.assertNotEqual(
                first.notebook_path.read_text(encoding="utf-8"),
                second.notebook_path.read_text(encoding="utf-8"),
            )

    def test_init_selects_active_case_without_overwriting_existing_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.workspace(Path(tmp))
            context, created = initialise_case(workspace, "INV-preserve")
            self.assertTrue(created)
            save_progress(context, {"completed": ["t1.1"], "current_index": 1})

            selected, created_again = initialise_case(workspace, "INV-preserve")
            self.assertFalse(created_again)
            self.assertEqual(selected, select_case(workspace))
            self.assertEqual(
                load_progress(selected),
                {
                    "completed": ["t1.1"],
                    "current_index": 1,
                    "completion_records": {},
                },
            )

    def test_explicit_case_selection_overrides_active_case(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.workspace(Path(tmp))
            first, _ = initialise_case(workspace, "INV-one")
            second, _ = initialise_case(workspace, "INV-two")

            self.assertEqual(select_case(workspace), second)
            self.assertEqual(select_case(workspace, "INV-one"), first)

    def test_no_case_fails_with_initialisation_instruction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.workspace(Path(tmp))
            with self.assertRaisesRegex(CaseStateError, "No investigation is selected"):
                select_case(workspace)

    def test_malformed_progress_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.workspace(Path(tmp))
            context, _ = initialise_case(workspace, "INV-bad-state")
            context.progress_file.write_text('{"completed": "t1.1"}', encoding="utf-8")

            with self.assertRaisesRegex(CaseStateError, "completed"):
                load_progress(context)

    def test_invalid_case_identifier_is_rejected(self) -> None:
        for value in ("../escape", "/absolute", "contains space", "", ".hidden"):
            with self.subTest(value=value):
                with self.assertRaises(CaseStateError):
                    validate_case_id(value)

    def test_environment_selection_is_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.workspace(Path(tmp))
            context, _ = initialise_case(workspace, "INV-env")
            with patch.dict(
                os.environ,
                {
                    "GREEN_INK_WORKSPACE": str(workspace),
                    "GREEN_INK_INVESTIGATION_ID": "INV-env",
                },
                clear=False,
            ):
                resolved = resolve_workspace()
                self.assertEqual(resolved, workspace.resolve())
                self.assertEqual(select_case(resolved), context)


if __name__ == "__main__":
    unittest.main()
