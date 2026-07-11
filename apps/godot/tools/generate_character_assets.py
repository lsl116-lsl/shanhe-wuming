"""Generate layered P0/P2 characters and a shared review lineup."""

from __future__ import annotations

from asset_tools_common import base_parser, svg_document, write_text


CANVAS_DEFS = """
<linearGradient id="cloth" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#788480"/>
  <stop offset="1" stop-color="#485b60"/>
</linearGradient>
<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#d2b38b"/>
  <stop offset="1" stop-color="#b68d67"/>
</linearGradient>
<pattern id="papergrain" width="13" height="13" patternUnits="userSpaceOnUse">
  <path d="M1 3 L12 1 M3 10 L11 8" stroke="#e8e1d2" stroke-opacity=".08" stroke-width=".7"/>
</pattern>
"""

SHADOW = """
<g id="shadow">
  <ellipse cx="128" cy="293" rx="53" ry="12" fill="#172326" fill-opacity=".32"/>
  <ellipse cx="128" cy="290" rx="36" ry="6" fill="#26363a" fill-opacity=".28"/>
</g>
"""

BODY = """
<g id="body_back" stroke="#292724" stroke-width="3" stroke-linejoin="round">
  <path d="M101 164 Q86 181 84 224 L79 277 Q91 288 108 281 L116 218 Z" fill="#53666a"/>
  <path d="M155 164 Q173 181 176 222 L182 273 Q168 286 151 278 L141 216 Z" fill="#45575b"/>
</g>
<g id="legs" stroke="#292724" stroke-width="3" stroke-linejoin="round">
  <path d="M102 222 L126 222 L121 284 Q111 296 96 286 Z" fill="#5e625d"/>
  <path d="M128 222 L153 222 L162 285 Q146 296 136 284 Z" fill="#535954"/>
  <path d="M93 283 Q108 278 123 285 L122 295 L91 295 Z" fill="#332f2a"/>
  <path d="M136 284 Q151 279 164 286 L166 295 L135 295 Z" fill="#332f2a"/>
</g>
<g id="torso" stroke="#292724" stroke-width="3" stroke-linejoin="round">
  <path d="M99 147 Q128 132 157 148 L162 229 Q130 244 94 229 Z" fill="url(#cloth)"/>
  <path d="M99 147 Q126 161 157 148" fill="none"/>
  <path d="M112 151 L145 227" fill="none" stroke="#a8b0aa" stroke-opacity=".45" stroke-width="2"/>
  <path d="M95 207 Q128 215 162 205" fill="none" stroke="#6b513d" stroke-width="7"/>
  <path d="M95 207 Q128 215 162 205" fill="none" stroke="#b09a74" stroke-width="2"/>
  <path d="M98 149 L158 149 L161 229 L94 229 Z" fill="url(#papergrain)" stroke="none"/>
</g>
<g id="back_arm" stroke="#292724" stroke-width="3" stroke-linecap="round">
  <path d="M99 158 Q79 178 88 214 Q95 228 105 214 L112 174 Z" fill="#627075"/>
  <path d="M90 213 Q91 229 103 230 Q114 222 104 211 Z" fill="url(#skin)"/>
</g>
"""

HEAD = """
<g id="head">
  <path d="M100 91 Q99 57 128 49 Q163 53 160 94 L154 127 Q143 143 126 143 Q107 139 101 123 Z"
        fill="url(#skin)" stroke="#292724" stroke-width="3"/>
  <path d="M99 91 Q92 66 113 49 Q139 29 162 56 Q173 69 159 99
           Q147 76 127 73 Q114 89 99 91 Z" fill="#292724"/>
  <path d="M110 54 Q128 35 151 48" fill="none" stroke="#423b34" stroke-width="6" stroke-linecap="round"/>
  <path d="M113 102 Q119 103 125 102 M139 102 Q145 103 151 102" fill="none" stroke="#292724" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M126 121 Q136 120 144 120" fill="none" stroke="#6b453b" stroke-width="2" stroke-linecap="round"/>
  <path d="M124 139 L127 150 L143 143 L145 131" fill="#c39f78" stroke="#292724" stroke-width="3"/>
  <path d="M160 66 Q178 67 178 82 Q172 94 158 91" fill="#2f2a26" stroke="#292724" stroke-width="3"/>
  <path d="M164 69 Q178 62 183 70" fill="none" stroke="#8a8174" stroke-width="4" stroke-linecap="round"/>
</g>
"""

