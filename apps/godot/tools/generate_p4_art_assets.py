"""Generate P4 rain-night cart-crash scene, props, and review board."""

from __future__ import annotations

import random

from asset_tools_common import base_parser, svg_document, write_text


WIDTH = 2200
HEIGHT = 720


def crash_far(rng: random.Random) -> str:
    rain_mist = []
    for _ in range(34):
        rain_mist.append(
            f'<ellipse cx="{rng.randint(-120, WIDTH + 120)}" cy="{rng.randint(90, 470)}" '
            f'rx="{rng.randint(120, 310)}" ry="{rng.randint(16, 52)}" '
            f'fill="#b5c2bd" fill-opacity="{rng.uniform(.025,.085):.3f}"/>'
        )
    defs = """
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#10181d"/>
  <stop offset=".6" stop-color="#202e35"/>
  <stop offset="1" stop-color="#28343a"/>
</linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#283f47"/>
  <stop offset="1" stop-color="#14262c"/>
</linearGradient>
"""
    return svg_document(
        WIDTH,
        HEIGHT,
        f"""
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#sky)"/>
<path d="M0 300 Q290 232 520 286 Q810 210 1050 292 Q1360 211 1640 290
         Q1900 218 2200 276 L2200 420 L0 420 Z"
      fill="#1d2e31" fill-opacity=".88"/>
<rect y="348" width="{WIDTH}" height="372" fill="url(#water)"/>
{''.join(rain_mist)}
<path d="M0 422 q210 -14 420 0 t420 0 t420 0 t420 0 t420 0"
      fill="none" stroke="#ced7d2" stroke-opacity=".12" stroke-width="4"/>
""",
        defs,
    )


def crash_mid() -> str:
    return svg_document(
        WIDTH,
        HEIGHT,
        """
<g id="old_ferry_rain_shelter" stroke="#211d1b" stroke-linejoin="round">
  <path d="M42 360 L420 286 L790 351 L1180 286 L1520 350 L1970 281 L2190 355
           L2190 426 L42 426 Z"
        fill="#3a352f" stroke-width="7"/>
  <g stroke="#5f503e" stroke-width="16">
    <path d="M178 322 L172 616"/><path d="M604 326 L598 616"/>
    <path d="M1020 319 L1014 616"/><path d="M1430 320 L1423 616"/>
    <path d="M1980 318 L1976 616"/>
  </g>
  <path d="M118 423 H2140" stroke="#78644a" stroke-width="9" stroke-opacity=".55"/>
</g>
<g id="torches" fill="#da9b4b" fill-opacity=".86">
  <path d="M418 448 q28 -79 56 0 q-27 38 -56 0"/>
  <path d="M1766 430 q23 -62 47 0 q-24 30 -47 0"/>
</g>
<g id="rain_dark_people" fill="#202828" stroke="#101616" stroke-width="3">
  <path d="M1700 456 q28 -47 57 0 l-8 107 h-41 Z"/>
  <path d="M1835 472 q32 -50 64 0 l-10 99 h-45 Z"/>
  <path d="M1925 455 q27 -42 54 0 l-8 108 h-39 Z"/>
</g>
""",
    )


def crash_near(rng: random.Random) -> str:
    puddles = []
    for _ in range(36):
        puddles.append(
            f'<ellipse cx="{rng.randint(20, WIDTH - 20)}" cy="{rng.randint(550, 704)}" '
            f'rx="{rng.randint(26, 95)}" ry="{rng.randint(4, 16)}" '
            f'fill="#6f8587" fill-opacity="{rng.uniform(.13,.29):.3f}"/>'
        )
    return svg_document(
        WIDTH,
        HEIGHT,
        f"""
<path d="M0 515 Q250 474 520 524 Q790 572 1080 522 Q1380 476 1665 531
         Q1920 574 2200 520 L2200 720 L0 720 Z" fill="#3b352f"/>
{''.join(puddles)}
<g stroke="#2a2521" stroke-width="8" stroke-linecap="round" opacity=".75">
  <path d="M62 654 l205 -76 M90 691 l242 -61 M742 670 l212 -72
           M1480 655 l240 -70 M1782 690 l270 -75"/>
</g>
<g fill="none" stroke="#d59a4b" stroke-opacity=".2" stroke-width="5">
  <ellipse cx="480" cy="610" rx="242" ry="34"/>
  <ellipse cx="1100" cy="622" rx="250" ry="39"/>
  <ellipse cx="1760" cy="606" rx="264" ry="42"/>
</g>
""",
    )


