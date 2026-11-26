#include "VaelithCharacter.h"
#include "VaelithGameMode.h"
#include "NoMuerto.h"
#include "Planilla.h"
#include "Interactuable.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "Engine/StaticMesh.h"
#include "EngineUtils.h"

namespace
{
	// Pose de un pivote: desplazamiento (cm, espacio de cámara) y rotación (grados).
	struct FPose
	{
		FVector Pos = FVector::ZeroVector;
		FRotator Rot = FRotator::ZeroRotator;
	};

	FPose Mezcla(const FPose& A, const FPose& B, float T)
	{
		const float S = FMath::SmoothStep(0.f, 1.f, FMath::Clamp(T, 0.f, 1.f));
		return { FMath::Lerp(A.Pos, B.Pos, S), FRotator(FMath::Lerp(A.Rot.Pitch, B.Rot.Pitch, S), FMath::Lerp(A.Rot.Yaw, B.Rot.Yaw, S), FMath::Lerp(A.Rot.Roll, B.Rot.Roll, S)) };
	}

	struct FClave
	{
		float Key;
		FPose Value;
	};

	// Evalúa una secuencia de claves (tiempo normalizado 0..1).
	FPose Curva(std::initializer_list<FClave> Lista, float T)
	{
		const TArray<FClave> Claves(Lista);
		if (Claves.Num() == 0) return {};
		if (T <= Claves[0].Key) return Claves[0].Value;
		for (int32 i = 1; i < Claves.Num(); ++i)
		{
			if (T <= Claves[i].Key)
			{
				const float A = Claves[i - 1].Key, B = Claves[i].Key;
				return Mezcla(Claves[i - 1].Value, Claves[i].Value, (T - A) / FMath::Max(B - A, KINDA_SMALL_NUMBER));
			}
		}
		return Claves.Last().Value;
	}

	const FVector BaseDerecha(42.f, 20.f, -20.f);
	const FVector BaseIzquierda(44.f, -24.f, -24.f);

	UStaticMesh* Malla(const TCHAR* Ruta, const TCHAR* Respaldo)
	{
		if (UStaticMesh* M = LoadObject<UStaticMesh>(nullptr, Ruta)) return M;
		return LoadObject<UStaticMesh>(nullptr, Respaldo);
	}
}

AVaelithCharacter::AVaelithCharacter()
{
	PrimaryActorTick.bCanEverTick = true;
	GetCapsuleComponent()->InitCapsuleSize(38.f, 92.f);

	Camara = CreateDefaultSubobject<UCameraComponent>(TEXT("Camara"));
	Camara->SetupAttachment(GetCapsuleComponent());
	Camara->SetRelativeLocation(FVector(0.f, 0.f, 70.f));
	Camara->bUsePawnControlRotation = true;
	Camara->SetFieldOfView(86.f);

	PivoteDerecho = CreateDefaultSubobject<USceneComponent>(TEXT("PivoteDerecho"));
	PivoteDerecho->SetupAttachment(Camara);
	PivoteIzquierdo = CreateDefaultSubobject<USceneComponent>(TEXT("PivoteIzquierdo"));
	PivoteIzquierdo->SetupAttachment(Camara);

	auto CrearArma = [this](const TCHAR* Nombre, USceneComponent* Padre)
	{
		UStaticMeshComponent* C = CreateDefaultSubobject<UStaticMeshComponent>(Nombre);
		C->SetupAttachment(Padre);
		C->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		C->SetCastShadow(false);
		C->bOnlyOwnerSee = true;
		return C;
	};
	Espada = CrearArma(TEXT("Espada"), PivoteDerecho);
	Daga = CrearArma(TEXT("Daga"), PivoteDerecho);
	Escudo = CrearArma(TEXT("Escudo"), PivoteIzquierdo);
	// La hoja (+Z del modelo) apunta hacia adelante y arriba.
	Espada->SetRelativeRotation(FRotator(-55.f, 8.f, 0.f));
	Daga->SetRelativeRotation(FRotator(-70.f, 0.f, 0.f));
	// La cara del escudo (+Y del modelo) mira hacia adelante.
	Escudo->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));
	Espada->SetRelativeScale3D(FVector(0.55f));
	Daga->SetRelativeScale3D(FVector(0.6f));
	Escudo->SetRelativeScale3D(FVector(0.42f));

	Penumbra = CreateDefaultSubobject<UPointLightComponent>(TEXT("Penumbra"));
	Penumbra->SetupAttachment(Camara);
	Penumbra->SetRelativeLocation(FVector(160.f, 0.f, 90.f));  // lejos de las armas para no quemarlas
	Penumbra->SetCastShadows(false);
	Penumbra->SetIntensityUnits(ELightUnits::Unitless);
	Penumbra->SetAttenuationRadius(1100.f);
	Penumbra->SetLightColor(FLinearColor(0.62f, 0.72f, 0.95f));
	Penumbra->SetIntensity(0.f);

	Ficha = CreateDefaultSubobject<UFichaComponent>(TEXT("Ficha"));

	UCharacterMovementComponent* Mov = GetCharacterMovement();
	Mov->MaxWalkSpeed = 330.f;  // armadura pesada: no es un velocista
	Mov->BrakingDecelerationWalking = 1600.f;
	Mov->JumpZVelocity = 380.f;
	Mov->AirControl = 0.1f;
	Mov->NavAgentProps.bCanCrouch = true;
	bUseControllerRotationYaw = true;
}

void AVaelithCharacter::BeginPlay()
{
	Super::BeginPlay();
	Espada->SetStaticMesh(Malla(TEXT("/Game/Vaelith/Armas/SM_Espada_Larga.SM_Espada_Larga"), TEXT("/Engine/BasicShapes/Cylinder.Cylinder")));
	Daga->SetStaticMesh(Malla(TEXT("/Game/Vaelith/Armas/SM_Daga_Pharasma.SM_Daga_Pharasma"), TEXT("/Engine/BasicShapes/Cylinder.Cylinder")));
	Escudo->SetStaticMesh(Malla(TEXT("/Game/Vaelith/Armas/SM_Escudo_Pharasma.SM_Escudo_Pharasma"), TEXT("/Engine/BasicShapes/Cube.Cube")));
	if (!LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Vaelith/Armas/SM_Espada_Larga.SM_Espada_Larga")))
	{
		Espada->SetRelativeScale3D(FVector(0.04f, 0.04f, 0.9f));
		Daga->SetRelativeScale3D(FVector(0.03f, 0.03f, 0.35f));
		Escudo->SetRelativeScale3D(FVector(0.65f, 0.06f, 0.85f));
	}
	AplicarDotes();
	Ficha->AlSalvarseDeMorir.AddLambda([this]()
	{
		if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>())
		{
			GM->ReproducirEscena(TEXT("salvado"), false);
			GM->Aviso(TEXT("Favor de Pharasma"), TEXT("Gastaste todo tu favor. Ella te devolvió una vez más."), 5.f);
		}
		Reproducir(TEXT("sfx_respiracion"), 1.f, 0.8f);
	});
}

