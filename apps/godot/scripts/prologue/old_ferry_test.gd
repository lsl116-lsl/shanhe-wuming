extends Node2D

const TITLE_SCENE := "res://scenes/ui/TitleScreen.tscn"
const INTERACT_POSITION := Vector2(1370.0, 540.0)
const INTERACT_RADIUS := 105.0

@onready var player: PlayerController2D = %Player
@onready var interaction_prompt: Label = %InteractionPrompt
@onready var subtitle_label: Label = %SubtitleLabel
@onready var river_morning: AudioStreamPlayer = $RiverMorning
@onready var old_ferry_music: AudioStreamPlayer = $OldFerryMusic

var _has_inspected_post := false


func _ready() -> void:
	SceneRouter.register_current_scene(scene_file_path)
	GameState.set_player_control(true)
	player.interact_pressed.connect(_on_player_interact)
	subtitle_label.text = "洛水旧渡。河雾尚未散去。"
	river_morning.finished.connect(river_morning.play)
	old_ferry_music.finished.connect(old_ferry_music.play)
	if DisplayServer.get_name() != "headless":
		river_morning.play()
		old_ferry_music.play()
	if OS.get_cmdline_user_args().has("--p0-review"):
		_finish_review_capture.call_deferred()


func _process(_delta: float) -> void:
	var can_interact := player.global_position.distance_to(INTERACT_POSITION) <= INTERACT_RADIUS
	interaction_prompt.visible = can_interact and not _has_inspected_post


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause_game"):
		SceneRouter.go_to_scene(TITLE_SCENE)
		get_viewport().set_input_as_handled()


func _exit_tree() -> void:
	if is_instance_valid(river_morning):
		river_morning.stop()
		river_morning.stream = null
	if is_instance_valid(old_ferry_music):
		old_ferry_music.stop()
		old_ferry_music.stream = null


func _finish_review_capture() -> void:
	await get_tree().process_frame
	await get_tree().process_frame
	river_morning.stop()
	old_ferry_music.stop()
	river_morning.stream = null
	old_ferry_music.stream = null
	await get_tree().process_frame
	get_tree().quit(0)


func _on_player_interact() -> void:
	if player.global_position.distance_to(INTERACT_POSITION) > INTERACT_RADIUS:
		return
	_has_inspected_post = true
	interaction_prompt.visible = false
	subtitle_label.text = "木缆被水汽泡得发黑。它还牢牢系着渡船。"
