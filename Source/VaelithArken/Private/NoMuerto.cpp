#include "NoMuerto.h"
#include "VaelithCharacter.h"
#include "VaelithGameMode.h"
#include "Interactuable.h"
#include "AIController.h"
#include "Animation/AnimInstance.h"
#include "Animation/AnimSequenceBase.h"
#include "Components/CapsuleComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Materials/MaterialInterface.h"
#include "Navigation/PathFollowingComponent.h"
#include "Sound/SoundBase.h"

ANoMuerto::ANoMuerto()
{
	PrimaryActorTick.bCanEverTick = true;
	AIControllerClass = AAIController::StaticClass();
	AutoPossessAI = EAutoPossessAI::PlacedInWorldOrSpawned;
	GetCapsuleComponent()->InitCapsuleSize(36.f, 90.f);
	GetMesh()->SetRelativeLocation(FVector(0.f, 0.f, -90.f));
	GetMesh()->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));
	bUseControllerRotationYaw = false;
	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.f, 360.f, 0.f);

	Ficha = CreateDefaultSubobject<UFichaComponent>(TEXT("Ficha"));
	Ficha->bTieneDiehard = false;
	Ficha->bTieneEscudo = false;

	Brillo = CreateDefaultSubobject<UPointLightComponent>(TEXT("Brillo"));
	Brillo->SetupAttachment(GetCapsuleComponent());
	Brillo->SetRelativeLocation(FVector(15.f, 0.f, 62.f));
	Brillo->SetCastShadows(false);
	Brillo->SetIntensityUnits(ELightUnits::Unitless);
	Brillo->SetAttenuationRadius(260.f);
	Brillo->SetIntensity(0.f);
}

void ANoMuerto::BeginPlay()
{
	Super::BeginPlay();
	Configurar();
	if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>())
	{
		if (!Hecho.IsNone() && GM->HechoOcurrido(Hecho))
		{
			Destroy();
			return;
		}
	}
	Cambiar(Tipo == ETipoNoMuerto::Sombra ? EEstadoNoMuerto::Dormido : EEstadoNoMuerto::Acecho);
}

