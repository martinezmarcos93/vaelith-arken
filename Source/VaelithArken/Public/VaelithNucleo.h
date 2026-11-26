// Tipos compartidos, instancia de juego y partida guardada.
#pragma once

#include "CoreMinimal.h"
#include "Engine/GameInstance.h"
#include "GameFramework/SaveGame.h"
#include "VaelithNucleo.generated.h"

UENUM(BlueprintType)
enum class EDote : uint8
{
	Ninguna,
	EscudoVeloz,       // levantar el escudo no cuesta acción
	GolpeVital,        // los tajos suman 1d6 vital contra no-muertos
	FocoExtra,         // +1 punto de foco
	AuraPharasma,      // los fantasmas cercanos sufren daño vital
	RetribucionMayor,  // el bloqueo perfecto aturde más y pega doble
	MuroEscudo         // dureza del escudo 7
};

/** Una línea del guion (se carga de Content/Vaelith/Guion/guion.json). */
USTRUCT(BlueprintType)
struct FLineaGuion
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString Texto;
	/** narracion | voz | pensamiento | titulo | pharasma | recuerdo | sombra | rotulo */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString Estilo = TEXT("narracion");
	UPROPERTY(EditAnywhere, BlueprintReadWrite) float Duracion = 4.f;
	/** Pausa antes de mostrarla. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) float Espera = 0.4f;
	/** La línea viene de una escena de interacción: mientras está en pantalla, Vaelith no se mueve. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bBloquea = false;
};

UCLASS()
class VAELITHARKEN_API UVaelithPartida : public USaveGame
{
	GENERATED_BODY()
public:
	UPROPERTY() FName Altar;
	UPROPERTY() int32 Nivel = 1;
	UPROPERTY() TArray<EDote> Dotes;
	UPROPERTY() int32 Gracia = 0;
	UPROPERTY() TArray<int32> Recuerdos;
	UPROPERTY() TArray<FName> Hechos;  // anclas liberadas, puertas abiertas, escenas vistas
	UPROPERTY() bool bTieneArmas = false;
	UPROPERTY() bool bTieneDaga = false;
	UPROPERTY() FDateTime Fecha;
};

UCLASS()
class VAELITHARKEN_API UVaelithGameInstance : public UGameInstance
{
	GENERATED_BODY()
public:
	static const FString Ranura;

	/** Al abrir el mapa: mostrar menú principal (true) o jugar. */
	UPROPERTY(BlueprintReadWrite) bool bArrancarEnMenu = true;
	/** Al jugar: cargar la partida guardada en vez de empezar de cero. */
	UPROPERTY(BlueprintReadWrite) bool bContinuar = false;

	UFUNCTION(BlueprintPure) bool HayPartidaGuardada() const;
};
