"""Generate P6-A refined visual-sample assets for Old Ferry morning.

The assets stay inside the deterministic SVG pipeline so the Godot runtime can
rebuild them offline without relying on external media.  P6-A deliberately
targets only the opening visual sample: old ferry morning, the protagonist,
Mother, Xinheng, and their immediate props.
"""

from __future__ import annotations

import random

from asset_tools_common import base_parser, svg_document, write_text


WIDTH = 2200
HEIGHT = 720


COMMON_DEFS = """
<linearGradient id="linen" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#cfc4ad"/>
  <stop offset=".45" stop-color="#8e846f"/>
  <stop offset="1" stop-color="#514b40"/>
</linearGradient>
<linearGradient id="warm_skin" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#d7b58d"/>
  <stop offset="1" stop-color="#a87858"/>
</linearGradient>
<linearGradient id="old_wood" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#9a7a52"/>
  <stop offset=".55" stop-color="#6d5138"/>
  <stop offset="1" stop-color="#3d3028"/>
</linearGradient>
<linearGradient id="dawn_water" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#8da6a5"/>
  <stop offset=".45" stop-color="#617f82"/>
  <stop offset="1" stop-color="#334f56"/>
</linearGradient>
<pattern id="cloth_threads" width="10" height="10" patternUnits="userSpaceOnUse">
  <path d="M0 2 H10 M2 0 V10" stroke="#f2ead7" stroke-opacity=".10" stroke-width=".7"/>
</pattern>
<pattern id="wood_grain" width="34" height="12" patternUnits="userSpaceOnUse">
  <path d="M1 7 C9 1 18 12 33 5 M3 11 C13 6 20 16 31 10"
        fill="none" stroke="#d3b079" stroke-opacity=".20" stroke-width="1.4"/>
</pattern>
<pattern id="rice_specks" width="18" height="18" patternUnits="userSpaceOnUse">
  <circle cx="5" cy="5" r="1.3" fill="#ead89c" fill-opacity=".75"/>
  <circle cx="13" cy="11" r="1.1" fill="#c9b46e" fill-opacity=".55"/>
</pattern>
"""


def _fog_ellipses(rng: random.Random, count: int, width: int = WIDTH) -> str:
    parts: list[str] = []
    for index in range(count):
        x = rng.randint(-150, width + 150)
        y = rng.randint(68, 435)
        rx = rng.randint(90, 285)
        ry = rng.randint(14, 45)
        opacity = rng.uniform(0.035, 0.15)
        if index % 7 == 0:
            opacity += 0.035
        parts.append(
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
            f'fill="#efe9d7" fill-opacity="{opacity:.3f}"/>'
        )
    return "\n".join(parts)


def _ripples(rng: random.Random, count: int, y_min: int, y_max: int) -> str:
    parts: list[str] = []
    for _ in range(count):
        x = rng.randint(-20, WIDTH - 60)
        y = rng.randint(y_min, y_max)
        length = rng.randint(70, 280)
        opacity = rng.uniform(0.08, 0.24)
        parts.append(
            f'<path d="M{x} {y} q{length // 2} {rng.randint(-7, 7)} {length} 0" '
            f'fill="none" stroke="#edf0dd" stroke-opacity="{opacity:.3f}" '
            f'stroke-width="{rng.randint(1, 3)}"/>'
        )
    return "\n".join(parts)


def morning_far(rng: random.Random) -> str:
    defs = COMMON_DEFS + """
<radialGradient id="dawn_glow" cx=".39" cy=".2" r=".55">
  <stop offset="0" stop-color="#f0d4a3" stop-opacity=".55"/>
  <stop offset=".48" stop-color="#e6d7bd" stop-opacity=".20"/>
  <stop offset="1" stop-color="#9aa9a4" stop-opacity="0"/>
</radialGradient>
<linearGradient id="sky_p6a" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#8fa6a2"/>
  <stop offset=".52" stop-color="#c8c0a9"/>
  <stop offset="1" stop-color="#87958d"/>
</linearGradient>
"""
    body = f"""
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#sky_p6a)"/>
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#dawn_glow)"/>
<circle cx="714" cy="142" r="42" fill="#e7c78f" fill-opacity=".28"/>
<path d="M0 276 Q192 185 384 250 Q560 149 752 244 Q925 167 1120 252
         Q1352 137 1580 244 Q1815 166 2200 252 L2200 388 L0 388 Z"
      fill="#68776c" fill-opacity=".52"/>
<path d="M0 330 Q245 247 480 316 Q742 224 1000 318 Q1246 225 1506 311
         Q1812 218 2200 306 L2200 420 L0 420 Z"
      fill="#435b58" fill-opacity=".48"/>
<rect y="350" width="{WIDTH}" height="370" fill="url(#dawn_water)"/>
{_fog_ellipses(rng, 40)}
{_ripples(rng, 30, 382, 548)}
<g fill="none" stroke="#f4ecd4" stroke-opacity=".14" stroke-width="2">
  <path d="M70 394 C340 378 520 410 780 390 S1280 392 1530 389 S1910 408 2160 386"/>
  <path d="M130 502 C390 486 610 515 860 501 S1360 490 1620 505 S1985 520 2190 498"/>
</g>
<g opacity=".28" fill="#27363a">
  <path d="M1908 168 q12 -10 24 0 q-12 -4 -24 0"/>
  <path d="M1952 190 q10 -8 20 0 q-10 -3 -20 0"/>
</g>
"""
    return svg_document(WIDTH, HEIGHT, body, defs)


