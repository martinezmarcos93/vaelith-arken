#include "VaelithHUD.h"
#include "Planilla.h"
#include "VaelithGameMode.h"
#include "VaelithCharacter.h"
#include "NoMuerto.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/Font.h"
#include "Engine/FontFace.h"
#include "Engine/Texture2D.h"
#include "Kismet/GameplayStatics.h"

namespace
{
	const FLinearColor Oro(0.85f, 0.70f, 0.40f);
	const FLinearColor Hueso(0.88f, 0.85f, 0.78f);
	const FLinearColor Tenue(0.55f, 0.55f, 0.58f);
	const FLinearColor Violeta(0.70f, 0.55f, 1.f);
	const FLinearColor Sangre(0.62f, 0.12f, 0.10f);

	float Alfa(float Inicio, float Dur, float Ahora, float Entrada = 0.6f, float Salida = 0.8f)
	{
		const float T = Ahora - Inicio;
		return FMath::Clamp(FMath::Min(T / Entrada, (Dur - T) / Salida), 0.f, 1.f);
	}
}

AVaelithHUD::AVaelithHUD() {}

void AVaelithHUD::BeginPlay()
{
	Super::BeginPlay();
	// Fuentes en tiempo de ejecución a partir de las caras importadas (EB Garamond, Cinzel).
	auto Crear = [this](const TCHAR* Cara) -> UFont*
	{
		UFontFace* F = LoadObject<UFontFace>(nullptr, Cara);
		if (!F) return nullptr;
		UFont* Fuente = NewObject<UFont>(this);
		Fuente->FontCacheType = EFontCacheType::Runtime;
		Fuente->LegacyFontSize = 24;
		FTypefaceEntry Entrada(TEXT("Regular"));
		Entrada.Font = FFontData(F);
		Fuente->GetMutableInternalCompositeFont().DefaultTypeface.Fonts.Add(Entrada);
		return Fuente;
	};
	FuenteTexto = Crear(TEXT("/Game/Vaelith/UI/Fuentes/EBGaramond.EBGaramond"));
	FuenteTitulo = Crear(TEXT("/Game/Vaelith/UI/Fuentes/Cinzel.Cinzel"));
	if (!FuenteTexto) FuenteTexto = GEngine->GetLargeFont();
	if (!FuenteTitulo) FuenteTitulo = FuenteTexto;
}

UTexture2D* AVaelithHUD::Tex(const FString& Nombre)
{
	if (UTexture2D** T = Texturas.Find(Nombre)) return *T;
	UTexture2D* T = LoadObject<UTexture2D>(nullptr, *FString::Printf(TEXT("/Game/Vaelith/UI/%s.%s"), *Nombre, *Nombre));
	Texturas.Add(Nombre, T);
	return T;
}

void AVaelithHUD::Texto(const FString& S, float X, float Y, const FLinearColor& Color, float Tam, bool bCentrado, UFont* Fuente)
{
	UFont* F = Fuente ? Fuente : FuenteTexto;
	// Las fuentes importadas se escalan a partir de 24 px de base.
	const float K = Tam * Escala / 24.f;
	float W = 0.f, H = 0.f;
	GetTextSize(S, W, H, F, K);
	const float PX = bCentrado ? X - W * 0.5f : X;
	DrawText(S, FLinearColor(0.f, 0.f, 0.f, Color.A * 0.6f), PX + 2.f, Y + 2.f, F, K);
	DrawText(S, Color, PX, Y, F, K);
}

TArray<FString> AVaelithHUD::Envolver(const FString& S, float Ancho, float Tam, UFont* Fuente)
{
	TArray<FString> Lineas, Palabras;
	S.ParseIntoArray(Palabras, TEXT(" "));
	FString Actual;
	const float K = Tam * Escala / 24.f;
	for (const FString& P : Palabras)
	{
		const FString Prueba = Actual.IsEmpty() ? P : Actual + TEXT(" ") + P;
		float W = 0.f, H = 0.f;
		GetTextSize(Prueba, W, H, Fuente ? Fuente : FuenteTexto, K);
		if (W > Ancho && !Actual.IsEmpty())
		{
			Lineas.Add(Actual);
			Actual = P;
		}
		else
		{
			Actual = Prueba;
		}
	}
	if (!Actual.IsEmpty()) Lineas.Add(Actual);
	return Lineas;
}

