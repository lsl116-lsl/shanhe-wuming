class_name CameraDirector
extends Node

signal camera_bound(camera: Camera2D)
signal move_started(target: Vector2, duration: float)
signal move_completed(target: Vector2)
signal focus_completed(node: Node2D)
signal shake_completed(duration: float, strength: float)

var camera: Camera2D


func bind_camera(target_camera: Camera2D) -> void:
	camera = target_camera
	camera_bound.emit(camera)


func move_to(target: Vector2, duration := 0.0) -> Error:
	if camera == null:
		push_error("CameraDirector has no bound Camera2D.")
		return ERR_UNCONFIGURED
	move_started.emit(target, duration)
	if duration <= 0.0:
		camera.global_position = target
	else:
		var tween := create_tween()
		tween.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		tween.tween_property(camera, "global_position", target, duration)
		await tween.finished
	move_completed.emit(target)
	return OK


func focus_node(target_node: Node2D, duration := 0.0, offset := Vector2.ZERO) -> Error:
	if target_node == null:
		return ERR_INVALID_PARAMETER
	var error := await move_to(target_node.global_position + offset, duration)
	if error == OK:
		focus_completed.emit(target_node)
	return error


func return_to(target: Vector2, duration := 0.0) -> Error:
	return await move_to(target, duration)


func shake(duration := 0.35, strength := 7.0) -> Error:
	if camera == null:
		push_error("CameraDirector has no bound Camera2D.")
		return ERR_UNCONFIGURED
	var settings_manager := get_node_or_null("/root/SettingsManager")
	if settings_manager != null and not bool(
		settings_manager.get_setting_value("screen_shake", true)
	):
		shake_completed.emit(duration, strength)
		return OK
	if duration <= 0.0 or strength <= 0.0:
		shake_completed.emit(duration, strength)
		return OK
	var original_offset := camera.offset
	var elapsed := 0.0
	while elapsed < duration:
		var delta := get_process_delta_time()
		elapsed += delta
		var amount := (1.0 - minf(1.0, elapsed / duration)) * strength
		camera.offset = Vector2(
			sin(elapsed * 81.0) * amount,
			cos(elapsed * 67.0) * amount * 0.58
		)
		await get_tree().process_frame
	camera.offset = original_offset
	shake_completed.emit(duration, strength)
	return OK