def morning_mid(rng: random.Random) -> str:
    houses: list[str] = []
    x = 58
    for index, (w, h) in enumerate(((330, 220), (205, 150), (270, 176), (235, 130))):
        y = 498 - h
        alpha = 0.88 - index * 0.05
        houses.append(
            f"""
<g opacity="{alpha:.2f}" stroke="#312b25" stroke-width="4" stroke-linejoin="round">
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#665847"/>
  <path d="M{x - 36} {y + 27} L{x + w // 2} {y - 77} L{x + w + 38} {y + 27} Z"
        fill="#3d3932"/>
  <path d="M{x + 16} {y + 42} H{x + w - 20}" stroke="#9d805a" stroke-opacity=".32"/>
  <rect x="{x + 50}" y="{y + h - 92}" width="{max(54, w // 5)}" height="92"
        fill="#2f2e2a"/>
  <rect x="{x + w - 91}" y="{y + 62}" width="49" height="58"
        fill="#a47f52" fill-opacity=".36"/>
</g>"""
        )
        x += w - rng.randint(24, 48)

    mooring_posts: list[str] = []
    for px in (830, 1046, 1265, 1498, 1738, 1898):
        mooring_posts.append(
            f"""
<path d="M{px} 356 L{px - 11} 558" stroke="#3a3028" stroke-width="13" stroke-linecap="round"/>
<path d="M{px - 2} 356 L{px - 9} 558" stroke="#b39466" stroke-opacity=".38" stroke-width="3"/>"""
        )

    body = f"""
<g id="home_line">{''.join(houses)}</g>
<g id="landing" stroke="#3a3028" stroke-linejoin="round">
  <path d="M762 447 L1817 447 L1908 519 L702 519 Z" fill="#765b40" stroke-width="5"/>
  <path d="M753 463 L1846 463 M732 486 L1878 486 M713 506 L1900 506"
        stroke="#b49367" stroke-opacity=".55" stroke-width="3"/>
  {''.join(mooring_posts)}
  <path d="M827 408 Q1064 484 1264 408 T1742 410"
        fill="none" stroke="#463a31" stroke-width="10" stroke-linecap="round"/>
  <path d="M828 407 Q1066 468 1265 407 T1740 408"
        fill="none" stroke="#b99c73" stroke-opacity=".46" stroke-width="3" stroke-linecap="round"/>
</g>
<g id="morning_boats" stroke="#302922" stroke-width="5" stroke-linejoin="round">
  <path d="M425 399 Q543 426 668 394 Q623 443 472 439 Z"
        fill="#554738" fill-opacity=".72"/>
  <path d="M505 391 L511 295" stroke="#393029" stroke-width="7"/>
  <path d="M515 306 Q590 342 520 366 Z" fill="#a79a7a" fill-opacity=".52"/>
  <path d="M1960 421 Q2040 437 2148 415 Q2112 455 1992 451 Z"
        fill="#4a4037" fill-opacity=".63"/>
</g>
<g id="nets_and_work" opacity=".78" stroke="#6f5b41" stroke-width="3" fill="none">
  <path d="M138 505 q88 36 174 0 q-19 66 -85 72 q-67 -10 -89 -72"/>
  <path d="M154 521 q70 27 140 0 M169 539 q55 18 108 0 M204 508 v58 M246 508 v58"/>
  <path d="M615 518 c40 14 94 14 135 0 c-18 54 -102 55 -135 0"/>
</g>
{_ripples(rng, 18, 410, 570)}
"""
    return svg_document(WIDTH, HEIGHT, body, COMMON_DEFS)


