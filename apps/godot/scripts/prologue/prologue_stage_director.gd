class_name PrologueStageDirector
extends Node

signal stage_ready(stage_id: String)
signal interaction_resolved(interaction_id: String)
signal name_committed(player_name: String)
signal p2_terminal_reached
signal p3_terminal_reached
signal p4_terminal_reached

const TIMELINE_PATH := "res://content/prologue/timeline.json"
const INTERACTABLES_PATH := "res://content/prologue/interactables.json"
const INTERACTION_SCENE := preload("res://scenes/core/InteractableArea2D.tscn")
const P2_TEST_SAVE_PATH := "user://p2_end_to_end_test_save.json"
const P3_TEST_SAVE_PATH := "user://p3_end_to_end_test_save.json"
const P4_TEST_SAVE_PATH := "user://p4_end_to_end_test_save.json"

@export var stage_id := ""
@export var camera_min_x := 640.0
@export var camera_max_x := 1560.0

@onready var player: PlayerController2D = %Player
@onready var scene_camera: Camera2D = %SceneCamera
@onready var actor_container: Node2D = %Actors
@onready var interaction_container: Node2D = %Interactions
@onready var camera_director: CameraDirector = %CameraDirector
@onready var timeline_runner: TimelineRunner = %TimelineRunner
@onready var dialogue_layer: DialogueLayer = %DialogueLayer
@onready var transition_layer: TransitionLayer = %TransitionLayer
@onready var interaction_prompt: InteractionPrompt = %InteractionPrompt
@onready var choice_pressure_controller: ChoicePressureController = get_node_or_null("../ChoicePressureController") as ChoicePressureController

var _stage_data: Dictionary = {}
var _interactables: Dictionary = {}
var _initially_disabled: Dictionary = {}
var _opening_finished := false
var _auto_sequence_started := false
var _name_input: NameInputLayer
var _objective_label: Label
var _location_label: Label
var _water_shimmer: Sprite2D
var _fog_front: Sprite2D
var _boat: Sprite2D
var _elapsed := 0.0


func _ready() -> void:
	SceneRouter.register_current_scene(get_tree().current_scene.scene_file_path)
	GameState.set_player_control(false)
	_name_input = get_node_or_null("../NameInputLayer") as NameInputLayer
	_objective_label = get_node_or_null("../HUD/ObjectivePanel/Margin/ObjectiveLabel") as Label
	_location_label = get_node_or_null("../HUD/LocationLabel") as Label
	_water_shimmer = get_node_or_null("../WaterShimmer") as Sprite2D
	_fog_front = get_node_or_null("../FogFront") as Sprite2D
	_boat = actor_container.get_node_or_null("boat") as Sprite2D
	if _name_input != null:
		_name_input.name_submitted.connect(_on_name_submitted)

	camera_director.bind_camera(scene_camera)
	timeline_runner.configure(
		camera_director,
		dialogue_layer,
		transition_layer,
		interaction_prompt,
		actor_container,
		interaction_container
	)
	timeline_runner.playback_speed = (
		0.035 if _is_e2e_test() else (0.16 if _is_review_capture() else 1.0)
	)
	timeline_runner.save_path_override = _test_save_path()
	for actor in actor_container.get_children():
		timeline_runner.register_actor(actor.name, actor)
	timeline_runner.register_actor("player", player)

	var load_error := _load_stage_data()
	if load_error != OK:
		push_error("P2 stage data failed to load: %s" % error_string(load_error))
		if _is_e2e_test():
			get_tree().quit(41)
		return
	_create_stage_interactables()
	_set_interactions_enabled(false)
	if _objective_label != null:
		_objective_label.text = str(_stage_data.get("objective", ""))

	if (
		stage_id == "SC02_Xinheng_Desk"
		and bool(GameState.get_state_value("prologue.name_written", false))
	):
		_resume_after_written_name.call_deferred()
	else:
		_play_opening.call_deferred()


