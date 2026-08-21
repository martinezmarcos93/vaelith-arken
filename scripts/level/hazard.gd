extends Hitbox
class_name Hazard

## Peligro ambiental estatico (Fase 4.3, Tramo C de docs/layout_level1.md).
## Hitbox normal se activa/desactiva por el estado de combate de quien la
## dispara (jugador/enemigo); un hazard no tiene "duenio" que la controle,
## asi que se reactiva sola en un ciclo para que _hit_targets no bloquee
## para siempre un segundo golpe si el jugador vuelve a tocarla despues de
## sus i-frames.

@export var reactivate_interval: float = 0.5

func _ready() -> void:
	super._ready()
	activate()
	var timer := Timer.new()
	timer.wait_time = reactivate_interval
	timer.autostart = true
	timer.timeout.connect(_on_reactivate_timeout)
	add_child(timer)


func _on_reactivate_timeout() -> void:
	deactivate()
	activate()
