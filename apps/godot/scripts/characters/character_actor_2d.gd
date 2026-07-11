class_name CharacterActor2D
extends Node2D

@export_enum(
	"mother",
	"xinheng",
	"hean",
	"boat_owner",
	"ferry_worker",
	"ferry_woman",
	"hanning",
	"hanning_mother",
	"liuniang",
	"refugee_old",
	"refugee_mother",
	"refugee_man"
)
var animation_profile := "mother"

@onready var visual: Node2D = $Visual
@onready var body: Sprite2D = $Visual/Body
@onready var head: Sprite2D = $Visual/Head
@onready var front_arm: Sprite2D = $Visual/FrontArm
@onready var held_prop: Sprite2D = $Visual/HeldProp
@onready var animation_player: AnimationPlayer = $AnimationPlayer


func _ready() -> void:
	_build_animation_library()
	if animation_player.has_animation(&"idle"):
		animation_player.play(&"idle")


func play_story_action(animation_name: StringName) -> Error:
	if not animation_player.has_animation(animation_name):
		return ERR_DOES_NOT_EXIST
	animation_player.play(animation_name)
	return OK


func _build_animation_library() -> void:
	var library := AnimationLibrary.new()
	_add_idle(library)
	match animation_profile:
		"mother":
			_add_mother_animations(library)
		"xinheng":
			_add_xinheng_animations(library)
		"hean":
			_add_hean_animations(library)
		"boat_owner":
			_add_boat_owner_animations(library)
		"ferry_worker", "ferry_woman":
			_add_ferry_animations(library)
		"hanning":
			_add_hanning_animations(library)
		"hanning_mother":
			_add_hanning_mother_animations(library)
		"liuniang":
			_add_liuniang_animations(library)
		"refugee_old", "refugee_mother", "refugee_man":
			_add_refugee_animations(library)
	animation_player.add_animation_library(&"", library)


func _add_idle(library: AnimationLibrary) -> void:
	_add_animation(
		library,
		"idle",
		2.8,
		{
			"Visual/Body:position": [[0.0, Vector2.ZERO], [1.4, Vector2(0, -1.5)], [2.8, Vector2.ZERO]],
			"Visual/Head:rotation": [[0.0, -0.006], [1.4, 0.008], [2.8, -0.006]],
		},
		true
	)


func _add_mother_animations(library: AnimationLibrary) -> void:
	_add_animation(
		library,
		"wash_basin",
		1.8,
		{
			"Visual/Body:rotation": [[0.0, 0.0], [0.35, 0.035], [1.45, 0.028], [1.8, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, -0.04], [0.35, 0.2], [0.85, -0.13], [1.35, 0.18], [1.8, -0.04]],
			"Visual/HeldProp:position": [[0.0, Vector2.ZERO], [0.9, Vector2(0, 3)], [1.8, Vector2.ZERO]],
		}
	)
	_add_counting_animation(library, "count_grain", -0.18)
	_add_counting_animation(library, "count_wood", 0.18)
	_add_animation(
		library,
		"look_river",
		1.55,
		{
			"Visual/Head:rotation": [[0.0, 0.0], [0.45, -0.17], [1.25, -0.17], [1.55, -0.05]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.35, 0.08], [1.3, 0.08], [1.55, 0.0]],
			"Visual/Body:position": [[0.0, Vector2.ZERO], [0.45, Vector2(-2, 0)], [1.55, Vector2.ZERO]],
		}
	)
	_add_animation(
		library,
		"resume_work",
		0.85,
		{
			"Visual/Head:rotation": [[0.0, -0.14], [0.45, 0.06], [0.85, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, 0.08], [0.5, 0.2], [0.85, 0.0]],
		}
	)


func _add_counting_animation(
	library: AnimationLibrary,
	animation_name: String,
	head_angle: float
) -> void:
	_add_animation(
		library,
		animation_name,
		1.35,
		{
			"Visual/Head:rotation": [[0.0, 0.0], [0.25, head_angle], [1.1, head_angle], [1.35, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.28, 0.18], [0.52, -0.08], [0.78, 0.18], [1.02, -0.06], [1.35, 0.0]],
		}
	)


