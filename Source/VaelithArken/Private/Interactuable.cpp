#include "Interactuable.h"
#include "VaelithCharacter.h"
#include "VaelithGameMode.h"
#include "NoMuerto.h"
#include "FichaComponent.h"
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
	if (Levantado >= 0.f)
	{
		// Se incorpora (0–1,2 s), queda de pie mientras la reja sube y se desploma (2,6–3,2 s).
		Levantado += DeltaTime;
		const float Sube = FMath::SmoothStep(0.f, 1.2f, Levantado) * (1.f - FMath::SmoothStep(2.6f, 3.2f, Levantado));
		SetActorLocation(PosInicial + FVector(0.f, 0.f, 70.f * Sube));
		SetActorRotation(RotInicial + FRotator(0.f, 0.f, 80.f * Sube));
		if (Levantado > 3.3f) Levantado = -1.f;
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
	if (Opciones.Num() > 0) return !bUsado && OpcionesVisibles().Num() > 0;
	if (Tipo == ETipoInteractuable::Altar || Tipo == ETipoInteractuable::Lectura) return true;
	return !bUsado;
}

TArray<int32> AInteractuable::OpcionesVisibles() const
{
	TArray<int32> R;
	const AVaelithGameMode* GM = GetWorld() ? GetWorld()->GetAuthGameMode<AVaelithGameMode>() : nullptr;
	for (int32 i = 0; i < Opciones.Num(); ++i)
	{
		const FOpcionInteraccion& O = Opciones[i];
		if (Agotadas.Contains(i)) continue;
		if (GM && !O.Requisito.IsNone() && !GM->HechoOcurrido(O.Requisito)) continue;
		if (GM && GM->HechoOcurrido(HechoOpcion(i))) continue;  // ya lograda (las no terminales, una vez)
		R.Add(i);
	}
	return R;
}

void AInteractuable::CambiarSeleccion(int32 Paso)
{
	const TArray<int32> V = OpcionesVisibles();
	if (V.Num() == 0) return;
	int32 Pos = FMath::Max(0, V.IndexOfByKey(Seleccion));
	Pos = (Pos + Paso + V.Num()) % V.Num();
	Seleccion = V[Pos];
}

FString AInteractuable::TextoOpciones(const UFichaComponent* Ficha) const
{
	const TArray<int32> V = OpcionesVisibles();
	if (V.Num() == 0) return FString();
	const int32 Sel = V.Contains(Seleccion) ? Seleccion : V[0];
	FString R;
	for (const int32 i : V)
	{
		const FOpcionInteraccion& O = Opciones[i];
		FString L = (i == Sel ? TEXT("[E] ") : TEXT("      ")) + O.Etiqueta;
		if (O.Habilidad != EHabilidad::Ninguna && Ficha)
		{
			const int32 M = Ficha->Habilidad(O.Habilidad);
			L += FString::Printf(TEXT("  ·  %s %s%d"), *Planilla::Nombre(O.Habilidad).ToString(), M >= 0 ? TEXT("+") : TEXT(""), M);
		}
		if (O.bAnatema) L += TEXT("  ·  anatema");
		if (!R.IsEmpty()) R += TEXT("|");
		R += L;
	}
	if (V.Num() > 1) R += TEXT("|(rueda del ratón: elegir)");
	return R;
}

void AInteractuable::AbrirDesdeAfuera()
{
	if (bUsado) return;
	if (AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>()) GM->RegistrarHecho(Id);
	Sonido(this, TEXT("sfx_reja"));
	MarcarUsado(false);
}