func _process(delta: float) -> void:
	_elapsed += delta
	if _water_shimmer != null:
		_water_shimmer.position.x = 1100.0 + sin(_elapsed * 0.17) * 24.0
		_water_shimmer.modulate.a = 0.32 + sin(_elapsed * 0.41) * 0.06
	if _fog_front != null:
		_fog_front.position.x = 1100.0 + sin(_elapsed * 0.09) * 32.0
	if _boat != null:
		_boat.rotation = sin(_elapsed * 0.62) * 0.012
		_boat.position.y += sin(_elapsed * 0.7) * delta * 0.55
	if (
		_opening_finished
		and bool(GameState.get_state_value("player.can_move", false))
		and is_instance_valid(player)
	):
		var target_x := clampf(player.global_position.x, camera_min_x, camera_max_x)
		scene_camera.global_position.x = lerpf(
			scene_camera.global_position.x,
			target_x,
			minf(1.0, delta * 5.5)
		)


func get_interactable(interaction_id: String) -> InteractableArea2D:
	return _interactables.get(interaction_id) as InteractableArea2D


func is_ready_for_interaction() -> bool:
	return _opening_finished


func trigger_interaction(interaction_id: String) -> Error:
	var interactable := get_interactable(interaction_id)
	if interactable == null:
		return ERR_DOES_NOT_EXIST
	interactable.perform_interaction()
	return OK


func _load_stage_data() -> Error:
	if not FileAccess.file_exists(TIMELINE_PATH):
		return ERR_FILE_NOT_FOUND
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(TIMELINE_PATH))
	if not parsed is Dictionary or not parsed.get("stages", {}) is Dictionary:
		return ERR_PARSE_ERROR
	var stages: Dictionary = parsed.get("stages", {})
	if not stages.has(stage_id) or not stages[stage_id] is Dictionary:
		return ERR_DOES_NOT_EXIST
	_stage_data = stages[stage_id].duplicate(true)
	return timeline_runner.load_timeline_stage(TIMELINE_PATH, stage_id, "events")


func _load_interactable_data() -> Array:
	if not FileAccess.file_exists(INTERACTABLES_PATH):
		return []
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(INTERACTABLES_PATH))
	if not parsed is Dictionary or not parsed.get("scenes", {}) is Dictionary:
		return []
	var scenes: Dictionary = parsed.get("scenes", {})
	if not scenes.has(stage_id) or not scenes[stage_id] is Array:
		return []
	return scenes[stage_id]


func _create_stage_interactables() -> void:
	for raw_data in _load_interactable_data():
		if not raw_data is Dictionary:
			continue
		var data: Dictionary = raw_data
		var interactable := INTERACTION_SCENE.instantiate() as InteractableArea2D
		if interactable == null:
			continue
		interaction_container.add_child(interactable)
		interactable.position = _vector2_from(data.get("position", [0.0, 0.0]))
		interactable.configure(data)
		interactable.bind_prompt(interaction_prompt)
		var radius := float(data.get("radius", 70.0))
		var collision_shape := interactable.get_node_or_null("CollisionShape2D") as CollisionShape2D
		if collision_shape != null and collision_shape.shape is CircleShape2D:
			(collision_shape.shape as CircleShape2D).radius = radius
		interactable.interaction_committed.connect(_on_interaction_committed)
		interactable.interaction_available.connect(_on_interaction_available)
		interactable.interaction_unavailable.connect(_on_interaction_unavailable)
		_interactables[interactable.interaction_id] = interactable
		if not bool(data.get("initially_enabled", true)):
			_initially_disabled[interactable.interaction_id] = true


func _play_opening() -> void:
	transition_layer.cover.modulate.a = 1.0
	var error := await timeline_runner.start_timeline()
	if error != OK:
		push_error("P2 opening timeline failed: %s" % error_string(error))
		if _is_e2e_test():
			get_tree().quit(42)
		return
	_finish_opening()


func _finish_opening() -> void:
	dialogue_layer.hide_dialogue()
	_opening_finished = true
	_set_initial_interactions_enabled()
	GameState.set_player_control(true)
	if (
		choice_pressure_controller != null
		and _stage_data.get("choice_pressure", {}) is Dictionary
	):
		choice_pressure_controller.start(_stage_data.get("choice_pressure", {}))
	if stage_id == "SC03_Ferry_Day":
		GameState.set_state_value("prologue.song_land_news_heard", true)
		var save_error := SaveManager.save_game(
			"song_land_news",
			_test_save_path()
		)
		if save_error != OK:
			push_error("P2 news checkpoint failed: " + error_string(save_error))
		p2_terminal_reached.emit()
	stage_ready.emit(stage_id)
	if _is_review_capture():
		_capture_review.call_deferred()


