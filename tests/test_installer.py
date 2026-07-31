from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ospo._install import InstallConflict, install_release, uninstall_release
from ospo._paths import ReleaseResources


class InstallerTests(unittest.TestCase):
    def resources(self, root: Path) -> ReleaseResources:
        skill = root / "resources" / "skill"
        claude = root / "resources" / "claude"
        codex = root / "resources" / "codex"
        for directory in (skill, claude, codex):
            directory.mkdir(parents=True)
        (skill / "SKILL.md").write_text("version one\n", encoding="utf-8")
        (skill / "scripts").mkdir()
        (skill / "scripts" / "runner.py").write_text("print('ok')\n", encoding="utf-8")
        (claude / "analyst.md").write_text("claude\n", encoding="utf-8")
        (codex / "analyst.toml").write_text("name='analyst'\n", encoding="utf-8")
        return ReleaseResources(skill, claude, codex)

    def test_project_scope_empty_install_dry_run_and_uninstall(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            resources = self.resources(root)
            project = root / "project"
            project.mkdir()
            with patch("ospo._install.release_resources", return_value=resources):
                preview = install_release(root=project, dry_run=True)
                self.assertEqual(len(preview.copied), 2)
                self.assertFalse((project / ".agents").exists())

                installed = install_release(root=project)
                self.assertEqual(len(installed.copied), 2)
                target = project / ".agents" / "skills" / "recon-rodeo" / "SKILL.md"
                self.assertTrue(target.is_file())

                unrelated = target.parent / "operator-notes.md"
                unrelated.write_text("mine\n", encoding="utf-8")
                removed = uninstall_release(root=project)
                self.assertEqual(len(removed.removed), 2)
                self.assertTrue(unrelated.is_file())

    def test_identical_unowned_file_is_preserved_without_claiming_ownership(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            resources = self.resources(root)
            project = root / "project"
            target = project / ".agents" / "skills" / "recon-rodeo" / "SKILL.md"
            target.parent.mkdir(parents=True)
            target.write_text("version one\n", encoding="utf-8")
            with patch("ospo._install.release_resources", return_value=resources):
                result = install_release(root=project)
                self.assertIn(str(target), result.unchanged)
                uninstall_release(root=project)
                self.assertTrue(target.is_file())

    def test_conflicting_unowned_file_blocks_whole_install(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            resources = self.resources(root)
            project = root / "project"
            target = project / ".agents" / "skills" / "recon-rodeo" / "SKILL.md"
            target.parent.mkdir(parents=True)
            target.write_text("operator version\n", encoding="utf-8")
            with patch("ospo._install.release_resources", return_value=resources):
                with self.assertRaisesRegex(InstallConflict, "unowned"):
                    install_release(root=project)
            self.assertFalse((target.parent / "scripts" / "runner.py").exists())

    def test_owned_update_and_modified_file_preservation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            resources = self.resources(root)
            project = root / "project"
            with patch("ospo._install.release_resources", return_value=resources):
                install_release(root=project)
                source = resources.skill / "SKILL.md"
                source.write_text("version two\n", encoding="utf-8")
                updated = install_release(root=project)
                target = project / ".agents" / "skills" / "recon-rodeo" / "SKILL.md"
                self.assertIn(str(target), updated.copied)
                self.assertEqual(target.read_text(encoding="utf-8"), "version two\n")

                target.write_text("operator modification\n", encoding="utf-8")
                with self.assertRaisesRegex(InstallConflict, "modified"):
                    install_release(root=project)
                result = uninstall_release(root=project)
                self.assertIn(str(target), result.preserved)
                self.assertEqual(target.read_text(encoding="utf-8"), "operator modification\n")

    def test_explicit_user_scope_uses_given_home(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            resources = self.resources(root)
            user_home = root / "home"
            user_home.mkdir()
            with patch("ospo._install.release_resources", return_value=resources):
                install_release(scope="user", root=user_home, claude=True, codex=True)
            self.assertTrue((user_home / ".agents" / "skills" / "recon-rodeo" / "SKILL.md").is_file())
            self.assertTrue((user_home / ".claude" / "agents" / "analyst.md").is_file())
            self.assertTrue((user_home / ".codex" / "agents" / "analyst.toml").is_file())

    def test_symlinked_destination_escaping_scope_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            resources = self.resources(root)
            project = root / "project"
            outside = root / "outside"
            project.mkdir()
            outside.mkdir()
            (project / ".agents").symlink_to(outside, target_is_directory=True)
            with patch("ospo._install.release_resources", return_value=resources):
                with self.assertRaisesRegex(InstallConflict, "escapes"):
                    install_release(root=project)
            self.assertEqual(list(outside.rglob("*")), [])


if __name__ == "__main__":
    unittest.main()
