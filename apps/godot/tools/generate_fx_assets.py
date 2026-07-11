"""Generate translucent river, fog, and name-memory overlays."""

from __future__ import annotations

import random

from asset_tools_common import base_parser, svg_document, write_text


def main() -> int:
    args = base_parser("Generate P0/P2 procedural FX SVG assets.").parse_args()
    rng = random.Random(args.seed + 71)
    fog_shapes = []
    for _ in range(34):
        x = rng.randint(-180, 2020)
        y = rng.randint(55, 610)
        rx = rng.randint(110, 360)
        ry = rng.randint(18, 72)
        opacity = rng.uniform(0.025, 0.1)
        fog_shapes.append(
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
            f'fill="#e8e1d2" fill-opacity="{opacity:.3f}"/>'
        )
    fog = svg_document(
        1920,
        720,
        f"""
<g id="fog_front">
{''.join(fog_shapes)}
<path d="M-80 530 Q260 450 590 535 T1240 520 T1980 515" fill="none" stroke="#e8e1d2" stroke-opacity=".08" stroke-width="70"/>
</g>
""",
    )
    write_text("assets/fx/p0/fog_front.svg", fog, args.force)
    p2_fog = svg_document(
        2200,
        720,
        fog.replace('viewBox="0 0 1920 720"', 'viewBox="0 0 2200 720"')
        if False
        else f"""
<g id="fog_front">
{''.join(fog_shapes)}
<path d="M-100 520 Q300 425 680 530 T1450 516 T2300 520"
      fill="none" stroke="#e8e1d2" stroke-opacity=".1" stroke-width="82"/>
</g>
""",
    )
    water_lines = []
    for _ in range(52):
        x = rng.randint(-80, 2200)
        y = rng.randint(350, 558)
        length = rng.randint(48, 210)
        water_lines.append(
            f'<path d="M{x} {y} q{length//2} {rng.randint(-4,4)} {length} 0" '
            f'fill="none" stroke="#e8e1d2" stroke-opacity="{rng.uniform(.05,.18):.3f}" '
            f'stroke-width="{rng.randint(1,3)}"/>'
        )
    water = svg_document(2200, 720, f'<g id="water_shimmer">{"".join(water_lines)}</g>')
    name_memory = svg_document(
        1280,
        720,
        """
<rect width="1280" height="720" fill="#10191d" fill-opacity=".82"/>
<path d="M105 530 Q313 420 530 505 T940 498 T1320 474"
      fill="none" stroke="#68888b" stroke-opacity=".35" stroke-width="94"/>
<path d="M102 168 L1170 168 L1104 468 L177 468 Z"
      fill="#40382f" stroke="#17191a" stroke-width="14"/>
<path d="M220 205 H1004 M198 258 H1030 M182 319 H1047"
      stroke="#806a4b" stroke-width="8" stroke-opacity=".7"/>
<g transform="translate(808 182) rotate(-13)">
  <path d="M47 15 Q84 3 108 39 L146 194 Q119 231 74 211 L20 78 Q14 31 47 15 Z"
        fill="#92735b" stroke="#302724" stroke-width="8"/>
  <path d="M45 76 L4 2 M66 68 L39 -12 M87 70 L76 -15 M106 83 L110 -4"
        stroke="#92735b" stroke-width="24" stroke-linecap="round"/>
</g>
<g fill="#d7d2c4" fill-opacity=".42">
  <ellipse cx="330" cy="559" rx="185" ry="22"/><ellipse cx="760" cy="587" rx="245" ry="27"/>
</g>
""",
    )
    write_text("assets/fx/p2/fog_front.svg", p2_fog, args.force)
    write_text("assets/fx/p2/water_shimmer.svg", water, args.force)
    write_text("assets/fx/p2/name_memory.svg", name_memory, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
