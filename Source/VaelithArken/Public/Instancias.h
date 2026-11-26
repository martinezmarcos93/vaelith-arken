#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Instancias.generated.h"

class UStaticMesh;
class UHierarchicalInstancedStaticMeshComponent;

USTRUCT(BlueprintType)
struct FGrupoInstancias
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite) UStaticMesh* Malla = nullptr;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) TArray<FTransform> Transformadas;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) float Distancia = 0.f;   // 0 = sin recorte
	UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bSombra = true;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bColision = true;
};

/** Muchas copias de pocas mallas (árboles, tumbas, cercas) en componentes instanciados:
 *  una llamada de dibujo por malla en lugar de una por actor. Los datos viven en Grupos;
 *  los componentes se arman al construir (editor) y al empezar el juego. */
UCLASS()
class VAELITHARKEN_API AInstancias : public AActor
{
	GENERATED_BODY()
public:
	AInstancias();
	virtual void OnConstruction(const FTransform& Transform) override;
	virtual void BeginPlay() override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite) TArray<FGrupoInstancias> Grupos;

private:
	void Armar();
	UPROPERTY(Transient) TArray<UHierarchicalInstancedStaticMeshComponent*> Componentes;
};