func _add_xinheng_animations(library: AnimationLibrary) -> void:
	_add_animation(
		library,
		"write",
		1.6,
		{
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.25, -0.22], [0.65, -0.1], [1.0, -0.25], [1.35, -0.12], [1.6, 0.0]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.3, 0.11], [1.3, 0.11], [1.6, 0.0]],
		}
	)
	_add_animation(
		library,
		"pause_pen",
		1.1,
		{
			"Visual/FrontArm:rotation": [[0.0, -0.12], [0.2, -0.24], [0.85, -0.24], [1.1, -0.08]],
			"Visual/Head:rotation": [[0.0, 0.08], [0.42, -0.05], [1.1, -0.05]],
		}
	)
	_add_animation(
		library,
		"look_over_tablet",
		1.25,
		{
			"Visual/Head:position": [[0.0, Vector2.ZERO], [0.38, Vector2(0, 5)], [0.85, Vector2(0, 5)], [1.25, Vector2.ZERO]],
			"Visual/HeldProp:rotation": [[0.0, 0.0], [0.4, -0.08], [1.0, -0.08], [1.25, 0.0]],
		}
	)
	_add_animation(
		library,
		"hand_tablet",
		1.45,
		{
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.55, -0.48], [1.05, -0.48], [1.45, 0.0]],
			"Visual/HeldProp:position": [[0.0, Vector2.ZERO], [0.55, Vector2(35, 8)], [1.05, Vector2(35, 8)], [1.45, Vector2.ZERO]],
		}
	)