void AVaelithHUD::Boton(const FString& Textura, FName Id, float CX, float Y, float Alto)
{
	UTexture2D* T = Tex(Textura);
	if (!T) return;
	const float Ratio = float(T->GetSizeX()) / FMath::Max(1, T->GetSizeY());
	const bool bSobre = Sobre == Id;
	const float H = Alto * (bSobre ? 1.06f : 1.f);
	const float W = H * Ratio;
	DrawTexture(T, CX - W * 0.5f, Y - (H - Alto) * 0.5f, W, H, 0.f, 0.f, 1.f, 1.f, bSobre ? FLinearColor(1.15f, 1.05f, 0.95f) : FLinearColor(0.82f, 0.82f, 0.82f));
	AddHitBox(FVector2D(CX - W * 0.5f, Y), FVector2D(W, Alto), Id, true);
}

void AVaelithHUD::DrawHUD()
{
	Super::DrawHUD();
	if (!Canvas) return;
	Escala = Canvas->ClipY / 1080.f;
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (!GM) return;

	switch (GM->Modo)
	{
	case EModoJuego::Menu:
		DibujarFundidos();
		DibujarMenu();
		return;
	case EModoJuego::Creditos:
		DibujarFundidos();
		DibujarCreditos();
		return;
	default:
		break;
	}
	DibujarJuego();
	DibujarLinea();
	DibujarAviso();
	DibujarFundidos();
	if (GM->Modo == EModoJuego::Muerte) DibujarLinea();  // la voz se lee sobre el negro
	if (GM->Modo == EModoJuego::EligiendoDote) DibujarDotes();
	if (GM->Modo == EModoJuego::Pausa) DibujarPausa();
}

void AVaelithHUD::DibujarFundidos()
{
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (GM->FundidoNegro > 0.001f) DrawRect(FLinearColor(0.f, 0.f, 0.f, GM->FundidoNegro), 0.f, 0.f, Canvas->ClipX, Canvas->ClipY);
	if (GM->FundidoBlanco > 0.001f) DrawRect(FLinearColor(0.95f, 0.93f, 0.88f, GM->FundidoBlanco), 0.f, 0.f, Canvas->ClipX, Canvas->ClipY);
}

void AVaelithHUD::DibujarMenu()
{
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	const float CX = Canvas->ClipX * 0.5f;
	// Viñeta para que el título se lea sobre la escena.
	DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.35f), 0.f, 0.f, Canvas->ClipX, Canvas->ClipY);

	if (UTexture2D* T = Tex(TEXT("T_Titulo")))
	{
		const float W = 900.f * Escala, H = W * T->GetSizeY() / FMath::Max(1, T->GetSizeX());
		DrawTexture(T, CX - W * 0.5f, 90.f * Escala, W, H, 0.f, 0.f, 1.f, 1.f);
	}
	else
	{
		Texto(TEXT("VAELITH ARKEN"), CX, 150.f * Escala, Oro, 72.f, true, FuenteTitulo);
	}
	if (UTexture2D* S = Tex(TEXT("T_Subtitulo")))
	{
		const float W = 520.f * Escala, H = W * S->GetSizeY() / FMath::Max(1, S->GetSizeX());
		DrawTexture(S, CX - W * 0.5f, 420.f * Escala, W, H, 0.f, 0.f, 1.f, 1.f, FLinearColor(1.f, 1.f, 1.f, 0.85f));
	}

	float Y = 610.f * Escala;
	const float Alto = 140.f * Escala;
	Boton(TEXT("T_Boton_Iniciar"), TEXT("iniciar"), CX, Y, Alto);
	Y += Alto + 12.f * Escala;
	UVaelithGameInstance* GI = Cast<UVaelithGameInstance>(GetGameInstance());
	if (GI && GI->HayPartidaGuardada())
	{
		Boton(TEXT("T_Boton_Continuar"), TEXT("continuar"), CX, Y, Alto);
		Y += Alto + 12.f * Escala;
	}
	Boton(TEXT("T_Boton_Salir"), TEXT("salir"), CX, Y, Alto);
	Texto(GM->TextoGuion(TEXT("menu_pie")), CX, Canvas->ClipY - 50.f * Escala, Tenue, 16.f, true);
}

