class_name InteractionPrompt
extends CanvasLayer

signal prompt_shown(text: String)
signal prompt_hidden

@onready var prompt_panel: PanelContainer = %PromptPanel
@onready var prompt_label: Label = %PromptLabel
@onready var hold_progress: ProgressBar = %HoldProgress


func _ready() -> void:
	hide_prompt()


func show_prompt(text: String, hold_duration := 0.0) -> void:
	if prompt_panel == null or prompt_label == null or hold_progress == null:
		return
	prompt_label.text = text
	hold_progress.visible = hold_duration > 0.0
	hold_progress.value = 0.0
	prompt_panel.visible = true
	prompt_shown.emit(text)


func set_hold_progress(progress: float) -> void:
	if hold_progress == null:
		return
	hold_progress.value = clampf(progress, 0.0, 1.0) * 100.0


func hide_prompt() -> void:
	if prompt_panel == null or hold_progress == null:
		return
	prompt_panel.visible = false
	hold_progress.value = 0.0
	prompt_hidden.emit()