func _add_hean_animations(library: AnimationLibrary) -> void:
	_add_animation(
		library,
		"carry_firewood",
		1.15,
		{
			"Visual:rotation": [[0.0, 0.0], [0.3, 0.075], [0.92, 0.075], [1.15, 0.03]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.35, -0.08], [1.15, -0.04]],
		}
	)
	_add_animation(
		library,
		"walk_fast",
		0.72,
		{
			"Visual/Body:position": [[0.0, Vector2.ZERO], [0.18, Vector2(0, -4)], [0.36, Vector2.ZERO], [0.54, Vector2(0, -4)], [0.72, Vector2.ZERO]],
			"Visual/Body:rotation": [[0.0, -0.025], [0.18, 0.04], [0.36, -0.025], [0.54, 0.04], [0.72, -0.025]],
			"Visual/FrontArm:rotation": [[0.0, -0.08], [0.36, 0.16], [0.72, -0.08]],
		},
		true
	)
	_add_animation(
		library,
		"place_porridge",
		1.45,
		{
			"Visual/Body:rotation": [[0.0, 0.04], [0.45, 0.13], [1.05, 0.13], [1.45, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.45, -0.42], [1.05, -0.42], [1.45, 0.0]],
			"Visual/HeldProp:position": [[0.0, Vector2.ZERO], [0.45, Vector2(41, 18)], [1.05, Vector2(52, 27)], [1.45, Vector2.ZERO]],
		}
	)
	_add_animation(
		library,
		"count_jars",
		1.55,
		{
			"Visual/Head:rotation": [[0.0, 0.0], [0.3, -0.18], [0.72, 0.2], [1.12, -0.1], [1.55, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.35, -0.2], [0.75, 0.12], [1.15, -0.22], [1.55, 0.0]],
		}
	)
	_add_animation(
		library,
		"pour_broken_rice",
		2.8,
		{
			"Visual:position": [[0.0, Vector2.ZERO], [0.7, Vector2(0, 23)], [2.25, Vector2(0, 23)], [2.8, Vector2.ZERO]],
			"Visual/Body:rotation": [[0.0, 0.0], [0.65, 0.16], [2.25, 0.16], [2.8, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.8, -0.58], [1.45, -0.76], [2.2, -0.58], [2.8, 0.0]],
			"Visual/HeldProp:position": [[0.0, Vector2.ZERO], [0.75, Vector2(45, 20)], [1.55, Vector2(61, 38)], [2.25, Vector2(45, 20)], [2.8, Vector2.ZERO]],
			"Visual/HeldProp:rotation": [[0.0, 0.0], [0.85, -0.22], [1.55, -0.52], [2.3, -0.22], [2.8, 0.0]],
		}
	)
	_add_animation(
		library,
		"look_after_player",
		1.25,
		{
			"Visual/Head:rotation": [[0.0, 0.0], [0.38, -0.23], [1.25, -0.23]],
			"Visual/Body:rotation": [[0.0, 0.0], [0.46, -0.045], [1.25, -0.045]],
		}
	)
	_add_animation(
		library,
		"drag_bucket",
		1.75,
		{
			"Visual:position": [[0.0, Vector2.ZERO], [0.42, Vector2(18, 0)], [0.9, Vector2(36, 2)], [1.32, Vector2(50, -1)], [1.75, Vector2(56, 0)]],
			"Visual/Body:rotation": [[0.0, 0.02], [0.45, 0.18], [1.3, 0.13], [1.75, 0.04]],
			"Visual/FrontArm:rotation": [[0.0, -0.1], [0.42, -0.68], [1.28, -0.76], [1.75, -0.36]],
			"Visual/HeldProp:position": [[0.0, Vector2.ZERO], [0.55, Vector2(56, 26)], [1.35, Vector2(78, 31)], [1.75, Vector2(68, 26)]],
		}
	)
	_add_animation(
		library,
		"brace_cart",
		1.55,
		{
			"Visual:position": [[0.0, Vector2.ZERO], [0.45, Vector2(18, 7)], [1.35, Vector2(18, 7)], [1.55, Vector2(12, 3)]],
			"Visual/Body:rotation": [[0.0, 0.04], [0.42, 0.27], [1.35, 0.27], [1.55, 0.14]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.42, 0.18], [1.35, 0.12]],
			"Visual/FrontArm:rotation": [[0.0, -0.08], [0.42, -1.0], [1.35, -1.05], [1.55, -0.72]],
		}
	)


func _add_boat_owner_animations(library: AnimationLibrary) -> void:
	_add_animation(
		library,
		"dock_brace",
		1.4,
		{
			"Visual/Body:rotation": [[0.0, 0.0], [0.38, -0.11], [0.92, -0.07], [1.4, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.38, 0.34], [0.92, 0.23], [1.4, 0.0]],
		}
	)
	_add_animation(
		library,
		"call_news",
		1.8,
		{
			"Visual/Body:rotation": [[0.0, 0.0], [0.35, -0.04], [1.45, -0.04], [1.8, 0.0]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.35, -0.12], [1.35, -0.12], [1.8, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.35, -0.52], [1.35, -0.52], [1.8, 0.0]],
			"Visual/Head:scale": [[0.0, Vector2.ONE], [0.55, Vector2(1.02, 1.02)], [1.35, Vector2(1.02, 1.02)], [1.8, Vector2.ONE]],
		}
	)


func _add_ferry_animations(library: AnimationLibrary) -> void:
	_add_animation(
		library,
		"work_loop",
		1.5,
		{
			"Visual/FrontArm:rotation": [[0.0, -0.12], [0.75, 0.18], [1.5, -0.12]],
			"Visual/Body:rotation": [[0.0, -0.015], [0.75, 0.025], [1.5, -0.015]],
		},
		true
	)
	_add_animation(
		library,
		"react_stop",
		1.1,
		{
			"Visual/FrontArm:rotation": [[0.0, 0.18], [0.22, 0.0], [1.1, 0.0]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.35, -0.19], [1.1, -0.19]],
		}
	)
	_add_animation(
		library,
		"murmur",
		1.35,
		{
			"Visual/Head:rotation": [[0.0, -0.1], [0.4, 0.14], [0.82, -0.06], [1.35, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.5, -0.16], [1.0, 0.08], [1.35, 0.0]],
		}
	)


