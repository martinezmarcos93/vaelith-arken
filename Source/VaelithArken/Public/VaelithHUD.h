// La interfaz vive en UMG (UVaelithPantalla, construida en C++). El HUD solo la crea y la mantiene en pantalla.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "VaelithHUD.generated.h"

class UVaelithPantalla;

UCLASS()
class VAELITHARKEN_API AVaelithHUD : public AHUD
{
	GENERATED_BODY()

public:
	AVaelithHUD();

protected:
	virtual void BeginPlay() override;

private:
	UPROPERTY() UVaelithPantalla* Pantalla = nullptr;
};
