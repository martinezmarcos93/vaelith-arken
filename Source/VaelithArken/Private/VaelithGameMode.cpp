#include "VaelithGameMode.h"
#include "VaelithCharacter.h"
#include "VaelithHUD.h"
#include "NoMuerto.h"
#include "Interactuable.h"
#include "Camera/CameraActor.h"
#include "Components/AudioComponent.h"
#include "Dom/JsonObject.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PlayerStart.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "Sound/SoundBase.h"
#include "UnrealClient.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Framework/Application/SlateApplication.h"
#include "Engine/GameViewportClient.h"

#define LOCTEXT_NAMESPACE "Vaelith"

AVaelithPlayerController::AVaelithPlayerController()
{
	bShouldPerformFullTickWhenPaused = true;  // el menú de pausa necesita leer teclas
}

AVaelithGameMode::AVaelithGameMode()
{
	DefaultPawnClass = AVaelithCharacter::StaticClass();
	HUDClass = AVaelithHUD::StaticClass();
	PlayerControllerClass = AVaelithPlayerController::StaticClass();
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bTickEvenWhenPaused = true;
}

float AVaelithGameMode::Ahora() const
{
	return GetWorld() ? GetWorld()->GetRealTimeSeconds() : 0.f;
}

AVaelithCharacter* AVaelithGameMode::Jugador() const
{
	return Cast<AVaelithCharacter>(UGameplayStatics::GetPlayerPawn(this, 0));
}

void AVaelithGameMode::CargarGuion()
{
	const FString Ruta = FPaths::ProjectContentDir() / TEXT("Vaelith/Guion/guion.json");
	FString Texto;
	if (!FFileHelper::LoadFileToString(Texto, *Ruta))
	{
		UE_LOG(LogTemp, Error, TEXT("[vaelith] no se pudo leer el guion: %s"), *Ruta);
		return;
	}
	TSharedPtr<FJsonObject> Raiz;
	if (!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Texto), Raiz) || !Raiz.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[vaelith] guion.json inválido"));
		return;
	}
	if (const TSharedPtr<FJsonObject>* T; Raiz->TryGetObjectField(TEXT("textos"), T))
	{
		for (const auto& Par : (*T)->Values) Textos.Add(FString(Par.Key), Par.Value->AsString());
	}
	if (const TSharedPtr<FJsonObject>* E; Raiz->TryGetObjectField(TEXT("escenas"), E))
	{
		for (const auto& Par : (*E)->Values)
		{
			TArray<FLineaGuion>& Lineas = Guion.Add(FString(Par.Key));
			for (const TSharedPtr<FJsonValue>& V : Par.Value->AsArray())
			{
				const TArray<TSharedPtr<FJsonValue>>& A = V->AsArray();
				if (A.Num() < 2) continue;
				FLineaGuion L;
				L.Estilo = A[0]->AsString();
				L.Texto = A[1]->AsString();
				L.Duracion = A.Num() > 2 ? A[2]->AsNumber() : 2.4f + L.Texto.Len() * 0.055f;
				L.Espera = A.Num() > 3 ? A[3]->AsNumber() : 0.45f;
				Lineas.Add(L);
			}
		}
	}
	const TArray<TSharedPtr<FJsonValue>>* Bloq;
	if (Raiz->TryGetArrayField(TEXT("bloquean"), Bloq))
	{
		for (const TSharedPtr<FJsonValue>& V : *Bloq) EscenasBloqueantes.Add(V->AsString());
	}
	UE_LOG(LogTemp, Log, TEXT("[vaelith] guion: %d escenas, %d textos, %d bloquean"), Guion.Num(), Textos.Num(), EscenasBloqueantes.Num());
}

FString AVaelithGameMode::TextoGuion(const FString& Clave) const
{
	const FString* T = Textos.Find(Clave);
	return T ? *T : FString();
}

