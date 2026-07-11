class_name PlayerController2D
extends CharacterBody2D

signal interact_pressed

@export var move_speed := 210.0
@export var min_bounds := Vector2(90.0, 490.0)
@export var max_bounds := Vector2(1830.0, 620.0)

@onready var visual: Node2D = $Visual
@onready var head: Sprite2D = $Visual/Head
@onready var front_arm_tablet: Sprite2D = $Visual/FrontArmTablet
@onready var animation_player: AnimationPlayer = $AnimationPlayer

var _visual_time := 0.0
var _story_action_active := false
var _footstep_elapsed := 0.0
var _footstep_variant := 0


func _ready() -> void:
	_build_story_animations()
	animation_player.animation_started.connect(_on_story_animation_started)
	animation_player.animation_finished.connect(_on_story_animation_finished)


func _physics_process(delta: float) -> void:
	var game_state := get_node_or_null("/root/GameState")
	if game_state != null and not bool(game_state.get_state_value("player.can_move", true)):
		velocity = Vector2.ZERO
		if not _story_action_active:
			_update_visual(Vector2.ZERO)
		return
	var input_vector := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if input_vector.length_squared() > 1.0:
		input_vector = input_vector.normalized()

	velocity = input_vector * move_speed
	move_and_slide()
	global_position.x = clampf(global_position.x, min_bounds.x, max_bounds.x)
	global_position.y = clampf(global_position.y, min_bounds.y, max_bounds.y)

	_visual_time += delta
	_update_visual(input_vector)
	_update_footsteps(delta, input_vector)

	if Input.is_action_just_pressed("interact"):
		interact_pressed.emit()


func _update_visual(input_vector: Vector2) -> void:
	var is_walking := input_vector.length_squared() > 0.01
	var breathe := sin(_visual_time * 2.1) * 1.2
	visual.position.y = -140.0 + breathe

	if is_walking:
		visual.rotation = sin(_visual_time * 9.0) * 0.018
		head.rotation = sin(_visual_time * 4.5) * 0.012
		front_arm_tablet.rotation = sin(_visual_time * 8.0) * 0.025
		if absf(input_vector.x) > 0.05:
			visual.scale.x = signf(input_vector.x)
	else:
		visual.rotation = lerpf(visual.rotation, 0.0, 0.18)
		head.rotation = sin(_visual_time * 0.9) * 0.01
		front_arm_tablet.rotation = lerpf(front_arm_tablet.rotation, 0.0, 0.12)


func _build_story_animations() -> void:
	var library := AnimationLibrary.new()
	var write := Animation.new()
	write.length = 1.55
	var arm_track := write.add_track(Animation.TYPE_VALUE)
	write.track_set_path(arm_track, NodePath("Visual/FrontArmTablet:rotation"))
	write.track_set_interpolation_type(arm_track, Animation.INTERPOLATION_CUBIC)
	write.track_insert_key(arm_track, 0.0, 0.0)
	write.track_insert_key(arm_track, 0.38, -0.28)
	write.track_insert_key(arm_track, 0.82, -0.19)
	write.track_insert_key(arm_track, 1.18, -0.31)
	write.track_insert_key(arm_track, 1.55, 0.0)
	var head_track := write.add_track(Animation.TYPE_VALUE)
	write.track_set_path(head_track, NodePath("Visual/Head:rotation"))
	write.track_set_interpolation_type(head_track, Animation.INTERPOLATION_CUBIC)
	write.track_insert_key(head_track, 0.0, 0.0)
	write.track_insert_key(head_track, 0.32, 0.11)
	write.track_insert_key(head_track, 1.22, 0.11)
	write.track_insert_key(head_track, 1.55, 0.0)
	library.add_animation(&"write", write)

	var look_up := Animation.new()
	look_up.length = 1.2
	var look_track := look_up.add_track(Animation.TYPE_VALUE)
	look_up.track_set_path(look_track, NodePath("Visual/Head:rotation"))
	look_up.track_set_interpolation_type(look_track, Animation.INTERPOLATION_CUBIC)
	look_up.track_insert_key(look_track, 0.0, 0.0)
	look_up.track_insert_key(look_track, 0.45, -0.18)
	look_up.track_insert_key(look_track, 1.2, -0.08)
	library.add_animation(&"look_up", look_up)
	_add_story_animation(
		library,
		"choice_scan",
		1.15,
		{
			"Visual/Head:rotation": [[0.0, -0.16], [0.38, 0.18], [0.74, 0.0], [1.15, -0.08]],
			"Visual/FrontArmTablet:rotation": [[0.0, 0.0], [0.5, -0.08], [1.15, 0.04]],
		}
	)
	_add_story_animation(
		library,
		"push_lift",
		1.65,
		{
			"Visual:position": [[0.0, Vector2(0, -140)], [0.45, Vector2(0, -126)], [1.25, Vector2(0, -132)], [1.65, Vector2(0, -140)]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.35, 0.2], [1.25, 0.12], [1.65, 0.0]],
			"Visual/FrontArmTablet:rotation": [[0.0, 0.0], [0.4, -0.72], [1.22, -0.9], [1.65, -0.12]],
		}
	)
	_add_story_animation(
		library,
		"kneel_pickup",
		1.55,
		{
			"Visual:position": [[0.0, Vector2(0, -140)], [0.45, Vector2(0, -104)], [1.2, Vector2(0, -112)], [1.55, Vector2(0, -140)]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.45, 0.22], [1.2, 0.18], [1.55, 0.0]],
			"Visual/FrontArmTablet:rotation": [[0.0, 0.0], [0.42, -0.82], [1.15, -0.96], [1.55, 0.0]],
		}
	)
	_add_story_animation(
		library,
		"organize_crowd",
		1.65,
		{
			"Visual/Head:rotation": [[0.0, -0.1], [0.35, 0.16], [0.85, -0.16], [1.65, 0.0]],
			"Visual/FrontArmTablet:rotation": [[0.0, 0.0], [0.32, -0.52], [0.84, 0.36], [1.28, -0.42], [1.65, 0.0]],
		}
	)
	animation_player.add_animation_library(&"", library)


func _add_story_animation(
	library: AnimationLibrary,
	animation_name: String,
	length: float,
	tracks: Dictionary
) -> void:
	var animation := Animation.new()
	animation.length = length
	for property_path: String in tracks:
		var track_index := animation.add_track(Animation.TYPE_VALUE)
		animation.track_set_path(track_index, NodePath(property_path))
		animation.track_set_interpolation_type(track_index, Animation.INTERPOLATION_CUBIC)
		for key_data: Array in tracks[property_path]:
			animation.track_insert_key(track_index, float(key_data[0]), key_data[1])
	library.add_animation(StringName(animation_name), animation)


func _on_story_animation_started(animation_name: StringName) -> void:
	_story_action_active = animation_name in [
		&"write",
		&"look_up",
		&"choice_scan",
		&"push_lift",
		&"kneel_pickup",
		&"organize_crowd",
	]


func _on_story_animation_finished(_animation_name: StringName) -> void:
	_story_action_active = false


func _update_footsteps(delta: float, input_vector: Vector2) -> void:
	if input_vector.length_squared() <= 0.01:
		_footstep_elapsed = 0.0
		return
	_footstep_elapsed += delta
	if _footstep_elapsed < 0.42:
		return
	_footstep_elapsed = 0.0
	_footstep_variant = (_footstep_variant % 6) + 1
	var audio_director := get_node_or_null("/root/AudioDirector")
	if audio_director != null:
		audio_director.play_sfx("sfx.footstep_dry_%02d" % _footstep_variant)