void AInteractuable::UsarOpcion(AVaelithCharacter* Quien, int32 Indice)
{
	AVaelithGameMode* GM = GetWorld()->GetAuthGameMode<AVaelithGameMode>();
	if (!GM || !Quien || !Opciones.IsValidIndex(Indice)) return;
	const FOpcionInteraccion O = Opciones[Indice];

	// Prueba de habilidad (d20 oculto). Pharasma narra; en pantalla solo el grado.
	EGrado G = EGrado::Exito;
	if (O.Habilidad != EHabilidad::Ninguna)
	{
		int32 Total = 0;
		G = Quien->Ficha->Prueba(O.Habilidad, O.CD, 0, &Total);
		if (G == EGrado::FalloCritico && Quien->Ficha->PuntosHeroe > 0)
		{
			// Favor de Pharasma: un Punto de Héroe repite la tirada y evita cerrar la vía.
			--Quien->Ficha->PuntosHeroe;
			G = Quien->Ficha->Prueba(O.Habilidad, O.CD, 0, &Total);
			GM->Aviso(TEXT("Favor de Pharasma"), TEXT("Gastaste un punto de favor: volvés a intentarlo."), 3.5f);
		}
		UE_LOG(LogTemp, Log, TEXT("[vaelith] prueba %s total=%d CD=%d grado=%d"), *Planilla::Nombre(O.Habilidad).ToString(), Total, O.CD, int32(G));
		GM->Destello(FString::Printf(TEXT("%s: %s"), *Planilla::Nombre(O.Habilidad).ToString(), *Planilla::Nombre(G).ToString()));
	}
	const bool bLogra = G == EGrado::Exito || G == EGrado::ExitoCritico;
	if (!bLogra)
	{
		if (!O.EscenaFallo.IsEmpty()) GM->ReproducirEscena(O.EscenaFallo, false);
		if (G == EGrado::FalloCritico) Agotadas.Add(Indice);  // esa vía se cerró
		Sonido(this, TEXT("sfx_cerrado"), 0.7f);
		return;
	}
	const FString EscenaLograda = (G == EGrado::ExitoCritico && !O.EscenaCritico.IsEmpty()) ? O.EscenaCritico : O.EscenaExito;
	GM->RegistrarHecho(HechoOpcion(Indice));
	switch (O.Efecto)
	{
	case EEfectoOpcion::Abrir:
	case EEfectoOpcion::Levantar:
	{
		AInteractuable* Puerta = this;
		if (!O.Objetivo.IsNone())
		{
			for (TActorIterator<AInteractuable> It(GetWorld()); It; ++It)
			{
				if (It->Id == O.Objetivo) { Puerta = *It; break; }
			}
		}
		if (Puerta == this) { GM->RegistrarHecho(Id); Sonido(this, TEXT("sfx_reja")); MarcarUsado(false); }
		else Puerta->AbrirDesdeAfuera();
		if (O.Efecto == EEfectoOpcion::Levantar)
		{
			Levantado = 0.f;
			GM->DestelloRecuerdo(2.8f);
			if (USoundBase* Snd = LoadObject<USoundBase>(nullptr, TEXT("/Game/Vaelith/Audio/sfx_recuerdo.sfx_recuerdo"))) UGameplayStatics::PlaySound2D(this, Snd, 0.8f, 0.7f);
		}
		break;
	}
	case EEfectoOpcion::Relevar:
		for (TActorIterator<ANoMuerto> It(GetWorld()); It; ++It)
		{
			if (It->Hecho == O.Objetivo) It->Relevar();
		}
		break;
	case EEfectoOpcion::Tomar:
		Quien->DarObjeto(O.Objeto, 1);
		break;
	case EEfectoOpcion::DarDescanso:
		Sonido(this, TEXT("sfx_liberacion"), 0.6f);
		break;
	default:
		break;
	}
	if (O.bAnatema) GM->RomperAnatema(O.Etiqueta);
	if (O.Gracia != 0) GM->SumarGracia(O.Gracia, O.Gracia > 0 ? TEXT("Hiciste lo que te toca.") : TEXT("Pharasma lo anotó."));
	if (O.Corrupcion != 0) GM->SumarCorrupcion(O.Corrupcion);
	if (!EscenaLograda.IsEmpty()) GM->ReproducirEscena(EscenaLograda, false);
	if (O.bTerminal && !bUsado)
	{
		// Objeto resuelto (cadáver, sello): sus opciones desaparecen. Una puerta propia ya quedó abierta arriba.
		GM->RegistrarHecho(Id);
		bUsado = true;
		Luz->SetIntensity(0.f);
	}
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
	if (Opciones.Num() > 0)
	{
		const TArray<int32> V = OpcionesVisibles();
		if (V.Num() > 0) UsarOpcion(Quien, V.Contains(Seleccion) ? Seleccion : V[0]);
		return;
	}

	switch (Tipo)
	{
	case ETipoInteractuable::Altar:
		if (Quien->Ficha->bAnatema)
		{
			// Expiación: rezar ante su altar después de romper el anatema devuelve el foco. La Corrupción no se borra.
			Quien->Ficha->Expiar();
			GM->ReproducirEscena(TEXT("expiacion"), false);
		}
		Quien->bTratoHeridasDisponible = true;
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
	if (!Escena.IsEmpty() && Prueba != EHabilidad::Ninguna)
	{
		// Eco de la muerte: un intento por eco; si no lo percibe, se pierde (no se avisa).
		const FName Intento(*(TEXT("eco_") + Escena));
		if (GM->HechoOcurrido(Intento)) return;
		GM->RegistrarHecho(Intento);
		AVaelithCharacter* J = Cast<AVaelithCharacter>(Otro);
		const EGrado G = J->Ficha->Prueba(Prueba, CD);
		UE_LOG(LogTemp, Log, TEXT("[vaelith] eco %s: %s"), *Escena, *Planilla::Nombre(G).ToString());
		if (G == EGrado::Exito || G == EGrado::ExitoCritico)
		{
			Sonido(this, TEXT("sfx_recuerdo"), 0.45f);
			GM->ReproducirEscena(Escena, true);
		}
		return;
	}
	if (!Escena.IsEmpty()) GM->ReproducirEscena(Escena, true);
	if (bJefe) GM->IniciarJefe();
}

#undef LOCTEXT_NAMESPACE
