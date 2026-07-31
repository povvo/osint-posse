from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from evidence_preservation import EvidencePreserver


class EvidenceReceiptTests(unittest.IsolatedAsyncioTestCase):
    async def receipt(self, html_result: dict) -> tuple[dict, Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        preserver = EvidencePreserver(output_dir=str(root), timeout_seconds=1)
        with (
            patch("evidence_preservation.validate_public_url"),
            patch.object(
                preserver,
                "capture_screenshot",
                new=AsyncMock(return_value={"type": "screenshot", "status": "skipped", "reason": "fixture"}),
            ),
            patch.object(preserver, "capture_html", new=AsyncMock(return_value=html_result)),
            patch.object(
                preserver,
                "create_warc",
                return_value={"type": "warc", "status": "skipped", "reason": "fixture"},
            ),
        ):
            result = await preserver.preserve("https://example.test/start", submit_to_wayback=False)
        return result, root

    async def test_redirect_and_non_200_metadata_are_preserved(self) -> None:
        result, _root = await self.receipt(
            {
                "type": "html",
                "status": "captured",
                "status_code": 404,
                "final_url": "https://example.test/final",
                "redirected": True,
                "response_headers": {"content-type": "text/plain"},
            }
        )
        self.assertEqual(result["record_type"], "acquisition_receipt")
        self.assertEqual(result["response_status"], 404)
        self.assertTrue(result["redirected"])
        self.assertEqual(result["final_url"], "https://example.test/final")

    async def test_rejected_content_and_optional_capture_remain_explicit(self) -> None:
        result, _root = await self.receipt(
            {
                "type": "html",
                "status": "failed",
                "error": "binary content rejected by capture policy",
            }
        )
        statuses = {item["type"]: item["status"] for item in result["artefacts"]}
        self.assertEqual(statuses["html"], "failed")
        self.assertEqual(statuses["screenshot"], "skipped")
        self.assertIn("that optional capture steps succeeded", result["does_not_prove"])

    async def test_receipt_hash_verification_detects_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artefact = root / "capture.bin"
            artefact.write_bytes(b"captured bytes")
            receipt = root / "acquisition_receipt.json"
            payload = {
                "record_type": "acquisition_receipt",
                "artefacts": [
                    {
                        "path": str(artefact),
                        "sha256": EvidencePreserver.sha256_file(artefact),
                    }
                ],
            }
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(EvidencePreserver.verify_receipt(receipt), (True, []))
            artefact.write_bytes(b"changed")
            valid, errors = EvidencePreserver.verify_receipt(receipt)
            self.assertFalse(valid)
            self.assertIn("hash mismatch", errors[0])


if __name__ == "__main__":
    unittest.main()