void AVaelithGameMode::BeginPlay()
{
	Super::BeginPlay();
	CargarGuion();
	if (APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0))
	{
		PC->SetTickableWhenPaused(true);
	}
	UVaelithGameInstance* GI = Cast<UVaelithGameInstance>(GetGameInstance());
	// Opciones de prueba: -jugar (saltea el menú), -ir=x,y,z[,yaw[,pitch]], -capturas=t1,t2 (segundos).
	static bool bPrimeraVez = true;
	if (GI && bPrimeraVez && FParse::Param(FCommandLine::Get(), TEXT("jugar"))) GI->bArrancarEnMenu = false;
	if (GI && bPrimeraVez && FParse::Param(FCommandLine::Get(), TEXT("continuar"))) { GI->bArrancarEnMenu = false; GI->bContinuar = true; }
	bPrimeraVez = false;
	FString Lista;
	if (FParse::Value(FCommandLine::Get(), TEXT("capturas="), Lista, false))
	{
		TArray<FString> Partes;
		Lista.ParseIntoArray(Partes, TEXT(","));
		for (const FString& P : Partes) Capturas.Add(FCString::Atof(*P));
	}
	if (!GI || GI->bArrancarEnMenu) PrepararMenu();
	else PrepararJuego(GI->bContinuar);
}

void AVaelithGameMode::PrepararMenu()
{
	Modo = EModoJuego::Menu;
	FundidoNegro = 1.f;
	Partida = NewObject<UVaelithPartida>(this);
	APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0);
	for (TActorIterator<ACameraActor> It(GetWorld()); It; ++It)
	{
		if (It->ActorHasTag(TEXT("CamaraMenu")) && PC)
		{
			PC->SetViewTarget(*It);
			break;
		}
	}
	if (PC)
	{
		PC->bShowMouseCursor = true;
		PC->bEnableClickEvents = true;
		PC->bEnableMouseOverEvents = true;
		PC->SetInputMode(FInputModeGameAndUI());
	}
	if (AVaelithCharacter* J = Jugador())
	{
		J->bControlBloqueado = true;
		J->NivelPenumbra = J->PenumbraObjetivo = 0.4f;
	}
	CambiarMusica(TEXT("mus_intro"), 0.55f);
}

void AVaelithGameMode::PrepararJuego(bool bContinuar)
{
	Modo = EModoJuego::Juego;
	FundidoNegro = 1.f;
	AVaelithCharacter* J = Jugador();
	APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0);
	if (PC)
	{
		PC->bShowMouseCursor = false;
		PC->SetInputMode(FInputModeGameOnly());
	}

	UVaelithPartida* Cargada = bContinuar ? Cast<UVaelithPartida>(UGameplayStatics::LoadGameFromSlot(UVaelithGameInstance::Ranura, 0)) : nullptr;
	Partida = Cargada ? Cargada : NewObject<UVaelithPartida>(this);

	if (!J) return;
	J->Dotes = Partida->Dotes;
	J->Ficha->Nivel = Partida->Nivel;
	J->bTieneArmas = Partida->bTieneArmas;
	J->bTieneDaga = Partida->bTieneDaga;
	if (FParse::Param(FCommandLine::Get(), TEXT("armas"))) { J->bTieneArmas = J->bTieneDaga = true; }
	J->AplicarDotes();
	J->Ficha->DescansarEnAltar();

	if (Cargada)
	{
		if (AInteractuable* Altar = BuscarAltar(Partida->Altar))
		{
			const FVector Delante = Altar->GetActorLocation() + Altar->GetActorForwardVector() * 160.f + FVector(0, 0, 100.f);
			J->SetActorLocation(Delante, false, nullptr, ETeleportType::TeleportPhysics);
			if (PC) PC->SetControlRotation(FRotator(0.f, (Altar->GetActorLocation() - Delante).Rotation().Yaw, 0.f));
		}
		CambiarMusica(TEXT("mus_catacumba"), 0.4f);
		ReproducirEscena(TEXT("continuar"), false);
	}
	else
	{
		J->IniciarDespertar();
		ReproducirEscena(TEXT("intro"), true);
		CambiarMusica(TEXT("mus_catacumba"), 0.35f);
	}
	if (USoundBase* Amb = LoadObject<USoundBase>(nullptr, TEXT("/Game/Vaelith/Audio/amb_cueva.amb_cueva")))
	{
		Ambiente = UGameplayStatics::SpawnSound2D(this, Amb, 0.35f, 1.f, 0.f, nullptr, true, false);
	}
}

