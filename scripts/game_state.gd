extends Node

## Autoload: progreso minimo de la demo. Sin guardado entre sesiones --
## GDD.md excluye explicitamente sistema de guardado del alcance de esta
## demo (un solo checkpoint por nivel alcanza).

signal memory_collected(total: int)
signal skull_collected(total: int)
signal corruption_changed(level: int)

const MAX_CORRUPTION := 3

var memories_collected: int = 0
var skulls_collected: int = 0

## Nivel de corrupcion (0-3, roadmap_level1_largo.md Fase 4): sube 1 por
## muerte, baja 1 por calavera recolectada, resetea al completar el nivel.
## El efecto ambiental por tramo (+1 enemigo, -luz) lo lee cada
## CorruptionController de tramo -- este autoload solo lleva el numero.
var corruption: int = 0


func collect_memory() -> void:
	memories_collected += 1
	memory_collected.emit(memories_collected)


func collect_skull() -> void:
	skulls_collected += 1
	skull_collected.emit(skulls_collected)
	_set_corruption(corruption - 1)


func register_death() -> void:
	_set_corruption(corruption + 1)


func reset_corruption() -> void:
	_set_corruption(0)


func _set_corruption(value: int) -> void:
	value = clampi(value, 0, MAX_CORRUPTION)
	if value == corruption:
		return
	corruption = value
	corruption_changed.emit(corruption)