void AVaelithCharacter::AplicarDotes()
{
	Ficha->DurezaEscudo = TieneDote(EDote::MuroEscudo) ? 7 : 5;
	Ficha->FocoAdicional = TieneDote(EDote::FocoExtra) ? 1 : 0;
}

void AVaelithCharacter::Reproducir(const TCHAR* Ruta, float Volumen, float Tono)
{
	const FString Clave(Ruta);
	USoundBase* S = nullptr;
	if (USoundBase** Encontrado = CacheSonidos.Find(Clave))
	{
		S = *Encontrado;
	}
	else
	{
		S = LoadObject<USoundBase>(nullptr, *FString::Printf(TEXT("/Game/Vaelith/Audio/%s.%s"), Ruta, Ruta));
		CacheSonidos.Add(Clave, S);
	}
	if (S)
	{
		UGameplayStatics::PlaySound2D(this, S, Volumen, Tono * FMath::FRandRange(0.94f, 1.06f));
	}
}

void AVaelithCharacter::Sacudir(float Fuerza)
{
	TemblorPantalla = FMath::Max(TemblorPantalla, Fuerza);
}

void AVaelithCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();

	if (Hitstop > 0.f)
	{
		Hitstop -= FApp::GetDeltaTime();
		if (Hitstop <= 0.f) UGameplayStatics::SetGlobalTimeDilation(this, 1.f);
	}

	if (EnDespertar())
	{
		ActualizarDespertar(DeltaTime);
	}
	else if (!bControlBloqueado && (!GM || GM->Modo == EModoJuego::Juego))
	{
		LeerControles(DeltaTime);
	}

	if (TratandoHasta > 0.f && GetWorld()->GetTimeSeconds() >= TratandoHasta)
	{
		TratandoHasta = -1.f;
		bControlBloqueado = false;
	}
	NivelPenumbra = FMath::FInterpTo(NivelPenumbra, PenumbraObjetivo, DeltaTime, 0.7f);
	ActualizarAccion(DeltaTime);
	AnimarArmas(DeltaTime);
	ActualizarPostProceso(DeltaTime);
	BuscarInteractuable();

	// Aura de Pharasma: los fantasmas cercanos sufren.
	if (TieneDote(EDote::AuraPharasma))
	{
		CadenciaAura += DeltaTime;
		if (CadenciaAura >= 1.f)
		{
			CadenciaAura = 0.f;
			TArray<AActor*> Todos;
			UGameplayStatics::GetAllActorsOfClass(this, ANoMuerto::StaticClass(), Todos);
			for (AActor* A : Todos)
			{
				ANoMuerto* N = Cast<ANoMuerto>(A);
				if (N && N->EstaVivo() && N->Tipo == ETipoNoMuerto::Fantasma && FVector::Dist(N->GetActorLocation(), GetActorLocation()) < 450.f)
				{
					N->RecibirAtaque(2, ETipoDanio::Vital, true, 0.f, FVector::ZeroVector);
				}
			}
		}
	}
}

