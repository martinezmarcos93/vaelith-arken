#include "VaelithPantalla.h"
#include "VaelithGameMode.h"
#include "VaelithCharacter.h"
#include "VaelithNucleo.h"
#include "FichaComponent.h"
#include "NoMuerto.h"
#include "Planilla.h"
#include "Blueprint/WidgetTree.h"
#include "Components/CanvasPanel.h"
#include "Components/CanvasPanelSlot.h"
#include "Components/Image.h"
#include "Components/TextBlock.h"
#include "Components/Button.h"
#include "Components/ButtonSlot.h"
#include "Components/Border.h"
#include "Components/VerticalBox.h"
#include "Components/VerticalBoxSlot.h"
#include "Components/HorizontalBox.h"
#include "Components/HorizontalBoxSlot.h"
#include "Components/Overlay.h"
#include "Components/OverlaySlot.h"
#include "Engine/Font.h"
#include "Engine/FontFace.h"
#include "Engine/Texture2D.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Kismet/GameplayStatics.h"

namespace
{
	const FLinearColor Oro(0.85f, 0.70f, 0.40f);
	const FLinearColor Hueso(0.88f, 0.85f, 0.78f);
	const FLinearColor Tenue(0.58f, 0.57f, 0.60f);
	const FLinearColor Violeta(0.72f, 0.56f, 1.f);
	const FLinearColor Sangre(0.75f, 0.2f, 0.16f);
	const TCHAR* RutaUI = TEXT("/Game/Vaelith/UI2/");

	float Alfa(float Inicio, float Dur, float Ahora, float Entrada = 0.6f, float Salida = 0.8f)
	{
		const float T = Ahora - Inicio;
		return FMath::Clamp(FMath::Min(T / Entrada, (Dur - T) / Salida), 0.f, 1.f);
	}

	FSlateBrush Pincel(UTexture2D* T, FVector2D Tam, bool bCaja = false)
	{
		FSlateBrush B;
		B.SetResourceObject(T);
		B.ImageSize = Tam;
		if (bCaja)
		{
			B.DrawAs = ESlateBrushDrawType::Box;
			B.Margin = FMargin(0.22f);
		}
		return B;
	}
}

UTexture2D* UVaelithPantalla::Tex(const TCHAR* Nombre) const
{
	return LoadObject<UTexture2D>(nullptr, *FString::Printf(TEXT("%s%s.%s"), RutaUI, Nombre, Nombre));
}

TSharedRef<SWidget> UVaelithPantalla::RebuildWidget()
{
	if (!bConstruido && WidgetTree)
	{
		Construir();
		bConstruido = true;
	}
	return Super::RebuildWidget();
}

UCanvasPanelSlot* UVaelithPantalla::Poner(UCanvasPanel* Canvas, UWidget* W, FVector2D Ancla, FVector2D Alineacion, FVector2D Pos, FVector2D Tam)
{
	UCanvasPanelSlot* S = Canvas->AddChildToCanvas(W);
	S->SetAnchors(FAnchors(Ancla.X, Ancla.Y));
	S->SetAlignment(Alineacion);
	S->SetPosition(Pos);
	if (Tam.IsZero()) S->SetAutoSize(true);
	else S->SetSize(Tam);
	return S;
}

UTextBlock* UVaelithPantalla::NuevoTexto(const FString& S, float Tam, const FLinearColor& Color, bool bTitulo)
{
	UTextBlock* T = WidgetTree->ConstructWidget<UTextBlock>();
	T->SetText(FText::FromString(S));
	UFont* F = bTitulo ? FuenteTitulo : FuenteTexto;
	if (F) T->SetFont(FSlateFontInfo(F, Tam));
	T->SetColorAndOpacity(FSlateColor(Color));
	T->SetShadowOffset(FVector2D(2.f, 2.f));
	T->SetShadowColorAndOpacity(FLinearColor(0.f, 0.f, 0.f, 0.7f));
	return T;
}

UImage* UVaelithPantalla::NuevaImagen(const TCHAR* Textura, FVector2D Tam, const FLinearColor& Tinte)
{
	UImage* I = WidgetTree->ConstructWidget<UImage>();
	if (UTexture2D* T = Tex(Textura)) I->SetBrush(Pincel(T, Tam));
	I->SetColorAndOpacity(Tinte);
	return I;
}

UBorder* UVaelithPantalla::NuevaPlaca(float Opacidad)
{
	UBorder* B = WidgetTree->ConstructWidget<UBorder>();
	if (UTexture2D* T = Tex(TEXT("T_UI_Placa"))) B->SetBrush(Pincel(T, FVector2D(256.f, 256.f), true));
	B->SetBrushColor(FLinearColor(1.f, 1.f, 1.f, Opacidad));
	B->SetPadding(FMargin(42.f, 26.f));
	return B;
}

UButton* UVaelithPantalla::NuevoBoton(const FString& Etiqueta)
{
	UButton* B = WidgetTree->ConstructWidget<UButton>();
	FButtonStyle Estilo;
	UTexture2D* Normal = Tex(TEXT("T_UI_Boton"));
	UTexture2D* Sobre = Tex(TEXT("T_UI_Boton_Sobre"));
	Estilo.SetNormal(Pincel(Normal, FVector2D(460.f, 100.f)));
	Estilo.SetHovered(Pincel(Sobre, FVector2D(460.f, 100.f)));
	Estilo.SetPressed(Pincel(Sobre, FVector2D(460.f, 100.f)));
	Estilo.SetNormalPadding(FMargin(0.f));
	Estilo.SetPressedPadding(FMargin(0.f));
	B->SetStyle(Estilo);
	UTextBlock* T = NuevoTexto(Etiqueta, 26.f, Hueso, true);
	T->SetJustification(ETextJustify::Center);
	B->AddChild(T);
	if (UButtonSlot* S = Cast<UButtonSlot>(T->Slot))
	{
		S->SetHorizontalAlignment(HAlign_Center);
		S->SetVerticalAlignment(VAlign_Center);
	}
	return B;
}