def morning_near(rng: random.Random) -> str:
    reeds: list[str] = []
    for index in range(96):
        x = rng.randint(-35, WIDTH + 35)
        base = rng.randint(645, 735)
        height = rng.randint(46, 156)
        lean = rng.randint(-22, 22)
        color = "#667258" if index % 4 else "#827b5d"
        reeds.append(
            f'<path d="M{x} {base} Q{x + lean // 2} {base - height // 2} {x + lean} {base - height}" '
            f'fill="none" stroke="{color}" stroke-width="{rng.randint(2, 5)}" stroke-linecap="round"/>'
        )
    stones: list[str] = []
    for _ in range(42):
        sx = rng.randint(0, WIDTH)
        sy = rng.randint(553, 704)
        rx = rng.randint(8, 31)
        stones.append(
            f'<ellipse cx="{sx}" cy="{sy}" rx="{rx}" ry="{max(3, rx // 3)}" '
            'fill="#312d27" fill-opacity=".26"/>'
        )
    body = f"""
<path d="M0 515 Q260 472 516 526 Q798 578 1047 522 Q1323 474 1568 528
         Q1844 584 2200 516 L2200 720 L0 720 Z" fill="#71614e"/>
<path d="M0 560 Q340 518 646 576 Q938 620 1240 560 Q1548 514 1810 572
         Q2027 606 2200 562 L2200 720 L0 720 Z" fill="#806d57" fill-opacity=".55"/>
<path d="M0 548 Q314 512 603 558 T1198 551 T1792 562 T2200 552"
      fill="none" stroke="#a38a63" stroke-opacity=".36" stroke-width="8"/>
{''.join(stones)}
<g id="mother_work_corner" stroke="#3b3028" stroke-width="4" stroke-linejoin="round">
  <ellipse cx="297" cy="585" rx="82" ry="24" fill="#2c2722" fill-opacity=".25"/>
  <path d="M226 551 q70 -36 141 0 l-18 55 q-55 27 -107 1 Z" fill="url(#old_wood)"/>
  <path d="M246 550 q51 25 101 0" fill="none" stroke="#c4a577" stroke-width="4"/>
  <path d="M100 520 h142 v96 h-142 Z" fill="#453b32"/>
  <path d="M122 540 h94 v74" fill="none" stroke="#8c7152" stroke-width="6"/>
  <g stroke="#5f4934" stroke-width="8" stroke-linecap="round">
    <path d="M410 602 l73 -83"/><path d="M435 606 l82 -61"/><path d="M462 608 l79 -39"/>
  </g>
</g>
<g id="front_reeds">{''.join(reeds)}</g>
"""
    return svg_document(WIDTH, HEIGHT, body, COMMON_DEFS)