void AVaelithGameMode::CambiarMusica(const FString& Nombre, float Volumen)
{
	if (Nombre == MusicaActual) return;
	MusicaActual = Nombre;
	if (Musica)
	{
		Musica->FadeOut(2.5f, 0.f);
		Musica = nullptr;
	}
	if (Nombre.IsEmpty()) return;
	if (USoundBase* S = LoadObject<USoundBase>(nullptr, *FString::Printf(TEXT("/Game/Vaelith/Audio/%s.%s"), *Nombre, *Nombre)))
	{
		Musica = UGameplayStatics::SpawnSound2D(this, S, Volumen, 1.f, 0.f, nullptr, true, false);
		if (Musica) Musica->FadeIn(3.f, Volumen);
	}
}

AInteractuable* AVaelithGameMode::BuscarAltar(FName Id) const
{
	AInteractuable* Primero = nullptr;
	for (TActorIterator<AInteractuable> It(GetWorld()); It; ++It)
	{
		if (It->Tipo != ETipoInteractuable::Altar) continue;
		if (It->Id == Id) return *It;
		if (!Primero) Primero = *It;
	}
	return Id.IsNone() ? nullptr : Primero;
}

// ---------------------------------------------------------------- guion

void AVaelithGameMode::ReproducirEscena(const FString& Clave, bool bUnaVez)
{
	const FName Hecho(*(TEXT("escena_") + Clave));
	if (bUnaVez && Partida && Partida->Hechos.Contains(Hecho)) return;
	const TArray<FLineaGuion>* Lineas = Guion.Find(Clave);
	if (!Lineas)
	{
		UE_LOG(LogTemp, Warning, TEXT("[vaelith] escena inexistente: %s"), *Clave);
		return;
	}
	if (bUnaVez && Partida) Partida->Hechos.AddUnique(Hecho);
	const bool bBloquea = EscenasBloqueantes.Contains(Clave);
	for (FLineaGuion L : *Lineas)
	{
		L.bBloquea = bBloquea;
		Cola.Add(L);
	}
}

void AVaelithGameMode::Aviso(const FString& Titulo, const FString& Texto, float Duracion)
{
	AvisoTitulo = Titulo;
	AvisoTexto = Texto;
	AvisoFin = Ahora() + Duracion;
}

bool AVaelithGameMode::HechoOcurrido(FName H) const
{
	return Partida && Partida->Hechos.Contains(H);
}

void AVaelithGameMode::RegistrarHecho(FName H)
{
	if (Partida && !H.IsNone()) Partida->Hechos.AddUnique(H);
}

void AVaelithGameMode::SumarGracia(int32 N, const FString& Motivo)
{
	if (!Partida) return;
	Partida->Gracia += N;
	Aviso(N > 0 ? TEXT("Gracia") : TEXT("Deuda"), Motivo, 4.f);
}

void AVaelithGameMode::Guardar(FName Altar)
{
	AVaelithCharacter* J = Jugador();
	if (!Partida || !J) return;
	Partida->Altar = Altar;
	Partida->Nivel = J->Ficha->Nivel;
	Partida->Dotes = J->Dotes;
	Partida->bTieneArmas = J->bTieneArmas;
	Partida->bTieneDaga = J->bTieneDaga;
	Partida->Fecha = FDateTime::Now();
	UGameplayStatics::SaveGameToSlot(Partida, UVaelithGameInstance::Ranura, 0);
	if (J->Penitencia > 0) J->Penitencia = FMath::Max(0, J->Penitencia - 1);  // rezar alivia la penitencia
}

// ---------------------------------------------------------------- recuerdos

void AVaelithGameMode::ActivarRecuerdo(int32 Fragmento)
{
	AVaelithCharacter* J = Jugador();
	if (!J) return;
	RecuerdoEnCurso = Fragmento;
	J->bControlBloqueado = true;
	if (Partida) Partida->Recuerdos.AddUnique(Fragmento);
	if (USoundBase* S = LoadObject<USoundBase>(nullptr, TEXT("/Game/Vaelith/Audio/sfx_recuerdo.sfx_recuerdo"))) UGameplayStatics::PlaySound2D(this, S);
	ReproducirEscena(FString::Printf(TEXT("recuerdo_%d"), Fragmento), true);
}

FText AVaelithGameMode::NombreDote(EDote D)
{
	switch (D)
	{
	case EDote::EscudoVeloz: return LOCTEXT("DoteEV", "Escudo veloz");
	case EDote::GolpeVital: return LOCTEXT("DoteGV", "Golpe vital");
	case EDote::FocoExtra: return LOCTEXT("DoteFE", "Devoción");
	case EDote::AuraPharasma: return LOCTEXT("DoteAP", "Aura de Pharasma");
	case EDote::RetribucionMayor: return LOCTEXT("DoteRM", "Retribución mayor");
	case EDote::MuroEscudo: return LOCTEXT("DoteMU", "Muro de escudo");
	default: return FText::GetEmpty();
	}
}

