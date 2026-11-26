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
	UFichaComponent* F = NuevaFicha();
	F->RecibirDanio(25, ETipoDanio::Vacio);
	TestTrue(TEXT("A 0 PG queda moribundo, no muerto"), F->bMoribundo && !F->bMuerto);
	TestFalse(TEXT("Moribundo no puede gastar acciones"), F->GastarAcciones(1));
	TestTrue(TEXT("Se levanta"), F->Levantarse());
	TestEqual(TEXT("Con 1 PG"), F->PG, 1);
	F->RecibirDanio(5, ETipoDanio::Vacio);
	TestTrue(TEXT("Diehard ya usado: muere"), F->bMuerto);
	F->DescansarEnAltar();
	TestTrue(TEXT("El altar restaura todo"), !F->bMuerto && F->PG == 20 && F->PGEscudo == 20 && F->Foco == 1);
	F->RecibirDanio(25, ETipoDanio::Vacio);
	F->RecibirDanio(1, ETipoDanio::Vacio);
	TestTrue(TEXT("Golpe estando moribundo: muere"), F->bMuerto);
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
