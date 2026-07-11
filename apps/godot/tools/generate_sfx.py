"""Generate UI, footsteps, wood, writing, grain, cloth, and P2 action SFX."""

from __future__ import annotations

import math
import random

from asset_tools_common import base_parser
from audio_tools_common import write_mono


def main() -> int:
    args = base_parser("Generate P0/P2 action and UI SFX.").parse_args()

    def ui_confirm(_index: int, t: float) -> float:
        envelope = math.exp(-t * 12.0)
        return (
            math.sin(math.tau * 440.0 * t) * 0.11
            + math.sin(math.tau * 660.0 * t) * 0.045
        ) * envelope

    write_mono("assets/audio/sfx/ui_confirm.wav", 0.32, ui_confirm, args.force)

    for variant in range(1, 7):
        rng = random.Random(args.seed * 17 + variant)
        noise_values = [rng.uniform(-1.0, 1.0) for _ in range(18_000)]

        def footstep(index: int, t: float, values=noise_values, offset=variant) -> float:
            envelope = math.exp(-t * (16.0 + offset * 0.35))
            noise = values[index % len(values)]
            body = math.sin(math.tau * (88.0 + offset * 4.0) * t) * math.exp(-t * 20.0)
            grit = noise * 0.075 * envelope
            return body * 0.12 + grit

        write_mono(
            f"assets/audio/sfx/footstep_dry_{variant:02d}.wav",
            0.38,
            footstep,
            args.force,
        )

    for variant in range(1, 5):
        rng = random.Random(args.seed * 31 + variant)
        phases = [rng.uniform(0.0, math.tau) for _ in range(3)]

        def cable_creak(_index: int, t: float, offset=variant, phase=phases) -> float:
            envelope = math.sin(math.pi * min(1.0, t / 1.18)) * math.exp(-t * 0.82)
            pitch = 48.0 + offset * 5.0 + 7.0 * math.sin(t * 8.0 + phase[0])
            return (
                math.sin(math.tau * pitch * t + phase[1])
                + 0.34 * math.sin(math.tau * (pitch * 2.37) * t + phase[2])
            ) * envelope * 0.09

        write_mono(
            f"assets/audio/sfx/wood_cable_creak_{variant:02d}.wav",
            1.25,
            cable_creak,
            args.force,
        )

    for variant in range(1, 5):
        rng = random.Random(args.seed * 37 + variant)
        noise = [rng.uniform(-1.0, 1.0) for _ in range(12_000)]

        def hull_creak(index: int, t: float, offset=variant, values=noise) -> float:
            envelope = math.sin(math.pi * min(1.0, t / 1.45)) * math.exp(-t * 0.65)
            body = math.sin(math.tau * (59.0 + offset * 4.0 + t * 12.0) * t)
            return body * envelope * 0.085 + values[index % len(values)] * envelope * 0.014

        write_mono(
            f"assets/audio/sfx/boat_hull_creak_{variant:02d}.wav",
            1.5,
            hull_creak,
            args.force,
        )

    for variant in range(1, 6):
        rng = random.Random(args.seed * 41 + variant)
        scratch = [rng.uniform(-1.0, 1.0) for _ in range(9000)]

        def tablet_write(index: int, t: float, offset=variant, values=scratch) -> float:
            pulse = 0.38 + 0.62 * abs(math.sin(math.tau * (9.0 + offset * 0.4) * t))
            envelope = math.sin(math.pi * min(1.0, t / 0.72)) ** 0.7
            grain = values[index % len(values)] * pulse * envelope * 0.045
            wood = math.sin(math.tau * (310.0 + offset * 17.0) * t) * envelope * 0.008
            return grain + wood

        write_mono(
            f"assets/audio/sfx/wood_tablet_write_{variant:02d}.wav",
            0.78,
            tablet_write,
            args.force,
        )

    def brush_lift(_index: int, t: float) -> float:
        envelope = math.exp(-t * 17.0)
        return (
            math.sin(math.tau * 580.0 * t) * 0.032
            + math.sin(math.tau * 910.0 * t) * 0.014
        ) * envelope

    write_mono("assets/audio/sfx/brush_lift.wav", 0.34, brush_lift, args.force)

    for variant in range(1, 6):
        rng = random.Random(args.seed * 43 + variant)
        noise = [rng.uniform(-1.0, 1.0) for _ in range(13_000)]

        def cloth_rustle(index: int, t: float, offset=variant, values=noise) -> float:
            envelope = math.sin(math.pi * min(1.0, t / 0.65)) * math.exp(-t * 1.2)
            flutter = 0.35 + 0.65 * abs(math.sin(math.tau * (5.0 + offset * 0.31) * t))
            return values[index % len(values)] * envelope * flutter * 0.038

        write_mono(
            f"assets/audio/sfx/cloth_rustle_{variant:02d}.wav",
            0.72,
            cloth_rustle,
            args.force,
        )

    for variant in range(1, 4):
        rng = random.Random(args.seed * 47 + variant)
        impacts = (0.03, 0.12 + variant * 0.012, 0.24 + variant * 0.009)

        def firewood_drop(index: int, t: float, offset=variant, hits=impacts) -> float:
            value = 0.0
            for hit_index, hit in enumerate(hits):
                dt = t - hit
                if 0.0 <= dt < 0.18:
                    env = math.exp(-dt * (32.0 + hit_index * 5.0))
                    value += math.sin(math.tau * (145.0 + offset * 19.0 + hit_index * 33.0) * dt) * env * 0.11
                    value += rng.uniform(-1.0, 1.0) * env * 0.025
            return value

        write_mono(
            f"assets/audio/sfx/firewood_drop_{variant:02d}.wav",
            0.62,
            firewood_drop,
            args.force,
        )

    for variant in range(1, 4):
        def bowl_place(_index: int, t: float, offset=variant) -> float:
            envelope = math.exp(-t * (21.0 + offset))
            return (
                math.sin(math.tau * (190.0 + offset * 22.0) * t) * 0.09
                + math.sin(math.tau * (520.0 + offset * 31.0) * t) * 0.035
            ) * envelope

        write_mono(
            f"assets/audio/sfx/bowl_place_{variant:02d}.wav",
            0.48,
            bowl_place,
            args.force,
        )

    grain_rng = random.Random(args.seed + 557)
    grain_noise = [grain_rng.uniform(-1.0, 1.0) for _ in range(20_000)]

    def grain_pour(index: int, t: float) -> float:
        envelope = math.sin(math.pi * min(1.0, t / 1.35)) ** 0.55
        ticks = 1.0 if grain_noise[index % len(grain_noise)] > 0.79 else 0.0
        return ticks * grain_noise[(index * 7) % len(grain_noise)] * envelope * 0.075

    write_mono("assets/audio/sfx/grain_pour_small.wav", 1.4, grain_pour, args.force)

    def grain_last(index: int, t: float) -> float:
        pulses = 0.0
        for hit in (0.05, 0.19, 0.34, 0.61):
            dt = t - hit
            if 0.0 <= dt < 0.08:
                pulses += grain_noise[(index * 5) % len(grain_noise)] * math.exp(-dt * 50.0) * 0.07
        return pulses

    write_mono("assets/audio/sfx/grain_last_scatter.wav", 0.9, grain_last, args.force)

    water_rng = random.Random(args.seed + 601)
    water_noise = [water_rng.uniform(-1.0, 1.0) for _ in range(20_000)]

    def basin_water(index: int, t: float) -> float:
        smooth = sum(water_noise[(index - k) % len(water_noise)] for k in range(8)) / 8.0
        return smooth * (0.04 + 0.03 * abs(math.sin(math.tau * 2.1 * t))) * math.sin(math.pi * min(1.0, t / 1.9))

    write_mono("assets/audio/sfx/basin_water.wav", 2.0, basin_water, args.force)

    def dock_impact(index: int, t: float) -> float:
        envelope = math.exp(-t * 7.5)
        return (
            math.sin(math.tau * 72.0 * t) * 0.13
            + math.sin(math.tau * 131.0 * t) * 0.07
            + water_noise[index % len(water_noise)] * 0.024
        ) * envelope

    write_mono("assets/audio/sfx/boat_dock_impact.wav", 1.2, dock_impact, args.force)

    def memory_water(index: int, t: float) -> float:
        rise = min(1.0, t / 0.7)
        fall = math.exp(-max(0.0, t - 0.8) * 0.9)
        smooth = sum(water_noise[(index - k) % len(water_noise)] for k in range(16)) / 16.0
        undertone = math.sin(math.tau * 43.0 * t) * 0.06 + math.sin(math.tau * 71.0 * t) * 0.025
        return (smooth * 0.11 + undertone) * rise * fall

    write_mono("assets/audio/sfx/name_memory_water.wav", 2.4, memory_water, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