func _add_hanning_animations(library: AnimationLibrary) -> void:
	_add_animation(
		library,
		"press_sleeve",
		1.6,
		{
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.35, -0.48], [1.35, -0.48], [1.6, -0.31]],
			"Visual/HeldProp:position": [[0.0, Vector2.ZERO], [0.35, Vector2(-12, 3)], [1.6, Vector2(-12, 3)]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.45, 0.17], [1.6, 0.17]],
			"Visual/Body:position": [[0.0, Vector2.ZERO], [0.4, Vector2(-4, 0)], [1.6, Vector2(-4, 0)]],
		}
	)
	_add_animation(
		library,
		"step_back",
		1.0,
		{
			"Visual:position": [[0.0, Vector2.ZERO], [0.45, Vector2(-14, 0)], [1.0, Vector2(-14, 0)]],
			"Visual/Head:rotation": [[0.0, 0.17], [0.35, 0.26], [1.0, 0.2]],
		}
	)
	_add_animation(
		library,
		"rush_records",
		1.05,
		{
			"Visual:position": [[0.0, Vector2.ZERO], [0.32, Vector2(22, -2)], [0.72, Vector2(50, 0)], [1.05, Vector2(62, 0)]],
			"Visual/Body:rotation": [[0.0, 0.0], [0.28, -0.18], [1.05, -0.12]],
			"Visual/FrontArm:rotation": [[0.0, -0.18], [0.35, -0.78], [1.05, -0.9]],
			"Visual/Head:rotation": [[0.0, 0.08], [0.3, -0.2], [1.05, -0.18]],
		}
	)
	_add_animation(
		library,
		"struggle",
		1.2,
		{
			"Visual:position": [[0.0, Vector2(18, 0)], [0.25, Vector2(34, 0)], [0.5, Vector2(14, 0)], [0.75, Vector2(30, 0)], [1.2, Vector2(20, 0)]],
			"Visual/FrontArm:rotation": [[0.0, -0.7], [0.25, -1.05], [0.5, -0.5], [0.75, -1.0], [1.2, -0.7]],
			"Visual/Head:rotation": [[0.0, -0.14], [0.6, -0.26], [1.2, -0.18]],
		}
	)
	_add_animation(
		library,
		"kneel_records",
		1.5,
		{
			"Visual:position": [[0.0, Vector2.ZERO], [0.45, Vector2(18, 28)], [1.22, Vector2(18, 28)], [1.5, Vector2(4, 10)]],
			"Visual/Body:rotation": [[0.0, 0.0], [0.42, 0.23], [1.22, 0.23], [1.5, 0.1]],
			"Visual/FrontArm:rotation": [[0.0, -0.3], [0.45, -1.02], [1.22, -1.12], [1.5, -0.6]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.42, 0.22], [1.22, 0.18], [1.5, 0.04]],
		}
	)


func _add_hanning_mother_animations(library: AnimationLibrary) -> void:
	_add_animation(
		library,
		"block_question",
		1.55,
		{
			"Visual:position": [[0.0, Vector2.ZERO], [0.45, Vector2(-18, 0)], [1.55, Vector2(-18, 0)]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.4, -0.62], [1.25, -0.62], [1.55, -0.46]],
			"Visual/HeldProp:position": [[0.0, Vector2.ZERO], [0.42, Vector2(-8, -4)], [1.55, Vector2(-8, -4)]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.42, -0.12], [1.55, -0.12]],
		}
	)
	_add_animation(
		library,
		"shield_hanning",
		1.25,
		{
			"Visual/Body:rotation": [[0.0, 0.0], [0.42, -0.07], [1.25, -0.07]],
			"Visual/FrontArm:rotation": [[0.0, -0.2], [0.42, -0.72], [1.25, -0.72]],
		}
	)


