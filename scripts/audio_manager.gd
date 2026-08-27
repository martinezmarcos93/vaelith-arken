extends Node

## Autoload. Punto único para música y SFX (Etapa 8).
##
## Buses (default_bus_layout.tres): Master / Music / SFX / Ambient / UI.
##
## Música: dos AudioStreamPlayer en el bus Music que se alternan para poder
## hacer crossfade entre temas (exploración → boss, o a silencio en el
## epílogo). `play_music(path)` carga y loopea; `stop_music()` fundea a nada.
##
## SFX: pool chico de AudioStreamPlayer en el bus SFX/UI, fire-and-forget.
## `play_sfx(path)` o `play_sfx_random([...])` con leve variación de pitch
## para que golpes/pasos repetidos no suenen idénticos.
##
## process_mode ALWAYS: la música/UI tienen que seguir sonando con el árbol
## pausado (DialogueBox, PauseMenu).

const MUSIC_FADE := 1.5
const SFX_POOL := 12

var _music: Array[AudioStreamPlayer] = []
var _music_tweens: Array[Tween] = [null, null]
var _music_active: int = 0
var _music_path: String = ""
var _sfx: Array[AudioStreamPlayer] = []
var _sfx_next: int = 0
var _ambient: AudioStreamPlayer
var _ambient_tween: Tween = null
var _ambient_path: String = ""
var _rng := RandomNumberGenerator.new()


## Arranca un fade de `volume_db` en `player`, matando cualquier fade previo
## sobre el mismo player (llamadas rápidas a play_music no deben apilar tweens).
func _fade(player: AudioStreamPlayer, slot: int, target_db: float, dur: float, stop_at_end: bool) -> void:
	var prev: Tween = _ambient_tween if slot < 0 else _music_tweens[slot]
	if prev != null and prev.is_valid():
		prev.kill()
	var tw := create_tween()
	tw.tween_property(player, "volume_db", target_db, dur)
	if stop_at_end:
		tw.tween_callback(player.stop)
	if slot < 0:
		_ambient_tween = tw
	else:
		_music_tweens[slot] = tw


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	for i in 2:
		var p := AudioStreamPlayer.new()
		p.bus = "Music"
		p.volume_db = -80.0
		add_child(p)
		_music.append(p)
	for i in SFX_POOL:
		var p := AudioStreamPlayer.new()
		p.bus = "SFX"
		add_child(p)
		_sfx.append(p)
	_ambient = AudioStreamPlayer.new()
	_ambient.bus = "Ambient"
	_ambient.volume_db = -80.0
	add_child(_ambient)


## Cambia el tema con crossfade. `path` puede ser "" para cortar la música.
func play_music(path: String, fade: float = MUSIC_FADE, volume_db: float = -6.0) -> void:
	if path == _music_path:
		return
	_music_path = path
	var from_slot := _music_active
	var from := _music[from_slot]
	_music_active = 1 - _music_active
	var to := _music[_music_active]

	if from.playing:
		_fade(from, from_slot, -80.0, fade, true)

	if path == "":
		return
	var stream: AudioStream = load(path)
	if stream == null:
		push_warning("AudioManager: no se pudo cargar la música '%s'" % path)
		return
	_set_stream_loop(stream, true)
	to.stream = stream
	to.volume_db = -80.0
	to.play()
	_fade(to, _music_active, volume_db, fade, false)


func stop_music(fade: float = MUSIC_FADE) -> void:
	play_music("", fade)


## Cama de ambiente (loop) en el bus Ambient. "" para cortarla.
func play_ambient(path: String, fade: float = 2.0, volume_db: float = -14.0) -> void:
	if path == _ambient_path:
		return
	_ambient_path = path
	if path == "":
		_fade(_ambient, -1, -80.0, fade, true)
		return
	var stream: AudioStream = load(path)
	if stream == null:
		push_warning("AudioManager: no se pudo cargar el ambiente '%s'" % path)
		return
	_set_stream_loop(stream, true)
	_ambient.stream = stream
	_ambient.volume_db = -80.0
	_ambient.play()
	_fade(_ambient, -1, volume_db, fade, false)


func stop_ambient(fade: float = 2.0) -> void:
	play_ambient("", fade)


## SFX one-shot. `bus` normalmente "SFX" o "UI". `pitch_var` = ± semitonos
## aleatorios (en factor de pitch_scale) para variar repeticiones.
func play_sfx(path: String, bus: String = "SFX", volume_db: float = 0.0, pitch_var: float = 0.06) -> void:
	if path == "":
		return
	var stream: AudioStream = load(path)
	if stream == null:
		push_warning("AudioManager: no se pudo cargar el SFX '%s'" % path)
		return
	var p := _sfx[_sfx_next]
	_sfx_next = (_sfx_next + 1) % _sfx.size()
	p.stream = stream
	p.bus = bus
	p.volume_db = volume_db
	p.pitch_scale = 1.0 + _rng.randf_range(-pitch_var, pitch_var)
	p.play()


func play_sfx_random(paths: Array, bus: String = "SFX", volume_db: float = 0.0, pitch_var: float = 0.08) -> void:
	if paths.is_empty():
		return
	play_sfx(paths[_rng.randi() % paths.size()], bus, volume_db, pitch_var)


## Los .ogg/.mp3 de música se importan sin loop por defecto; forzarlo acá
## evita depender de tocar cada .import a mano.
func _set_stream_loop(stream: AudioStream, value: bool) -> void:
	if stream is AudioStreamOggVorbis or stream is AudioStreamMP3:
		stream.loop = value
	elif stream is AudioStreamWAV:
		stream.loop_mode = AudioStreamWAV.LOOP_FORWARD if value else AudioStreamWAV.LOOP_DISABLED
