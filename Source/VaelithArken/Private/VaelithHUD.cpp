#include "VaelithHUD.h"
#include "VaelithPantalla.h"
#include "Blueprint/UserWidget.h"

AVaelithHUD::AVaelithHUD() {}

void AVaelithHUD::BeginPlay()
{
	Super::BeginPlay();
	if (APlayerController* PC = GetOwningPlayerController())
	{
		Pantalla = CreateWidget<UVaelithPantalla>(PC, UVaelithPantalla::StaticClass());
		if (Pantalla) Pantalla->AddToViewport(0);
	}
}
