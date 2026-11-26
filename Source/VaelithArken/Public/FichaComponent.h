// Ficha de Pathfinder 2e llevada a tiempo real. Diseño: docs/sistemas.md
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "FichaComponent.generated.h"

UENUM(BlueprintType)
enum class ETipoDanio : uint8
{
	Cortante,
	Perforante,
	Contundente,
	Vital,     // energía de Pharasma: hiere a los no-muertos
	Vacio      // energía de no-muerte: hiere a los vivos
};

USTRUCT(BlueprintType)
struct FAtributosPF2e
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Fuerza = 4;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Destreza = 1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Constitucion = 2;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Inteligencia = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Sabiduria = 2;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Carisma = 2;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAlCambiarValor, int32, Actual, int32, Maximo);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAlEvento);

UCLASS(ClassGroup=(Vaelith), meta=(BlueprintSpawnableComponent))
class VAELITHARKEN_API UFichaComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UFichaComponent();

	// ---- Ficha ----
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") FAtributosPF2e Atributos;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha", meta=(ClampMin=1, ClampMax=20)) int32 Nivel = 1;
	/** PG de ascendencia (humano 8) y por nivel de clase (campeón 10). Enemigos: PG fijos en PGBaseFijos. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") int32 PGAscendencia = 8;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") int32 PGClasePorNivel = 10;
	/** Si es > 0, ignora la fórmula de PF2e (útil para enemigos). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") int32 PGBaseFijos = 0;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Defensa") TMap<ETipoDanio, int32> Debilidades;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Defensa") TMap<ETipoDanio, int32> Resistencias;
	/** Inmaterial (fantasmas): mitad del daño físico salvo que el golpe sea "toque fantasmal". */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Defensa") bool bInmaterial = false;

	// ---- Escudo (Bloqueo con escudo de PF2e) ----
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Escudo") bool bTieneEscudo = true;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Escudo") int32 DurezaEscudo = 5;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Escudo") int32 PGEscudoMax = 20;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Escudo") int32 UmbralRoturaEscudo = 10;

	// ---- Tres acciones ----
	/** Foco extra por dotes. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") int32 FocoAdicional = 0;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Acciones") int32 AccionesMax = 3;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Acciones") float SegundosPorAccion = 0.9f;
	/** Ventana en la que cuenta la penalización por ataque múltiple. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Acciones") float VentanaAtaqueMultiple = 1.5f;

	// ---- Estado (solo lectura) ----
	UPROPERTY(BlueprintReadOnly, Category="Estado") int32 PG = 0;
	UPROPERTY(BlueprintReadOnly, Category="Estado") int32 PGEscudo = 0;
	UPROPERTY(BlueprintReadOnly, Category="Estado") int32 Acciones = 3;
	UPROPERTY(BlueprintReadOnly, Category="Estado") int32 Foco = 1;
	UPROPERTY(BlueprintReadOnly, Category="Estado") bool bBloqueando = false;
	UPROPERTY(BlueprintReadOnly, Category="Estado") bool bMoribundo = false;
	UPROPERTY(BlueprintReadOnly, Category="Estado") bool bMuerto = false;

	UPROPERTY(BlueprintAssignable) FAlCambiarValor AlCambiarPG;
	UPROPERTY(BlueprintAssignable) FAlCambiarValor AlCambiarEscudo;
	UPROPERTY(BlueprintAssignable) FAlCambiarValor AlCambiarAcciones;
	UPROPERTY(BlueprintAssignable) FAlCambiarValor AlCambiarFoco;
	UPROPERTY(BlueprintAssignable) FAlEvento AlQuedarMoribundo;
	UPROPERTY(BlueprintAssignable) FAlEvento AlMorir;
	UPROPERTY(BlueprintAssignable) FAlEvento AlRomperseEscudo;

	// ---- Consultas ----
	UFUNCTION(BlueprintPure, Category="Ficha") int32 PGMax() const;
	UFUNCTION(BlueprintPure, Category="Ficha") int32 FocoMax() const;
	UFUNCTION(BlueprintPure, Category="Escudo") bool EscudoRoto() const { return bTieneEscudo && PGEscudo <= UmbralRoturaEscudo; }
	UFUNCTION(BlueprintPure, Category="Escudo") bool EscudoDestruido() const { return !bTieneEscudo || PGEscudo <= 0; }
	/** 1.0 / 0.8 / 0.6 según cuántos ataques se hicieron dentro de la ventana. */
	UFUNCTION(BlueprintPure, Category="Acciones") float FactorAtaqueMultiple() const;

	// ---- Acciones ----
	/** Intenta gastar acciones; false si no alcanzan. */
	UFUNCTION(BlueprintCallable, Category="Acciones") bool GastarAcciones(int32 Cantidad);
	/** Registra un ataque (para la penalización por ataque múltiple) y devuelve el daño ya multiplicado. */
	UFUNCTION(BlueprintCallable, Category="Acciones") int32 RegistrarAtaque(int32 DanioBase);
	UFUNCTION(BlueprintCallable, Category="Escudo") void SetBloqueando(bool bNuevo);

	/**
	 * Aplica daño con debilidades, resistencias, inmaterialidad y escudo.
	 * Devuelve los PG que efectivamente perdió el portador.
	 */
	UFUNCTION(BlueprintCallable, Category="Ficha") int32 RecibirDanio(int32 Cantidad, ETipoDanio Tipo, bool bToqueFantasmal = false);
	UFUNCTION(BlueprintCallable, Category="Ficha") void Curar(int32 Cantidad);
	/** Imponer las Manos: cura 6 o, si se usa sobre un no-muerto, devuelve true y el llamador aplica 2d6 vital. */
	UFUNCTION(BlueprintCallable, Category="Foco") bool GastarFoco();
	/** Diehard: levantarse del estado Moribundo con 1 PG (una vez por altar). */
	UFUNCTION(BlueprintCallable, Category="Ficha") bool Levantarse();
	/** Altar de Pharasma: restaura todo. */
	UFUNCTION(BlueprintCallable, Category="Ficha") void DescansarEnAltar();

	/** Segundos que dura el estado Moribundo antes de morir (Diehard: margen extra). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") float SegundosMoribundo = 3.0f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") bool bTieneDiehard = true;

protected:
	virtual void BeginPlay() override;
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
	float AcumuladoAcciones = 0.f;
	float TiempoMoribundo = 0.f;
	bool bDiehardDisponible = true;
	TArray<float> MarcasAtaque;

	void Morir();
	void AvisarTodo();
};
