"""Generate P5 review boards for cast, actions, color script, and UI language."""

from __future__ import annotations

from asset_tools_common import base_parser, svg_document, write_text


def _text(x: int, y: int, content: str, size: int = 22, fill: str = "#e6dfcf") -> str:
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" '
        f'font-family="Microsoft YaHei, SimSun, sans-serif" fill="{fill}">{content}</text>'
    )


def _card(x: int, y: int, w: int, h: int, title: str, body: str, color: str) -> str:
    return f"""
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#171512" stroke="{color}" stroke-width="3"/>
<rect x="{x + 14}" y="{y + 14}" width="{w - 28}" height="72" rx="8" fill="{color}" fill-opacity=".22"/>
{_text(x + 28, y + 54, title, 24, "#f1dfaf")}
{_text(x + 28, y + 106, body, 17, "#cfc7b6")}
"""


def _swatch(x: int, y: int, label: str, colors: list[str]) -> str:
    rects = []
    for index, color in enumerate(colors):
        rects.append(
            f'<rect x="{x + index * 64}" y="{y}" width="58" height="86" '
            f'rx="6" fill="{color}" stroke="#211d19" stroke-width="2"/>'
        )
    return "\n".join(rects) + "\n" + _text(x, y + 118, label, 18, "#d8cfba")


