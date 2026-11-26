// La planilla de PF2e de Vaelith como sistema de juego. Diseño: docs/planilla-en-juego.md
// Reglas puras (sin mundo): competencias, grados de éxito y tablas. Se testean en Tests/PlanillaTests.cpp.
#pragma once

#include "CoreMinimal.h"
#include "Planilla.generated.h"

/** Rango de competencia de PF2e: sin entrenar (0), entrenado (+2), experto (+4), maestro (+6), legendario (+8), más el nivel. */
UENUM(BlueprintType)
enum class ERango : uint8
{
	SinEntrenar,
	Entrenado,
	Experto,
	Maestro,
	Legendario
};

UENUM(BlueprintType)
enum class EAtributo : uint8
{
	Fuerza,
	Destreza,
	Constitucion,
	Inteligencia,
	Sabiduria,
	Carisma
};

UENUM(BlueprintType)
enum class ESalvacion : uint8
{
	Fortaleza,
	Reflejos,
	Voluntad
};

/** Las habilidades de la hoja (página uno) más Percepción, que se usa igual que una prueba. */
UENUM(BlueprintType)
enum class EHabilidad : uint8
{
	Acrobacias,
	Arcanos,
	Atletismo,
	Artesania,
	Diplomacia,
	Engano,
	Intimidacion,
	Medicina,
	Naturaleza,
	Ocultismo,
	Interpretacion,
	Religion,
	Sociedad,
	Sigilo,
	Supervivencia,
	Robo,
	SaberOsario,
	Percepcion,
	Ninguna
};

/** Condiciones de PF2e que el juego usa en tiempo real. */
UENUM(BlueprintType)
enum class ECondicion : uint8
{
	Asustado,      // valor: −valor a todas las pruebas y a la CA; baja 1 por ronda
	Desprevenido,  // −2 a la CA (temporal)
	Debilitado,    // −valor a lo que usa Fuerza
	Aturdido,      // no actúa (temporal)
	Herido,        // al caer, Moribundo empieza más alto; se cura en el altar
	Moribundo      // al llegar a 4 (5 con Diehard), muere
};

UENUM(BlueprintType)
enum class EGrado : uint8
{
	FalloCritico,
	Fallo,
	Exito,
	ExitoCritico
};

namespace Planilla
{
	/** Bono de competencia: 0 sin entrenar; si no, 2/4/6/8 + nivel. */
	VAELITHARKEN_API int32 BonoRango(ERango Rango, int32 Nivel);
	/** Grado de éxito de PF2e: ±10 sobre la CD da crítico; un 20 natural sube un grado y un 1 natural baja uno. */
	VAELITHARKEN_API EGrado Grado(int32 Total, int32 CD, int32 Dado);
	VAELITHARKEN_API EAtributo AtributoDe(EHabilidad H);
	/** CD por nivel (tabla de PF2e): nivel 0 → 14, 1 → 15, 2 → 16, 3 → 18, 4 → 19, 5 → 20. */
	VAELITHARKEN_API int32 CDPorNivel(int32 Nivel);
	VAELITHARKEN_API FText Nombre(EHabilidad H);
	VAELITHARKEN_API FText Nombre(ERango R);
	VAELITHARKEN_API FText Nombre(ECondicion C);
	VAELITHARKEN_API FText Nombre(EGrado G);
	VAELITHARKEN_API FText Nombre(EAtributo A);
	/** Letra del rango como en la hoja: E, X, M, L (vacío sin entrenar). */
	VAELITHARKEN_API FString Letra(ERango R);
	/** Tira 1d20 (o usa Forzado si 1..20, para pruebas). */
	VAELITHARKEN_API int32 D20(int32 Forzado = 0);
}
