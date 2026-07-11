"""Standard-library WAV helpers for deterministic generated audio."""

from __future__ import annotations

import math
import wave
from array import array
from pathlib import Path
from typing import Callable

from asset_tools_common import PROJECT_ROOT, ensure_output_path


SAMPLE_RATE = 44_100
MAX_AMPLITUDE = 28_500


def clamp_sample(value: float) -> int:
    return int(max(-1.0, min(1.0, value)) * MAX_AMPLITUDE)


def write_mono(
    relative_path: str,
    duration_seconds: float,
    sample_function: Callable[[int, float], float],
    force: bool,
) -> Path:
    target = ensure_output_path(relative_path, force)
    sample_count = int(duration_seconds * SAMPLE_RATE)
    samples = array("h")
    for index in range(sample_count):
        samples.append(clamp_sample(sample_function(index, index / SAMPLE_RATE)))
    with wave.open(str(target), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(SAMPLE_RATE)
        output.writeframes(samples.tobytes())
    print(f"[generated] {relative_path} ({duration_seconds:.1f}s mono)")
    return target


def write_stereo_samples(relative_path: str, samples: array, force: bool) -> Path:
    target = ensure_output_path(relative_path, force)
    with wave.open(str(target), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(SAMPLE_RATE)
        output.writeframes(samples.tobytes())
    duration = len(samples) / (SAMPLE_RATE * 2)
    print(f"[generated] {relative_path} ({duration:.1f}s stereo)")
    return target


def equal_power_fade_to_start(samples: array, fade_seconds: float = 1.5) -> None:
    frame_count = len(samples) // 2
    fade_frames = min(int(fade_seconds * SAMPLE_RATE), frame_count // 4)
    for offset in range(fade_frames):
        amount = offset / max(1, fade_frames - 1)
        end_frame = frame_count - fade_frames + offset
        start_frame = offset
        fade_out = math.cos(amount * math.pi * 0.5)
        fade_in = math.sin(amount * math.pi * 0.5)
        for channel in (0, 1):
            end_index = end_frame * 2 + channel
            start_index = start_frame * 2 + channel
            mixed = samples[end_index] * fade_out + samples[start_index] * fade_in
            samples[end_index] = int(max(-MAX_AMPLITUDE, min(MAX_AMPLITUDE, mixed)))
