class_name TimelineRunner
extends Node

signal timeline_loaded(path: String)
signal timeline_started(timeline_id: String)
signal event_started(event_id: String, event_type: String)
signal event_completed(event_id: String, event_type: String)
signal interaction_created(interactable: InteractableArea2D)
signal timeline_completed(timeline_id: String)
signal timeline_failed(event_id: String, error: Error)

var camera_director: CameraDirector
var dialogue_layer: DialogueLayer
var transition_layer: TransitionLayer
var interaction_prompt: InteractionPrompt
var actor_container: Node2D
var interaction_container: Node2D

var _timeline_path := ""
var _timeline_id := ""
var _events: Array = []
var _asset_paths: Dictionary = {}
var _actors: Dictionary = {}
var _running := false
var playback_speed := 1.0
var save_path_override := ""


func configure(
	p_camera_director: CameraDirector,
	p_dialogue_layer: DialogueLayer,
	p_transition_layer: TransitionLayer,
	p_interaction_prompt: InteractionPrompt,
	p_actor_container: Node2D,
	p_interaction_container: Node2D
) -> void:
	camera_director = p_camera_director
	dialogue_layer = p_dialogue_layer
	transition_layer = p_transition_layer
	interaction_prompt = p_interaction_prompt
	actor_container = p_actor_container
	interaction_container = p_interaction_container


func load_timeline(path: String) -> Error:
	if not _is_configured():
		return ERR_UNCONFIGURED
	if not FileAccess.file_exists(path):
		return ERR_FILE_NOT_FOUND
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary or not parsed.get("events", []) is Array:
		return ERR_PARSE_ERROR

	var dialogue_path := str(parsed.get("dialogue_path", ""))
	var asset_manifest_path := str(parsed.get("asset_manifest_path", ""))
	if dialogue_path.is_empty() or asset_manifest_path.is_empty():
		return ERR_INVALID_DATA
	var error := dialogue_layer.load_dialogue_file(dialogue_path)
	if error != OK:
		return error
	error = _load_asset_manifest(asset_manifest_path)
	if error != OK:
		return error
	AudioDirector.load_asset_manifest(asset_manifest_path)

	_timeline_path = path
	_timeline_id = str(parsed.get("timeline_id", path.get_file()))
	_events = parsed.get("events", []).duplicate(true)
	GameState.set_state_value("runtime.current_timeline", _timeline_id, false)
	timeline_loaded.emit(path)
	return OK


func load_timeline_stage(path: String, stage_id: String, event_key := "events") -> Error:
	if not _is_configured():
		return ERR_UNCONFIGURED
	if not FileAccess.file_exists(path):
		return ERR_FILE_NOT_FOUND
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary or not parsed.get("stages", {}) is Dictionary:
		return ERR_PARSE_ERROR
	var stages: Dictionary = parsed.get("stages", {})
	if not stages.has(stage_id) or not stages[stage_id] is Dictionary:
		return ERR_DOES_NOT_EXIST
	var stage: Dictionary = stages[stage_id]
	if not stage.get(event_key, []) is Array:
		return ERR_INVALID_DATA
	var dialogue_path := str(parsed.get("dialogue_path", ""))
	var asset_manifest_path := str(parsed.get("asset_manifest_path", ""))
	if dialogue_path.is_empty() or asset_manifest_path.is_empty():
		return ERR_INVALID_DATA
	var error := dialogue_layer.load_dialogue_file(dialogue_path)
	if error != OK:
		return error
	error = _load_asset_manifest(asset_manifest_path)
	if error != OK:
		return error
	error = AudioDirector.load_asset_manifest(asset_manifest_path)
	if error != OK:
		return error
	_timeline_path = path
	_timeline_id = "%s:%s" % [stage_id, event_key]
	_events = stage.get(event_key, []).duplicate(true)
	GameState.set_state_value("runtime.current_timeline", _timeline_id, false)
	timeline_loaded.emit(path)
	return OK


