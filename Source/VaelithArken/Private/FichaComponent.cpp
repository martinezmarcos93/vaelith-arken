#include "FichaComponent.h"

UFichaComponent::UFichaComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	// Campeón de Pharasma (Religión + Medicina por la deidad), trasfondo Retornado (Saber del Osario), Atletismo e Intimidación.
	Habilidades.Add(EHabilidad::Atletismo, ERango::Entrenado);
	Habilidades.Add(EHabilidad::Religion, ERango::Entrenado);
	Habilidades.Add(EHabilidad::Medicina, ERango::Entrenado);
	Habilidades.Add(EHabilidad::Intimidacion, ERango::Entrenado);
	Habilidades.Add(EHabilidad::SaberOsario, ERango::Entrenado);
}

float UFichaComponent::Ahora() const
{
	const UWorld* Mundo = GetWorld();
	return Mundo ? Mundo->GetTimeSeconds() : 0.f;
}

int32 UFichaComponent::Mod(EAtributo A) const
{
	switch (A)
	{
	case EAtributo::Fuerza:       return Atributos.Fuerza;
	case EAtributo::Destreza:     return Atributos.Destreza;
	case EAtributo::Constitucion: return Atributos.Constitucion;
	case EAtributo::Inteligencia: return Atributos.Inteligencia;
	case EAtributo::Sabiduria:    return Atributos.Sabiduria;
	default:                      return Atributos.Carisma;
	}
}

int32 UFichaComponent::CA() const
{
	int32 Valor = CAFija > 0 ? CAFija
		: 10 + FMath::Min(Atributos.Destreza, DesMaxArmadura) + Planilla::BonoRango(RangoArmadura, Nivel) + ArmaduraObjeto;
	if (bBloqueando && !EscudoDestruido()) Valor += 2;  // Alzar el escudo
	Valor -= Condicion(ECondicion::Asustado);
	if (Condicion(ECondicion::Desprevenido) > 0) Valor -= 2;
	return Valor;
}

int32 UFichaComponent::Salvacion(ESalvacion S) const
{
	if (S == ESalvacion::Voluntad && VoluntadFija > 0) return VoluntadFija - Condicion(ECondicion::Asustado);
	int32 Base = 0;
	switch (S)
	{
	case ESalvacion::Fortaleza: Base = Atributos.Constitucion + Planilla::BonoRango(RangoFortaleza, Nivel); break;
	case ESalvacion::Reflejos:  Base = Atributos.Destreza + Planilla::BonoRango(RangoReflejos, Nivel); break;
	default:                    Base = Atributos.Sabiduria + Planilla::BonoRango(RangoVoluntad, Nivel); break;
	}
	return Base - Condicion(ECondicion::Asustado);
}

int32 UFichaComponent::Percepcion() const
{
	return Atributos.Sabiduria + Planilla::BonoRango(RangoPercepcion, Nivel) - Condicion(ECondicion::Asustado);
}

int32 UFichaComponent::CDClase() const
{
	return 10 + Atributos.Fuerza + Planilla::BonoRango(RangoCDClase, Nivel);
}

int32 UFichaComponent::Ataque() const
{
	if (AtaqueFijo > 0) return AtaqueFijo - Condicion(ECondicion::Asustado) - Condicion(ECondicion::Debilitado);
	return Atributos.Fuerza + Planilla::BonoRango(RangoArmas, Nivel) - Condicion(ECondicion::Asustado) - Condicion(ECondicion::Debilitado);
}

ERango UFichaComponent::RangoHabilidad(EHabilidad H) const
{
	if (H == EHabilidad::Percepcion) return RangoPercepcion;
	const ERango* R = Habilidades.Find(H);
	return R ? *R : ERango::SinEntrenar;
}

int32 UFichaComponent::Habilidad(EHabilidad H) const
{
	if (H == EHabilidad::Percepcion) return Percepcion();
	int32 V = Mod(Planilla::AtributoDe(H)) + Planilla::BonoRango(RangoHabilidad(H), Nivel) - Condicion(ECondicion::Asustado);
	if (H == EHabilidad::SaberOsario) V += BonoMemoria;
	if (Planilla::AtributoDe(H) == EAtributo::Fuerza) V -= Condicion(ECondicion::Debilitado);
	return V;
}

EGrado UFichaComponent::Prueba(EHabilidad H, int32 CD, int32 Dado, int32* OutTotal) const
{
	const int32 D = Planilla::D20(Dado);
	const int32 Total = D + Habilidad(H);
	if (OutTotal) *OutTotal = Total;
	return Planilla::Grado(Total, CD, D);
}

