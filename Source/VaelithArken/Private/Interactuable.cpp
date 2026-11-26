#include "Interactuable.h"
#include "VaelithCharacter.h"
#include "VaelithGameMode.h"
#include "NoMuerto.h"
#include "Components/BoxComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "EngineUtils.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"

#define LOCTEXT_NAMESPACE "Vaelith"

namespace
{
	void Sonido(UObject* Ctx, const TCHAR* Nombre, float Vol = 1.f)
	{
		if (USoundBase* S = LoadObject<USoundBase>(nullptr, *FString::Printf(TEXT("/Game/Vaelith/Audio/%s.%s"), Nombre, Nombre)))
		{
			UGameplayStatics::PlaySound2D(Ctx, S, Vol);
		}
	}
}

AInteractuable::AInteractuable()
{
	PrimaryActorTick.bCanEverTick = true;
	Malla = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Malla"));
	RootComponent = Malla;
	Malla->SetCollisionProfileName(TEXT("BlockAll"));
	Luz = CreateDefaultSubobject<UPointLightComponent>(TEXT("Luz"));
	Luz->SetupAttachment(Malla);
	Luz->SetRelativeLocation(FVector(0.f, 0.f, 80.f));
	Luz->SetCastShadows(false);
	Luz->SetIntensityUnits(ELightUnits::Unitless);
	Luz->SetAttenuationRadius(500.f);
	Luz->SetIntensity(0.f);
}

void AInteractuable::BeginPlay()
{
	Super::BeginPlay();
	PosInicial = GetActorLocation();
	RotInicial = GetActorRotation();
	switch (Tipo)
	{
	case ETipoInteractuable::Altar:    Luz->SetLightColor(FLinearColor(1.f, 0.78f, 0.45f)); Luz->SetIntensity(900.f); Luz->SetAttenuationRadius(800.f); Luz->SetRelativeLocation(FVector(0.f, 0.f, 260.f)); break;
	case ETipoInteractuable::Recuerdo: Luz->SetLightColor(FLinearColor(0.85f, 0.85f, 1.f)); Luz->SetIntensity(1500.f); break;
	case ETipoInteractuable::Ancla:    Luz->SetLightColor(FLinearColor(0.4f, 0.6f, 1.f)); Luz->SetIntensity(1200.f); break;
	case ETipoInteractuable::Armas:
	case ETipoInteractuable::DagaPharasma: Luz->SetLightColor(FLinearColor(0.9f, 0.85f, 0.7f)); Luz->SetIntensity(800.f); Luz->SetAttenuationRadius(300.f); break;
	default: break;
	}
	if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>())
	{
		if (!Id.IsNone() && GM->HechoOcurrido(Id) && Tipo != ETipoInteractuable::Altar && Tipo != ETipoInteractuable::Lectura)
		{
			MarcarUsado(true);
		}
	}
}

void AInteractuable::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	if (Tipo == ETipoInteractuable::Recuerdo && !bUsado)
	{
		Luz->SetIntensity(1300.f + FMath::Sin(GetWorld()->GetTimeSeconds() * 2.2f) * 600.f);
	}
	if (Animacion >= 0.f)
	{
		Animacion += DeltaTime;
		const float T = FMath::SmoothStep(0.f, 1.f, FMath::Clamp(Animacion / 1.6f, 0.f, 1.f));
		if (Tipo == ETipoInteractuable::Puerta)
		{
			// Las rejas suben; las puertas de piedra se hunden.
			SetActorLocation(PosInicial + FVector(0.f, 0.f, 330.f * T));
		}
		else if (Tipo == ETipoInteractuable::Ancla)
		{
			SetActorLocation(PosInicial - FVector(0.f, 0.f, 60.f * T));
			Luz->SetIntensity(1200.f * (1.f - T));
		}
		if (T >= 1.f) Animacion = -1.f;
	}
}

bool AInteractuable::PuedeUsarse() const
{
	if (Tipo == ETipoInteractuable::Altar || Tipo == ETipoInteractuable::Lectura) return true;
	return !bUsado;
}

FText AInteractuable::TextoAccion() const
{
	if (!Etiqueta.IsEmpty()) return FText::FromString(TEXT("[E] ") + Etiqueta);
	switch (Tipo)
	{
	case ETipoInteractuable::Altar: return LOCTEXT("Altar", "[E] Rezar ante el altar de Pharasma");
	case ETipoInteractuable::Recuerdo: return LOCTEXT("Recuerdo", "[E] Tocar");
	case ETipoInteractuable::Ancla: return LOCTEXT("Ancla", "[E] Romper la cadena");
	case ETipoInteractuable::Armas: return LOCTEXT("Armas", "[E] Tomar la espada y el escudo");
	case ETipoInteractuable::DagaPharasma: return LOCTEXT("Daga", "[E] Tomar la daga");
	case ETipoInteractuable::Puerta: return LOCTEXT("Puerta", "[E] Abrir");
	case ETipoInteractuable::Cadaver: return LOCTEXT("Cadaver", "[E] Cubrir el cuerpo");
	case ETipoInteractuable::Lectura: return LOCTEXT("Lectura", "[E] Leer");
	case ETipoInteractuable::Espejo: return LOCTEXT("Espejo", "[E] Mirar el agua");
	}
	return FText::GetEmpty();
}