func register_actor(actor_id: String, actor: Node) -> void:
	if actor_id.is_empty() or actor == null:
		return
	_actors[actor_id] = actor


func clear_registered_actors() -> void:
	_actors.clear()


func start_timeline() -> Error:
	if _running:
		return ERR_ALREADY_IN_USE
	if _events.is_empty():
		return ERR_INVALID_DATA
	_running = true
	timeline_started.emit(_timeline_id)

	for event_data in _events:
		if not event_data is Dictionary:
			_running = false
			return ERR_INVALID_DATA
		var event: Dictionary = event_data
		var event_id := str(event.get("id", "event_%d" % GameState.event_log.size()))
		var event_type := str(event.get("type", ""))
		GameState.set_state_value("runtime.current_timeline_event", event_id, false)
		event_started.emit(event_id, event_type)

		if event_type == "scene_change":
			_record_flow_step(event, event_type)
			event_completed.emit(event_id, event_type)
			var scene_error := _handle_scene_change(event)
			if scene_error != OK:
				timeline_failed.emit(event_id, scene_error)
				_running = false
				return scene_error
			_running = false
			return OK

		var error := await _execute_event(event_type, event)
		if error != OK:
			timeline_failed.emit(event_id, error)
			_running = false
			return error
		_record_flow_step(event, event_type)
		event_completed.emit(event_id, event_type)

	_running = false
	timeline_completed.emit(_timeline_id)
	return OK


func _execute_event(event_type: String, event: Dictionary) -> Error:
	match event_type:
		"camera_move":
			return await _handle_camera_move(event)
		"camera_focus":
			return await _handle_camera_focus(event)
		"camera_shake":
			return await _handle_camera_shake(event)
		"character_enter":
			return await _handle_character_enter(event)
		"character_move":
			return await _handle_character_move(event)
		"character_exit":
			return await _handle_character_exit(event)
		"animation_play":
			return await _handle_animation_play(event)
		"dialogue":
			return await _handle_dialogue(event)
		"player_control":
			GameState.set_player_control(bool(event.get("enabled", true)))
			return OK
		"interaction_enable":
			return await _handle_interaction(event)
		"state_set":
			GameState.set_state_value(str(event.get("path", "")), event.get("value"))
			return OK
		"save_checkpoint":
			return SaveManager.save_game(
				str(event.get("checkpoint", "")),
				str(event.get("save_path", save_path_override))
			)
		"transition":
			return await transition_layer.run_transition(
				str(event.get("mode", "fade_out")),
				_scaled_duration(float(event.get("duration", 0.25)))
			)
		"audio_play":
			return await _handle_audio_play(event)
		"spatial_audio_play":
			return _handle_spatial_audio_play(event)
		"audio_stop":
			await AudioDirector.stop_channel(
				str(event.get("channel", "")),
				_scaled_duration(float(event.get("fade_duration", 0.0)))
			)
			return OK
		"wait":
			await get_tree().create_timer(
				_scaled_duration(float(event.get("duration", 0.0)))
			).timeout
			return OK
		_:
			push_error("TimelineRunner does not support event type: " + event_type)
			return ERR_INVALID_PARAMETER


func _handle_camera_move(event: Dictionary) -> Error:
	return await camera_director.move_to(
		_vector2_from(event.get("target", [0.0, 0.0])),
		_scaled_duration(float(event.get("duration", 0.0)))
	)


func _handle_camera_focus(event: Dictionary) -> Error:
	var actor_id := str(event.get("actor_id", ""))
	if not _actors.has(actor_id) or not _actors[actor_id] is Node2D:
		return ERR_DOES_NOT_EXIST
	return await camera_director.focus_node(
		_actors[actor_id],
		_scaled_duration(float(event.get("duration", 0.0))),
		_vector2_from(event.get("offset", [0.0, 0.0]))
	)


func _handle_camera_shake(event: Dictionary) -> Error:
	return await camera_director.shake(
		_scaled_duration(float(event.get("duration", 0.35))),
		float(event.get("strength", 7.0))
	)


