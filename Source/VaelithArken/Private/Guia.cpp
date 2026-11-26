#include "Guia.h"
#include "VaelithCharacter.h"
#include "VaelithGameMode.h"
#include "Components/PointLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"

AEstatuaGuia::AEstatuaGuia()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.TickInterval = 0.05f;
	Base = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Base"));
	RootComponent = Base;
	Estatua = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Estatua"));
	Estatua->SetupAttachment(Base);
	Estatua->SetRelativeLocation(FVector(0.f, 0.f, 59.f));
	Farol = CreateDefaultSubobject<UPointLightComponent>(TEXT("Farol"));
	Farol->SetupAttachment(Base);
	Farol->SetRelativeLocation(FVector(0.f, 0.f, 200.f));
	Farol->SetIntensityUnits(ELightUnits::Unitless);
	Farol->SetLightColor(FLinearColor(1.f, 0.6f, 0.28f));
	Farol->SetAttenuationRadius(1300.f);
	Farol->SetCastShadows(false);
	Farol->SetIntensity(0.f);
	if (UStaticMesh* B = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Vaelith/Ext/cementerio/SM_Estatua_Base.SM_Estatua_Base"))) Base->SetStaticMesh(B);
	if (UStaticMesh* E = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Vaelith/Ext/cementerio/SM_Estatua_Pharasma.SM_Estatua_Pharasma"))) Estatua->SetStaticMesh(E);
}

void AEstatuaGuia::BeginPlay()
{
	Super::BeginPlay();
	Fase = FMath::FRand() * 10.f;
	if (bEncendidaAlInicio)
	{
		bEncendida = true;
		Brillo = 1.f;
	}
}

void AEstatuaGuia::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	if (!bEncendida)
	{
		const APawn* P = UGameplayStatics::GetPlayerPawn(this, 0);
		if (P && FVector::Dist2D(P->GetActorLocation(), GetActorLocation()) < Radio)
		{
			bEncendida = true;
			if (USoundBase* S = LoadObject<USoundBase>(nullptr, TEXT("/Game/Vaelith/Audio/sfx_altar.sfx_altar")))
			{
				UGameplayStatics::PlaySoundAtLocation(this, S, Farol->GetComponentLocation(), 0.6f, 0.7f);
			}
			if (!Escena.IsEmpty())
			{
				if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->ReproducirEscena(Escena, true);
			}
		}
	}
	if (bEncendida)
	{
		Brillo = FMath::FInterpTo(Brillo, 1.f, DeltaTime, 0.8f);
		Fase += DeltaTime;
		const float Parpadeo = 0.85f + 0.1f * FMath::Sin(Fase * 9.f) + 0.05f * FMath::Sin(Fase * 23.f);
		Farol->SetIntensity(2400.f * Brillo * Parpadeo);
	}
}

ADestelloTorre::ADestelloTorre()
{
	PrimaryActorTick.bCanEverTick = true;
	Luz = CreateDefaultSubobject<UPointLightComponent>(TEXT("Luz"));
	RootComponent = Luz;
	Luz->SetIntensityUnits(ELightUnits::Unitless);
	Luz->SetLightColor(FLinearColor(0.55f, 0.3f, 1.f));
	Luz->SetAttenuationRadius(4500.f);
	Luz->SetCastShadows(false);
	Luz->SetIntensity(0.f);
}

void ADestelloTorre::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	T += DeltaTime;
	// Pulso: sube y baja en 1,4 s, después oscuridad hasta el próximo período.
	const float Ciclo = FMath::Fmod(T, Periodo);
	const float Pulso = Ciclo < 1.4f ? FMath::Sin(Ciclo / 1.4f * PI) : 0.f;
	Luz->SetIntensity(IntensidadMax * (0.06f + 0.94f * Pulso * Pulso));

	AVaelithCharacter* C = Cast<AVaelithCharacter>(UGameplayStatics::GetPlayerPawn(this, 0));
	if (!C) return;
	const FVector A = C->GetActorLocation();
	if (A.Y < YMinimaLlamado || FVector::Dist2D(A, GetActorLocation()) > RadioLlamado) return;
	FVector Hacia = GetActorLocation() - A;
	Hacia.Z = 0.f;
	const float Alineado = FVector::DotProduct(C->GetControlRotation().Vector().GetSafeNormal2D(), Hacia.GetSafeNormal());
	// El bosque oscuro apaga la Penumbra; mirar hacia la torre la enciende.
	C->PenumbraObjetivo = 0.6f + 0.4f * FMath::Clamp((Alineado - 0.55f) / 0.45f, 0.f, 1.f);
}
