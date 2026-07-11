"""Generate P3 evening shelter, ritual storehouse, props, rain, and memory art."""

from __future__ import annotations

import random

from asset_tools_common import base_parser, svg_document, write_text


WIDTH = 2200
HEIGHT = 720


def evening_far(rng: random.Random, night: bool) -> str:
    sky_top = "#222f35" if night else "#657477"
    sky_bottom = "#47565a" if night else "#ad9278"
    bank = "#263739" if night else "#4c5c58"
    mist = []
    for _ in range(30):
        x = rng.randint(-140, WIDTH + 100)
        y = rng.randint(100, 440)
        mist.append(
            f'<ellipse cx="{x}" cy="{y}" rx="{rng.randint(100, 280)}" '
            f'ry="{rng.randint(18, 54)}" fill="#d8d8cf" '
            f'fill-opacity="{rng.uniform(.025,.09):.3f}"/>'
        )
    defs = f"""
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{sky_top}"/>
  <stop offset="1" stop-color="{sky_bottom}"/>
</linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{"#354b50" if night else "#657a7a"}"/>
  <stop offset="1" stop-color="{"#1d3137" if night else "#364e52"}"/>
</linearGradient>
"""
    return svg_document(
        WIDTH,
        HEIGHT,
        f"""
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#sky)"/>
<path d="M0 300 Q210 210 430 286 Q670 184 910 287 Q1180 191 1430 280
         Q1740 175 2200 280 L2200 420 L0 420 Z"
      fill="{bank}" fill-opacity=".72"/>
<rect y="348" width="{WIDTH}" height="372" fill="url(#water)"/>
{''.join(mist)}
<path d="M0 421 q190 -12 380 0 t380 0 t380 0 t380 0 t380 0 t380 0"
      fill="none" stroke="#d9dfd6" stroke-opacity=".14" stroke-width="3"/>
""",
        defs,
    )


def shelter_mid(night: bool) -> str:
    timber = "#322d29" if night else "#4c4035"
    awning = "#3c3832" if night else "#5a5042"
    lamp = "#e0a65b" if night else "#bd8651"
    return svg_document(
        WIDTH,
        HEIGHT,
        f"""
<g id="shelter" stroke="#292622" stroke-linejoin="round">
  <path d="M160 344 L558 254 L913 337 L1360 246 L1842 331 L2130 277 L2190 390
           L120 390 Z" fill="{awning}" stroke-width="7"/>
  <path d="M168 349 L537 283 L903 351 M937 349 L1344 276 L1819 351
           M1836 346 L2114 303" fill="none" stroke="#8b7657" stroke-opacity=".5" stroke-width="8"/>
  <g stroke="{timber}" stroke-width="18">
    <path d="M220 288 L211 592"/><path d="M704 295 L695 592"/>
    <path d="M1125 276 L1117 592"/><path d="M1580 281 L1572 592"/>
    <path d="M2040 276 L2034 592"/>
  </g>
  <g stroke="#8a7659" stroke-opacity=".42" stroke-width="4">
    <path d="M211 373 L695 373"/><path d="M1117 373 L1572 373"/>
    <path d="M1572 373 L2034 373"/>
  </g>
</g>
<g id="registry_table" stroke="#302820" stroke-linejoin="round">
  <path d="M837 474 L1213 474 L1183 523 L868 523 Z" fill="#69523d" stroke-width="6"/>
  <path d="M900 516 l-10 98 M1150 516 l13 98" stroke="#453529" stroke-width="14"/>
  <g fill="#a37e4f" stroke="#49372b" stroke-width="2">
    <rect x="906" y="446" width="115" height="34" rx="3"/>
    <rect x="1033" y="450" width="94" height="28" rx="3"/>
  </g>
</g>
<g id="stove">
  <ellipse cx="1472" cy="567" rx="118" ry="25" fill="#171c1c" fill-opacity=".38"/>
  <path d="M1394 500 Q1472 464 1550 501 L1532 582 Q1470 611 1411 580 Z"
        fill="#55483a" stroke="#2d2925" stroke-width="6"/>
  <path d="M1413 532 q59 31 118 0" fill="none" stroke="#8d6d4d" stroke-width="5"/>
  <path d="M1444 566 q28 -59 57 0 q-29 35 -57 0" fill="{lamp}" fill-opacity=".82"/>
  <ellipse cx="1472" cy="488" rx="76" ry="22" fill="#35322f" stroke="#201f1d" stroke-width="5"/>
</g>
<g id="small_lamps" fill="{lamp}" fill-opacity="{"0.78" if night else "0.32"}">
  <circle cx="730" cy="413" r="8"/><circle cx="1580" cy="404" r="8"/>
</g>
""",
    )


