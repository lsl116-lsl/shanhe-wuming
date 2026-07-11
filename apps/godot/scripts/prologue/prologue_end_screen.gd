extends Control

const REVIEW_PATH := "res://content/prologue/prologue_review.zh-CN.json"
const ASSET_MANIFEST_PATH := "res://content/prologue/asset_manifest.json"
const TITLE_SCENE := "res://scenes/ui/TitleScreen.tscn"

@onready var title_label: Label = %TitleLabel
@onready var subtitle_label: Label = %SubtitleLabel
@onready var summary_label: Label = %SummaryLabel
@onready var priority_label: Label = %PriorityLabel
@onready var memory_label: Label = %MemoryLabel
@onready var hook_label: Label = %ChapterHookLabel
@onready var cast_label: Label = %CastLabel
@onready var chapter_title_label: Label = %ChapterTitleLabel
@onready var chapter_theme_label: Label = %ChapterThemeLabel
@onready var detail_panel: PanelContainer = %DetailPanel
@onready var toggle_detail_button: Button = %ToggleDetailButton
@onready var replay_button: Button = %ReplayButton
@onready var return_title_button: Button = %ReturnTitleButton

var _review_data: Dictionary = {}


func _ready() -> void:
	SceneRouter.register_current_scene(scene_file_path)
	GameState.set_player_control(false)
	_review_data = _load_review_data()
	_apply_review_text()
	_mark_prologue_completed()
	toggle_detail_button.pressed.connect(_on_toggle_detail_pressed)
	replay_button.pressed.connect(_on_replay_pressed)
	return_title_button.pressed.connect(_on_return_title_pressed)
	return_title_button.grab_focus()
	await AudioDirector.play_music("music.name_and_registry", 0.0)
	await get_tree().process_frame
	SaveManager.save_game("prologue_completed")


func _load_review_data() -> Dictionary:
	if not FileAccess.file_exists(REVIEW_PATH):
		push_error("P5 review JSON not found: " + REVIEW_PATH)
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(REVIEW_PATH))
	if not parsed is Dictionary:
		push_error("P5 review JSON is invalid: " + REVIEW_PATH)
		return {}
	return parsed


func _apply_review_text() -> void:
	var first_priority := str(GameState.get_state_value("prologue.first_priority", "unknown"))
	var priority_review: Dictionary = _review_data.get("priority_review", {})
	var priority_data: Dictionary = priority_review.get(
		first_priority,
		priority_review.get("unknown", {})
	)
	var summary_lines: Array = _review_data.get("summary_lines", [])
	var cast_lines: Array = _review_data.get("cast", [])
	var buttons: Dictionary = _review_data.get("buttons", {})

	title_label.text = str(_review_data.get("title", "序章"))
	subtitle_label.text = str(_review_data.get("subtitle", ""))
	summary_label.text = "\n".join(summary_lines)
	priority_label.text = "本次第一选择：%s" % str(priority_data.get("label", "尚未锁定"))
	memory_label.text = str(priority_data.get("memory", ""))
	hook_label.text = str(priority_data.get("chapter_hook", ""))
	cast_label.text = "\n".join(cast_lines)
	chapter_title_label.text = str(_review_data.get("chapter_title", "第一章"))
	chapter_theme_label.text = str(_review_data.get("chapter_theme", ""))
	toggle_detail_button.text = str(buttons.get("toggle_detail", "查看/收起本次回顾"))
	replay_button.text = str(buttons.get("replay", "重玩序章"))
	return_title_button.text = str(buttons.get("return_title", "回到标题"))


func _mark_prologue_completed() -> void:
	GameState.set_state_value("prologue.completed", true)
	GameState.set_state_value("prologue.chapter_title_reached", true)
	GameState.record_event(
		"prologue_completed",
		{
			"first_priority": GameState.get_state_value("prologue.first_priority", ""),
			"scene": scene_file_path,
		}
	)


func _on_toggle_detail_pressed() -> void:
	detail_panel.visible = not detail_panel.visible


func _on_replay_pressed() -> void:
	GameState.reset_state()
	SaveManager.delete_save()
	SceneRouter.go_to_scene(_resolve_start_scene())


func _on_return_title_pressed() -> void:
	SceneRouter.go_to_scene(TITLE_SCENE)


func _resolve_start_scene() -> String:
	if not FileAccess.file_exists(ASSET_MANIFEST_PATH):
		return "res://scenes/prologue/SC01_Home_Morning.tscn"
	var manifest: Variant = JSON.parse_string(FileAccess.get_file_as_string(ASSET_MANIFEST_PATH))
	if not manifest is Dictionary:
		return "res://scenes/prologue/SC01_Home_Morning.tscn"
	var runtime_assets: Variant = manifest.get("runtime_assets", {})
	if runtime_assets is Dictionary:
		var path := str(runtime_assets.get("scene.sc01_home_morning", ""))
		if ResourceLoader.exists(path):
			return path
	return "res://scenes/prologue/SC01_Home_Morning.tscn"