void ANoMuerto::Configurar()
{
	const TCHAR* RutaMalla = TEXT("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple");
	const TCHAR* RutaMaterial = TEXT("/Game/Vaelith/Materiales/M_Zombi.M_Zombi");
	FLinearColor ColorBrillo(0.5f, 0.8f, 0.6f);
	float IntensidadBrillo = 0.f;
	FVector Escala(1.f);
	UCharacterMovementComponent* Mov = GetCharacterMovement();

	switch (Tipo)
	{
	case ETipoNoMuerto::Zombi:
		Ficha->PGBaseFijos = 22; VelocidadBase = 140.f; DanioDado = 6; DanioFijo = 3; TipoGolpe = ETipoDanio::Contundente;
		TiempoAmago = 1.0f; TiempoRecuperacion = 1.1f; AlcanceGolpe = 160.f;
		Ficha->Debilidades.Add(ETipoDanio::Cortante, 3); Ficha->Debilidades.Add(ETipoDanio::Vital, 5);
		Escala = FVector(1.05f, 1.05f, 0.97f);
		break;
	case ETipoNoMuerto::Esqueleto:
		// Esqueleto propio (riggeado al maniquí UE5 por tools/blender/rig_esqueleto.py); si falta, maniquí teñido.
		if (LoadObject<USkeletalMesh>(nullptr, TEXT("/Game/Vaelith/Ext/personajes/SKM_Esqueleto.SKM_Esqueleto")))
		{
			RutaMalla = TEXT("/Game/Vaelith/Ext/personajes/SKM_Esqueleto.SKM_Esqueleto");
			RutaMaterial = nullptr;
		}
		else
		{
			RutaMalla = TEXT("/Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple.SKM_Quinn_Simple");
			RutaMaterial = TEXT("/Game/Vaelith/Materiales/M_Esqueleto.M_Esqueleto");
		}
		Ficha->PGBaseFijos = 18; VelocidadBase = 290.f; DanioDado = 6; DanioFijo = 2; TipoGolpe = ETipoDanio::Cortante;
		TiempoAmago = 0.6f; TiempoRecuperacion = 0.8f; AlcanceGolpe = 175.f;
		Ficha->Resistencias.Add(ETipoDanio::Cortante, 5); Ficha->Resistencias.Add(ETipoDanio::Perforante, 5);
		Ficha->Debilidades.Add(ETipoDanio::Contundente, 5); Ficha->Debilidades.Add(ETipoDanio::Vital, 5);
		ColorBrillo = FLinearColor(0.9f, 0.35f, 0.2f); IntensidadBrillo = 250.f;  // brasas en las cuencas
		Escala = FVector(0.92f, 0.92f, 1.02f);
		break;
	case ETipoNoMuerto::Fantasma:
		RutaMaterial = TEXT("/Game/Vaelith/Materiales/M_Fantasma.M_Fantasma");
		Ficha->PGBaseFijos = 16; VelocidadBase = 250.f; DanioDado = 6; DanioFijo = 2; TipoGolpe = ETipoDanio::Vacio;
		TiempoAmago = 0.75f; TiempoRecuperacion = 0.9f; AlcanceGolpe = 170.f;
		Ficha->bInmaterial = true; Ficha->Debilidades.Add(ETipoDanio::Vital, 5);
		ColorBrillo = FLinearColor(0.45f, 0.65f, 1.f); IntensidadBrillo = 1800.f;
		Mov->SetMovementMode(MOVE_Flying);
		Mov->MaxFlySpeed = VelocidadBase;
		Mov->BrakingDecelerationFlying = 800.f;
		GetMesh()->SetCastShadow(false);
		break;
	case ETipoNoMuerto::Guardian:
		// El centinela es un soldado ya descarnado: usa el esqueleto propio si está importado.
		if (LoadObject<USkeletalMesh>(nullptr, TEXT("/Game/Vaelith/Ext/personajes/SKM_Esqueleto.SKM_Esqueleto")))
		{
			RutaMalla = TEXT("/Game/Vaelith/Ext/personajes/SKM_Esqueleto.SKM_Esqueleto");
			RutaMaterial = nullptr;
		}
		Ficha->PGBaseFijos = 22; VelocidadBase = 0.f;
		ColorBrillo = FLinearColor(0.6f, 0.7f, 0.9f); IntensidadBrillo = 150.f;
		break;
	case ETipoNoMuerto::Sombra:
		RutaMaterial = TEXT("/Game/Vaelith/Materiales/M_Sombra.M_Sombra");
		Ficha->PGBaseFijos = 60; VelocidadBase = 340.f; DanioDado = 8; DanioFijo = 4; TipoGolpe = ETipoDanio::Cortante;
		TiempoAmago = 0.55f; TiempoRecuperacion = 0.7f; AlcanceGolpe = 190.f;
		Ficha->bTieneEscudo = true; Ficha->DurezaEscudo = 5; Ficha->PGEscudoMax = 20; Ficha->UmbralRoturaEscudo = 10;
		ColorBrillo = FLinearColor(0.55f, 0.25f, 0.9f); IntensidadBrillo = 900.f;
		DistanciaVision = 3000.f;
		break;
	}
	Mov->MaxWalkSpeed = VelocidadBase;
	SetActorScale3D(Escala);
	Ficha->DescansarEnAltar();

	if (USkeletalMesh* M = LoadObject<USkeletalMesh>(nullptr, RutaMalla))
	{
		GetMesh()->SetSkeletalMeshAsset(M);
	}
	if (UClass* ABP = LoadClass<UAnimInstance>(nullptr, TEXT("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C")))
	{
		GetMesh()->SetAnimInstanceClass(ABP);
	}
	if (UMaterialInterface* Mat = RutaMaterial ? LoadObject<UMaterialInterface>(nullptr, RutaMaterial) : nullptr)
	{
		for (int32 i = 0; i < GetMesh()->GetNumMaterials(); ++i) GetMesh()->SetMaterial(i, Mat);
	}
	Brillo->SetLightColor(ColorBrillo);
	Brillo->SetIntensity(IntensidadBrillo);
}

FText ANoMuerto::NombreVisible() const
{
	switch (Tipo)
	{
	case ETipoNoMuerto::Zombi: return NSLOCTEXT("Vaelith", "Zombi", "Muerto levantado");
	case ETipoNoMuerto::Esqueleto: return NSLOCTEXT("Vaelith", "Esqueleto", "Esqueleto");
	case ETipoNoMuerto::Fantasma: return Ancla ? NSLOCTEXT("Vaelith", "Atado", "Espíritu atado") : NSLOCTEXT("Vaelith", "Fantasma", "Espectro");
	case ETipoNoMuerto::Guardian: return NSLOCTEXT("Vaelith", "Guardian", "Centinela");
	case ETipoNoMuerto::Sombra: return NSLOCTEXT("Vaelith", "Sombra", "La Sombra");
	}
	return FText::GetEmpty();
}

