from __future__ import annotations

import unittest

from ospo._deps import import_name


class DependencyImportNameTests(unittest.TestCase):
    def test_known_distribution_names_map_to_import_modules(self) -> None:
        expectations = {
            "Pillow>=10.0": "PIL",
            "dnspython>=2.4": "dns",
            "edgartools": "edgar",
            "scikit-learn>=1.3": "sklearn",
            "sherlock-project": "sherlock",
            "yt-dlp": "yt_dlp",
        }

        for requirement, expected in expectations.items():
            with self.subTest(requirement=requirement):
                self.assertEqual(import_name(requirement), expected)
