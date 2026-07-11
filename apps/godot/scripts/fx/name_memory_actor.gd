extends Node2D

@onready var memory_visual: Sprite2D = $MemoryVisual
@onready var animation_player: AnimationPlayer = $AnimationPlayer


func _ready() -> void:
	var animation := Animation.new()
	animation.length = 2.25
	animation.loop_mode = Animation.LOOP_NONE
	var alpha_track := animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(alpha_track, NodePath("MemoryVisual:modulate"))
	animation.track_set_interpolation_type(alpha_track, Animation.INTERPOLATION_CUBIC)
	animation.track_insert_key(alpha_track, 0.0, Color(1, 1, 1, 0))
	animation.track_insert_key(alpha_track, 0.35, Color(1, 1, 1, 0.88))
	animation.track_insert_key(alpha_track, 1.48, Color(0.78, 0.9, 0.92, 0.94))
	animation.track_insert_key(alpha_track, 2.25, Color(1, 1, 1, 0))
	var scale_track := animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(scale_track, NodePath("MemoryVisual:scale"))
	animation.track_set_interpolation_type(scale_track, Animation.INTERPOLATION_CUBIC)
	animation.track_insert_key(scale_track, 0.0, Vector2(1.035, 1.035))
	animation.track_insert_key(scale_track, 2.25, Vector2.ONE)
	var library := AnimationLibrary.new()
	library.add_animation(&"flash", animation)
	animation_player.add_animation_library(&"", library)
