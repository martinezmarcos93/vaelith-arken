// No-muertos: zombi, esqueleto, fantasma (atado o libre), guardián pacífico y la Sombra.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "FichaComponent.h"
#include "NoMuerto.generated.h"

class UPointLightComponent;
class AInteractuable;

UENUM(BlueprintType)
enum class ETipoNoMuerto : uint8
{
	Zombi, Esqueleto, Fantasma, Guardian, Sombra
};

UENUM()
enum class EEstadoNoMuerto : uint8
{
	Dormido, Acecho, Persecucion, Amago, Golpe, Recuperacion, Aturdido, Rodeo, Muerto, Liberado
};

UCLASS()
class VAELITHARKEN_API ANoMuerto : public ACharacter
{
	GENERATED_BODY()

public:
	ANoMuerto();

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Vaelith") ETipoNoMuerto Tipo = ETipoNoMuerto::Zombi;
	/** Si está asignada, destruir esa ancla libera al fantasma en vez de matarlo. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Vaelith") AInteractuable* Ancla = nullptr;
	/** Se despierta solo al ver al jugador a esta distancia (cm). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Vaelith") float DistanciaVision = 1400.f;
	/** Nombre del hecho que se registra al morir (para no reaparecer al cargar). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Vaelith") FName Hecho;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) UFichaComponent* Ficha;
	UPROPERTY(VisibleAnywhere) UPointLightComponent* Brillo;

	EEstadoNoMuerto Estado = EEstadoNoMuerto::Dormido;

	/** Daño del jugador. bToque = toque fantasmal (daga). Devuelve PG perdidos. */
	int32 RecibirAtaque(int32 Danio, ETipoDanio TipoDanio, bool bToque, float Aturdir, FVector Empuje);
	void Aturdir(float Segundos);
	void Liberar();
	/** Saca a la Sombra de su espera (la llama el director al empezar el duelo). */
	void Despertar() { if (Estado == EEstadoNoMuerto::Dormido) Cambiar(EEstadoNoMuerto::Acecho); }
	bool EstaVivo() const { return Estado != EEstadoNoMuerto::Muerto && Estado != EEstadoNoMuerto::Liberado; }
	FText NombreVisible() const;

	/** Sombra: fase 2 a la mitad de vida. */
	bool bFase2 = false;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	float TiempoEstado = 0.f;
	float DuracionAturdido = 0.f;
	float VelocidadBase = 200.f;
	float AlcanceGolpe = 170.f;
	float TiempoAmago = 0.8f;
	float TiempoRecuperacion = 0.9f;
	int32 DanioDado = 6;
	int32 DanioFijo = 2;
	ETipoDanio TipoGolpe = ETipoDanio::Contundente;
	float FaseFlotar = 0.f;
	float CadenciaGemido = 0.f;
	int32 GolpesSeguidos = 0;
	bool bAvisoSaber = false;

	void Configurar();
	void Cambiar(EEstadoNoMuerto Nuevo);
	void Morir();
	bool VeAlJugador(float Distancia) const;
	void MoverHacia(const FVector& Destino, float Dt);
	void TickSombra(float Dt, class AVaelithCharacter* J, float Dist);
	void Sonar(const TCHAR* Ruta, float Volumen = 1.f, float Tono = 1.f);
	void ReproducirAnim(const TCHAR* Ruta, float Ritmo = 1.f);
};