FRONT_ARM_TABLET = """
<g id="held_prop" stroke="#292724" stroke-linejoin="round">
  <g transform="rotate(-7 174 194)">
    <rect x="151" y="151" width="46" height="91" rx="4" fill="#765b3d" stroke-width="3"/>
    <rect x="158" y="158" width="32" height="77" rx="2" fill="#9a7b51" stroke="#4a3828" stroke-width="1.5"/>
    <path d="M164 171 L184 168 M163 184 L185 181 M162 197 L182 194 M161 211 L180 208"
          stroke="#4a3828" stroke-width="2" stroke-linecap="round"/>
  </g>
</g>
<g id="front_arm" stroke="#292724" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
  <path d="M153 159 Q171 176 166 204 L154 215 Q141 204 142 177 Z" fill="#596b6f"/>
  <path d="M156 205 Q168 203 174 215 Q171 228 159 226 Q149 218 156 205 Z" fill="url(#skin)"/>
  <path d="M160 216 Q169 219 174 214" fill="none" stroke="#4f7770" stroke-width="3"/>
</g>
<g id="ink_marks" fill="#2a3436" fill-opacity=".7">
  <circle cx="162" cy="216" r="2.3"/><circle cx="169" cy="218" r="1.4"/>
</g>
"""

P2_CHARACTER_SPECS = {
    "mother": {
        "height": 300,
        "shoulder": 58,
        "cloth": "#77746b",
        "cloth_dark": "#4f4b45",
        "accent": "#83969a",
        "skin": "#c6a178",
        "hair": "#302b28",
        "stance": 0,
        "prop": "basin",
    },
    "xinheng": {
        "height": 292,
        "shoulder": 48,
        "cloth": "#545552",
        "cloth_dark": "#383a38",
        "accent": "#3f5958",
        "skin": "#b7936f",
        "hair": "#6d675f",
        "stance": -7,
        "prop": "tablet_brush",
    },
    "hean": {
        "height": 258,
        "shoulder": 49,
        "cloth": "#945848",
        "cloth_dark": "#5b4138",
        "accent": "#b19b73",
        "skin": "#cfa87d",
        "hair": "#352c29",
        "stance": 8,
        "prop": "firewood_bowl",
    },
    "boat_owner": {
        "height": 310,
        "shoulder": 66,
        "cloth": "#465e62",
        "cloth_dark": "#354348",
        "accent": "#8c7351",
        "skin": "#b88863",
        "hair": "#2d2926",
        "stance": 5,
        "prop": "rope_tally",
    },
    "ferry_worker": {
        "height": 306,
        "shoulder": 74,
        "cloth": "#68645d",
        "cloth_dark": "#48443e",
        "accent": "#776047",
        "skin": "#b58a64",
        "hair": "#312c28",
        "stance": -4,
        "prop": "shoulder_pole",
    },
    "ferry_woman": {
        "height": 294,
        "shoulder": 55,
        "cloth": "#5f6c67",
        "cloth_dark": "#434a47",
        "accent": "#735a47",
        "skin": "#c19872",
        "hair": "#2f2927",
        "stance": 4,
        "prop": "water_jar",
    },
}


