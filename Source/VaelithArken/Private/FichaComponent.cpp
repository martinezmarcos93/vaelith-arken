#include "FichaComponent.h"

UFichaComponent::UFichaComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

int32 UFichaComponent::PGMax() const
{
	if (PGBaseFijos > 0)
	{
		return PGBaseFijos;
	}
	return PGAscendencia + (PGClasePorNivel + Atributos.Constitucion) * Nivel;
}

int32 UFichaComponent::FocoMax() const
{
	return (Nivel >= 3 ? 2 : 1) + FocoAdicional;
}

void UFichaComponent::BeginPlay()
{
	Super::BeginPlay();
	DescansarEnAltar();
}

void UFichaComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (bMuerto)
	{
		return;
	}
	if (bMoribundo)
	{
		TiempoMoribundo += DeltaTime;
		if (TiempoMoribundo >= SegundosMoribundo)
		{
			Morir();
		}
		return;
	}
	if (Acciones < AccionesMax)
	{
		AcumuladoAcciones += DeltaTime;
		if (AcumuladoAcciones >= SegundosPorAccion)
		{
			AcumuladoAcciones -= SegundosPorAccion;
			++Acciones;
			AlCambiarAcciones.Broadcast(Acciones, AccionesMax);
		}
	}
	else
	{
		AcumuladoAcciones = 0.f;
	}
}

float UFichaComponent::FactorAtaqueMultiple() const
{
	const UWorld* Mundo = GetWorld();
	const float Ahora = Mundo ? Mundo->GetTimeSeconds() : 0.f;
	int32 Recientes = 0;
	for (const float Marca : MarcasAtaque)
	{
		if (Ahora - Marca <= VentanaAtaqueMultiple)
		{
			++Recientes;
		}
	}
	return Recientes == 0 ? 1.f : (Recientes == 1 ? 0.8f : 0.6f);
}

bool UFichaComponent::GastarAcciones(int32 Cantidad)
{
	if (bMuerto || bMoribundo || Cantidad > Acciones)
	{
		return false;
	}
	Acciones -= Cantidad;
	AlCambiarAcciones.Broadcast(Acciones, AccionesMax);
	return true;
}

int32 UFichaComponent::RegistrarAtaque(int32 DanioBase)
{
	const float Factor = FactorAtaqueMultiple();
	const float Ahora = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f;
	MarcasAtaque.RemoveAll([&](float Marca) { return Ahora - Marca > VentanaAtaqueMultiple; });
	MarcasAtaque.Add(Ahora);
	return FMath::Max(1, FMath::RoundToInt(DanioBase * Factor));
}

void UFichaComponent::SetBloqueando(bool bNuevo)
{
	bBloqueando = bNuevo && !EscudoDestruido() && !bMoribundo && !bMuerto;
}

int32 UFichaComponent::RecibirDanio(int32 Cantidad, ETipoDanio Tipo, bool bToqueFantasmal)
{
	if (bMuerto || Cantidad <= 0)
	{
		return 0;
	}

	int32 Danio = Cantidad;
	const bool bFisico = Tipo == ETipoDanio::Cortante || Tipo == ETipoDanio::Perforante || Tipo == ETipoDanio::Contundente;
	if (bInmaterial && bFisico && !bToqueFantasmal)
	{
		Danio /= 2;
	}
	if (const int32* Deb = Debilidades.Find(Tipo))
	{
		Danio += *Deb;
	}
	if (const int32* Res = Resistencias.Find(Tipo))
	{
		Danio = FMath::Max(0, Danio - *Res);
	}

	// Bloqueo con escudo: la dureza absorbe; el resto lo reparten escudo y portador por igual.
	if (bBloqueando && !EscudoDestruido())
	{
		const int32 Dureza = EscudoRoto() ? 2 : DurezaEscudo;
		const int32 Pasa = FMath::Max(0, Danio - Dureza);
		const bool bEstabaEntero = !EscudoRoto();
		PGEscudo = FMath::Max(0, PGEscudo - Pasa);
		AlCambiarEscudo.Broadcast(PGEscudo, PGEscudoMax);
		if (bEstabaEntero && EscudoRoto())
		{
			AlRomperseEscudo.Broadcast();
		}
		if (EscudoDestruido())
		{
			bBloqueando = false;
		}
		Danio = Pasa;
	}

	if (bMoribundo)
	{
		Morir();  // cualquier golpe estando moribundo es mortal
		return Danio;
	}

	const int32 Antes = PG;
	PG = FMath::Max(0, PG - Danio);
	AlCambiarPG.Broadcast(PG, PGMax());
	if (PG == 0)
	{
		if (bTieneDiehard && bDiehardDisponible)
		{
			bMoribundo = true;
			TiempoMoribundo = 0.f;
			bBloqueando = false;
			AlQuedarMoribundo.Broadcast();
		}
		else
		{
			Morir();
		}
	}
	return Antes - PG;
}

void UFichaComponent::Curar(int32 Cantidad)
{
	if (bMuerto || Cantidad <= 0)
	{
		return;
	}
	if (bMoribundo)
	{
		Levantarse();
	}
	PG = FMath::Min(PGMax(), PG + Cantidad);
	AlCambiarPG.Broadcast(PG, PGMax());
}

bool UFichaComponent::GastarFoco()
{
	if (Foco <= 0 || bMuerto)
	{
		return false;
	}
	--Foco;
	AlCambiarFoco.Broadcast(Foco, FocoMax());
	return true;
}

bool UFichaComponent::Levantarse()
{
	if (!bMoribundo || bMuerto)
	{
		return false;
	}
	bMoribundo = false;
	bDiehardDisponible = false;
	PG = FMath::Max(PG, 1);
	AlCambiarPG.Broadcast(PG, PGMax());
	return true;
}

void UFichaComponent::DescansarEnAltar()
{
	bMuerto = false;
	bMoribundo = false;
	bDiehardDisponible = true;
	PG = PGMax();
	PGEscudo = bTieneEscudo ? PGEscudoMax : 0;
	Acciones = AccionesMax;
	Foco = FocoMax();
	MarcasAtaque.Reset();
	AvisarTodo();
}

void UFichaComponent::Morir()
{
	bMuerto = true;
	bMoribundo = false;
	bBloqueando = false;
	PG = 0;
	AlCambiarPG.Broadcast(PG, PGMax());
	AlMorir.Broadcast();
}

void UFichaComponent::AvisarTodo()
{
	AlCambiarPG.Broadcast(PG, PGMax());
	AlCambiarEscudo.Broadcast(PGEscudo, PGEscudoMax);
	AlCambiarAcciones.Broadcast(Acciones, AccionesMax);
	AlCambiarFoco.Broadcast(Foco, FocoMax());
}
