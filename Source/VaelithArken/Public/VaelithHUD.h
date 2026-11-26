// Todo lo que se dibuja en pantalla (Canvas): HUD, narración, menús, dotes, créditos.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "VaelithHUD.generated.h"

class UTexture2D;
class UFont;

UCLASS()
class VAELITHARKEN_API AVaelithHUD : public AHUD
{
	GENERATED_BODY()

public:
	AVaelithHUD();
	virtual void DrawHUD() override;
	virtual void NotifyHitBoxClick(FName BoxName) override;
	virtual void NotifyHitBoxBeginCursorOver(FName BoxName) override;
	virtual void NotifyHitBoxEndCursorOver(FName BoxName) override;

protected:
	virtual void BeginPlay() override;

private:
	UPROPERTY() TMap<FString, UTexture2D*> Texturas;
	UPROPERTY() UFont* FuenteTexto = nullptr;
	UPROPERTY() UFont* FuenteTitulo = nullptr;
	FName Sobre;
	float Escala = 1.f;

	UTexture2D* Tex(const FString& Nombre);
	void Texto(const FString& S, float X, float Y, const FLinearColor& Color, float Tam, bool bCentrado = false, UFont* Fuente = nullptr);
	TArray<FString> Envolver(const FString& S, float Ancho, float Tam, UFont* Fuente);
	void Boton(const FString& Textura, FName Id, float CX, float Y, float Alto);

	void DibujarMenu();
	void DibujarPausa();
	void DibujarJuego();
	void DibujarLinea();
	void DibujarAviso();
	void DibujarDotes();
	void DibujarCreditos();
	void DibujarFundidos();
};