def p2_character_layers(character_id: str, spec: dict[str, object]) -> dict[str, str]:
    height = int(spec["height"])
    shoulder = int(spec["shoulder"])
    cloth = str(spec["cloth"])
    cloth_dark = str(spec["cloth_dark"])
    accent = str(spec["accent"])
    skin = str(spec["skin"])
    hair = str(spec["hair"])
    stance = int(spec["stance"])
    head_y = 330 - height
    neck_y = head_y + 78
    hip_y = 248 if height > 280 else 258
    foot_y = 334
    center = 160 + stance
    left = center - shoulder
    right = center + shoulder

    shadow = f"""
<g id="shadow">
  <ellipse cx="{center}" cy="338" rx="{shoulder + 20}" ry="10" fill="#182326" fill-opacity=".34"/>
  <ellipse cx="{center}" cy="336" rx="{shoulder - 4}" ry="5" fill="#2a3637" fill-opacity=".2"/>
</g>
"""
    body = f"""
<g id="body_back" stroke="#2e2925" stroke-width="3" stroke-linejoin="round">
  <path d="M{left+10} {neck_y+16} Q{left-20} {neck_y+48} {left-13} {hip_y+3}
           Q{left+1} {hip_y+16} {left+17} {hip_y-1} L{center-18} {neck_y+28} Z"
        fill="{cloth_dark}"/>
  <path d="M{right-8} {neck_y+16} Q{right+24} {neck_y+49} {right+17} {hip_y+4}
           Q{right+2} {hip_y+17} {right-13} {hip_y-2} L{center+18} {neck_y+28} Z"
        fill="{cloth_dark}"/>
</g>
<g id="legs" stroke="#2e2925" stroke-width="3" stroke-linejoin="round">
  <path d="M{center-42} {hip_y-4} L{center-3} {hip_y-4} L{center-11} {foot_y-7}
           Q{center-31} {foot_y+3} {center-49} {foot_y-7} Z" fill="{cloth_dark}"/>
  <path d="M{center-2} {hip_y-4} L{center+42} {hip_y-4} L{center+49} {foot_y-7}
           Q{center+28} {foot_y+3} {center+9} {foot_y-7} Z" fill="{cloth_dark}"/>
  <path d="M{center-53} {foot_y-9} Q{center-31} {foot_y-16} {center-8} {foot_y-8}
           L{center-7} {foot_y+2} L{center-56} {foot_y+2} Z" fill="#332f2a"/>
  <path d="M{center+7} {foot_y-8} Q{center+31} {foot_y-16} {center+54} {foot_y-7}
           L{center+57} {foot_y+2} L{center+7} {foot_y+2} Z" fill="#332f2a"/>
</g>
<g id="torso" stroke="#2e2925" stroke-width="3" stroke-linejoin="round">
  <path d="M{left} {neck_y+7} Q{center} {neck_y-8} {right} {neck_y+7}
           L{right-8} {hip_y} Q{center} {hip_y+18} {left+8} {hip_y} Z" fill="{cloth}"/>
  <path d="M{left+5} {neck_y+11} Q{center} {neck_y+31} {right-5} {neck_y+11}"
        fill="none" stroke="{accent}" stroke-width="5"/>
  <path d="M{left+6} {hip_y-25} Q{center} {hip_y-14} {right-6} {hip_y-25}"
        fill="none" stroke="{accent}" stroke-width="8"/>
  <path d="M{left+7} {neck_y+12} L{right-10} {hip_y-2}" fill="none"
        stroke="#e8e1d2" stroke-opacity=".2" stroke-width="2"/>
</g>
"""
    age_lines = (
        f'<path d="M{center-25} {head_y+42} q8 -5 16 0 M{center+9} {head_y+42} q8 -5 16 0" '
        'fill="none" stroke="#5d4a3c" stroke-width="2" stroke-linecap="round"/>'
    )
    beard = ""
    if character_id in {"xinheng", "boat_owner", "ferry_worker"}:
        beard_color = "#71685d" if character_id == "xinheng" else hair
        beard = (
            f'<path d="M{center-20} {head_y+68} Q{center} {head_y+105} {center+21} {head_y+68} '
            f'Q{center+12} {head_y+113} {center} {head_y+122} '
            f'Q{center-13} {head_y+112} {center-20} {head_y+68} Z" '
            f'fill="{beard_color}" fill-opacity=".82" stroke="#2e2925" stroke-width="2"/>'
        )
    hair_shape = (
        f'<path d="M{center-37} {head_y+36} Q{center-33} {head_y-6} {center} {head_y-9} '
        f'Q{center+37} {head_y-4} {center+40} {head_y+38} '
        f'Q{center+16} {head_y+16} {center-6} {head_y+19} '
        f'Q{center-22} {head_y+35} {center-37} {head_y+36} Z" fill="{hair}"/>'
    )
    if character_id == "hean":
        hair_shape += (
            f'<path d="M{center+18} {head_y-8} q18 -24 34 -4 q-7 18 -26 19" '
            f'fill="{hair}" stroke="#2e2925" stroke-width="3"/>'
            f'<path d="M{center+28} {head_y-4} l23 8" stroke="{accent}" stroke-width="5"/>'
        )
    head = f"""
<g id="head">
  <path d="M{center-36} {head_y+30} Q{center-35} {head_y+3} {center} {head_y}
           Q{center+37} {head_y+3} {center+38} {head_y+33}
           L{center+31} {head_y+68} Q{center} {head_y+89} {center-30} {head_y+68} Z"
        fill="{skin}" stroke="#2e2925" stroke-width="3"/>
  {hair_shape}
  {age_lines}
  <path d="M{center-9} {head_y+66} q9 5 19 0" fill="none" stroke="#6e493e"
        stroke-width="2" stroke-linecap="round"/>
  {beard}
  <path d="M{center-13} {head_y+78} L{center-10} {neck_y+6} L{center+15} {neck_y+6}
        L{center+16} {head_y+78}" fill="{skin}" stroke="#2e2925" stroke-width="3"/>
</g>
"""
    front_arm = f"""
<g id="front_arm" stroke="#2e2925" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
  <path d="M{right-7} {neck_y+20} Q{right+18} {neck_y+48} {right+3} {hip_y-8}
           L{right-17} {hip_y-2} Q{right-13} {neck_y+55} {right-30} {neck_y+32} Z"
        fill="{cloth}"/>
  <path d="M{right-15} {hip_y-7} q20 -9 31 7 q-2 20 -21 19 q-16 -8 -10 -26 Z"
        fill="{skin}"/>
</g>
"""
    prop_by_kind = {
        "basin": f"""
<g id="held_prop" stroke="#3c3028" stroke-width="3">
  <ellipse cx="{center+10}" cy="{hip_y+2}" rx="61" ry="18" fill="#9a7650"/>
  <path d="M{center-49} {hip_y+2} Q{center+10} {hip_y+62} {center+68} {hip_y+2}"
        fill="#71543d"/>
  <ellipse cx="{center+10}" cy="{hip_y}" rx="52" ry="12" fill="#8fa0a0" fill-opacity=".76"/>
</g>
""",
        "tablet_brush": f"""
<g id="held_prop" stroke="#3b3028" stroke-linejoin="round">
  <rect x="{center+12}" y="{neck_y+23}" width="40" height="101" rx="3"
        fill="#8b6844" stroke-width="3"/>
  <path d="M{center-22} {neck_y+18} L{center+18} {hip_y+8}" stroke="#4c3528" stroke-width="5"/>
  <path d="M{center-24} {neck_y+13} l7 17" stroke="#202b33" stroke-width="5"/>
</g>
""",
        "firewood_bowl": f"""
<g id="held_prop" stroke="#443429" stroke-linecap="round">
  <g transform="translate(-24 -6)">
    <path d="M{center+10} {neck_y+25} l92 -38 M{center+7} {neck_y+35} l98 -17
             M{center+13} {neck_y+45} l91 4 M{center+6} {neck_y+52} l84 24"
          stroke="#604831" stroke-width="8"/>
    <path d="M{center+29} {neck_y+8} q26 24 58 42" fill="none" stroke="#9a7a52" stroke-width="4"/>
  </g>
  <path d="M{center+3} {hip_y+5} q38 22 73 0 q-8 38 -37 39 q-29 -1 -36 -39 Z"
        fill="#8a6745" stroke-width="3"/>
  <path d="M{center+11} {hip_y+5} q29 11 57 0" fill="none" stroke="#d0b279" stroke-width="5"/>
</g>
""",
        "rope_tally": f"""
<g id="held_prop" stroke="#45362a" stroke-linecap="round" fill="none">
  <circle cx="{center+42}" cy="{neck_y+78}" r="35" stroke="#8b714f" stroke-width="9"/>
  <circle cx="{center+42}" cy="{neck_y+78}" r="22" stroke="#5e4b39" stroke-width="5"/>
  <rect x="{center-48}" y="{neck_y+38}" width="29" height="65" rx="3"
        fill="#8c6d46" stroke-width="3"/>
  <path d="M{center-42} {neck_y+51} l18 0 m-18 14 l18 0 m-18 14 l18 0"
        stroke="#473629" stroke-width="2"/>
</g>
""",
        "shoulder_pole": f"""
<g id="held_prop" stroke="#443529" stroke-linecap="round">
  <path d="M{center-89} {neck_y+15} Q{center} {neck_y+4} {center+100} {neck_y+20}"
        fill="none" stroke="#6e5438" stroke-width="10"/>
  <path d="M{center-71} {neck_y+18} v101 M{center+84} {neck_y+18} v100"
        fill="none" stroke="#836a4c" stroke-width="4"/>
  <path d="M{center-94} {hip_y+17} q24 -18 47 0 l-8 43 h-31 Z"
        fill="#70533a" stroke-width="3"/>
  <path d="M{center+62} {hip_y+17} q24 -18 47 0 l-8 43 h-31 Z"
        fill="#70533a" stroke-width="3"/>
</g>
""",
        "water_jar": f"""
<g id="held_prop" stroke="#42342a" stroke-width="3">
  <path d="M{center+17} {hip_y-3} q31 -18 58 0 l-8 17 q20 52 -21 70
           q-44 -14 -21 -70 Z" fill="#76634d"/>
  <path d="M{center+28} {hip_y+8} q20 8 38 0" fill="none" stroke="#aa916d" stroke-width="4"/>
</g>
""",
    }
    held_prop = prop_by_kind[str(spec["prop"])]
    return {
        "shadow": shadow,
        "body": body,
        "head": head,
        "front_arm": front_arm,
        "held_prop": held_prop,
    }


