extends SceneTree

const SCENES := [
	"res://scenes/ui/TitleScreen.tscn",
	"res://scenes/ui/DialogueLayer.tscn",
	"res://scenes/ui/TransitionLayer.tscn",
	"res://scenes/ui/InteractionPrompt.tscn",
	"res://scenes/ui/NameInputLayer.tscn",
	"res://scenes/core/InteractableArea2D.tscn",
	"res://scenes/characters/Player.tscn",
	"res://scenes/characters/P1TestActor.tscn",
	"res://scenes/characters/Mother.tscn",
	"res://scenes/characters/Xinheng.tscn",
	"res://scenes/characters/Hean.tscn",
	"res://scenes/characters/BoatOwner.tscn",
	"res://scenes/characters/FerryWorker.tscn",
	"res://scenes/characters/FerryWoman.tscn",
	"res://scenes/characters/Hanning.tscn",
	"res://scenes/characters/HanningMother.tscn",
	"res://scenes/characters/Liuniang.tscn",
	"res://scenes/characters/RefugeeOld.tscn",
	"res://scenes/characters/RefugeeMother.tscn",
	"res://scenes/characters/RefugeeMan.tscn",
	"res://scenes/prologue/SC01_OldFerry_Test.tscn",
	"res://scenes/prologue/SC01_Home_Morning.tscn",
	"res://scenes/prologue/SC02_Xinheng_Desk.tscn",
	"res://scenes/prologue/SC03_Ferry_Day.tscn",
	"res://scenes/prologue/SC04_Refugee_Shelter.tscn",
	"res://scenes/prologue/SC05_Ritual_Storehouse.tscn",
	"res://scenes/prologue/SC06_Cart_Crash_Rain.tscn",
	"res://scenes/prologue/SC07_Prologue_End.tscn",
	"res://tests/scenes/P1NarrativeInfrastructureTest.tscn",
	"res://tests/scenes/P1Destination.tscn",
	"res://tests/scenes/SaveManagerTest.tscn",
]

const JSON_FILES := [
	"res://content/prologue/timeline.json",
	"res://content/prologue/dialogue.zh-CN.json",
	"res://content/prologue/interactables.json",
	"res://content/prologue/prologue_review.zh-CN.json",
	"res://content/prologue/asset_manifest.json",
	"res://assets/generated_asset_manifest.json",
	"res://tests/fixtures/p1_timeline.json",
	"res://tests/fixtures/p1_dialogue.zh-CN.json",
	"res://tests/fixtures/p1_asset_manifest.json",
]

const REQUIRED_BUSES := [&"Master", &"Music", &"Ambience", &"SFX", &"Voice", &"UI"]

var _failures: Array[String] = []


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	_check_project_settings()
	_check_json_files()
	_check_content_links()
	await _check_scenes()
	_check_audio_buses()

	if _failures.is_empty():
		print("[P0 SMOKE] PASS: scenes, JSON, references and audio buses loaded.")
		quit(0)
		return

	for failure in _failures:
		push_error("[P0 SMOKE] " + failure)
	quit(1)


func _check_project_settings() -> void:
	if ProjectSettings.get_setting("display/window/size/viewport_width") != 1280:
		_failures.append("Viewport width is not 1280.")
	if ProjectSettings.get_setting("display/window/size/viewport_height") != 720:
		_failures.append("Viewport height is not 720.")
	if ProjectSettings.get_setting("rendering/renderer/rendering_method") != "gl_compatibility":
		_failures.append("Renderer is not gl_compatibility.")


func _check_json_files() -> void:
	for path in JSON_FILES:
		if not FileAccess.file_exists(path):
			_failures.append("Missing JSON: " + path)
			continue
		var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
		if parsed == null:
			_failures.append("Invalid JSON: " + path)


func _check_content_links() -> void:
	var dialogue: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://content/prologue/dialogue.zh-CN.json")
	)
	var timeline: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://content/prologue/timeline.json")
	)
	var interactables: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://content/prologue/interactables.json")
	)
	var manifest: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://content/prologue/asset_manifest.json")
	)
	var lines: Dictionary = dialogue.get("lines", {})
	var asset_paths: Dictionary = {}
	for group_name in ["runtime_assets", "p0_assets"]:
		var group: Variant = manifest.get(group_name, {})
		if group is Dictionary:
			for asset_id in group:
				if group[asset_id] is String:
					asset_paths[asset_id] = group[asset_id]
	for asset_id in asset_paths:
		var path := str(asset_paths[asset_id])
		if not ResourceLoader.exists(path):
			_failures.append("Manifest asset cannot be loaded: %s -> %s" % [asset_id, path])
	for stage_value in timeline.get("stages", {}).values():
		if not stage_value is Dictionary:
			continue
		for event_key in stage_value:
			if not stage_value[event_key] is Array:
				continue
			for event_value in stage_value.get(event_key, []):
				if not event_value is Dictionary:
					continue
				var event: Dictionary = event_value
				if event.get("type", "") == "dialogue":
					var line_id := str(event.get("line_id", ""))
					if not lines.has(line_id):
						_failures.append("Timeline dialogue ID is missing: " + line_id)
				var asset_id := str(event.get("asset_id", ""))
				if not asset_id.is_empty() and not asset_paths.has(asset_id):
					_failures.append("Timeline asset ID is missing: " + asset_id)
	for scene_value in interactables.get("scenes", {}).values():
		if not scene_value is Array:
			continue
		for item_value in scene_value:
			if not item_value is Dictionary:
				continue
			var payload: Dictionary = item_value.get("payload", {})
			var line_id := str(payload.get("line_id", ""))
			if not line_id.is_empty() and not lines.has(line_id):
				_failures.append("Interactable dialogue ID is missing: " + line_id)
			var target_id := str(payload.get("target_asset_id", ""))
			if not target_id.is_empty() and not asset_paths.has(target_id):
				_failures.append("Interactable target asset ID is missing: " + target_id)
			var event_key := str(payload.get("event_key", ""))
			if not event_key.is_empty():
				var found_event_key := false
				for stage_value in timeline.get("stages", {}).values():
					if stage_value is Dictionary and stage_value.has(event_key):
						found_event_key = true
						break
				if not found_event_key:
					_failures.append("Interactable event block is missing: " + event_key)


func _check_scenes() -> void:
	for path in SCENES:
		var packed := load(path) as PackedScene
		if packed == null:
			_failures.append("Unable to load scene: " + path)
			continue
		var instance := packed.instantiate()
		if instance == null:
			_failures.append("Unable to instantiate scene: " + path)
			continue
		if path.ends_with("TitleScreen.tscn"):
			for button_name in [
				"NewGameButton",
				"ContinueButton",
				"SettingsButton",
				"ExitButton",
			]:
				if instance.find_child(button_name, true, false) == null:
					_failures.append("Title menu is missing: " + button_name)
		if path.contains("/prologue/SC0") and not path.ends_with("SC01_OldFerry_Test.tscn"):
			instance.free()
			continue
		root.add_child(instance)
		await process_frame
		instance.free()
		await process_frame


func _check_audio_buses() -> void:
	for bus_name in REQUIRED_BUSES:
		if AudioServer.get_bus_index(bus_name) < 0:
			_failures.append("Missing audio bus: " + String(bus_name))