func _resume_after_written_name() -> void:
	transition_layer.cover.modulate.a = 1.0
	var error := timeline_runner.load_timeline_stage(
		TIMELINE_PATH,
		stage_id,
		"after_name_events"
	)
	if error == OK:
		await timeline_runner.start_timeline()


func _set_interactions_enabled(enabled: bool) -> void:
	for interactable_value in _interactables.values():
		var interactable := interactable_value as InteractableArea2D
		if interactable != null:
			interactable.set_interaction_enabled(enabled)


func _set_initial_interactions_enabled() -> void:
	for interaction_id in _interactables:
		var interactable := _interactables[interaction_id] as InteractableArea2D
		if interactable != null:
			interactable.set_interaction_enabled(not _initially_disabled.has(interaction_id))


func _enable_only_interactions(interaction_ids: Array) -> void:
	_set_interactions_enabled(false)
	for interaction_id_value in interaction_ids:
		var interaction_id := str(interaction_id_value)
		var interactable := get_interactable(interaction_id)
		if interactable != null:
			interactable.set_interaction_enabled(true)


func _on_interaction_committed(interaction_id: String, payload: Dictionary) -> void:
	var state_path := str(payload.get("state_path", ""))
	if not state_path.is_empty():
		GameState.set_state_value(state_path, payload.get("state_value", true))
	GameState.record_event(
		"prologue_interaction",
		{"stage": stage_id, "interaction_id": interaction_id}
	)
	var actor_id := str(payload.get("actor_id", ""))
	var animation_name := str(payload.get("animation", ""))
	if not actor_id.is_empty() and not animation_name.is_empty():
		var actor := actor_container.get_node_or_null(actor_id)
		var animation_player := (
			actor.get_node_or_null("AnimationPlayer") as AnimationPlayer
			if actor != null
			else null
		)
		if animation_player != null and animation_player.has_animation(animation_name):
			animation_player.play(animation_name)
	var sfx_id := str(payload.get("sfx_id", ""))
	if not sfx_id.is_empty():
		await AudioDirector.play_sfx(sfx_id)

	match str(payload.get("action", "dialogue")):
		"name_input":
			_begin_name_input()
		"scene_change":
			await _change_scene_from_payload(payload)
		"event_block":
			await _run_event_block(str(payload.get("event_key", "")))
		"choice_commit":
			await _commit_choice(interaction_id, payload)
		_:
			await _show_payload_dialogue(payload)
	interaction_resolved.emit(interaction_id)
	await _maybe_run_auto_sequence()


func _on_interaction_available(interaction_id: String) -> void:
	var interactable := get_interactable(interaction_id)
	if interactable == null:
		return
	var payload := interactable.payload
	if str(payload.get("action", "")) != "choice_commit":
		return
	var choice_id := str(payload.get("choice_id", ""))
	var preview_state_path := str(payload.get("preview_state_path", ""))
	if not preview_state_path.is_empty():
		GameState.set_state_value(preview_state_path, true)
	if choice_pressure_controller != null:
		choice_pressure_controller.preview_choice(choice_id, payload)


func _on_interaction_unavailable(interaction_id: String) -> void:
	var interactable := get_interactable(interaction_id)
	if interactable == null:
		return
	var payload := interactable.payload
	if str(payload.get("action", "")) != "choice_commit":
		return
	if choice_pressure_controller != null:
		choice_pressure_controller.clear_preview(str(payload.get("choice_id", "")))


func _show_payload_dialogue(payload: Dictionary) -> void:
	var line_id := str(payload.get("line_id", ""))
	if line_id.is_empty():
		return
	GameState.set_player_control(false)
	var error := await dialogue_layer.show_line(
		line_id,
		{"player_name": GameState.get_state_value("player.name", "")},
		false,
		_scaled_duration(float(payload.get("auto_duration", 3.4)))
	)
	if error != OK:
		push_error("P2 interaction dialogue failed: " + line_id)
	dialogue_layer.hide_dialogue()
	GameState.set_player_control(true)