void AVaelithHUD::DibujarPausa()
{
	const float CX = Canvas->ClipX * 0.5f;
	DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.9f), 0.f, 0.f, Canvas->ClipX, Canvas->ClipY); // negro: la noche azul no se cuela
	if (UTexture2D* T = Tex(TEXT("T_Menu_Pausa")))
	{
		const float W = 560.f * Escala, H = W * T->GetSizeY() / FMath::Max(1, T->GetSizeX());
		DrawTexture(T, CX - W * 0.5f, 140.f * Escala, W, H, 0.f, 0.f, 1.f, 1.f);
	}
	const float Alto = 130.f * Escala;
	float Y = 470.f * Escala;
	Boton(TEXT("T_Boton_Continuar"), TEXT("volver"), CX, Y, Alto);
	Y += Alto + 12.f * Escala;
	Boton(TEXT("T_Boton_Regresar"), TEXT("menu"), CX, Y, Alto);
	Y += Alto + 12.f * Escala;
	Boton(TEXT("T_Boton_Salir"), TEXT("salir"), CX, Y, Alto);

	// Controles, por si el jugador los olvidó.
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	TArray<FString> Lineas;
	GM->TextoGuion(TEXT("controles")).ParseIntoArray(Lineas, TEXT("|"));
	float YC = Canvas->ClipY - (Lineas.Num() * 24.f + 40.f) * Escala;
	for (const FString& L : Lineas)
	{
		Texto(L, 60.f * Escala, YC, Tenue, 17.f);
		YC += 24.f * Escala;
	}
}