def shelter_near(rng: random.Random, night: bool) -> str:
    mud = "#343431" if night else "#62554a"
    puddles = []
    for _ in range(26):
        x = rng.randint(30, WIDTH - 40)
        y = rng.randint(570, 690)
        puddles.append(
            f'<ellipse cx="{x}" cy="{y}" rx="{rng.randint(15,70)}" '
            f'ry="{rng.randint(3,12)}" fill="#738387" fill-opacity=".18"/>'
        )
    return svg_document(
        WIDTH,
        HEIGHT,
        f"""
<path d="M0 526 Q260 484 530 529 Q790 570 1040 526 Q1320 480 1598 532
         Q1880 577 2200 520 L2200 720 L0 720 Z" fill="{mud}"/>
{''.join(puddles)}
<g stroke="#40352b" stroke-width="7" stroke-linecap="round">
  <path d="M76 652 l150 -62 M92 673 l160 -50 M1900 655 l179 -74 M1945 681 l165 -45"/>
</g>
""",
    )


def storehouse_layers() -> dict[str, str]:
    far_defs = """
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#171c1d"/><stop offset="1" stop-color="#252927"/>
</linearGradient>
"""
    far = svg_document(
        WIDTH,
        HEIGHT,
        f"""
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#wall)"/>
<path d="M0 165 L410 58 L885 145 L1336 49 L1790 139 L2200 54 L2200 0 L0 0 Z"
      fill="#0b1012"/>
<g stroke="#394244" stroke-opacity=".48" stroke-width="5">
  <path d="M92 75 L92 526 M188 58 L188 530 M296 44 L296 534
           M1910 66 L1910 538 M2024 48 L2024 537 M2132 40 L2132 538"/>
</g>
<path d="M0 175 L2200 175" stroke="#564636" stroke-width="25"/>
<path d="M242 175 L528 32 M718 175 L1014 24 M1204 175 L1506 22
         M1690 175 L1988 22" stroke="#3b3028" stroke-width="28"/>
<path d="M0 390 Q320 360 630 396 T1260 390 T1890 398 T2200 389"
      fill="none" stroke="#61767c" stroke-opacity=".09" stroke-width="110"/>
""",
        far_defs,
    )
    mid = svg_document(
        WIDTH,
        HEIGHT,
        """
<g id="beams" stroke="#49392d" stroke-width="22">
  <path d="M250 150 L240 625"/><path d="M695 150 L687 625"/>
  <path d="M1114 150 L1106 625"/><path d="M1588 150 L1580 625"/>
  <path d="M2040 150 L2033 625"/>
</g>
<g id="shelves" stroke="#302720" stroke-linejoin="round">
  <rect x="72" y="258" width="480" height="279" fill="#302b27" stroke-width="7"/>
  <path d="M92 345 h440 M92 435 h440 M1648 257 h460 v285 h-460"
        fill="none" stroke="#6b513d" stroke-width="15"/>
  <path d="M1668 347 h420 M1668 438 h420" stroke="#6b513d" stroke-width="15"/>
</g>
<path d="M984 215 Q1112 170 1238 216 L1195 552 L1022 552 Z"
      fill="#263033" fill-opacity=".34" stroke="#4b4238" stroke-width="5"/>
<g fill="#d89b55" fill-opacity=".55">
  <path d="M1092 510 q22 -53 45 0 q-22 31 -45 0"/>
</g>
""",
    )
    near = svg_document(
        WIDTH,
        HEIGHT,
        """
<path d="M0 536 Q350 514 700 547 T1400 540 T2200 532 L2200 720 L0 720 Z"
      fill="#2e2d29"/>
<g stroke="#4a3b2e" stroke-width="6" stroke-linecap="round" opacity=".75">
  <path d="M48 665 l205 -78 M76 693 l210 -58 M1776 679 l246 -91
           M1834 704 l240 -62 M816 655 l143 -43"/>
</g>
<g fill="#6d7776" fill-opacity=".15">
  <ellipse cx="443" cy="620" rx="118" ry="15"/><ellipse cx="1347" cy="650" rx="172" ry="18"/>
</g>
""",
    )
    return {"far.svg": far, "mid.svg": mid, "near.svg": near}


