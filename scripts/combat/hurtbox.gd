extends Area2D
class_name Hurtbox

## Representa la parte "vulnerable" de un personaje. No decide reglas de
## juego (bloqueo, i-frames, vida): eso lo resuelve quien escucha la señal.

signal hurt(damage: int, direction: Vector2, knockback: float, stagger_time: float)

func _ready() -> void:
	add_to_group("hurtbox")

## Llamado por un Hitbox cuando conecta un golpe.
func receive_hit(damage: int, direction: Vector2, knockback: float, stagger_time: float) -> void:
	hurt.emit(damage, direction, knockback, stagger_time)
