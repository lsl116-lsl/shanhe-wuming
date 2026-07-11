extends Node

signal settings_changed(key: String, value: Variant)
signal settings_loaded(settings: Dictionary)

const SETTINGS_PATH := "user://settings.json"

const DEFAULT_SETTINGS := {
	"master_volume": 1.0,
	"music_volume": 0.72,
	"ambience_volume": 0.82,
	"sfx_volume": 1.0,
	"voice_volume": 1.0,
	"ui_volume": 0.9,
	"subtitle_speed": 1.0,
	"fullscreen": false,
	"screen_shake": true,
	"fx_quality": "medium",
}

const BUS_KEYS := {
	"master_volume": "Master",
	"music_volume": "Music",
	"ambience_volume": "Ambience",
	"sfx_volume": "SFX",
	"voice_volume": "Voice",
	"ui_volume": "UI",
}

var settings: Dictionary = DEFAULT_SETTINGS.duplicate(true)


func _ready() -> void:
	load_settings()
	call_deferred("apply_all")


func get_setting_value(key: String, fallback: Variant = null) -> Variant:
	return settings.get(key, fallback)


func set_setting_value(key: String, value: Variant, persist := true) -> void:
	if not DEFAULT_SETTINGS.has(key):
		push_warning("Ignoring unknown setting: " + key)
		return
	settings[key] = value
	_apply_setting(key, value)
	settings_changed.emit(key, value)
	if persist:
		save_settings()


func get_settings_snapshot() -> Dictionary:
	return settings.duplicate(true)


func restore_settings(snapshot: Dictionary, persist := false) -> void:
	settings = DEFAULT_SETTINGS.duplicate(true)
	for key in snapshot:
		if DEFAULT_SETTINGS.has(key):
			settings[key] = snapshot[key]
	apply_all()
	if persist:
		save_settings()


func apply_all() -> void:
	for key in settings:
		_apply_setting(key, settings[key])


func _apply_setting(key: String, value: Variant) -> void:
	if BUS_KEYS.has(key):
		var bus_index := AudioServer.get_bus_index(BUS_KEYS[key])
		if bus_index >= 0:
			var linear_value := maxf(float(value), 0.0001)
			AudioServer.set_bus_volume_db(bus_index, linear_to_db(linear_value))
		return

	if key == "fullscreen" and DisplayServer.get_name() != "headless":
		var mode := (
			DisplayServer.WINDOW_MODE_EXCLUSIVE_FULLSCREEN
			if bool(value)
			else DisplayServer.WINDOW_MODE_WINDOWED
		)
		DisplayServer.window_set_mode(mode)


func save_settings(path := SETTINGS_PATH) -> Error:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		return FileAccess.get_open_error()
	file.store_string(JSON.stringify(settings, "\t", false))
	file.close()
	return OK


func load_settings(path := SETTINGS_PATH) -> Error:
	if not FileAccess.file_exists(path):
		settings = DEFAULT_SETTINGS.duplicate(true)
		settings_loaded.emit(settings.duplicate(true))
		return OK

	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary:
		push_warning("Settings file is invalid; defaults restored.")
		settings = DEFAULT_SETTINGS.duplicate(true)
		settings_loaded.emit(settings.duplicate(true))
		return ERR_PARSE_ERROR

	restore_settings(parsed, false)
	settings_loaded.emit(settings.duplicate(true))
	return OK
