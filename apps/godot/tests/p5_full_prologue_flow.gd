extends Node

const TEST_NAME := "洛川无名"
const STAGE_TIMEOUT_SECONDS := 22.0
const SCENE_TIMEOUT_SECONDS := 12.0

var _failed := false
var _phase := "not_started"


func start(title_screen: Control) -> void:
	var watchdog := get_tree().create_timer(75.0)
	watchdog.timeout.connect(_on_watchdog_timeout)
	_run.call_deferred(title_screen)


func _run(title_screen: Control) -> void:
	_phase = "title_new_game"
	print("[P5 E2E] phase: " + _phase)
	SaveManager.delete_save()
	var new_game_button := title_screen.find_child("NewGameButton", true, false) as Button
	if new_game_button == null:
		_fail("title screen has no NewGameButton")
		return
	new_game_button.pressed.emit()

	var morning := await _wait_for_stage("SC01_Home_Morning")
	if morning == null:
		return
	_phase = "morning"
	print("[P5 E2E] phase: " + _phase)
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
	_phase = "desk_name"
	print("[P5 E2E] phase: " + _phase)
	if not await _perform_interaction(desk, "desk.write_name", 1.35, false):
		return
	var name_input := get_tree().current_scene.find_child("NameInputLayer", true, false) as NameInputLayer
	if name_input == null:
		_fail("SC02 has no NameInputLayer")
		return
	var input_deadline := Time.get_ticks_msec() + 4000
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
	_phase = "ferry_day"
	print("[P5 E2E] phase: " + _phase)
	for interaction_id in [
		"news.boat_owner",
		"news.hean",
		"news.xinheng",
		"news.ferry_people",
	]:
		if not await _perform_interaction(ferry_day, interaction_id, 0.12):
			return
	var refugee_exit := ferry_day.get_interactable("news.to_refugees")
	if refugee_exit == null:
		_fail("SC03 has no refugee exit")
		return
	if not await _wait_for_interaction_enabled(refugee_exit):
		return
	if not await _perform_interaction(ferry_day, "news.to_refugees", 0.12, false):
		return

	var shelter := await _wait_for_stage("SC04_Refugee_Shelter")
	if shelter == null:
		return
	_phase = "shelter"
	print("[P5 E2E] phase: " + _phase)
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
	if storehouse_exit == null:
		_fail("SC04 has no storehouse exit")
		return
	if not await _wait_for_interaction_enabled(storehouse_exit):
		return
	if not await _perform_interaction(shelter, "shelter.to_storehouse", 0.12, false):
		return

	var storehouse := await _wait_for_stage("SC05_Ritual_Storehouse")
	if storehouse == null:
		return
	_phase = "storehouse"
	print("[P5 E2E] phase: " + _phase)
	for interaction_id in [
		"storehouse.broken_ding",
		"storehouse.chipped_gui",
		"storehouse.damaged_qing",
	]:
		if not await _perform_interaction(storehouse, interaction_id, 0.12):
			return
	if not await _perform_interaction(storehouse, "storehouse.cracked_bell", 1.65, false):
		return

	var crash := await _wait_for_stage("SC06_Cart_Crash_Rain")
	if crash == null:
		return
	_phase = "cart_choice"
	print("[P5 E2E] phase: " + _phase)
	if not await _perform_interaction(crash, "cart.rescue_child", 1.38, false):
		return
	_phase = "wait_ending"
	print("[P5 E2E] phase: " + _phase)
	var ending := await _wait_for_scene("SC07_Prologue_End")
	if ending == null:
		return
	_phase = "ending"
	print("[P5 E2E] phase: " + _phase)
	await get_tree().create_timer(0.2).timeout

	if not _assert_state("player.name", TEST_NAME):
		return
	if not _assert_state("prologue.first_priority", "rescue_child"):
		return
	if not _assert_state("prologue.completed", true):
		return
	if not _assert_state("prologue.chapter_title_reached", true):
		return
	if ending.find_child("ChapterTitleLabel", true, false) == null:
		_fail("ending scene has no chapter title label")
		return

	var saved := SaveManager.read_save()
	if not bool(saved.get("ok", false)):
		_fail("default autosave could not be read after prologue completion")
		return
	var save_data: Dictionary = saved.get("data", {})
	if str(save_data.get("checkpoint", "")) != "prologue_completed":
		_fail("autosave checkpoint is not prologue_completed")
		return
	if str(save_data.get("current_scene", "")) != "res://scenes/prologue/SC07_Prologue_End.tscn":
		_fail("autosave current_scene is not SC07_Prologue_End")
		return

	var title_error := SceneRouter.go_to_scene("res://scenes/ui/TitleScreen.tscn")
	if title_error != OK:
		_fail("could not return to title for continue test")
		return
	_phase = "return_title"
	print("[P5 E2E] phase: " + _phase)
	var title := await _wait_for_scene("TitleScreen")
	if title == null:
		return
	var continue_button := title.find_child("ContinueButton", true, false) as Button
	if continue_button == null:
		_fail("title screen has no ContinueButton")
		return
	continue_button.pressed.emit()
	_phase = "continue_game"
	print("[P5 E2E] phase: " + _phase)
	var continued := await _wait_for_scene("SC07_Prologue_End")
	if continued == null:
		return

	print(
		"[P5 E2E] PASS: title -> full prologue -> first priority rescue_child "
		+ "-> prologue review -> First Chapter title -> autosave -> Continue returns to SC07."
	)
	await AudioDirector.stop_channel("music")
	await AudioDirector.stop_channel("ambience")
	await AudioDirector.stop_channel("sfx")
	await get_tree().create_timer(0.2).timeout
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