EGrado UFichaComponent::TirarSalvacion(ESalvacion S, int32 CD, int32 Dado) const
{
	const int32 D = Planilla::D20(Dado);
	return Planilla::Grado(D + Salvacion(S), CD, D);
}

EGrado UFichaComponent::RecibirTiradaAtaque(int32 Bono, int32 Dado, int32* OutTotal) const
{
	const int32 D = Planilla::D20(Dado);
	if (OutTotal) *OutTotal = D + Bono;
	return Planilla::Grado(D + Bono, CA(), D);
}

void UFichaComponent::SetCondicion(ECondicion C, int32 Valor, float Segundos)
{
	if (Valor <= 0)
	{
		Condiciones.Remove(C);
		VenceCondicion.Remove(C);
		return;
	}
	Condiciones.Add(C, Valor);
	if (Segundos > 0.f) VenceCondicion.Add(C, Ahora() + Segundos);
	else VenceCondicion.Remove(C);
}

void UFichaComponent::SubirCondicion(ECondicion C, int32 Cuanto)
{
	SetCondicion(C, Condicion(C) + Cuanto);
}

void UFichaComponent::ComprobarMuerte()
{
	if (Condicion(ECondicion::Moribundo) < MuerteEn()) return;
	if (PuntosHeroe > 0)
	{
		// "Gastá todos para evitar la muerte": Pharasma lo devuelve. Herido no cambia.
		PuntosHeroe = 0;
		bMoribundo = false;
		SetCondicion(ECondicion::Moribundo, 0);
		PG = 1;
		AlCambiarPG.Broadcast(PG, PGMax());
		AlSalvarseDeMorir.Broadcast();
		return;
	}
	Morir();
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
	// Condiciones temporales y rondas
	const float T = Ahora();
	for (auto It = VenceCondicion.CreateIterator(); It; ++It)
	{
		if (T >= It.Value())
		{
			Condiciones.Remove(It.Key());
			It.RemoveCurrent();
		}
	}
	TiempoRonda += DeltaTime;
	const bool bRonda = TiempoRonda >= SegundosRonda;
	if (bRonda)
	{
		TiempoRonda = 0.f;
		if (Condicion(ECondicion::Asustado) > 0) SetCondicion(ECondicion::Asustado, Condicion(ECondicion::Asustado) - 1);
	}
	if (bMoribundo)
	{
		// Moribundo empeora 1 por ronda (sin tirada de recuperación: el tiempo real ya presiona).
		TiempoMoribundo += DeltaTime;
		if (bRonda)
		{
			SubirCondicion(ECondicion::Moribundo);
			ComprobarMuerte();
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

int32 UFichaComponent::RecibirDanio(int32 Cantidad, ETipoDanio Tipo, bool bToqueFantasmal, bool bCritico)
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
		// PF2e: recibir daño estando Moribundo lo sube 1 (2 si es crítico).
		if (Danio > 0)
		{
			SubirCondicion(ECondicion::Moribundo, bCritico ? 2 : 1);
			ComprobarMuerte();
		}
		return Danio;
	}

	const int32 Antes = PG;
	PG = FMath::Max(0, PG - Danio);
	AlCambiarPG.Broadcast(PG, PGMax());
	if (PG == 0)
	{
		if (PGBaseFijos > 0)
		{
			Morir();  // los enemigos no quedan moribundos
		}
		else
		{
			// PF2e: al caer, Moribundo 1 (2 si fue crítico) más el valor de Herido.
			bMoribundo = true;
			TiempoMoribundo = 0.f;
			TiempoRonda = 0.f;
			bBloqueando = false;
			SetCondicion(ECondicion::Moribundo, (bCritico ? 2 : 1) + Condicion(ECondicion::Herido));
			AlQuedarMoribundo.Broadcast();
			ComprobarMuerte();
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
	if (Foco <= 0 || bMuerto || bAnatema)
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
	SetCondicion(ECondicion::Moribundo, 0);
	SubirCondicion(ECondicion::Herido);
	PG = FMath::Max(PG, 1);
	AlCambiarPG.Broadcast(PG, PGMax());
	return true;
}

void UFichaComponent::DescansarEnAltar()
{
	bMuerto = false;
	bMoribundo = false;
	Condiciones.Reset();
	VenceCondicion.Reset();
	PG = PGMax();
	PGEscudo = bTieneEscudo ? PGEscudoMax : 0;
	Acciones = AccionesMax;
	Foco = bAnatema ? 0 : FocoMax();
	MarcasAtaque.Reset();
	AvisarTodo();
}

void UFichaComponent::Morir()
{
	bMuerto = true;
	bMoribundo = false;
	bBloqueando = false;
	SetCondicion(ECondicion::Moribundo, 0);
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