def heavy_rain(rng: random.Random) -> str:
    drops = []
    for index in range(270):
        x = rng.randint(-160, WIDTH + 160)
        y = rng.randint(-140, HEIGHT)
        length = rng.randint(28, 88)
        drops.append(
            f'<path d="M{x} {y} l{-length // 4} {length}" stroke="#bfd0d1" '
            f'stroke-opacity="{rng.uniform(.10,.38):.3f}" '
            f'stroke-width="{1 if index % 6 else 2}"/>'
        )
    return svg_document(WIDTH, HEIGHT, f'<g id="heavy_rain">{"".join(drops)}</g>')


def props() -> dict[str, str]:
    cart = svg_document(
        760,
        430,
        """
<ellipse cx="350" cy="390" rx="300" ry="32" fill="#101719" fill-opacity=".45"/>
<g transform="translate(88 48) rotate(-9 310 180)" stroke="#211a16" stroke-linejoin="round">
  <path d="M72 88 L515 45 L633 188 L169 246 Z" fill="#5f4532" stroke-width="10"/>
  <path d="M118 120 L552 79 M154 168 L592 125 M190 217 L628 177"
        stroke="#8a6744" stroke-width="9"/>
  <path d="M84 260 L670 120" stroke="#4b3426" stroke-width="20"/>
  <path d="M290 244 q-92 10 -129 87" stroke="#39281e" stroke-width="15"/>
  <circle cx="143" cy="316" r="67" fill="#2b211b" stroke="#7d5b3c" stroke-width="13"/>
  <path d="M99 270 L186 360 M185 268 L101 361 M143 249 V383 M72 316 H214"
        stroke="#866544" stroke-width="7"/>
  <path d="M520 205 q64 18 96 66" stroke="#2d211b" stroke-width="15"/>
</g>
<path d="M116 212 L283 273" stroke="#211a16" stroke-width="14"/>
<path d="M128 216 L278 270" stroke="#a77d4d" stroke-width="5" stroke-dasharray="28 15"/>
""",
    )
    child = svg_document(
        280,
        220,
        """
<ellipse cx="141" cy="188" rx="100" ry="16" fill="#0d1416" fill-opacity=".45"/>
<path d="M60 102 q71 -55 142 0 l-20 64 q-52 33 -103 0 Z"
      fill="#756451" stroke="#2c2520" stroke-width="6"/>
<circle cx="132" cy="84" r="29" fill="#9a765e" stroke="#2c2520" stroke-width="5"/>
<path d="M107 118 L53 154 M154 119 L215 151" stroke="#514139" stroke-width="16" stroke-linecap="round"/>
<path d="M28 44 L254 76" stroke="#4b3426" stroke-width="25" stroke-linecap="round"/>
<path d="M30 43 L254 75" stroke="#916842" stroke-width="7" stroke-linecap="round"/>
""",
    )
    tablets = svg_document(
        520,
        260,
        """
<ellipse cx="262" cy="209" rx="223" ry="31" fill="#5e7679" fill-opacity=".28"/>
<g fill="#9b764c" stroke="#342921" stroke-width="4">
  <rect x="68" y="86" width="76" height="146" rx="3" transform="rotate(-18 106 159)"/>
  <rect x="170" y="64" width="76" height="156" rx="3" transform="rotate(7 208 142)"/>
  <rect x="284" y="76" width="80" height="144" rx="3" transform="rotate(-6 324 148)"/>
  <rect x="394" y="92" width="58" height="118" rx="3" transform="rotate(17 423 151)"/>
</g>
<g stroke="#1f1a16" stroke-opacity=".58" stroke-width="4">
  <path d="M85 121 h42 M82 148 h45 M80 176 h43"/>
  <path d="M191 102 h39 M192 130 h41 M191 157 h36"/>
  <path d="M303 116 h45 M302 143 h41"/>
</g>
<g fill="#1f2222" fill-opacity=".32">
  <ellipse cx="249" cy="154" rx="74" ry="20"/>
  <ellipse cx="372" cy="181" rx="92" ry="23"/>
</g>
""",
    )
    crowd = svg_document(
        620,
        300,
        """
<ellipse cx="318" cy="258" rx="265" ry="26" fill="#101719" fill-opacity=".45"/>
<g stroke="#171d1d" stroke-width="4">
  <g fill="#5d554b">
    <path d="M64 113 q33 -57 66 0 l-12 119 H77 Z"/>
    <path d="M146 88 q38 -66 76 0 l-12 146 h-52 Z"/>
    <path d="M250 123 q30 -51 61 0 l-10 108 h-41 Z"/>
    <path d="M334 78 q39 -67 78 0 l-11 157 h-56 Z"/>
    <path d="M458 112 q33 -58 66 0 l-11 122 h-44 Z"/>
    <path d="M525 142 q26 -42 52 0 l-8 88 h-36 Z"/>
  </g>
  <g fill="#8a6850">
    <circle cx="96" cy="89" r="22"/><circle cx="184" cy="61" r="24"/>
    <circle cx="281" cy="101" r="20"/><circle cx="373" cy="49" r="24"/>
    <circle cx="491" cy="88" r="22"/><circle cx="551" cy="124" r="17"/>
  </g>
</g>
<path d="M151 140 q58 22 98 0 M398 141 q48 -39 96 -4"
      fill="none" stroke="#d79a48" stroke-opacity=".55" stroke-width="8"/>
<path d="M238 188 q-27 -38 -56 -1" fill="none" stroke="#a08a64" stroke-width="7"/>
""",
    )
    horse = svg_document(
        480,
        260,
        """
<ellipse cx="243" cy="225" rx="176" ry="18" fill="#0b1112" fill-opacity=".44"/>
<path d="M87 129 q107 -78 236 -20 q45 22 90 -30 q35 26 10 67
         q-35 48 -104 44 q-101 40 -214 6 q-50 -14 -60 -47 q-9 -31 42 -20 Z"
      fill="#1b2020" stroke="#0f1414" stroke-width="8"/>
<path d="M139 183 l-24 58 M218 192 l-10 58 M309 185 l22 58 M374 164 l43 46"
      stroke="#1b2020" stroke-width="17" stroke-linecap="round"/>
<path d="M398 84 q25 -62 70 -32" fill="none" stroke="#1b2020" stroke-width="13"/>
""",
    )
    bucket = svg_document(
        220,
        220,
        """
<ellipse cx="111" cy="190" rx="75" ry="15" fill="#111719" fill-opacity=".4"/>
<path d="M55 74 Q111 50 166 74 L151 176 Q111 202 70 176 Z"
      fill="#6e5036" stroke="#2b221b" stroke-width="7"/>
<path d="M61 85 q50 27 101 0 M67 132 q43 22 88 0" fill="none"
      stroke="#aa8355" stroke-width="6"/>
<path d="M64 70 q47 -65 94 0" fill="none" stroke="#3f3025" stroke-width="8"/>
<g fill="#d8e2df" fill-opacity=".45">
  <ellipse cx="109" cy="80" rx="48" ry="10"/>
  <path d="M84 54 q22 -46 48 0" fill="none" stroke="#d8e2df" stroke-width="7" stroke-opacity=".28"/>
</g>
""",
    )
    ink = svg_document(
        480,
        240,
        """
<rect width="480" height="240" fill="none"/>
<g fill="#1f2323" fill-opacity=".32">
  <ellipse cx="150" cy="129" rx="80" ry="24"/>
  <ellipse cx="245" cy="151" rx="126" ry="31"/>
  <ellipse cx="330" cy="118" rx="70" ry="20"/>
</g>
<g fill="none" stroke="#9bb2b2" stroke-opacity=".22">
  <ellipse cx="240" cy="135" rx="180" ry="46" stroke-width="5"/>
  <ellipse cx="244" cy="136" rx="118" ry="28" stroke-width="3"/>
</g>
""",
    )
    return {
        "overturned_cart.svg": cart,
        "trapped_child.svg": child,
        "wet_tablets.svg": tablets,
        "separated_crowd.svg": crowd,
        "horse_shadow.svg": horse,
        "hot_water_bucket.svg": bucket,
        "wet_ink_spread.svg": ink,
    }