def prop_documents() -> dict[str, str]:
    boat = svg_document(
        660,
        280,
        """
<ellipse cx="330" cy="243" rx="276" ry="23" fill="#17282d" fill-opacity=".32"/>
<path d="M42 128 Q333 183 618 113 Q568 247 329 253 Q100 245 42 128 Z"
      fill="url(#old_wood)" stroke="#302821" stroke-width="8"/>
<path d="M79 151 Q333 196 579 139 M123 183 Q333 219 535 173"
      fill="none" stroke="#c7a170" stroke-opacity=".48" stroke-width="5"/>
<g fill="#4c3b2e" stroke="#2c241f" stroke-width="5">
  <path d="M205 128 q124 -82 245 0 l-16 45 h-211 Z"/>
  <rect x="265" y="91" width="128" height="54" rx="6"/>
</g>
<path d="M331 83 L337 22" stroke="#3a3028" stroke-width="9"/>
<path d="M343 31 q76 36 4 79 Z" fill="#b6a17d" fill-opacity=".54" stroke="#4a3c31" stroke-width="4"/>
""",
        COMMON_DEFS,
    )
    cable = svg_document(
        620,
        190,
        """
<path d="M28 42 Q287 175 592 44" fill="none" stroke="#3d332b"
      stroke-width="21" stroke-linecap="round"/>
<path d="M31 37 Q290 157 590 39" fill="none" stroke="#b99b70"
      stroke-opacity=".62" stroke-width="5" stroke-linecap="round"/>
<g stroke="#2f2924" stroke-opacity=".45" stroke-width="2">
  <path d="M96 73 q19 11 39 17 M202 121 q23 13 50 18 M376 130 q26 -1 58 -12 M500 88 q24 -4 55 -18"/>
</g>
""",
    )
    grain_bag = svg_document(
        250,
        260,
        """
<ellipse cx="123" cy="226" rx="82" ry="16" fill="#20292b" fill-opacity=".25"/>
<path d="M62 34 Q122 58 184 35 L205 211 Q128 252 45 211 Z"
      fill="#ad9975" stroke="#46392d" stroke-width="7"/>
<path d="M61 52 Q123 74 186 51" fill="none" stroke="#68543e" stroke-width="8"/>
<path d="M63 93 q58 16 121 1 M57 134 q66 19 135 0 M52 176 q71 23 145 0"
      fill="none" stroke="#efe4c6" stroke-opacity=".18" stroke-width="3"/>
<rect x="48" y="67" width="151" height="128" fill="url(#rice_specks)" opacity=".72"/>
<path d="M168 37 q19 38 22 82" fill="none" stroke="#5b4632" stroke-width="5"/>
""",
        COMMON_DEFS,
    )
    pen_box = svg_document(
        320,
        180,
        """
<ellipse cx="160" cy="148" rx="125" ry="13" fill="#182428" fill-opacity=".24"/>
<rect x="34" y="50" width="252" height="86" rx="9" fill="url(#old_wood)"
      stroke="#352b24" stroke-width="7"/>
<rect x="52" y="64" width="216" height="54" rx="5" fill="#936e47"
      stroke="#49372a" stroke-width="3"/>
<path d="M77 93 L232 77" stroke="#362920" stroke-width="7" stroke-linecap="round"/>
<path d="M232 77 l20 9 l-17 10" fill="#202b33"/>
<path d="M57 123 q91 13 199 0" fill="none" stroke="#d0b07e" stroke-opacity=".34" stroke-width="3"/>
""",
        COMMON_DEFS,
    )
    desk = svg_document(
        680,
        345,
        """
<ellipse cx="336" cy="313" rx="255" ry="19" fill="#1c2628" fill-opacity=".25"/>
<path d="M64 119 L617 119 L576 185 L102 185 Z" fill="url(#old_wood)"
      stroke="#302820" stroke-width="8"/>
<path d="M130 178 L116 321 M527 178 L548 321" stroke="#4a382b" stroke-width="20" stroke-linecap="round"/>
<path d="M99 146 H587 M132 168 H557" stroke="#c29c68" stroke-opacity=".34" stroke-width="4"/>
<g fill="#a88355" stroke="#453329" stroke-width="4">
  <rect x="154" y="76" width="222" height="52" rx="5"/>
  <rect x="400" y="94" width="124" height="30" rx="3"/>
  <rect x="213" y="139" width="142" height="27" rx="4" fill="#7f6040"/>
</g>
<path d="M182 94 h151 M182 109 h126 M423 107 h71" stroke="#4c3829" stroke-width="3"/>
<path d="M454 39 L423 130" stroke="#3d2e25" stroke-width="8" stroke-linecap="round"/>
<path d="M455 35 l10 25" stroke="#202b33" stroke-width="8" stroke-linecap="round"/>
<path d="M89 119 q246 35 526 0" fill="none" stroke="#edd5a7" stroke-opacity=".18" stroke-width="4"/>
""",
        COMMON_DEFS,
    )
    return {
        "wood_boat.svg": boat,
        "wood_cable.svg": cable,
        "grain_bag.svg": grain_bag,
        "pen_box.svg": pen_box,
        "xinheng_desk.svg": desk,
    }