FText AVaelithGameMode::DescripcionDote(EDote D)
{
	switch (D)
	{
	case EDote::EscudoVeloz: return LOCTEXT("DoteEVd", "Levantar el escudo no cuesta acciones.");
	case EDote::GolpeVital: return LOCTEXT("DoteGVd", "Tus tajos suman 1d6 de daño vital contra no-muertos.");
	case EDote::FocoExtra: return LOCTEXT("DoteFEd", "Un punto de foco más para Imponer las Manos.");
	case EDote::AuraPharasma: return LOCTEXT("DoteAPd", "Los espíritus que se acercan a menos de cuatro metros arden en luz.");
	case EDote::RetribucionMayor: return LOCTEXT("DoteRMd", "El bloqueo perfecto devuelve el doble de daño y aturde dos segundos.");
	case EDote::MuroEscudo: return LOCTEXT("DoteMUd", "La dureza de tu escudo sube de 5 a 7.");
	default: return FText::GetEmpty();
	}
}

void AVaelithGameMode::ElegirDote(int32 Opcion)
{
	AVaelithCharacter* J = Jugador();
	if (!J || Modo != EModoJuego::EligiendoDote) return;
	const EDote D = OpcionesDote[FMath::Clamp(Opcion, 0, 1)];
	J->Dotes.AddUnique(D);
	J->Ficha->Nivel = FMath::Min(J->Ficha->Nivel + 1, 4);
	J->AplicarDotes();
	J->Ficha->Curar(99);
	J->Ficha->Foco = J->Ficha->FocoMax();
	if (Partida) { Partida->Nivel = J->Ficha->Nivel; Partida->Dotes = J->Dotes; }
	Modo = EModoJuego::Juego;
	J->bControlBloqueado = false;
	Aviso(FString::Printf(TEXT("Nivel %d"), J->Ficha->Nivel), NombreDote(D).ToString() + TEXT(": ") + DescripcionDote(D).ToString(), 6.f);
}

// ---------------------------------------------------------------- muerte

void AVaelithGameMode::JugadorMurio()
{
	if (Modo == EModoJuego::Muerte) return;
	Modo = EModoJuego::Muerte;
	TiempoMuerte = 0.f;
	UGameplayStatics::SetGlobalTimeDilation(this, 0.35f);
	Cola.Reset();
	Activa = FLineaActiva();
	ReproducirEscena(FString::Printf(TEXT("muerte_%d"), FMath::RandRange(1, 3)), false);
}

void AVaelithGameMode::Respawnear()
{
	AVaelithCharacter* J = Jugador();
	if (!J) return;
	UGameplayStatics::SetGlobalTimeDilation(this, 1.f);
	J->Penitencia = FMath::Min(J->Penitencia + 1, 3);
	J->Ficha->DescansarEnAltar();
	APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0);
	FVector Destino = J->GetActorLocation();
	if (AInteractuable* Altar = BuscarAltar(Partida ? Partida->Altar : NAME_None))
	{
		Destino = Altar->GetActorLocation() + Altar->GetActorForwardVector() * 160.f + FVector(0, 0, 100.f);
		if (PC) PC->SetControlRotation(FRotator(0.f, (Altar->GetActorLocation() - Destino).Rotation().Yaw, 0.f));
	}
	else if (AActor* Inicio = FindPlayerStart(PC))
	{
		Destino = Inicio->GetActorLocation();
	}
	J->SetActorLocation(Destino, false, nullptr, ETeleportType::TeleportPhysics);
	Modo = EModoJuego::Juego;
	Aviso(TEXT("Penitencia"), TextoGuion(FString::Printf(TEXT("penitencia_%d"), J->Penitencia)), 6.f);
}

// ---------------------------------------------------------------- zonas, jefe, final

void AVaelithGameMode::EntrarZona(float Penumbra, const FString& NuevaMusica)
{
	if (AVaelithCharacter* J = Jugador())
	{
		if (Penumbra >= 0.f) J->PenumbraObjetivo = Penumbra;  // se suaviza en el personaje
	}
	if (!NuevaMusica.IsEmpty()) CambiarMusica(NuevaMusica, 0.4f);
}

