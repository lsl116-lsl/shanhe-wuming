class_name ChoicePressureController
extends Node

signal pressure_started
signal preview_changed(choice_id: String)
signal preview_cleared(choice_id: String)
signal choice_locked(choice_id: String, elapsed_seconds: float)

@onready var title_label: Label = get_node_or_null("../HUD/PressurePanel/Margin/VBox/ChoiceTitle") as Label
@onready var detail_label: Label = get_node_or_null("../HUD/PressurePanel/Margin/VBox/ChoiceDetail") as Label
@onready var clock_label: Label = get_node_or_null("../HUD/PressurePanel/Margin/VBox/ChoiceClock") as Label

var _config: Dictionary = {}
var _running := false
var _locked := false
var _elapsed := 0.0
var _preview_id := ""
var _threshold_index := -1


func start(config: Dictionary) -> void:
	_config = config.duplicate(true)
	_running = true
	_locked = false
	_elapsed = 0.0
	_preview_id = ""
	_threshold_index = -1
	_set_labels(
		str(_config.get("initial_title", "先靠近看清，按住互动键才会承担。")),
		str(_config.get("initial_detail", "")),
		"观察时间：0.0 秒。前几秒只展示现场，不暗扣后果。"
	)
	GameState.record_event("choice_pressure_started", {})
	pressure_started.emit()


func _process(delta: float) -> void:
	if not _running or _locked:
		return
	_elapsed += delta
	_update_threshold()
	_update_clock()


func preview_choice(choice_id: String, payload: Dictionary) -> void:
	if not _running or _locked or choice_id.is_empty():
		return
	_preview_id = choice_id
	var title := str(payload.get("preview_title", ""))
	var detail := str(payload.get("preview_detail", ""))
	var costs := _string_array(payload.get("preview_costs", []))
	var directions: Dictionary = _config.get("directions", {})
	if directions.has(choice_id) and directions[choice_id] is Dictionary:
		var direction: Dictionary = directions[choice_id]
		if title.is_empty():
			title = str(direction.get("title", ""))
		if detail.is_empty():
			detail = str(direction.get("detail", ""))
		if costs.is_empty():
			costs = _string_array(direction.get("costs", []))
	if not costs.is_empty():
		detail = "%s\n眼前代价：%s" % [detail, "；".join(costs)]
	_set_labels(title, detail, _clock_text())
	GameState.record_event(
		"choice_previewed",
		{
			"choice_id": choice_id,
			"elapsed_seconds": get_elapsed_seconds(),
		}
	)
	preview_changed.emit(choice_id)


func clear_preview(choice_id: String) -> void:
	if not _running or _locked:
		return
	if not choice_id.is_empty() and _preview_id != choice_id:
		return
	_preview_id = ""
	_set_labels(
		str(_config.get("initial_title", "先靠近看清，按住互动键才会承担。")),
		str(_config.get("initial_detail", "")),
		_clock_text()
	)
	preview_cleared.emit(choice_id)


func lock_choice(choice_id: String) -> void:
	if not _running or _locked:
		return
	_locked = true
	_preview_id = choice_id
	_set_labels(
		"已经承担：%s" % choice_id,
		"行动已经锁定，其他方向会由旁人继续处理，但先后不同，现场代价不同。",
		_clock_text()
	)
	GameState.record_event(
		"choice_locked",
		{
			"choice_id": choice_id,
			"elapsed_seconds": get_elapsed_seconds(),
		}
	)
	choice_locked.emit(choice_id, get_elapsed_seconds())


func get_elapsed_seconds() -> float:
	return snappedf(_elapsed, 0.001)


func is_locked() -> bool:
	return _locked


func _update_threshold() -> void:
	var thresholds: Array = _config.get("thresholds", [])
	for index in range(thresholds.size()):
		var threshold: Variant = thresholds[index]
		if not threshold is Dictionary:
			continue
		if index <= _threshold_index:
			continue
		if _elapsed >= float(threshold.get("seconds", 0.0)):
			_threshold_index = index
			GameState.record_event(
				"choice_pressure_threshold",
				{
					"seconds": float(threshold.get("seconds", 0.0)),
					"text": str(threshold.get("text", "")),
				}
			)


func _update_clock() -> void:
	if clock_label != null:
		clock_label.text = _clock_text()


func _clock_text() -> String:
	var threshold_text := ""
	var thresholds: Array = _config.get("thresholds", [])
	if _threshold_index >= 0 and _threshold_index < thresholds.size():
		var threshold: Variant = thresholds[_threshold_index]
		if threshold is Dictionary:
			threshold_text = str(threshold.get("text", ""))
	var prefix := "观察时间：%.1f 秒" % _elapsed
	if threshold_text.is_empty():
		return prefix + "。移动只让你看见，按住 E 才会锁定。"
	return "%s。%s" % [prefix, threshold_text]


func _set_labels(title: String, detail: String, clock: String) -> void:
	if title_label != null:
		title_label.text = title
	if detail_label != null:
		detail_label.text = detail
	if clock_label != null:
		clock_label.text = clock


func _string_array(value: Variant) -> Array[String]:
	var result: Array[String] = []
	if value is Array:
		for item in value:
			result.append(str(item))
	return result
