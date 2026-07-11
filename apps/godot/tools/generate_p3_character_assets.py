"""Generate the layered P3 refugee cast and a review lineup."""

from __future__ import annotations

from asset_tools_common import base_parser, svg_document, write_text
from generate_character_assets import CANVAS_DEFS, p2_character_layers


P3_CHARACTER_SPECS = {
    "hanning": {
        "height": 273,
        "shoulder": 43,
        "cloth": "#4d5957",
        "cloth_dark": "#333c3b",
        "accent": "#756b57",
        "skin": "#bd9875",
        "hair": "#272522",
        "stance": -5,
        "prop": "water_jar",
    },
    "hanning_mother": {
        "height": 289,
        "shoulder": 53,
        "cloth": "#665b59",
        "cloth_dark": "#403a3a",
        "accent": "#7d7468",
        "skin": "#b48c6b",
        "hair": "#3d3732",
        "stance": 5,
        "prop": "water_jar",
    },
    "liuniang": {
        "height": 294,
        "shoulder": 52,
        "cloth": "#496866",
        "cloth_dark": "#344b4b",
        "accent": "#8f5147",
        "skin": "#c19a77",
        "hair": "#2e2927",
        "stance": 2,
        "prop": "water_jar",
    },
    "refugee_old": {
        "height": 283,
        "shoulder": 48,
        "cloth": "#5f5b52",
        "cloth_dark": "#3d3b36",
        "accent": "#74674f",
        "skin": "#aa8263",
        "hair": "#777169",
        "stance": -10,
        "prop": "water_jar",
    },
    "refugee_mother": {
        "height": 288,
        "shoulder": 55,
        "cloth": "#59615d",
        "cloth_dark": "#3b423f",
        "accent": "#71564a",
        "skin": "#bb9270",
        "hair": "#332e2a",
        "stance": 4,
        "prop": "water_jar",
    },
    "refugee_man": {
        "height": 309,
        "shoulder": 69,
        "cloth": "#555c59",
        "cloth_dark": "#373d3b",
        "accent": "#765e42",
        "skin": "#ad805f",
        "hair": "#292724",
        "stance": 8,
        "prop": "water_jar",
    },
}


