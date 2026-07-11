extends Node

const TIMELINE_PATH := "res://tests/fixtures/p1_timeline.json"
const TEST_SAVE_PATH := "user://p1_infrastructure_test_save.json"

@onready var timeline_runner: TimelineRunner = %TimelineRunner
@onready var camera_director: CameraDirector = %CameraDirector
@onready var camera: Camera2D = %Camera2D
@onready var dialogue_layer: DialogueLayer = %DialogueLayer
@onready var transition_layer: TransitionLayer = %TransitionLayer
@onready var interaction_prompt: InteractionPrompt = %InteractionPrompt
@onready var actor_container: Node2D = %ActorContainer
@onready var interaction_container: Node2D = %InteractionContainer
@onready var timeout_timer: Timer = %TimeoutTimer


func _ready() -> void:
	if not OS.get_cmdline_user_args().has("--p1-test"):
		return
	GameState.reset_state()
	GameState.set_state_value("player.name", "无名测试者", false)
	SaveManager.delete_save(TEST_SAVE_PATH)
	SceneRouter.register_current_scene(scene_file_path)

	camera_director.bind_camera(camera)
	timeline_runner.configure(
		camera_director,
		dialogue_layer,
		transition_layer,
		interaction_prompt,
		actor_container,
		interaction_container
	)
	timeline_runner.interaction_created.connect(_on_interaction_created)
	timeline_runner.timeline_failed.connect(_on_timeline_failed)
	timeout_timer.timeout.connect(_on_timeout)
	timeout_timer.start()

	var load_error := timeline_runner.load_timeline(TIMELINE_PATH)
	if load_error != OK:
		_fail("Timeline JSON failed to load.", load_error)
		return
	var run_error := await timeline_runner.start_timeline()
	if run_error != OK:
		_fail("Timeline execution returned an error.", run_error)


func _on_interaction_created(interactable: InteractableArea2D) -> void:
	await get_tree().process_frame
	interactable.perform_interaction()


func _on_timeline_failed(event_id: String, error: Error) -> void:
	_fail("Timeline event failed: " + event_id, error)


func _on_timeout() -> void:
	_fail("P1 integration flow timed out.", ERR_TIMEOUT)


func _fail(message: String, error: Error) -> void:
	push_error("[P1 FLOW] %s Error=%s" % [message, error_string(error)])
	get_tree().quit(1)
