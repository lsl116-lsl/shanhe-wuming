extends Node

const TEST_SAVE_PATH := "user://p4_end_to_end_test_save.json"
const STAGE_TIMEOUT_SECONDS := 18.0

const ROUTES := [
	{
		"interaction_id": "cart.rescue_child",
		"priority": "rescue_child",
		"saw_flag": "prologue.saw_child_cost",
		"feedback_flag": "prologue.rescue_child_feedback_seen",
		"checkpoint": "first_priority_rescue_child",
		"trace_step": "rescue_child_immediate_feedback",
	},
	{
		"interaction_id": "cart.save_records",
		"priority": "save_records",
		"saw_flag": "prologue.saw_record_cost",
		"feedback_flag": "prologue.save_records_feedback_seen",
		"checkpoint": "first_priority_save_records",
		"trace_step": "save_records_immediate_feedback",
	},
	{
		"interaction_id": "cart.mutual_recognition",
		"priority": "mutual_recognition",
		"saw_flag": "prologue.saw_recognition_cost",
		"feedback_flag": "prologue.mutual_recognition_feedback_seen",
		"checkpoint": "first_priority_mutual_recognition",
		"trace_step": "mutual_recognition_immediate_feedback",
	},
]

var _failed := false


func start() -> void:
	_run.call_deferred()


func _run() -> void:
	if not await _run_memory_to_crash_bridge():
		return
	await AudioDirector.stop_channel("music")
	await AudioDirector.stop_channel("ambience")
	await AudioDirector.stop_channel("sfx")
	await get_tree().create_timer(0.12).timeout
	for route in ROUTES:
		if not await _run_route(route):
			return
		await AudioDirector.stop_channel("music")
		await AudioDirector.stop_channel("ambience")
		await AudioDirector.stop_channel("sfx")
		await get_tree().create_timer(0.12).timeout
	SaveManager.delete_save(TEST_SAVE_PATH)
	print(
		"[P4 E2E] PASS: cart crash scene scanned, proximity previews did not lock, "
		+ "hold-E committed rescue_child / save_records / mutual_recognition, "
		+ "state + autosave + immediate feedback verified for all routes."
	)
	get_tree().quit(0)


func _run_memory_to_crash_bridge() -> bool:
	GameState.reset_state()
	GameState.set_state_value("player.name", "无名")
	SaveManager.delete_save(TEST_SAVE_PATH)
	var scene_error := SceneRouter.go_to_scene("res://scenes/prologue/SC05_Ritual_Storehouse.tscn")
	if scene_error != OK:
		_fail("could not start SC05 bridge: " + error_string(scene_error))
		return false
	var storehouse := await _wait_for_stage("SC05_Ritual_Storehouse")
	if storehouse == null:
		return false
	if not await _hold_interaction(storehouse, "storehouse.cracked_bell", 1.65):
		return false
	var crash := await _wait_for_stage("SC06_Cart_Crash_Rain")
	if crash == null:
		return false
	for step in [
		"memory_cuts_to_black",
		"half_second_black_after_memory",
		"cart_wheel_breaks_before_cut",
		"horse_panics_before_cut",
		"cart_hits_mud_before_cut",
		"hard_cut_to_cart_crash",
		"cart_crash_hard_cut_visual",
	]:
		if not _assert_trace_has(step):
			return false
	return true


