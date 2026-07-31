#!/usr/bin/env python3
"""
ospo :: media verification
Local image/video verification: perceptual hashes, frame extraction, metadata and derivative manifest.
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any

from osint_common import ensure_dir, sha256_file, slugify, utc_now, write_json

try:
    from PIL import Image, ImageStat  # type: ignore
    HAS_PIL = True
except Exception:
    HAS_PIL = False


@dataclass
class MediaAnalysis:
    file: str
    media_type: str
    bytes: int
    sha256: str
    width: int | None = None
    height: int | None = None
    average_hash: str = ""
    difference_hash: str = ""
    dominant_stats: dict[str, Any] = field(default_factory=dict)
    frames: list[dict[str, Any]] = field(default_factory=list)
    reverse_search_queries: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class MediaVerifier:
    def __init__(self, output_dir: str = "./media_verification"):
        self.output_dir = ensure_dir(output_dir)

    def analyse(self, path: str | Path) -> dict[str, Any]:
        p = Path(path)
        if not p.exists():
            return {"error": f"File not found: {p}"}
        suffix = p.suffix.lower()
        media_type = "image" if suffix in {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"} else "video"
        analysis = MediaAnalysis(file=str(p), media_type=media_type, bytes=p.stat().st_size, sha256=sha256_file(p))
        if media_type == "image":
            self._analyse_image(p, analysis)
        else:
            self._analyse_video(p, analysis)
        analysis.reverse_search_queries = self.reverse_search_query_pack(p.name)
        result = {"analysed_at_utc": utc_now(), "analysis": asdict(analysis)}
        write_json(self.output_dir / f"media_{slugify(p.name)}.json", result)
        return result

    def _analyse_image(self, path: Path, out: MediaAnalysis) -> None:
        if not HAS_PIL:
            out.warnings.append("Pillow not installed; image hashes unavailable")
            return
        try:
            img = Image.open(path).convert("RGB")  # type: ignore[name-defined]
            out.width, out.height = img.size
            out.average_hash = self.average_hash(img)
            out.difference_hash = self.difference_hash(img)
            stat = ImageStat.Stat(img)  # type: ignore[name-defined]
            out.dominant_stats = {"mean_rgb": [round(x, 2) for x in stat.mean], "stddev_rgb": [round(x, 2) for x in stat.stddev]}
        except Exception as exc:
            out.warnings.append(f"image analysis failed: {exc}")

    def _analyse_video(self, path: Path, out: MediaAnalysis) -> None:
        if not shutil.which("ffmpeg"):
            out.warnings.append("ffmpeg not installed; keyframe extraction skipped")
            return
        frame_dir = ensure_dir(self.output_dir / f"frames_{slugify(path.stem)}")
        pattern = frame_dir / "frame_%03d.jpg"
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path), "-vf", "fps=1/10", "-frames:v", "12", str(pattern)]
        try:
            subprocess.run(cmd, check=False, timeout=120)
            for frame in sorted(frame_dir.glob("frame_*.jpg")):
                frame_result = {"path": str(frame), "sha256": sha256_file(frame), "bytes": frame.stat().st_size}
                if HAS_PIL:
                    img = Image.open(frame).convert("RGB")  # type: ignore[name-defined]
                    frame_result["average_hash"] = self.average_hash(img)
                    frame_result["difference_hash"] = self.difference_hash(img)
                out.frames.append(frame_result)
        except Exception as exc:
            out.warnings.append(f"ffmpeg extraction failed: {exc}")

    @staticmethod
    def average_hash(img: Any, hash_size: int = 8) -> str:
        small = img.resize((hash_size, hash_size)).convert("L")
        pixels = list(small.getdata())
        avg = sum(pixels) / len(pixels)
        bits = ''.join('1' if p > avg else '0' for p in pixels)
        return f"{int(bits, 2):0{hash_size * hash_size // 4}x}"

    @staticmethod
    def difference_hash(img: Any, hash_size: int = 8) -> str:
        small = img.resize((hash_size + 1, hash_size)).convert("L")
        pixels = list(small.getdata())
        bits = []
        for row in range(hash_size):
            for col in range(hash_size):
                left = pixels[row * (hash_size + 1) + col]
                right = pixels[row * (hash_size + 1) + col + 1]
                bits.append('1' if left > right else '0')
        return f"{int(''.join(bits), 2):0{hash_size * hash_size // 4}x}"

    @staticmethod
    def hamming_distance(hex_a: str, hex_b: str) -> int:
        return bin(int(hex_a, 16) ^ int(hex_b, 16)).count("1")

    @staticmethod
    def reverse_search_query_pack(filename: str) -> list[str]:
        stem = Path(filename).stem.replace("_", " ").replace("-", " ")
        return [
            f'"{filename}"',
            f'"{stem}" image source',
            f'"{stem}" site:twitter.com OR site:x.com',
            f'"{stem}" site:facebook.com OR site:instagram.com',
        ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse image/video evidence locally")
    parser.add_argument("file")
    parser.add_argument("--out-dir", default="./media_verification")
    args = parser.parse_args()
    print(json.dumps(MediaVerifier(args.out_dir).analyse(args.file), indent=2))


if __name__ == "__main__":
    main()
