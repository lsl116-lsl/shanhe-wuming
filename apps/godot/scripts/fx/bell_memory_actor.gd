extends CanvasLayer

const MEMORY_DURATION_SECONDS := 27.0

@onready var animation_player: AnimationPlayer = $AnimationPlayer


func _ready() -> void:
	var library := AnimationLibrary.new()
	var animation := Animation.new()
	animation.length = MEMORY_DURATION_SECONDS
	animation.loop_mode = Animation.LOOP_NONE
	_add_layer_fade(animation, "Black", 0.0, 0.45, 26.4, 27.0, 0.98)
	_add_layer_fade(animation, "Water", 0.2, 1.1, 4.2, 5.3, 1.0)
	_add_layer_fade(animation, "CityFire", 4.1, 5.2, 8.1, 9.0, 1.0)
	_add_layer_fade(animation, "BrokenRituals", 8.0, 9.0, 11.6, 12.5, 1.0)
	_add_layer_fade(animation, "ScrapedRegistry", 11.4, 12.3, 15.9, 16.8, 1.0)
	_add_layer_fade(animation, "WetHand", 15.7, 16.7, 19.7, 20.6, 1.0)
	_add_layer_fade(animation, "BellSinking", 19.4, 20.4, 26.4, 27.0, 1.0)
	_add_position_track(
		animation,
		"BellSinking:position",
		[[19.4, Vector2(640, 308)], [26.8, Vector2(640, 416)]]
	)
	_add_scale_track(
		animation,
		"BellSinking:scale",
		[[19.4, Vector2(1.04, 1.04)], [26.8, Vector2(0.94, 0.94)]]
	)
	library.add_animation(&"memory", animation)
	animation_player.add_animation_library(&"", library)


func get_memory_duration_seconds() -> float:
	return MEMORY_DURATION_SECONDS


func _add_layer_fade(
	animation: Animation,
	node_name: String,
	fade_in_start: float,
	fade_in_end: float,
	fade_out_start: float,
	fade_out_end: float,
	max_alpha: float
) -> void:
	var track := animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(track, NodePath("%s:modulate" % node_name))
	animation.track_set_interpolation_type(track, Animation.INTERPOLATION_CUBIC)
	animation.track_insert_key(track, 0.0, Color(1, 1, 1, 0))
	animation.track_insert_key(track, fade_in_start, Color(1, 1, 1, 0))
	animation.track_insert_key(track, fade_in_end, Color(1, 1, 1, max_alpha))
	animation.track_insert_key(track, fade_out_start, Color(1, 1, 1, max_alpha))
	animation.track_insert_key(track, fade_out_end, Color(1, 1, 1, 0))


func _add_position_track(animation: Animation, path: String, keys: Array) -> void:
	var track := animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(track, NodePath(path))
	animation.track_set_interpolation_type(track, Animation.INTERPOLATION_CUBIC)
	for key in keys:
		animation.track_insert_key(track, float(key[0]), key[1])


func _add_scale_track(animation: Animation, path: String, keys: Array) -> void:
	var track := animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(track, NodePath(path))
	animation.track_set_interpolation_type(track, Animation.INTERPOLATION_CUBIC)
	for key in keys:
		animation.track_insert_key(track, float(key[0]), key[1])
