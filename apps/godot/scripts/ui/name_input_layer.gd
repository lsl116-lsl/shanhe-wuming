class_name NameInputLayer
extends CanvasLayer

signal name_submitted(player_name: String)

@onready var panel: PanelContainer = %NamePanel
@onready var dim: ColorRect = %Dim
@onready var title_label: Label = %TitleLabel
@onready var hint_label: Label = %HintLabel
@onready var name_edit: LineEdit = %NameEdit
@onready var validation_label: Label = %ValidationLabel
@onready var confirm_button: Button = %ConfirmButton


func _ready() -> void:
	panel.visible = false
	dim.visible = false
	confirm_button.pressed.connect(_on_confirm_pressed)
	name_edit.text_submitted.connect(_on_text_submitted)
	name_edit.text_changed.connect(_on_text_changed)


func show_input(title: String, hint: String, prefill := "") -> void:
	title_label.text = title
	hint_label.text = hint
	name_edit.text = prefill
	validation_label.text = ""
	panel.visible = true
	dim.visible = true
	name_edit.grab_focus()
	name_edit.caret_column = name_edit.text.length()


func hide_input() -> void:
	panel.visible = false
	dim.visible = false
	name_edit.release_focus()


func submit_name(value: String) -> Error:
	var cleaned := value.strip_edges()
	if cleaned.is_empty():
		validation_label.text = "名字不能为空。"
		return ERR_INVALID_DATA
	if cleaned.length() > 8:
		validation_label.text = "请写下 1—8 个字。"
		return ERR_PARAMETER_RANGE_ERROR
	hide_input()
	name_submitted.emit(cleaned)
	return OK


func _on_confirm_pressed() -> void:
	submit_name(name_edit.text)


func _on_text_submitted(value: String) -> void:
	submit_name(value)


func _on_text_changed(value: String) -> void:
	if value.strip_edges().length() <= 8:
		validation_label.text = ""
	else:
		validation_label.text = "最多写下 8 个字。"
