extends CanvasLayer

const TITLE_SCENE := "res://scenes/ui/TitleScreen.tscn"
const BUS_SETTINGS := {
	"Master": "master_volume",
	"Music": "music_volume",
	"Ambience": "ambience_volume",
	"SFX": "sfx_volume",
	"Voice": "voice_volume",
	"UI": "ui_volume",
}

var _root: Control
var _panel: PanelContainer
var _settings_box: VBoxContainer
var _resume_button: Button
var _title_button: Button


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	layer = 90
	_build_ui()
	_refresh_values()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause_game") and not _is_title_scene():
		_toggle_pause()
		get_viewport().set_input_as_handled()


func _build_ui() -> void:
	_root = Control.new()
	_root.name = "PauseMenuRoot"
	_root.visible = false
	_root.process_mode = Node.PROCESS_MODE_ALWAYS
	_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(_root)

	var shade := ColorRect.new()
	shade.name = "PauseShade"
	shade.color = Color(0.02, 0.025, 0.028, 0.68)
	shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root.add_child(shade)

	_panel = PanelContainer.new()
	_panel.name = "PausePanel"
	_panel.process_mode = Node.PROCESS_MODE_ALWAYS
	_panel.set_anchors_preset(Control.PRESET_CENTER)
	_panel.size = Vector2(560, 610)
	_panel.position = Vector2(360, 54)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.075, 0.078, 0.072, 0.97)
	style.border_color = Color(0.54, 0.42, 0.26, 1.0)
	style.set_border_width_all(2)
	style.set_corner_radius_all(6)
	_panel.add_theme_stylebox_override("panel", style)
	_root.add_child(_panel)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 38)
	margin.add_theme_constant_override("margin_top", 30)
	margin.add_theme_constant_override("margin_right", 38)
	margin.add_theme_constant_override("margin_bottom", 30)
	_panel.add_child(margin)

	_settings_box = VBoxContainer.new()
	_settings_box.name = "PauseSettings"
	_settings_box.add_theme_constant_override("separation", 8)
	margin.add_child(_settings_box)

	var title := Label.new()
	title.text = "暂停"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 30)
	_settings_box.add_child(title)

	for bus_name in BUS_SETTINGS:
		_add_slider("%s 音量" % bus_name, BUS_SETTINGS[bus_name], 0, 100, 1)

	_add_slider("字幕速度", "subtitle_speed", 50, 200, 1, 100.0)
	_add_toggle("全屏", "fullscreen")
	_add_toggle("镜头震动", "screen_shake")

	var button_row := HBoxContainer.new()
	button_row.name = "PauseButtonRow"
	button_row.add_theme_constant_override("separation", 12)
	_settings_box.add_child(button_row)

	_resume_button = Button.new()
	_resume_button.text = "继续"
	_resume_button.custom_minimum_size = Vector2(0, 46)
	_resume_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_resume_button.pressed.connect(_close_pause)
	button_row.add_child(_resume_button)

	_title_button = Button.new()
	_title_button.text = "回到标题"
	_title_button.custom_minimum_size = Vector2(0, 46)
	_title_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_title_button.pressed.connect(_return_to_title)
	button_row.add_child(_title_button)


func _add_slider(
	label_text: String,
	setting_key: String,
	min_value: float,
	max_value: float,
	step: float,
	scale := 100.0
) -> void:
	var label := Label.new()
	label.text = label_text
	label.add_theme_font_size_override("font_size", 16)
	_settings_box.add_child(label)

	var slider := HSlider.new()
	slider.name = "%sSlider" % setting_key.to_pascal_case()
	slider.min_value = min_value
	slider.max_value = max_value
	slider.step = step
	slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	slider.value_changed.connect(_on_slider_changed.bind(setting_key, scale))
	_settings_box.add_child(slider)


func _add_toggle(label_text: String, setting_key: String) -> void:
	var check := CheckButton.new()
	check.name = "%sCheck" % setting_key.to_pascal_case()
	check.text = label_text
	check.toggled.connect(_on_toggle_changed.bind(setting_key))
	_settings_box.add_child(check)


func _refresh_values() -> void:
	for bus_name in BUS_SETTINGS:
		var key := str(BUS_SETTINGS[bus_name])
		var slider := _settings_box.find_child("%sSlider" % key.to_pascal_case(), true, false) as HSlider
		if slider != null:
			slider.set_value_no_signal(float(SettingsManager.get_setting_value(key, 1.0)) * 100.0)
	var subtitle_slider := _settings_box.find_child(
		"%sSlider" % "subtitle_speed".to_pascal_case(),
		true,
		false
	) as HSlider
	if subtitle_slider != null:
		subtitle_slider.set_value_no_signal(
			float(SettingsManager.get_setting_value("subtitle_speed", 1.0)) * 100.0
		)
	for key_value in ["fullscreen", "screen_shake"]:
		var key := str(key_value)
		var check := _settings_box.find_child("%sCheck" % key.to_pascal_case(), true, false) as CheckButton
		if check != null:
			check.set_pressed_no_signal(bool(SettingsManager.get_setting_value(key, false)))


func _on_slider_changed(value: float, setting_key: String, scale: float) -> void:
	SettingsManager.set_setting_value(setting_key, value / scale)


func _on_toggle_changed(enabled: bool, setting_key: String) -> void:
	SettingsManager.set_setting_value(setting_key, enabled)


func _toggle_pause() -> void:
	if get_tree().paused:
		_close_pause()
	else:
		_open_pause()


func _open_pause() -> void:
	_refresh_values()
	_root.visible = true
	get_tree().paused = true
	_resume_button.grab_focus()


func _close_pause() -> void:
	_root.visible = false
	get_tree().paused = false


func _return_to_title() -> void:
	SaveManager.save_game("pause_menu_return")
	_close_pause()
	SceneRouter.go_to_scene(TITLE_SCENE)


func _is_title_scene() -> bool:
	var scene := get_tree().current_scene
	return scene != null and scene.scene_file_path == TITLE_SCENE
