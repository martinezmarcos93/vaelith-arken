extends CharacterBody2D

## Muñeco de entrenamiento del sandbox de pruebas (Etapa 1.5). Recibe golpes
## del jugador y ataca periodicamente para poder validar tambien el bloqueo
## y la ruptura de postura. No es contenido final del juego.

@export var max_health: int = 10
@export var gravity: float = 1400.0
@export var attack_interval: float = 2.0
@export var attack_damage: int = 1
@export var attack_windup: float = 0.3

@onready var hurtbox: Hurtbox = $Hurtbox
@onready var attack_hitbox: Hitbox = $AttackHitbox

var health: int
var _attack_timer: float = 0.0


func _ready() -> void:
	health = max_health
	hurtbox.hurt.connect(_on_hurt)
	attack_hitbox.source = self
	attack_hitbox.damage = attack_damage
	attack_hitbox.knockback = 60.0


func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y += gravity * delta
	velocity.x = move_toward(velocity.x, 0.0, 600.0 * delta)
	move_and_slide()

	if health <= 0:
		return
	_attack_timer += delta
	if _attack_timer >= attack_interval:
		_attack_timer = 0.0
		_perform_attack()


func _perform_attack() -> void:
	attack_hitbox.activate()
	await get_tree().create_timer(attack_windup).timeout
	attack_hitbox.deactivate()


func _on_hurt(damage: int, direction: Vector2, knockback: float, stagger_time: float) -> void:
	health = max(health - damage, 0)
	velocity = direction * knockback
	print("Dummy: recibe %d de daño (vida=%d/%d)" % [damage, health, max_health])
	if health <= 0:
		print("Dummy: destruido")