def prop_documents() -> dict[str, str]:
    bronze_defs = """
<linearGradient id="bronze" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#71856f"/><stop offset=".45" stop-color="#40584f"/>
  <stop offset="1" stop-color="#263c39"/>
</linearGradient>
"""
    ding = svg_document(
        430,
        390,
        """
<ellipse cx="214" cy="352" rx="151" ry="21" fill="#111819" fill-opacity=".45"/>
<path d="M69 96 Q214 40 361 96 L338 239 Q214 302 91 239 Z"
      fill="url(#bronze)" stroke="#1e2928" stroke-width="9"/>
<path d="M77 113 Q214 165 353 113 M91 189 Q214 239 340 188"
      fill="none" stroke="#9a8a63" stroke-opacity=".48" stroke-width="9"/>
<path d="M111 79 q-10 -69 49 -57 q48 15 32 73 M237 80 q6 -70 60 -55
      q47 20 22 76" fill="none" stroke="#40584f" stroke-width="18"/>
<path d="M128 246 L111 349 M287 249 L310 348" stroke="#344941" stroke-width="29"/>
<path d="M205 259 L188 334" stroke="#685c47" stroke-width="23" stroke-dasharray="24 13"/>
<path d="M177 335 L229 335" stroke="#78654a" stroke-width="18"/>
""",
        bronze_defs,
    )
    gui = svg_document(
        330,
        280,
        """
<ellipse cx="165" cy="250" rx="116" ry="18" fill="#12191a" fill-opacity=".42"/>
<path d="M62 77 Q165 32 270 77 L247 188 Q165 234 83 188 Z"
      fill="url(#bronze)" stroke="#1e2928" stroke-width="8"/>
<path d="M71 94 Q165 127 259 94 M84 155 Q165 188 248 154"
      fill="none" stroke="#9b8861" stroke-opacity=".42" stroke-width="7"/>
<path d="M70 104 q-58 18 -19 78 q24 26 55 -4 M260 106 q54 23 16 76 q-24 23 -52 -4"
      fill="none" stroke="#40584f" stroke-width="15"/>
<path d="M199 63 l25 23 l-18 22 l-27 -17 Z" fill="#171d1d"/>
""",
        bronze_defs,
    )
    qing = svg_document(
        330,
        340,
        """
<path d="M44 32 H286" stroke="#624d39" stroke-width="17" stroke-linecap="round"/>
<path d="M80 32 v58 M247 32 v61" stroke="#8b704e" stroke-width="5"/>
<path d="M71 86 Q164 49 259 87 L225 251 Q164 288 105 252 Z"
      fill="#5d6863" stroke="#222a29" stroke-width="8"/>
<path d="M92 112 q72 32 145 0 M102 181 q62 29 126 1"
      fill="none" stroke="#a09370" stroke-opacity=".45" stroke-width="7"/>
<path d="M178 70 L151 151 L184 196 L153 277"
      fill="none" stroke="#252d2c" stroke-width="11"/>
<path d="M145 280 l38 -8 l-14 37 l-36 0 Z" fill="#242b2b"/>
""",
    )
    bell = svg_document(
        520,
        590,
        """
<ellipse cx="260" cy="548" rx="188" ry="25" fill="#101718" fill-opacity=".5"/>
<path d="M213 39 Q260 3 307 39 L327 83 L194 83 Z"
      fill="#52675d" stroke="#1f2927" stroke-width="9"/>
<path d="M135 78 Q260 33 386 78 L423 456 Q260 546 97 456 Z"
      fill="url(#bronze)" stroke="#1d2826" stroke-width="11"/>
<path d="M122 130 Q260 177 400 130 M109 218 Q260 267 410 217
         M102 340 Q260 392 418 339 M99 447 Q260 503 421 446"
      fill="none" stroke="#a08d64" stroke-opacity=".42" stroke-width="10"/>
<g fill="#293f3b" stroke="#8c7e5d" stroke-opacity=".38" stroke-width="4">
  <circle cx="169" cy="183" r="18"/><circle cx="235" cy="196" r="18"/>
  <circle cx="302" cy="196" r="18"/><circle cx="368" cy="182" r="18"/>
</g>
<path d="M319 282 L285 351 L329 406 L292 487"
      fill="none" stroke="#152120" stroke-width="15"/>
<path d="M321 283 L299 351 L340 405 L305 485"
      fill="none" stroke="#a99972" stroke-opacity=".22" stroke-width="4"/>
""",
        bronze_defs,
    )
    registry = svg_document(
        500,
        250,
        """
<g fill="#9b7950" stroke="#3d3027" stroke-width="4">
  <rect x="24" y="54" width="92" height="168" rx="3"/>
  <rect x="126" y="38" width="92" height="184" rx="3"/>
  <rect x="228" y="48" width="92" height="174" rx="3"/>
  <rect x="330" y="30" width="92" height="192" rx="3"/>
  <rect x="432" y="58" width="44" height="164" rx="3"/>
</g>
<g stroke="#503a2a" stroke-width="3" opacity=".62">
  <path d="M46 82 h48 M46 108 h48 M46 134 h48 M46 160 h48"/>
  <path d="M147 71 h50 M147 98 h50 M147 125 h50"/>
  <path d="M250 79 h47 M250 106 h47 M250 133 h47"/>
</g>
""",
    )
    stove = svg_document(
        360,
        260,
        """
<ellipse cx="180" cy="229" rx="130" ry="20" fill="#13191a" fill-opacity=".4"/>
<path d="M76 84 Q180 40 284 84 L260 209 Q178 251 98 208 Z"
      fill="#5b4939" stroke="#2d2824" stroke-width="7"/>
<ellipse cx="180" cy="80" rx="91" ry="27" fill="#312f2c" stroke="#1d1d1b" stroke-width="6"/>
<path d="M142 197 q38 -88 77 0 q-38 43 -77 0" fill="#d78942"/>
<path d="M159 194 q19 -48 39 0 q-19 27 -39 0" fill="#e8b35f"/>
""",
    )
    return {
        "broken_ding.svg": ding,
        "chipped_gui.svg": gui,
        "damaged_qing.svg": qing,
        "cracked_bell.svg": bell,
        "refugee_registry.svg": registry,
        "shelter_stove.svg": stove,
    }