func _change_scene_from_payload(payload: Dictionary) -> void:
	GameState.set_player_control(false)
	var checkpoint := str(payload.get("checkpoint", ""))
	if not checkpoint.is_empty():
		var save_error := SaveManager.save_game(
			checkpoint,
			_test_save_path()
		)
		if save_error != OK:
			push_error("P2 scene checkpoint failed: " + error_string(save_error))
	await transition_layer.fade_out(_scaled_duration(0.45))
	var target_asset_id := str(payload.get("target_asset_id", ""))
	var target_path := timeline_runner.resolve_asset(target_asset_id)
	if target_path.is_empty():
		push_error("P2 scene target could not be resolved: " + target_asset_id)
		if _is_e2e_test():
			get_tree().quit(43)
		return
	SceneRouter.go_to_scene(target_path)


func _commit_choice(interaction_id: String, payload: Dictionary) -> void:
	GameState.set_player_control(false)
	_set_interactions_enabled(false)
	var choice_id := str(payload.get("choice_id", ""))
	var priority := str(payload.get("priority_value", choice_id))
	var elapsed := 0.0
	if choice_pressure_controller != null:
		elapsed = choice_pressure_controller.get_elapsed_seconds()
		choice_pressure_controller.lock_choice(choice_id)
	GameState.set_state_value("prologue.first_priority", priority)
	GameState.set_state_value("prologue.choice_elapsed_seconds", elapsed)
	GameState.set_state_value("prologue.cart_choice_locked", true)
	GameState.record_event(
		"prologue_first_priority_committed",
		{
			"stage": stage_id,
			"interaction_id": interaction_id,
			"choice_id": choice_id,
			"priority": priority,
			"elapsed_seconds": elapsed,
		}
	)
	var event_key := str(payload.get("event_key", ""))
	if not event_key.is_empty():
		var error := await _run_event_block(event_key, false)
		if error != OK:
			push_error("P4 choice feedback failed: " + error_string(error))
			if _is_e2e_test():
				get_tree().quit(46)
			return
	_stop_spatial_pressure_audio()
	GameState.set_state_value("prologue.cart_choice_feedback_completed", true)
	p4_terminal_reached.emit()
	var completion_asset_id := str(_stage_data.get("completion_scene_asset_id", ""))
	if not completion_asset_id.is_empty() and not OS.get_cmdline_user_args().has("--p4-e2e"):
		await transition_layer.fade_out(_scaled_duration(0.65))
		var completion_scene := timeline_runner.resolve_asset(completion_asset_id)
		if completion_scene.is_empty():
			push_error("P5 completion scene could not be resolved: " + completion_asset_id)
			if _is_e2e_test():
				get_tree().quit(47)
			return
		SceneRouter.go_to_scene(completion_scene)


func _stop_spatial_pressure_audio() -> void:
	for node in actor_container.find_children("*", "AudioStreamPlayer2D", true, false):
		var player := node as AudioStreamPlayer2D
		if player != null:
			player.stop()
			player.stream = null


func _begin_name_input() -> void:
	GameState.set_player_control(false)
	var config: Dictionary = _stage_data.get("name_input", {})
	if _name_input == null:
		push_error("SC02 has no NameInputLayer.")
		return
	_name_input.show_input(
		str(config.get("title", "写下姓名")),
		str(config.get("hint", "1—8 个字")),
		str(config.get("development_prefill", "")) if OS.is_debug_build() else ""
	)


func _on_name_submitted(player_name: String) -> void:
	GameState.set_state_value("player.name", player_name)
	GameState.set_state_value("prologue.name_written", true)
	GameState.record_event("player_name_committed", {"name": player_name})
	var save_error := SaveManager.save_game(
		"name_written",
		_test_save_path()
	)
	if save_error != OK:
		push_error("P2 name checkpoint failed: " + error_string(save_error))
	name_committed.emit(player_name)
	var load_error := timeline_runner.load_timeline_stage(
		TIMELINE_PATH,
		stage_id,
		"after_name_events"
	)
	if load_error != OK:
		push_error("P2 post-name timeline failed to load: " + error_string(load_error))
		if _is_e2e_test():
			get_tree().quit(44)
		return
	await timeline_runner.start_timeline()


