extends Node

const TEST_SAVE_PATH := "user://p3_end_to_end_test_save.json"
const STAGE_TIMEOUT_SECONDS := 15.0

var _failed := false


func start() -> void:
	_run.call_deferred()


func _run() -> void:
	GameState.reset_state()
	SaveManager.delete_save(TEST_SAVE_PATH)
	var scene_error := SceneRouter.go_to_scene(
		"res://scenes/prologue/SC04_Refugee_Shelter.tscn"
	)
	if scene_error != OK:
		_fail("could not start SC04: " + error_string(scene_error))
		return

	var shelter := await _wait_for_stage("SC04_Refugee_Shelter")
	if shelter == null:
		return
	await _capture_if_requested("p3_sc04_refugees_arrived")
	for interaction_id in [
		"shelter.hanning_sleeve",
		"shelter.hanning_mother",
		"shelter.xinheng_pen",
		"shelter.liuniang_song",
		"shelter.temporary_registry",
	]:
		if not await _perform_interaction(shelter, interaction_id, 0.12):
			return

	var storehouse_exit := shelter.get_interactable("shelter.to_storehouse")
	var sequence_deadline := Time.get_ticks_msec() + 5000
	while (
		storehouse_exit != null
		and not storehouse_exit.interaction_enabled
		and Time.get_ticks_msec() < sequence_deadline
	):
		await get_tree().process_frame
	if storehouse_exit == null or not storehouse_exit.interaction_enabled:
		_fail("broken-rice/night/bell sequence did not reveal the storehouse path")
		return
	await _capture_if_requested("p3_sc04_night_bell_lure")
	if not await _perform_interaction(
		shelter,
		"shelter.to_storehouse",
		0.12,
		false
	):
		return

	var storehouse := await _wait_for_stage("SC05_Ritual_Storehouse")
	if storehouse == null:
		return
	await _capture_if_requested("p3_sc05_ritual_storehouse")
	for interaction_id in [
		"storehouse.broken_ding",
		"storehouse.chipped_gui",
		"storehouse.damaged_qing",
	]:
		if not await _perform_interaction(storehouse, interaction_id, 0.12):
			return
	if not await _perform_interaction(
		storehouse,
		"storehouse.cracked_bell",
		1.65,
		false
	):
		return
	if OS.get_cmdline_user_args().has("--p3-visual-capture"):
		await get_tree().create_timer(0.46).timeout
		await _capture_if_requested("p3_sc05_cracked_bell_memory")
		await get_tree().create_timer(0.32).timeout
		await _capture_if_requested("p3_sc05_memory_line")

	var memory_deadline := Time.get_ticks_msec() + 7000
	while (
		not bool(GameState.get_state_value("prologue.cracked_bell_memory_completed", false))
		and Time.get_ticks_msec() < memory_deadline
	):
		await get_tree().process_frame
	if not bool(GameState.get_state_value("prologue.cracked_bell_memory_completed", false)):
		_fail("cracked-bell memory did not complete")
		return

	for state_path in [
		"prologue.first_refugees_arrived",
		"prologue.saw_hanning_sleeve",
		"prologue.hanning_mother_blocked_question",
		"prologue.saw_xinheng_pen_pause",
		"prologue.heard_liuniang_song_stop",
		"prologue.inspected_temporary_registry",
		"prologue.hean_poured_broken_rice",
		"prologue.shelter_night_fallen",
		"prologue.rain_intensified",
		"prologue.heard_cracked_bell_lure",
		"prologue.followed_bell_to_storehouse",
		"prologue.entered_ritual_storehouse",
		"prologue.inspected_broken_ding",
		"prologue.inspected_chipped_gui",
		"prologue.inspected_damaged_qing",
		"prologue.touched_cracked_bell",
		"prologue.cracked_bell_memory_completed",
	]:
		if not _assert_state(state_path, true):
			return

	var memory_actor := get_tree().current_scene.find_child(
		"bell_memory",
		true,
		false
	)
	if memory_actor == null or not memory_actor.has_method("get_memory_duration_seconds"):
		_fail("SC05 has no measurable cracked-bell memory actor")
		return
	var memory_duration := float(memory_actor.call("get_memory_duration_seconds"))
	if memory_duration < 20.0 or memory_duration > 35.0:
		_fail("cracked-bell memory duration is outside 20–35 seconds: %.2f" % memory_duration)
		return

	var saved := SaveManager.read_save(TEST_SAVE_PATH)
	if not bool(saved.get("ok", false)):
		_fail("P3 checkpoint save could not be read")
		return
	var save_data: Dictionary = saved.get("data", {})
	if str(save_data.get("checkpoint", "")) != "cracked_bell_memory":
		_fail("P3 checkpoint did not reach cracked_bell_memory")
		return

	if not _assert_trace_order(
		[
			"old_refugee_helped_ashore",
			"hanning_presses_sleeve",
			"hanning_mother_shields_him",
			"xinheng_pen_stops",
			"liuniang_stops_at_place_name",
			"hean_pours_broken_rice",
			"evening_turns_to_night",
			"rain_intensifies",
			"bell_calls_from_storehouse",
			"enter_ritual_storehouse",
			"cracked_bell_touched",
			"cracked_bell_memory_animation_begins",
			"not_first_time_mountains_rivers_changed",
			"cracked_bell_memory_completed",
			"cracked_bell_checkpoint_saved",
		]
	):
		return

	SaveManager.delete_save(TEST_SAVE_PATH)
	print(
		"[P3 E2E] PASS: first Song refugees -> Han Ning sleeve/mother block "
		+ "-> Xin Heng pen/Liu Niang song/registry -> He An last rice "
		+ "-> night/rain/spatial bell -> ritual objects -> hold E "
		+ "-> 27-second cracked-bell memory -> checkpoint."
	)
	await AudioDirector.stop_channel("music")
	await AudioDirector.stop_channel("ambience")
	await AudioDirector.stop_channel("sfx")
	await get_tree().create_timer(0.25).timeout
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
	var player := get_tree().current_scene.find_child(
		"Player",
		true,
		false
	) as PlayerController2D
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
	var deadline := Time.get_ticks_msec() + 4500
	while interactable.interaction_enabled and Time.get_ticks_msec() < deadline:
		await get_tree().process_frame
	if interactable.interaction_enabled:
		_fail("interaction did not commit: " + interaction_id)
		return false
	await get_tree().create_timer(0.18).timeout
	return true


