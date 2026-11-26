#include "Planilla.h"

#define LOCTEXT_NAMESPACE "Planilla"

namespace Planilla
{
	int32 BonoRango(ERango Rango, int32 Nivel)
	{
		switch (Rango)
		{
		case ERango::Entrenado:  return 2 + Nivel;
		case ERango::Experto:    return 4 + Nivel;
		case ERango::Maestro:    return 6 + Nivel;
		case ERango::Legendario: return 8 + Nivel;
		default:                 return 0;
		}
	}

	EGrado Grado(int32 Total, int32 CD, int32 Dado)
	{
		int32 G = Total >= CD + 10 ? 3 : (Total >= CD ? 2 : (Total <= CD - 10 ? 0 : 1));
		if (Dado == 20) G = FMath::Min(3, G + 1);
		else if (Dado == 1) G = FMath::Max(0, G - 1);
		return static_cast<EGrado>(G);
	}

	EAtributo AtributoDe(EHabilidad H)
	{
		switch (H)
		{
		case EHabilidad::Acrobacias:
		case EHabilidad::Sigilo:
		case EHabilidad::Robo:          return EAtributo::Destreza;
		case EHabilidad::Atletismo:     return EAtributo::Fuerza;
		case EHabilidad::Arcanos:
		case EHabilidad::Artesania:
		case EHabilidad::Ocultismo:
		case EHabilidad::Sociedad:
		case EHabilidad::SaberOsario:   return EAtributo::Inteligencia;
		case EHabilidad::Medicina:
		case EHabilidad::Naturaleza:
		case EHabilidad::Religion:
		case EHabilidad::Supervivencia:
		case EHabilidad::Percepcion:    return EAtributo::Sabiduria;
		default:                        return EAtributo::Carisma;  // Diplomacia, Engaño, Intimidación, Interpretación
		}
	}

	int32 CDPorNivel(int32 Nivel)
	{
		static const int32 Tabla[] = { 14, 15, 16, 18, 19, 20, 22, 23, 24, 26, 27 };
		return Tabla[FMath::Clamp(Nivel, 0, 10)];
	}

	FText Nombre(EHabilidad H)
	{
		switch (H)
		{
		case EHabilidad::Acrobacias:     return LOCTEXT("Acro", "Acrobacias");
		case EHabilidad::Arcanos:        return LOCTEXT("Arca", "Arcanos");
		case EHabilidad::Atletismo:      return LOCTEXT("Atle", "Atletismo");
		case EHabilidad::Artesania:      return LOCTEXT("Arte", "Artesanía");
		case EHabilidad::Diplomacia:     return LOCTEXT("Dipl", "Diplomacia");
		case EHabilidad::Engano:         return LOCTEXT("Enga", "Engaño");
		case EHabilidad::Intimidacion:   return LOCTEXT("Inti", "Intimidación");
		case EHabilidad::Medicina:       return LOCTEXT("Medi", "Medicina");
		case EHabilidad::Naturaleza:     return LOCTEXT("Natu", "Naturaleza");
		case EHabilidad::Ocultismo:      return LOCTEXT("Ocul", "Ocultismo");
		case EHabilidad::Interpretacion: return LOCTEXT("Inte", "Interpretación");
		case EHabilidad::Religion:       return LOCTEXT("Reli", "Religión");
		case EHabilidad::Sociedad:       return LOCTEXT("Soci", "Sociedad");
		case EHabilidad::Sigilo:         return LOCTEXT("Sigi", "Sigilo");
		case EHabilidad::Supervivencia:  return LOCTEXT("Supe", "Supervivencia");
		case EHabilidad::Robo:           return LOCTEXT("Robo", "Robo");
		case EHabilidad::SaberOsario:    return LOCTEXT("Sabe", "Saber del Osario");
		case EHabilidad::Percepcion:     return LOCTEXT("Perc", "Percepción");
		default:                         return FText::GetEmpty();
		}
	}

	FText Nombre(ERango R)
	{
		switch (R)
		{
		case ERango::Entrenado:  return LOCTEXT("RE", "Entrenado");
		case ERango::Experto:    return LOCTEXT("RX", "Experto");
		case ERango::Maestro:    return LOCTEXT("RM", "Maestro");
		case ERango::Legendario: return LOCTEXT("RL", "Legendario");
		default:                 return LOCTEXT("RS", "Sin entrenar");
		}
	}

	FText Nombre(ECondicion C)
	{
		switch (C)
		{
		case ECondicion::Asustado:     return LOCTEXT("CAs", "Asustado");
		case ECondicion::Desprevenido: return LOCTEXT("CDe", "Desprevenido");
		case ECondicion::Debilitado:   return LOCTEXT("CDb", "Debilitado");
		case ECondicion::Aturdido:     return LOCTEXT("CAt", "Aturdido");
		case ECondicion::Herido:       return LOCTEXT("CHe", "Herido");
		default:                       return LOCTEXT("CMo", "Moribundo");
		}
	}

	FText Nombre(EGrado G)
	{
		switch (G)
		{
		case EGrado::FalloCritico: return LOCTEXT("GFC", "Fallo crítico");
		case EGrado::Fallo:        return LOCTEXT("GF", "Fallo");
		case EGrado::Exito:        return LOCTEXT("GE", "Éxito");
		default:                   return LOCTEXT("GEC", "Éxito crítico");
		}
	}

	FText Nombre(EAtributo A)
	{
		switch (A)
		{
		case EAtributo::Fuerza:       return LOCTEXT("AFue", "Fuerza");
		case EAtributo::Destreza:     return LOCTEXT("ADes", "Destreza");
		case EAtributo::Constitucion: return LOCTEXT("ACon", "Constitución");
		case EAtributo::Inteligencia: return LOCTEXT("AInt", "Inteligencia");
		case EAtributo::Sabiduria:    return LOCTEXT("ASab", "Sabiduría");
		default:                      return LOCTEXT("ACar", "Carisma");
		}
	}

	FString Letra(ERango R)
	{
		switch (R)
		{
		case ERango::Entrenado:  return TEXT("E");
		case ERango::Experto:    return TEXT("X");
		case ERango::Maestro:    return TEXT("M");
		case ERango::Legendario: return TEXT("L");
		default:                 return TEXT("");
		}
	}

	int32 D20(int32 Forzado)
	{
		return (Forzado >= 1 && Forzado <= 20) ? Forzado : FMath::RandRange(1, 20);
	}
}

#undef LOCTEXT_NAMESPACE