func _add_liuniang_animations(library: AnimationLibrary) -> void:
	_add_animation(
		library,
		"sing_old_song",
		3.4,
		{
			"Visual/Head:rotation": [[0.0, 0.0], [0.8, -0.1], [1.7, 0.04], [2.6, -0.08], [3.4, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.7, -0.16], [1.7, 0.08], [2.7, -0.14], [3.4, 0.0]],
			"Visual/Body:position": [[0.0, Vector2.ZERO], [1.7, Vector2(0, -2)], [3.4, Vector2.ZERO]],
		}
	)
	_add_animation(
		library,
		"song_stops",
		1.4,
		{
			"Visual/Head:rotation": [[0.0, -0.08], [0.25, 0.0], [1.4, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, -0.14], [0.28, 0.0], [1.4, 0.0]],
			"Visual/HeldProp:position": [[0.0, Vector2.ZERO], [0.28, Vector2(0, 2)], [1.4, Vector2(0, 2)]],
		}
	)
	_add_animation(
		library,
		"hold_child",
		1.3,
		{
			"Visual/Body:rotation": [[0.0, 0.0], [0.35, 0.08], [1.3, 0.05]],
			"Visual/FrontArm:rotation": [[0.0, -0.08], [0.36, -0.54], [1.3, -0.48]],
			"Visual/HeldProp:position": [[0.0, Vector2.ZERO], [0.36, Vector2(20, 12)], [1.3, Vector2(20, 12)]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.42, -0.16], [1.3, -0.12]],
		}
	)
	_add_animation(
		library,
		"call_names",
		1.8,
		{
			"Visual/Head:rotation": [[0.0, -0.08], [0.35, 0.18], [0.9, -0.16], [1.4, 0.16], [1.8, 0.0]],
			"Visual/FrontArm:rotation": [[0.0, -0.12], [0.35, -0.54], [0.9, 0.28], [1.4, -0.48], [1.8, 0.0]],
			"Visual/Body:position": [[0.0, Vector2.ZERO], [0.9, Vector2(0, -3)], [1.8, Vector2.ZERO]],
		}
	)


func _add_refugee_animations(library: AnimationLibrary) -> void:
	_add_animation(
		library,
		"enter_burdened",
		1.4,
		{
			"Visual:rotation": [[0.0, -0.055], [0.45, 0.035], [0.9, -0.045], [1.4, 0.0]],
			"Visual:position": [[0.0, Vector2.ZERO], [0.35, Vector2(0, -5)], [0.7, Vector2.ZERO], [1.05, Vector2(0, -4)], [1.4, Vector2.ZERO]],
			"Visual/FrontArm:rotation": [[0.0, -0.08], [0.7, 0.15], [1.4, -0.08]],
		}
	)
	_add_animation(
		library,
		"guard_burden",
		1.35,
		{
			"Visual/Body:rotation": [[0.0, 0.0], [0.32, 0.08], [1.35, 0.08]],
			"Visual/FrontArm:rotation": [[0.0, 0.0], [0.38, -0.3], [1.35, -0.3]],
			"Visual/Head:rotation": [[0.0, 0.0], [0.38, 0.12], [1.35, 0.12]],
		}
	)


func _add_animation(
	library: AnimationLibrary,
	animation_name: String,
	length: float,
	tracks: Dictionary,
	loop := false
) -> void:
	var animation := Animation.new()
	animation.length = length
	animation.loop_mode = Animation.LOOP_LINEAR if loop else Animation.LOOP_NONE
	for property_path: String in tracks:
		var track_index := animation.add_track(Animation.TYPE_VALUE)
		animation.track_set_path(track_index, NodePath(property_path))
		animation.track_set_interpolation_type(track_index, Animation.INTERPOLATION_CUBIC)
		for key_data: Array in tracks[property_path]:
			animation.track_insert_key(track_index, float(key_data[0]), key_data[1])
	library.add_animation(StringName(animation_name), animation)
