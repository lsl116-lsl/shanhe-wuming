extends Node

signal state_changed(path: String, value: Variant)
signal event_recorded(entry: Dictionary)
signal state_reset
signal state_restored

const SAVE_VERSION := 1

var state: Dictionary = {}
var event_log: Array[Dictionary] = []


func _ready() -> void:
	if state.is_empty():
		reset_state()


func reset_state() -> void:
	state = {
		"player": {
			"name": "",
			"can_move": false,
		},
		"prologue": {
			"p1_interacted": false,
			"inspected_grain": false,
			"inspected_pen_box": false,
			"looked_downriver": false,
			"spoke_to_mother": false,
			"name_written": false,
			"name_memory_seen": false,
			"hean_arrived": false,
			"porridge_placed": false,
			"song_land_news_heard": false,
			"heard_boat_owner_fragment": false,
			"heard_hean_fragment": false,
			"heard_xinheng_fragment": false,
			"heard_ferry_people_fragment": false,
			"refugees_expected": false,
			"first_refugees_arrived": false,
			"saw_hanning_sleeve": false,
			"hanning_mother_blocked_question": false,
			"saw_xinheng_pen_pause": false,
			"heard_liuniang_song_stop": false,
			"inspected_temporary_registry": false,
			"hean_poured_broken_rice": false,
			"shelter_night_fallen": false,
			"rain_intensified": false,
			"heard_cracked_bell_lure": false,
			"followed_bell_to_storehouse": false,
			"entered_ritual_storehouse": false,
			"inspected_broken_ding": false,
			"inspected_chipped_gui": false,
			"inspected_damaged_qing": false,
			"cracked_bell_contact_started": false,
			"touched_cracked_bell": false,
			"cracked_bell_memory_completed": false,
			"first_priority": "",
			"choice_elapsed_seconds": 0.0,
			"saw_child_cost": false,
			"saw_record_cost": false,
			"saw_recognition_cost": false,
			"cart_crash_seen": false,
			"cart_scan_completed": false,
			"cart_choice_locked": false,
			"cart_choice_feedback_completed": false,
			"rescue_child_feedback_seen": false,
			"save_records_feedback_seen": false,
			"mutual_recognition_feedback_seen": false,
			"completed": false,
			"chapter_title_reached": false,
		},
		"runtime": {
			"current_scene": "",
			"current_timeline": "",
			"current_timeline_event": "",
			"checkpoint": "",
		},
		"meta": {
			"save_version": SAVE_VERSION,
			"playtime": 0.0,
		},
	}
	event_log.clear()
	state_reset.emit()


func set_state_value(path: String, value: Variant, record_change := true) -> void:
	var keys := path.split(".", false)
	if keys.is_empty():
		push_error("GameState cannot write an empty state path.")
		return

	var cursor: Dictionary = state
	for index in range(keys.size() - 1):
		var key := keys[index]
		if not cursor.has(key) or not cursor[key] is Dictionary:
			cursor[key] = {}
		cursor = cursor[key]
	cursor[keys[-1]] = value
	state_changed.emit(path, value)

	if record_change:
		record_event("state_changed", {"path": path, "value": value})


func get_state_value(path: String, fallback: Variant = null) -> Variant:
	var keys := path.split(".", false)
	if keys.is_empty():
		return fallback

	var cursor: Variant = state
	for key in keys:
		if not cursor is Dictionary or not cursor.has(key):
			return fallback
		cursor = cursor[key]
	return cursor


func set_player_control(enabled: bool) -> void:
	set_state_value("player.can_move", enabled)


func get_snapshot() -> Dictionary:
	return state.duplicate(true)


func restore_snapshot(snapshot: Dictionary, restored_events: Array = []) -> void:
	state = snapshot.duplicate(true)
	event_log.clear()
	for entry in restored_events:
		if entry is Dictionary:
			event_log.append(entry.duplicate(true))
	state_restored.emit()


func record_event(event_type: String, payload: Dictionary = {}) -> Dictionary:
	var entry := {
		"index": event_log.size(),
		"type": event_type,
		"payload": payload.duplicate(true),
		"ticks_msec": Time.get_ticks_msec(),
	}
	event_log.append(entry)
	event_recorded.emit(entry)
	return entry


func get_event_log_snapshot() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for entry in event_log:
		result.append(entry.duplicate(true))
	return result
