"""Validate P0/P2/P3/P4/P5/P6-A generated art, manifests, character layers, and references."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from asset_tools_common import PROJECT_ROOT


P2_CHARACTERS = (
    "mother",
    "xinheng",
    "hean",
    "boat_owner",
    "ferry_worker",
    "ferry_woman",
)
P2_CHARACTER_LAYERS = ("shadow", "body", "head", "front_arm", "held_prop", "composite")
P3_CHARACTERS = (
    "hanning",
    "hanning_mother",
    "liuniang",
    "refugee_old",
    "refugee_mother",
    "refugee_man",
)
P6A_CHARACTERS = ("mother", "xinheng")

EXPECTED_ART = (
    "assets/characters/player/p0/player_shadow.svg",
    "assets/characters/player/p0/player_body.svg",
    "assets/characters/player/p0/player_head.svg",
    "assets/characters/player/p0/player_front_arm_tablet.svg",
    "assets/characters/player/p0/player_composite.svg",
    "assets/environments/old_ferry/p0/old_ferry_far.svg",
    "assets/environments/old_ferry/p0/old_ferry_mid.svg",
    "assets/environments/old_ferry/p0/old_ferry_near.svg",
    "assets/ui/p0/title_seal.svg",
    "assets/ui/p0/button_frame.svg",
    "assets/ui/p0/subtitle_panel.svg",
    "assets/fx/p0/fog_front.svg",
    "art/reference/generated_character_lineup.svg",
    "art/reference/generated_scene_color_script.svg",
) + tuple(
    f"assets/characters/{character}/p2/{character}_{layer}.svg"
    for character in P2_CHARACTERS
    for layer in P2_CHARACTER_LAYERS
) + (
    "assets/environments/old_ferry/p2/morning_far.svg",
    "assets/environments/old_ferry/p2/morning_mid.svg",
    "assets/environments/old_ferry/p2/morning_near.svg",
    "assets/environments/old_ferry/p2/day_far.svg",
    "assets/environments/old_ferry/p2/day_mid.svg",
    "assets/environments/old_ferry/p2/day_near.svg",
    "assets/props/p2/wood_boat.svg",
    "assets/props/p2/wood_cable.svg",
    "assets/props/p2/merchant_boat.svg",
    "assets/props/p2/xinheng_desk.svg",
    "assets/props/p2/grain_bag.svg",
    "assets/props/p2/pen_box.svg",
    "assets/props/p2/porridge_bowl.svg",
    "assets/fx/p2/fog_front.svg",
    "assets/fx/p2/water_shimmer.svg",
    "assets/fx/p2/name_memory.svg",
    "assets/ui/p2/name_input_panel.svg",
    "assets/ui/p2/objective_panel.svg",
    "art/reference/p2_old_ferry_morning_ai_reference.png",
    "art/reference/p2_character_lineup_ai_reference.png",
) + tuple(
    f"assets/characters/{character}/p3/{character}_{layer}.svg"
    for character in P3_CHARACTERS
    for layer in P2_CHARACTER_LAYERS
) + (
    "assets/environments/old_ferry/p3/shelter_evening_far.svg",
    "assets/environments/old_ferry/p3/shelter_evening_mid.svg",
    "assets/environments/old_ferry/p3/shelter_evening_near.svg",
    "assets/environments/old_ferry/p3/shelter_night_far.svg",
    "assets/environments/old_ferry/p3/shelter_night_mid.svg",
    "assets/environments/old_ferry/p3/shelter_night_near.svg",
    "assets/environments/ritual_storehouse/p3/storehouse_far.svg",
    "assets/environments/ritual_storehouse/p3/storehouse_mid.svg",
    "assets/environments/ritual_storehouse/p3/storehouse_near.svg",
    "assets/props/p3/broken_ding.svg",
    "assets/props/p3/chipped_gui.svg",
    "assets/props/p3/damaged_qing.svg",
    "assets/props/p3/cracked_bell.svg",
    "assets/props/p3/refugee_registry.svg",
    "assets/props/p3/shelter_stove.svg",
    "assets/fx/p3/rain.svg",
    "assets/fx/p3/memory/water_mask.svg",
    "assets/fx/p3/memory/city_fire.svg",
    "assets/fx/p3/memory/broken_rituals.svg",
    "assets/fx/p3/memory/scraped_registry.svg",
    "assets/fx/p3/memory/wet_hand.svg",
    "assets/fx/p3/memory/bell_sinking.svg",
    "art/reference/generated_p3_refugee_lineup.svg",
    "art/reference/generated_p3_scene_color_script.svg",
    "art/reference/p3_refugee_shelter_ai_reference.png",
    "art/reference/p3_ritual_storehouse_ai_reference.png",
) + (
    "assets/environments/old_ferry/p4/crash_rain_far.svg",
    "assets/environments/old_ferry/p4/crash_rain_mid.svg",
    "assets/environments/old_ferry/p4/crash_rain_near.svg",
    "assets/props/p4/overturned_cart.svg",
    "assets/props/p4/trapped_child.svg",
    "assets/props/p4/wet_tablets.svg",
    "assets/props/p4/separated_crowd.svg",
    "assets/props/p4/horse_shadow.svg",
    "assets/props/p4/hot_water_bucket.svg",
    "assets/props/p4/wet_ink_spread.svg",
    "assets/fx/p4/rain_heavy.svg",
    "art/reference/generated_p4_crash_scene.svg",
    "art/reference/generated_p5_character_lineup.svg",
    "art/reference/generated_p5_animation_action_sheet.svg",
    "art/reference/generated_p5_scene_color_script.svg",
    "art/reference/generated_p5_ui_board.svg",
) + (
    "assets/characters/player/p6a/player_shadow.svg",
    "assets/characters/player/p6a/player_body.svg",
    "assets/characters/player/p6a/player_head.svg",
    "assets/characters/player/p6a/player_front_arm_tablet.svg",
    "assets/characters/player/p6a/player_composite.svg",
) + tuple(
    f"assets/characters/{character}/p6a/{character}_{layer}.svg"
    for character in P6A_CHARACTERS
    for layer in P2_CHARACTER_LAYERS
) + (
    "assets/environments/old_ferry/p6a/morning_far.svg",
    "assets/environments/old_ferry/p6a/morning_mid.svg",
    "assets/environments/old_ferry/p6a/morning_near.svg",
    "assets/props/p6a/wood_boat.svg",
    "assets/props/p6a/wood_cable.svg",
    "assets/props/p6a/grain_bag.svg",
    "assets/props/p6a/pen_box.svg",
    "assets/props/p6a/xinheng_desk.svg",
    "art/reference/generated_p6a_old_ferry_visual_sheet.svg",
    "art/reference/generated_p6a_character_sheet.svg",
)

BANNED_FINAL_NAMES = ("placeholder", "dummy", "temp")
RESOURCE_PATTERN = re.compile(r'path="res://([^"]+)"')


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    for relative in EXPECTED_ART:
        path = PROJECT_ROOT / relative
        if not path.is_file():
            failures.append(f"missing required generated art: {relative}")
            continue
        if path.stat().st_size < 180:
            failures.append(f"generated art is unexpectedly small: {relative}")
        if path.suffix == ".svg":
            try:
                root = ET.parse(path).getroot()
                if "viewBox" not in root.attrib:
                    failures.append(f"SVG has no viewBox: {relative}")
            except ET.ParseError as error:
                failures.append(f"invalid SVG {relative}: {error}")

    manifest_path = PROJECT_ROOT / "assets" / "generated_asset_manifest.json"
    if not manifest_path.is_file():
        failures.append("missing assets/generated_asset_manifest.json")
        manifest = {"assets": []}
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            failures.append(f"invalid generated manifest: {error}")
            manifest = {"assets": []}

    for entry in manifest.get("assets", []):
        relative = entry.get("path", "")
        lowered = Path(relative).name.lower()
        if any(term in lowered for term in BANNED_FINAL_NAMES):
            failures.append(f"banned final asset name: {relative}")
        path = PROJECT_ROOT / relative
        if not path.is_file():
            failures.append(f"manifest path does not exist: {relative}")
            continue
        if entry.get("sha256") != file_sha256(path):
            failures.append(f"manifest hash mismatch: {relative}")

    for scene_path in sorted((PROJECT_ROOT / "scenes").rglob("*.tscn")):
        text = scene_path.read_text(encoding="utf-8")
        for relative in RESOURCE_PATTERN.findall(text):
            if not (PROJECT_ROOT / relative).exists():
                failures.append(
                    f"{scene_path.relative_to(PROJECT_ROOT).as_posix()} references missing res://{relative}"
                )

    content_manifest_path = PROJECT_ROOT / "content" / "prologue" / "asset_manifest.json"
    if content_manifest_path.is_file():
        content_manifest = json.loads(content_manifest_path.read_text(encoding="utf-8"))
        runtime_assets = content_manifest.get("runtime_assets", {})
        for asset_id, resource_path in runtime_assets.items():
            if not isinstance(resource_path, str) or not resource_path.startswith("res://"):
                failures.append(f"invalid runtime asset alias: {asset_id}")
                continue
            if not (PROJECT_ROOT / resource_path.removeprefix("res://")).exists():
                failures.append(f"runtime asset alias is missing: {asset_id} -> {resource_path}")
    else:
        failures.append("missing content/prologue/asset_manifest.json")

    required_p2_scenes = (
        "scenes/prologue/SC01_Home_Morning.tscn",
        "scenes/prologue/SC02_Xinheng_Desk.tscn",
        "scenes/prologue/SC03_Ferry_Day.tscn",
    )
    for relative in required_p2_scenes:
        scene_path = PROJECT_ROOT / relative
        if not scene_path.is_file():
            failures.append(f"missing P2 scene: {relative}")
            continue
        scene_text = scene_path.read_text(encoding="utf-8")
        for required_node in ("WaterShimmer", "Actors", "Interactions", "SceneCamera"):
            if f'name="{required_node}"' not in scene_text:
                failures.append(f"{relative} is missing layered runtime node: {required_node}")

    required_p6a_refs = {
        "scenes/prologue/SC01_Home_Morning.tscn": (
            "assets/environments/old_ferry/p6a/morning_far.svg",
            "assets/props/p6a/wood_boat.svg",
            "assets/props/p6a/grain_bag.svg",
        ),
        "scenes/prologue/SC02_Xinheng_Desk.tscn": (
            "assets/environments/old_ferry/p6a/morning_far.svg",
            "assets/props/p6a/xinheng_desk.svg",
        ),
        "scenes/characters/Player.tscn": ("assets/characters/player/p6a/player_body.svg",),
        "scenes/characters/Mother.tscn": ("assets/characters/mother/p6a/mother_body.svg",),
        "scenes/characters/Xinheng.tscn": ("assets/characters/xinheng/p6a/xinheng_body.svg",),
    }
    for relative, required_paths in required_p6a_refs.items():
        scene_path = PROJECT_ROOT / relative
        if not scene_path.is_file():
            failures.append(f"missing P6-A scene/reference target: {relative}")
            continue
        scene_text = scene_path.read_text(encoding="utf-8")
        for required_path in required_paths:
            if required_path not in scene_text:
                failures.append(f"{relative} does not reference P6-A asset: {required_path}")

    required_p3_scenes = {
        "scenes/prologue/SC04_Refugee_Shelter.tscn": (
            "EveningFar",
            "NightFar",
            "RainBack",
            "Actors",
            "Interactions",
            "SceneCamera",
        ),
        "scenes/prologue/SC05_Ritual_Storehouse.tscn": (
            "BrokenDingVisual",
            "ChippedGuiVisual",
            "DamagedQingVisual",
            "cracked_bell",
            "bell_memory",
            "Interactions",
        ),
    }
    for relative, required_nodes in required_p3_scenes.items():
        scene_path = PROJECT_ROOT / relative
        if not scene_path.is_file():
            failures.append(f"missing P3 scene: {relative}")
            continue
        scene_text = scene_path.read_text(encoding="utf-8")
        for required_node in required_nodes:
            if f'name="{required_node}"' not in scene_text:
                failures.append(f"{relative} is missing P3 runtime node: {required_node}")

    required_p4_scenes = {
        "scenes/prologue/SC06_Cart_Crash_Rain.tscn": (
            "OverturnedCartVisual",
            "TrappedChildVisual",
            "WetTabletsVisual",
            "SeparatedCrowdVisual",
            "ChoicePressureController",
            "choice_child",
            "choice_records",
            "choice_crowd",
            "Interactions",
            "SceneCamera",
        ),
    }
    for relative, required_nodes in required_p4_scenes.items():
        scene_path = PROJECT_ROOT / relative
        if not scene_path.is_file():
            failures.append(f"missing P4 scene: {relative}")
            continue
        scene_text = scene_path.read_text(encoding="utf-8")
        for required_node in required_nodes:
            if f'name="{required_node}"' not in scene_text:
                failures.append(f"{relative} is missing P4 runtime node: {required_node}")

    required_p5_scenes = {
        "scenes/prologue/SC07_Prologue_End.tscn": (
            "TitleLabel",
            "SummaryLabel",
            "PriorityLabel",
            "ChapterTitleLabel",
            "DetailPanel",
            "ReturnTitleButton",
        ),
    }
    for relative, required_nodes in required_p5_scenes.items():
        scene_path = PROJECT_ROOT / relative
        if not scene_path.is_file():
            failures.append(f"missing P5 scene: {relative}")
            continue
        scene_text = scene_path.read_text(encoding="utf-8")
        for required_node in required_nodes:
            if f'name="{required_node}"' not in scene_text:
                failures.append(f"{relative} is missing P5 runtime node: {required_node}")

    timeline_path = PROJECT_ROOT / "content" / "prologue" / "timeline.json"
    if timeline_path.is_file():
        timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
        memory_duration = float(
            timeline.get("stages", {})
            .get("SC05_Ritual_Storehouse", {})
            .get("memory_duration_seconds", 0.0)
        )
        if not 20.0 <= memory_duration <= 35.0:
            failures.append(
                f"P3 cracked-bell memory duration must be 20–35 seconds, got {memory_duration}"
            )

    json_paths = list((PROJECT_ROOT / "content").rglob("*.json"))
    json_paths.extend((PROJECT_ROOT / "tests" / "fixtures").rglob("*.json"))
    for json_path in sorted(json_paths):
        try:
            json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            failures.append(
                f"invalid JSON {json_path.relative_to(PROJECT_ROOT).as_posix()}: {error}"
            )

    if failures:
        for failure in failures:
            print(f"[asset validation] FAIL: {failure}", file=sys.stderr)
        return 1

    print(
        f"[asset validation] PASS: {len(EXPECTED_ART)} required art assets, "
        f"{len(manifest.get('assets', []))} manifest entries, all scene references."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