func _handle_character_enter(event: Dictionary) -> Error:
	var actor_id := str(event.get("actor_id", ""))
	var scene_path := resolve_asset(str(event.get("asset_id", "")))
	if actor_id.is_empty() or scene_path.is_empty() or not ResourceLoader.exists(scene_path):
		return ERR_FILE_NOT_FOUND
	var packed := load(scene_path) as PackedScene
	if packed == null:
		return ERR_CANT_OPEN
	var actor := packed.instantiate() as Node2D
	if actor == null:
		return ERR_CANT_CREATE
	actor.name = actor_id
	actor_container.add_child(actor)
	var target := _vector2_from(event.get("position", [0.0, 0.0]))
	actor.position = _vector2_from(event.get("from", [target.x, target.y]))
	_actors[actor_id] = actor
	var duration := _scaled_duration(float(event.get("duration", 0.0)))
	if duration > 0.0:
		var tween := create_tween()
		tween.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
		tween.tween_property(actor, "position", target, duration)
		await tween.finished
	else:
		actor.position = target
	return OK


func _handle_character_move(event: Dictionary) -> Error:
	var actor_id := str(event.get("actor_id", ""))
	if not _actors.has(actor_id) or not _actors[actor_id] is Node2D:
		return ERR_DOES_NOT_EXIST
	var actor: Node2D = _actors[actor_id]
	var target := _vector2_from(event.get("position", [actor.position.x, actor.position.y]))
	var duration := _scaled_duration(float(event.get("duration", 0.0)))
	if duration <= 0.0:
		actor.position = target
		return OK
	var tween := create_tween()
	tween.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(actor, "position", target, duration)
	await tween.finished
	return OK


func _handle_character_exit(event: Dictionary) -> Error:
	var actor_id := str(event.get("actor_id", ""))
	if not _actors.has(actor_id) or not _actors[actor_id] is Node2D:
		return ERR_DOES_NOT_EXIST
	var actor: Node2D = _actors[actor_id]
	var target := _vector2_from(event.get("position", [actor.position.x, actor.position.y]))
	var duration := _scaled_duration(float(event.get("duration", 0.0)))
	if duration > 0.0:
		var tween := create_tween()
		tween.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN)
		tween.tween_property(actor, "position", target, duration)
		await tween.finished
	_actors.erase(actor_id)
	actor.queue_free()
	return OK


func _handle_animation_play(event: Dictionary) -> Error:
	var actor_id := str(event.get("actor_id", ""))
	if not _actors.has(actor_id):
		return ERR_DOES_NOT_EXIST
	var actor: Node = _actors[actor_id]
	var animation_player := actor.get_node_or_null("AnimationPlayer") as AnimationPlayer
	var animation_name := StringName(str(event.get("animation", "")))
	if animation_player == null or not animation_player.has_animation(animation_name):
		return ERR_DOES_NOT_EXIST
	var wait_for_finish := bool(event.get("wait_for_finish", true))
	animation_player.speed_scale = 1.0 / maxf(playback_speed, 0.001)
	animation_player.play(animation_name)
	if wait_for_finish:
		await animation_player.animation_finished
		animation_player.speed_scale = 1.0
	return OK


func _handle_dialogue(event: Dictionary) -> Error:
	var substitutions: Dictionary = {}
	var configured_substitutions: Variant = event.get("substitutions", {})
	if configured_substitutions is Dictionary:
		substitutions = configured_substitutions.duplicate(true)
	substitutions["player_name"] = GameState.get_state_value("player.name", "")
	return await dialogue_layer.show_line(
		str(event.get("line_id", "")),
		substitutions,
		bool(event.get("wait_for_input", true)),
		_scaled_duration(float(event.get("auto_duration", 0.0)))
	)


