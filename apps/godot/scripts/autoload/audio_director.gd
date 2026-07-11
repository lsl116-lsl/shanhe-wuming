extends Node

signal asset_manifest_loaded(path: String)
signal audio_started(channel: String, asset_id: String)
signal audio_stopped(channel: String)

const DEFAULT_ASSET_MANIFEST := "res://content/prologue/asset_manifest.json"

var _asset_paths: Dictionary = {}
var _music_player: AudioStreamPlayer
var _ambience_player: AudioStreamPlayer
var _sfx_player: AudioStreamPlayer
var _voice_player: AudioStreamPlayer
var _ui_player: AudioStreamPlayer
var _sfx_one_shots: Array[AudioStreamPlayer] = []


func _ready() -> void:
	_music_player = _create_player("MusicPlayer", &"Music")
	_ambience_player = _create_player("AmbiencePlayer", &"Ambience")
	_sfx_player = _create_player("SFXPlayer", &"SFX")
	_voice_player = _create_player("VoicePlayer", &"Voice")
	_ui_player = _create_player("UIPlayer", &"UI")
	if FileAccess.file_exists(DEFAULT_ASSET_MANIFEST):
		load_asset_manifest(DEFAULT_ASSET_MANIFEST)


func _create_player(node_name: String, bus_name: StringName) -> AudioStreamPlayer:
	var player := AudioStreamPlayer.new()
	player.name = node_name
	player.bus = bus_name
	add_child(player)
	return player


func load_asset_manifest(path: String) -> Error:
	if not FileAccess.file_exists(path):
		push_error("AudioDirector asset manifest not found: " + path)
		return ERR_FILE_NOT_FOUND
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary:
		push_error("AudioDirector asset manifest is invalid JSON: " + path)
		return ERR_PARSE_ERROR

	_asset_paths.clear()
	for group_name in ["runtime_assets", "test_assets"]:
		var group: Variant = parsed.get(group_name, {})
		if group is Dictionary:
			for asset_id in group:
				if group[asset_id] is String:
					_asset_paths[asset_id] = group[asset_id]
	var p0_assets: Variant = parsed.get("p0_assets", {})
	if p0_assets is Dictionary:
		for asset_id in p0_assets:
			if p0_assets[asset_id] is String:
				_asset_paths[asset_id] = p0_assets[asset_id]
	asset_manifest_loaded.emit(path)
	return OK


func resolve_asset(asset_id: String) -> String:
	return str(_asset_paths.get(asset_id, ""))


func play_music(asset_id: String, fade_seconds := 0.0) -> Error:
	return await _play_channel(_music_player, "music", asset_id, fade_seconds, true)


func play_ambience(asset_id: String, fade_seconds := 0.0) -> Error:
	return await _play_channel(_ambience_player, "ambience", asset_id, fade_seconds, true)


func play_sfx(asset_id: String) -> Error:
	return await _play_one_shot_sfx(asset_id)


func play_voice(asset_id: String) -> Error:
	return await _play_channel(_voice_player, "voice", asset_id, 0.0, false)


func play_ui(asset_id: String) -> Error:
	return await _play_channel(_ui_player, "ui", asset_id, 0.0, false)


func _play_channel(
	player: AudioStreamPlayer,
	channel: String,
	asset_id: String,
	fade_seconds: float,
	loop_playback: bool
) -> Error:
	var path := resolve_asset(asset_id)
	if path.is_empty() or not ResourceLoader.exists(path):
		push_error("Audio asset cannot be resolved: " + asset_id)
		return ERR_FILE_NOT_FOUND
	var stream := load(path) as AudioStream
	if stream == null:
		return ERR_CANT_OPEN

	if fade_seconds > 0.0 and player.playing:
		var fade_out := create_tween()
		fade_out.tween_property(player, "volume_db", -50.0, fade_seconds * 0.5)
		await fade_out.finished
	player.stop()
	player.stream = stream
	player.volume_db = -50.0 if fade_seconds > 0.0 else 0.0
	if loop_playback and not player.finished.is_connected(player.play):
		player.finished.connect(player.play)
	player.play()
	if fade_seconds > 0.0:
		var fade_in := create_tween()
		fade_in.tween_property(player, "volume_db", 0.0, fade_seconds * 0.5)
		await fade_in.finished
	audio_started.emit(channel, asset_id)
	return OK


func stop_channel(channel: String, fade_seconds := 0.0) -> void:
	var player := _player_for_channel(channel)
	if channel == "sfx":
		for one_shot in _sfx_one_shots.duplicate():
			if is_instance_valid(one_shot):
				one_shot.stop()
				one_shot.queue_free()
		_sfx_one_shots.clear()
	if player == null:
		return
	if fade_seconds > 0.0 and player.playing:
		var tween := create_tween()
		tween.tween_property(player, "volume_db", -50.0, fade_seconds)
		await tween.finished
	player.stop()
	player.stream = null
	audio_stopped.emit(channel)


func _player_for_channel(channel: String) -> AudioStreamPlayer:
	match channel:
		"music":
			return _music_player
		"ambience":
			return _ambience_player
		"sfx":
			return _sfx_player
		"voice":
			return _voice_player
		"ui":
			return _ui_player
	return null


func _play_one_shot_sfx(asset_id: String) -> Error:
	var path := resolve_asset(asset_id)
	if path.is_empty() or not ResourceLoader.exists(path):
		push_error("Audio asset cannot be resolved: " + asset_id)
		return ERR_FILE_NOT_FOUND
	var stream := load(path) as AudioStream
	if stream == null:
		return ERR_CANT_OPEN
	var player := AudioStreamPlayer.new()
	player.name = "SFXOneShot"
	player.bus = &"SFX"
	player.stream = stream
	add_child(player)
	_sfx_one_shots.append(player)
	player.finished.connect(_on_sfx_one_shot_finished.bind(player))
	player.play()
	audio_started.emit("sfx", asset_id)
	return OK


func _on_sfx_one_shot_finished(player: AudioStreamPlayer) -> void:
	_sfx_one_shots.erase(player)
	if is_instance_valid(player):
		player.queue_free()