void AInteractuable::Usar(AVaelithCharacter* Quien)
{
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (!GM || !Quien) return;

	switch (Tipo)
	{
	case ETipoInteractuable::Altar:
		Quien->Ficha->DescansarEnAltar();
		Quien->AplicarDotes();
		Quien->Ficha->DescansarEnAltar();
		GM->Guardar(Id);
		Sonido(this, TEXT("sfx_altar"));
		GM->Aviso(TEXT("Altar de Pharasma"), GM->TextoGuion(TEXT("aviso_altar")), 4.f);
		if (!Escena.IsEmpty()) GM->ReproducirEscena(Escena, true);
		return;
	case ETipoInteractuable::Recuerdo:
		MarcarUsado(false);
		GM->RegistrarHecho(Id);
		GM->ActivarRecuerdo(Valor);
		return;
	case ETipoInteractuable::Ancla:
		for (TActorIterator<ANoMuerto> It(GetWorld()); It; ++It)
		{
			if (It->Ancla == this) It->Liberar();
		}
		Sonido(this, TEXT("sfx_cadena"));
		MarcarUsado(false);
		GM->RegistrarHecho(Id);
		return;
	case ETipoInteractuable::Armas:
		Quien->bTieneArmas = true;
		GM->Partida->bTieneArmas = true;
		Sonido(this, TEXT("sfx_desenvainar"));
		MarcarUsado(false);
		GM->RegistrarHecho(Id);
		break;
	case ETipoInteractuable::DagaPharasma:
		Quien->bTieneDaga = true;
		GM->Partida->bTieneDaga = true;
		Sonido(this, TEXT("sfx_desenvainar"), 0.7f);
		MarcarUsado(false);
		GM->RegistrarHecho(Id);
		GM->Aviso(TEXT("Daga de Pharasma"), GM->TextoGuion(TEXT("aviso_daga")), 7.f);
		break;
	case ETipoInteractuable::Puerta:
		if (!Requisito.IsNone() && !GM->HechoOcurrido(Requisito))
		{
			Sonido(this, TEXT("sfx_cerrado"));
			GM->ReproducirEscena(Escena.IsEmpty() ? TEXT("puerta_cerrada") : Escena, false);
			return;
		}
		Sonido(this, TEXT("sfx_reja"));
		MarcarUsado(false);
		GM->RegistrarHecho(Id);
		return;
	case ETipoInteractuable::Cadaver:
		GM->SumarGracia(1, TEXT("Le devolviste la dignidad a un muerto."));
		MarcarUsado(false);
		GM->RegistrarHecho(Id);
		break;
	case ETipoInteractuable::Lectura:
		GM->ReproducirEscena(Escena, false);
		return;
	case ETipoInteractuable::Espejo:
		MarcarUsado(false);
		GM->RegistrarHecho(Id);
		break;
	}
	if (!Escena.IsEmpty()) GM->ReproducirEscena(Escena, true);
}

void AInteractuable::MarcarUsado(bool bInstantaneo)
{
	bUsado = true;
	switch (Tipo)
	{
	case ETipoInteractuable::Puerta:
		if (bInstantaneo) SetActorLocation(GetActorLocation() + FVector(0.f, 0.f, 330.f));
		else Animacion = 0.f;
		break;
	case ETipoInteractuable::Ancla:
		if (bInstantaneo) { SetActorHiddenInGame(true); SetActorEnableCollision(false); }
		else Animacion = 0.f;
		break;
	case ETipoInteractuable::Armas:
	case ETipoInteractuable::DagaPharasma:
		SetActorHiddenInGame(true);
		SetActorEnableCollision(false);
		break;
	default:
		Luz->SetIntensity(0.f);
		break;
	}
}

// ---------------------------------------------------------------------------

ATriggerGuion::ATriggerGuion()
{
	Caja = CreateDefaultSubobject<UBoxComponent>(TEXT("Caja"));
	RootComponent = Caja;
	Caja->SetBoxExtent(FVector(200.f, 200.f, 200.f));
	Caja->SetCollisionProfileName(TEXT("Trigger"));
	Caja->OnComponentBeginOverlap.AddDynamic(this, &ATriggerGuion::AlEntrar);
}

void ATriggerGuion::AlEntrar(UPrimitiveComponent*, AActor* Otro, UPrimitiveComponent*, int32, bool, const FHitResult&)
{
	if (!Cast<AVaelithCharacter>(Otro)) return;
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (!GM || GM->Modo == EModoJuego::Menu) return;
	if (Penumbra >= 0.f || !Musica.IsEmpty()) GM->EntrarZona(Penumbra, Musica);
	if (!Escena.IsEmpty()) GM->ReproducirEscena(Escena, true);
	if (bJefe) GM->IniciarJefe();
}

#undef LOCTEXT_NAMESPACE
