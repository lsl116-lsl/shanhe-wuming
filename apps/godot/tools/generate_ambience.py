"""Generate layered old-ferry morning and ferry-day ambience."""

from __future__ import annotations

import math
import random
from array import array

from asset_tools_common import base_parser
from audio_tools_common import (
    MAX_AMPLITUDE,
    SAMPLE_RATE,
    clamp_sample,
    equal_power_fade_to_start,
    write_stereo_samples,
)


DURATION = 90.0


def main() -> int:
    args = base_parser("Generate P0/P2 old-ferry ambience WAV.").parse_args()
    rng = random.Random(args.seed + 401)
    frame_count = int(DURATION * SAMPLE_RATE)
    samples = array("h")
    water_l = 0.0
    water_r = 0.0
    wind = 0.0

    creak_times = [8.5, 21.2, 35.8, 53.4, 71.7, 83.1]
    bird_times = [13.0, 29.4, 47.2, 66.0]
    cable_times = [18.1, 42.7, 77.4]

    for index in range(frame_count):
        t = index / SAMPLE_RATE
        water_l = water_l * 0.992 + rng.uniform(-1.0, 1.0) * 0.008
        water_r = water_r * 0.992 + rng.uniform(-1.0, 1.0) * 0.008
        wind = wind * 0.9992 + rng.uniform(-1.0, 1.0) * 0.0008

        tide = (
            math.sin(math.tau * t / 9.0) * 0.055
            + math.sin(math.tau * t / 4.5 + 0.7) * 0.025
        )
        left = water_l * 0.48 + wind * 0.24 + tide
        right = water_r * 0.48 + wind * 0.24 + tide * 0.92

        for event_time in creak_times:
            dt = t - event_time
            if 0.0 <= dt < 1.5:
                envelope = math.sin(math.pi * dt / 1.5) * math.exp(-dt * 1.1)
                creak = (
                    math.sin(math.tau * (78.0 + 19.0 * dt) * dt)
                    + 0.42 * math.sin(math.tau * 137.0 * dt)
                ) * envelope * 0.08
                left += creak * 0.85
                right += creak

        for event_time in cable_times:
            dt = t - event_time
            if 0.0 <= dt < 1.1:
                envelope = math.sin(math.pi * dt / 1.1) * math.exp(-dt * 0.7)
                cable = math.sin(math.tau * (54.0 + 7.0 * math.sin(dt * 9.0)) * dt)
                left += cable * envelope * 0.055
                right += cable * envelope * 0.043

        for event_time in bird_times:
            dt = t - event_time
            if 0.0 <= dt < 0.75:
                envelope = math.sin(math.pi * dt / 0.75) ** 2
                frequency = 920.0 + 330.0 * math.sin(math.pi * dt / 0.75)
                bird = math.sin(math.tau * frequency * dt) * envelope * 0.026
                left += bird
                right += bird * 0.72

        samples.append(clamp_sample(left))
        samples.append(clamp_sample(right))

    equal_power_fade_to_start(samples, 2.0)
    peak = max(abs(value) for value in samples)
    if peak > MAX_AMPLITUDE:
        raise RuntimeError("Generated ambience exceeded safe peak")
    write_stereo_samples(
        "assets/audio/ambience/river_morning.wav",
        samples,
        args.force,
    )

    day_rng = random.Random(args.seed + 403)
    day_samples = array("h")
    water_l = 0.0
    water_r = 0.0
    crowd = 0.0
    plank_times = [4.2, 4.55, 15.1, 28.4, 28.75, 44.0, 61.8, 62.15, 78.4]
    hull_times = [9.0, 25.6, 39.4, 58.2, 73.0, 86.1]
    for index in range(frame_count):
        t = index / SAMPLE_RATE
        water_l = water_l * 0.988 + day_rng.uniform(-1.0, 1.0) * 0.012
        water_r = water_r * 0.988 + day_rng.uniform(-1.0, 1.0) * 0.012
        crowd = crowd * 0.997 + day_rng.uniform(-1.0, 1.0) * 0.003
        tide = math.sin(math.tau * t / 6.8) * 0.045
        murmur = crowd * (0.025 + 0.012 * math.sin(math.tau * t / 11.0))
        left = water_l * 0.41 + tide + murmur
        right = water_r * 0.42 + tide * 0.9 + murmur * 0.82
        for event_time in plank_times:
            dt = t - event_time
            if 0.0 <= dt < 0.36:
                envelope = math.exp(-dt * 18.0)
                step = (
                    math.sin(math.tau * 118.0 * dt)
                    + 0.3 * math.sin(math.tau * 251.0 * dt)
                ) * envelope * 0.075
                left += step
                right += step * 0.68
        for event_time in hull_times:
            dt = t - event_time
            if 0.0 <= dt < 1.4:
                envelope = math.sin(math.pi * dt / 1.4) * math.exp(-dt * 0.9)
                hull = (
                    math.sin(math.tau * (67.0 + dt * 11.0) * dt)
                    + 0.35 * math.sin(math.tau * 121.0 * dt)
                ) * envelope * 0.07
                left += hull * 0.72
                right += hull
        day_samples.append(clamp_sample(left))
        day_samples.append(clamp_sample(right))
    equal_power_fade_to_start(day_samples, 2.0)
    write_stereo_samples(
        "assets/audio/ambience/ferry_day.wav",
        day_samples,
        args.force,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