func _run_route(route: Dictionary) -> bool:
	GameState.reset_state()
	GameState.set_state_value("player.name", "无名")
	GameState.set_state_value("prologue.cracked_bell_memory_completed", true)
	SaveManager.delete_save(TEST_SAVE_PATH)
	var scene_error := SceneRouter.go_to_scene("res://scenes/prologue/SC06_Cart_Crash_Rain.tscn")
	if scene_error != OK:
		_fail("could not start SC06: " + error_string(scene_error))
		return false

	var director := await _wait_for_stage("SC06_Cart_Crash_Rain")
	if director == null:
		return false
	if not _assert_state("prologue.cart_crash_seen", true):
		return false
	if not _assert_state("prologue.cart_scan_completed", true):
		return false
	if not _assert_trace_has("cart_wheel_breaks"):
		return false
	if not _assert_trace_has("cart_choice_player_control"):
		return false

	var interactable := director.get_interactable(str(route["interaction_id"]))
	if interactable == null:
		_fail("missing P4 interactable: " + str(route["interaction_id"]))
		return false
	var player := get_tree().current_scene.find_child("Player", true, false) as PlayerController2D
	if player == null:
		_fail("SC06 has no player")
		return false
	player.global_position = interactable.global_position
	await get_tree().physics_frame
	await get_tree().physics_frame
	await get_tree().create_timer(0.18).timeout
	if str(GameState.get_state_value("prologue.first_priority", "")) != "":
		_fail("proximity preview locked first_priority before hold-E for " + str(route["priority"]))
		return false
	if not _assert_state(str(route["saw_flag"]), true):
		return false

	Input.action_press("interact")
	await get_tree().create_timer(1.38).timeout
	Input.action_release("interact")
	var deadline := Time.get_ticks_msec() + 6000
	while (
		not bool(GameState.get_state_value("prologue.cart_choice_feedback_completed", false))
		and Time.get_ticks_msec() < deadline
	):
		await get_tree().process_frame
	if not bool(GameState.get_state_value("prologue.cart_choice_feedback_completed", false)):
		_fail("P4 route feedback did not complete: " + str(route["priority"]))
		return false

	if not _assert_state("prologue.first_priority", str(route["priority"])):
		return false
	if not _assert_state(str(route["feedback_flag"]), true):
		return false
	var elapsed := float(GameState.get_state_value("prologue.choice_elapsed_seconds", -1.0))
	if elapsed < 0.0:
		_fail("choice elapsed seconds was not recorded for " + str(route["priority"]))
		return false
	if not _assert_trace_has(str(route["trace_step"])):
		return false

	var saved := SaveManager.read_save(TEST_SAVE_PATH)
	if not bool(saved.get("ok", false)):
		_fail("P4 checkpoint save could not be read for " + str(route["priority"]))
		return false
	var save_data: Dictionary = saved.get("data", {})
	if str(save_data.get("checkpoint", "")) != str(route["checkpoint"]):
		_fail("P4 checkpoint mismatch for " + str(route["priority"]))
		return false
	if str(save_data.get("first_priority", "")) != str(route["priority"]):
		_fail("P4 save first_priority mismatch for " + str(route["priority"]))
		return false
	var flags: Dictionary = save_data.get("prologue_flags", {})
	if str(flags.get("first_priority", "")) != str(route["priority"]):
		_fail("P4 saved prologue flag mismatch for " + str(route["priority"]))
		return false
	if float(flags.get("choice_elapsed_seconds", -1.0)) < 0.0:
		_fail("P4 saved elapsed seconds missing for " + str(route["priority"]))
		return false
	if not bool(flags.get(str(route["saw_flag"]).get_slice(".", 1), false)):
		_fail("P4 saved saw-cost flag missing for " + str(route["priority"]))
		return false
	if not bool(flags.get(str(route["feedback_flag"]).get_slice(".", 1), false)):
		_fail("P4 saved feedback flag missing for " + str(route["priority"]))
		return false
	return true


func _hold_interaction(
	director: PrologueStageDirector,
	interaction_id: String,
	hold_seconds: float
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
	return true


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


func _assert_state(path: String, expected: Variant) -> bool:
	var actual: Variant = GameState.get_state_value(path)
	if actual != expected:
		_fail("state mismatch at %s: expected %s, got %s" % [path, expected, actual])
		return false
	return true


func _assert_trace_has(expected_step: String) -> bool:
	for entry in GameState.event_log:
		if entry.get("type", "") != "flow_step":
			continue
		var payload: Dictionary = entry.get("payload", {})
		if str(payload.get("step", "")) == expected_step:
			return true
	_fail("missing P4 trace step: " + expected_step)
	return false


func _fail(message: String) -> void:
	if _failed:
		return
	_failed = true
	Input.action_release("interact")
	push_error("[P4 E2E] FAIL: " + message)
	get_tree().quit(1)