void AVaelithGameMode::IniciarJefe()
{
	for (TActorIterator<ANoMuerto> It(GetWorld()); It; ++It)
	{
		if (It->Tipo == ETipoNoMuerto::Sombra && It->EstaVivo())
		{
			Jefe = *It;
			Jefe->Despertar();
			ReproducirEscena(TEXT("sombra_aparece"), true);
			CambiarMusica(TEXT("mus_jefe"), 0.55f);
			return;
		}
	}
}

void AVaelithGameMode::JefeDerrotado(ANoMuerto* Sombra)
{
	RegistrarHecho(TEXT("sombra"));
	CambiarMusica(TEXT(""));
	TiempoFinal = 0.f;
	Cola.Reset();
	Activa = FLineaActiva();
	const int32 Gracia = Partida ? Partida->Gracia : 0;
	ReproducirEscena(Gracia >= 3 ? TEXT("final_gracia") : (Gracia <= -1 ? TEXT("final_deuda") : TEXT("final_neutro")), true);
	ReproducirEscena(TEXT("final"), true);
	if (AVaelithCharacter* J = Jugador()) J->bControlBloqueado = true;
	if (Partida) UGameplayStatics::SaveGameToSlot(Partida, UVaelithGameInstance::Ranura, 0);
}

// ---------------------------------------------------------------- menú

void AVaelithGameMode::MenuIniciar()
{
	if (UVaelithGameInstance* GI = Cast<UVaelithGameInstance>(GetGameInstance()))
	{
		GI->bArrancarEnMenu = false;
		GI->bContinuar = false;
	}
	UGameplayStatics::OpenLevel(this, FName(*UGameplayStatics::GetCurrentLevelName(this)));
}

void AVaelithGameMode::MenuContinuar()
{
	if (UVaelithGameInstance* GI = Cast<UVaelithGameInstance>(GetGameInstance()))
	{
		GI->bArrancarEnMenu = false;
		GI->bContinuar = true;
	}
	UGameplayStatics::SetGamePaused(this, false);
	UGameplayStatics::OpenLevel(this, FName(*UGameplayStatics::GetCurrentLevelName(this)));
}

void AVaelithGameMode::MenuSalir()
{
	UKismetSystemLibrary::QuitGame(this, UGameplayStatics::GetPlayerController(this, 0), EQuitPreference::Quit, false);
}

bool AVaelithGameMode::TeclaNueva(APlayerController* PC, const FKey& K)
{
	if (!PC || !PC->WasInputKeyJustPressed(K)) return false;
	const double Ahora = FPlatformTime::Seconds();
	double& Ultima = TeclasConsumidas.FindOrAdd(K, -1.0);
	if (Ahora - Ultima < 0.15) return false;
	Ultima = Ahora;
	return true;
}

void AVaelithGameMode::Pausar(bool bPausa)
{
	if (Modo != EModoJuego::Juego && Modo != EModoJuego::Pausa) return;
	Modo = bPausa ? EModoJuego::Pausa : EModoJuego::Juego;
	UGameplayStatics::SetGamePaused(this, bPausa);
	if (APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0))
	{
		PC->bShowMouseCursor = bPausa;
		PC->bEnableClickEvents = bPausa;
		PC->bEnableMouseOverEvents = bPausa;
		if (bPausa)
		{
			// Soltar el ratón: en juego el viewport lo captura (modo relativo de SDL) y,
			// aunque bShowMouseCursor sea true, el cursor sigue oculto hasta liberar la captura.
			FInputModeGameAndUI M;
			M.SetHideCursorDuringCapture(false);
			M.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
			PC->SetInputMode(M);
			if (UGameViewportClient* VC = GetWorld()->GetGameViewport())
			{
				VC->SetMouseCaptureMode(EMouseCaptureMode::NoCapture);
				if (VC->Viewport) { VC->Viewport->CaptureMouse(false); VC->Viewport->ShowCursor(true); }
			}
			FSlateApplication::Get().ReleaseAllPointerCapture();
			int32 SX = 0, SY = 0;
			PC->GetViewportSize(SX, SY);
			PC->SetMouseLocation(SX / 2, FMath::RoundToInt(SY * 0.62f)); // sobre "Continuar"
		}
		else PC->SetInputMode(FInputModeGameOnly());
	}
}