void ANoMuerto::Sonar(const TCHAR* Ruta, float Volumen, float Tono)
{
	if (USoundBase* S = LoadObject<USoundBase>(nullptr, *FString::Printf(TEXT("/Game/Vaelith/Audio/%s.%s"), Ruta, Ruta)))
	{
		UGameplayStatics::PlaySoundAtLocation(this, S, GetActorLocation(), Volumen, Tono * FMath::FRandRange(0.92f, 1.08f));
	}
}

void ANoMuerto::ReproducirAnim(const TCHAR* Ruta, float Ritmo)
{
	UAnimSequenceBase* A = LoadObject<UAnimSequenceBase>(nullptr, Ruta);
	UAnimInstance* AI = GetMesh()->GetAnimInstance();
	if (A && AI)
	{
		AI->PlaySlotAnimationAsDynamicMontage(A, TEXT("DefaultSlot"), 0.15f, 0.2f, Ritmo);
	}
}

void ANoMuerto::Cambiar(EEstadoNoMuerto Nuevo)
{
	Estado = Nuevo;
	TiempoEstado = 0.f;
	if (Nuevo == EEstadoNoMuerto::Amago)
	{
		static const TCHAR* Ataques[] = {
			TEXT("/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01.MM_Attack_01"),
			TEXT("/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_02.MM_Attack_02"),
			TEXT("/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_03.MM_Attack_03") };
		ReproducirAnim(Tipo == ETipoNoMuerto::Zombi ? Ataques[0] : Ataques[FMath::RandRange(0, 2)], Tipo == ETipoNoMuerto::Zombi ? 0.7f : 1.f);
		Sonar(Tipo == ETipoNoMuerto::Fantasma ? TEXT("sfx_lamento") : TEXT("sfx_grunido"), 0.8f, Tipo == ETipoNoMuerto::Esqueleto ? 1.4f : 1.f);
		if (AController* C = GetController()) C->StopMovement();
	}
}

bool ANoMuerto::VeAlJugador(float Distancia) const
{
	const APawn* J = UGameplayStatics::GetPlayerPawn(this, 0);
	if (!J || FVector::Dist(J->GetActorLocation(), GetActorLocation()) > Distancia) return false;
	FHitResult H;
	FCollisionQueryParams P(SCENE_QUERY_STAT(VerJugador), false, this);
	P.AddIgnoredActor(J);
	return !GetWorld()->LineTraceSingleByChannel(H, GetActorLocation() + FVector(0, 0, 60.f), J->GetActorLocation() + FVector(0, 0, 60.f), ECC_Visibility, P);
}

void ANoMuerto::MoverHacia(const FVector& Destino, float Dt)
{
	if (Tipo == ETipoNoMuerto::Fantasma)
	{
		FaseFlotar += Dt;
		const FVector Objetivo = Destino + FVector(0.f, 0.f, 40.f + FMath::Sin(FaseFlotar * 2.f) * 25.f);
		AddMovementInput((Objetivo - GetActorLocation()).GetSafeNormal(), 1.f);
		return;
	}
	AAIController* AI = Cast<AAIController>(GetController());
	if (AI)
	{
		const EPathFollowingRequestResult::Type R = AI->MoveToLocation(Destino, 60.f, true, true, false, true);
		if (R != EPathFollowingRequestResult::Failed) return;
	}
	AddMovementInput((Destino - GetActorLocation()).GetSafeNormal2D(), 1.f);
}