def layer(body: str) -> str:
    return svg_document(256, 320, body, CANVAS_DEFS)


def main() -> int:
    args = base_parser("Generate layered protagonist and P2 cast SVG assets.").parse_args()
    base = "assets/characters/player/p0"
    write_text(f"{base}/player_shadow.svg", layer(SHADOW), args.force)
    write_text(f"{base}/player_body.svg", layer(BODY), args.force)
    write_text(f"{base}/player_head.svg", layer(HEAD), args.force)
    write_text(f"{base}/player_front_arm_tablet.svg", layer(FRONT_ARM_TABLET), args.force)
    write_text(
        f"{base}/player_composite.svg",
        layer(SHADOW + BODY + HEAD + FRONT_ARM_TABLET),
        args.force,
    )

    lineup_images = [
        '<g transform="translate(14 145) scale(.82)">'
        + SHADOW + BODY + HEAD + FRONT_ARM_TABLET + "</g>"
    ]
    for index, (character_id, spec) in enumerate(P2_CHARACTER_SPECS.items()):
        layers = p2_character_layers(character_id, spec)
        p2_base = f"assets/characters/{character_id}/p2"
        for layer_name, content in layers.items():
            write_text(
                f"{p2_base}/{character_id}_{layer_name}.svg",
                svg_document(320, 360, content, CANVAS_DEFS),
                args.force,
            )
        composite = "".join(layers.values())
        write_text(
            f"{p2_base}/{character_id}_composite.svg",
            svg_document(320, 360, composite, CANVAS_DEFS),
            args.force,
        )
        x = 206 + index * 184
        lineup_images.append(
            f'<g transform="translate({x} 105) scale(.56)">{composite}</g>'
        )

    review_body = f"""
<rect width="1440" height="620" fill="#e8e1d2"/>
<rect x="24" y="24" width="1392" height="572" rx="10" fill="#d8cfba" stroke="#302c27" stroke-width="3"/>
{''.join(lineup_images)}
<text x="52" y="73" font-family="Microsoft YaHei, sans-serif" font-size="31" fill="#292724">序章 P2 人物阵容：主角 / 母亲 / 辛衡 / 禾安 / 船主 / 旧渡人</text>
<text x="52" y="565" font-family="Microsoft YaHei, sans-serif" font-size="18" fill="#54483e">分层：阴影、身体、头部、前臂、持有物 · seed {args.seed} · generator p2.0</text>
"""
    write_text(
        "art/reference/generated_character_lineup.svg",
        svg_document(1440, 620, review_body, CANVAS_DEFS),
        args.force,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
