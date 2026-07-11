"""Build generated-asset inventory, content aliases, and provenance notes."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from asset_tools_common import DEFAULT_SEED, GENERATOR_VERSION, PROJECT_ROOT


GENERATED_ROOTS = (
    PROJECT_ROOT / "assets" / "characters",
    PROJECT_ROOT / "assets" / "environments",
    PROJECT_ROOT / "assets" / "props",
    PROJECT_ROOT / "assets" / "fx",
    PROJECT_ROOT / "assets" / "ui",
    PROJECT_ROOT / "assets" / "audio",
    PROJECT_ROOT / "art" / "reference",
)


def generator_for(path: str) -> str:
    if "/p6a/" in path or path.startswith("art/reference/generated_p6a_"):
        return "tools/generate_p6a_visual_assets.py"
    if path.startswith("art/reference/generated_p5_"):
        return "tools/generate_review_boards.py"
    if path.endswith("_ai_reference.png"):
        return "OpenAI built-in image_gen"
    if "/p4/" in path and (
        path.startswith("assets/environments/")
        or path.startswith("assets/props/")
        or path.startswith("assets/fx/")
    ):
        return "tools/generate_p4_art_assets.py"
    if "/p3/" in path and path.startswith("assets/characters/"):
        return "tools/generate_p3_character_assets.py"
    if "/p3/" in path and (
        path.startswith("assets/environments/")
        or path.startswith("assets/props/")
        or path.startswith("assets/fx/")
    ):
        return "tools/generate_p3_art_assets.py"
    if Path(path).name in {
        "rain_night.wav",
        "music_cart_crash_pressure.wav",
        "cart_wheel_break.wav",
        "cart_impact_mud.wav",
        "horse_panic.wav",
        "water_bucket_drag.wav",
        "wet_ink_spread.wav",
        "child_cry_pressure_loop.wav",
        "crowd_call_names_loop.wav",
        "wood_tablet_splash_01.wav",
        "wood_tablet_splash_02.wav",
        "wood_tablet_splash_03.wav",
        "wood_tablet_splash_04.wav",
        "refugee_shelter_evening.wav",
        "ritual_storehouse_rain.wav",
        "music_refugees_evening.wav",
        "music_cracked_bell_memory.wav",
        "bell_body.wav",
        "bell_crack.wav",
        "bell_underwater.wav",
        "bell_reverse_tail.wav",
        "bell_memory_mix.wav",
        "liuniang_old_song_hum.wav",
        "shelter_fire_crackle.wav",
    }:
        return "tools/generate_p3_audio_assets.py"
    if path.startswith("assets/characters/"):
        return "tools/generate_character_assets.py"
    if path.startswith("assets/environments/"):
        return "tools/generate_environment_assets.py"
    if path.startswith("assets/ui/"):
        return "tools/generate_ui_assets.py"
    if path.startswith("assets/fx/"):
        return "tools/generate_fx_assets.py"
    if path.startswith("assets/audio/ambience/"):
        return "tools/generate_ambience.py"
    if path.startswith("assets/audio/sfx/"):
        return "tools/generate_sfx.py"
    if path.startswith("assets/audio/music/"):
        return "tools/generate_music_stems.py"
    if "character" in path:
        return "tools/generate_character_assets.py"
    return "tools/generate_environment_assets.py"


def category_for(path: str) -> str:
    parts = Path(path).parts
    if path.startswith("art/reference/"):
        return "review"
    if len(parts) > 1:
        return parts[1]
    return "generated"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    files: list[Path] = []
    for root in GENERATED_ROOTS:
        if root.exists():
            files.extend(
                path
                for path in root.rglob("*")
                if path.is_file() and path.suffix != ".import"
            )
    files = sorted(set(files))
    if not files:
        raise RuntimeError("No generated assets found. Run generators first.")

    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    assets = []
    for file_path in files:
        relative = file_path.relative_to(PROJECT_ROOT).as_posix()
        source_type = (
            "ai_generated_reference"
            if relative.endswith("_ai_reference.png")
            else "procedural_generated"
        )
        assets.append(
            {
                "path": relative,
                "category": category_for(relative),
                "generator_script": generator_for(relative),
                "generator_version": GENERATOR_VERSION,
                "seed": args.seed,
                "source_type": source_type,
                "license": "project_owned",
                "created_at": created_at,
                "sha256": sha256(file_path),
                "notes": (
                    "P2/P3 visual production reference generated with the built-in image tool"
                    if source_type == "ai_generated_reference"
                    else "P0/P2/P3/P4/P5/P6-A deterministic runtime or review asset"
                ),
            }
        )

    manifest = {
        "manifest_version": "p5.0",
        "generated_at": created_at,
        "seed": args.seed,
        "assets": assets,
    }
    manifest_path = PROJECT_ROOT / "assets" / "generated_asset_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    content_manifest = {
        "content_version": "p5.0",
        "generated_manifest": "res://assets/generated_asset_manifest.json",
        "fallbacks": {
            "font": "res://assets/ui/fonts/system_chinese_fallback.tres"
        },
        "p0_assets": {
            "player_layers": [
                "res://assets/characters/player/p0/player_shadow.svg",
                "res://assets/characters/player/p0/player_body.svg",
                "res://assets/characters/player/p0/player_head.svg",
                "res://assets/characters/player/p0/player_front_arm_tablet.svg",
            ],
            "old_ferry_layers": [
                "res://assets/environments/old_ferry/p0/old_ferry_far.svg",
                "res://assets/environments/old_ferry/p0/old_ferry_mid.svg",
                "res://assets/environments/old_ferry/p0/old_ferry_near.svg",
            ],
            "fog_front": "res://assets/fx/p0/fog_front.svg",
            "river_morning": "res://assets/audio/ambience/river_morning.wav",
            "old_ferry_music": "res://assets/audio/music/music_old_ferry_morning.wav",
            "ui_confirm": "res://assets/audio/sfx/ui_confirm.wav",
        },
        "runtime_assets": {
            "scene.sc01_home_morning": "res://scenes/prologue/SC01_Home_Morning.tscn",
            "scene.sc02_xinheng_desk": "res://scenes/prologue/SC02_Xinheng_Desk.tscn",
            "scene.sc03_ferry_day": "res://scenes/prologue/SC03_Ferry_Day.tscn",
            "scene.sc04_refugee_shelter": "res://scenes/prologue/SC04_Refugee_Shelter.tscn",
            "scene.sc05_ritual_storehouse": "res://scenes/prologue/SC05_Ritual_Storehouse.tscn",
            "scene.sc06_cart_crash_rain": "res://scenes/prologue/SC06_Cart_Crash_Rain.tscn",
            "scene.sc07_prologue_end": "res://scenes/prologue/SC07_Prologue_End.tscn",
            "actor.mother": "res://scenes/characters/Mother.tscn",
            "actor.xinheng": "res://scenes/characters/Xinheng.tscn",
            "actor.hean": "res://scenes/characters/Hean.tscn",
            "actor.boat_owner": "res://scenes/characters/BoatOwner.tscn",
            "actor.ferry_worker": "res://scenes/characters/FerryWorker.tscn",
            "actor.ferry_woman": "res://scenes/characters/FerryWoman.tscn",
            "actor.hanning": "res://scenes/characters/Hanning.tscn",
            "actor.hanning_mother": "res://scenes/characters/HanningMother.tscn",
            "actor.liuniang": "res://scenes/characters/Liuniang.tscn",
            "actor.refugee_old": "res://scenes/characters/RefugeeOld.tscn",
            "actor.refugee_mother": "res://scenes/characters/RefugeeMother.tscn",
            "actor.refugee_man": "res://scenes/characters/RefugeeMan.tscn",
            "interaction.default": "res://scenes/core/InteractableArea2D.tscn",
            "ambience.river_morning": "res://assets/audio/ambience/river_morning.wav",
            "ambience.ferry_day": "res://assets/audio/ambience/ferry_day.wav",
            "ambience.refugee_shelter_evening": "res://assets/audio/ambience/refugee_shelter_evening.wav",
            "ambience.ritual_storehouse_rain": "res://assets/audio/ambience/ritual_storehouse_rain.wav",
            "ambience.rain_night": "res://assets/audio/ambience/rain_night.wav",
            "music.old_ferry_morning": "res://assets/audio/music/music_old_ferry_morning.wav",
            "music.name_and_registry": "res://assets/audio/music/music_name_and_registry.wav",
            "music.ferry_day_news": "res://assets/audio/music/music_ferry_day_news.wav",
            "music.refugees_evening": "res://assets/audio/music/music_refugees_evening.wav",
            "music.cracked_bell_memory": "res://assets/audio/music/music_cracked_bell_memory.wav",
            "music.cart_crash_pressure": "res://assets/audio/music/music_cart_crash_pressure.wav",
            "sfx.ui_confirm": "res://assets/audio/sfx/ui_confirm.wav",
            "sfx.footstep_dry_01": "res://assets/audio/sfx/footstep_dry_01.wav",
            "sfx.footstep_dry_02": "res://assets/audio/sfx/footstep_dry_02.wav",
            "sfx.footstep_dry_03": "res://assets/audio/sfx/footstep_dry_03.wav",
            "sfx.footstep_dry_04": "res://assets/audio/sfx/footstep_dry_04.wav",
            "sfx.footstep_dry_05": "res://assets/audio/sfx/footstep_dry_05.wav",
            "sfx.footstep_dry_06": "res://assets/audio/sfx/footstep_dry_06.wav",
            "sfx.basin_water": "res://assets/audio/sfx/basin_water.wav",
            "sfx.cable_creak": "res://assets/audio/sfx/wood_cable_creak_01.wav",
            "sfx.boat_hull": "res://assets/audio/sfx/boat_hull_creak_01.wav",
            "sfx.tablet_write": "res://assets/audio/sfx/wood_tablet_write_01.wav",
            "sfx.brush_lift": "res://assets/audio/sfx/brush_lift.wav",
            "sfx.firewood_drop": "res://assets/audio/sfx/firewood_drop_01.wav",
            "sfx.bowl_place": "res://assets/audio/sfx/bowl_place_01.wav",
            "sfx.boat_dock": "res://assets/audio/sfx/boat_dock_impact.wav",
            "sfx.name_memory": "res://assets/audio/sfx/name_memory_water.wav",
            "sfx.cloth_rustle": "res://assets/audio/sfx/cloth_rustle_01.wav",
            "sfx.grain_last_scatter": "res://assets/audio/sfx/grain_last_scatter.wav",
            "sfx.liuniang_old_song": "res://assets/audio/sfx/liuniang_old_song_hum.wav",
            "sfx.shelter_fire": "res://assets/audio/sfx/shelter_fire_crackle.wav",
            "sfx.bell_body": "res://assets/audio/sfx/bell_body.wav",
            "sfx.bell_crack": "res://assets/audio/sfx/bell_crack.wav",
            "sfx.bell_underwater": "res://assets/audio/sfx/bell_underwater.wav",
            "sfx.bell_reverse_tail": "res://assets/audio/sfx/bell_reverse_tail.wav",
            "sfx.bell_memory_mix": "res://assets/audio/sfx/bell_memory_mix.wav",
            "sfx.cart_wheel_break": "res://assets/audio/sfx/cart_wheel_break.wav",
            "sfx.cart_impact_mud": "res://assets/audio/sfx/cart_impact_mud.wav",
            "sfx.horse_panic": "res://assets/audio/sfx/horse_panic.wav",
            "sfx.water_bucket_drag": "res://assets/audio/sfx/water_bucket_drag.wav",
            "sfx.tablet_splash": "res://assets/audio/sfx/wood_tablet_splash_01.wav",
            "sfx.wet_ink_spread": "res://assets/audio/sfx/wet_ink_spread.wav",
            "sfx.child_cry_pressure": "res://assets/audio/sfx/child_cry_pressure_loop.wav",
            "sfx.crowd_call_names": "res://assets/audio/sfx/crowd_call_names_loop.wav"
        },
    }
    (PROJECT_ROOT / "content" / "prologue" / "asset_manifest.json").write_text(
        json.dumps(content_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    provenance_lines = [
        "# P0/P2/P3/P4/P5/P6-A Generated Asset Provenance",
        "",
        f"- Generator version: `{GENERATOR_VERSION}`",
        f"- Seed: `{args.seed}`",
        f"- Generated at: `{created_at}`",
        "- Runtime source type: `procedural_generated`",
        "- Image concept-reference source type: `ai_generated_reference`",
        "- License: `project_owned`",
        "- Network media used: no",
        "",
        "Runtime visual assets were built from SVG primitives generated by repository scripts.",
        "Files ending in `_ai_reference.png` were generated with the built-in image tool and are review references only; runtime scenes do not depend on them.",
        "All WAV files were synthesized with Python standard-library math, random, array, and wave modules.",
        "The system-font resource stores fallback family names only; no commercial font file is copied into the repository.",
        "",
        "## Assets",
        "",
        "| Path | Generator | SHA-256 |",
        "|---|---|---|",
    ]
    for asset in assets:
        provenance_lines.append(
            f"| `{asset['path']}` | `{asset['generator_script']}` | `{asset['sha256'][:16]}…` |"
        )
    (PROJECT_ROOT / "assets" / "ASSET_PROVENANCE.md").write_text(
        "\n".join(provenance_lines) + "\n",
        encoding="utf-8",
    )
    print(f"[manifest] {len(assets)} generated assets indexed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