def held_prop(character_id: str) -> str:
    if character_id == "hanning":
        return """
<g id="held_prop" stroke="#302b27" stroke-linejoin="round">
  <path d="M199 139 Q225 165 211 244 L181 246 Q188 190 174 154 Z"
        fill="#3e4948" stroke-width="4"/>
  <rect x="184" y="172" width="31" height="81" rx="3"
        fill="#7d6040" stroke-width="3"/>
  <path d="M190 188 h18 m-18 13 h18 m-18 13 h18" stroke="#3d3027" stroke-width="2"/>
  <path d="M179 178 Q207 185 219 170" fill="none" stroke="#756b57" stroke-width="5"/>
</g>
"""
    if character_id == "hanning_mother":
        return """
<g id="held_prop" stroke="#322c29" stroke-linecap="round">
  <path d="M96 171 Q129 203 166 210" fill="none" stroke="#665b59" stroke-width="23"/>
  <path d="M165 210 Q181 215 193 204" fill="none" stroke="#b48c6b" stroke-width="16"/>
  <path d="M91 166 Q128 194 167 202" fill="none" stroke="#7d7468" stroke-width="4"/>
</g>
"""
    if character_id == "liuniang":
        return """
<g id="held_prop" stroke="#342c27" stroke-linejoin="round">
  <rect x="79" y="247" width="188" height="74" rx="7"
        fill="#554337" stroke-width="5"/>
  <rect x="91" y="257" width="164" height="52" rx="4"
        fill="#6e5541" stroke="#947052" stroke-width="3"/>
  <path d="M132 247 q42 -32 84 0" fill="none" stroke="#40332b" stroke-width="7"/>
  <path d="M118 278 h119" stroke="#9c7956" stroke-opacity=".45" stroke-width="3"/>
  <path d="M190 61 l34 -15" stroke="#a98855" stroke-width="5" stroke-linecap="round"/>
  <circle cx="225" cy="45" r="6" fill="#8f5147"/>
</g>
"""
    if character_id == "refugee_old":
        return """
<g id="held_prop" stroke="#3c3027" stroke-linecap="round">
  <path d="M95 128 Q80 224 77 338" fill="none" stroke="#71583c" stroke-width="11"/>
  <path d="M88 132 q18 -28 31 -4" fill="none" stroke="#9b7b55" stroke-width="4"/>
</g>
"""
    if character_id == "refugee_mother":
        return """
<g id="held_prop" stroke="#312b27" stroke-linejoin="round">
  <path d="M182 176 Q238 165 259 224 Q251 287 191 288 Q161 244 182 176 Z"
        fill="#68574b" stroke-width="4"/>
  <circle cx="220" cy="180" r="27" fill="#bd9875" stroke-width="3"/>
  <path d="M194 176 q25 -31 50 0" fill="#332e2a"/>
  <path d="M180 221 q40 27 76 1" fill="none" stroke="#8b6a51" stroke-width="7"/>
</g>
"""
    return """
<g id="held_prop" stroke="#342b25" stroke-linejoin="round">
  <path d="M178 117 Q242 93 274 144 L267 275 Q217 306 165 274 Z"
        fill="#847258" stroke-width="5"/>
  <path d="M179 128 q48 19 93 1" fill="none" stroke="#ac9875" stroke-width="7"/>
  <path d="M177 174 q47 19 93 1 m-96 43 q49 19 96 0"
        fill="none" stroke="#4e4438" stroke-opacity=".58" stroke-width="4"/>
  <path d="M185 111 q38 31 79 2" fill="none" stroke="#4e3c2d" stroke-width="9"/>
</g>
"""


def main() -> int:
    args = base_parser("Generate layered P3 refugee character assets.").parse_args()
    lineup = []
    for index, (character_id, spec) in enumerate(P3_CHARACTER_SPECS.items()):
        layers = p2_character_layers(character_id, spec)
        layers["head"] = (
            layers["head"]
            .replace("q8 -5 16 0", "q8 1 16 0")
            .replace("q9 5 19 0", "q9 -2 19 0")
        )
        layers["held_prop"] = held_prop(character_id)
        base = f"assets/characters/{character_id}/p3"
        for layer_name, content in layers.items():
            write_text(
                f"{base}/{character_id}_{layer_name}.svg",
                svg_document(320, 360, content, CANVAS_DEFS),
                args.force,
            )
        composite = "".join(layers.values())
        write_text(
            f"{base}/{character_id}_composite.svg",
            svg_document(320, 360, composite, CANVAS_DEFS),
            args.force,
        )
        lineup.append(
            f'<g transform="translate({38 + index * 214} 126) scale(.60)">'
            f"{composite}</g>"
        )

    review = f"""
<rect width="1320" height="570" fill="#202b2d"/>
<rect x="20" y="20" width="1280" height="530" rx="10"
      fill="#d8cfba" stroke="#302c27" stroke-width="3"/>
{''.join(lineup)}
<text x="48" y="72" font-family="Microsoft YaHei, sans-serif"
      font-size="29" fill="#292724">序章 P3 流民人物：韩宁 / 韩宁母亲 / 柳娘 / 老者 / 抱病儿妇人 / 湿粮汉子</text>
<text x="48" y="525" font-family="Microsoft YaHei, sans-serif"
      font-size="18" fill="#54483e">各自持物与姿态分层 · seed {args.seed} · generator p3.0</text>
"""
    write_text(
        "art/reference/generated_p3_refugee_lineup.svg",
        svg_document(1320, 570, review, CANVAS_DEFS),
        args.force,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
