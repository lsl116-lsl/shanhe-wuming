extends Control

const PLAYABLE_PROLOGUE := "res://scenes/ui/TitleScreen.tscn"

@onready var video: VideoStreamPlayer = %Video
@onready var end_panel: Control = %EndPanel
@onready var pause_hint: Label = %PauseHint


func _ready() -> void:
	%ReplayButton.pressed.connect(_replay)
	%EnterGameButton.pressed.connect(_enter_playable_prologue)
	%BackButton.pressed.connect(_return_to_title)
	video.finished.connect(_on_video_finished)
	end_panel.hide()
	pause_hint.show()
	video.play()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		_return_to_title()
		get_viewport().set_input_as_handled()
		return

	if event.is_action_pressed("ui_accept"):
		if end_panel.visible:
			_enter_playable_prologue()
		else:
			video.paused = not video.paused
			pause_hint.text = "已暂停 · 空格继续 · Esc 返回" if video.paused else "空格暂停 · Esc 返回"
		get_viewport().set_input_as_handled()

	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_R:
		_replay()
		get_viewport().set_input_as_handled()


func _on_video_finished() -> void:
	pause_hint.hide()
	end_panel.show()
	%EnterGameButton.grab_focus()


func _replay() -> void:
	end_panel.hide()
	pause_hint.text = "空格暂停 · Esc 返回"
	pause_hint.show()
	video.stop()
	video.play()


func _enter_playable_prologue() -> void:
	get_tree().change_scene_to_file(PLAYABLE_PROLOGUE)


func _return_to_title() -> void:
	get_tree().change_scene_to_file(PLAYABLE_PROLOGUE)
