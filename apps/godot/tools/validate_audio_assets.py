"""Validate P0/P2/P3/P4/P5 WAV encoding, duration, channel layout, peaks, and variants."""

from __future__ import annotations

import json
import sys
import wave
from array import array
from pathlib import Path

from asset_tools_common import PROJECT_ROOT


REQUIRED_AUDIO = {
    "assets/audio/ambience/river_morning.wav": (2, 90.0),
    "assets/audio/ambience/ferry_day.wav": (2, 90.0),
    "assets/audio/music/music_old_ferry_morning.wav": (2, 40.0),
    "assets/audio/music/music_name_and_registry.wav": (2, 40.0),
    "assets/audio/music/music_ferry_day_news.wav": (2, 40.0),
    "assets/audio/sfx/ui_confirm.wav": (1, 0.2),
    "assets/audio/sfx/basin_water.wav": (1, 1.8),
    "assets/audio/sfx/brush_lift.wav": (1, 0.25),
    "assets/audio/sfx/grain_pour_small.wav": (1, 1.2),
    "assets/audio/sfx/grain_last_scatter.wav": (1, 0.7),
    "assets/audio/sfx/boat_dock_impact.wav": (1, 1.0),
    "assets/audio/sfx/name_memory_water.wav": (1, 2.2),
    "assets/audio/ambience/refugee_shelter_evening.wav": (2, 90.0),
    "assets/audio/ambience/ritual_storehouse_rain.wav": (2, 90.0),
    "assets/audio/music/music_refugees_evening.wav": (2, 40.0),
    "assets/audio/music/music_cracked_bell_memory.wav": (2, 40.0),
    "assets/audio/sfx/liuniang_old_song_hum.wav": (1, 5.8),
    "assets/audio/sfx/shelter_fire_crackle.wav": (1, 7.8),
    "assets/audio/sfx/bell_body.wav": (1, 7.8),
    "assets/audio/sfx/bell_crack.wav": (1, 2.0),
    "assets/audio/sfx/bell_underwater.wav": (1, 9.8),
    "assets/audio/sfx/bell_reverse_tail.wav": (1, 4.8),
    "assets/audio/sfx/bell_memory_mix.wav": (2, 27.0),
    "assets/audio/ambience/rain_night.wav": (2, 120.0),
    "assets/audio/music/music_cart_crash_pressure.wav": (2, 40.0),
    "assets/audio/sfx/cart_wheel_break.wav": (1, 1.0),
    "assets/audio/sfx/cart_impact_mud.wav": (1, 1.4),
    "assets/audio/sfx/horse_panic.wav": (1, 1.6),
    "assets/audio/sfx/water_bucket_drag.wav": (1, 2.0),
    "assets/audio/sfx/wet_ink_spread.wav": (1, 3.8),
    "assets/audio/sfx/child_cry_pressure_loop.wav": (1, 29.0),
    "assets/audio/sfx/crowd_call_names_loop.wav": (2, 29.0),
}