void ANoMuerto::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	TiempoEstado += DeltaTime;
	AVaelithCharacter* J = Cast<AVaelithCharacter>(UGameplayStatics::GetPlayerPawn(this, 0));
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (!J || !GM || GM->Modo != EModoJuego::Juego || J->EnDespertar())
	{
		return;
	}
	// Tregua: mientras Vaelith no se puede controlar (recuerdo, escena que bloquea), nadie lo ataca.
	// Quien estaba por golpear se recupera, así al volver el control no pega en el primer cuadro.
	if (J->bControlBloqueado)
	{
		if (Estado == EEstadoNoMuerto::Amago || Estado == EEstadoNoMuerto::Golpe) Cambiar(EEstadoNoMuerto::Recuperacion);
		return;
	}
	const float Dist = FVector::Dist2D(J->GetActorLocation(), GetActorLocation());

	if (Estado == EEstadoNoMuerto::Muerto) return;
	if (Estado == EEstadoNoMuerto::Liberado)
	{
		AddActorWorldOffset(FVector(0.f, 0.f, 60.f * DeltaTime));
		Brillo->SetLightColor(FLinearColor(1.f, 0.85f, 0.55f));
		Brillo->SetIntensity(FMath::Max(0.f, 3000.f - TiempoEstado * 1000.f));
		SetActorScale3D(FVector(FMath::Max(0.05f, 1.f - TiempoEstado * 0.3f)));
		if (TiempoEstado > 3.2f) Destroy();
		return;
	}

	// Gemidos ocasionales: el jugador los oye antes de verlos (Sentir la muerte).
	CadenciaGemido -= DeltaTime;
	if (CadenciaGemido <= 0.f && Tipo != ETipoNoMuerto::Guardian && Dist < 1600.f)
	{
		CadenciaGemido = FMath::FRandRange(5.f, 11.f);
		Sonar(Tipo == ETipoNoMuerto::Fantasma ? TEXT("sfx_lamento") : TEXT("sfx_grunido"), 0.45f, Tipo == ETipoNoMuerto::Esqueleto ? 1.5f : 0.85f);
	}

	if (Tipo == ETipoNoMuerto::Guardian)
	{
		const FRotator Mirar = (J->GetActorLocation() - GetActorLocation()).Rotation();
		if (Dist < 600.f) SetActorRotation(FMath::RInterpTo(GetActorRotation(), FRotator(0.f, Mirar.Yaw, 0.f), DeltaTime, 1.5f));
		if (Dist < 500.f) GM->ReproducirEscena(TEXT("guardian"), true);
		return;
	}

	if (Tipo == ETipoNoMuerto::Sombra)
	{
		TickSombra(DeltaTime, J, Dist);
		return;
	}

	switch (Estado)
	{
	case EEstadoNoMuerto::Dormido:
		break;
	case EEstadoNoMuerto::Acecho:
		if (VeAlJugador(DistanciaVision))
		{
			Cambiar(EEstadoNoMuerto::Persecucion);
			if (!bAvisoSaber)
			{
				bAvisoSaber = true;
				const FString Clave = Tipo == ETipoNoMuerto::Zombi ? TEXT("zombi") : (Tipo == ETipoNoMuerto::Esqueleto ? TEXT("esqueleto") : TEXT("fantasma"));
				const FName H(*(TEXT("saber_") + Clave));
				if (!GM->HechoOcurrido(H))
				{
					GM->RegistrarHecho(H);
					GM->Aviso(TEXT("Saber del Osario · ") + NombreVisible().ToString(), GM->TextoGuion(TEXT("saber_") + Clave), 7.f);
				}
			}
		}
		break;
	case EEstadoNoMuerto::Persecucion:
		if (Dist <= AlcanceGolpe * 0.9f)
		{
			Cambiar(EEstadoNoMuerto::Amago);
		}
		else
		{
			MoverHacia(J->GetActorLocation(), DeltaTime);
			if (Dist > DistanciaVision * 2.f) Cambiar(EEstadoNoMuerto::Acecho);
		}
		break;
	case EEstadoNoMuerto::Amago:
	{
		const FRotator Mirar = (J->GetActorLocation() - GetActorLocation()).Rotation();
		SetActorRotation(FMath::RInterpTo(GetActorRotation(), FRotator(0.f, Mirar.Yaw, 0.f), DeltaTime, 6.f));
		if (TiempoEstado >= TiempoAmago) Cambiar(EEstadoNoMuerto::Golpe);
		break;
	}
	case EEstadoNoMuerto::Golpe:
	{
		const FVector Hacia = (J->GetActorLocation() - GetActorLocation()).GetSafeNormal2D();
		const bool bDelante = FVector::DotProduct(Hacia, GetActorForwardVector()) > 0.5f;
		if (Dist <= AlcanceGolpe && bDelante)
		{
			J->RecibirGolpe(FMath::RandRange(1, DanioDado) + DanioFijo, TipoGolpe, this);
		}
		else
		{
			Sonar(TEXT("sfx_tajo"), 0.5f, 0.8f);  // golpe al aire
		}
		Cambiar(EEstadoNoMuerto::Recuperacion);
		break;
	}
	case EEstadoNoMuerto::Recuperacion:
		if (TiempoEstado >= TiempoRecuperacion) Cambiar(EEstadoNoMuerto::Persecucion);
		break;
	case EEstadoNoMuerto::Aturdido:
		if (TiempoEstado >= DuracionAturdido) Cambiar(EEstadoNoMuerto::Persecucion);
		break;
	default:
		break;
	}
}

