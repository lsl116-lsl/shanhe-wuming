"""Generate sparse original pentatonic cues for morning, writing, and news."""

from __future__ import annotations

import math
import random
from array import array

from asset_tools_common import base_parser
from audio_tools_common import SAMPLE_RATE, clamp_sample, equal_power_fade_to_start, write_stereo_samples


DURATION = 48.0
PENTATONIC = (196.0, 220.0, 261.63, 293.66, 349.23)


def main() -> int:
    args = base_parser("Generate P0/P2 original narrative music.").parse_args()
    rng = random.Random(args.seed + 911)
    events = []
    cursor = 2.0
    while cursor < DURATION - 3.0:
        frequency = rng.choice(PENTATONIC)
        pan = rng.uniform(-0.4, 0.4)
        events.append((cursor, frequency, pan))
        cursor += rng.choice((2.8, 3.6, 4.4))

    frame_count = int(DURATION * SAMPLE_RATE)
    samples = array("h")
    breath_l = 0.0
    breath_r = 0.0

    for index in range(frame_count):
        t = index / SAMPLE_RATE
        breath_l = breath_l * 0.999 + rng.uniform(-1.0, 1.0) * 0.001
        breath_r = breath_r * 0.999 + rng.uniform(-1.0, 1.0) * 0.001
        drone = math.sin(math.tau * 49.0 * t) * 0.025 + math.sin(math.tau * 73.5 * t) * 0.013
        left = drone + breath_l * 0.018
        right = drone * 0.92 + breath_r * 0.018

        for event_time, frequency, pan in events:
            dt = t - event_time
            if 0.0 <= dt < 2.6:
                envelope = math.exp(-dt * 2.3) * (1.0 - math.exp(-dt * 28.0))
                pluck = (
                    math.sin(math.tau * frequency * dt)
                    + 0.31 * math.sin(math.tau * frequency * 2.01 * dt)
                    + 0.12 * math.sin(math.tau * frequency * 3.97 * dt)
                ) * envelope * 0.075
                left += pluck * (1.0 - max(0.0, pan))
                right += pluck * (1.0 + min(0.0, pan))

        beat_phase = t % 8.0
        if 6.8 <= beat_phase < 6.95:
            dt = beat_phase - 6.8
            wood = math.sin(math.tau * 128.0 * dt) * math.exp(-dt * 45.0) * 0.045
            left += wood
            right += wood * 0.88

        samples.append(clamp_sample(left))
        samples.append(clamp_sample(right))

    equal_power_fade_to_start(samples, 2.0)
    write_stereo_samples(
        "assets/audio/music/music_old_ferry_morning.wav",
        samples,
        args.force,
    )

    name_rng = random.Random(args.seed + 919)
    name_events = [
        (3.0, 220.0, -0.2),
        (7.4, 261.63, 0.18),
        (12.8, 196.0, -0.1),
        (20.2, 293.66, 0.25),
        (28.8, 220.0, -0.24),
        (35.4, 174.61, 0.05),
        (42.0, 261.63, 0.16),
    ]
    name_samples = array("h")
    breath = 0.0
    for index in range(frame_count):
        t = index / SAMPLE_RATE
        breath = breath * 0.9991 + name_rng.uniform(-1.0, 1.0) * 0.0009
        low = math.sin(math.tau * 55.0 * t) * 0.021
        left = low + breath * 0.015
        right = low * 0.92 + breath * 0.012
        for event_time, frequency, pan in name_events:
            dt = t - event_time
            if 0.0 <= dt < 3.1:
                envelope = math.exp(-dt * 1.7) * (1.0 - math.exp(-dt * 24.0))
                note = (
                    math.sin(math.tau * frequency * dt)
                    + 0.23 * math.sin(math.tau * frequency * 2.02 * dt)
                ) * envelope * 0.061
                left += note * (1.0 - max(0.0, pan))
                right += note * (1.0 + min(0.0, pan))
        name_samples.append(clamp_sample(left))
        name_samples.append(clamp_sample(right))
    equal_power_fade_to_start(name_samples, 2.0)
    write_stereo_samples(
        "assets/audio/music/music_name_and_registry.wav",
        name_samples,
        args.force,
    )

    news_rng = random.Random(args.seed + 929)
    news_samples = array("h")
    wind_l = 0.0
    wind_r = 0.0
    news_events = [(5.0, 98.0), (14.5, 110.0), (25.0, 82.41), (37.0, 98.0)]
    for index in range(frame_count):
        t = index / SAMPLE_RATE
        wind_l = wind_l * 0.999 + news_rng.uniform(-1.0, 1.0) * 0.001
        wind_r = wind_r * 0.999 + news_rng.uniform(-1.0, 1.0) * 0.001
        drone = (
            math.sin(math.tau * 41.2 * t) * 0.027
            + math.sin(math.tau * 61.8 * t + 0.4) * 0.018
        )
        left = drone + wind_l * 0.017
        right = drone * 0.94 + wind_r * 0.017
        for event_time, frequency in news_events:
            dt = t - event_time
            if 0.0 <= dt < 4.8:
                envelope = math.exp(-dt * 0.78) * (1.0 - math.exp(-dt * 8.0))
                wood = (
                    math.sin(math.tau * frequency * dt)
                    + 0.21 * math.sin(math.tau * frequency * 2.63 * dt)
                ) * envelope * 0.043
                left += wood
                right += wood * 0.87
        news_samples.append(clamp_sample(left))
        news_samples.append(clamp_sample(right))
    equal_power_fade_to_start(news_samples, 2.0)
    write_stereo_samples(
        "assets/audio/music/music_ferry_day_news.wav",
        news_samples,
        args.force,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
