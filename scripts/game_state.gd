extends Node

## Autoload: progreso minimo de la demo. Sin guardado entre sesiones --
## GDD.md excluye explicitamente sistema de guardado del alcance de esta
## demo (un solo checkpoint por nivel alcanza).

signal memory_collected(total: int)

var memories_collected: int = 0


func collect_memory() -> void:
	memories_collected += 1
	memory_collected.emit(memories_collected)