void ANoMuerto::TickSombra(float Dt, AVaelithCharacter* J, float Dist)
{
	const FRotator Mirar = (J->GetActorLocation() - GetActorLocation()).Rotation();
	SetActorRotation(FMath::RInterpTo(GetActorRotation(), FRotator(0.f, Mirar.Yaw, 0.f), Dt, 8.f));
	GetCharacterMovement()->bOrientRotationToMovement = false;

	switch (Estado)
	{
	case EEstadoNoMuerto::Dormido:
		break;  // la despierta el GameMode (IniciarJefe)
	case EEstadoNoMuerto::Acecho:
	case EEstadoNoMuerto::Persecucion:
	case EEstadoNoMuerto::Rodeo:
	{
		// Imita al jugador: si él carga un golpe, la Sombra levanta el escudo.
		const bool bJugadorAtaca = J->Ficha->FactorAtaqueMultiple() < 1.f || J->Ficha->Acciones < J->Ficha->AccionesMax - 1;
		Ficha->SetBloqueando(bJugadorAtaca && Dist < 300.f && FMath::Fmod(TiempoEstado, 2.f) < 1.2f);
		if (Dist > 260.f)
		{
			MoverHacia(J->GetActorLocation(), Dt);
		}
		else
		{
			// Rodea a distancia de espada, como haría un duelista.
			const FVector Lado = FVector::CrossProduct((J->GetActorLocation() - GetActorLocation()).GetSafeNormal2D(), FVector::UpVector);
			AddMovementInput(Lado * (FMath::Fmod(TiempoEstado, 6.f) < 3.f ? 1.f : -1.f), 0.6f);
			if (TiempoEstado > (bFase2 ? 0.9f : 1.6f))
			{
				Ficha->SetBloqueando(false);
				Cambiar(EEstadoNoMuerto::Amago);
			}
		}
		break;
	}
	case EEstadoNoMuerto::Amago:
		if (TiempoEstado >= (bFase2 ? TiempoAmago * 0.7f : TiempoAmago)) Cambiar(EEstadoNoMuerto::Golpe);
		break;
	case EEstadoNoMuerto::Golpe:
	{
		if (Dist <= AlcanceGolpe) J->RecibirGolpe(FMath::RandRange(1, DanioDado) + DanioFijo + (bFase2 ? 2 : 0), TipoGolpe, this);
		else Sonar(TEXT("sfx_tajo"), 0.6f, 0.9f);
		++GolpesSeguidos;
		// En la fase 2 encadena: alto y bajo, como Vaelith.
		if (bFase2 && GolpesSeguidos < 2) Cambiar(EEstadoNoMuerto::Amago);
		else { GolpesSeguidos = 0; Cambiar(EEstadoNoMuerto::Recuperacion); }
		break;
	}
	case EEstadoNoMuerto::Recuperacion:
		if (TiempoEstado >= (bFase2 ? TiempoRecuperacion * 0.7f : TiempoRecuperacion)) Cambiar(EEstadoNoMuerto::Rodeo);
		break;
	case EEstadoNoMuerto::Aturdido:
		Ficha->SetBloqueando(false);
		if (TiempoEstado >= DuracionAturdido) Cambiar(EEstadoNoMuerto::Rodeo);
		break;
	default:
		break;
	}
}

