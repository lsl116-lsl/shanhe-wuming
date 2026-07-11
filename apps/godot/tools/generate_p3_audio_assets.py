"""Generate P3 refuge, rain, ritual-storehouse, song, music, and cracked-bell audio."""

from __future__ import annotations

import math
import random
from array import array

from asset_tools_common import base_parser
from audio_tools_common import (
    SAMPLE_RATE,
    clamp_sample,
    equal_power_fade_to_start,
    write_mono,
    write_stereo_samples,
)


def make_ambience(path: str, duration: float, seed: int, storehouse: bool, force: bool) -> None:
    rng = random.Random(seed)
    samples = array("h")
    rain_l = 0.0
    rain_r = 0.0
    wind = 0.0
    frames = int(duration * SAMPLE_RATE)
    drops = (7.3, 18.6, 32.1, 47.4, 63.7, 78.8)
    fire_times = (4.8, 12.4, 25.0, 41.8, 58.2, 74.1, 87.0)
    for index in range(frames):
        t = index / SAMPLE_RATE
        rain_l = rain_l * 0.972 + rng.uniform(-1.0, 1.0) * 0.028
        rain_r = rain_r * 0.972 + rng.uniform(-1.0, 1.0) * 0.028
        wind = wind * 0.9993 + rng.uniform(-1.0, 1.0) * 0.0007
        build = min(1.0, 0.42 + t / 115.0)
        low = math.sin(math.tau * 37.0 * t) * (0.009 if storehouse else 0.004)
        left = rain_l * 0.037 * build + wind * 0.025 + low
        right = rain_r * 0.039 * build + wind * 0.022 + low * 0.92
        if storehouse:
            left *= 0.62
            right *= 0.64
            for event_time in drops:
                dt = t - event_time
                if 0.0 <= dt < 0.9:
                    ring = (
                        math.sin(math.tau * 287.0 * dt)
                        + 0.32 * math.sin(math.tau * 511.0 * dt)
                    ) * math.exp(-dt * 7.0) * 0.03
                    left += ring
                    right += ring * 0.72
        else:
            murmur = (
                math.sin(math.tau * 91.0 * t + math.sin(t * 0.37))
                + math.sin(math.tau * 118.0 * t + 1.2)
            ) * 0.0028
            left += murmur
            right += murmur * 0.83
            for event_time in fire_times:
                dt = t - event_time
                if 0.0 <= dt < 0.14:
                    crack = rng.uniform(-1.0, 1.0) * math.exp(-dt * 34.0) * 0.045
                    left += crack * 0.68
                    right += crack
        samples.append(clamp_sample(left))
        samples.append(clamp_sample(right))
    equal_power_fade_to_start(samples, 2.0)
    write_stereo_samples(path, samples, force)


def make_music(path: str, duration: float, seed: int, memory: bool, force: bool) -> None:
    rng = random.Random(seed)
    samples = array("h")
    frames = int(duration * SAMPLE_RATE)
    notes = (73.42, 82.41, 98.0, 110.0, 130.81, 146.83)
    events = []
    cursor = 2.0
    while cursor < duration - 2.0:
        events.append((cursor, rng.choice(notes), rng.uniform(-0.35, 0.35)))
        cursor += rng.choice((3.4, 4.2, 5.1, 6.0))
    air_l = 0.0
    air_r = 0.0
    for index in range(frames):
        t = index / SAMPLE_RATE
        air_l = air_l * 0.999 + rng.uniform(-1.0, 1.0) * 0.001
        air_r = air_r * 0.999 + rng.uniform(-1.0, 1.0) * 0.001
        root = 36.71 if memory else 49.0
        drone = math.sin(math.tau * root * t) * (0.025 if memory else 0.018)
        left = drone + air_l * 0.012
        right = drone * 0.91 + air_r * 0.012
        for event_time, frequency, pan in events:
            dt = t - event_time
            if 0.0 <= dt < 4.0:
                envelope = (1.0 - math.exp(-dt * 12.0)) * math.exp(-dt * (0.72 if memory else 1.0))
                tone = (
                    math.sin(math.tau * frequency * dt)
                    + 0.25 * math.sin(math.tau * frequency * 2.01 * dt)
                    + 0.09 * math.sin(math.tau * frequency * 3.98 * dt)
                ) * envelope * (0.041 if memory else 0.052)
                left += tone * (1.0 - max(0.0, pan))
                right += tone * (1.0 + min(0.0, pan))
        samples.append(clamp_sample(left))
        samples.append(clamp_sample(right))
    equal_power_fade_to_start(samples, 2.0)
    write_stereo_samples(path, samples, force)


def bell_component(t: float, kind: str, noise: float = 0.0) -> float:
    if kind == "body":
        attack = 1.0 - math.exp(-t * 32.0)
        decay = math.exp(-t * 0.38)
        return (
            math.sin(math.tau * 46.2 * t) * 0.13
            + math.sin(math.tau * 69.7 * t) * 0.082
            + math.sin(math.tau * 113.3 * t) * 0.047
        ) * attack * decay
    if kind == "crack":
        return (
            noise * 0.055
            + math.sin(math.tau * (231.0 + 95.0 * t) * t) * 0.07
        ) * math.exp(-t * 5.6)
    if kind == "underwater":
        return (
            math.sin(math.tau * 32.7 * t) * 0.058
            + math.sin(math.tau * 54.1 * t) * 0.031
            + noise * 0.011
        ) * (1.0 - math.exp(-t * 2.5)) * math.exp(-t * 0.18)
    swell = math.sin(math.pi * min(1.0, t / 4.5)) ** 2
    return (
        math.sin(math.tau * (61.0 - 7.0 * t) * t) * 0.035 + noise * 0.016
    ) * swell