UCanvasPanel* UVaelithPantalla::NuevaCapa(UCanvasPanel* Padre)
{
	UCanvasPanel* C = WidgetTree->ConstructWidget<UCanvasPanel>();
	UCanvasPanelSlot* S = Padre->AddChildToCanvas(C);
	S->SetAnchors(FAnchors(0.f, 0.f, 1.f, 1.f));
	S->SetOffsets(FMargin(0.f));
	return C;
}

void UVaelithPantalla::Construir()
{
	auto Crear = [this](const TCHAR* Cara) -> UFont*
	{
		UFontFace* F = LoadObject<UFontFace>(nullptr, Cara);
		if (!F) return nullptr;
		UFont* Fuente = NewObject<UFont>(this);
		Fuente->FontCacheType = EFontCacheType::Runtime;
		FTypefaceEntry Entrada(TEXT("Regular"));
		Entrada.Font = FFontData(F);
		Fuente->GetMutableInternalCompositeFont().DefaultTypeface.Fonts.Add(Entrada);
		return Fuente;
	};
	FuenteTexto = Crear(TEXT("/Game/Vaelith/UI/Fuentes/EBGaramond.EBGaramond"));
	FuenteTitulo = Crear(TEXT("/Game/Vaelith/UI/Fuentes/Cinzel.Cinzel"));
	if (!FuenteTitulo) FuenteTitulo = FuenteTexto;

	Raiz = WidgetTree->ConstructWidget<UCanvasPanel>(UCanvasPanel::StaticClass(), TEXT("Raiz"));
	WidgetTree->RootWidget = Raiz;
	CapaJuego = NuevaCapa(Raiz);
	CapaJuego->SetVisibility(ESlateVisibility::HitTestInvisible);
	ConstruirJuego();
	ConstruirLinea();
	// Fundidos (debajo de los menús, encima del juego)
	FundidoNegro = WidgetTree->ConstructWidget<UImage>();
	FundidoNegro->SetColorAndOpacity(FLinearColor(0.f, 0.f, 0.f, 0.f));
	FundidoNegro->SetVisibility(ESlateVisibility::HitTestInvisible);
	UCanvasPanelSlot* SN = Raiz->AddChildToCanvas(FundidoNegro);
	SN->SetAnchors(FAnchors(0.f, 0.f, 1.f, 1.f));
	SN->SetOffsets(FMargin(0.f));
	FundidoBlanco = WidgetTree->ConstructWidget<UImage>();
	FundidoBlanco->SetColorAndOpacity(FLinearColor(0.95f, 0.93f, 0.88f, 0.f));
	FundidoBlanco->SetVisibility(ESlateVisibility::HitTestInvisible);
	UCanvasPanelSlot* SB = Raiz->AddChildToCanvas(FundidoBlanco);
	SB->SetAnchors(FAnchors(0.f, 0.f, 1.f, 1.f));
	SB->SetOffsets(FMargin(0.f));
	ConstruirMenu();
	ConstruirPausa();
	ConstruirDote();
	ConstruirCreditos();
}