func _is_e2e_test() -> bool:
	var args := OS.get_cmdline_user_args()
	return (
		args.has("--p2-e2e")
		or args.has("--p3-e2e")
		or args.has("--p4-e2e")
		or args.has("--p5-e2e")
	)


func _is_review_capture() -> bool:
	var args := OS.get_cmdline_user_args()
	return args.has("--p2-capture") or args.has("--p3-capture") or args.has("--p4-visual-capture")


func _capture_review() -> void:
	await get_tree().process_frame
	await get_tree().process_frame
	var image := get_viewport().get_texture().get_image()
	var review_dir := ProjectSettings.globalize_path("res://review")
	DirAccess.make_dir_recursive_absolute(review_dir)
	var prefix := "p3" if stage_id in [
		"SC04_Refugee_Shelter",
		"SC05_Ritual_Storehouse",
	] else ("p4" if stage_id == "SC06_Cart_Crash_Rain" else "p2")
	var output_path := "%s/%s_%s.png" % [review_dir, prefix, stage_id.to_snake_case()]
	var error := image.save_png(output_path)
	if error != OK:
		push_error("P2 review capture failed: " + error_string(error))
		get_tree().quit(61)
		return
	print("[P2 REVIEW] " + output_path)
	AudioDirector.stop_channel("music")
	AudioDirector.stop_channel("ambience")
	get_tree().quit(0)


func _maybe_run_auto_sequence() -> void:
	if _auto_sequence_started:
		return
	var config: Variant = _stage_data.get("auto_sequence", {})
	if not config is Dictionary or config.is_empty():
		return
	for state_path_value in config.get("requirements", []):
		if not bool(GameState.get_state_value(str(state_path_value), false)):
			return
	_auto_sequence_started = true
	_set_interactions_enabled(false)
	GameState.set_player_control(false)
	var error := await _run_event_block(str(config.get("event_key", "")), false)
	if error != OK:
		push_error("P3 automatic sequence failed: " + error_string(error))
		if _is_e2e_test():
			get_tree().quit(45)
		return
	var objective := str(config.get("objective_after", ""))
	if _objective_label != null and not objective.is_empty():
		_objective_label.text = objective
	var location := str(config.get("location_after", ""))
	if _location_label != null and not location.is_empty():
		_location_label.text = location
	_enable_only_interactions(config.get("enable_interactions", []))
	GameState.set_player_control(true)


func _run_event_block(event_key: String, restore_control := true) -> Error:
	if event_key.is_empty():
		return ERR_INVALID_PARAMETER
	GameState.set_player_control(false)
	_set_interactions_enabled(false)
	var error := timeline_runner.load_timeline_stage(TIMELINE_PATH, stage_id, event_key)
	if error != OK:
		return error
	error = await timeline_runner.start_timeline()
	if error != OK:
		return error
	var enabled_after: Variant = _stage_data.get("%s_enable_interactions" % event_key, [])
	if enabled_after is Array and not enabled_after.is_empty():
		_enable_only_interactions(enabled_after)
	var objective_after := str(_stage_data.get("%s_objective" % event_key, ""))
	if _objective_label != null and not objective_after.is_empty():
		_objective_label.text = objective_after
	if restore_control:
		GameState.set_player_control(true)
	if event_key == "after_bell_touch_events":
		if OS.get_cmdline_user_args().has("--p3-e2e"):
			p3_terminal_reached.emit()
		elif _stage_data.has("after_memory_crash_events"):
			return await _run_event_block("after_memory_crash_events", false)
	return OK


func _test_save_path() -> String:
	var args := OS.get_cmdline_user_args()
	if args.has("--p4-e2e"):
		return P4_TEST_SAVE_PATH
	if args.has("--p3-e2e"):
		return P3_TEST_SAVE_PATH
	if args.has("--p2-e2e"):
		return P2_TEST_SAVE_PATH
	return ""


func _scaled_duration(duration: float) -> float:
	return duration * (
		0.035 if _is_e2e_test() else (0.16 if _is_review_capture() else 1.0)
	)


func _vector2_from(value: Variant) -> Vector2:
	if value is Vector2:
		return value
	if value is Array and value.size() >= 2:
		return Vector2(float(value[0]), float(value[1]))
	return Vector2.ZERO
