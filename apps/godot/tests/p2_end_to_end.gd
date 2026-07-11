extends Node

const TEST_NAME := "洛川无名"
const TEST_SAVE_PATH := "user://p2_end_to_end_test_save.json"
const STAGE_TIMEOUT_SECONDS := 12.0

var _failed := false


func start(title_screen: Control) -> void:
	_run.call_deferred(title_screen)


func _run(title_screen: Control) -> void:
	await get_tree().process_frame
	var new_game_button := title_screen.find_child("NewGameButton", true, false) as Button
	if new_game_button == null:
		_fail("title screen has no NewGameButton")
		return
	new_game_button.pressed.emit()

	var morning := await _wait_for_stage("SC01_Home_Morning")
	if morning == null:
		return
	for interaction_id in [
		"morning.grain",
		"morning.pen_box",
		"morning.river",
		"morning.mother",
	]:
		if not await _perform_interaction(morning, interaction_id, 0.12):
			return
	if not await _perform_interaction(morning, "morning.to_xinheng", 0.12, false):
		return

	var desk := await _wait_for_stage("SC02_Xinheng_Desk")
	if desk == null:
		return
	if not await _perform_interaction(desk, "desk.write_name", 1.35):
		return
	var name_input := get_tree().current_scene.find_child("NameInputLayer", true, false) as NameInputLayer
	if name_input == null:
		_fail("SC02 has no NameInputLayer")
		return
	var input_deadline := Time.get_ticks_msec() + 3000
	while not name_input.panel.visible and Time.get_ticks_msec() < input_deadline:
		await get_tree().process_frame
	if not name_input.panel.visible:
		_fail("hold-E writing did not open name input")
		return
	var submit_error := name_input.submit_name(TEST_NAME)
	if submit_error != OK:
		_fail("Chinese name input was rejected: %s" % error_string(submit_error))
		return

	var ferry_day := await _wait_for_stage("SC03_Ferry_Day")
	if ferry_day == null:
		return
	for interaction_id in [
		"news.boat_owner",
		"news.hean",
		"news.xinheng",
		"news.ferry_people",
	]:
		if not await _perform_interaction(ferry_day, interaction_id, 0.12):
			return

	if not _assert_state("player.name", TEST_NAME):
		return
	for state_path in [
		"prologue.inspected_grain",
		"prologue.inspected_pen_box",
		"prologue.looked_downriver",
		"prologue.spoke_to_mother",
		"prologue.name_written",
		"prologue.name_memory_seen",
		"prologue.hean_arrived",
		"prologue.porridge_placed",
		"prologue.song_land_news_heard",
		"prologue.heard_boat_owner_fragment",
		"prologue.heard_hean_fragment",
		"prologue.heard_xinheng_fragment",
		"prologue.heard_ferry_people_fragment",
	]:
		if not _assert_state(state_path, true):
			return

	var saved := SaveManager.read_save(TEST_SAVE_PATH)
	if not bool(saved.get("ok", false)):
		_fail("P2 checkpoint save could not be read")
		return
	var save_data: Dictionary = saved.get("data", {})
	if str(save_data.get("player_name", "")) != TEST_NAME:
		_fail("P2 checkpoint did not persist the Chinese player name")
		return
	if str(save_data.get("checkpoint", "")) != "song_land_news":
		_fail("P2 checkpoint did not reach song_land_news")
		return
	if not _assert_trace_order(
		[
			"mother_wash_basin",
			"morning_player_control",
			"xinheng_write",
			"player_writes_name",
			"name_memory_flash",
			"hean_carries_firewood",
			"song_land_is_in_chaos",
			"merchant_boat_docks",
			"hean_counts_water_and_grain",
			"news_player_control",
		]
	):
		return

	SaveManager.delete_save(TEST_SAVE_PATH)
	print(
		"[P2 E2E] PASS: title -> morning layers/exploration -> hold E -> Chinese name/save "
		+ "-> name anomaly -> He'an actions -> merchant boat -> 宋地乱了 -> four spatial fragments."
	)
	AudioDirector.stop_channel("music")
	AudioDirector.stop_channel("ambience")
	AudioDirector.stop_channel("sfx")
	var current_scene := get_tree().current_scene
	if current_scene != null:
		current_scene.queue_free()
	await get_tree().process_frame
	await get_tree().process_frame
	get_tree().quit(0)


func _wait_for_stage(expected_name: String) -> PrologueStageDirector:
	var deadline := Time.get_ticks_msec() + int(STAGE_TIMEOUT_SECONDS * 1000.0)
	while Time.get_ticks_msec() < deadline:
		var current := get_tree().current_scene
		if current != null and current.name == expected_name:
			var director := current.find_child(
				"PrologueStageDirector",
				true,
				false
			) as PrologueStageDirector
			if director != null and director.is_ready_for_interaction():
				return director
		await get_tree().process_frame
	_fail("timed out waiting for stage: " + expected_name)
	return null


func _perform_interaction(
	director: PrologueStageDirector,
	interaction_id: String,
	hold_seconds: float,
	wait_for_resolution := true
) -> bool:
	var interactable := director.get_interactable(interaction_id)
	if interactable == null:
		_fail("missing interactable: " + interaction_id)
		return false
	var player := get_tree().current_scene.find_child("Player", true, false) as PlayerController2D
	if player == null:
		_fail("stage has no player: " + director.stage_id)
		return false
	player.global_position = interactable.global_position
	await get_tree().physics_frame
	await get_tree().physics_frame
	Input.action_press("interact")
	await get_tree().create_timer(hold_seconds).timeout
	Input.action_release("interact")
	if not wait_for_resolution:
		return true
	var deadline := Time.get_ticks_msec() + 4000
	while interactable.interaction_enabled and Time.get_ticks_msec() < deadline:
		await get_tree().process_frame
	if interactable.interaction_enabled:
		_fail("interaction did not commit: " + interaction_id)
		return false
	await get_tree().create_timer(0.22).timeout
	return true


func _assert_state(path: String, expected: Variant) -> bool:
	var actual: Variant = GameState.get_state_value(path)
	if actual != expected:
		_fail("state mismatch at %s: expected %s, got %s" % [path, expected, actual])
		return false
	return true


func _assert_trace_order(expected_steps: Array[String]) -> bool:
	var positions: Dictionary = {}
	for entry in GameState.event_log:
		if entry.get("type", "") != "flow_step":
			continue
		var payload: Dictionary = entry.get("payload", {})
		var step := str(payload.get("step", ""))
		if not positions.has(step):
			positions[step] = int(entry.get("index", -1))
	var last_position := -1
	for step in expected_steps:
		if not positions.has(step):
			_fail("missing P2 trace step: " + step)
			return false
		var position := int(positions[step])
		if position <= last_position:
			_fail("P2 trace order is invalid at: " + step)
			return false
		last_position = position
	return true


func _fail(message: String) -> void:
	if _failed:
		return
	_failed = true
	Input.action_release("interact")
	push_error("[P2 E2E] FAIL: " + message)
	get_tree().quit(1)