def main() -> int:
    failures: list[str] = []
    report: list[dict[str, object]] = []

    for relative, (expected_channels, minimum_duration) in REQUIRED_AUDIO.items():
        path = PROJECT_ROOT / relative
        if not path.is_file():
            failures.append(f"missing audio: {relative}")
            continue
        with wave.open(str(path), "rb") as source:
            channels = source.getnchannels()
            sample_width = source.getsampwidth()
            sample_rate = source.getframerate()
            frame_count = source.getnframes()
            raw = source.readframes(frame_count)
        duration = frame_count / sample_rate
        samples = array("h")
        samples.frombytes(raw)
        peak = max((abs(value) for value in samples), default=0)
        peak_dbfs = -120.0 if peak == 0 else 20.0 * __import__("math").log10(peak / 32767.0)

        if channels != expected_channels:
            failures.append(f"{relative}: expected {expected_channels} channels, got {channels}")
        if sample_width != 2:
            failures.append(f"{relative}: expected 16-bit PCM")
        if sample_rate != 44_100:
            failures.append(f"{relative}: expected 44100 Hz, got {sample_rate}")
        if duration + 0.01 < minimum_duration:
            failures.append(f"{relative}: duration {duration:.2f}s is below {minimum_duration}s")
        if peak_dbfs > -1.0:
            failures.append(f"{relative}: peak {peak_dbfs:.2f} dBFS exceeds -1 dBFS")
        report.append(
            {
                "path": relative,
                "channels": channels,
                "sample_rate": sample_rate,
                "bit_depth": sample_width * 8,
                "duration_seconds": round(duration, 3),
                "peak_dbfs": round(peak_dbfs, 3),
            }
        )

    footsteps = sorted((PROJECT_ROOT / "assets" / "audio" / "sfx").glob("footstep_dry_*.wav"))
    if len(footsteps) < 6:
        failures.append(f"expected at least 6 dry footstep variants, got {len(footsteps)}")
    variant_requirements = {
        "wood_cable_creak_*.wav": 4,
        "boat_hull_creak_*.wav": 4,
        "wood_tablet_write_*.wav": 5,
        "cloth_rustle_*.wav": 5,
        "firewood_drop_*.wav": 3,
        "bowl_place_*.wav": 3,
        "wood_tablet_splash_*.wav": 4,
    }
    sfx_dir = PROJECT_ROOT / "assets" / "audio" / "sfx"
    for pattern, minimum in variant_requirements.items():
        count = len(list(sfx_dir.glob(pattern)))
        if count < minimum:
            failures.append(f"expected at least {minimum} variants for {pattern}, got {count}")

    review_dir = PROJECT_ROOT / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    (review_dir / "audio_loudness_report.json").write_text(
        json.dumps({"p2_p3_audio": report}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    loudness_lines = [
        "# P0/P2/P3/P4/P5 Audio Loudness Report",
        "",
        "| Path | Channels | Rate | Bit depth | Duration | Peak |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for item in report:
        loudness_lines.append(
            "| `{path}` | {channels} | {sample_rate} Hz | {bit_depth}-bit | "
            "{duration_seconds:.3f} s | {peak_dbfs:.3f} dBFS |".format(**item)
        )
    (review_dir / "audio_loudness_report.md").write_text(
        "\n".join(loudness_lines) + "\n",
        encoding="utf-8",
    )
    cue_lines = [
        "# P2/P3/P4/P5 Audio Cue List",
        "",
        "| Cue | Scene | Entry | Exit | Bus |",
        "|---|---|---|---|---|",
        "| `river_morning.wav` | SC01 / SC02 | 河雾淡入 | 午前渡口 | Ambience |",
        "| `ferry_day.wav` | SC03 | 东来商船尚在画外 | P2 结束 | Ambience |",
        "| `music_old_ferry_morning.wav` | SC01 | 河雾建立 | 前往辛衡书案 | Music |",
        "| `music_name_and_registry.wav` | SC02 | 辛衡递木牍 | 写名后转入午前 | Music |",
        "| `music_ferry_day_news.wav` | SC03 | 午前旧渡日常 | P2 结束 | Music |",
        "| `footstep_dry_01—06.wav` | SC01—SC03 | 主角移动时轮换 | 停步 | SFX |",
        "| `wood_cable_creak_01.wav` | SC01 | 木缆镜头 | One shot | SFX |",
        "| `wood_tablet_write_01.wav` | SC02 | 按住 E 完成写名 | One shot | SFX |",
        "| `name_memory_water.wav` | SC02 | 姓名落笔后的短暂异常 | One shot | SFX |",
        "| `firewood_drop_01.wav` / `bowl_place_01.wav` | SC02 | 禾安抱柴、放粥 | One shot | SFX |",
        "| `boat_hull_creak_01.wav` / `boat_dock_impact.wav` | SC03 | 声音先到、商船靠岸 | One shot | SFX |",
        "| `ui_confirm.wav` | Title | Menu confirmation | One shot | UI |",
        "| `refugee_shelter_evening.wav` | SC04 | 流民入棚 | 进入礼器库 | Ambience |",
        "| `music_refugees_evening.wav` | SC04 | 流民入场 | 钟声引路 | Music |",
        "| `liuniang_old_song_hum.wav` | SC04 | 柳娘开口 | 地名处突然停住 | SFX |",
        "| `grain_last_scatter.wav` | SC04 | 禾安倒碎米 | One shot | SFX |",
        "| `ritual_storehouse_rain.wav` | SC05 | 入库 | 裂钟记忆时暂退 | Ambience |",
        "| `bell_body/crack/underwater/reverse_tail.wav` | SC04 / SC05 | 空间钟声与记忆层 | 分层尾音 | SFX |",
        "| `bell_memory_mix.wav` | SC05 | 长按触钟 | 27 秒记忆结束 | SFX |",
        "| `music_cracked_bell_memory.wav` | SC05 | 触钟 | 回到雨夜 | Music |",
        "| `rain_night.wav` | SC06 | 车翻硬切后立刻进入 | 序章选择反馈后 | Ambience |",
        "| `music_cart_crash_pressure.wav` | SC06 | 现场扫描开始 | 选择反馈后 | Music |",
        "| `cart_wheel_break.wav` / `horse_panic.wav` / `cart_impact_mud.wav` | SC06 | 裂钟记忆后黑场硬切 | One shot | SFX |",
        "| `child_cry_pressure_loop.wav` | SC06 左侧 | 扫到车下孩子 | 选择反馈后 | SFX 2D |",
        "| `wet_ink_spread.wav` / `wood_tablet_splash_01.wav` | SC06 中间 | 扫到湿简与抢救湿简 | One shot / 2D | SFX |",
        "| `crowd_call_names_loop.wav` | SC06 右侧 | 扫到失散人群 | 选择反馈后 | SFX 2D |",
        "| `water_bucket_drag.wav` | SC06 左侧 | 禾安拖热水桶 | One shot | SFX |",
    ]
    (review_dir / "audio_cue_list.md").write_text(
        "\n".join(cue_lines) + "\n",
        encoding="utf-8",
    )

    if failures:
        for failure in failures:
            print(f"[audio validation] FAIL: {failure}", file=sys.stderr)
        return 1
    print(
        f"[audio validation] PASS: {len(report)} P0/P2/P3/P4/P5 core files, "
        f"{len(footsteps)} footstep variants plus narrative action families, WAV PCM 16-bit/44.1 kHz."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
