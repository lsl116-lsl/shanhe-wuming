class_name InteractableArea2D
extends Area2D

signal interaction_available(interaction_id: String)
signal interaction_unavailable(interaction_id: String)
signal interaction_committed(interaction_id: String, payload: Dictionary)

@export var interaction_id := ""
@export var prompt_text := "按 E 互动"
@export var hold_duration := 0.0
@export var payload: Dictionary = {}

var interaction_enabled := true
var _player_in_range := false
var _hold_elapsed := 0.0
var _prompt_layer: InteractionPrompt


func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	monitoring = interaction_enabled


func _process(delta: float) -> void:
	if not interaction_enabled or not _player_in_range:
		return
	if Input.is_action_pressed("interact"):
		if hold_duration <= 0.0:
			perform_interaction()
			return
		_hold_elapsed += delta
		if _prompt_layer != null:
			_prompt_layer.set_hold_progress(_hold_elapsed / hold_duration)
		if _hold_elapsed >= hold_duration:
			perform_interaction()
	else:
		_hold_elapsed = 0.0
		if _prompt_layer != null:
			_prompt_layer.set_hold_progress(0.0)


func configure(data: Dictionary) -> void:
	interaction_id = str(data.get("interaction_id", interaction_id))
	prompt_text = str(data.get("prompt", prompt_text))
	hold_duration = float(data.get("hold_duration", hold_duration))
	var configured_payload: Variant = data.get("payload", {})
	if configured_payload is Dictionary:
		payload = configured_payload.duplicate(true)


func bind_prompt(prompt: InteractionPrompt) -> void:
	_prompt_layer = prompt


func set_interaction_enabled(enabled: bool) -> void:
	interaction_enabled = enabled
	monitoring = enabled
	if not enabled:
		_player_in_range = false
		_hold_elapsed = 0.0
		if _prompt_layer != null:
			_prompt_layer.hide_prompt()


func perform_interaction() -> void:
	if not interaction_enabled:
		return
	interaction_enabled = false
	monitoring = false
	_hold_elapsed = 0.0
	if _prompt_layer != null:
		_prompt_layer.hide_prompt()
	interaction_committed.emit(interaction_id, payload.duplicate(true))


func _on_body_entered(body: Node) -> void:
	if not interaction_enabled or not body.is_in_group("player"):
		return
	_player_in_range = true
	if _prompt_layer != null:
		_prompt_layer.show_prompt(prompt_text, hold_duration)
	interaction_available.emit(interaction_id)


func _on_body_exited(body: Node) -> void:
	if not body.is_in_group("player"):
		return
	_player_in_range = false
	_hold_elapsed = 0.0
	if _prompt_layer != null:
		_prompt_layer.hide_prompt()
	interaction_unavailable.emit(interaction_id)
