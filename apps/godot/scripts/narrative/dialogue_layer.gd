class_name DialogueLayer
extends CanvasLayer

signal dialogue_file_loaded(path: String)
signal line_started(line_id: String, speaker: String, text: String)
signal line_finished(line_id: String)
signal advance_requested

@onready var panel: PanelContainer = %DialoguePanel
@onready var speaker_label: Label = %SpeakerLabel
@onready var text_label: Label = %TextLabel
@onready var continue_label: Label = %ContinueLabel

var _lines: Dictionary = {}
var _waiting_for_advance := false


func _ready() -> void:
	panel.visible = false


func _unhandled_input(event: InputEvent) -> void:
	if _waiting_for_advance and event.is_action_pressed("advance_dialogue"):
		_waiting_for_advance = false
		advance_requested.emit()
		get_viewport().set_input_as_handled()


func load_dialogue_file(path: String) -> Error:
	if not FileAccess.file_exists(path):
		push_error("Dialogue JSON not found: " + path)
		return ERR_FILE_NOT_FOUND
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary or not parsed.get("lines", {}) is Dictionary:
		push_error("Dialogue JSON is invalid: " + path)
		return ERR_PARSE_ERROR
	_lines = parsed.get("lines", {}).duplicate(true)
	dialogue_file_loaded.emit(path)
	return OK


func has_line(line_id: String) -> bool:
	return _lines.has(line_id)


func show_line(
	line_id: String,
	substitutions: Dictionary = {},
	wait_for_input := true,
	auto_duration := 0.0
) -> Error:
	if not _lines.has(line_id):
		push_error("Dialogue line ID not found: " + line_id)
		return ERR_DOES_NOT_EXIST
	var line: Dictionary = _lines[line_id]
	var speaker := str(line.get("speaker", ""))
	var text := str(line.get("text", "")).format(substitutions)
	speaker_label.text = speaker
	speaker_label.visible = not speaker.is_empty()
	text_label.text = text
	continue_label.visible = wait_for_input
	panel.visible = true
	line_started.emit(line_id, speaker, text)

	if wait_for_input:
		_waiting_for_advance = true
		await advance_requested
	elif auto_duration > 0.0:
		var settings_manager := get_node_or_null("/root/SettingsManager")
		var subtitle_speed := 1.0
		if settings_manager != null:
			subtitle_speed = maxf(
				float(settings_manager.get_setting_value("subtitle_speed", 1.0)),
				0.2
			)
		await get_tree().create_timer(auto_duration / subtitle_speed).timeout
	else:
		await get_tree().process_frame

	_waiting_for_advance = false
	continue_label.visible = false
	line_finished.emit(line_id)
	return OK


func hide_dialogue() -> void:
	_waiting_for_advance = false
	panel.visible = false