void AVaelithHUD::DibujarJuego()
{
	AVaelithCharacter* J = Cast<AVaelithCharacter>(GetOwningPawn());
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (!J || J->EnDespertar()) return;
	UFichaComponent* F = J->Ficha;
	const float E = Escala;
	const float X = 48.f * E, Y = Canvas->ClipY - 150.f * E;

	// Barras: PG (oro) y escudo (violeta apagado), con el marco del proyecto original.
	auto Barra = [&](float BY, float Frac, const FString& Relleno, float Ancho, const FLinearColor& Tinte)
	{
		const float H = 26.f * E;
		if (UTexture2D* Pista = Tex(TEXT("T_Barra_Pista"))) DrawTexture(Pista, X, BY, Ancho, H, 0, 0, 1, 1, FLinearColor(1, 1, 1, 0.8f));
		else DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.6f), X, BY, Ancho, H);
		if (UTexture2D* R = Tex(Relleno)) DrawTexture(R, X, BY, Ancho * Frac, H, 0, 0, Frac, 1, Tinte);
		else DrawRect(Tinte, X + 3.f, BY + 3.f, (Ancho - 6.f) * Frac, H - 6.f);
		if (UTexture2D* Marco = Tex(TEXT("T_Barra_Marco"))) DrawTexture(Marco, X - 6.f * E, BY - 5.f * E, Ancho + 12.f * E, H + 10.f * E, 0, 0, 1, 1);
	};
	const float FracPG = F->PGMax() > 0 ? float(F->PG) / F->PGMax() : 0.f;
	Barra(Y, FracPG, TEXT("T_Barra_Oro"), 320.f * E, F->bMoribundo ? Sangre : FLinearColor::White);
	Texto(FString::Printf(TEXT("%d / %d"), F->PG, F->PGMax()), X + 330.f * E, Y - 1.f * E, Hueso, 18.f);
	if (J->bTieneArmas && F->bTieneEscudo)
	{
		const float FracEsc = F->PGEscudoMax > 0 ? float(F->PGEscudo) / F->PGEscudoMax : 0.f;
		Barra(Y + 38.f * E, FracEsc, TEXT("T_Barra_Violeta"), 200.f * E, F->EscudoRoto() ? FLinearColor(1.f, 0.5f, 0.4f) : FLinearColor(0.75f, 0.75f, 0.85f));
		Texto(F->EscudoDestruido() ? TEXT("escudo destruido") : (F->EscudoRoto() ? TEXT("escudo roto") : TEXT("escudo")), X + 210.f * E, Y + 37.f * E, Tenue, 15.f);
	}
	// Tres acciones: rombos.
	for (int32 i = 0; i < F->AccionesMax; ++i)
	{
		const bool bLlena = i < F->Acciones;
		const float RX = X + i * 30.f * E, RY = Y + 78.f * E, S = 16.f * E;
		DrawRect(bLlena ? Oro : FLinearColor(0.2f, 0.2f, 0.22f, 0.8f), RX, RY, S, S);
	}
	// Foco: espirales.
	for (int32 i = 0; i < F->FocoMax(); ++i)
	{
		const bool bLleno = i < F->Foco;
		const float S = 26.f * E, FX = X + 110.f * E + i * 32.f * E, FY = Y + 73.f * E;
		if (UTexture2D* Esp = Tex(TEXT("T_Espiral"))) DrawTexture(Esp, FX, FY, S, S, 0, 0, 1, 1, bLleno ? Oro : FLinearColor(0.25f, 0.25f, 0.28f, 0.8f));
		else DrawRect(bLleno ? Oro : FLinearColor(0.25f, 0.25f, 0.28f, 0.8f), FX + 5.f, FY + 5.f, S - 10.f, S - 10.f);
	}
	if (J->bUsandoDaga) Texto(TEXT("daga"), X + 200.f * E, Y + 76.f * E, Tenue, 15.f);

	// Mira
	const float CX = Canvas->ClipX * 0.5f, CY = Canvas->ClipY * 0.5f;
	DrawRect(FLinearColor(0.9f, 0.88f, 0.8f, 0.5f), CX - 1.5f, CY - 1.5f, 3.f, 3.f);

	// Interacción
	if (!J->TextoInteraccion.IsEmpty() && GM->Modo == EModoJuego::Juego)
	{
		// Varias vías (opciones de la planilla): una línea por opción; la elegida lleva [E].
		TArray<FString> Lineas;
		J->TextoInteraccion.ParseIntoArray(Lineas, TEXT("|"));
		float LY = CY + 60.f * E;
		for (const FString& L : Lineas)
		{
			const bool bElegida = L.StartsWith(TEXT("[E]"));
			const bool bAyuda = L.StartsWith(TEXT("("));
			Texto(L.TrimStart(), CX, LY, bAyuda ? Tenue : (bElegida || Lineas.Num() == 1 ? Hueso : Tenue), bAyuda ? 14.f : 20.f, true);
			LY += (bAyuda ? 20.f : 27.f) * E;
		}
	}
	// Destello: resultado de una prueba, "Crítico", "Esquivado".
	if (!GM->DestelloTexto.IsEmpty() && GM->Ahora() < GM->DestelloFin)
	{
		const float Resta = GM->DestelloFin - GM->Ahora();
		Texto(GM->DestelloTexto, CX, CY - 70.f * E, FLinearColor(Oro.R, Oro.G, Oro.B, FMath::Clamp(Resta * 2.f, 0.f, 1.f)), 22.f, true, FuenteTitulo);
	}
	// Condiciones activas (PF2e) y recursos, bajo las barras.
	{
		FString Cond;
		for (const ECondicion C : { ECondicion::Asustado, ECondicion::Desprevenido, ECondicion::Debilitado, ECondicion::Herido, ECondicion::Moribundo })
		{
			const int32 V = F->Condicion(C);
			if (V <= 0) continue;
			if (!Cond.IsEmpty()) Cond += TEXT("  ·  ");
			Cond += Planilla::Nombre(C).ToString() + (C == ECondicion::Desprevenido ? FString() : FString::Printf(TEXT(" %d"), V));
		}
		if (F->bAnatema) Cond += Cond.IsEmpty() ? TEXT("Anatema") : TEXT("  ·  Anatema");
		if (!Cond.IsEmpty()) Texto(Cond, X, Y - 34.f * E, FLinearColor(0.95f, 0.55f, 0.45f), 16.f);
		FString Rec = FString::Printf(TEXT("favor %d   agua bendita %d"), F->PuntosHeroe, J->AguaBendita);
		if (J->Pociones > 0) Rec += FString::Printf(TEXT("   pociones %d"), J->Pociones);
		Texto(Rec, X + 250.f * E, Y + 76.f * E, Tenue, 14.f);
	}

	// Moribundo: Diehard
	if (F->bMoribundo)
	{
		const float Pulso = 0.6f + 0.4f * FMath::Sin(GM->Ahora() * 6.f);
		Texto(GM->TextoGuion(TEXT("moribundo")), CX, CY - 120.f * E, FLinearColor(0.9f, 0.3f, 0.25f, Pulso), 30.f, true, FuenteTitulo);
		Texto(FString::Printf(TEXT("Moribundo %d de %d"), F->Condicion(ECondicion::Moribundo), F->MuerteEn()), CX, CY - 80.f * E, FLinearColor(0.9f, 0.5f, 0.45f, Pulso), 18.f, true);
	}

	// Bloqueo perfecto
	const float DesdeParada = GetWorld()->GetTimeSeconds() - J->UltimoBloqueoPerfecto;
	if (DesdeParada < 0.9f)
	{
		Texto(TEXT("Retribución"), CX, CY - 80.f * E, FLinearColor(Oro.R, Oro.G, Oro.B, 1.f - DesdeParada / 0.9f), 26.f, true, FuenteTitulo);
	}

	// Vida del jefe
	if (GM->Jefe && GM->Jefe->EstaVivo())
	{
		const float W = 700.f * E, BX = CX - W * 0.5f, BY = 60.f * E;
		Texto(GM->Jefe->NombreVisible().ToString(), CX, BY - 34.f * E, Violeta, 26.f, true, FuenteTitulo);
		DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.7f), BX, BY, W, 14.f * E);
		const float Frac = float(GM->Jefe->Ficha->PG) / FMath::Max(1, GM->Jefe->Ficha->PGMax());
		DrawRect(FLinearColor(0.42f, 0.22f, 0.7f), BX + 2.f, BY + 2.f, (W - 4.f) * Frac, 14.f * E - 4.f);
	}
}