int32 ANoMuerto::RecibirAtaque(int32 Danio, ETipoDanio TipoDanio, bool bToque, float SegundosAturdir, FVector Empuje)
{
	if (!EstaVivo()) return 0;
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();

	if (Tipo == ETipoNoMuerto::Guardian && GM)
	{
		// Un centinela que no ataca: matarlo no es justicia.
		GM->SumarGracia(-1, TEXT("Heriste a quien no te atacó."));
		GM->ReproducirEscena(TEXT("guardian_herido"), true);
		Ficha->PG = 1;
		Danio = FMath::Max(Danio, 1);
	}

	const bool bBloqueaba = Ficha->bBloqueando;
	const int32 Perdido = Danio > 0 ? Ficha->RecibirDanio(Danio, TipoDanio, bToque) : 0;
	if (bBloqueaba && Tipo == ETipoNoMuerto::Sombra) Sonar(TEXT("sfx_bloqueo"), 1.f, 0.9f);
	if (Perdido > 0)
	{
		Sonar(Tipo == ETipoNoMuerto::Esqueleto ? TEXT("sfx_huesos") : TEXT("sfx_impacto_carne"), 0.9f);
	}
	if (!Empuje.IsNearlyZero()) LaunchCharacter(Empuje + FVector(0, 0, 80.f), true, false);
	if (SegundosAturdir > 0.f && Estado != EEstadoNoMuerto::Dormido) Aturdir(SegundosAturdir);

	if (Tipo == ETipoNoMuerto::Sombra && !bFase2 && Ficha->PG <= Ficha->PGMax() / 2 && GM)
	{
		bFase2 = true;
		Aturdir(1.2f);
		GM->ReproducirEscena(TEXT("sombra_mitad"), true);
		Brillo->SetIntensity(2500.f);
		GetCharacterMovement()->MaxWalkSpeed = VelocidadBase * 1.15f;
	}
	if (Ficha->bMuerto || Ficha->PG <= 0)
	{
		Morir();
	}
	else if (Estado == EEstadoNoMuerto::Acecho)
	{
		Cambiar(EEstadoNoMuerto::Persecucion);
	}
	return Perdido;
}

void ANoMuerto::Aturdir(float Segundos)
{
	if (!EstaVivo()) return;
	DuracionAturdido = Segundos;
	Cambiar(EEstadoNoMuerto::Aturdido);
	if (UAnimInstance* AI = GetMesh()->GetAnimInstance()) AI->StopAllMontages(0.1f);
}

void ANoMuerto::Liberar()
{
	if (!EstaVivo()) return;
	Cambiar(EEstadoNoMuerto::Liberado);
	GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>())
	{
		if (!Hecho.IsNone()) GM->RegistrarHecho(Hecho);
		GM->SumarGracia(1, TEXT("Un alma siguió su camino."));
		GM->ReproducirEscena(TEXT("alma_liberada"), false);
	}
	Sonar(TEXT("sfx_liberacion"), 1.f);
}

void ANoMuerto::Morir()
{
	Cambiar(EEstadoNoMuerto::Muerto);
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (GM && !Hecho.IsNone()) GM->RegistrarHecho(Hecho);
	GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	GetCharacterMovement()->DisableMovement();
	Brillo->SetIntensity(0.f);
	Sonar(Tipo == ETipoNoMuerto::Esqueleto ? TEXT("sfx_huesos") : TEXT("sfx_muerte_nomuerto"), 1.f, 0.9f);

	if (Tipo == ETipoNoMuerto::Fantasma)
	{
		SetLifeSpan(0.6f);
		return;
	}
	static const TCHAR* Muertes[] = {
		TEXT("/Game/Characters/Mannequins/Anims/Death/MM_Death_Front_01.MM_Death_Front_01"),
		TEXT("/Game/Characters/Mannequins/Anims/Death/MM_Death_Front_02.MM_Death_Front_02"),
		TEXT("/Game/Characters/Mannequins/Anims/Death/MM_Death_Back_01.MM_Death_Back_01") };
	if (UAnimSequenceBase* A = LoadObject<UAnimSequenceBase>(nullptr, Muertes[FMath::RandRange(0, 2)]))
	{
		GetMesh()->PlayAnimation(A, false);
	}
	if (Tipo == ETipoNoMuerto::Guardian && GM)
	{
		GM->SumarGracia(-2, TEXT("Mataste a un centinela que cumplía su guardia."));
		GM->ReproducirEscena(TEXT("guardian_muerto"), true);
	}
	if (Tipo == ETipoNoMuerto::Sombra && GM)
	{
		GM->JefeDerrotado(this);
	}
}
