// Todo lo que se usa con E (altares, recuerdos, anclas, armas, puertas, cadáveres)
// y los disparadores de guion por zona.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Planilla.h"
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

/** Qué hace una opción al lograrse. */
UENUM(BlueprintType)
enum class EEfectoOpcion : uint8
{
	Escena,       // solo narra (según el grado)
	Abrir,        // abre la puerta Objetivo (o esta misma)
	Diagnosticar, // Saber del Osario: Pharasma dice qué es (Respeto, Compasión, Liberación, Enemigo, Amenaza)
	DarDescanso,  // cubrir o enterrar: Gracia
	Levantar,     // anatema: levanta al muerto (abre Objetivo), Corrupción
	Relevar,      // revoca la orden de un centinela (no-muerto con Hecho = Objetivo)
	Tomar         // toma Objeto; si es de un muerto, anatema
};

/** Una vía de resolver un obstáculo: con prueba de habilidad (Habilidad != Ninguna) o directa. */
USTRUCT(BlueprintType)
struct FOpcionInteraccion
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString Etiqueta;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) EEfectoOpcion Efecto = EEfectoOpcion::Escena;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) EHabilidad Habilidad = EHabilidad::Ninguna;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 CD = 15;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString EscenaExito;
	/** Si está vacía, el crítico usa la de éxito. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString EscenaCritico;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString EscenaFallo;
	/** Hecho necesario para que la opción aparezca (una llave, un recuerdo). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Requisito;
	/** Abrir/Levantar: Id de la puerta. Relevar: Hecho del no-muerto. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Objetivo;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Gracia = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Corrupcion = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bAnatema = false;
	/** Al lograrse, el objeto queda usado (desaparecen todas sus opciones). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bTerminal = true;
	/** Tomar: "pocion" o "agua_bendita". */
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString Objeto;
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

	/** Varias vías para el mismo obstáculo (la planilla en juego). Si hay opciones, reemplazan a Usar(). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Vaelith") TArray<FOpcionInteraccion> Opciones;
	int32 Seleccion = 0;

	UPROPERTY(VisibleAnywhere) UStaticMeshComponent* Malla;
	UPROPERTY(VisibleAnywhere) UPointLightComponent* Luz;

	bool bUsado = false;
	FText TextoAccion() const;
	bool PuedeUsarse() const;
	void Usar(class AVaelithCharacter* Quien);
	/** Índices de las opciones disponibles ahora (requisito cumplido, no agotadas ni ya logradas). */
	TArray<int32> OpcionesVisibles() const;
	/** Texto de la mira con las opciones, separadas por '|'; la elegida lleva ▸. */
	FString TextoOpciones(const class UFichaComponent* Ficha) const;
	void CambiarSeleccion(int32 Paso);
	/** Abrir esta puerta desde otra opción (Levantar, Forzar). */
	void AbrirDesdeAfuera();
	/** Restaura estado desde la partida (puertas abiertas, anclas rotas, etc.). */
	void MarcarUsado(bool bInstantaneo);

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	void UsarOpcion(class AVaelithCharacter* Quien, int32 Indice);
	FName HechoOpcion(int32 Indice) const { return FName(*FString::Printf(TEXT("%s_op%d"), *Id.ToString(), Indice)); }
	TSet<int32> Agotadas;  // fallo crítico: esa vía se cerró
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
	/** Eco de la muerte (Retornado): la escena solo aparece si pasa esta prueba oculta (Percepción). Una sola vez. */
	UPROPERTY(EditAnywhere, Category="Vaelith") EHabilidad Prueba = EHabilidad::Ninguna;
	UPROPERTY(EditAnywhere, Category="Vaelith") int32 CD = 15;

protected:
	UFUNCTION() void AlEntrar(UPrimitiveComponent* Comp, AActor* Otro, UPrimitiveComponent* OtroComp, int32 Indice, bool bBarrido, const FHitResult& Hit);
};
