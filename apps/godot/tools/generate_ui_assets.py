"""Generate title, dialogue, interaction, and P2 writing UI vectors."""

from __future__ import annotations

from asset_tools_common import base_parser, svg_document, write_text


def main() -> int:
    args = base_parser("Generate P0/P2 UI SVG assets.").parse_args()
    title_seal = svg_document(
        96,
        96,
        """
<rect x="8" y="8" width="80" height="80" rx="7" fill="#713f36" stroke="#2d2925" stroke-width="5"/>
<path d="M27 25 H69 V36 H43 V47 H68 V70 H27 V59 H53 V52 H28 Z" fill="#e8e1d2" fill-opacity=".9"/>
<path d="M17 16 H79 V80 H17 Z" fill="none" stroke="#c2a45a" stroke-width="2" stroke-dasharray="3 5" opacity=".75"/>
""",
    )
    button_frame = svg_document(
        480,
        80,
        """
<rect x="5" y="5" width="470" height="70" rx="7" fill="#302a23" fill-opacity=".94" stroke="#8c7046" stroke-width="3"/>
<path d="M20 18 H460 M20 62 H460" stroke="#b28a4a" stroke-opacity=".35" stroke-width="2"/>
<circle cx="21" cy="40" r="4" fill="#6d5a42"/><circle cx="459" cy="40" r="4" fill="#6d5a42"/>
""",
    )
    subtitle_panel = svg_document(
        1100,
        128,
        """
<rect x="8" y="8" width="1084" height="112" rx="9" fill="#12110f" fill-opacity=".88" stroke="#6b513d" stroke-width="3"/>
<path d="M26 25 H1074 M26 103 H1074" stroke="#b28a4a" stroke-opacity=".25" stroke-width="2"/>
<path d="M34 17 L49 32 M1066 17 L1051 32 M34 111 L49 96 M1066 111 L1051 96" stroke="#b28a4a" stroke-width="2"/>
""",
    )
    write_text("assets/ui/p0/title_seal.svg", title_seal, args.force)
    write_text("assets/ui/p0/button_frame.svg", button_frame, args.force)
    write_text("assets/ui/p0/subtitle_panel.svg", subtitle_panel, args.force)
    name_panel = svg_document(
        760,
        390,
        """
<rect x="10" y="10" width="740" height="370" rx="12" fill="#171512"
      fill-opacity=".96" stroke="#806846" stroke-width="4"/>
<rect x="31" y="31" width="698" height="328" rx="8" fill="#d8cfba"
      fill-opacity=".08" stroke="#b28a4a" stroke-opacity=".35" stroke-width="2"/>
<path d="M55 82 H705 M55 305 H705" stroke="#8c7046" stroke-opacity=".35" stroke-width="2"/>
<circle cx="49" cy="49" r="5" fill="#6d5a42"/><circle cx="711" cy="49" r="5" fill="#6d5a42"/>
<circle cx="49" cy="341" r="5" fill="#6d5a42"/><circle cx="711" cy="341" r="5" fill="#6d5a42"/>
""",
    )
    objective_panel = svg_document(
        520,
        72,
        """
<path d="M8 8 H500 L512 36 L500 64 H8 L20 36 Z" fill="#171512"
      fill-opacity=".88" stroke="#806846" stroke-width="2"/>
<path d="M34 22 H486 M34 50 H486" stroke="#b28a4a" stroke-opacity=".25"/>
""",
    )
    write_text("assets/ui/p2/name_input_panel.svg", name_panel, args.force)
    write_text("assets/ui/p2/objective_panel.svg", objective_panel, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