void AVaelithGameMode::VolverAlMenu()
{
	if (UVaelithGameInstance* GI = Cast<UVaelithGameInstance>(GetGameInstance())) GI->bArrancarEnMenu = true;
	UGameplayStatics::SetGamePaused(this, false);
	UGameplayStatics::SetGlobalTimeDilation(this, 1.f);
	UGameplayStatics::OpenLevel(this, FName(*UGameplayStatics::GetCurrentLevelName(this)));
}

// ---------------------------------------------------------------- tick

void AVaelithGameMode::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	const float Dt = FApp::GetDeltaTime();  // tiempo real: no lo afecta el hitstop ni la pausa
	const float T = Ahora();
	AVaelithCharacter* J = Jugador();
	APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0);

	// Prueba: diagnóstico de visibilidad cerca de la torre
	if (!bDiagHecho && T > 3.f && FParse::Param(FCommandLine::Get(), TEXT("diag")))
	{
		bDiagHecho = true;
		int32 N = 0, Ocultos = 0, SinMalla = 0;
		for (TActorIterator<AActor> It(GetWorld()); It; ++It)
		{
			if (FVector::Dist2D(It->GetActorLocation(), FVector(6400.f, 27000.f, 0.f)) > 1200.f) continue;
			++N;
			if (It->IsHidden()) ++Ocultos;
			TArray<UStaticMeshComponent*> C;
			It->GetComponents(C);
			for (UStaticMeshComponent* S : C)
			{
				if (!S->GetStaticMesh()) ++SinMalla;
				if (N <= 4) UE_LOG(LogTemp, Log, TEXT("[vaelith] diag %s malla=%s visible=%d escala=%s"), *It->GetName(), S->GetStaticMesh() ? *S->GetStaticMesh()->GetName() : TEXT("-"), S->IsVisible(), *S->GetComponentScale().ToString());
			}
		}
		UE_LOG(LogTemp, Log, TEXT("[vaelith] diag torre: %d actores, %d ocultos, %d sin malla"), N, Ocultos, SinMalla);
	}
	// Prueba: dispara un flujo sin teclado (-probar=recuerdo1..4|jefe|final|muerte)
	FString Probar;
	if (!bProbado && T > 3.f && FParse::Value(FCommandLine::Get(), TEXT("probar="), Probar, false))
	{
		bProbado = true;
		if (J) J->TiempoDespertarCancelar();
		Cola.Reset();
		Activa = FLineaActiva();
		if (Probar.StartsWith(TEXT("recuerdo"))) ActivarRecuerdo(FCString::Atoi(*Probar.RightChop(8)));
		else if (Probar == TEXT("jefe")) IniciarJefe();
		else if (Probar == TEXT("final")) JefeDerrotado(nullptr);
		else if (Probar == TEXT("muerte")) JugadorMurio();
	}
	// Prueba: teclas reales inyectadas por Slate, mismo camino que el teclado (-teclas=Escape@20,E@22; segundos de juego).
	FString Teclas;
	if (FParse::Value(FCommandLine::Get(), TEXT("teclas="), Teclas, false) && FSlateApplication::IsInitialized())
	{
		TArray<FString> Lista;
		Teclas.ParseIntoArray(Lista, TEXT(","));
		FString Nombre, Cuando;
		if (Lista.IsValidIndex(TeclasPrueba) && Lista[TeclasPrueba].Split(TEXT("@"), &Nombre, &Cuando) && T >= FCString::Atof(*Cuando))
		{
			const FKey K(*Nombre);
			FSlateApplication::Get().ProcessKeyDownEvent(FKeyEvent(K, FModifierKeysState(), 0, false, 0, 0));
			FSlateApplication::Get().ProcessKeyUpEvent(FKeyEvent(K, FModifierKeysState(), 0, false, 0, 0));
			UE_LOG(LogTemp, Log, TEXT("[vaelith] tecla %s inyectada (modo=%d)"), *Nombre, int32(Modo));
			++TeclasPrueba;
		}
	}
	// Prueba: usa interactuables por Id, uno por segundo (-usar=armas,puerta_1,...)
	FString Usar;
	if (J && T > 3.f + UsadosPrueba && FParse::Value(FCommandLine::Get(), TEXT("usar="), Usar, false))
	{
		TArray<FString> Ids;
		Usar.ParseIntoArray(Ids, TEXT(","));
		if (Ids.IsValidIndex(UsadosPrueba))
		{
			const FName Id(*Ids[UsadosPrueba]);
			bool bEncontrado = false;
			for (TActorIterator<AInteractuable> It(GetWorld()); It; ++It)
			{
				if (It->Id != Id) continue;
				bEncontrado = true;
				It->Usar(J);
				UE_LOG(LogTemp, Log, TEXT("[vaelith] usar %s -> usado=%d hecho=%d armas=%d daga=%d"), *Id.ToString(), It->bUsado, HechoOcurrido(Id), J->bTieneArmas, J->bTieneDaga);
			}
			if (!bEncontrado) UE_LOG(LogTemp, Warning, TEXT("[vaelith] usar %s: no existe"), *Id.ToString());
			++UsadosPrueba;
		}
	}
	// Prueba: teletransporte y capturas programadas
	if (Capturas.Num() > 0 && FMath::FloorToInt(T / 3.f) != FMath::FloorToInt((T - Dt) / 3.f))
	{
		UE_LOG(LogTemp, Log, TEXT("[vaelith] reloj T=%.1f modo=%d capturas=%d despertar=%d bloqueado=%d pg=%d mira='%s'"), T, int32(Modo), Capturas.Num(), J ? int32(J->EnDespertar()) : -1, J ? int32(J->bControlBloqueado) : -1, J ? J->Ficha->PG : -1, J ? *J->TextoInteraccion : TEXT(""));
	}
	FString Ir;
	if (!bTeletransportado && J && T > 1.f && FParse::Value(FCommandLine::Get(), TEXT("ir="), Ir, false))
	{
		TArray<FString> P;
		Ir.ParseIntoArray(P, TEXT(","));
		if (J->EnDespertar())
		{
			// Primero se corta el despertar; se teletransporta en un cuadro posterior, cuando ya no pisa la mira.
			J->TiempoDespertarCancelar();
		}
		else if (P.Num() >= 3)
		{
			J->SetActorLocation(FVector(FCString::Atof(*P[0]), FCString::Atof(*P[1]), FCString::Atof(*P[2])), false, nullptr, ETeleportType::TeleportPhysics);
			if (P.Num() >= 4 && PC) PC->SetControlRotation(FRotator(P.Num() >= 5 ? FCString::Atof(*P[4]) : 0.f, FCString::Atof(*P[3]), 0.f));
			bTeletransportado = true;
		}
		else
		{
			bTeletransportado = true;
		}
	}
	for (int32 i = Capturas.Num() - 1; i >= 0; --i)
	{
		if (T >= Capturas[i])
		{
			const FString Archivo = FPaths::ProjectSavedDir() / FString::Printf(TEXT("Capturas/cap_%03d.png"), FMath::RoundToInt(Capturas[i]));
			FScreenshotRequest::RequestScreenshot(Archivo, false, false);
			UE_LOG(LogTemp, Log, TEXT("[vaelith] captura %s"), *Archivo);
			Capturas.RemoveAt(i);
		}
	}

	// Líneas del guion
	if (Activa.Linea.Texto.Len() > 0 && T - Activa.Inicio > Activa.Linea.Duracion)
	{
		Activa = FLineaActiva();
		EsperaLinea = Cola.Num() > 0 ? Cola[0].Espera : 0.f;
	}
	if (Activa.Linea.Texto.IsEmpty() && Cola.Num() > 0)
	{
		EsperaLinea -= Dt;
		if (EsperaLinea <= 0.f)
		{
			Activa.Linea = Cola[0];
			Activa.Inicio = T;
			Cola.RemoveAt(0);
			UE_LOG(LogTemp, Log, TEXT("[vaelith] linea T=%.1f: %s"), T, *Activa.Linea.Texto.Left(50));
		}
	}

	// Fundido de entrada (salvo que lo maneje una cinemática)
	const bool bCinematica = J && J->EnDespertar();
	if (!bCinematica && Modo != EModoJuego::Muerte && TiempoFinal < 0.f)
	{
		FundidoNegro = FMath::FInterpConstantTo(FundidoNegro, 0.f, Dt, 0.4f);
	}

	if (PC && TeclaNueva(PC, EKeys::Escape))
	{
		if (Modo == EModoJuego::Juego) Pausar(true);
		else if (Modo == EModoJuego::Pausa) Pausar(false);
		else if (Modo == EModoJuego::Creditos) VolverAlMenu();
	}
	// E (o Enter) adelanta la línea en pantalla. Mientras hay una línea, la E es del texto: el personaje
	// no la usa para interactuar (ver AVaelithCharacter::LeerControles). No en la muerte.
	if (PC && Modo == EModoJuego::Juego && HayEscenaEnCurso() && (TeclaNueva(PC, EKeys::E) || TeclaNueva(PC, EKeys::Enter)))
	{
		if (Activa.Linea.Texto.Len() > 0) Activa.Inicio = T - Activa.Linea.Duracion;
		else EsperaLinea = 0.f;  // entre dos líneas: la siguiente aparece ya
		UE_LOG(LogTemp, Log, TEXT("[vaelith] linea adelantada T=%.1f"), T);
	}

	// Escenas de interacción: bloquean mientras SUS líneas están en pantalla (o a punto de salir), no al encolarse.
	if (J && Modo == EModoJuego::Juego)
	{
		const bool bLineaBloquea = (Activa.Linea.Texto.Len() > 0 && Activa.Linea.bBloquea)
			|| (Activa.Linea.Texto.IsEmpty() && Cola.Num() > 0 && Cola[0].bBloquea);
		if (bLineaBloquea && !bBloqueoPorEscena && !J->bControlBloqueado)
		{
			bBloqueoPorEscena = true;  // solo se libera lo que se bloqueó acá
			J->bControlBloqueado = true;
		}
		else if (!bLineaBloquea && bBloqueoPorEscena && RecuerdoEnCurso == 0)
		{
			bBloqueoPorEscena = false;
			J->bControlBloqueado = false;
		}
	}
	if (J)
	{
		// Recuerdos: la pantalla se lava mientras dura la escena.
		const bool bEnRecuerdo = RecuerdoEnCurso > 0 && Modo == EModoJuego::Juego;
		J->Desaturacion = FMath::FInterpTo(J->Desaturacion, bEnRecuerdo ? 1.f : 0.f, Dt, 1.5f);
		if (bEnRecuerdo && !HayEscenaEnCurso())
		{
			const int32 N = RecuerdoEnCurso;
			RecuerdoEnCurso = 0;
			if (N >= 1 && N <= 3)
			{
				static const EDote Opciones[3][2] = {
					{ EDote::EscudoVeloz, EDote::GolpeVital },
					{ EDote::FocoExtra, EDote::AuraPharasma },
					{ EDote::RetribucionMayor, EDote::MuroEscudo } };
				OpcionesDote[0] = Opciones[N - 1][0];
				OpcionesDote[1] = Opciones[N - 1][1];
				Modo = EModoJuego::EligiendoDote;
			}
			else
			{
				J->bControlBloqueado = false;
				if (N == 4) IniciarJefe();
			}
		}
		if (Modo == EModoJuego::EligiendoDote && PC)
		{
			if (TeclaNueva(PC, EKeys::One)) ElegirDote(0);
			else if (TeclaNueva(PC, EKeys::Two)) ElegirDote(1);
		}
	}

	// Secuencia de muerte
	if (Modo == EModoJuego::Muerte)
	{
		TiempoMuerte += Dt;
		if (TiempoMuerte > 3.5f) FundidoNegro = FMath::FInterpConstantTo(FundidoNegro, 1.f, Dt, 0.8f);
		if (TiempoMuerte > 6.5f && !HayEscenaEnCurso()) Respawnear();
	}

	// Final
	if (TiempoFinal >= 0.f && Modo != EModoJuego::Creditos)
	{
		TiempoFinal += Dt;
		if (!HayEscenaEnCurso() && TiempoFinal > 3.f)
		{
			FundidoBlanco = FMath::FInterpConstantTo(FundidoBlanco, 1.f, Dt, 0.25f);
			if (FundidoBlanco >= 1.f)
			{
				Modo = EModoJuego::Creditos;
				InicioCreditos = T;
				CambiarMusica(TEXT("mus_intro"), 0.5f);
			}
		}
	}
	if (Modo == EModoJuego::Creditos)
	{
		FundidoBlanco = FMath::FInterpConstantTo(FundidoBlanco, 0.f, Dt, 0.5f);
		FundidoNegro = 1.f;
		if (T - InicioCreditos > 75.f) VolverAlMenu();
	}
}

#undef LOCTEXT_NAMESPACE
