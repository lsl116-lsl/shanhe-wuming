"""Generate P4 rain-night cart crash, directional pressure, and feedback audio."""

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


def make_rain_night(path: str, duration: float, seed: int, force: bool) -> None:
    rng = random.Random(seed)
    frames = int(duration * SAMPLE_RATE)
    samples = array("h")
    rain_l = 0.0
    rain_r = 0.0
    gutter = 0.0
    thunder_times = (31.0, 84.0)
    for index in range(frames):
        t = index / SAMPLE_RATE
        rain_l = rain_l * 0.968 + rng.uniform(-1.0, 1.0) * 0.032
        rain_r = rain_r * 0.968 + rng.uniform(-1.0, 1.0) * 0.032
        gutter = gutter * 0.995 + rng.uniform(-1.0, 1.0) * 0.005
        left = rain_l * 0.048 + gutter * 0.018
        right = rain_r * 0.05 + gutter * 0.015
        for event_time in thunder_times:
            dt = t - event_time
            if 0.0 <= dt < 8.0:
                roll = math.sin(math.tau * 36.0 * dt) * math.exp(-dt * 0.55) * 0.025
                left += roll
                right += roll * 0.86
        samples.append(clamp_sample(left))
        samples.append(clamp_sample(right))
    equal_power_fade_to_start(samples, 2.0)
    write_stereo_samples(path, samples, force)


def make_pressure_music(path: str, duration: float, seed: int, force: bool) -> None:
    rng = random.Random(seed)
    frames = int(duration * SAMPLE_RATE)
    samples = array("h")
    pulses = [2.0]
    while pulses[-1] < duration - 3.0:
        pulses.append(pulses[-1] + rng.choice((2.6, 3.1, 3.8, 4.6)))
    for index in range(frames):
        t = index / SAMPLE_RATE
        low = math.sin(math.tau * 43.0 * t) * 0.018
        air = rng.uniform(-1.0, 1.0) * 0.006
        left = low + air
        right = low * 0.9 - air * 0.72
        for event_time in pulses:
            dt = t - event_time
            if 0.0 <= dt < 1.35:
                env = math.exp(-dt * 2.9)
                drum = math.sin(math.tau * 74.0 * dt) * env * 0.05
                left += drum
                right += drum * 0.82
        samples.append(clamp_sample(left))
        samples.append(clamp_sample(right))
    equal_power_fade_to_start(samples, 2.0)
    write_stereo_samples(path, samples, force)


def make_cart_wheel_break(force: bool) -> None:
    rng = random.Random(4301)

    def sample(_index: int, t: float) -> float:
        crack = 0.0
        for start, freq in ((0.05, 210.0), (0.18, 118.0), (0.32, 72.0)):
            dt = t - start
            if 0.0 <= dt < 0.45:
                crack += (
                    math.sin(math.tau * freq * dt)
                    + rng.uniform(-1.0, 1.0) * 0.9
                ) * math.exp(-dt * 10.0) * 0.05
        return crack

    write_mono("assets/audio/sfx/cart_wheel_break.wav", 1.2, sample, force)


def make_cart_impact(force: bool) -> None:
    rng = random.Random(4303)

    def sample(_index: int, t: float) -> float:
        thud = math.sin(math.tau * 45.0 * t) * math.exp(-t * 3.0) * 0.09
        mud = rng.uniform(-1.0, 1.0) * math.exp(-t * 5.0) * 0.035
        splash = 0.0
        if 0.14 <= t < 0.8:
            dt = t - 0.14
            splash = rng.uniform(-1.0, 1.0) * math.exp(-dt * 6.0) * 0.04
        return thud + mud + splash

    write_mono("assets/audio/sfx/cart_impact_mud.wav", 1.6, sample, force)


def make_horse_panic(force: bool) -> None:
    rng = random.Random(4305)

    def sample(_index: int, t: float) -> float:
        value = 0.0
        for start, base in ((0.1, 520.0), (0.92, 440.0)):
            dt = t - start
            if 0.0 <= dt < 0.62:
                sweep = base + 180.0 * math.sin(dt * 8.0)
                value += (
                    math.sin(math.tau * sweep * dt)
                    + 0.25 * math.sin(math.tau * sweep * 2.02 * dt)
                ) * math.sin(math.pi * dt / 0.62) * 0.045
        return value + rng.uniform(-1.0, 1.0) * 0.003

    write_mono("assets/audio/sfx/horse_panic.wav", 1.8, sample, force)


