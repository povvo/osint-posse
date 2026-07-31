from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[4] / "src" / "skills" / "recon-rodeo" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from case_manager import CaseManager  # noqa: E402


class CaseManagerExportTests(unittest.TestCase):
    def test_case_export_is_openable_and_hash_manifested(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manager = CaseManager(root)
            created = manager.create_case("Release fixture", analyst="test")
            case_id = created["case_id"]
            output = root / "fixture.zip"

            result = manager.export_case(case_id, output)

            self.assertTrue(output.is_file())
            with zipfile.ZipFile(output) as archive:
                manifest_name = f"{case_id}/package_manifest.json"
                manifest = json.loads(archive.read(manifest_name))
                self.assertEqual(manifest["case_id"], case_id)
            sidecar = json.loads(Path(result["sidecar_manifest_path"]).read_text())
            self.assertEqual(sidecar["export_sha256"], result["sha256"])


if __name__ == "__main__":
    unittest.main()