def player_layers() -> dict[str, str]:
    shadow = """
<g id="shadow">
  <ellipse cx="128" cy="294" rx="58" ry="13" fill="#142328" fill-opacity=".34"/>
  <ellipse cx="128" cy="291" rx="37" ry="6" fill="#2b3d40" fill-opacity=".25"/>
</g>
"""
    body = """
<g id="legs" stroke="#29241f" stroke-width="3" stroke-linejoin="round">
  <path d="M98 220 L124 220 L119 285 Q109 297 94 287 Z" fill="#535952"/>
  <path d="M128 220 L154 220 L164 286 Q148 297 137 285 Z" fill="#4b534d"/>
  <path d="M90 284 q17 -8 35 1 l-1 11 h-35 Z" fill="#342f29"/>
  <path d="M135 285 q18 -8 34 1 l2 10 h-36 Z" fill="#342f29"/>
</g>
<g id="torso" stroke="#29241f" stroke-width="3" stroke-linejoin="round">
  <path d="M94 147 q34 -20 70 0 l8 79 q-40 24 -84 1 Z" fill="#596b68"/>
  <path d="M99 149 q29 19 61 0" fill="none" stroke="#9aa696" stroke-width="5"/>
  <path d="M111 151 L150 226" fill="none" stroke="#e9dfc8" stroke-opacity=".25" stroke-width="2"/>
  <path d="M88 203 q40 18 83 0" fill="none" stroke="#6f4f35" stroke-width="7"/>
  <path d="M95 147 h68 l8 79 q-40 24 -84 1 Z" fill="url(#cloth_threads)" stroke="none"/>
</g>
<g id="back_arm" stroke="#29241f" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
  <path d="M96 158 q-23 26 -15 63 q13 16 27 -1 l8 -44 Z" fill="#667571"/>
  <path d="M83 218 q5 17 20 15 q15 -9 3 -23 Z" fill="url(#warm_skin)"/>
</g>
<g id="tablet_strap" stroke="#544331" stroke-width="4" stroke-linecap="round">
  <path d="M97 158 q35 38 72 68"/>
</g>
"""
    head = """
<g id="head">
  <path d="M99 91 q-1 -34 29 -43 q36 3 35 45 l-7 33 q-12 18 -31 17
           q-20 -3 -26 -20 Z" fill="url(#warm_skin)" stroke="#29241f" stroke-width="3"/>
  <path d="M99 91 q-9 -26 11 -43 q26 -25 53 6 q16 20 -3 48
           q-14 -24 -34 -28 q-15 17 -27 17 Z" fill="#29241f"/>
  <path d="M111 55 q21 -22 48 -4" fill="none" stroke="#42382f" stroke-width="6" stroke-linecap="round"/>
  <path d="M112 101 q7 3 15 -1 M139 101 q7 3 14 -1" fill="none" stroke="#29241f" stroke-width="2.4" stroke-linecap="round"/>
  <path d="M124 119 q10 2 22 0" fill="none" stroke="#70463c" stroke-width="2" stroke-linecap="round"/>
  <path d="M116 137 q13 9 27 0" fill="none" stroke="#d5b78c" stroke-opacity=".35" stroke-width="3"/>
  <path d="M122 140 L126 151 L145 143 L146 130" fill="#bf9871" stroke="#29241f" stroke-width="3"/>
  <path d="M160 66 q18 3 18 16 q-6 14 -20 10" fill="#2f2925" stroke="#29241f" stroke-width="3"/>
  <path d="M162 70 q15 -10 25 -1" fill="none" stroke="#8c8172" stroke-width="4" stroke-linecap="round"/>
</g>
"""
    front_arm = """
<g id="held_prop" stroke="#29241f" stroke-linejoin="round">
  <g transform="rotate(-7 176 195)">
    <rect x="151" y="147" width="50" height="96" rx="4" fill="#74563a" stroke-width="3"/>
    <rect x="159" y="156" width="34" height="80" rx="2" fill="#a27d50" stroke="#4a3828" stroke-width="1.5"/>
    <path d="M165 171 L186 168 M164 185 L187 182 M163 199 L184 196 M162 214 L182 211"
          stroke="#4a3828" stroke-width="2" stroke-linecap="round"/>
    <path d="M167 231 q12 6 24 0" fill="none" stroke="#d8c191" stroke-opacity=".45" stroke-width="2"/>
  </g>
</g>
<g id="front_arm" stroke="#29241f" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
  <path d="M154 160 q21 20 13 49 l-14 8 q-15 -12 -11 -39 Z" fill="#5f706c"/>
  <path d="M155 207 q14 -4 21 10 q-4 16 -18 12 q-11 -9 -3 -22 Z" fill="url(#warm_skin)"/>
  <path d="M160 218 q8 5 17 -2" fill="none" stroke="#47746f" stroke-width="3"/>
</g>
<g id="ink_marks" fill="#223235" fill-opacity=".75">
  <circle cx="162" cy="217" r="2.3"/><circle cx="170" cy="219" r="1.5"/>
</g>
"""
    return {
        "shadow": shadow,
        "body": body,
        "head": head,
        "front_arm_tablet": front_arm,
    }


ADULT_SPECS = {
    "mother": {
        "center": 158,
        "head_y": 53,
        "skin": "#c59a73",
        "cloth": "#747064",
        "cloth_dark": "#4f4b43",
        "accent": "#839894",
        "hair": "#2d2825",
        "prop": "basin",
        "mood": "waiting",
    },
    "xinheng": {
        "center": 160,
        "head_y": 45,
        "skin": "#b99370",
        "cloth": "#545550",
        "cloth_dark": "#383936",
        "accent": "#425d58",
        "hair": "#6b645a",
        "prop": "tablet_brush",
        "mood": "ink",
    },
}