void AVaelithCharacter::LeerControles(float Dt)
{
	APlayerController* PC = Cast<APlayerController>(GetController());
	if (!PC) return;

	// Mirar
	float MX = 0.f, MY = 0.f;
	PC->GetInputMouseDelta(MX, MY);
	const float Sens = (Accion == EAccionArma::Ninguna ? 1.f : 0.7f) * (Ficha->bBloqueando ? 0.75f : 1.f);
	AddControllerYawInput(MX * 0.6f * Sens);
	AddControllerPitchInput(-MY * 0.6f * Sens);

	if (Ficha->bMoribundo)
	{
		// Diehard: un último esfuerzo para levantarse.
		if (PC->WasInputKeyJustPressed(EKeys::LeftMouseButton) || PC->WasInputKeyJustPressed(EKeys::R))
		{
			if (Ficha->Levantarse())
			{
				Reproducir(TEXT("sfx_respiracion"), 1.f, 0.9f);
				Sacudir(0.6f);
				if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->ReproducirEscena(TEXT("diehard"), false);
			}
		}
		return;
	}

	// Moverse
	FVector2D Mov(0.f, 0.f);
	if (PC->IsInputKeyDown(EKeys::W)) Mov.X += 1.f;
	if (PC->IsInputKeyDown(EKeys::S)) Mov.X -= 1.f;
	if (PC->IsInputKeyDown(EKeys::D)) Mov.Y += 1.f;
	if (PC->IsInputKeyDown(EKeys::A)) Mov.Y -= 1.f;
	const FRotator Yaw(0.f, GetControlRotation().Yaw, 0.f);
	AddMovementInput(FRotationMatrix(Yaw).GetUnitAxis(EAxis::X), Mov.X);
	AddMovementInput(FRotationMatrix(Yaw).GetUnitAxis(EAxis::Y), Mov.Y);

	const bool bCorre = PC->IsInputKeyDown(EKeys::LeftShift) && Mov.X > 0.f && !Ficha->bBloqueando && Ficha->Acciones > 0;
	float Velocidad = bCorre ? 520.f : 330.f;
	if (Ficha->bBloqueando) Velocidad = 180.f;
	if (Accion == EAccionArma::TajoPotente || Accion == EAccionArma::Cargando) Velocidad = 200.f;
	GetCharacterMovement()->MaxWalkSpeed = Velocidad;

	if (PC->WasInputKeyJustPressed(EKeys::SpaceBar) && Ficha->GastarAcciones(1)) Jump();

	// Bloqueo (clic derecho mantenido)
	const bool bPideBloqueo = PC->IsInputKeyDown(EKeys::RightMouseButton);
	if (bPideBloqueo && !bBloqueoPedido && bTieneArmas && Accion == EAccionArma::Ninguna)
	{
		const int32 Costo = TieneDote(EDote::EscudoVeloz) ? 0 : 1;
		if (Costo == 0 || Ficha->GastarAcciones(Costo))
		{
			bBloqueoPedido = true;
			InicioBloqueo = GetWorld()->GetTimeSeconds();
			Ficha->SetBloqueando(true);
		}
	}
	else if (!bPideBloqueo && bBloqueoPedido)
	{
		bBloqueoPedido = false;
		Ficha->SetBloqueando(false);
	}

	// Ataques: clic izquierdo (mantener = tajo potente)
	if (bTieneArmas && !Ficha->bBloqueando)
	{
		if (PC->WasInputKeyJustPressed(EKeys::LeftMouseButton) && Accion == EAccionArma::Ninguna)
		{
			Accion = EAccionArma::Cargando;
			TiempoCarga = 0.f;
		}
		if (Accion == EAccionArma::Cargando)
		{
			TiempoCarga += Dt;
			if (!PC->IsInputKeyDown(EKeys::LeftMouseButton))
			{
				Accion = EAccionArma::Ninguna;
				EmpezarAccion(TiempoCarga >= 0.45f && !bUsandoDaga ? EAccionArma::TajoPotente : EAccionArma::Tajo);
			}
		}
		if (Accion == EAccionArma::Ninguna)
		{
			if (PC->WasInputKeyJustPressed(EKeys::F)) EmpezarAccion(EAccionArma::GolpeEscudo);
			if (PC->WasInputKeyJustPressed(EKeys::Q)) EmpezarAccion(EAccionArma::Embestida);
		}
	}
	if (PC->WasInputKeyJustPressed(EKeys::R) && Accion == EAccionArma::Ninguna) UsarManos();
	if (Accion == EAccionArma::Ninguna)
	{
		if (PC->WasInputKeyJustPressed(EKeys::T)) Desmoralizar();
		if (PC->WasInputKeyJustPressed(EKeys::V)) TratarHeridas();
		if (PC->WasInputKeyJustPressed(EKeys::G)) ArrojarAguaBendita();
		if (PC->WasInputKeyJustPressed(EKeys::C)) BeberPocion();
	}
	// Varias vías para un mismo obstáculo: la rueda del ratón elige.
	if (InteractuableEnMira && InteractuableEnMira->Opciones.Num() > 1)
	{
		if (PC->WasInputKeyJustPressed(EKeys::MouseScrollUp)) InteractuableEnMira->CambiarSeleccion(-1);
		if (PC->WasInputKeyJustPressed(EKeys::MouseScrollDown)) InteractuableEnMira->CambiarSeleccion(1);
	}
	if (PC->WasInputKeyJustPressed(EKeys::Two) && bTieneDaga && Accion == EAccionArma::Ninguna)
	{
		bUsandoDaga = !bUsandoDaga;
		Reproducir(TEXT("sfx_desenvainar"), 0.7f, bUsandoDaga ? 1.2f : 1.f);
	}

	// Con una escena en curso la E adelanta el texto (lo maneja el GameMode); si no, interactúa.
	AVaelithGameMode* GMe = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	const bool bHayLinea = GMe && GMe->HayEscenaEnCurso();
	if (!bHayLinea && InteractuableEnMira && InteractuableEnMira->PuedeUsarse() && (GMe ? GMe->TeclaNueva(PC, EKeys::E) : PC->WasInputKeyJustPressed(EKeys::E)))
	{
		InteractuableEnMira->Usar(this);
	}
}

void AVaelithCharacter::EmpezarAccion(EAccionArma Nueva)
{
	int32 Costo = 1;
	if (Nueva == EAccionArma::TajoPotente) Costo = 2;
	if (!Ficha->GastarAcciones(Costo))
	{
		Reproducir(TEXT("sfx_respiracion"), 0.5f, 1.2f);  // sin aliento
		return;
	}
	Accion = Nueva;
	TiempoAccion = 0.f;
	bGolpeAplicado = false;
	GolpeadosEnAccion.Reset();
	switch (Nueva)
	{
	case EAccionArma::Tajo:        DuracionAccion = bUsandoDaga ? 0.34f : 0.52f; break;
	case EAccionArma::TajoPotente: DuracionAccion = 0.85f; break;
	case EAccionArma::GolpeEscudo: DuracionAccion = 0.45f; break;
	case EAccionArma::Embestida:   DuracionAccion = 0.6f;
		LaunchCharacter(GetActorForwardVector() * 650.f + FVector(0, 0, 60.f), true, false);
		break;
	default: DuracionAccion = 0.5f; break;
	}
	Reproducir(Nueva == EAccionArma::GolpeEscudo || Nueva == EAccionArma::Embestida ? TEXT("sfx_esfuerzo") : TEXT("sfx_tajo"), 0.8f,
		Nueva == EAccionArma::TajoPotente ? 0.85f : (bUsandoDaga ? 1.25f : 1.f));
}

void AVaelithCharacter::ActualizarAccion(float Dt)
{
	if (Accion == EAccionArma::Ninguna || Accion == EAccionArma::Cargando) return;
	TiempoAccion += Dt;
	const float T = TiempoAccion / DuracionAccion;
	float Desde = 0.3f, Hasta = 0.55f;
	switch (Accion)
	{
	case EAccionArma::Tajo:        Desde = bUsandoDaga ? 0.2f : 0.3f; Hasta = bUsandoDaga ? 0.5f : 0.55f; break;
	case EAccionArma::TajoPotente: Desde = 0.45f; Hasta = 0.62f; break;
	case EAccionArma::GolpeEscudo: Desde = 0.18f; Hasta = 0.42f; break;
	case EAccionArma::Embestida:   Desde = 0.05f; Hasta = 0.5f; break;
	default: break;
	}
	if (T >= Desde && T <= Hasta) AplicarGolpe();
	if (T >= 1.f) Accion = EAccionArma::Ninguna;
}

