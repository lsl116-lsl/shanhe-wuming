extends Node

const CAPTURES := [
	{
		"scene": "res://scenes/prologue/SC01_Home_Morning.tscn",
		"output": "p6a_sc01_home_morning.png",
	},
	{
		"scene": "res://scenes/prologue/SC02_Xinheng_Desk.tscn",
		"output": "p6a_sc02_xinheng_desk.png",
	},
]

const READY_TIMEOUT_MSEC := 18000


func _ready() -> void:
	Engine.time_scale = 5.0
	_run.call_deferred()


func _run() -> void:
	for config in CAPTURES:
		var scene_path := str(config.get("scene", ""))
		var output_name := str(config.get("output", ""))
		var error := await _capture_scene(scene_path, output_name)
		if error != OK:
			Engine.time_scale = 1.0
			get_tree().quit(error)
			return
	Engine.time_scale = 1.0
	print("[P6-A VISUAL] PASS: captured SC01/SC02 visual samples.")
	get_tree().quit(0)


func _capture_scene(scene_path: String, output_name: String) -> Error:
	var packed := load(scene_path) as PackedScene
	if packed == null:
		push_error("[P6-A VISUAL] could not load scene: " + scene_path)
		return ERR_CANT_OPEN

	var scene := packed.instantiate()
	if scene == null:
		push_error("[P6-A VISUAL] could not instantiate scene: " + scene_path)
		return ERR_CANT_CREATE

	get_tree().root.add_child(scene)
	get_tree().current_scene = scene

	var director := await _wait_for_director_ready(scene, scene_path)
	if director == null:
		scene.queue_free()
		get_tree().current_scene = self
		return ERR_TIMEOUT

	await get_tree().process_frame
	await get_tree().process_frame

	var image := get_viewport().get_texture().get_image()
	if image == null:
		push_error("[P6-A VISUAL] viewport image unavailable for: " + scene_path)
		scene.queue_free()
		get_tree().current_scene = self
		return ERR_UNAVAILABLE

	var review_dir := ProjectSettings.globalize_path("res://review")
	DirAccess.make_dir_recursive_absolute(review_dir)
	var output_path := "%s/%s" % [review_dir, output_name]
	var save_error := image.save_png(output_path)
	if save_error != OK:
		push_error("[P6-A VISUAL] could not save %s: %s" % [output_path, error_string(save_error)])
		scene.queue_free()
		get_tree().current_scene = self
		return save_error

	print("[P6-A VISUAL] " + output_path)
	scene.queue_free()
	get_tree().current_scene = self
	await get_tree().process_frame
	await get_tree().process_frame
	return OK


func _wait_for_director_ready(scene: Node, scene_path: String) -> PrologueStageDirector:
	var deadline := Time.get_ticks_msec() + READY_TIMEOUT_MSEC
	while Time.get_ticks_msec() < deadline:
		var director := scene.find_child("PrologueStageDirector", true, false) as PrologueStageDirector
		if director != null and director.is_ready_for_interaction():
			return director
		await get_tree().process_frame
	var current_event := str(GameState.get_state_value("runtime.current_timeline_event", ""))
	push_error(
		"[P6-A VISUAL] timed out waiting for %s, current timeline event=%s"
		% [scene_path, current_event]
	)
	return null
