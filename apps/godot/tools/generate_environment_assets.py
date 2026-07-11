"""Generate layered P0/P2 old-ferry environments and narrative props."""

from __future__ import annotations

import random

from asset_tools_common import base_parser, svg_document, write_text


WIDTH = 1920
HEIGHT = 720
P2_WIDTH = 2200


def far_layer(rng: random.Random) -> str:
    wisps = []
    for _ in range(22):
        x = rng.randint(-120, WIDTH)
        y = rng.randint(75, 315)
        rx = rng.randint(95, 260)
        ry = rng.randint(16, 42)
        opacity = rng.uniform(0.035, 0.11)
        wisps.append(
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
            f'fill="#e8e1d2" fill-opacity="{opacity:.3f}"/>'
        )
    defs = """
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#93a3a0"/><stop offset=".58" stop-color="#b8b8aa"/>
  <stop offset="1" stop-color="#8b9690"/>
</linearGradient>
<linearGradient id="farwater" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#647d7e"/><stop offset="1" stop-color="#30484e"/>
</linearGradient>
"""
    return svg_document(
        WIDTH,
        HEIGHT,
        f"""
<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#sky)"/>
<path d="M0 278 Q180 190 350 248 Q510 155 710 245 Q900 176 1080 247 Q1290 148 1510 238 Q1730 178 1920 250 L1920 390 L0 390 Z"
      fill="#586d69" fill-opacity=".48"/>
<path d="M0 325 Q220 242 430 310 Q670 218 890 315 Q1110 225 1340 304 Q1610 212 1920 300 L1920 420 L0 420 Z"
      fill="#475e5d" fill-opacity=".58"/>
<rect y="342" width="{WIDTH}" height="378" fill="url(#farwater)"/>
{''.join(wisps)}
<path d="M0 390 Q260 381 520 392 T1040 388 T1560 394 T1920 386" fill="none" stroke="#d8ded4" stroke-opacity=".18" stroke-width="3"/>
""",
        defs,
    )


def mid_layer(rng: random.Random) -> str:
    houses = []
    x = 1180
    for index in range(5):
        width = rng.randint(105, 155)
        height = rng.randint(88, 132)
        houses.append(
            f'<g opacity="{0.72 - index * 0.04:.2f}">'
            f'<rect x="{x}" y="{405-height}" width="{width}" height="{height}" fill="#55493d" stroke="#332f2a" stroke-width="3"/>'
            f'<path d="M{x-18} {405-height+10} L{x+width/2:.0f} {365-height} L{x+width+18} {405-height+10} Z" '
            f'fill="#403b34" stroke="#2d2b28" stroke-width="3"/>'
            f'<rect x="{x+18}" y="{405-height+35}" width="21" height="34" fill="#b78c50" fill-opacity=".34"/>'
            f'</g>'
        )
        x += width - 4

    ripples = []
    for _ in range(19):
        x1 = rng.randint(20, WIDTH - 120)
        y = rng.randint(390, 520)
        length = rng.randint(55, 180)
        ripples.append(
            f'<path d="M{x1} {y} q{length//2} {rng.randint(-4,4)} {length} 0" '
            'fill="none" stroke="#d9dfd6" stroke-opacity=".18" stroke-width="2"/>'
        )
    return svg_document(
        WIDTH,
        HEIGHT,
        f"""
<g id="far_boats" opacity=".65">
  <path d="M210 386 Q310 405 408 384 Q367 425 252 422 Z" fill="#4b4238" stroke="#2f2b27" stroke-width="4"/>
  <path d="M308 382 L312 295" stroke="#3b352f" stroke-width="6"/>
  <path d="M313 304 Q373 335 314 356 Z" fill="#8a8174" fill-opacity=".52"/>
  <path d="M760 423 Q847 438 929 418 Q895 454 790 453 Z" fill="#51473b" stroke="#302c28" stroke-width="4"/>
</g>
<g id="buildings_back">{''.join(houses)}</g>
<g id="landing">
  <path d="M1040 445 L1635 445 L1730 516 L980 516 Z" fill="#6b513d" stroke="#3b3128" stroke-width="4"/>
  <path d="M1040 461 L1660 461 M1018 483 L1690 483" stroke="#8b6c4b" stroke-width="3" stroke-opacity=".65"/>
  <g stroke="#3e332a" stroke-width="10"><path d="M1120 386 L1112 548"/><path d="M1512 379 L1506 545"/><path d="M1750 397 L1736 548"/></g>
  <path d="M1115 407 Q1310 480 1510 409" fill="none" stroke="#54483e" stroke-width="8"/>
  <path d="M1120 408 Q1310 468 1512 408" fill="none" stroke="#9d8568" stroke-width="2" stroke-opacity=".65"/>
</g>
{''.join(ripples)}
""",
    )