void AVaelithCharacter::AplicarGolpe()
{
	const FVector Ojo = Camara->GetComponentLocation();
	const FVector Frente = GetViewRotation().Vector();  // mira real (ver BuscarInteractuable)
	float Alcance = 210.f, Radio = 45.f;
	if (bUsandoDaga && (Accion == EAccionArma::Tajo)) Alcance = 150.f;
	if (Accion == EAccionArma::GolpeEscudo) { Alcance = 150.f; Radio = 55.f; }
	if (Accion == EAccionArma::Embestida) { Alcance = 120.f; Radio = 70.f; }

	TArray<FHitResult> Golpes;
	FCollisionQueryParams Params(SCENE_QUERY_STAT(GolpeVaelith), false, this);
	GetWorld()->SweepMultiByChannel(Golpes, Ojo + Frente * 30.f, Ojo + Frente * Alcance, FQuat::Identity, ECC_Pawn, FCollisionShape::MakeSphere(Radio), Params);

	bool bAlguno = false;
	for (const FHitResult& H : Golpes)
	{
		ANoMuerto* N = Cast<ANoMuerto>(H.GetActor());
		if (!N || !N->EstaVivo() || GolpeadosEnAccion.Contains(N)) continue;
		GolpeadosEnAccion.Add(N);

		int32 Base = 0;
		ETipoDanio Tipo = ETipoDanio::Cortante;
		bool bToque = false;
		float Aturdir = 0.f;
		FVector Empuje = FVector::ZeroVector;
		const int32 Fue = Ficha->Atributos.Fuerza;
		switch (Accion)
		{
		case EAccionArma::Tajo:
			if (bUsandoDaga) { Base = FMath::RandRange(1, 4) + Fue; Tipo = ETipoDanio::Perforante; bToque = true; }
			else { Base = FMath::RandRange(1, 8) + Fue; }
			break;
		case EAccionArma::TajoPotente:
			Base = FMath::RoundToInt((FMath::RandRange(1, 8) + Fue) * 1.5f); Aturdir = 0.6f; Empuje = Frente * 250.f;
			break;
		case EAccionArma::GolpeEscudo:
			Base = FMath::RandRange(1, 4) + Fue; Tipo = ETipoDanio::Contundente; Aturdir = 0.5f; Empuje = Frente * 200.f;
			break;
		case EAccionArma::Embestida:
			Base = 0; Tipo = ETipoDanio::Contundente; Aturdir = 0.8f; Empuje = Frente * 700.f;
			break;
		default: break;
		}
		// PF2e: contra un enemigo desprevenido (aturdido, después de una Embestida o de la Retribución) o por la
		// espalda, el golpe es crítico (+10 sobre su CA, traducido): daño doble.
		const bool bEspalda = FVector::DotProduct(N->GetActorForwardVector().GetSafeNormal2D(), Frente.GetSafeNormal2D()) > 0.5f;
		const bool bCritico = Base > 0 && (N->Ficha->Condicion(ECondicion::Desprevenido) > 0 || bEspalda);
		if (bCritico)
		{
			Base *= 2;
			if (AVaelithGameMode* GMc = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GMc->Destello(TEXT("Crítico"), 0.9f);
		}
		const int32 Danio = Base > 0 ? Ficha->RegistrarAtaque(Base) : 0;
		if (Danio > 0 || Aturdir > 0.f)
		{
			N->RecibirAtaque(Danio, Tipo, bToque, Aturdir, Empuje);
		}
		if (TieneDote(EDote::GolpeVital) && (Accion == EAccionArma::Tajo || Accion == EAccionArma::TajoPotente) && N->EstaVivo())
		{
			N->RecibirAtaque(FMath::RandRange(1, 6), ETipoDanio::Vital, true, 0.f, FVector::ZeroVector);
		}
		bAlguno = true;
	}
	if (bAlguno && !bGolpeAplicado)
	{
		bGolpeAplicado = true;
		Reproducir(Accion == EAccionArma::GolpeEscudo || Accion == EAccionArma::Embestida ? TEXT("sfx_impacto_escudo") : TEXT("sfx_impacto_carne"), 0.9f);
		Sacudir(Accion == EAccionArma::TajoPotente ? 0.8f : 0.45f);
		Retroceso = 1.f;
		UGameplayStatics::SetGlobalTimeDilation(this, 0.08f);
		Hitstop = Accion == EAccionArma::TajoPotente ? 0.09f : 0.05f;
	}
}

bool AVaelithCharacter::RecibirGolpe(int32 Danio, ETipoDanio Tipo, AActor* Atacante)
{
	if (EnDespertar() || Ficha->bMuerto) return false;
	const float Ahora = GetWorld()->GetTimeSeconds();
	const FVector HaciaAtacante = Atacante ? (Atacante->GetActorLocation() - GetActorLocation()).GetSafeNormal2D() : GetActorForwardVector();
	const bool bDeFrente = FVector::DotProduct(HaciaAtacante, GetActorForwardVector().GetSafeNormal2D()) > 0.35f;

	if (Ficha->bBloqueando && bDeFrente && Ahora - InicioBloqueo <= 0.25f)
	{
		// Bloqueo perfecto: Golpe de retribución.
		UltimoBloqueoPerfecto = Ahora;
		Reproducir(TEXT("sfx_parada"), 1.f);
		Sacudir(0.5f);
		UGameplayStatics::SetGlobalTimeDilation(this, 0.1f);
		Hitstop = 0.12f;
		if (ANoMuerto* N = Cast<ANoMuerto>(Atacante))
		{
			const bool bMayor = TieneDote(EDote::RetribucionMayor);
			const int32 Ret = (FMath::RandRange(1, 8) + Ficha->Atributos.Fuerza) * (bMayor ? 2 : 1);
			N->RecibirAtaque(Ret, ETipoDanio::Cortante, false, bMayor ? 2.f : 1.f, GetActorForwardVector() * 300.f);
		}
		return true;
	}

	const bool bBloqueaba = Ficha->bBloqueando;
	if (!bDeFrente) Ficha->bBloqueando = false;  // el escudo alzado solo cuenta de frente (CA +2)

	// Tirada de ataque oculta contra la CA (grados de PF2e): fallo = no entra, crítico = doble.
	ANoMuerto* Enemigo = Cast<ANoMuerto>(Atacante);
	const int32 Bono = Enemigo ? Enemigo->Ficha->Ataque() : 7;
	int32 Total = 0;
	const EGrado Grado = Ficha->RecibirTiradaAtaque(Bono, 0, &Total);
	UE_LOG(LogTemp, Log, TEXT("[vaelith] ataque enemigo +%d total=%d CA=%d grado=%d"), Bono, Total, Ficha->CA(), int32(Grado));
	if (Grado == EGrado::Fallo || Grado == EGrado::FalloCritico)
	{
		Ficha->bBloqueando = bBloqueaba;
		Reproducir(bBloqueaba && bDeFrente ? TEXT("sfx_bloqueo") : TEXT("sfx_tajo"), 0.5f, 1.4f);
		if (AVaelithGameMode* GMd = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GMd->Destello(bBloqueaba && bDeFrente ? TEXT("Desviado") : TEXT("Esquivado"), 0.7f);
		return false;
	}
	const bool bCritico = Grado == EGrado::ExitoCritico;
	if (bCritico) Danio *= 2;

	const int32 Antes = Ficha->PGEscudo;
	const int32 Perdido = Ficha->RecibirDanio(Danio, Tipo, false, bCritico);
	Ficha->bBloqueando = bBloqueaba && !Ficha->EscudoDestruido();
	// Toque del espectro: salvación de Voluntad contra el miedo (CD 16). Fallo: Asustado 1; fallo crítico: 2.
	if (Enemigo && Enemigo->Tipo == ETipoNoMuerto::Fantasma && !Ficha->bMoribundo && !Ficha->bMuerto)
	{
		const EGrado Miedo = Ficha->TirarSalvacion(ESalvacion::Voluntad, 16);
		const int32 Asustado = Miedo == EGrado::FalloCritico ? 2 : (Miedo == EGrado::Fallo ? 1 : 0);
		if (Asustado > Ficha->Condicion(ECondicion::Asustado))
		{
			Ficha->SetCondicion(ECondicion::Asustado, Asustado);
			if (AVaelithGameMode* GMm = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GMm->Destello(FString::Printf(TEXT("Asustado %d"), Asustado), 1.2f);
		}
	}
	if (bBloqueaba && bDeFrente)
	{
		Reproducir(TEXT("sfx_bloqueo"), 0.9f);
		Sacudir(0.3f);
		if (Antes > 0 && Ficha->EscudoDestruido())
		{
			Reproducir(TEXT("sfx_escudo_roto"), 1.f);
			if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->Aviso(TEXT("Escudo destruido"), TEXT("Un altar de Pharasma puede repararlo."));
		}
	}
	if (Perdido > 0)
	{
		UltimoDanioRecibido = Ahora;
		Reproducir(TEXT("sfx_herido"), 0.9f);
		Sacudir(0.7f);
	}
	if (Ficha->bMuerto)
	{
		if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->JugadorMurio();
	}
	return false;
}

void AVaelithCharacter::UsarManos()
{
	if (Ficha->bAnatema)
	{
		if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->Aviso(TEXT("Anatema"), TEXT("Tu foco no responde. Expiá ante un altar de Pharasma."), 3.f);
		return;
	}
	if (Ficha->Foco <= 0)
	{
		if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->Aviso(TEXT("Sin foco"), TEXT("Rezá en un altar de Pharasma para recuperarlo."), 3.f);
		return;
	}
	if (!Ficha->GastarAcciones(1)) return;
	Ficha->GastarFoco();
	Accion = EAccionArma::Manos;
	TiempoAccion = 0.f;
	DuracionAccion = 0.7f;
	Reproducir(TEXT("sfx_manos"), 1.f);

	// Si hay un no-muerto delante, la energía de Pharasma lo hiere; si no, cura.
	FHitResult H;
	const FVector Ojo = Camara->GetComponentLocation();
	FCollisionQueryParams Params(SCENE_QUERY_STAT(Manos), false, this);
	if (GetWorld()->SweepSingleByChannel(H, Ojo, Ojo + GetViewRotation().Vector() * 220.f, FQuat::Identity, ECC_Pawn, FCollisionShape::MakeSphere(50.f), Params))
	{
		if (ANoMuerto* N = Cast<ANoMuerto>(H.GetActor()))
		{
			if (N->EstaVivo())
			{
				N->RecibirAtaque(FMath::RandRange(1, 6) + FMath::RandRange(1, 6), ETipoDanio::Vital, true, 0.4f, FVector::ZeroVector);
				return;
			}
		}
	}
	Ficha->Curar(6);
}

ANoMuerto* AVaelithCharacter::EnemigoDelante(float Alcance, float Radio) const
{
	TArray<FHitResult> Golpes;
	const FVector Ojo = Camara->GetComponentLocation();
	const FVector Frente = GetViewRotation().Vector();
	FCollisionQueryParams Params(SCENE_QUERY_STAT(EnemigoDelante), false, this);
	GetWorld()->SweepMultiByChannel(Golpes, Ojo + Frente * 30.f, Ojo + Frente * Alcance, FQuat::Identity, ECC_Pawn, FCollisionShape::MakeSphere(Radio), Params);
	for (const FHitResult& H : Golpes)
	{
		if (ANoMuerto* N = Cast<ANoMuerto>(H.GetActor()))
		{
			if (N->EstaVivo()) return N;
		}
	}
	return nullptr;
}

bool AVaelithCharacter::HayEnemigoCerca(float Radio) const
{
	for (TActorIterator<ANoMuerto> It(GetWorld()); It; ++It)
	{
		if (It->EstaVivo() && It->Tipo != ETipoNoMuerto::Guardian && FVector::Dist(It->GetActorLocation(), GetActorLocation()) < Radio) return true;
	}
	return false;
}

void AVaelithCharacter::Desmoralizar()
{
	// Intimidación (1 acción) contra la Voluntad del objetivo. Los no-muertos sin mente son inmunes (PF2e).
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	ANoMuerto* N = EnemigoDelante(700.f, 60.f);
	if (!N || !GM) return;
	if (!Ficha->GastarAcciones(1)) return;
	Reproducir(TEXT("sfx_esfuerzo"), 0.9f, 0.8f);
	if (N->Ficha->bSinMente)
	{
		GM->Destello(TEXT("No tiene mente que asustar"), 1.4f);
		return;
	}
	const int32 CD = 10 + N->Ficha->Salvacion(ESalvacion::Voluntad);
	const EGrado G = Ficha->Prueba(EHabilidad::Intimidacion, CD);
	const int32 Valor = G == EGrado::ExitoCritico ? 2 : (G == EGrado::Exito ? 1 : 0);
	GM->Destello(FString::Printf(TEXT("Intimidación: %s"), *Planilla::Nombre(G).ToString()), 1.2f);
	if (Valor > 0) N->Ficha->SetCondicion(ECondicion::Asustado, Valor);
}

void AVaelithCharacter::TratarHeridas()
{
	// Medicina (Tratar heridas): fuera de combate, 3 s quieto. CD 15: éxito 2d8, crítico 4d8, fallo crítico 1d8 de daño.
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (!GM || Ficha->PG >= Ficha->PGMax()) return;
	if (!bTratoHeridasDisponible) { GM->Destello(TEXT("Ya trataste tus heridas: rezá en un altar"), 1.8f); return; }
	if (HayEnemigoCerca(1500.f)) { GM->Destello(TEXT("No con enemigos cerca"), 1.4f); return; }
	bTratoHeridasDisponible = false;
	const EGrado G = Ficha->Prueba(EHabilidad::Medicina, 15);
	int32 Cura = 0;
	if (G == EGrado::ExitoCritico) for (int32 i = 0; i < 4; ++i) Cura += FMath::RandRange(1, 8);
	else if (G == EGrado::Exito) Cura = FMath::RandRange(1, 8) + FMath::RandRange(1, 8);
	if (G == EGrado::FalloCritico) Ficha->RecibirDanio(FMath::RandRange(1, 8), ETipoDanio::Contundente);
	else Ficha->Curar(Cura);
	TratandoHasta = GetWorld()->GetTimeSeconds() + 3.f;
	bControlBloqueado = true;
	Reproducir(TEXT("sfx_respiracion"), 0.8f, 1.1f);
	GM->Destello(FString::Printf(TEXT("Medicina: %s"), *Planilla::Nombre(G).ToString()), 2.5f);
}

void AVaelithCharacter::ArrojarAguaBendita()
{
	// Frasco de agua bendita (los pharasmitas siempre llevan): 1 acción, daño vital 1d6 + 1 a un no-muerto delante.
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (!GM) return;
	if (AguaBendita <= 0) { GM->Destello(TEXT("Sin agua bendita"), 1.f); return; }
	ANoMuerto* N = EnemigoDelante(1100.f, 70.f);
	if (!N) { GM->Destello(TEXT("No hay a quién arrojarla"), 1.f); return; }
	if (!Ficha->GastarAcciones(1)) return;
	--AguaBendita;
	Reproducir(TEXT("sfx_manos"), 0.9f, 1.3f);
	N->RecibirAtaque(FMath::RandRange(1, 6) + 1, ETipoDanio::Vital, true, 0.3f, FVector::ZeroVector);
}

void AVaelithCharacter::BeberPocion()
{
	// Poción de curación menor: 1 acción, 1d8.
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (!GM) return;
	if (Pociones <= 0) { GM->Destello(TEXT("Sin pociones"), 1.f); return; }
	if (Ficha->PG >= Ficha->PGMax() || !Ficha->GastarAcciones(1)) return;
	--Pociones;
	Ficha->Curar(FMath::RandRange(1, 8));
	Reproducir(TEXT("sfx_respiracion"), 0.6f, 1.2f);
}

void AVaelithCharacter::DarObjeto(const FString& Objeto, int32 Cantidad)
{
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (Objeto == TEXT("pocion")) { Pociones += Cantidad; if (GM) GM->Destello(TEXT("Poción de curación (C)"), 1.8f); }
	else if (Objeto == TEXT("agua_bendita")) { AguaBendita += Cantidad; if (GM) GM->Destello(TEXT("Agua bendita (G)"), 1.8f); }
}

float AVaelithCharacter::Carga() const
{
	// Armadura completa 4 + espada larga 1 + escudo 1 + daga (ligera) + frascos y pociones (ligeros, 0,1 cada uno).
	float C = 4.f;
	if (bTieneArmas) C += 2.f;
	if (bTieneDaga) C += 0.1f;
	return C + 0.1f * (AguaBendita + Pociones);
}

void AVaelithCharacter::AnimarArmas(float Dt)
{
	const bool bMueve = GetVelocity().Size2D() > 30.f && GetCharacterMovement()->IsMovingOnGround();
	// Pasos: uno cada ~1,6 m caminando (más seguidos al correr).
	if (bMueve)
	{
		DistanciaPaso += GetVelocity().Size2D() * Dt;
		if (DistanciaPaso > 165.f)
		{
			DistanciaPaso = 0.f;
			Reproducir(TEXT("sfx_paso"), Ficha->bBloqueando ? 0.2f : 0.35f, 1.f);
		}
	}
	FaseCabeceo += Dt * (bMueve ? GetVelocity().Size2D() / 330.f * 9.f : 1.6f);
	const float Amp = bMueve ? 1.f : 0.25f;
	const FVector Cabeceo(0.f, FMath::Sin(FaseCabeceo * 0.5f) * 1.2f * Amp, FMath::Abs(FMath::Sin(FaseCabeceo * 0.5f)) * -1.4f * Amp);

	// Balanceo por el movimiento del mouse (las armas se atrasan un poco).
	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		float MX = 0.f, MY = 0.f;
		PC->GetInputMouseDelta(MX, MY);
		Balanceo = FMath::Vector2DInterpTo(Balanceo, FVector2D(FMath::Clamp(MX, -4.f, 4.f), FMath::Clamp(MY, -4.f, 4.f)), Dt, 10.f);
	}
	const FRotator RotBalanceo(Balanceo.Y * 1.2f, -Balanceo.X * 1.5f, -Balanceo.X * 1.f);

	// ---- Mano derecha (espada o daga) ----
	FPose Der;
	const float T = DuracionAccion > 0.f ? TiempoAccion / DuracionAccion : 1.f;
	if (Accion == EAccionArma::Cargando)
	{
		Der = Mezcla({}, { FVector(-6.f, 6.f, 10.f), FRotator(28.f, 32.f, -80.f) }, TiempoCarga / 0.45f);
		Der.Pos += FVector(0.f, FMath::FRandRange(-0.3f, 0.3f), FMath::FRandRange(-0.3f, 0.3f)) * FMath::Clamp(TiempoCarga - 0.45f, 0.f, 1.f) * 3.f;
	}
	else if (Accion == EAccionArma::Tajo && bUsandoDaga)
	{
		Der = Curva({ {0.f, {}}, {0.2f, {FVector(-8.f, 2.f, 2.f), FRotator(5.f, 0.f, 0.f)}}, {0.42f, {FVector(30.f, -10.f, 6.f), FRotator(-20.f, -10.f, 0.f)}}, {1.f, {}} }, T);
	}
	else if (Accion == EAccionArma::Tajo)
	{
		Der = Curva({ {0.f, {}}, {0.25f, {FVector(-4.f, 6.f, 8.f), FRotator(18.f, 28.f, -65.f)}}, {0.58f, {FVector(16.f, -34.f, -14.f), FRotator(-38.f, -42.f, 78.f)}}, {1.f, {}} }, T);
	}
	else if (Accion == EAccionArma::TajoPotente)
	{
		Der = Curva({ {0.f, {FVector(-6.f, 6.f, 10.f), FRotator(28.f, 32.f, -80.f)}}, {0.4f, {FVector(-10.f, 10.f, 18.f), FRotator(40.f, 30.f, -95.f)}}, {0.62f, {FVector(22.f, -30.f, -26.f), FRotator(-60.f, -35.f, 70.f)}}, {1.f, {}} }, T);
	}
	else if (Accion == EAccionArma::Manos || Accion == EAccionArma::GolpeEscudo || Accion == EAccionArma::Embestida)
	{
		Der = Curva({ {0.f, {}}, {0.3f, {FVector(-8.f, 8.f, -8.f), FRotator(-10.f, 10.f, 0.f)}}, {1.f, {}} }, T);
	}
	if (Retroceso > 0.f)
	{
		Der.Pos.X -= Retroceso * 4.f;
		Retroceso = FMath::Max(0.f, Retroceso - Dt * 6.f);
	}
	PivoteDerecho->SetRelativeLocation(BaseDerecha + Cabeceo + Der.Pos);
	PivoteDerecho->SetRelativeRotation(Der.Rot + RotBalanceo);
	Espada->SetVisibility(bTieneArmas && !bUsandoDaga);
	Daga->SetVisibility(bTieneArmas && bUsandoDaga);

	// ---- Mano izquierda (escudo) ----
	AlturaEscudo = FMath::FInterpTo(AlturaEscudo, Ficha->bBloqueando ? 1.f : 0.f, Dt, Ficha->bBloqueando ? 18.f : 9.f);
	FPose Izq = Mezcla({ FVector::ZeroVector, FRotator(-6.f, 32.f, -12.f) }, { FVector(4.f, 16.f, 10.f), FRotator(0.f, 4.f, 0.f) }, AlturaEscudo);
	if (Accion == EAccionArma::GolpeEscudo)
	{
		Izq = Curva({ {0.f, Izq}, {0.18f, {FVector(-6.f, 14.f, 12.f), FRotator(0.f, 10.f, 0.f)}}, {0.36f, {FVector(34.f, 22.f, 16.f), FRotator(0.f, 0.f, 0.f)}}, {1.f, Izq} }, T);
	}
	else if (Accion == EAccionArma::Embestida)
	{
		Izq = Curva({ {0.f, Izq}, {0.15f, {FVector(20.f, 20.f, 14.f), FRotator::ZeroRotator}}, {0.7f, {FVector(24.f, 20.f, 14.f), FRotator::ZeroRotator}}, {1.f, Izq} }, T);
	}
	PivoteIzquierdo->SetRelativeLocation(BaseIzquierda + Cabeceo * 0.8f + Izq.Pos);
	PivoteIzquierdo->SetRelativeRotation(Izq.Rot + RotBalanceo * 0.7f);
	const bool bEscudoVisible = bTieneArmas && !Ficha->EscudoDestruido();
	Escudo->SetVisibility(bEscudoVisible);

	// Temblor de cámara (sin assets): ruido que decae.
	if (TemblorPantalla > 0.f)
	{
		const float S = TemblorPantalla * TemblorPantalla;
		Camara->SetRelativeRotation(FRotator(FMath::FRandRange(-1.f, 1.f) * 1.4f * S, FMath::FRandRange(-1.f, 1.f) * 1.4f * S, FMath::FRandRange(-1.f, 1.f) * 1.8f * S));
		TemblorPantalla = FMath::Max(0.f, TemblorPantalla - FApp::GetDeltaTime() * 2.5f);
	}
	else if (!EnDespertar())
	{
		Camara->SetRelativeRotation(FRotator::ZeroRotator);
	}
}

void AVaelithCharacter::ActualizarPostProceso(float Dt)
{
	FPostProcessSettings& P = Camara->PostProcessSettings;
	const float Ahora = GetWorld()->GetTimeSeconds();
	const float Herida = FMath::Clamp(1.f - (Ahora - UltimoDanioRecibido) / 0.6f, 0.f, 1.f);
	const float Vida = Ficha->PGMax() > 0 ? float(Ficha->PG) / Ficha->PGMax() : 1.f;
	const float Peligro = Ficha->bMoribundo ? 1.f : FMath::Clamp((0.35f - Vida) / 0.35f, 0.f, 1.f);
	const float Corr = Penitencia / 3.f;

	float Sat = FMath::Lerp(1.f, 0.72f, NivelPenumbra);
	Sat = FMath::Lerp(Sat, 0.05f, Desaturacion);
	Sat *= 1.f - 0.15f * Corr;
	Sat = FMath::Lerp(Sat, 0.2f, Peligro * 0.8f);
	P.bOverride_ColorSaturation = true;
	P.ColorSaturation = FVector4(Sat, Sat, Sat, 1.f);

	FVector4 Ganancia(1.f, 1.f, 1.f, 1.f);
	Ganancia = FMath::Lerp(Ganancia, FVector4(0.86f, 0.94f, 1.12f, 1.f), NivelPenumbra);
	Ganancia = FMath::Lerp(Ganancia, FVector4(0.9f, 1.f, 0.9f, 1.f), Corr * 0.6f);
	Ganancia = FMath::Lerp(Ganancia, FVector4(1.4f, 0.75f, 0.7f, 1.f), Herida * 0.5f);
	Ganancia = FMath::Lerp(Ganancia, FVector4(1.05f, 0.97f, 0.85f, 1.f), Desaturacion);  // recuerdos: sepia frío
	P.bOverride_ColorGain = true;
	P.ColorGain = Ganancia;

	P.bOverride_VignetteIntensity = true;
	P.VignetteIntensity = 0.45f + 0.25f * NivelPenumbra + 0.2f * Corr + 0.5f * Peligro + 0.3f * Herida + 0.3f * Desaturacion;

	P.bOverride_SceneFringeIntensity = true;
	P.SceneFringeIntensity = 1.5f * Desaturacion + 2.f * Herida + 1.5f * Peligro;
	P.bOverride_FilmGrainIntensity = true;
	P.FilmGrainIntensity = 0.15f + 0.35f * Desaturacion + 0.2f * Corr;

	P.bOverride_AutoExposureBias = true;
	P.AutoExposureBias = 0.6f * NivelPenumbra - 0.5f * Corr;

	if (Desenfoque > 0.01f)
	{
		P.bOverride_DepthOfFieldFocalDistance = true;
		P.DepthOfFieldFocalDistance = FMath::Lerp(2000.f, 3.f, Desenfoque);
		P.bOverride_DepthOfFieldFstop = true;
		P.DepthOfFieldFstop = FMath::Lerp(4.f, 0.6f, Desenfoque);
	}
	else
	{
		P.bOverride_DepthOfFieldFocalDistance = false;
		P.bOverride_DepthOfFieldFstop = false;
	}

	// La visión en penumbra: una luz suave sin sombras, solo en las catacumbas.
	Penumbra->SetIntensity(FMath::FInterpTo(Penumbra->Intensity, 700.f * NivelPenumbra * (1.f - 0.25f * Corr), Dt, 2.f));
}

void AVaelithCharacter::BuscarInteractuable()
{
	InteractuableEnMira = nullptr;
	TextoInteraccion.Reset();
	if (EnDespertar() || bControlBloqueado) return;
	FHitResult H;
	const FVector Ojo = Camara->GetComponentLocation();
	FCollisionQueryParams Params(SCENE_QUERY_STAT(Mirar), false, this);
	// La mira real es la rotación de control: en Tick la cámara está en rotación cero y la
	// inclinación se aplica después, al calcular la vista. Con GetForwardVector() el barrido
	// salía siempre horizontal y nunca tocaba objetos bajos (urnas, lápidas).
	const FVector Frente = GetViewRotation().Vector();
	if (GetWorld()->SweepSingleByChannel(H, Ojo, Ojo + Frente * 260.f, FQuat::Identity, ECC_Visibility, FCollisionShape::MakeSphere(18.f), Params))
	{
		if (AInteractuable* I = Cast<AInteractuable>(H.GetActor()))
		{
			if (I->PuedeUsarse())
			{
				InteractuableEnMira = I;
				TextoInteraccion = I->Opciones.Num() > 0 ? I->TextoOpciones(Ficha) : I->TextoAccion().ToString();
				return;
			}
		}
	}
	// Si la mira no toca justo el objeto (urnas, dagas: son chicos), se toma el
	// interactuable más cercano dentro de un cono de ~20° delante de la mira, sin paredes en el medio.
	float Mejor = 250.f;
	for (TActorIterator<AInteractuable> It(GetWorld()); It; ++It)
	{
		AInteractuable* I = *It;
		if (!I->PuedeUsarse()) continue;
		const FVector Centro = I->GetComponentsBoundingBox(false, true).GetCenter();
		const FVector A = Centro - Ojo;
		const float Dist = A.Size();
		if (Dist >= Mejor || Dist < 1.f || FVector::DotProduct(A / Dist, Frente) < 0.94f) continue;
		FHitResult Muro;
		if (GetWorld()->LineTraceSingleByChannel(Muro, Ojo, Centro, ECC_Visibility, Params) && Muro.GetActor() != I) continue;
		Mejor = Dist;
		InteractuableEnMira = I;
	}
	if (InteractuableEnMira) TextoInteraccion = InteractuableEnMira->Opciones.Num() > 0 ? InteractuableEnMira->TextoOpciones(Ficha) : InteractuableEnMira->TextoAccion().ToString();
}

void AVaelithCharacter::IniciarDespertar()
{
	TiempoDespertar = 0.f;
	YawDespertar = GetActorRotation().Yaw;
	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		PC->SetControlRotation(FRotator(80.f, YawDespertar, 0.f));
	}
	Camara->SetRelativeLocation(FVector(0.f, 0.f, -70.f));
	Desenfoque = 1.f;
}

void AVaelithCharacter::ActualizarDespertar(float Dt)
{
	TiempoDespertar += Dt;
	const float T = TiempoDespertar;
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();

	// Parpadeos: abre, se cierra, abre de nuevo.
	float Negro = 1.f;
	if (T > 4.f) Negro = 1.f - FMath::SmoothStep(4.f, 6.f, T);
	if (T > 6.3f && T < 7.4f) Negro = FMath::Max(Negro, FMath::Sin((T - 6.3f) / 1.1f * PI) * 0.9f);
	if (T > 8.6f && T < 9.2f) Negro = FMath::Max(Negro, FMath::Sin((T - 8.6f) / 0.6f * PI) * 0.6f);
	if (GM) GM->FundidoNegro = Negro;
	Desenfoque = 1.f - FMath::SmoothStep(5.f, 14.f, T);

	if (T > 0.5f && T - Dt <= 0.5f) Reproducir(TEXT("sfx_latido"), 0.9f);
	if (T > 3.f && T - Dt <= 3.f) Reproducir(TEXT("sfx_respiracion"), 0.8f, 0.85f);

	// Mira el techo; a los 13 s se incorpora.
	const float Incorporarse = FMath::SmoothStep(13.f, 16.5f, T);
	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		const float Mirar = T > 9.5f && T < 13.f ? FMath::Sin((T - 9.5f) * 0.9f) * 12.f : 0.f;
		// Yaw fijo de la losa: el cuerpo copia el yaw del control (bUseControllerRotationYaw), así que
		// sumar Mirar al yaw del cuerpo lo acumulaba cuadro a cuadro y la cámara daba vueltas.
		PC->SetControlRotation(FRotator(FMath::Lerp(80.f, -6.f, Incorporarse), YawDespertar + Mirar, 0.f));
	}
	Camara->SetRelativeLocation(FVector(0.f, 0.f, FMath::Lerp(-70.f, 70.f, Incorporarse)));
	Camara->SetRelativeRotation(FRotator(0.f, 0.f, FMath::Lerp(8.f, 0.f, Incorporarse)));

	if (T >= 17.f)
	{
		TiempoDespertar = -1.f;
		Desenfoque = 0.f;
		if (GM) GM->FundidoNegro = 0.f;
		Camara->SetRelativeLocation(FVector(0.f, 0.f, 70.f));
	}
}
