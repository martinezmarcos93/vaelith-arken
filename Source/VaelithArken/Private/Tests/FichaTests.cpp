// Oráculo de la ficha PF2e. Correr: tools/ue/tests.sh
#include "FichaComponent.h"
#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

namespace
{
	UFichaComponent* NuevaFicha()
	{
		UFichaComponent* F = NewObject<UFichaComponent>();
		F->DescansarEnAltar();
		return F;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FFichaPG, "Vaelith.Ficha.PG", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FFichaPG::RunTest(const FString&)
{
	UFichaComponent* F = NuevaFicha();
	TestEqual(TEXT("Nivel 1: 8 humano + 10 campeón + 2 Con = 20"), F->PGMax(), 20);
	F->Nivel = 2;
	TestEqual(TEXT("Nivel 2 = 32"), F->PGMax(), 32);
	TestEqual(TEXT("Foco nivel 2 = 1"), F->FocoMax(), 1);
	F->Nivel = 3;
	TestEqual(TEXT("Foco nivel 3 = 2"), F->FocoMax(), 2);
	F->PGBaseFijos = 15;
	TestEqual(TEXT("PG fijos (enemigos)"), F->PGMax(), 15);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FFichaEscudo, "Vaelith.Ficha.Escudo", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FFichaEscudo::RunTest(const FString&)
{
	UFichaComponent* F = NuevaFicha();
	F->SetBloqueando(true);
	TestEqual(TEXT("12 bloqueado: pasan 7"), F->RecibirDanio(12, ETipoDanio::Cortante), 7);
	TestEqual(TEXT("Escudo 20-7 = 13"), F->PGEscudo, 13);
	TestEqual(TEXT("PG 20-7 = 13"), F->PG, 13);
	TestFalse(TEXT("13 > 10: todavía no está roto"), F->EscudoRoto());
	F->RecibirDanio(8, ETipoDanio::Cortante);  // pasan 3 -> escudo 10
	TestTrue(TEXT("Escudo en 10: roto"), F->EscudoRoto());
	TestEqual(TEXT("Roto: dureza 2, 6 -> pasan 4"), F->RecibirDanio(6, ETipoDanio::Cortante), 4);
	TestEqual(TEXT("4 golpes de 3 de dureza 2 bloqueados no matan"), F->bMuerto, false);
	F->SetBloqueando(false);
	TestEqual(TEXT("Sin bloquear: daño completo"), F->RecibirDanio(3, ETipoDanio::Cortante), 3);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FFichaDebilidades, "Vaelith.Ficha.Debilidades", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FFichaDebilidades::RunTest(const FString&)
{
	UFichaComponent* Esqueleto = NuevaFicha();
	Esqueleto->bTieneEscudo = false;
	Esqueleto->PGBaseFijos = 30;
	Esqueleto->Resistencias.Add(ETipoDanio::Cortante, 5);
	Esqueleto->Debilidades.Add(ETipoDanio::Contundente, 5);
	Esqueleto->DescansarEnAltar();
	TestEqual(TEXT("Esqueleto: tajo de 8 cortante -> 3"), Esqueleto->RecibirDanio(8, ETipoDanio::Cortante), 3);
	TestEqual(TEXT("Esqueleto: golpe de escudo de 6 contundente -> 11"), Esqueleto->RecibirDanio(6, ETipoDanio::Contundente), 11);

	UFichaComponent* Fantasma = NuevaFicha();
	Fantasma->bTieneEscudo = false;
	Fantasma->PGBaseFijos = 30;
	Fantasma->bInmaterial = true;
	Fantasma->Debilidades.Add(ETipoDanio::Vital, 5);
	Fantasma->DescansarEnAltar();
	TestEqual(TEXT("Fantasma: espada 10 -> 5"), Fantasma->RecibirDanio(10, ETipoDanio::Cortante), 5);
	TestEqual(TEXT("Fantasma: daga (toque fantasmal) 6 -> 6"), Fantasma->RecibirDanio(6, ETipoDanio::Perforante, true), 6);
	TestEqual(TEXT("Fantasma: Imponer las Manos 7 vital -> 12"), Fantasma->RecibirDanio(7, ETipoDanio::Vital), 12);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FFichaAcciones, "Vaelith.Ficha.Acciones", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FFichaAcciones::RunTest(const FString&)
{
	UFichaComponent* F = NuevaFicha();
	TestTrue(TEXT("Gasta 2 de 3"), F->GastarAcciones(2));
	TestFalse(TEXT("No alcanza para 2 más"), F->GastarAcciones(2));
	TestEqual(TEXT("Queda 1"), F->Acciones, 1);
	TestEqual(TEXT("1er ataque: 100 %"), F->RegistrarAtaque(10), 10);
	TestEqual(TEXT("2do ataque: 80 %"), F->RegistrarAtaque(10), 8);
	TestEqual(TEXT("3er ataque: 60 %"), F->RegistrarAtaque(10), 6);
	TestEqual(TEXT("4to ataque: sigue en 60 %"), F->RegistrarAtaque(10), 6);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FFichaDiehard, "Vaelith.Ficha.Diehard", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FFichaDiehard::RunTest(const FString&)
{
	// PF2e: Moribundo y Herido. Diehard: muere en Moribundo 5 (no 4). Puntos de Héroe: gastar todos evita la muerte.
	UFichaComponent* F = NuevaFicha();
	F->PuntosHeroe = 0;
	F->RecibirDanio(25, ETipoDanio::Vacio);
	TestTrue(TEXT("A 0 PG queda moribundo, no muerto"), F->bMoribundo && !F->bMuerto);
	TestEqual(TEXT("Moribundo 1"), F->Condicion(ECondicion::Moribundo), 1);
	TestFalse(TEXT("Moribundo no puede gastar acciones"), F->GastarAcciones(1));
	TestTrue(TEXT("Se levanta"), F->Levantarse());
	TestEqual(TEXT("Con 1 PG"), F->PG, 1);
	TestEqual(TEXT("Herido 1"), F->Condicion(ECondicion::Herido), 1);
	F->RecibirDanio(5, ETipoDanio::Vacio, false, true);
	TestEqual(TEXT("Crítico al caer con Herido 1: Moribundo 3"), F->Condicion(ECondicion::Moribundo), 3);
	F->RecibirDanio(2, ETipoDanio::Vacio);
	TestEqual(TEXT("Golpe estando moribundo: Moribundo 4"), F->Condicion(ECondicion::Moribundo), 4);
	TestFalse(TEXT("Diehard: en 4 todavía vive"), F->bMuerto);
	F->RecibirDanio(2, ETipoDanio::Vacio);
	TestTrue(TEXT("Moribundo 5: muere"), F->bMuerto);
	F->DescansarEnAltar();
	TestTrue(TEXT("El altar restaura todo y cura Herido"), !F->bMuerto && F->PG == 20 && F->PGEscudo == 20 && F->Foco == 1 && F->Condicion(ECondicion::Herido) == 0);
	F->PuntosHeroe = 2;
	F->RecibirDanio(25, ETipoDanio::Vacio, false, true);
	F->RecibirDanio(3, ETipoDanio::Vacio, false, true);
	F->RecibirDanio(3, ETipoDanio::Vacio);
	TestFalse(TEXT("Con Puntos de Héroe no muere"), F->bMuerto || F->bMoribundo);
	TestEqual(TEXT("Gastó todos"), F->PuntosHeroe, 0);
	TestEqual(TEXT("Vuelve con 1 PG"), F->PG, 1);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FFichaPlanilla, "Vaelith.Ficha.Planilla", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FFichaPlanilla::RunTest(const FString&)
{
	// Oráculo: la hoja de nivel 1 (Vaelith Arken - Nivel 1 (ES).pdf).
	UFichaComponent* F = NuevaFicha();
	TestEqual(TEXT("CA 21 (10 + Des 0 por armadura + experto 5 + armadura 6)"), F->CA(), 21);
	TestEqual(TEXT("Fortaleza +7"), F->Salvacion(ESalvacion::Fortaleza), 7);
	TestEqual(TEXT("Reflejos +6"), F->Salvacion(ESalvacion::Reflejos), 6);
	TestEqual(TEXT("Voluntad +7"), F->Salvacion(ESalvacion::Voluntad), 7);
	TestEqual(TEXT("Percepción +7"), F->Percepcion(), 7);
	TestEqual(TEXT("Golpe con espada +7"), F->Ataque(), 7);
	TestEqual(TEXT("CD de clase 17"), F->CDClase(), 17);
	TestEqual(TEXT("Atletismo entrenado: Fue 4 + 3 = +7"), F->Habilidad(EHabilidad::Atletismo), 7);
	TestEqual(TEXT("Saber del Osario: Int 0 + 3 = +3"), F->Habilidad(EHabilidad::SaberOsario), 3);
	TestEqual(TEXT("Diplomacia sin entrenar: Car +2"), F->Habilidad(EHabilidad::Diplomacia), 2);
	F->BonoMemoria = 2;
	TestEqual(TEXT("Memoria residual: +2 al Saber del Osario"), F->Habilidad(EHabilidad::SaberOsario), 5);
	F->SetBloqueando(true);
	TestEqual(TEXT("Escudo alzado: CA 23"), F->CA(), 23);
	F->SetBloqueando(false);
	F->SetCondicion(ECondicion::Asustado, 2);
	TestEqual(TEXT("Asustado 2: CA 19"), F->CA(), 19);
	TestEqual(TEXT("Asustado 2: Voluntad +5"), F->Salvacion(ESalvacion::Voluntad), 5);
	F->SetCondicion(ECondicion::Asustado, 0);
	F->SetCondicion(ECondicion::Desprevenido, 1);
	TestEqual(TEXT("Desprevenido: CA 19"), F->CA(), 19);
	F->Nivel = 5;
	TestEqual(TEXT("Nivel 5: golpe +11 (Fue 4 + entrenado 2 + nivel 5)"), F->Ataque(), 11);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPlanillaGrados, "Vaelith.Planilla.Grados", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FPlanillaGrados::RunTest(const FString&)
{
	TestEqual(TEXT("Igualar la CD: éxito"), Planilla::Grado(15, 15, 8), EGrado::Exito);
	TestEqual(TEXT("+10: crítico"), Planilla::Grado(25, 15, 12), EGrado::ExitoCritico);
	TestEqual(TEXT("−1: fallo"), Planilla::Grado(14, 15, 7), EGrado::Fallo);
	TestEqual(TEXT("−10: fallo crítico"), Planilla::Grado(5, 15, 3), EGrado::FalloCritico);
	TestEqual(TEXT("20 natural sube un grado"), Planilla::Grado(14, 15, 20), EGrado::Exito);
	TestEqual(TEXT("1 natural baja un grado"), Planilla::Grado(20, 15, 1), EGrado::Fallo);
	TestEqual(TEXT("Rango experto nivel 1 = 5"), Planilla::BonoRango(ERango::Experto, 1), 5);
	TestEqual(TEXT("Sin entrenar = 0"), Planilla::BonoRango(ERango::SinEntrenar, 5), 0);
	TestEqual(TEXT("CD nivel 3 = 18"), Planilla::CDPorNivel(3), 18);
	UFichaComponent* F = NuevaFicha();
	TestEqual(TEXT("Zombi +8 con 13 contra CA 21: éxito"), F->RecibirTiradaAtaque(8, 13), EGrado::Exito);
	TestEqual(TEXT("Zombi +8 con 12 contra CA 21: fallo"), F->RecibirTiradaAtaque(8, 12), EGrado::Fallo);
	TestEqual(TEXT("Zombi +8 con 20 natural: crítico"), F->RecibirTiradaAtaque(8, 20), EGrado::ExitoCritico);
	TestEqual(TEXT("Religión +5 con 10 contra CD 15: éxito"), F->Prueba(EHabilidad::Religion, 15, 10), EGrado::Exito);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FFichaFoco, "Vaelith.Ficha.Foco", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)
bool FFichaFoco::RunTest(const FString&)
{
	UFichaComponent* F = NuevaFicha();
	F->RecibirDanio(10, ETipoDanio::Vacio);
	TestTrue(TEXT("Gasta el foco"), F->GastarFoco());
	F->Curar(6);
	TestEqual(TEXT("Imponer las Manos cura 6"), F->PG, 16);
	TestFalse(TEXT("Sin foco"), F->GastarFoco());
	return true;
}

#endif