func _assert_state(path: String, expected: Variant) -> bool:
	var actual: Variant = GameState.get_state_value(path)
	if actual != expected:
		_fail("state mismatch at %s: expected %s, got %s" % [path, expected, actual])
		return false
	return true


func _capture_if_requested(file_stem: String) -> void:
	if not OS.get_cmdline_user_args().has("--p3-visual-capture"):
		return
	await get_tree().process_frame
	await get_tree().process_frame
	var texture := get_viewport().get_texture()
	if texture == null:
		_fail("viewport texture is unavailable for visual capture: " + file_stem)
		return
	var image := texture.get_image()
	if image == null:
		_fail("viewport image is unavailable for visual capture: " + file_stem)
		return
	var review_dir := ProjectSettings.globalize_path("res://review")
	DirAccess.make_dir_recursive_absolute(review_dir)
	var error := image.save_png("%s/%s.png" % [review_dir, file_stem])
	if error != OK:
		_fail("could not save visual capture: " + file_stem)


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
			_fail("missing P3 trace step: " + step)
			return false
		var position := int(positions[step])
		if position <= last_position:
			_fail("P3 trace order is invalid at: " + step)
			return false
		last_position = position
	return true


func _fail(message: String) -> void:
	if _failed:
		return
	_failed = true
	Input.action_release("interact")
	push_error("[P3 E2E] FAIL: " + message)
	get_tree().quit(1)
