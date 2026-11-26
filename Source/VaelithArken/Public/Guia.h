#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Guia.generated.h"

class UStaticMeshComponent;
class UPointLightComponent;

/** Estatua de Pharasma con farol: se enciende sola cuando Vaelith pasa cerca y queda encendida.
 *  Varias en fila marcan, sin sendero, el camino del bosque oscuro hacia la torre. */
UCLASS()
class VAELITHARKEN_API AEstatuaGuia : public AActor
{
	GENERATED_BODY()
public:
	AEstatuaGuia();
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere) UStaticMeshComponent* Base;
	UPROPERTY(VisibleAnywhere) UStaticMeshComponent* Estatua;
	UPROPERTY(VisibleAnywhere) UPointLightComponent* Farol;
	UPROPERTY(EditAnywhere) float Radio = 1100.f;
	UPROPERTY(EditAnywhere) FString Escena;          // se reproduce la primera vez (una sola vez en la partida)
	UPROPERTY(EditAnywhere) bool bEncendidaAlInicio = false;

protected:
	virtual void BeginPlay() override;
	bool bEncendida = false;
	float Brillo = 0.f;
	float Fase = 0.f;
};

/** El llamado de la torre: un destello violeta que cada tantos segundos escapa por la cima y,
 *  en el bosque oscuro, la Penumbra de Vaelith sube cuando mira hacia la torre. */
UCLASS()
class VAELITHARKEN_API ADestelloTorre : public AActor
{
	GENERATED_BODY()
public:
	ADestelloTorre();
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere) UPointLightComponent* Luz;
	UPROPERTY(EditAnywhere) float Periodo = 7.5f;
	UPROPERTY(EditAnywhere) float IntensidadMax = 60000.f;
	UPROPERTY(EditAnywhere) float RadioLlamado = 30000.f;   // dentro de este radio la Penumbra responde
	UPROPERTY(EditAnywhere) float YMinimaLlamado = 40000.f;  // solo después de la loma

protected:
	float T = 0.f;
};
