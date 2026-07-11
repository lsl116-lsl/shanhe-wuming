class_name TransitionLayer
extends CanvasLayer

signal transition_started(mode: String)
signal transition_completed(mode: String)

@onready var cover: ColorRect = %TransitionCover


func _ready() -> void:
	cover.modulate.a = 0.0
	cover.visible = true


func run_transition(mode: String, duration := 0.25) -> Error:
	match mode:
		"fade_out":
			return await fade_out(duration)
		"fade_in":
			return await fade_in(duration)
		"pulse":
			transition_started.emit(mode)
			await fade_out(duration * 0.5)
			await fade_in(duration * 0.5)
			transition_completed.emit(mode)
			return OK
		_:
			push_error("Unsupported transition mode: " + mode)
			return ERR_INVALID_PARAMETER


func fade_out(duration := 0.25) -> Error:
	transition_started.emit("fade_out")
	await _tween_alpha(1.0, duration)
	transition_completed.emit("fade_out")
	return OK


func fade_in(duration := 0.25) -> Error:
	transition_started.emit("fade_in")
	await _tween_alpha(0.0, duration)
	transition_completed.emit("fade_in")
	return OK


func _tween_alpha(target_alpha: float, duration: float) -> void:
	if duration <= 0.0:
		cover.modulate.a = target_alpha
		await get_tree().process_frame
		return
	var tween := create_tween()
	tween.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(cover, "modulate:a", target_alpha, duration)
	await tween.finished