def rain_overlay(rng: random.Random) -> str:
    drops = []
    for index in range(185):
        x = rng.randint(-100, WIDTH + 100)
        y = rng.randint(-120, HEIGHT)
        length = rng.randint(20, 70)
        opacity = rng.uniform(.09, .36)
        drops.append(
            f'<path d="M{x} {y} l{-length // 5} {length}" stroke="#bac9c9" '
            f'stroke-opacity="{opacity:.3f}" stroke-width="{1 if index % 5 else 2}"/>'
        )
    return svg_document(WIDTH, HEIGHT, f'<g id="rain">{"".join(drops)}</g>')


def memory_frames() -> dict[str, str]:
    water = svg_document(
        1280,
        720,
        """
<rect width="1280" height="720" fill="#080d10"/>
<g fill="none" stroke="#536e73" stroke-opacity=".38">
  <path d="M-80 180 Q180 84 430 178 T940 176 T1360 161" stroke-width="75"/>
  <path d="M-100 430 Q180 322 470 426 T1040 414 T1400 391" stroke-width="112"/>
</g>
<g fill="#d4d5ca" fill-opacity=".12">
  <ellipse cx="310" cy="295" rx="245" ry="31"/><ellipse cx="916" cy="555" rx="330" ry="39"/>
</g>
""",
    )
    city = svg_document(
        1280,
        720,
        """
<rect width="1280" height="720" fill="#0b1012"/>
<path d="M83 590 V202 H281 V132 H476 V232 H652 V109 H850 V217 H1054 V171 H1211 V590 Z"
      fill="#272624" stroke="#4a3b31" stroke-width="8"/>
<path d="M486 590 V379 Q640 287 794 379 V590 Z" fill="#080b0c"/>
<g fill="#a63e28" fill-opacity=".8">
  <path d="M137 590 q70 -183 140 0"/><path d="M809 590 q94 -265 188 0"/>
  <path d="M1027 590 q56 -155 112 0"/>
</g>
<g fill="#552c27">
  <path d="M214 141 l160 44 l-160 55 Z"/><path d="M902 118 l191 55 l-191 48 Z"/>
</g>
<g fill="#2c3332" fill-opacity=".8">
  <ellipse cx="283" cy="205" rx="178" ry="96"/><ellipse cx="938" cy="224" rx="231" ry="116"/>
</g>
""",
    )
    vessels = svg_document(
        1280,
        720,
        """
<rect width="1280" height="720" fill="#090d0f"/>
<g fill="#334941" stroke="#17221f" stroke-width="10">
  <path d="M109 263 q151 -95 303 0 l-45 239 q-107 69 -215 0 Z"/>
  <path d="M480 302 q119 -71 238 0 l-31 194 q-86 53 -172 0 Z"/>
  <path d="M797 237 q167 -104 336 0 l-53 274 q-115 76 -231 0 Z"/>
</g>
<path d="M254 231 L209 358 L270 426 L218 553 M938 203 L884 344 L955 432 L899 558"
      fill="none" stroke="#0c1312" stroke-width="22"/>
<g fill="#8b3d2d" fill-opacity=".36">
  <ellipse cx="288" cy="575" rx="214" ry="27"/><ellipse cx="923" cy="582" rx="268" ry="33"/>
</g>
""",
    )
    registry = svg_document(
        1280,
        720,
        """
<rect width="1280" height="720" fill="#0a1012"/>
<g transform="translate(115 104) rotate(-3 520 250)" fill="#846343" stroke="#30271f" stroke-width="6">
  <rect x="0" y="0" width="142" height="500"/><rect x="157" y="18" width="142" height="482"/>
  <rect x="314" y="-7" width="142" height="507"/><rect x="471" y="10" width="142" height="490"/>
  <rect x="628" y="-14" width="142" height="514"/><rect x="785" y="22" width="142" height="478"/>
</g>
<g stroke="#29231e" stroke-width="9" opacity=".76">
  <path d="M151 180 h80 M151 241 h80 M151 302 h80 M310 196 h80 M310 257 h80
           M468 170 h80 M468 231 h80 M625 191 h80 M625 252 h80 M782 171 h80"/>
</g>
<g stroke="#b7a98b" stroke-opacity=".3" stroke-width="31">
  <path d="M126 212 L925 175 M139 292 L942 251 M151 374 L954 330"/>
</g>
""",
    )
    hand = svg_document(
        1280,
        720,
        """
<rect width="1280" height="720" fill="#080e10"/>
<path d="M-50 558 Q313 413 667 521 T1350 497" fill="none"
      stroke="#506a6e" stroke-opacity=".32" stroke-width="142"/>
<g transform="translate(552 72) rotate(9 220 250)">
  <path d="M137 154 Q235 88 319 175 L442 552 Q342 640 227 568 L54 278 Q42 199 137 154 Z"
        fill="#8e6d58" stroke="#241f1d" stroke-width="12"/>
  <path d="M129 238 L34 53 M177 219 L110 24 M229 213 L202 17 M279 222 L297 39"
        stroke="#8e6d58" stroke-width="57" stroke-linecap="round"/>
</g>
<g fill="#d9dbd3" fill-opacity=".23">
  <circle cx="661" cy="152" r="13"/><circle cx="731" cy="119" r="9"/><circle cx="827" cy="203" r="15"/>
</g>
""",
    )
    sink = svg_document(
        1280,
        720,
        """
<rect width="1280" height="720" fill="#05090b"/>
<g stroke="#526e70" stroke-opacity=".22" fill="none" stroke-linecap="round">
  <path d="M151 99 Q304 38 489 72 Q682 101 865 61 Q1014 39 1137 98"
        stroke-width="18"/>
  <path d="M222 210 Q387 159 544 190 Q710 222 858 181 Q976 153 1062 207"
        stroke-width="12"/>
  <path d="M337 362 Q474 322 601 349 Q728 379 847 342 Q923 322 984 358"
        stroke-width="8"/>
  <path d="M108 493 Q283 447 430 477 M888 469 Q1031 436 1188 483"
        stroke-width="7"/>
</g>
<g transform="translate(424 191) rotate(-5 260 280) scale(.82)">
  <path d="M135 78 Q260 33 386 78 L423 456 Q260 546 97 456 Z"
        fill="#344b45" stroke="#16221f" stroke-width="12"/>
  <path d="M319 282 L285 351 L329 406 L292 487"
        fill="none" stroke="#0d1715" stroke-width="17"/>
  <path d="M122 130 Q260 177 400 130 M109 218 Q260 267 410 217
           M102 340 Q260 392 418 339" fill="none"
        stroke="#8e805e" stroke-opacity=".4" stroke-width="10"/>
</g>
<g stroke="#536e70" stroke-opacity=".14" stroke-linecap="round">
  <path d="M612 576 q38 42 9 103" stroke-width="31"/>
  <path d="M711 539 q31 56 2 134" stroke-width="13"/>
</g>
""",
    )
    return {
        "water_mask.svg": water,
        "city_fire.svg": city,
        "broken_rituals.svg": vessels,
        "scraped_registry.svg": registry,
        "wet_hand.svg": hand,
        "bell_sinking.svg": sink,
    }