def main() -> int:
    args = base_parser("Generate P4 cart-crash art assets.").parse_args()
    rng = random.Random(args.seed + 4001)
    base = "assets/environments/old_ferry/p4"
    write_text(f"{base}/crash_rain_far.svg", crash_far(rng), args.force)
    write_text(f"{base}/crash_rain_mid.svg", crash_mid(), args.force)
    write_text(f"{base}/crash_rain_near.svg", crash_near(random.Random(args.seed + 4003)), args.force)
    write_text("assets/fx/p4/rain_heavy.svg", heavy_rain(random.Random(args.seed + 4005)), args.force)
    for filename, document in props().items():
        write_text(f"assets/props/p4/{filename}", document, args.force)
    review = svg_document(
        1100,
        380,
        f"""
<rect width="1100" height="380" fill="#10181d"/>
<g transform="translate(0 10) scale(.5)">
  <image href="../../assets/environments/old_ferry/p4/crash_rain_far.svg" width="{WIDTH}" height="{HEIGHT}"/>
  <image href="../../assets/environments/old_ferry/p4/crash_rain_mid.svg" width="{WIDTH}" height="{HEIGHT}"/>
  <image href="../../assets/environments/old_ferry/p4/crash_rain_near.svg" width="{WIDTH}" height="{HEIGHT}"/>
</g>
<text x="24" y="362" font-family="Microsoft YaHei, sans-serif" font-size="18" fill="#e8e1d2">
P4 雨夜翻车：左=车辕下孩子 / 中=泥水湿简 / 右=失散人群；暖火只作方向引导
</text>
""",
    )
    write_text("art/reference/generated_p4_crash_scene.svg", review, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