void AVaelithHUD::DibujarLinea()
{
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	const FLineaActiva& A = GM->LineaActiva();
	if (A.Linea.Texto.IsEmpty()) return;
	const float Al = Alfa(A.Inicio, A.Linea.Duracion, GM->Ahora());
	const FString& Estilo = A.Linea.Estilo;
	const float CX = Canvas->ClipX * 0.5f;

	FLinearColor Color = Hueso;
	float Tam = 26.f;
	float Y = Canvas->ClipY * 0.72f;
	UFont* Fuente = FuenteTexto;
	bool bMarco = false;
	if (Estilo == TEXT("titulo")) { Color = Oro; Tam = 54.f; Y = Canvas->ClipY * 0.42f; Fuente = FuenteTitulo; }
	else if (Estilo == TEXT("rotulo")) { Color = Tenue; Tam = 22.f; Y = Canvas->ClipY * 0.12f; Fuente = FuenteTitulo; }
	else if (Estilo == TEXT("pharasma")) { Color = Oro; Tam = 30.f; Y = Canvas->ClipY * 0.45f; Fuente = FuenteTitulo; }
	else if (Estilo == TEXT("recuerdo")) { Color = FLinearColor(0.92f, 0.86f, 0.74f); Tam = 28.f; Y = Canvas->ClipY * 0.62f; }
	else if (Estilo == TEXT("sombra")) { Color = Violeta; Tam = 28.f; }
	else if (Estilo == TEXT("pensamiento")) { Color = FLinearColor(0.7f, 0.72f, 0.78f); Tam = 24.f; }
	else if (Estilo == TEXT("voz")) { Color = Hueso; Tam = 26.f; bMarco = true; }
	else { bMarco = true; }  // narracion
	Color.A = Al;

	const TArray<FString> Lineas = Envolver(A.Linea.Texto, Canvas->ClipX * 0.62f, Tam, Fuente);
	const float Alto = Tam * Escala * 1.35f;
	const float Total = Lineas.Num() * Alto;
	if (bMarco)
	{
		if (UTexture2D* M = Tex(TEXT("T_Marco_Narracion")))
		{
			const float W = Canvas->ClipX * 0.7f;
			DrawTexture(M, CX - W * 0.5f, Y - 28.f * Escala, W, Total + 56.f * Escala, 0, 0, 1, 1, FLinearColor(1, 1, 1, Al * 0.85f));
		}
		else
		{
			DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.45f * Al), CX - Canvas->ClipX * 0.34f, Y - 16.f * Escala, Canvas->ClipX * 0.68f, Total + 32.f * Escala);
		}
	}
	for (int32 i = 0; i < Lineas.Num(); ++i)
	{
		Texto(Lineas[i], CX, Y + i * Alto, Color, Tam, true, Fuente);
	}
}