def main() -> int:
    args = base_parser("Generate P3 environments, props, rain, and memory art.").parse_args()
    evening_rng = random.Random(args.seed + 3001)
    night_rng = random.Random(args.seed + 3003)
    base = "assets/environments/old_ferry/p3"
    write_text(f"{base}/shelter_evening_far.svg", evening_far(evening_rng, False), args.force)
    write_text(f"{base}/shelter_evening_mid.svg", shelter_mid(False), args.force)
    write_text(f"{base}/shelter_evening_near.svg", shelter_near(evening_rng, False), args.force)
    write_text(f"{base}/shelter_night_far.svg", evening_far(night_rng, True), args.force)
    write_text(f"{base}/shelter_night_mid.svg", shelter_mid(True), args.force)
    write_text(f"{base}/shelter_night_near.svg", shelter_near(night_rng, True), args.force)
    for filename, document in storehouse_layers().items():
        write_text(f"assets/environments/ritual_storehouse/p3/storehouse_{filename}", document, args.force)
    for filename, document in prop_documents().items():
        write_text(f"assets/props/p3/{filename}", document, args.force)
    write_text(
        "assets/fx/p3/rain.svg",
        rain_overlay(random.Random(args.seed + 3011)),
        args.force,
    )
    for filename, document in memory_frames().items():
        write_text(f"assets/fx/p3/memory/{filename}", document, args.force)
    review = svg_document(
        1100,
        760,
        f"""
<rect width="1100" height="760" fill="#111719"/>
<g transform="translate(0 18) scale(.5)">
  <image href="../../assets/environments/old_ferry/p3/shelter_evening_far.svg" width="{WIDTH}" height="720"/>
  <image href="../../assets/environments/old_ferry/p3/shelter_evening_mid.svg" width="{WIDTH}" height="720"/>
  <image href="../../assets/environments/old_ferry/p3/shelter_evening_near.svg" width="{WIDTH}" height="720"/>
</g>
<g transform="translate(0 390) scale(.5)">
  <image href="../../assets/environments/ritual_storehouse/p3/storehouse_far.svg" width="{WIDTH}" height="720"/>
  <image href="../../assets/environments/ritual_storehouse/p3/storehouse_mid.svg" width="{WIDTH}" height="720"/>
  <image href="../../assets/environments/ritual_storehouse/p3/storehouse_near.svg" width="{WIDTH}" height="720"/>
</g>
<text x="24" y="378" font-family="Microsoft YaHei, sans-serif" font-size="17" fill="#e8e1d2">P3 傍晚流民棚：冷雨 / 灶火 / 临时名册</text>
<text x="24" y="747" font-family="Microsoft YaHei, sans-serif" font-size="17" fill="#e8e1d2">P3 旧礼器库：暗木 / 铜绿 / 漏雨冷光</text>
""",
    )
    write_text("art/reference/generated_p3_scene_color_script.svg", review, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