def make_bell_layers(seed: int, force: bool) -> None:
    body_rng = random.Random(seed + 31)
    crack_rng = random.Random(seed + 37)
    under_rng = random.Random(seed + 41)
    reverse_rng = random.Random(seed + 43)
    write_mono(
        "assets/audio/sfx/bell_body.wav",
        8.0,
        lambda _i, t: bell_component(t, "body", body_rng.uniform(-1.0, 1.0)),
        force,
    )
    write_mono(
        "assets/audio/sfx/bell_crack.wav",
        2.2,
        lambda _i, t: bell_component(t, "crack", crack_rng.uniform(-1.0, 1.0)),
        force,
    )
    write_mono(
        "assets/audio/sfx/bell_underwater.wav",
        10.0,
        lambda _i, t: bell_component(t, "underwater", under_rng.uniform(-1.0, 1.0)),
        force,
    )
    write_mono(
        "assets/audio/sfx/bell_reverse_tail.wav",
        5.0,
        lambda _i, t: bell_component(t, "reverse", reverse_rng.uniform(-1.0, 1.0)),
        force,
    )

    duration = 27.0
    frames = int(duration * SAMPLE_RATE)
    mix_rng = random.Random(seed + 47)
    samples = array("h")
    wash_l = 0.0
    wash_r = 0.0
    for index in range(frames):
        t = index / SAMPLE_RATE
        wash_l = wash_l * 0.992 + mix_rng.uniform(-1.0, 1.0) * 0.008
        wash_r = wash_r * 0.992 + mix_rng.uniform(-1.0, 1.0) * 0.008
        left = wash_l * 0.018
        right = wash_r * 0.018
        if t < 8.0:
            body = bell_component(t, "body")
            left += body * 0.84
            right += body
        if 0.15 <= t < 2.35:
            crack = bell_component(t - 0.15, "crack", mix_rng.uniform(-1.0, 1.0))
            left += crack
            right += crack * 0.7
        if 4.0 <= t < 14.0:
            under = bell_component(t - 4.0, "underwater", mix_rng.uniform(-1.0, 1.0))
            left += under * 0.82
            right += under
        if 14.0 <= t < 19.0:
            reverse = bell_component(t - 14.0, "reverse", mix_rng.uniform(-1.0, 1.0))
            left += reverse
            right += reverse * 0.78
        if 18.2 <= t < 26.5:
            final_body = bell_component(t - 18.2, "body") * 0.68
            left += final_body
            right += final_body * 0.88
        samples.append(clamp_sample(left))
        samples.append(clamp_sample(right))
    write_stereo_samples("assets/audio/sfx/bell_memory_mix.wav", samples, force)


def main() -> int:
    args = base_parser("Generate P3 narrative audio assets.").parse_args()
    make_ambience(
        "assets/audio/ambience/refugee_shelter_evening.wav",
        90.0,
        args.seed + 3101,
        False,
        args.force,
    )
    make_ambience(
        "assets/audio/ambience/ritual_storehouse_rain.wav",
        90.0,
        args.seed + 3103,
        True,
        args.force,
    )
    make_music(
        "assets/audio/music/music_refugees_evening.wav",
        48.0,
        args.seed + 3201,
        False,
        args.force,
    )
    make_music(
        "assets/audio/music/music_cracked_bell_memory.wav",
        48.0,
        args.seed + 3203,
        True,
        args.force,
    )
    make_bell_layers(args.seed + 3301, args.force)

    song_rng = random.Random(args.seed + 3401)
    notes = ((0.2, 220.0), (1.3, 261.63), (2.4, 293.66), (3.5, 261.63), (4.6, 220.0))

    def old_song(_index: int, t: float) -> float:
        value = song_rng.uniform(-1.0, 1.0) * 0.004
        for start, frequency in notes:
            dt = t - start
            if 0.0 <= dt < 0.95:
                envelope = math.sin(math.pi * dt / 0.95) ** 0.7
                value += (
                    math.sin(math.tau * frequency * dt)
                    + 0.18 * math.sin(math.tau * frequency * 2.0 * dt)
                ) * envelope * 0.037
        return value

    write_mono("assets/audio/sfx/liuniang_old_song_hum.wav", 6.0, old_song, args.force)

    fire_rng = random.Random(args.seed + 3403)

    def fire_crackle(_index: int, t: float) -> float:
        pulse = 1.0 if abs(math.sin(math.tau * 7.3 * t)) > 0.92 else 0.22
        return fire_rng.uniform(-1.0, 1.0) * pulse * 0.022

    write_mono("assets/audio/sfx/shelter_fire_crackle.wav", 8.0, fire_crackle, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