def adult_layers(character_id: str, spec: dict[str, object]) -> dict[str, str]:
    center = int(spec["center"])
    head_y = int(spec["head_y"])
    skin = str(spec["skin"])
    cloth = str(spec["cloth"])
    cloth_dark = str(spec["cloth_dark"])
    accent = str(spec["accent"])
    hair = str(spec["hair"])
    shoulder = 57 if character_id == "mother" else 51
    left = center - shoulder
    right = center + shoulder
    neck_y = head_y + 86
    hip_y = 258
    foot_y = 338
    shadow = f"""
<g id="shadow">
  <ellipse cx="{center}" cy="343" rx="{shoulder + 26}" ry="12" fill="#172629" fill-opacity=".34"/>
  <ellipse cx="{center}" cy="340" rx="{shoulder - 2}" ry="6" fill="#2c3a3b" fill-opacity=".22"/>
</g>
"""
    body = f"""
<g id="body_back" stroke="#2c2723" stroke-width="3" stroke-linejoin="round">
  <path d="M{left+8} {neck_y+16} q-30 36 -17 91 q15 18 34 0 l17 -76 Z" fill="{cloth_dark}"/>
  <path d="M{right-8} {neck_y+16} q31 37 18 91 q-16 19 -35 0 l-16 -76 Z" fill="{cloth_dark}"/>
</g>
<g id="legs" stroke="#2c2723" stroke-width="3" stroke-linejoin="round">
  <path d="M{center-46} {hip_y-4} L{center-4} {hip_y-5} L{center-13} {foot_y-8}
           q-18 12 -39 0 Z" fill="{cloth_dark}"/>
  <path d="M{center-2} {hip_y-5} L{center+44} {hip_y-4} L{center+53} {foot_y-8}
           q-21 12 -40 0 Z" fill="{cloth_dark}"/>
  <path d="M{center-56} {foot_y-9} q25 -10 50 0 l1 12 h-53 Z" fill="#332f2a"/>
  <path d="M{center+5} {foot_y-9} q25 -10 54 1 l2 11 h-55 Z" fill="#332f2a"/>
</g>
<g id="torso" stroke="#2c2723" stroke-width="3" stroke-linejoin="round">
  <path d="M{left} {neck_y+4} q{shoulder} -20 {right} 0 L{right-8} {hip_y}
           q-{shoulder} 24 -{shoulder * 2 - 16} 0 Z" fill="{cloth}"/>
  <path d="M{left+4} {neck_y+12} q{shoulder-4} 27 {right-4} 0" fill="none"
        stroke="{accent}" stroke-width="5"/>
  <path d="M{left+7} {hip_y-29} q{shoulder} 14 {right-8} 0" fill="none"
        stroke="{accent}" stroke-width="8"/>
  <path d="M{left+5} {neck_y+10} L{right-10} {hip_y-2}" fill="none"
        stroke="#efe4c6" stroke-opacity=".20" stroke-width="2"/>
  <path d="M{left} {neck_y+4} q{shoulder} -20 {right} 0 L{right-8} {hip_y}
           q-{shoulder} 24 -{shoulder * 2 - 16} 0 Z" fill="url(#cloth_threads)" stroke="none"/>
</g>
"""
    forehead_lines = (
        f'<path d="M{center-26} {head_y+43} q10 -6 20 0 M{center+8} {head_y+43} q10 -6 20 0" '
        'fill="none" stroke="#5d4a3c" stroke-width="2" stroke-linecap="round"/>'
    )
    beard = ""
    hair_shape = (
        f'<path d="M{center-39} {head_y+37} q5 -44 {center - (center-4)} -45 '
        f'q42 4 43 47 q-25 -26 -47 -20 q-18 17 -36 18 Z" fill="{hair}"/>'
    )
    if character_id == "mother":
        hair_shape += (
            f'<path d="M{center+22} {head_y+2} q34 -24 46 8 q-15 22 -43 11 Z" '
            f'fill="{hair}" stroke="#2c2723" stroke-width="3"/>'
            f'<path d="M{center+34} {head_y+4} l31 6" stroke="{accent}" stroke-width="5" stroke-linecap="round"/>'
        )
    else:
        beard = (
            f'<path d="M{center-21} {head_y+69} q21 48 43 0 q-8 54 -22 67 q-15 -13 -21 -67 Z" '
            f'fill="{hair}" fill-opacity=".78" stroke="#2c2723" stroke-width="2"/>'
            f'<path d="M{center-30} {head_y+53} q9 9 20 0 M{center+10} {head_y+53} q10 9 21 0" '
            f'fill="none" stroke="{hair}" stroke-width="5" stroke-linecap="round"/>'
        )
    mouth_curve = "q10 1 21 0" if character_id == "mother" else "q10 2 21 0"
    head = f"""
<g id="head">
  <path d="M{center-37} {head_y+31} q1 -29 37 -32 q39 2 39 35
           l-7 36 q-13 22 -33 21 q-22 -2 -33 -21 Z"
        fill="{skin}" stroke="#2c2723" stroke-width="3"/>
  {hair_shape}
  {forehead_lines}
  <path d="M{center-10} {head_y+67} {mouth_curve}" fill="none" stroke="#714a3d"
        stroke-width="2" stroke-linecap="round"/>
  {beard}
  <path d="M{center-14} {head_y+82} L{center-10} {neck_y+8} L{center+16} {neck_y+8}
        L{center+16} {head_y+82}" fill="{skin}" stroke="#2c2723" stroke-width="3"/>
</g>
"""
    front_arm = f"""
<g id="front_arm" stroke="#2c2723" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
  <path d="M{right-6} {neck_y+20} q25 29 9 81 l-20 6 q-13 -28 -4 -76 Z" fill="{cloth}"/>
  <path d="M{right-16} {hip_y-6} q23 -10 35 6 q-4 21 -23 19 q-18 -8 -12 -25 Z" fill="{skin}"/>
</g>
"""
    if str(spec["prop"]) == "basin":
        held_prop = f"""
<g id="held_prop" stroke="#3b3028" stroke-width="3" stroke-linejoin="round">
  <ellipse cx="{center+8}" cy="{hip_y+1}" rx="68" ry="20" fill="#aa8559"/>
  <path d="M{center-58} {hip_y+2} q67 65 134 0 q-13 54 -68 70 q-53 -17 -66 -70 Z"
        fill="#70523a"/>
  <ellipse cx="{center+8}" cy="{hip_y-2}" rx="56" ry="13" fill="#9db0ad" fill-opacity=".78"/>
  <path d="M{center-39} {hip_y-4} q50 14 96 0" fill="none" stroke="#e9efe1" stroke-opacity=".45" stroke-width="3"/>
</g>
"""
    else:
        held_prop = f"""
<g id="held_prop" stroke="#3b3028" stroke-linejoin="round">
  <rect x="{center+12}" y="{neck_y+22}" width="44" height="108" rx="4"
        fill="#8b6844" stroke-width="3"/>
  <path d="M{center+20} {neck_y+42} h28 M{center+20} {neck_y+59} h26 M{center+20} {neck_y+76} h24"
        stroke="#4c3829" stroke-width="2"/>
  <path d="M{center-29} {neck_y+12} L{center+17} {hip_y+8}" stroke="#4c3528" stroke-width="5" stroke-linecap="round"/>
  <path d="M{center-32} {neck_y+6} l8 20" stroke="#202b33" stroke-width="5" stroke-linecap="round"/>
</g>
"""
    return {
        "shadow": shadow,
        "body": body,
        "head": head,
        "front_arm": front_arm,
        "held_prop": held_prop,
    }


