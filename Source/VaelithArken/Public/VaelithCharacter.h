// Vaelith en primera persona: espada, escudo, daga, Imponer las Manos. Diseño: docs/sistemas.md
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "FichaComponent.h"
#include "VaelithNucleo.h"
#include "VaelithCharacter.generated.h"

class UCameraComponent;
class UStaticMeshComponent;
class UPointLightComponent;
class AInteractuable;
class ANoMuerto;

UENUM()
enum class EAccionArma : uint8
{
	Ninguna, Tajo, TajoPotente, GolpeEscudo, Embestida, Manos, Cargando
};

UCLASS()
class VAELITHARKEN_API AVaelithCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	AVaelithCharacter();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) UCameraComponent* Camara;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) UFichaComponent* Ficha;
	UPROPERTY(VisibleAnywhere) USceneComponent* PivoteDerecho;
	UPROPERTY(VisibleAnywhere) USceneComponent* PivoteIzquierdo;
	UPROPERTY(VisibleAnywhere) UStaticMeshComponent* Espada;
	UPROPERTY(VisibleAnywhere) UStaticMeshComponent* Daga;
	UPROPERTY(VisibleAnywhere) UStaticMeshComponent* Escudo;
	/** Luz tenue sin sombras: la visión en penumbra de su sangre élfica. */
	UPROPERTY(VisibleAnywhere) UPointLightComponent* Penumbra;

	// ---- Estado de juego ----
	UPROPERTY(BlueprintReadOnly) bool bTieneArmas = true;
	UPROPERTY(BlueprintReadOnly) bool bTieneDaga = true;
	UPROPERTY(BlueprintReadOnly) bool bUsandoDaga = false;
	UPROPERTY(BlueprintReadOnly) TArray<EDote> Dotes;
	/** Bloquea el control (cinemáticas, menús). */
	UPROPERTY(BlueprintReadOnly) bool bControlBloqueado = false;
	UPROPERTY(BlueprintReadOnly) FString TextoInteraccion;

	UFUNCTION(BlueprintPure) bool TieneDote(EDote D) const { return Dotes.Contains(D); }
	void AplicarDotes();

	/** Golpe de un enemigo. Devuelve true si fue un bloqueo perfecto. */
	bool RecibirGolpe(int32 Danio, ETipoDanio Tipo, AActor* Atacante);

	// ---- Cinemática del despertar ----
	void IniciarDespertar();
	bool EnDespertar() const { return TiempoDespertar >= 0.f; }
	/** Prueba: corta la cinemática del despertar. */
	/** Yaw del cuerpo sobre la losa al empezar el despertar. */
	float YawDespertar = 0.f;
	void TiempoDespertarCancelar() { if (TiempoDespertar >= 0.f) TiempoDespertar = 16.99f; }

	/** Efectos de pantalla que pide el director (0..1). */
	float Desaturacion = 0.f;
	float Desenfoque = 0.f;
	float TemblorPantalla = 0.f;
	/** 0 = normal; > 0 = catacumbas (visión en penumbra). Lo setea el GameMode por zona. */
	float NivelPenumbra = 1.f;
	float PenumbraObjetivo = 1.f;
	/** Corrupción del tramo (0..3): oscurece y enfría. */
	int32 Penitencia = 0;  // muertes en el tramo (0..3): niebla y un no-muerto extra

	/** Para el HUD. */
	float UltimoDanioRecibido = -100.f;
	float UltimoBloqueoPerfecto = -100.f;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	// Acción en curso
	EAccionArma Accion = EAccionArma::Ninguna;
	float TiempoAccion = 0.f;
	float DuracionAccion = 0.f;
	bool bGolpeAplicado = false;
	float TiempoCarga = 0.f;
	TSet<TWeakObjectPtr<AActor>> GolpeadosEnAccion;

	// Bloqueo
	bool bBloqueoPedido = false;
	float InicioBloqueo = -100.f;
	float AlturaEscudo = 0.f;  // 0 = bajo, 1 = arriba

	// Movimiento y "peso"
	float FaseCabeceo = 0.f;
	float Retroceso = 0.f;
	FVector2D Balanceo = FVector2D::ZeroVector;
	float TiempoDespertar = -1.f;
	float CadenciaAura = 0.f;
	float Hitstop = 0.f;
	float DistanciaPaso = 0.f;

	void LeerControles(float Dt);
	void EmpezarAccion(EAccionArma Nueva);
	void ActualizarAccion(float Dt);
	void AplicarGolpe();
	void AnimarArmas(float Dt);
	void ActualizarPostProceso(float Dt);
	void ActualizarDespertar(float Dt);
	void BuscarInteractuable();
	void UsarManos();
	void Sacudir(float Fuerza);
	void Reproducir(const TCHAR* Ruta, float Volumen = 1.f, float Tono = 1.f);

	UPROPERTY() AInteractuable* InteractuableEnMira = nullptr;
	UPROPERTY() TMap<FString, USoundBase*> CacheSonidos;
};
