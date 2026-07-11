extends SceneTree

const PLAYER_SCENE := "res://scenes/characters/Player.tscn"
const OLD_FERRY_SCENE := "res://scenes/prologue/SC01_OldFerry_Test.tscn"

var _interaction_received := false


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	var game_state := root.get_node_or_null("GameState")
	if game_state != null:
		game_state.set_player_control(true)
	var packed := load(PLAYER_SCENE) as PackedScene
	if packed == null:
		push_error("[P0 MOVEMENT] Unable to load player scene.")
		quit(1)
		return

	var player := packed.instantiate() as PlayerController2D
	root.add_child(player)
	player.global_position = Vector2(500.0, 550.0)
	player.interact_pressed.connect(_on_interact_pressed)
	await physics_frame

	var start_x := player.global_position.x
	Input.action_press("move_right")
	for _frame in range(8):
		await physics_frame
	Input.action_release("move_right")

	if player.global_position.x <= start_x + 1.0:
		push_error("[P0 MOVEMENT] Player did not move right.")
		player.free()
		quit(1)
		return

	Input.action_press("interact")
	await physics_frame
	Input.action_release("interact")
	await physics_frame
	if not _interaction_received:
		push_error("[P0 MOVEMENT] Interact action did not emit a signal.")
		player.free()
		quit(1)
		return

	print(
		"[P0 MOVEMENT] PASS: keyboard action moved player %.2f px and interact emitted."
		% (player.global_position.x - start_x)
	)
	player.free()
	await process_frame

	var ferry_packed := load(OLD_FERRY_SCENE) as PackedScene
	var ferry := ferry_packed.instantiate()
	root.add_child(ferry)
	await process_frame
	var ferry_player := ferry.get_node("Player") as PlayerController2D
	var subtitle := ferry.get_node("UI/SubtitlePanel/Margin/SubtitleLabel") as Label
	ferry_player.global_position = Vector2(1370.0, 540.0)
	ferry_player.interact_pressed.emit()
	await process_frame
	if subtitle.text != "木缆被水汽泡得发黑。它还牢牢系着渡船。":
		push_error("[P0 MOVEMENT] Old-ferry interaction did not update the subtitle.")
		ferry.free()
		quit(1)
		return
	print("[P0 INTERACTION] PASS: old-ferry post updated the Chinese subtitle.")
	ferry.free()
	quit(0)


func _on_interact_pressed() -> void:
	_interaction_received = true