def _wrap_player_layer(content: str) -> str:
    return svg_document(256, 320, content, COMMON_DEFS)


def _wrap_adult_layer(content: str) -> str:
    return svg_document(320, 360, content, COMMON_DEFS)


def write_character_assets(args) -> tuple[str, str, str]:
    player = player_layers()
    player_base = "assets/characters/player/p6a"
    for layer_name, content in player.items():
        write_text(f"{player_base}/player_{layer_name}.svg", _wrap_player_layer(content), args.force)
    player_composite = "".join(player.values())
    write_text(
        f"{player_base}/player_composite.svg",
        _wrap_player_layer(player_composite),
        args.force,
    )

    composites = {"player": player_composite}
    for character_id, spec in ADULT_SPECS.items():
        layers = adult_layers(character_id, spec)
        base = f"assets/characters/{character_id}/p6a"
        for layer_name, content in layers.items():
            write_text(f"{base}/{character_id}_{layer_name}.svg", _wrap_adult_layer(content), args.force)
        composite = "".join(layers.values())
        composites[character_id] = composite
        write_text(
            f"{base}/{character_id}_composite.svg",
            _wrap_adult_layer(composite),
            args.force,
        )

    review_body = f"""
<rect width="1300" height="560" fill="#e8e1d2"/>
<rect x="28" y="28" width="1244" height="504" rx="12" fill="#d8cfba" stroke="#302c27" stroke-width="3"/>
<text x="58" y="82" font-family="Microsoft YaHei, sans-serif" font-size="32" fill="#292724">P6-A 序章视觉样片：主角 / 母亲 / 辛衡</text>
<text x="58" y="115" font-family="Microsoft YaHei, sans-serif" font-size="17" fill="#5b4d40">动作差异：主角停顿称量；母亲数米又望河道；辛衡停笔、递牍、墨痕在手。</text>
<g transform="translate(135 172) scale(.9)">{composites["player"]}</g>
<g transform="translate(455 134) scale(.82)">{composites["mother"]}</g>
<g transform="translate(820 134) scale(.82)">{composites["xinheng"]}</g>
<text x="174" y="495" font-family="Microsoft YaHei, sans-serif" font-size="20" fill="#292724">十岁主角</text>
<text x="529" y="495" font-family="Microsoft YaHei, sans-serif" font-size="20" fill="#292724">母亲：不说等，却一直看</text>
<text x="910" y="495" font-family="Microsoft YaHei, sans-serif" font-size="20" fill="#292724">辛衡：旧书吏，停笔的人</text>
<text x="58" y="528" font-family="Microsoft YaHei, sans-serif" font-size="15" fill="#6a5948">seed {args.seed} · runtime SVG layers · generator P6-A</text>
"""
    write_text(
        "art/reference/generated_p6a_character_sheet.svg",
        svg_document(1300, 560, review_body, COMMON_DEFS),
        args.force,
    )
    return composites["player"], composites["mother"], composites["xinheng"]