void AVaelithHUD::DibujarAviso()
{
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	const float Resta = GM->AvisoFin - GM->Ahora();
	if (Resta <= 0.f || GM->AvisoTitulo.IsEmpty()) return;
	const float Al = FMath::Clamp(Resta / 0.8f, 0.f, 1.f);
	const float W = 560.f * Escala, X = Canvas->ClipX - W - 40.f * Escala, Y = 40.f * Escala;
	const TArray<FString> Lineas = Envolver(GM->AvisoTexto, W - 40.f * Escala, 18.f, FuenteTexto);
	const float H = (50.f + Lineas.Num() * 24.f) * Escala;
	DrawRect(FLinearColor(0.02f, 0.02f, 0.03f, 0.75f * Al), X, Y, W, H);
	DrawRect(FLinearColor(Oro.R, Oro.G, Oro.B, 0.8f * Al), X, Y, 3.f * Escala, H);
	Texto(GM->AvisoTitulo, X + 20.f * Escala, Y + 10.f * Escala, FLinearColor(Oro.R, Oro.G, Oro.B, Al), 21.f, false, FuenteTitulo);
	for (int32 i = 0; i < Lineas.Num(); ++i)
	{
		Texto(Lineas[i], X + 20.f * Escala, Y + (40.f + i * 24.f) * Escala, FLinearColor(Hueso.R, Hueso.G, Hueso.B, Al), 18.f);
	}
}

void AVaelithHUD::DibujarDotes()
{
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	const float CX = Canvas->ClipX * 0.5f, CY = Canvas->ClipY * 0.5f;
	DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.55f), 0.f, 0.f, Canvas->ClipX, Canvas->ClipY);
	Texto(GM->TextoGuion(TEXT("dote_titulo")), CX, CY - 220.f * Escala, Oro, 36.f, true, FuenteTitulo);
	for (int32 i = 0; i < 2; ++i)
	{
		const float W = 460.f * Escala, H = 220.f * Escala;
		const float X = CX + (i == 0 ? -W - 30.f * Escala : 30.f * Escala), Y = CY - 120.f * Escala;
		DrawRect(FLinearColor(0.03f, 0.03f, 0.05f, 0.85f), X, Y, W, H);
		DrawRect(FLinearColor(Oro.R, Oro.G, Oro.B, 0.6f), X, Y, W, 2.f);
		Texto(FString::Printf(TEXT("[%d]"), i + 1), X + 20.f * Escala, Y + 18.f * Escala, Tenue, 20.f);
		Texto(AVaelithGameMode::NombreDote(GM->OpcionesDote[i]).ToString(), X + W * 0.5f, Y + 20.f * Escala, Oro, 28.f, true, FuenteTitulo);
		const TArray<FString> L = Envolver(AVaelithGameMode::DescripcionDote(GM->OpcionesDote[i]).ToString(), W - 50.f * Escala, 20.f, FuenteTexto);
		for (int32 k = 0; k < L.Num(); ++k) Texto(L[k], X + W * 0.5f, Y + (80.f + k * 28.f) * Escala, Hueso, 20.f, true);
	}
}

void AVaelithHUD::DibujarCreditos()
{
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	TArray<FString> Lineas;
	GM->TextoGuion(TEXT("creditos")).ParseIntoArray(Lineas, TEXT("|"), false);
	const float T = GM->Ahora() - GM->InicioCreditos;
	const float CX = Canvas->ClipX * 0.5f;
	float Y = Canvas->ClipY + 40.f * Escala - T * 42.f * Escala;
	for (const FString& L : Lineas)
	{
		const bool bTitulo = L.StartsWith(TEXT("#"));
		const FString S = bTitulo ? L.RightChop(1) : L;
		if (Y > -60.f && Y < Canvas->ClipY + 40.f)
		{
			Texto(S, CX, Y, bTitulo ? Oro : Hueso, bTitulo ? 30.f : 20.f, true, bTitulo ? FuenteTitulo : FuenteTexto);
		}
		Y += (bTitulo ? 58.f : 32.f) * Escala;
	}
}

void AVaelithHUD::NotifyHitBoxClick(FName BoxName)
{
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (!GM) return;
	if (BoxName == TEXT("iniciar")) GM->MenuIniciar();
	else if (BoxName == TEXT("continuar")) GM->MenuContinuar();
	else if (BoxName == TEXT("salir")) GM->MenuSalir();
	else if (BoxName == TEXT("volver")) GM->Pausar(false);
	else if (BoxName == TEXT("menu")) GM->VolverAlMenu();
}

void AVaelithHUD::NotifyHitBoxBeginCursorOver(FName BoxName) { Sobre = BoxName; }
void AVaelithHUD::NotifyHitBoxEndCursorOver(FName BoxName) { if (Sobre == BoxName) Sobre = NAME_None; }
