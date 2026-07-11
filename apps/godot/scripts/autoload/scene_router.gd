extends Node

signal scene_change_started(path: String)
signal scene_changed(path: String)
signal scene_change_failed(path: String, error: Error)

var current_scene_path := ""


func _ready() -> void:
	call_deferred("_synchronize_current_scene")


func _synchronize_current_scene() -> void:
	var current_scene := get_tree().current_scene
	if current_scene != null and not current_scene.scene_file_path.is_empty():
		register_current_scene(current_scene.scene_file_path)


func register_current_scene(path: String) -> void:
	current_scene_path = path
	GameState.set_state_value("runtime.current_scene", path, false)


func go_to_scene(path: String) -> Error:
	if path.is_empty() or not ResourceLoader.exists(path):
		scene_change_failed.emit(path, ERR_FILE_NOT_FOUND)
		return ERR_FILE_NOT_FOUND

	scene_change_started.emit(path)
	register_current_scene(path)
	var error := get_tree().change_scene_to_file(path)
	if error != OK:
		scene_change_failed.emit(path, error)
		return error
	call_deferred("_emit_scene_changed_after_frame", path)
	return OK


func _emit_scene_changed_after_frame(path: String) -> void:
	await get_tree().process_frame
	scene_changed.emit(path)


func reload_current_scene() -> Error:
	if current_scene_path.is_empty():
		return ERR_DOES_NOT_EXIST
	return go_to_scene(current_scene_path)
