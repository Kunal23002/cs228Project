#!/usr/bin/env python3
"""
Compress adversarial audio samples to MP3 and ALAC formats using ffmpeg.

The script reads the 90 sampled adversarial pairs stored in
`audio_analysis_results.json`, locates the corresponding adversarial audio files
under the dataset root, and creates compressed copies inside the local
`compressed_audio/` directory.
"""
import json
import subprocess
from pathlib import Path
from typing import Dict, Iterable, Optional

# Paths
PROJECT_ROOT = Path(__file__).parent
RESULTS_PATH = PROJECT_ROOT / "audio_analysis_results.json"
DATASET_ROOT = Path(
    "/Users/kunal/Downloads/adversarial_dataset-A/Adversarial-Examples"
)
OUTPUT_ROOT = PROJECT_ROOT / "compressed_audio"

# Compression formats and ffmpeg options
FORMATS: Dict[str, Dict[str, Iterable[str]]] = {
    "mp3": {
        "extension": ".mp3",
        "options": ["-codec:a", "libmp3lame", "-b:a", "192k"],
    },
    "alac": {
        "extension": ".m4a",
        "options": ["-codec:a", "alac"],
    },
}


class CompressionError(Exception):
    """Raised when ffmpeg fails to compress an audio file."""


def load_results(path: Path) -> Iterable[Dict]:
    """Load analysis results JSON."""
    with path.open("r") as handle:
        return json.load(handle)


def determine_paths(adversarial_filename: str) -> Optional[Path]:
    """
    Construct the path to the adversarial audio inside the dataset structure.

    Filenames follow the pattern: adv-<orig>2<target>-<id>.wav
    Example: adv-short2long-000303.wav
    """
    stem = adversarial_filename.removeprefix("adv-")
    try:
        orig_target, _ = stem.rsplit("-", 1)
        original_type, target_type = orig_target.split("2", 1)
    except ValueError:
        return None

    signal_dir = f"{original_type}-signals"
    adv_dir = f"adv-{target_type}-target"

    return DATASET_ROOT / signal_dir / adv_dir / adversarial_filename


def ensure_directory(path: Path) -> None:
    """Create directory if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)


def run_ffmpeg(input_path: Path, output_path: Path, options: Iterable[str]) -> None:
    """Invoke ffmpeg with the given options."""
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(input_path),
        *options,
        str(output_path),
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        raise CompressionError(
            f"ffmpeg failed for {input_path.name} -> {output_path.name}"
        ) from exc


def compress_file(adversarial_path: Path, original_type: str) -> None:
    """Compress a single adversarial file to all configured formats."""
    for name, config in FORMATS.items():
        extension = config["extension"]
        output_dir = OUTPUT_ROOT / name / original_type
        ensure_directory(output_dir)
        output_path = output_dir / (adversarial_path.stem + extension)

        if output_path.exists():
            continue

        run_ffmpeg(adversarial_path, output_path, config["options"])


def main() -> None:
    if not RESULTS_PATH.exists():
        raise FileNotFoundError(
            f"Analysis results not found at {RESULTS_PATH}. Run analyze_audio.py first."
        )

    ensure_directory(OUTPUT_ROOT)
    results = load_results(RESULTS_PATH)

    processed = 0
    skipped = 0
    for entry in results:
        if entry.get("error"):
            skipped += 1
            continue

        filename = entry.get("adversarial_file")
        if not filename:
            skipped += 1
            continue

        adversarial_path = determine_paths(filename)
        if adversarial_path is None or not adversarial_path.exists():
            skipped += 1
            continue

        original_type = filename.split("-")[1].split("2", 1)[0]
        compress_file(adversarial_path, original_type)
        processed += 1

    print(
        f"Compression complete. Processed {processed} files. "
        f"Skipped {skipped} entries (errors or missing files)."
    )


if __name__ == "__main__":
    main()