func _wait_for_scene(expected_name: String) -> Node:
	var deadline := Time.get_ticks_msec() + int(SCENE_TIMEOUT_SECONDS * 1000.0)
	while Time.get_ticks_msec() < deadline:
		var current := get_tree().current_scene
		if current != null and current.name == expected_name:
			return current
		await get_tree().process_frame
	var current_scene := get_tree().current_scene
	var current_name: String = current_scene.name if current_scene != null else "<none>"
	_fail(
		"timed out waiting for scene: %s, current=%s, first_priority=%s, feedback=%s"
		% [
			expected_name,
			current_name,
			str(GameState.get_state_value("prologue.first_priority", "")),
			str(GameState.get_state_value("prologue.cart_choice_feedback_completed", false)),
		]
	)
	return null


func _wait_for_interaction_enabled(interactable: InteractableArea2D) -> bool:
	var deadline := Time.get_ticks_msec() + 5000
	while is_instance_valid(interactable) and not interactable.interaction_enabled and Time.get_ticks_msec() < deadline:
		await get_tree().process_frame
	if not is_instance_valid(interactable) or not interactable.interaction_enabled:
		_fail("interaction did not become enabled: " + str(interactable))
		return false
	return true


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
	var deadline := Time.get_ticks_msec() + 5000
	while is_instance_valid(interactable) and interactable.interaction_enabled and Time.get_ticks_msec() < deadline:
		await get_tree().process_frame
	if is_instance_valid(interactable) and interactable.interaction_enabled:
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


func _fail(message: String) -> void:
	if _failed:
		return
	_failed = true
	Input.action_release("interact")
	push_error("[P5 E2E] FAIL: " + message)
	get_tree().quit(1)


func _on_watchdog_timeout() -> void:
	if _failed:
		return
	var current_scene := get_tree().current_scene
	var current_name: String = current_scene.name if current_scene != null else "<none>"
	_fail(
		"watchdog timeout at phase=%s current=%s first_priority=%s feedback=%s completed=%s"
		% [
			_phase,
			current_name,
			str(GameState.get_state_value("prologue.first_priority", "")),
			str(GameState.get_state_value("prologue.cart_choice_feedback_completed", false)),
			str(GameState.get_state_value("prologue.completed", false)),
		]
	)
