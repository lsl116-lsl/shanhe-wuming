"""Run every P0 audio generator with one deterministic command."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from asset_tools_common import base_parser


SCRIPTS = (
    "generate_ambience.py",
    "generate_sfx.py",
    "generate_music_stems.py",
    "generate_p3_audio_assets.py",
    "generate_p4_audio_assets.py",
)


def main() -> int:
    args = base_parser("Generate all P0/P2/P3 audio assets.").parse_args()
    tools_dir = Path(__file__).resolve().parent
    for script in SCRIPTS:
        command = [sys.executable, str(tools_dir / script), "--seed", str(args.seed)]
        if args.force:
            command.append("--force")
        print(f"[pipeline] {script}")
        subprocess.run(command, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
