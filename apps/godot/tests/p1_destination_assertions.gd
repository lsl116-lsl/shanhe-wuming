extends Node

const TEST_SAVE_PATH := "user://p1_infrastructure_test_save.json"

const EXPECTED_STEPS := [
	"camera_move",
	"character_enter",
	"animation_play",
	"dialogue",
	"player_control",
	"interaction",
	"state_set",
	"save_checkpoint",
	"transition",
	"scene_change",
]


func _ready() -> void:
	if not OS.get_cmdline_user_args().has("--p1-test"):
		return
	call_deferred("_run_assertions")


func _run_assertions() -> void:
	await get_tree().process_frame
	var failures: Array[String] = []
	var actual_steps: Array[String] = []
	for entry in GameState.event_log:
		if entry.get("type") == "flow_step":
			actual_steps.append(str(entry.get("payload", {}).get("step", "")))

	if actual_steps != EXPECTED_STEPS:
		failures.append(
			"Flow order mismatch. Expected=%s Actual=%s"
			% [str(EXPECTED_STEPS), str(actual_steps)]
		)
	if GameState.get_state_value("player.can_move", false) != true:
		failures.append("Player control was not granted.")
	if GameState.get_state_value("prologue.p1_interacted", false) != true:
		failures.append("Interaction state was not written.")
	if SceneRouter.current_scene_path != scene_file_path:
		failures.append("SceneRouter did not register the destination scene.")

	var save_result := SaveManager.read_save(TEST_SAVE_PATH)
	if not save_result.get("ok", false):
		failures.append("Save file was not created or could not be parsed.")
	else:
		var save_data: Dictionary = save_result.get("data", {})
		if save_data.get("checkpoint", "") != "P1_INFRA_COMPLETE":
			failures.append("Checkpoint was not persisted.")
		var snapshot: Dictionary = save_data.get("state_snapshot", {})
		var prologue: Dictionary = snapshot.get("prologue", {})
		if prologue.get("p1_interacted", false) != true:
			failures.append("Saved state does not contain the interaction result.")
		if save_data.get("current_timeline_event", "") != "P1-EVT-08-SAVE":
			failures.append("Saved timeline cursor is incorrect.")

	SaveManager.delete_save(TEST_SAVE_PATH)
	if failures.is_empty():
		print(
			"[P1 FLOW] PASS: camera -> actor -> animation -> dialogue -> control "
			+ "-> interaction -> state -> save -> transition -> scene."
		)
		get_tree().quit(0)
		return
	for failure in failures:
		push_error("[P1 FLOW] " + failure)
	get_tree().quit(1)