def build_character_lineup() -> str:
    cards = [
        ("主角", "初醒、观察、承担", "#85745a"),
        ("母亲", "等人归来、不说满", "#7d6957"),
        ("辛衡", "笔停、递牍、怕漏名", "#8b7952"),
        ("禾安", "数米、倒粥、顶车辕", "#9b7a3e"),
        ("韩宁", "按袖口、抢湿简", "#6c7890"),
        ("柳娘", "旧曲、喊名互认", "#8b6471"),
        ("船主", "带来宋亡消息", "#795f45"),
        ("流民母子", "被追问、先活下去", "#6f6b5c"),
    ]
    body = [
        '<rect width="1600" height="900" fill="#0f1214"/>',
        _text(54, 70, "P5 人物阵容图 / Prologue Cast Lineup", 36, "#f0d48d"),
    ]
    for index, item in enumerate(cards):
        x = 54 + (index % 4) * 374
        y = 120 + (index // 4) * 310
        body.append(_card(x, y, 330, 244, item[0], item[1], item[2]))
        body.append(
            f'<ellipse cx="{x + 165}" cy="{y + 184}" rx="64" ry="34" '
            f'fill="{item[2]}" fill-opacity=".65"/>'
        )
        body.append(
            f'<path d="M{x + 130} {y + 168} q35 -72 70 0" '
            f'stroke="#d8cfba" stroke-width="6" fill="none" opacity=".72"/>'
        )
    return svg_document(1600, 900, "\n".join(body))


def build_animation_sheet() -> str:
    rows = [
        ("主角", "walk / write / choice_scan / push_lift / kneel_pickup / organize_crowd"),
        ("母亲", "wash_basin / count_grain / count_wood / look_river / resume_work"),
        ("辛衡", "write / pause_pen / hand_tablet / look_over_tablet"),
        ("禾安", "carry_firewood / place_porridge / count_jars / drag_bucket / brace_cart"),
        ("韩宁", "press_sleeve / rush_records / struggle / kneel_records"),
        ("柳娘", "song_stops / hold_child / call_names"),
    ]
    body = [
        '<rect width="1600" height="900" fill="#11100e"/>',
        _text(54, 68, "P5 动画动作表 / Animation Action Sheet", 36, "#f0d48d"),
    ]
    y = 126
    for index, (character, actions) in enumerate(rows):
        fill = "#161b1f" if index % 2 == 0 else "#171512"
        body.append(f'<rect x="54" y="{y - 36}" width="1480" height="86" rx="8" fill="{fill}" stroke="#3f3428"/>')
        body.append(_text(82, y, character, 24, "#f1dfaf"))
        body.append(_text(250, y, actions, 20, "#d8cfba"))
        y += 104
    body.append(_text(82, 812, "验收重点：动作不替代选择菜单；动作先让玩家看见代价，再让按住 E 承担。", 24, "#d2b276"))
    return svg_document(1600, 900, "\n".join(body))


def build_color_script() -> str:
    body = [
        '<rect width="1600" height="900" fill="#101316"/>',
        _text(54, 68, "P5 场景色彩脚本 / Scene Color Script", 36, "#f0d48d"),
        _swatch(76, 134, "SC01 清晨旧渡：雾蓝、湿木、粟米灰", ["#9fb5b5", "#51696d", "#2d3a3b", "#b69a61"]),
        _swatch(76, 340, "SC03 午前消息：河雾退、土色显、船声近", ["#b9b07d", "#7d876d", "#4a5d60", "#9c744e"]),
        _swatch(76, 546, "SC04 傍晚转夜：棚火、泥灰、雨意", ["#5f6268", "#2b3540", "#9a6f3e", "#1d2024"]),
        _swatch(780, 134, "SC05 礼器库：青铜暗绿、裂纹冷光", ["#24302f", "#4f665e", "#87917e", "#c0a56a"]),
        _swatch(780, 340, "SC06 雨夜翻车：黑雨、火把、湿简墨色", ["#111820", "#263443", "#c16f3d", "#5b4a35"]),
        _swatch(780, 546, "SC07 第一章标题：雨后余冷、礼崩金褐", ["#14191d", "#3c4a51", "#8b7143", "#d2b276"]),
    ]
    return svg_document(1600, 900, "\n".join(body))


def build_ui_board() -> str:
    body = [
        '<rect width="1600" height="900" fill="#11100e"/>',
        _text(54, 68, "P5 UI 图板 / UI Board", 36, "#f0d48d"),
        '<rect x="82" y="126" width="620" height="210" rx="12" fill="#171512" stroke="#806846" stroke-width="3"/>',
        _text(112, 178, "字幕 / 对话层", 30, "#f1dfaf"),
        _text(112, 224, "低透明黑底，金褐边，中文字体回退；字幕速度受设置控制。", 21, "#d8cfba"),
        '<rect x="82" y="396" width="620" height="210" rx="12" fill="#171512" stroke="#806846" stroke-width="3"/>',
        _text(112, 448, "按住 E 交互", 30, "#f1dfaf"),
        _text(112, 494, "靠近只展示信息，环形进度确认承担；不用 A/B/C 菜单。", 21, "#d8cfba"),
        '<rect x="860" y="126" width="620" height="210" rx="12" fill="#171512" stroke="#806846" stroke-width="3"/>',
        _text(890, 178, "暂停 / 设置", 30, "#f1dfaf"),
        _text(890, 224, "Master、Music、Ambience、SFX、Voice、UI 与全屏/震动。", 21, "#d8cfba"),
        '<rect x="860" y="396" width="620" height="210" rx="12" fill="#171512" stroke="#806846" stroke-width="3"/>',
        _text(890, 448, "章节结束回顾", 30, "#f1dfaf"),
        _text(890, 494, "从 JSON 读取路线回顾，显示第一选择如何进入第一章。", 21, "#d8cfba"),
        _text(82, 760, "UI 原则：移动负责让玩家看见；互动负责让玩家承担。", 28, "#d2b276"),
    ]
    return svg_document(1600, 900, "\n".join(body))


def main() -> int:
    args = base_parser("Generate P5 review boards.").parse_args()
    write_text("art/reference/generated_p5_character_lineup.svg", build_character_lineup(), args.force)
    write_text("art/reference/generated_p5_animation_action_sheet.svg", build_animation_sheet(), args.force)
    write_text("art/reference/generated_p5_scene_color_script.svg", build_color_script(), args.force)
    write_text("art/reference/generated_p5_ui_board.svg", build_ui_board(), args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
