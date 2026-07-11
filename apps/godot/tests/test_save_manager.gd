extends Node

const TEST_SAVE_PATH := "user://p1_save_manager_unit.json"


func _ready() -> void:
	if not OS.get_cmdline_user_args().has("--p1-save-test"):
		return
	call_deferred("_run_test")


func _run_test() -> void:
	SaveManager.delete_save(TEST_SAVE_PATH)
	GameState.reset_state()
	GameState.set_state_value("player.name", "存档测试")
	GameState.set_state_value("prologue.p1_interacted", true)
	var error := SaveManager.save_game("P1_SAVE_UNIT", TEST_SAVE_PATH)
	if error != OK:
		_fail("Save failed.", error)
		return

	GameState.set_state_value("player.name", "已被改写")
	error = SaveManager.load_game(TEST_SAVE_PATH)
	if error != OK:
		_fail("Load failed.", error)
		return
	if GameState.get_state_value("player.name", "") != "存档测试":
		_fail("Player name was not restored.", ERR_INVALID_DATA)
		return
	if GameState.get_state_value("prologue.p1_interacted", false) != true:
		_fail("Nested state was not restored.", ERR_INVALID_DATA)
		return

	SaveManager.delete_save(TEST_SAVE_PATH)
	print("[P1 SAVE] PASS: snapshot and event log saved and restored.")
	get_tree().quit(0)


func _fail(message: String, error: Error) -> void:
	SaveManager.delete_save(TEST_SAVE_PATH)
	push_error("[P1 SAVE] %s Error=%s" % [message, error_string(error)])
	get_tree().quit(1)