func _handle_interaction(event: Dictionary) -> Error:
	var scene_path := resolve_asset(str(event.get("asset_id", "")))
	if scene_path.is_empty() or not ResourceLoader.exists(scene_path):
		return ERR_FILE_NOT_FOUND
	var packed := load(scene_path) as PackedScene
	var interactable := packed.instantiate() as InteractableArea2D
	if interactable == null:
		return ERR_CANT_CREATE
	interaction_container.add_child(interactable)
	interactable.position = _vector2_from(event.get("position", [0.0, 0.0]))
	interactable.configure(event)
	interactable.bind_prompt(interaction_prompt)
	interaction_prompt.show_prompt(interactable.prompt_text, interactable.hold_duration)
	interaction_created.emit(interactable)
	await interactable.interaction_committed
	interaction_prompt.hide_prompt()
	return OK


func _handle_audio_play(event: Dictionary) -> Error:
	var channel := str(event.get("channel", "sfx"))
	var asset_id := str(event.get("asset_id", ""))
	var fade_duration := _scaled_duration(float(event.get("fade_duration", 0.0)))
	match channel:
		"music":
			return await AudioDirector.play_music(asset_id, fade_duration)
		"ambience":
			return await AudioDirector.play_ambience(asset_id, fade_duration)
		"voice":
			return await AudioDirector.play_voice(asset_id)
		"ui":
			return await AudioDirector.play_ui(asset_id)
		_:
			return await AudioDirector.play_sfx(asset_id)


func _handle_spatial_audio_play(event: Dictionary) -> Error:
	var actor_id := str(event.get("actor_id", ""))
	if not _actors.has(actor_id):
		return ERR_DOES_NOT_EXIST
	var actor: Node = _actors[actor_id]
	var player := actor.get_node_or_null("AudioStreamPlayer2D") as AudioStreamPlayer2D
	if player == null:
		return ERR_DOES_NOT_EXIST
	var path := resolve_asset(str(event.get("asset_id", "")))
	if path.is_empty() or not ResourceLoader.exists(path):
		return ERR_FILE_NOT_FOUND
	var stream := load(path) as AudioStream
	if stream == null:
		return ERR_CANT_OPEN
	player.stream = stream
	player.bus = StringName(str(event.get("bus", "SFX")))
	player.max_distance = float(event.get("max_distance", 1500.0))
	player.attenuation = float(event.get("attenuation", 1.0))
	player.volume_db = float(event.get("volume_db", 0.0))
	player.play()
	return OK


func _handle_scene_change(event: Dictionary) -> Error:
	var path := resolve_asset(str(event.get("asset_id", "")))
	if path.is_empty():
		return ERR_FILE_NOT_FOUND
	return SceneRouter.go_to_scene(path)


func _load_asset_manifest(path: String) -> Error:
	if not FileAccess.file_exists(path):
		return ERR_FILE_NOT_FOUND
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary:
		return ERR_PARSE_ERROR
	_asset_paths.clear()
	for group_name in ["runtime_assets", "test_assets", "p0_assets"]:
		var group: Variant = parsed.get(group_name, {})
		if group is Dictionary:
			for asset_id in group:
				if group[asset_id] is String:
					_asset_paths[asset_id] = group[asset_id]
	return OK


func resolve_asset(asset_id: String) -> String:
	return str(_asset_paths.get(asset_id, ""))


func _record_flow_step(event: Dictionary, event_type: String) -> void:
	GameState.record_event(
		"flow_step",
		{
			"step": str(event.get("trace_step", event_type)),
			"event_id": str(event.get("id", "")),
		}
	)


func _is_configured() -> bool:
	return (
		camera_director != null
		and dialogue_layer != null
		and transition_layer != null
		and interaction_prompt != null
		and actor_container != null
		and interaction_container != null
	)


func _vector2_from(value: Variant) -> Vector2:
	if value is Vector2:
		return value
	if value is Array and value.size() >= 2:
		return Vector2(float(value[0]), float(value[1]))
	return Vector2.ZERO


func _scaled_duration(duration: float) -> float:
	return duration * maxf(playback_speed, 0.001)