def make_bucket_drag(force: bool) -> None:
    rng = random.Random(4307)

    def sample(_index: int, t: float) -> float:
        scrape = rng.uniform(-1.0, 1.0) * 0.015
        pulse = abs(math.sin(math.tau * 4.3 * t)) ** 8
        return scrape + pulse * math.sin(math.tau * 132.0 * t) * 0.04

    write_mono("assets/audio/sfx/water_bucket_drag.wav", 2.2, sample, force)


def make_tablet_splashes(force: bool) -> None:
    for variant in range(1, 5):
        rng = random.Random(4310 + variant)

        def sample(_index: int, t: float, local_rng=rng) -> float:
            drip = local_rng.uniform(-1.0, 1.0) * math.exp(-t * 9.0) * 0.045
            ring = math.sin(math.tau * (280.0 + variant * 33.0) * t) * math.exp(-t * 10.0) * 0.018
            return drip + ring

        write_mono(f"assets/audio/sfx/wood_tablet_splash_{variant:02d}.wav", 0.9, sample, force)


def make_wet_ink(force: bool) -> None:
    rng = random.Random(4321)

    def sample(_index: int, t: float) -> float:
        cycle = t % 3.4
        spread_env = (1.0 - math.exp(-cycle * 3.0)) * math.exp(-cycle * 0.55)
        spread = rng.uniform(-1.0, 1.0) * spread_env * 0.014
        ripple = math.sin(math.tau * 113.0 * cycle) * math.exp(-cycle * 1.8) * 0.018
        return spread + ripple

    write_mono("assets/audio/sfx/wet_ink_spread.wav", 30.0, sample, force)


def make_child_cry(force: bool) -> None:
    rng = random.Random(4323)

    def sample(_index: int, t: float) -> float:
        cycle = t % 2.8
        env = math.sin(math.pi * min(1.0, cycle / 1.1)) if cycle < 1.1 else math.exp(-(cycle - 1.1) * 2.8)
        pitch = 380.0 + 65.0 * math.sin(t * 4.0)
        cry = (math.sin(math.tau * pitch * t) + 0.22 * math.sin(math.tau * pitch * 2.01 * t)) * env * 0.026
        return cry + rng.uniform(-1.0, 1.0) * 0.003

    write_mono("assets/audio/sfx/child_cry_pressure_loop.wav", 30.0, sample, force)


def make_crowd_loop(force: bool) -> None:
    rng = random.Random(4325)
    frames = int(30.0 * SAMPLE_RATE)
    samples = array("h")
    call_times = [0.4, 2.1, 4.6, 7.4, 10.2, 13.7, 16.3, 19.6, 23.2, 26.1, 28.4]
    for index in range(frames):
        t = index / SAMPLE_RATE
        bed = rng.uniform(-1.0, 1.0) * 0.008
        left = bed
        right = bed * 0.85
        for n, start in enumerate(call_times):
            dt = t - start
            if 0.0 <= dt < 0.95:
                f = 155.0 + (n % 4) * 34.0
                env = math.sin(math.pi * dt / 0.95)
                voice = (math.sin(math.tau * f * dt) + 0.18 * math.sin(math.tau * f * 2.0 * dt)) * env * 0.026
                pan = -0.45 if n % 2 == 0 else 0.42
                left += voice * (1.0 - max(0.0, pan))
                right += voice * (1.0 + min(0.0, pan))
        samples.append(clamp_sample(left))
        samples.append(clamp_sample(right))
    equal_power_fade_to_start(samples, 1.5)
    write_stereo_samples("assets/audio/sfx/crowd_call_names_loop.wav", samples, force)


def main() -> int:
    args = base_parser("Generate P4 rain-night crash audio.").parse_args()
    make_rain_night("assets/audio/ambience/rain_night.wav", 120.0, args.seed + 4201, args.force)
    make_pressure_music("assets/audio/music/music_cart_crash_pressure.wav", 48.0, args.seed + 4203, args.force)
    make_cart_wheel_break(args.force)
    make_cart_impact(args.force)
    make_horse_panic(args.force)
    make_bucket_drag(args.force)
    make_tablet_splashes(args.force)
    make_wet_ink(args.force)
    make_child_cry(args.force)
    make_crowd_loop(args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
