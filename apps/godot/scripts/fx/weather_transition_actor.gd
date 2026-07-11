extends Node2D

@onready var animation_player: AnimationPlayer = $AnimationPlayer


func _ready() -> void:
	var library := AnimationLibrary.new()
	var animation := Animation.new()
	animation.length = 7.0
	animation.loop_mode = Animation.LOOP_NONE
	_add_color_track(
		animation,
		"../../NightFar:modulate",
		[[0.0, Color(1, 1, 1, 0)], [7.0, Color(1, 1, 1, 1)]]
	)
	_add_color_track(
		animation,
		"../../NightMid:modulate",
		[[0.0, Color(1, 1, 1, 0)], [7.0, Color(1, 1, 1, 1)]]
	)
	_add_color_track(
		animation,
		"../../NightNear:modulate",
		[[0.0, Color(1, 1, 1, 0)], [7.0, Color(1, 1, 1, 1)]]
	)
	_add_color_track(
		animation,
		"../../RainBack:modulate",
		[[0.0, Color(0.82, 0.9, 0.92, 0.15)], [7.0, Color(0.82, 0.9, 0.92, 0.48)]]
	)
	_add_color_track(
		animation,
		"../../RainFront:modulate",
		[[0.0, Color(0.78, 0.87, 0.9, 0.08)], [7.0, Color(0.78, 0.87, 0.9, 0.42)]]
	)
	_add_position_track(
		animation,
		"../../RainBack:position",
		[[0.0, Vector2(1100, 300)], [7.0, Vector2(1060, 410)]]
	)
	_add_position_track(
		animation,
		"../../RainFront:position",
		[[0.0, Vector2(1100, 240)], [7.0, Vector2(1040, 420)]]
	)
	library.add_animation(&"evening_to_night", animation)
	animation_player.add_animation_library(&"", library)


func _add_color_track(animation: Animation, path: String, keys: Array) -> void:
	var track := animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(track, NodePath(path))
	animation.track_set_interpolation_type(track, Animation.INTERPOLATION_CUBIC)
	for key in keys:
		animation.track_insert_key(track, float(key[0]), key[1])


func _add_position_track(animation: Animation, path: String, keys: Array) -> void:
	var track := animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(track, NodePath(path))
	animation.track_set_interpolation_type(track, Animation.INTERPOLATION_LINEAR)
	for key in keys:
		animation.track_insert_key(track, float(key[0]), key[1])
