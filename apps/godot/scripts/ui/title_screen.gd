extends Control

const FALLBACK_NEW_GAME_SCENE := "res://scenes/prologue/SC01_OldFerry_Test.tscn"
const TIMELINE_PATH := "res://content/prologue/timeline.json"
const ASSET_MANIFEST_PATH := "res://content/prologue/asset_manifest.json"
const SAVE_PATH := "user://save_0.json"
const BUS_SETTING_KEYS := {
	"Master": "master_volume",
	"Music": "music_volume",
	"Ambience": "ambience_volume",
	"SFX": "sfx_volume",
	"Voice": "voice_volume",
	"UI": "ui_volume",
}

@onready var new_game_button: Button = %NewGameButton
@onready var continue_button: Button = %ContinueButton
@onready var settings_button: Button = %SettingsButton
@onready var exit_button: Button = %ExitButton
@onready var settings_panel: PanelContainer = %SettingsPanel
@onready var status_label: Label = %StatusLabel
@onready var ui_audio: AudioStreamPlayer = %UIAudio
@onready var river_ambience: AudioStreamPlayer = $RiverAmbience


func _ready() -> void:
	SceneRouter.register_current_scene(scene_file_path)
	GameState.set_player_control(false)
	new_game_button.pressed.connect(_on_new_game_pressed)
	continue_button.pressed.connect(_on_continue_pressed)
	settings_button.pressed.connect(_on_settings_pressed)
	exit_button.pressed.connect(_on_exit_pressed)
	%CloseSettingsButton.pressed.connect(_on_close_settings_pressed)
	%MasterSlider.value_changed.connect(_on_bus_slider_changed.bind("Master"))
	%MusicSlider.value_changed.connect(_on_bus_slider_changed.bind("Music"))
	%AmbienceSlider.value_changed.connect(_on_bus_slider_changed.bind("Ambience"))
	%SFXSlider.value_changed.connect(_on_bus_slider_changed.bind("SFX"))
	%VoiceSlider.value_changed.connect(_on_bus_slider_changed.bind("Voice"))
	%UISlider.value_changed.connect(_on_bus_slider_changed.bind("UI"))
	%SubtitleSpeedSlider.value_changed.connect(_on_subtitle_speed_changed)
	%FullscreenCheck.toggled.connect(_on_fullscreen_toggled)
	%ScreenShakeCheck.toggled.connect(_on_screen_shake_toggled)
	_initialize_slider(%MasterSlider, "Master")
	_initialize_slider(%MusicSlider, "Music")
	_initialize_slider(%AmbienceSlider, "Ambience")
	_initialize_slider(%SFXSlider, "SFX")
	_initialize_slider(%VoiceSlider, "Voice")
	_initialize_slider(%UISlider, "UI")
	_initialize_non_bus_settings()
	river_ambience.finished.connect(river_ambience.play)
	if DisplayServer.get_name() != "headless":
		river_ambience.play()
	new_game_button.grab_focus()
	if OS.get_cmdline_user_args().has("--p2-e2e"):
		_start_p2_test_driver.call_deferred()
	if OS.get_cmdline_user_args().has("--p3-e2e"):
		_start_p3_test_driver.call_deferred()
	if OS.get_cmdline_user_args().has("--p4-e2e"):
		_start_p4_test_driver.call_deferred()
	if (
		OS.get_cmdline_user_args().has("--p5-e2e")
		and get_tree().root.get_node_or_null("P5FullPrologueDriver") == null
	):
		_start_p5_test_driver.call_deferred()
	if OS.get_cmdline_user_args().has("--p0-review"):
		_finish_review_capture.call_deferred()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause_game") and settings_panel.visible:
		_on_close_settings_pressed()
		get_viewport().set_input_as_handled()


func _exit_tree() -> void:
	if is_instance_valid(river_ambience):
		river_ambience.stop()
		river_ambience.stream = null
	if is_instance_valid(ui_audio):
		ui_audio.stop()
		ui_audio.stream = null


func _finish_review_capture() -> void:
	await get_tree().process_frame
	await get_tree().process_frame
	river_ambience.stop()
	river_ambience.stream = null
	ui_audio.stream = null
	await get_tree().process_frame
	get_tree().quit(0)


func _initialize_slider(slider: HSlider, bus_name: String) -> void:
	if not BUS_SETTING_KEYS.has(bus_name):
		return
	var value := float(SettingsManager.get_setting_value(BUS_SETTING_KEYS[bus_name], 1.0))
	slider.set_value_no_signal(value * 100.0)


func _initialize_non_bus_settings() -> void:
	%SubtitleSpeedSlider.set_value_no_signal(
		float(SettingsManager.get_setting_value("subtitle_speed", 1.0)) * 100.0
	)
	%FullscreenCheck.set_pressed_no_signal(
		bool(SettingsManager.get_setting_value("fullscreen", false))
	)
	%ScreenShakeCheck.set_pressed_no_signal(
		bool(SettingsManager.get_setting_value("screen_shake", true))
	)


