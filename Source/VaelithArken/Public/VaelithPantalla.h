// La interfaz del juego en UMG, construida en C++ (sin Blueprints ni PNG del proyecto Godot).
// Arte propio en /Game/Vaelith/UI2 (tools/ui_generar.py) y materiales M_UI_Barra / M_UI_Mapa (tools/ue/ui_importar.py).
#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "VaelithPantalla.generated.h"

class UCanvasPanel;
class UImage;
class UTextBlock;
class UButton;
class UBorder;
class UVerticalBox;
class UHorizontalBox;
class UFont;
class UTexture2D;
class UMaterialInstanceDynamic;
class AVaelithGameMode;
class AVaelithCharacter;

UCLASS()
class VAELITHARKEN_API UVaelithPantalla : public UUserWidget
{
	GENERATED_BODY()

public:
	/** Mapa de exploración (niebla de guerra): 128x128 sobre la imagen de cada mapa. */
	static constexpr int32 LadoNiebla = 128;

protected:
	virtual TSharedRef<SWidget> RebuildWidget() override;
	virtual void NativeTick(const FGeometry& Geo, float Dt) override;

private:
	bool bConstruido = false;
	UPROPERTY() UFont* FuenteTexto = nullptr;
	UPROPERTY() UFont* FuenteTitulo = nullptr;
	UPROPERTY() UCanvasPanel* Raiz = nullptr;

	// Capas
	UPROPERTY() UCanvasPanel* CapaJuego = nullptr;
	UPROPERTY() UCanvasPanel* CapaMenu = nullptr;
	UPROPERTY() UCanvasPanel* CapaPausa = nullptr;
	UPROPERTY() UCanvasPanel* CapaDote = nullptr;
	UPROPERTY() UCanvasPanel* CapaCreditos = nullptr;

	// Juego
	UPROPERTY() UMaterialInstanceDynamic* MatPG = nullptr;
	UPROPERTY() UMaterialInstanceDynamic* MatEscudo = nullptr;
	UPROPERTY() UMaterialInstanceDynamic* MatJefe = nullptr;
	UPROPERTY() UMaterialInstanceDynamic* MatMapa = nullptr;
	UPROPERTY() UTextBlock* TxtPG = nullptr;
	UPROPERTY() UTextBlock* TxtEscudo = nullptr;
	UPROPERTY() UBorder* BloqueEscudo = nullptr;
	UPROPERTY() TArray<UImage*> Rombos;
	UPROPERTY() TArray<UImage*> Espirales;
	UPROPERTY() UTextBlock* TxtCondiciones = nullptr;
	UPROPERTY() UTextBlock* TxtRecursos = nullptr;
	UPROPERTY() UVerticalBox* CajaInteraccion = nullptr;
	UPROPERTY() UTextBlock* TxtDestello = nullptr;
	UPROPERTY() UTextBlock* TxtMoribundo = nullptr;
	UPROPERTY() UTextBlock* TxtRetribucion = nullptr;
	UPROPERTY() UCanvasPanel* BloqueHUD = nullptr;
	UPROPERTY() UCanvasPanel* BloqueMapa = nullptr;
	UPROPERTY() UCanvasPanel* BloqueJefe = nullptr;
	UPROPERTY() UTextBlock* TxtJefe = nullptr;
	UPROPERTY() UBorder* MarcoAviso = nullptr;
	UPROPERTY() UTextBlock* TxtAvisoTitulo = nullptr;
	UPROPERTY() UTextBlock* TxtAvisoTexto = nullptr;
	// Línea del guion
	UPROPERTY() UBorder* MarcoLinea = nullptr;
	UPROPERTY() UTextBlock* TxtLinea = nullptr;
	UPROPERTY() UTextBlock* TxtLineaCentro = nullptr;
	UPROPERTY() UTextBlock* TxtRotulo = nullptr;
	// Fundidos
	UPROPERTY() UImage* FundidoNegro = nullptr;
	UPROPERTY() UImage* FundidoBlanco = nullptr;
	// Menú, pausa, dotes, créditos
	UPROPERTY() UButton* BtnContinuarPartida = nullptr;
	UPROPERTY() UTextBlock* TxtPie = nullptr;
	UPROPERTY() UTextBlock* TxtControles = nullptr;
	UPROPERTY() UTextBlock* TxtDoteTitulo = nullptr;
	UPROPERTY() TArray<UTextBlock*> TxtDoteNombre;
	UPROPERTY() TArray<UTextBlock*> TxtDoteDesc;
	UPROPERTY() UVerticalBox* CajaCreditos = nullptr;

	// Niebla de guerra
	UPROPERTY() UTexture2D* TexNiebla = nullptr;
	UPROPERTY() UTexture2D* TexMapaExterior = nullptr;
	UPROPERTY() UTexture2D* TexMapaCatacumba = nullptr;
	bool bEnCatacumbaAntes = false;
	int32 UltimaCeldaNiebla = -1;
	float RastroPG = 1.f, RastroEscudo = 1.f;
	int32 PGAntes = -1;
	float DestelloPG = 0.f;
	bool bCreditosArmados = false;

	void Construir();
	void ConstruirJuego();
	void ConstruirLinea();
	void ConstruirMenu();
	void ConstruirPausa();
	void ConstruirDote();
	void ConstruirCreditos();

	void ActualizarJuego(AVaelithGameMode* GM, AVaelithCharacter* J, float Dt);
	void ActualizarLinea(AVaelithGameMode* GM);
	void ActualizarMapa(AVaelithGameMode* GM, AVaelithCharacter* J);
	void ActualizarCreditos(AVaelithGameMode* GM);

	// Utilidades de construcción
	UTextBlock* NuevoTexto(const FString& S, float Tam, const FLinearColor& Color, bool bTitulo = false);
	UImage* NuevaImagen(const TCHAR* Textura, FVector2D Tam, const FLinearColor& Tinte = FLinearColor::White);
	UButton* NuevoBoton(const FString& Etiqueta);
	UBorder* NuevaPlaca(float Opacidad = 1.f);
	UCanvasPanel* NuevaCapa(UCanvasPanel* Padre);
	static class UCanvasPanelSlot* Poner(UCanvasPanel* Canvas, class UWidget* W, FVector2D Ancla, FVector2D Alineacion, FVector2D Pos, FVector2D Tam = FVector2D::ZeroVector);
	UTexture2D* Tex(const TCHAR* Nombre) const;

	UFUNCTION() void AlIniciar();
	UFUNCTION() void AlContinuar();
	UFUNCTION() void AlSalir();
	UFUNCTION() void AlVolver();
	UFUNCTION() void AlMenu();
	UFUNCTION() void AlDote0();
	UFUNCTION() void AlDote1();
};