def near_layer(rng: random.Random) -> str:
    reeds = []
    for index in range(58):
        x = rng.randint(-20, WIDTH + 20)
        base = rng.randint(650, 735)
        height = rng.randint(48, 150)
        lean = rng.randint(-18, 18)
        color = "#59654f" if index % 3 else "#707358"
        reeds.append(
            f'<path d="M{x} {base} Q{x+lean//2} {base-height//2} {x+lean} {base-height}" '
            f'fill="none" stroke="{color}" stroke-width="{rng.randint(2,5)}" stroke-linecap="round"/>'
        )
    stones = []
    for _ in range(28):
        x = rng.randint(0, WIDTH)
        y = rng.randint(565, 690)
        rx = rng.randint(8, 28)
        stones.append(
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{max(3, rx//3)}" fill="#3d3934" fill-opacity=".26"/>'
        )
    return svg_document(
        WIDTH,
        HEIGHT,
        f"""
<path d="M0 528 Q225 489 430 532 Q690 575 925 525 Q1150 486 1390 529 Q1660 579 1920 520 L1920 720 L0 720 Z"
      fill="#54483e"/>
<path d="M0 560 Q285 529 535 574 Q775 612 1040 558 Q1325 513 1570 568 Q1765 606 1920 570 L1920 720 L0 720 Z"
      fill="#65584b" fill-opacity=".78"/>
<path d="M0 548 Q300 515 590 560 T1160 548 T1710 559 T1920 550" fill="none" stroke="#857461" stroke-opacity=".45" stroke-width="8"/>
{''.join(stones)}
<g id="foreground_reeds">{''.join(reeds)}</g>
<g id="home_props" transform="translate(90 0)">
  <ellipse cx="215" cy="580" rx="62" ry="20" fill="#3b3430" fill-opacity=".35"/>
  <path d="M165 556 Q215 530 265 556 L254 593 Q214 611 176 592 Z" fill="#70563e" stroke="#3a3028" stroke-width="4"/>
  <path d="M180 553 Q214 574 251 553" fill="none" stroke="#b2966f" stroke-width="4"/>
  <g stroke="#564534" stroke-width="7" stroke-linecap="round">
    <path d="M300 591 L354 530"/><path d="M315 594 L375 544"/><path d="M335 596 L388 555"/>
  </g>
</g>
""",
    )


def p2_far_layer(rng: random.Random, daylight: bool) -> str:
    sky_top = "#aab6ae" if daylight else "#839794"
    sky_bottom = "#c8c4ad" if daylight else "#aeb4a8"
    far_bank = "#65766d" if daylight else "#536a67"
    water_top = "#769194" if daylight else "#5d797c"
    water_bottom = "#3f5e63" if daylight else "#304d54"
    fog = []
    for _ in range(30):
        x = rng.randint(-120, P2_WIDTH + 100)
        y = rng.randint(55, 385)
        fog.append(
            f'<ellipse cx="{x}" cy="{y}" rx="{rng.randint(90, 250)}" '
            f'ry="{rng.randint(14, 38)}" fill="#e8e1d2" '
            f'fill-opacity="{rng.uniform(.035, .12):.3f}"/>'
        )
    defs = f"""
<linearGradient id="p2sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{sky_top}"/><stop offset="1" stop-color="{sky_bottom}"/>
</linearGradient>
<linearGradient id="p2water" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{water_top}"/><stop offset="1" stop-color="{water_bottom}"/>
</linearGradient>
"""
    body = f"""
<rect width="{P2_WIDTH}" height="{HEIGHT}" fill="url(#p2sky)"/>
<path d="M0 282 Q180 184 388 254 Q560 150 760 250 Q930 175 1130 258
         Q1330 142 1575 246 Q1830 169 2200 252 L2200 391 L0 391 Z"
      fill="{far_bank}" fill-opacity=".56"/>
<path d="M0 333 Q240 248 470 319 Q730 226 985 320 Q1245 222 1495 312
         Q1810 218 2200 307 L2200 411 L0 411 Z" fill="#445c59" fill-opacity=".46"/>
<rect y="350" width="{P2_WIDTH}" height="370" fill="url(#p2water)"/>
{''.join(fog)}
<g fill="none" stroke="#e7e6d8" stroke-opacity=".18" stroke-width="2">
  <path d="M40 405 q160 -10 320 0 t320 0 t320 0 t320 0 t320 0 t320 0"/>
  <path d="M130 458 q120 8 245 0 t250 0 t250 0 t250 0 t250 0 t250 0"/>
</g>
"""
    return svg_document(P2_WIDTH, HEIGHT, body, defs)


def p2_mid_layer(daylight: bool) -> str:
    building = "#625445" if daylight else "#554a3f"
    roof = "#403a32"
    return svg_document(
        P2_WIDTH,
        HEIGHT,
        f"""
<g id="buildings_back" stroke="#302c28" stroke-width="4">
  <rect x="38" y="284" width="350" height="214" fill="{building}"/>
  <path d="M2 306 L211 210 L431 306 Z" fill="{roof}"/>
  <rect x="78" y="344" width="104" height="154" fill="#2d2c29"/>
  <rect x="235" y="365" width="94" height="72" fill="#80694c" fill-opacity=".55"/>
  <path d="M450 391 L635 293 L823 391 Z" fill="{roof}" fill-opacity=".82"/>
  <rect x="482" y="380" width="304" height="120" fill="{building}" fill-opacity=".86"/>
  <rect x="541" y="421" width="62" height="79" fill="#302f2b"/>
  <path d="M1710 410 L1850 334 L1997 410 Z" fill="{roof}" fill-opacity=".78"/>
  <rect x="1734" y="401" width="240" height="102" fill="{building}" fill-opacity=".74"/>
</g>
<g id="landing" stroke="#3b3027" stroke-linejoin="round">
  <path d="M820 447 L1780 447 L1875 518 L757 518 Z" fill="#755b40" stroke-width="4"/>
  <path d="M808 463 L1804 463 M786 485 L1835 485 M765 505 L1861 505"
        fill="none" stroke="#a1845e" stroke-opacity=".55" stroke-width="3"/>
  <g stroke-width="11">
    <path d="M878 375 L868 560"/><path d="M1240 373 L1230 559"/>
    <path d="M1604 374 L1594 558"/><path d="M1860 392 L1845 558"/>
  </g>
</g>
<g id="far_boats" fill="#4d4338" stroke="#302c28" stroke-width="4" opacity=".72">
  <path d="M405 398 Q520 423 640 395 Q598 442 460 438 Z"/>
  <path d="M2010 422 Q2084 436 2164 417 Q2138 452 2034 451 Z"/>
</g>
""",
    )


def p2_near_layer(rng: random.Random, daylight: bool) -> str:
    mud = "#6f604e" if daylight else "#5e5145"
    reeds = []
    for index in range(76):
        x = rng.randint(-30, P2_WIDTH + 30)
        base = rng.randint(646, 730)
        height = rng.randint(44, 139)
        reeds.append(
            f'<path d="M{x} {base} q{rng.randint(-16,16)} {-height//2} '
            f'{rng.randint(-18,18)} {-height}" fill="none" '
            f'stroke="{"#65705a" if index % 3 else "#77765b"}" '
            f'stroke-width="{rng.randint(2,5)}" stroke-linecap="round"/>'
        )
    return svg_document(
        P2_WIDTH,
        HEIGHT,
        f"""
<path d="M0 514 Q240 475 484 525 Q760 575 1005 521 Q1270 472 1510 526
         Q1790 581 2200 514 L2200 720 L0 720 Z" fill="{mud}"/>
<path d="M0 560 Q330 520 625 575 Q920 617 1205 560 Q1525 512 1790 570
         Q1990 607 2200 562 L2200 720 L0 720 Z" fill="#7c6a56" fill-opacity=".55"/>
<g id="home_props" stroke="#3c3129" stroke-width="4">
  <path d="M258 551 q55 -27 109 0 l-11 48 q-47 19 -88 0 Z" fill="#785d43"/>
  <path d="M274 549 q38 22 78 0" fill="none" stroke="#b79b70"/>
  <g stroke="#5f4934" stroke-width="8" stroke-linecap="round">
    <path d="M410 601 l64 -77"/><path d="M431 604 l71 -59"/><path d="M454 606 l71 -39"/>
  </g>
  <path d="M95 510 h118 v88 h-118 Z" fill="#423a33"/>
  <path d="M115 529 h78 v69" fill="none" stroke="#7e684e" stroke-width="6"/>
</g>
<g id="foreground_reeds">{''.join(reeds)}</g>
""",
    )


def p2_prop_documents() -> dict[str, str]:
    common_defs = """
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#8b6b49"/><stop offset="1" stop-color="#4b3a2e"/>
</linearGradient>
"""
    boat = svg_document(
        560,
        250,
        """
<ellipse cx="282" cy="218" rx="225" ry="18" fill="#1e2e32" fill-opacity=".25"/>
<path d="M42 118 Q281 163 520 111 Q478 221 280 224 Q88 219 42 118 Z"
      fill="url(#wood)" stroke="#302720" stroke-width="7"/>
<path d="M78 138 Q281 174 482 132 M112 165 Q282 192 449 159"
      fill="none" stroke="#b18a5d" stroke-opacity=".54" stroke-width="5"/>
<path d="M218 119 Q282 64 348 118" fill="none" stroke="#3c3128" stroke-width="12"/>
<path d="M224 111 Q281 73 340 111 L332 144 L231 144 Z"
      fill="#66503b" stroke="#352b24" stroke-width="5"/>
""",
        common_defs,
    )
    cable = svg_document(
        520,
        170,
        """
<path d="M22 35 Q244 151 497 42" fill="none" stroke="#43372d" stroke-width="18"
      stroke-linecap="round"/>
<path d="M24 31 Q246 139 495 38" fill="none" stroke="#a0835d" stroke-opacity=".62"
      stroke-width="5" stroke-linecap="round"/>
""",
    )
    merchant_boat = svg_document(
        770,
        370,
        """
<ellipse cx="395" cy="329" rx="310" ry="24" fill="#1d2d31" fill-opacity=".32"/>
<path d="M38 190 Q380 245 730 172 Q672 324 386 332 Q110 318 38 190 Z"
      fill="url(#wood)" stroke="#2f2721" stroke-width="8"/>
<path d="M92 213 Q386 264 681 201 M134 248 Q390 288 635 240"
      fill="none" stroke="#ba9160" stroke-opacity=".5" stroke-width="6"/>
<path d="M388 185 L390 30" stroke="#392f27" stroke-width="13"/>
<path d="M395 47 Q560 103 399 165 Z" fill="#9a8669" fill-opacity=".84"
      stroke="#4b4034" stroke-width="5"/>
<rect x="198" y="135" width="182" height="78" rx="8" fill="#594838"
      stroke="#302821" stroke-width="6"/>
<g fill="#876845" stroke="#3b3028" stroke-width="4">
  <rect x="486" y="171" width="63" height="54"/><rect x="555" y="178" width="66" height="47"/>
</g>
""",
        common_defs,
    )
    desk = svg_document(
        520,
        300,
        """
<ellipse cx="254" cy="277" rx="205" ry="17" fill="#1c2628" fill-opacity=".25"/>
<path d="M52 108 L470 108 L439 164 L77 164 Z" fill="url(#wood)"
      stroke="#302820" stroke-width="7"/>
<path d="M104 158 L95 279 M405 158 L418 279" stroke="#4a382b" stroke-width="17"/>
<g fill="#a17e52" stroke="#453329" stroke-width="3">
  <rect x="126" y="77" width="172" height="43" rx="4"/>
  <rect x="319" y="90" width="94" height="24" rx="3"/>
</g>
<path d="M174 91 l77 0 m-71 13 l65 0" stroke="#4c3829" stroke-width="3"/>
<path d="M350 39 L326 111" stroke="#3d2e25" stroke-width="7"/>
<path d="M351 34 l8 21" stroke="#202b33" stroke-width="7"/>
""",
        common_defs,
    )
    grain_bag = svg_document(
        210,
        230,
        """
<path d="M59 34 Q104 53 151 34 L169 190 Q105 222 40 190 Z"
      fill="#a48f6b" stroke="#44382e" stroke-width="6"/>
<path d="M56 49 Q105 65 154 48" fill="none" stroke="#6c5842" stroke-width="7"/>
<g fill="#c1a65c"><circle cx="83" cy="72" r="5"/><circle cx="104" cy="76" r="4"/>
<circle cx="126" cy="70" r="5"/><circle cx="144" cy="79" r="3"/></g>
<path d="M57 103 q47 15 95 0 M53 139 q52 16 105 0" fill="none"
      stroke="#e8e1d2" stroke-opacity=".18" stroke-width="3"/>
""",
    )
    pen_box = svg_document(
        270,
        150,
        """
<ellipse cx="135" cy="125" rx="105" ry="12" fill="#1b2426" fill-opacity=".25"/>
<rect x="26" y="42" width="218" height="75" rx="8" fill="#6d5239"
      stroke="#352a23" stroke-width="6"/>
<rect x="39" y="54" width="192" height="49" rx="5" fill="#896846"
      stroke="#49372a" stroke-width="3"/>
<path d="M61 82 L205 68" stroke="#382a23" stroke-width="7"/>
<path d="M204 67 l17 8 l-15 8" fill="#202b33"/>
""",
    )
    bowl = svg_document(
        190,
        120,
        """
<ellipse cx="95" cy="42" rx="72" ry="21" fill="#b49a70" stroke="#40342b" stroke-width="5"/>
<path d="M24 42 Q37 107 95 111 Q153 107 166 42" fill="#765b42"
      stroke="#40342b" stroke-width="5"/>
<ellipse cx="95" cy="42" rx="61" ry="14" fill="#d5c08c"/>
<path d="M48 39 q47 13 94 0" fill="none" stroke="#efe1b2" stroke-width="4"/>
""",
    )
    return {
        "wood_boat.svg": boat,
        "wood_cable.svg": cable,
        "merchant_boat.svg": merchant_boat,
        "xinheng_desk.svg": desk,
        "grain_bag.svg": grain_bag,
        "pen_box.svg": pen_box,
        "porridge_bowl.svg": bowl,
    }


def main() -> int:
    args = base_parser("Generate layered P0/P2 old-ferry SVG environments.").parse_args()
    rng = random.Random(args.seed)
    base = "assets/environments/old_ferry/p0"
    write_text(f"{base}/old_ferry_far.svg", far_layer(rng), args.force)
    write_text(f"{base}/old_ferry_mid.svg", mid_layer(rng), args.force)
    write_text(f"{base}/old_ferry_near.svg", near_layer(rng), args.force)

    contact = svg_document(
        960,
        420,
        """
<rect width="960" height="420" fill="#202b33"/>
<g transform="translate(0 30) scale(.5)">
  <image href="../../assets/environments/old_ferry/p0/old_ferry_far.svg" width="1920" height="720"/>
  <image href="../../assets/environments/old_ferry/p0/old_ferry_mid.svg" width="1920" height="720"/>
  <image href="../../assets/environments/old_ferry/p0/old_ferry_near.svg" width="1920" height="720"/>
</g>
<rect x="0" y="390" width="960" height="30" fill="#12110f"/>
<text x="24" y="412" font-family="Microsoft YaHei, sans-serif" font-size="16" fill="#e8e1d2">P0 旧渡色彩脚本：雾灰 / 洛水青灰 / 旧木 / 湿泥</text>
""",
    )
    write_text("art/reference/generated_scene_color_script.svg", contact, args.force)

    p2_base = "assets/environments/old_ferry/p2"
    morning_rng = random.Random(args.seed + 201)
    day_rng = random.Random(args.seed + 203)
    write_text(f"{p2_base}/morning_far.svg", p2_far_layer(morning_rng, False), args.force)
    write_text(f"{p2_base}/morning_mid.svg", p2_mid_layer(False), args.force)
    write_text(f"{p2_base}/morning_near.svg", p2_near_layer(morning_rng, False), args.force)
    write_text(f"{p2_base}/day_far.svg", p2_far_layer(day_rng, True), args.force)
    write_text(f"{p2_base}/day_mid.svg", p2_mid_layer(True), args.force)
    write_text(f"{p2_base}/day_near.svg", p2_near_layer(day_rng, True), args.force)
    for filename, document in p2_prop_documents().items():
        write_text(f"assets/props/p2/{filename}", document, args.force)

    p2_review = svg_document(
        1100,
        760,
        f"""
<rect width="1100" height="760" fill="#202b33"/>
<g transform="translate(0 20) scale(.5)">
  <image href="../../assets/environments/old_ferry/p2/morning_far.svg" width="{P2_WIDTH}" height="720"/>
  <image href="../../assets/environments/old_ferry/p2/morning_mid.svg" width="{P2_WIDTH}" height="720"/>
  <image href="../../assets/environments/old_ferry/p2/morning_near.svg" width="{P2_WIDTH}" height="720"/>
</g>
<g transform="translate(0 390) scale(.5)">
  <image href="../../assets/environments/old_ferry/p2/day_far.svg" width="{P2_WIDTH}" height="720"/>
  <image href="../../assets/environments/old_ferry/p2/day_mid.svg" width="{P2_WIDTH}" height="720"/>
  <image href="../../assets/environments/old_ferry/p2/day_near.svg" width="{P2_WIDTH}" height="720"/>
</g>
<text x="24" y="375" font-family="Microsoft YaHei, sans-serif" font-size="17" fill="#e8e1d2">P2 清晨：冷雾 / 旧木 / 湿泥</text>
<text x="24" y="746" font-family="Microsoft YaHei, sans-serif" font-size="17" fill="#e8e1d2">P2 午前：亮水 / 商船 / 停下的旧渡人</text>
""",
    )
    write_text("art/reference/generated_scene_color_script.svg", p2_review, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
