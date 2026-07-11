extends Node

signal save_completed(path: String)
signal save_loaded(path: String)
signal save_failed(path: String, error: Error)

const DEFAULT_SAVE_PATH := "user://save_0.json"

var last_save_path := ""


func save_game(checkpoint := "", override_path := "") -> Error:
	var path := override_path if not override_path.is_empty() else DEFAULT_SAVE_PATH
	if not checkpoint.is_empty():
		GameState.set_state_value("runtime.checkpoint", checkpoint, false)

	var settings_manager := get_node_or_null("/root/SettingsManager")
	var settings_snapshot: Dictionary = {}
	if settings_manager != null:
		settings_snapshot = settings_manager.get_settings_snapshot()

	var payload := {
		"save_version": GameState.SAVE_VERSION,
		"current_scene": GameState.get_state_value("runtime.current_scene", ""),
		"current_timeline_event": GameState.get_state_value(
			"runtime.current_timeline_event", ""
		),
		"player_name": GameState.get_state_value("player.name", ""),
		"prologue_flags": GameState.get_state_value("prologue", {}).duplicate(true),
		"first_priority": GameState.get_state_value("prologue.first_priority", ""),
		"settings": settings_snapshot,
		"playtime": GameState.get_state_value("meta.playtime", 0.0),
		"checkpoint": GameState.get_state_value("runtime.checkpoint", ""),
		"state_snapshot": GameState.get_snapshot(),
		"event_log": GameState.get_event_log_snapshot(),
		"updated_at_unix": int(Time.get_unix_time_from_system()),
	}

	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		var open_error := FileAccess.get_open_error()
		save_failed.emit(path, open_error)
		return open_error
	file.store_string(JSON.stringify(payload, "\t", false))
	file.close()
	last_save_path = path
	save_completed.emit(path)
	return OK


func load_game(override_path := "") -> Error:
	var path := override_path if not override_path.is_empty() else DEFAULT_SAVE_PATH
	var result := read_save(path)
	if not result.ok:
		save_failed.emit(path, result.error)
		return result.error

	var data: Dictionary = result.data
	GameState.restore_snapshot(data.get("state_snapshot", {}), data.get("event_log", []))
	var settings_manager := get_node_or_null("/root/SettingsManager")
	if settings_manager != null and data.get("settings", {}) is Dictionary:
		settings_manager.restore_settings(data.get("settings", {}), false)
	last_save_path = path
	save_loaded.emit(path)
	return OK


func read_save(path := DEFAULT_SAVE_PATH) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {"ok": false, "error": ERR_FILE_NOT_FOUND, "data": {}}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary:
		return {"ok": false, "error": ERR_PARSE_ERROR, "data": {}}
	if int(parsed.get("save_version", -1)) != GameState.SAVE_VERSION:
		return {"ok": false, "error": ERR_FILE_UNRECOGNIZED, "data": parsed}
	if not parsed.get("state_snapshot", {}) is Dictionary:
		return {"ok": false, "error": ERR_INVALID_DATA, "data": parsed}
	return {"ok": true, "error": OK, "data": parsed}


func has_save(path := DEFAULT_SAVE_PATH) -> bool:
	return FileAccess.file_exists(path)


func delete_save(path := DEFAULT_SAVE_PATH) -> Error:
	if not FileAccess.file_exists(path):
		return OK
	return DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