void UVaelithPantalla::ConstruirJuego()
{
	UMaterialInterface* MBarra = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Vaelith/UI2/M_UI_Barra.M_UI_Barra"));
	BloqueHUD = WidgetTree->ConstructWidget<UCanvasPanel>();
	Poner(CapaJuego, BloqueHUD, FVector2D(0.f, 1.f), FVector2D(0.f, 1.f), FVector2D(36.f, -24.f), FVector2D(760.f, 200.f));

	// Barra de vida: pista + relleno (material) + marco
	auto Barra = [&](float Y, float Ancho, UMaterialInstanceDynamic*& Mat, const FLinearColor& A, const FLinearColor& B) -> UTextBlock*
	{
		Poner(BloqueHUD, NuevaImagen(TEXT("T_UI_Barra_Pista"), FVector2D(Ancho, 44.f)), FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(0.f, Y), FVector2D(Ancho, 44.f));
		UImage* Relleno = WidgetTree->ConstructWidget<UImage>();
		if (MBarra)
		{
			Mat = UMaterialInstanceDynamic::Create(MBarra, this);
			Mat->SetVectorParameterValue(TEXT("ColorA"), A);
			Mat->SetVectorParameterValue(TEXT("ColorB"), B);
			Relleno->SetBrushFromMaterial(Mat);
		}
		Poner(BloqueHUD, Relleno, FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(0.f, Y), FVector2D(Ancho, 44.f));
		Poner(BloqueHUD, NuevaImagen(TEXT("T_UI_Barra_Marco"), FVector2D(Ancho, 44.f)), FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(0.f, Y), FVector2D(Ancho, 44.f));
		UTextBlock* T = NuevoTexto(TEXT(""), 18.f, Hueso);
		Poner(BloqueHUD, T, FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(Ancho + 12.f, Y + 9.f));
		return T;
	};
	TxtCondiciones = NuevoTexto(TEXT(""), 16.f, FLinearColor(0.95f, 0.55f, 0.45f));
	Poner(BloqueHUD, TxtCondiciones, FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(4.f, 0.f));
	TxtPG = Barra(26.f, 380.f, MatPG, FLinearColor(0.55f, 0.36f, 0.12f), FLinearColor(0.97f, 0.80f, 0.45f));
	TxtEscudo = Barra(74.f, 250.f, MatEscudo, FLinearColor(0.30f, 0.20f, 0.50f), FLinearColor(0.62f, 0.50f, 0.85f));
	// Acciones (rombos) y foco (espirales)
	for (int32 i = 0; i < 3; ++i)
	{
		UImage* R = NuevaImagen(TEXT("T_UI_Rombo"), FVector2D(24.f, 24.f), Oro);
		Poner(BloqueHUD, R, FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(6.f + i * 32.f, 128.f), FVector2D(24.f, 24.f));
		Rombos.Add(R);
	}
	for (int32 i = 0; i < 3; ++i)
	{
		UImage* E = NuevaImagen(TEXT("T_UI_Espiral"), FVector2D(30.f, 30.f), Oro);
		Poner(BloqueHUD, E, FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(118.f + i * 36.f, 125.f), FVector2D(30.f, 30.f));
		Espirales.Add(E);
	}
	TxtRecursos = NuevoTexto(TEXT(""), 15.f, Tenue);
	Poner(BloqueHUD, TxtRecursos, FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(240.f, 131.f));

	// Mira
	UImage* Mira = WidgetTree->ConstructWidget<UImage>();
	Mira->SetColorAndOpacity(FLinearColor(0.9f, 0.88f, 0.8f, 0.55f));
	Poner(CapaJuego, Mira, FVector2D(0.5f, 0.5f), FVector2D(0.5f, 0.5f), FVector2D::ZeroVector, FVector2D(4.f, 4.f));
	CajaInteraccion = WidgetTree->ConstructWidget<UVerticalBox>();
	Poner(CapaJuego, CajaInteraccion, FVector2D(0.5f, 0.5f), FVector2D(0.5f, 0.f), FVector2D(0.f, 60.f));
	TxtDestello = NuevoTexto(TEXT(""), 24.f, Oro, true);
	Poner(CapaJuego, TxtDestello, FVector2D(0.5f, 0.5f), FVector2D(0.5f, 1.f), FVector2D(0.f, -60.f));
	TxtRetribucion = NuevoTexto(TEXT("Retribución"), 28.f, Oro, true);
	Poner(CapaJuego, TxtRetribucion, FVector2D(0.5f, 0.5f), FVector2D(0.5f, 1.f), FVector2D(0.f, -100.f));
	TxtMoribundo = NuevoTexto(TEXT(""), 30.f, Sangre, true);
	TxtMoribundo->SetJustification(ETextJustify::Center);
	Poner(CapaJuego, TxtMoribundo, FVector2D(0.5f, 0.5f), FVector2D(0.5f, 1.f), FVector2D(0.f, -120.f));

	// Minimapa (arriba a la derecha)
	BloqueMapa = WidgetTree->ConstructWidget<UCanvasPanel>();
	Poner(CapaJuego, BloqueMapa, FVector2D(1.f, 0.f), FVector2D(1.f, 0.f), FVector2D(-30.f, 30.f), FVector2D(250.f, 250.f));
	TexMapaExterior = Tex(TEXT("T_Mapa_Exterior"));
	TexMapaCatacumba = Tex(TEXT("T_Mapa_Catacumba"));
	TexNiebla = UTexture2D::CreateTransient(LadoNiebla, LadoNiebla, PF_B8G8R8A8);
	if (TexNiebla)
	{
		TexNiebla->Filter = TF_Bilinear;
		TexNiebla->SRGB = false;
		TexNiebla->UpdateResource();
	}
	UImage* Mapa = WidgetTree->ConstructWidget<UImage>();
	if (UMaterialInterface* MM = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Vaelith/UI2/M_UI_Mapa.M_UI_Mapa")))
	{
		MatMapa = UMaterialInstanceDynamic::Create(MM, this);
		if (TexNiebla) MatMapa->SetTextureParameterValue(TEXT("Niebla"), TexNiebla);
		Mapa->SetBrushFromMaterial(MatMapa);
	}
	Poner(BloqueMapa, Mapa, FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(250.f, 250.f));
	Poner(BloqueMapa, NuevaImagen(TEXT("T_UI_Flecha"), FVector2D(22.f, 22.f)), FVector2D(0.f, 0.f), FVector2D(0.5f, 0.5f), FVector2D(125.f, 125.f), FVector2D(22.f, 22.f));
	Poner(BloqueMapa, NuevaImagen(TEXT("T_UI_Mapa_Marco"), FVector2D(250.f, 250.f)), FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(250.f, 250.f));

	// Aviso (debajo del minimapa)
	MarcoAviso = NuevaPlaca(0.95f);
	UVerticalBox* CajaAviso = WidgetTree->ConstructWidget<UVerticalBox>();
	TxtAvisoTitulo = NuevoTexto(TEXT(""), 21.f, Oro, true);
	TxtAvisoTexto = NuevoTexto(TEXT(""), 18.f, Hueso);
	TxtAvisoTexto->SetAutoWrapText(true);
	CajaAviso->AddChildToVerticalBox(TxtAvisoTitulo);
	CajaAviso->AddChildToVerticalBox(TxtAvisoTexto);
	MarcoAviso->SetContent(CajaAviso);
	Poner(CapaJuego, MarcoAviso, FVector2D(1.f, 0.f), FVector2D(1.f, 0.f), FVector2D(-30.f, 300.f), FVector2D(520.f, 150.f));

	// Vida del jefe
	BloqueJefe = WidgetTree->ConstructWidget<UCanvasPanel>();
	Poner(CapaJuego, BloqueJefe, FVector2D(0.5f, 0.f), FVector2D(0.5f, 0.f), FVector2D(0.f, 24.f), FVector2D(720.f, 90.f));
	TxtJefe = NuevoTexto(TEXT(""), 26.f, Violeta, true);
	Poner(BloqueJefe, TxtJefe, FVector2D(0.5f, 0.f), FVector2D(0.5f, 0.f), FVector2D(0.f, 0.f));
	UImage* RellenoJefe = WidgetTree->ConstructWidget<UImage>();
	if (MBarra)
	{
		MatJefe = UMaterialInstanceDynamic::Create(MBarra, this);
		MatJefe->SetVectorParameterValue(TEXT("ColorA"), FLinearColor(0.25f, 0.10f, 0.45f));
		MatJefe->SetVectorParameterValue(TEXT("ColorB"), FLinearColor(0.60f, 0.32f, 0.95f));
		RellenoJefe->SetBrushFromMaterial(MatJefe);
	}
	Poner(BloqueJefe, NuevaImagen(TEXT("T_UI_Barra_Pista"), FVector2D(720.f, 44.f)), FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(0.f, 40.f), FVector2D(720.f, 44.f));
	Poner(BloqueJefe, RellenoJefe, FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(0.f, 40.f), FVector2D(720.f, 44.f));
	Poner(BloqueJefe, NuevaImagen(TEXT("T_UI_Barra_Marco"), FVector2D(720.f, 44.f)), FVector2D(0.f, 0.f), FVector2D(0.f, 0.f), FVector2D(0.f, 40.f), FVector2D(720.f, 44.f));
}

void UVaelithPantalla::ConstruirLinea()
{
	MarcoLinea = NuevaPlaca(0.9f);
	TxtLinea = NuevoTexto(TEXT(""), 27.f, Hueso);
	TxtLinea->SetJustification(ETextJustify::Center);
	TxtLinea->SetAutoWrapText(true);
	MarcoLinea->SetContent(TxtLinea);
	MarcoLinea->SetHorizontalAlignment(HAlign_Center);
	MarcoLinea->SetVisibility(ESlateVisibility::HitTestInvisible);
	UCanvasPanelSlot* S = Poner(Raiz, MarcoLinea, FVector2D(0.5f, 0.78f), FVector2D(0.5f, 0.5f), FVector2D::ZeroVector, FVector2D(1240.f, 120.f));
	S->SetAutoSize(true);
	TxtLineaCentro = NuevoTexto(TEXT(""), 54.f, Oro, true);
	TxtLineaCentro->SetJustification(ETextJustify::Center);
	TxtLineaCentro->SetAutoWrapText(true);
	TxtLineaCentro->SetVisibility(ESlateVisibility::HitTestInvisible);
	Poner(Raiz, TxtLineaCentro, FVector2D(0.5f, 0.44f), FVector2D(0.5f, 0.5f), FVector2D::ZeroVector, FVector2D(1400.f, 220.f));
	TxtRotulo = NuevoTexto(TEXT(""), 24.f, Tenue, true);
	TxtRotulo->SetVisibility(ESlateVisibility::HitTestInvisible);
	Poner(Raiz, TxtRotulo, FVector2D(0.5f, 0.12f), FVector2D(0.5f, 0.5f), FVector2D::ZeroVector);
}

void UVaelithPantalla::ConstruirMenu()
{
	CapaMenu = NuevaCapa(Raiz);
	UImage* Velo = WidgetTree->ConstructWidget<UImage>();
	Velo->SetColorAndOpacity(FLinearColor(0.f, 0.f, 0.f, 0.35f));
	UCanvasPanelSlot* SV = CapaMenu->AddChildToCanvas(Velo);
	SV->SetAnchors(FAnchors(0.f, 0.f, 1.f, 1.f));
	SV->SetOffsets(FMargin(0.f));
	Velo->SetVisibility(ESlateVisibility::HitTestInvisible);
	Poner(CapaMenu, NuevaImagen(TEXT("T_UI_Titulo"), FVector2D(900.f, 280.f)), FVector2D(0.5f, 0.f), FVector2D(0.5f, 0.f), FVector2D(0.f, 70.f), FVector2D(900.f, 280.f));
	Poner(CapaMenu, NuevaImagen(TEXT("T_UI_Subtitulo"), FVector2D(620.f, 95.f)), FVector2D(0.5f, 0.f), FVector2D(0.5f, 0.f), FVector2D(0.f, 360.f), FVector2D(620.f, 95.f));
	UVerticalBox* Caja = WidgetTree->ConstructWidget<UVerticalBox>();
	UButton* B1 = NuevoBoton(TEXT("Iniciar partida"));
	B1->OnClicked.AddDynamic(this, &UVaelithPantalla::AlIniciar);
	BtnContinuarPartida = NuevoBoton(TEXT("Continuar partida"));
	BtnContinuarPartida->OnClicked.AddDynamic(this, &UVaelithPantalla::AlContinuar);
	UButton* B3 = NuevoBoton(TEXT("Salir del juego"));
	B3->OnClicked.AddDynamic(this, &UVaelithPantalla::AlSalir);
	for (UButton* B : { B1, BtnContinuarPartida, B3 })
	{
		UVerticalBoxSlot* S = Caja->AddChildToVerticalBox(B);
		S->SetPadding(FMargin(0.f, 8.f));
		S->SetHorizontalAlignment(HAlign_Center);
	}
	Poner(CapaMenu, Caja, FVector2D(0.5f, 0.f), FVector2D(0.5f, 0.f), FVector2D(0.f, 500.f));
	TxtPie = NuevoTexto(TEXT(""), 18.f, Tenue);
	Poner(CapaMenu, TxtPie, FVector2D(0.5f, 1.f), FVector2D(0.5f, 1.f), FVector2D(0.f, -36.f));
}

void UVaelithPantalla::ConstruirPausa()
{
	CapaPausa = NuevaCapa(Raiz);
	UImage* Velo = WidgetTree->ConstructWidget<UImage>();
	Velo->SetColorAndOpacity(FLinearColor(0.f, 0.f, 0.f, 0.9f));  // negro: la noche azul no se cuela
	UCanvasPanelSlot* SV = CapaPausa->AddChildToCanvas(Velo);
	SV->SetAnchors(FAnchors(0.f, 0.f, 1.f, 1.f));
	SV->SetOffsets(FMargin(0.f));
	UTextBlock* Tit = NuevoTexto(TEXT("Pausa"), 54.f, Oro, true);
	Poner(CapaPausa, Tit, FVector2D(0.5f, 0.f), FVector2D(0.5f, 0.f), FVector2D(0.f, 150.f));
	Poner(CapaPausa, NuevaImagen(TEXT("T_UI_Espiral"), FVector2D(48.f, 48.f), Violeta), FVector2D(0.5f, 0.f), FVector2D(0.5f, 0.f), FVector2D(0.f, 235.f), FVector2D(48.f, 48.f));
	UVerticalBox* Caja = WidgetTree->ConstructWidget<UVerticalBox>();
	UButton* B1 = NuevoBoton(TEXT("Continuar partida"));
	B1->OnClicked.AddDynamic(this, &UVaelithPantalla::AlVolver);
	UButton* B2 = NuevoBoton(TEXT("Menú principal"));
	B2->OnClicked.AddDynamic(this, &UVaelithPantalla::AlMenu);
	UButton* B3 = NuevoBoton(TEXT("Salir del juego"));
	B3->OnClicked.AddDynamic(this, &UVaelithPantalla::AlSalir);
	for (UButton* B : { B1, B2, B3 })
	{
		UVerticalBoxSlot* S = Caja->AddChildToVerticalBox(B);
		S->SetPadding(FMargin(0.f, 8.f));
		S->SetHorizontalAlignment(HAlign_Center);
	}
	Poner(CapaPausa, Caja, FVector2D(0.5f, 0.f), FVector2D(0.5f, 0.f), FVector2D(0.f, 320.f));
	TxtControles = NuevoTexto(TEXT(""), 17.f, Tenue);
	Poner(CapaPausa, TxtControles, FVector2D(0.f, 1.f), FVector2D(0.f, 1.f), FVector2D(60.f, -40.f));
}

void UVaelithPantalla::ConstruirDote()
{
	CapaDote = NuevaCapa(Raiz);
	UImage* Velo = WidgetTree->ConstructWidget<UImage>();
	Velo->SetColorAndOpacity(FLinearColor(0.f, 0.f, 0.f, 0.6f));
	UCanvasPanelSlot* SV = CapaDote->AddChildToCanvas(Velo);
	SV->SetAnchors(FAnchors(0.f, 0.f, 1.f, 1.f));
	SV->SetOffsets(FMargin(0.f));
	TxtDoteTitulo = NuevoTexto(TEXT(""), 38.f, Oro, true);
	Poner(CapaDote, TxtDoteTitulo, FVector2D(0.5f, 0.5f), FVector2D(0.5f, 1.f), FVector2D(0.f, -200.f));
	for (int32 i = 0; i < 2; ++i)
	{
		UButton* B = WidgetTree->ConstructWidget<UButton>();
		FButtonStyle Estilo;
		UTexture2D* Placa = Tex(TEXT("T_UI_Placa"));
		Estilo.SetNormal(Pincel(Placa, FVector2D(256.f, 256.f), true));
		FSlateBrush Sobre = Pincel(Placa, FVector2D(256.f, 256.f), true);
		Sobre.TintColor = FSlateColor(FLinearColor(1.15f, 1.05f, 1.3f));
		Estilo.SetHovered(Sobre);
		Estilo.SetPressed(Sobre);
		B->SetStyle(Estilo);
		B->OnClicked.AddDynamic(this, i == 0 ? &UVaelithPantalla::AlDote0 : &UVaelithPantalla::AlDote1);
		UVerticalBox* Caja = WidgetTree->ConstructWidget<UVerticalBox>();
		UTextBlock* Tecla = NuevoTexto(FString::Printf(TEXT("[%d]"), i + 1), 18.f, Tenue);
		UTextBlock* Nombre = NuevoTexto(TEXT(""), 28.f, Oro, true);
		UTextBlock* Desc = NuevoTexto(TEXT(""), 20.f, Hueso);
		Desc->SetAutoWrapText(true);
		Nombre->SetJustification(ETextJustify::Center);
		Desc->SetJustification(ETextJustify::Center);
		Caja->AddChildToVerticalBox(Tecla);
		Caja->AddChildToVerticalBox(Nombre)->SetPadding(FMargin(0.f, 6.f));
		Caja->AddChildToVerticalBox(Desc);
		B->AddChild(Caja);
		if (UButtonSlot* S = Cast<UButtonSlot>(Caja->Slot)) S->SetPadding(FMargin(40.f, 30.f));
		Poner(CapaDote, B, FVector2D(0.5f, 0.5f), FVector2D(i == 0 ? 1.f : 0.f, 0.f), FVector2D(i == 0 ? -20.f : 20.f, -130.f), FVector2D(500.f, 260.f));
		TxtDoteNombre.Add(Nombre);
		TxtDoteDesc.Add(Desc);
	}
}

void UVaelithPantalla::ConstruirCreditos()
{
	CapaCreditos = NuevaCapa(Raiz);
	CapaCreditos->SetVisibility(ESlateVisibility::HitTestInvisible);
	CajaCreditos = WidgetTree->ConstructWidget<UVerticalBox>();
	Poner(CapaCreditos, CajaCreditos, FVector2D(0.5f, 1.f), FVector2D(0.5f, 0.f), FVector2D(0.f, 40.f));
}

// ---------------------------------------------------------------- tick

void UVaelithPantalla::NativeTick(const FGeometry& Geo, float Dt)
{
	Super::NativeTick(Geo, Dt);
	AVaelithGameMode* GM = GetWorld() ? GetWorld()->GetAuthGameMode<AVaelithGameMode>() : nullptr;
	if (!GM || !bConstruido) return;
	AVaelithCharacter* J = Cast<AVaelithCharacter>(UGameplayStatics::GetPlayerPawn(this, 0));
	const EModoJuego M = GM->Modo;
	const bool bMenu = M == EModoJuego::Menu, bCreditos = M == EModoJuego::Creditos;
	CapaMenu->SetVisibility(bMenu ? ESlateVisibility::SelfHitTestInvisible : ESlateVisibility::Collapsed);
	CapaPausa->SetVisibility(M == EModoJuego::Pausa ? ESlateVisibility::Visible : ESlateVisibility::Collapsed);
	CapaDote->SetVisibility(M == EModoJuego::EligiendoDote ? ESlateVisibility::SelfHitTestInvisible : ESlateVisibility::Collapsed);
	CapaCreditos->SetVisibility(bCreditos ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
	CapaJuego->SetVisibility(!bMenu && !bCreditos && J && !J->EnDespertar() ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
	FundidoNegro->SetColorAndOpacity(FLinearColor(0.f, 0.f, 0.f, GM->FundidoNegro));
	FundidoBlanco->SetColorAndOpacity(FLinearColor(0.95f, 0.93f, 0.88f, GM->FundidoBlanco));

	if (bMenu)
	{
		UVaelithGameInstance* GI = Cast<UVaelithGameInstance>(GetGameInstance());
		BtnContinuarPartida->SetVisibility(GI && GI->HayPartidaGuardada() ? ESlateVisibility::Visible : ESlateVisibility::Collapsed);
		TxtPie->SetText(FText::FromString(GM->TextoGuion(TEXT("menu_pie"))));
	}
	if (M == EModoJuego::Pausa)
	{
		TxtControles->SetText(FText::FromString(GM->TextoGuion(TEXT("controles")).Replace(TEXT("|"), TEXT("\n"))));
	}
	if (M == EModoJuego::EligiendoDote)
	{
		TxtDoteTitulo->SetText(FText::FromString(GM->TextoGuion(TEXT("dote_titulo"))));
		for (int32 i = 0; i < 2; ++i)
		{
			TxtDoteNombre[i]->SetText(AVaelithGameMode::NombreDote(GM->OpcionesDote[i]));
			TxtDoteDesc[i]->SetText(AVaelithGameMode::DescripcionDote(GM->OpcionesDote[i]));
		}
	}
	if (bCreditos) ActualizarCreditos(GM);
	if (J && !bMenu && !bCreditos) ActualizarJuego(GM, J, Dt);
	ActualizarLinea(GM);
}

void UVaelithPantalla::ActualizarJuego(AVaelithGameMode* GM, AVaelithCharacter* J, float Dt)
{
	UFichaComponent* F = J->Ficha;
	const float Ahora = GM->Ahora();
	// Vida con rastro de daño y destello
	const float FracPG = F->PGMax() > 0 ? float(F->PG) / F->PGMax() : 0.f;
	if (PGAntes >= 0 && F->PG < PGAntes) DestelloPG = 1.f;
	PGAntes = F->PG;
	RastroPG = FracPG > RastroPG ? FracPG : FMath::FInterpConstantTo(RastroPG, FracPG, Dt, 0.35f);
	DestelloPG = FMath::FInterpConstantTo(DestelloPG, 0.f, Dt, 3.f);
	if (MatPG)
	{
		MatPG->SetScalarParameterValue(TEXT("Llenado"), FracPG);
		MatPG->SetScalarParameterValue(TEXT("Rastro"), RastroPG);
		MatPG->SetScalarParameterValue(TEXT("Destello"), DestelloPG);
		MatPG->SetVectorParameterValue(TEXT("ColorB"), F->bMoribundo ? Sangre : FLinearColor(0.97f, 0.80f, 0.45f));
	}
	TxtPG->SetText(FText::FromString(FString::Printf(TEXT("%d / %d"), F->PG, F->PGMax())));
	const float FracEsc = F->PGEscudoMax > 0 ? float(F->PGEscudo) / F->PGEscudoMax : 0.f;
	RastroEscudo = FracEsc > RastroEscudo ? FracEsc : FMath::FInterpConstantTo(RastroEscudo, FracEsc, Dt, 0.35f);
	if (MatEscudo)
	{
		MatEscudo->SetScalarParameterValue(TEXT("Llenado"), (J->bTieneArmas && F->bTieneEscudo) ? FracEsc : 0.f);
		MatEscudo->SetScalarParameterValue(TEXT("Rastro"), (J->bTieneArmas && F->bTieneEscudo) ? RastroEscudo : 0.f);
		MatEscudo->SetVectorParameterValue(TEXT("ColorB"), F->EscudoRoto() ? FLinearColor(0.95f, 0.45f, 0.35f) : FLinearColor(0.62f, 0.50f, 0.85f));
	}
	TxtEscudo->SetText(FText::FromString(!J->bTieneArmas ? TEXT("") : (F->EscudoDestruido() ? TEXT("escudo destruido") : (F->EscudoRoto() ? TEXT("escudo roto") : TEXT("escudo")))));
	for (int32 i = 0; i < Rombos.Num(); ++i)
	{
		Rombos[i]->SetVisibility(i < F->AccionesMax ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
		Rombos[i]->SetColorAndOpacity(i < F->Acciones ? Oro : FLinearColor(0.2f, 0.2f, 0.22f, 0.8f));
	}
	for (int32 i = 0; i < Espirales.Num(); ++i)
	{
		Espirales[i]->SetVisibility(i < F->FocoMax() ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
		Espirales[i]->SetColorAndOpacity(F->bAnatema ? FLinearColor(0.35f, 0.15f, 0.12f, 0.8f) : (i < F->Foco ? Violeta : FLinearColor(0.25f, 0.25f, 0.28f, 0.8f)));
	}
	// Condiciones y recursos
	FString Cond;
	for (const ECondicion C : { ECondicion::Asustado, ECondicion::Desprevenido, ECondicion::Debilitado, ECondicion::Herido, ECondicion::Moribundo })
	{
		const int32 V = F->Condicion(C);
		if (V <= 0) continue;
		if (!Cond.IsEmpty()) Cond += TEXT("  ·  ");
		Cond += Planilla::Nombre(C).ToString() + (C == ECondicion::Desprevenido ? FString() : FString::Printf(TEXT(" %d"), V));
	}
	if (F->bAnatema) Cond += Cond.IsEmpty() ? TEXT("Anatema") : TEXT("  ·  Anatema");
	TxtCondiciones->SetText(FText::FromString(Cond));
	FString Rec = FString::Printf(TEXT("favor %d   ·   agua bendita %d"), F->PuntosHeroe, J->AguaBendita);
	if (J->Pociones > 0) Rec += FString::Printf(TEXT("   ·   pociones %d"), J->Pociones);
	if (J->bUsandoDaga) Rec += TEXT("   ·   daga");
	TxtRecursos->SetText(FText::FromString(Rec));

	// Interacción (varias vías: la elegida en hueso, las otras tenues)
	CajaInteraccion->ClearChildren();
	if (!J->TextoInteraccion.IsEmpty() && GM->Modo == EModoJuego::Juego)
	{
		TArray<FString> Lineas;
		J->TextoInteraccion.ParseIntoArray(Lineas, TEXT("|"));
		for (const FString& L : Lineas)
		{
			const bool bAyuda = L.StartsWith(TEXT("("));
			const bool bElegida = L.StartsWith(TEXT("[E]")) || Lineas.Num() == 1;
			UTextBlock* T = NuevoTexto(L.TrimStart(), bAyuda ? 14.f : 21.f, bAyuda ? Tenue : (bElegida ? Hueso : Tenue));
			T->SetJustification(ETextJustify::Center);
			if (UVerticalBoxSlot* S = CajaInteraccion->AddChildToVerticalBox(T)) S->SetHorizontalAlignment(HAlign_Center);
		}
	}
	const bool bDestello = !GM->DestelloTexto.IsEmpty() && Ahora < GM->DestelloFin;
	TxtDestello->SetText(FText::FromString(bDestello ? GM->DestelloTexto : FString()));
	TxtDestello->SetColorAndOpacity(FSlateColor(FLinearColor(Oro.R, Oro.G, Oro.B, bDestello ? FMath::Clamp((GM->DestelloFin - Ahora) * 2.f, 0.f, 1.f) : 0.f)));
	const float DesdeParada = GetWorld()->GetTimeSeconds() - J->UltimoBloqueoPerfecto;
	TxtRetribucion->SetRenderOpacity(DesdeParada < 0.9f ? 1.f - DesdeParada / 0.9f : 0.f);
	if (F->bMoribundo)
	{
		TxtMoribundo->SetText(FText::FromString(GM->TextoGuion(TEXT("moribundo")) + FString::Printf(TEXT("\nMoribundo %d de %d"), F->Condicion(ECondicion::Moribundo), F->MuerteEn())));
		TxtMoribundo->SetRenderOpacity(0.6f + 0.4f * FMath::Sin(Ahora * 6.f));
	}
	else TxtMoribundo->SetText(FText::GetEmpty());

	// Aviso
	const float Resta = GM->AvisoFin - Ahora;
	const bool bAviso = Resta > 0.f && !GM->AvisoTitulo.IsEmpty();
	MarcoAviso->SetVisibility(bAviso ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
	if (bAviso)
	{
		MarcoAviso->SetRenderOpacity(FMath::Clamp(Resta / 0.8f, 0.f, 1.f));
		TxtAvisoTitulo->SetText(FText::FromString(GM->AvisoTitulo));
		TxtAvisoTexto->SetText(FText::FromString(GM->AvisoTexto));
	}
	// Jefe
	const bool bJefe = GM->Jefe && GM->Jefe->EstaVivo();
	BloqueJefe->SetVisibility(bJefe ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
	if (bJefe && MatJefe)
	{
		TxtJefe->SetText(GM->Jefe->NombreVisible());
		const float Frac = float(GM->Jefe->Ficha->PG) / FMath::Max(1, GM->Jefe->Ficha->PGMax());
		MatJefe->SetScalarParameterValue(TEXT("Llenado"), Frac);
		MatJefe->SetScalarParameterValue(TEXT("Rastro"), Frac);
	}
	ActualizarMapa(GM, J);
}

void UVaelithPantalla::ActualizarMapa(AVaelithGameMode* GM, AVaelithCharacter* J)
{
	if (!MatMapa || !TexNiebla || !GM->Partida) return;
	const FVector P = J->GetActorLocation();
	// Catacumba: y < 6200 (el terreno empieza en la boca de la cripta). Coordenadas = las de tools/ui_generar.py.
	const bool bCatacumba = P.Y < 6200.f;
	FVector2D UV;
	float Zoom, Radio;
	if (bCatacumba)
	{
		UV = FVector2D((96.f + 16.f + P.X / 400.f * 32.f) / 1024.f, (256.f + 16.f + P.Y / 400.f * 32.f) / 1024.f);
		Zoom = 0.26f;
		Radio = 0.05f;
	}
	else
	{
		UV = FVector2D((P.X + 24000.f) / 84000.f, (P.Y - 6200.f) / 84000.f);
		Zoom = 0.11f;
		Radio = 0.026f;
	}
	TArray<uint8>& Visto = bCatacumba ? GM->Partida->ExploradoCatacumba : GM->Partida->ExploradoExterior;
	if (Visto.Num() != LadoNiebla * LadoNiebla) Visto.Init(0, LadoNiebla * LadoNiebla);
	const int32 CX = FMath::Clamp(FMath::FloorToInt(UV.X * LadoNiebla), 0, LadoNiebla - 1);
	const int32 CY = FMath::Clamp(FMath::FloorToInt(UV.Y * LadoNiebla), 0, LadoNiebla - 1);
	const int32 Celda = CY * LadoNiebla + CX + (bCatacumba ? 1 << 20 : 0);
	if (Celda != UltimaCeldaNiebla || bCatacumba != bEnCatacumbaAntes)
	{
		UltimaCeldaNiebla = Celda;
		bEnCatacumbaAntes = bCatacumba;
		MatMapa->SetTextureParameterValue(TEXT("Mapa"), bCatacumba ? TexMapaCatacumba : TexMapaExterior);
		const int32 R = FMath::CeilToInt(Radio * LadoNiebla);
		for (int32 y = CY - R; y <= CY + R; ++y)
		{
			for (int32 x = CX - R; x <= CX + R; ++x)
			{
				if (x < 0 || y < 0 || x >= LadoNiebla || y >= LadoNiebla) continue;
				const float D = FVector2D(x - CX, y - CY).Size() / FMath::Max(1, R);
				const uint8 V = uint8(FMath::Clamp((1.25f - D) * 255.f, 0.f, 255.f));
				uint8& Celda2 = Visto[y * LadoNiebla + x];
				Celda2 = FMath::Max(Celda2, V);
			}
		}
		// Subir la máscara a la textura (BGRA, el material lee R)
		TArray<FColor>* Datos = new TArray<FColor>();
		Datos->SetNumUninitialized(LadoNiebla * LadoNiebla);
		for (int32 i = 0; i < Visto.Num(); ++i) (*Datos)[i] = FColor(Visto[i], Visto[i], Visto[i], 255);
		FUpdateTextureRegion2D* Region = new FUpdateTextureRegion2D(0, 0, 0, 0, LadoNiebla, LadoNiebla);
		TexNiebla->UpdateTextureRegions(0, 1, Region, LadoNiebla * 4, 4, reinterpret_cast<uint8*>(Datos->GetData()),
			[Datos](uint8*, const FUpdateTextureRegion2D* Reg) { delete Datos; delete Reg; });
	}
	MatMapa->SetVectorParameterValue(TEXT("Centro"), FLinearColor(UV.X, UV.Y, 0.f, 0.f));
	MatMapa->SetScalarParameterValue(TEXT("Zoom"), Zoom);
	// El mapa gira para que el frente de Vaelith apunte hacia arriba (imagen: +x derecha, +y abajo).
	MatMapa->SetScalarParameterValue(TEXT("Giro"), FMath::DegreesToRadians(J->GetControlRotation().Yaw + 90.f));
}

void UVaelithPantalla::ActualizarLinea(AVaelithGameMode* GM)
{
	const FLineaActiva& A = GM->LineaActiva();
	const bool bHay = !A.Linea.Texto.IsEmpty() && GM->Modo != EModoJuego::Menu && GM->Modo != EModoJuego::Pausa;
	const FString& E = A.Linea.Estilo;
	const bool bCentro = E == TEXT("titulo") || E == TEXT("pharasma");
	const bool bRotulo = E == TEXT("rotulo");
	const float Al = bHay ? Alfa(A.Inicio, A.Linea.Duracion, GM->Ahora()) : 0.f;
	MarcoLinea->SetVisibility(bHay && !bCentro && !bRotulo ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
	TxtLineaCentro->SetVisibility(bHay && bCentro ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
	TxtRotulo->SetVisibility(bHay && bRotulo ? ESlateVisibility::HitTestInvisible : ESlateVisibility::Collapsed);
	if (!bHay) return;
	const FText Texto = FText::FromString(A.Linea.Texto);
	if (bCentro)
	{
		TxtLineaCentro->SetText(Texto);
		if (FuenteTitulo) TxtLineaCentro->SetFont(FSlateFontInfo(FuenteTitulo, E == TEXT("titulo") ? 56.f : 32.f));
		TxtLineaCentro->SetRenderOpacity(Al);
	}
	else if (bRotulo)
	{
		TxtRotulo->SetText(Texto);
		TxtRotulo->SetRenderOpacity(Al);
	}
	else
	{
		FLinearColor C = Hueso;
		if (E == TEXT("recuerdo")) C = FLinearColor(0.92f, 0.86f, 0.74f);
		else if (E == TEXT("sombra")) C = Violeta;
		else if (E == TEXT("voz")) C = FLinearColor(0.95f, 0.92f, 0.85f);
		TxtLinea->SetText(Texto);
		TxtLinea->SetColorAndOpacity(FSlateColor(C));
		TxtLinea->SetWrapTextAt(1150.f);
		MarcoLinea->SetRenderOpacity(Al);
	}
}

void UVaelithPantalla::ActualizarCreditos(AVaelithGameMode* GM)
{
	if (!bCreditosArmados)
	{
		bCreditosArmados = true;
		TArray<FString> Lineas;
		GM->TextoGuion(TEXT("creditos")).ParseIntoArray(Lineas, TEXT("|"), false);
		for (const FString& L : Lineas)
		{
			const bool bTitulo = L.StartsWith(TEXT("#"));
			UTextBlock* T = NuevoTexto(bTitulo ? L.RightChop(1) : L, bTitulo ? 30.f : 21.f, bTitulo ? Oro : Hueso, bTitulo);
			T->SetJustification(ETextJustify::Center);
			UVerticalBoxSlot* S = CajaCreditos->AddChildToVerticalBox(T);
			S->SetHorizontalAlignment(HAlign_Center);
			S->SetPadding(FMargin(0.f, bTitulo ? 18.f : 4.f));
		}
	}
	CajaCreditos->SetRenderTranslation(FVector2D(0.f, -(GM->Ahora() - GM->InicioCreditos) * 42.f));
}

// ---------------------------------------------------------------- botones

void UVaelithPantalla::AlIniciar() { if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->MenuIniciar(); }
void UVaelithPantalla::AlContinuar() { if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->MenuContinuar(); }
void UVaelithPantalla::AlSalir() { if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->MenuSalir(); }
void UVaelithPantalla::AlVolver() { if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->Pausar(false); }
void UVaelithPantalla::AlMenu() { if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->VolverAlMenu(); }
void UVaelithPantalla::AlDote0() { if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->ElegirDote(0); }
void UVaelithPantalla::AlDote1() { if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->ElegirDote(1); }
