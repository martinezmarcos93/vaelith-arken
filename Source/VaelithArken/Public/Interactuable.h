// Todo lo que se usa con E (altares, recuerdos, anclas, armas, puertas, cadáveres)
// y los disparadores de guion por zona.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Interactuable.generated.h"

class UBoxComponent;
class UStaticMeshComponent;
class UPointLightComponent;

UENUM(BlueprintType)
enum class ETipoInteractuable : uint8
{
	Altar,       // punto de control, guarda la partida
	Recuerdo,    // fragmento de memoria (Valor = 1..4)
	Ancla,       // libera a un fantasma atado
	Armas,       // espada y escudo (al despertar)
	DagaPharasma,
	Puerta,      // se abre si se cumple Requisito (hecho)
	Cadaver,     // cubrirlo suma Gracia
	Lectura,     // inscripción: muestra una escena del guion
	Espejo       // reflejo en el agua: escena del guion, una sola vez
};

UCLASS()
class VAELITHARKEN_API AInteractuable : public AActor
{
	GENERATED_BODY()

public:
	AInteractuable();

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Vaelith") ETipoInteractuable Tipo = ETipoInteractuable::Lectura;
	/** Identificador único (altar, hecho que registra al usarse). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Vaelith") FName Id;
	/** Escena del guion que se reproduce al usarlo. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Vaelith") FString Escena;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Vaelith") int32 Valor = 0;
	/** Puerta: hecho necesario para abrirla. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Vaelith") FName Requisito;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Vaelith") FString Etiqueta;

	UPROPERTY(VisibleAnywhere) UStaticMeshComponent* Malla;
	UPROPERTY(VisibleAnywhere) UPointLightComponent* Luz;

	bool bUsado = false;
	FText TextoAccion() const;
	bool PuedeUsarse() const;
	void Usar(class AVaelithCharacter* Quien);
	/** Restaura estado desde la partida (puertas abiertas, anclas rotas, etc.). */
	void MarcarUsado(bool bInstantaneo);

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	float Animacion = -1.f;
	FVector PosInicial;
	FRotator RotInicial;
};

/** Volumen que dispara una escena del guion (una vez) y fija la penumbra de la zona. */
UCLASS()
class VAELITHARKEN_API ATriggerGuion : public AActor
{
	GENERATED_BODY()

public:
	ATriggerGuion();

	UPROPERTY(VisibleAnywhere) UBoxComponent* Caja;
	UPROPERTY(EditAnywhere, Category="Vaelith") FString Escena;
	/** Si >= 0, al entrar fija la penumbra (1 = catacumba, 0 = exterior). */
	UPROPERTY(EditAnywhere, Category="Vaelith") float Penumbra = -1.f;
	/** Música de la zona (ruta de asset) o vacío. */
	UPROPERTY(EditAnywhere, Category="Vaelith") FString Musica;
	/** Inicia la pelea con la Sombra. */
	UPROPERTY(EditAnywhere, Category="Vaelith") bool bJefe = false;

protected:
	UFUNCTION() void AlEntrar(UPrimitiveComponent* Comp, AActor* Otro, UPrimitiveComponent* OtroComp, int32 Indice, bool bBarrido, const FHitResult& Hit);
};