func _play_ui_confirm() -> void:
	if ui_audio.stream != null:
		ui_audio.play()


func _on_new_game_pressed() -> void:
	_play_ui_confirm()
	status_label.text = "河雾渐开……"
	GameState.reset_state()
	SaveManager.delete_save(
		"user://p2_end_to_end_test_save.json"
		if OS.get_cmdline_user_args().has("--p2-e2e")
		else SAVE_PATH
	)
	await get_tree().create_timer(0.08).timeout
	SceneRouter.go_to_scene(_resolve_new_game_scene())


func _on_continue_pressed() -> void:
	_play_ui_confirm()
	if SaveManager.has_save(SAVE_PATH):
		status_label.text = "正在读取最近的旧渡记录……"
		var error := SaveManager.load_game(SAVE_PATH)
		if error != OK:
			status_label.text = "存档读取失败。"
			return
		var target_scene := str(
			GameState.get_state_value("runtime.current_scene", _resolve_new_game_scene())
		)
		SceneRouter.go_to_scene(target_scene)
	else:
		status_label.text = "还没有可继续的旧渡记录。"


func _on_settings_pressed() -> void:
	_play_ui_confirm()
	settings_panel.visible = true
	%MasterSlider.grab_focus()


func _on_close_settings_pressed() -> void:
	_play_ui_confirm()
	settings_panel.visible = false
	settings_button.grab_focus()


func _on_exit_pressed() -> void:
	_play_ui_confirm()
	await get_tree().create_timer(0.08).timeout
	get_tree().quit()


func _on_bus_slider_changed(value: float, bus_name: String) -> void:
	if not BUS_SETTING_KEYS.has(bus_name):
		return
	SettingsManager.set_setting_value(BUS_SETTING_KEYS[bus_name], value / 100.0)


func _on_subtitle_speed_changed(value: float) -> void:
	SettingsManager.set_setting_value("subtitle_speed", value / 100.0)


func _on_fullscreen_toggled(enabled: bool) -> void:
	SettingsManager.set_setting_value("fullscreen", enabled)


func _on_screen_shake_toggled(enabled: bool) -> void:
	SettingsManager.set_setting_value("screen_shake", enabled)


func _resolve_new_game_scene() -> String:
	if not FileAccess.file_exists(TIMELINE_PATH) or not FileAccess.file_exists(ASSET_MANIFEST_PATH):
		return FALLBACK_NEW_GAME_SCENE
	var timeline: Variant = JSON.parse_string(FileAccess.get_file_as_string(TIMELINE_PATH))
	var manifest: Variant = JSON.parse_string(FileAccess.get_file_as_string(ASSET_MANIFEST_PATH))
	if not timeline is Dictionary or not manifest is Dictionary:
		return FALLBACK_NEW_GAME_SCENE
	var asset_id := str(timeline.get("start_scene_asset_id", ""))
	var runtime_assets: Variant = manifest.get("runtime_assets", {})
	if runtime_assets is Dictionary and runtime_assets.get(asset_id, "") is String:
		var resolved := str(runtime_assets.get(asset_id, ""))
		if ResourceLoader.exists(resolved):
			return resolved
	return FALLBACK_NEW_GAME_SCENE


func _start_p2_test_driver() -> void:
	var driver_script := load("res://tests/p2_end_to_end.gd") as Script
	if driver_script == null:
		push_error("P2 end-to-end driver could not be loaded.")
		get_tree().quit(51)
		return
	var driver := Node.new()
	driver.set_script(driver_script)
	driver.name = "P2EndToEndDriver"
	get_tree().root.add_child(driver)
	driver.call("start", self)


func _start_p3_test_driver() -> void:
	var driver_script := load("res://tests/p3_end_to_end.gd") as Script
	if driver_script == null:
		push_error("P3 end-to-end driver could not be loaded.")
		get_tree().quit(52)
		return
	var driver := Node.new()
	driver.set_script(driver_script)
	driver.name = "P3EndToEndDriver"
	get_tree().root.add_child(driver)
	driver.call("start")


func _start_p4_test_driver() -> void:
	var driver_script := load("res://tests/p4_choice_routes.gd") as Script
	if driver_script == null:
		push_error("P4 choice-route driver could not be loaded.")
		get_tree().quit(53)
		return
	var driver := Node.new()
	driver.set_script(driver_script)
	driver.name = "P4ChoiceRoutesDriver"
	get_tree().root.add_child(driver)
	driver.call("start")


func _start_p5_test_driver() -> void:
	var driver_script := load("res://tests/p5_full_prologue_flow.gd") as Script
	if driver_script == null:
		push_error("P5 full-prologue driver could not be loaded.")
		get_tree().quit(54)
		return
	var driver := Node.new()
	driver.set_script(driver_script)
	if not driver.has_method("start"):
		push_error("P5 full-prologue driver does not expose start().")
		driver.queue_free()
		get_tree().quit(55)
		return
	driver.name = "P5FullPrologueDriver"
	get_tree().root.add_child(driver)
	driver.call("start", self)