def write_environment_assets(args) -> None:
    base = "assets/environments/old_ferry/p6a"
    write_text(f"{base}/morning_far.svg", morning_far(random.Random(args.seed + 611)), args.force)
    write_text(f"{base}/morning_mid.svg", morning_mid(random.Random(args.seed + 613)), args.force)
    write_text(f"{base}/morning_near.svg", morning_near(random.Random(args.seed + 617)), args.force)
    for filename, document in prop_documents().items():
        write_text(f"assets/props/p6a/{filename}", document, args.force)

    review_body = f"""
<rect width="1180" height="760" fill="#202b33"/>
<g transform="translate(0 24) scale(.536)">
  <image href="../../assets/environments/old_ferry/p6a/morning_far.svg" width="{WIDTH}" height="{HEIGHT}"/>
  <image href="../../assets/environments/old_ferry/p6a/morning_mid.svg" width="{WIDTH}" height="{HEIGHT}"/>
  <image href="../../assets/environments/old_ferry/p6a/morning_near.svg" width="{WIDTH}" height="{HEIGHT}"/>
</g>
<rect x="0" y="426" width="1180" height="334" fill="#2b3333"/>
<text x="34" y="470" font-family="Microsoft YaHei, sans-serif" font-size="28" fill="#e8e1d2">P6-A 旧渡清晨视觉样片</text>
<text x="34" y="504" font-family="Microsoft YaHei, sans-serif" font-size="16" fill="#cfc4ad">冷雾、湿木、旧屋檐、木缆、河面亮线；把“父亲未归”的压力留在母亲的动作和河道尽头。</text>
<g transform="translate(42 532) scale(.34)">
  <image href="../../assets/props/p6a/wood_boat.svg" width="660" height="280"/>
</g>
<g transform="translate(312 552) scale(.34)">
  <image href="../../assets/props/p6a/wood_cable.svg" width="620" height="190"/>
</g>
<g transform="translate(572 528) scale(.42)">
  <image href="../../assets/props/p6a/grain_bag.svg" width="250" height="260"/>
</g>
<g transform="translate(714 552) scale(.42)">
  <image href="../../assets/props/p6a/pen_box.svg" width="320" height="180"/>
</g>
<g transform="translate(884 520) scale(.36)">
  <image href="../../assets/props/p6a/xinheng_desk.svg" width="680" height="345"/>
</g>
<text x="34" y="734" font-family="Microsoft YaHei, sans-serif" font-size="15" fill="#cfc4ad">seed {args.seed} · generator P6-A · no external downloaded media</text>
"""
    write_text(
        "art/reference/generated_p6a_old_ferry_visual_sheet.svg",
        svg_document(1180, 760, review_body, COMMON_DEFS),
        args.force,
    )


def main() -> int:
    args = base_parser("Generate P6-A old-ferry morning visual sample assets.").parse_args()
    write_environment_assets(args)
    write_character_assets(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
