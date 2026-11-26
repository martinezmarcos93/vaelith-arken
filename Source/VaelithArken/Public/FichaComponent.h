// Ficha de Pathfinder 2e llevada a tiempo real. Diseño: docs/sistemas.md
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Planilla.h"
#include "FichaComponent.generated.h"

UENUM(BlueprintType)
enum class ETipoDanio : uint8
{
	Cortante,
	Perforante,
	Contundente,
	Vital,     // energía de Pharasma: hiere a los no-muertos
	Vacio      // energía de no-muerte: hiere a los vivos
};

USTRUCT(BlueprintType)
struct FAtributosPF2e
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Fuerza = 4;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Destreza = 1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Constitucion = 2;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Inteligencia = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Sabiduria = 2;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Carisma = 2;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FAlCambiarValor, int32, Actual, int32, Maximo);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FAlEvento);
DECLARE_MULTICAST_DELEGATE(FAlEventoNativo);

UCLASS(ClassGroup=(Vaelith), meta=(BlueprintSpawnableComponent))
class VAELITHARKEN_API UFichaComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UFichaComponent();

	// ---- Ficha ----
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") FAtributosPF2e Atributos;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha", meta=(ClampMin=1, ClampMax=20)) int32 Nivel = 1;
	/** PG de ascendencia (humano 8) y por nivel de clase (campeón 10). Enemigos: PG fijos en PGBaseFijos. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") int32 PGAscendencia = 8;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") int32 PGClasePorNivel = 10;
	/** Si es > 0, ignora la fórmula de PF2e (útil para enemigos). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") int32 PGBaseFijos = 0;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Defensa") TMap<ETipoDanio, int32> Debilidades;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Defensa") TMap<ETipoDanio, int32> Resistencias;
	/** Inmaterial (fantasmas): mitad del daño físico salvo que el golpe sea "toque fantasmal". */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Defensa") bool bInmaterial = false;

	// ---- Competencias (hoja de nivel 1: CA 21, Fort +7, Ref +6, Vol +7, Percepción +7, golpes +7, CD de clase 17) ----
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") ERango RangoArmadura = ERango::Experto;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") ERango RangoFortaleza = ERango::Experto;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") ERango RangoReflejos = ERango::Experto;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") ERango RangoVoluntad = ERango::Experto;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") ERango RangoPercepcion = ERango::Experto;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") ERango RangoArmas = ERango::Entrenado;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") ERango RangoCDClase = ERango::Entrenado;
	/** Armadura completa: +6 de objeto, límite de Destreza +0. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") int32 ArmaduraObjeto = 6;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") int32 DesMaxArmadura = 0;
	/** Habilidades entrenadas (las demás, sin entrenar). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") TMap<EHabilidad, ERango> Habilidades;
	/** Regla de la casa (memoria residual): +1 al Saber del Osario por cada recuerdo recuperado. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") int32 BonoMemoria = 0;
	/** Enemigos: si es > 0, reemplaza el cálculo (bono de ataque y CA del bloque de PF2e). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") int32 AtaqueFijo = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") int32 CAFija = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Competencias") int32 VoluntadFija = 0;
	/** Sin mente (zombis, esqueletos): inmunes a Desmoralizar y al miedo. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Defensa") bool bSinMente = false;

	// ---- Puntos de Héroe = favor de Pharasma ----
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Heroe") int32 PuntosHeroe = 1;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha|Heroe") int32 PuntosHeroeMax = 3;
	/** Rompió el anatema: sin foco ni Imponer las Manos hasta expiar en un altar. */
	UPROPERTY(BlueprintReadOnly, Category="Ficha|Credo") bool bAnatema = false;

	// ---- Escudo (Bloqueo con escudo de PF2e) ----
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Escudo") bool bTieneEscudo = true;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Escudo") int32 DurezaEscudo = 5;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Escudo") int32 PGEscudoMax = 20;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Escudo") int32 UmbralRoturaEscudo = 10;

	// ---- Tres acciones ----
	/** Foco extra por dotes. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") int32 FocoAdicional = 0;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Acciones") int32 AccionesMax = 3;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Acciones") float SegundosPorAccion = 0.9f;
	/** Ventana en la que cuenta la penalización por ataque múltiple. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Acciones") float VentanaAtaqueMultiple = 1.5f;

	// ---- Estado (solo lectura) ----
	UPROPERTY(BlueprintReadOnly, Category="Estado") int32 PG = 0;
	UPROPERTY(BlueprintReadOnly, Category="Estado") int32 PGEscudo = 0;
	UPROPERTY(BlueprintReadOnly, Category="Estado") int32 Acciones = 3;
	UPROPERTY(BlueprintReadOnly, Category="Estado") int32 Foco = 1;
	UPROPERTY(BlueprintReadOnly, Category="Estado") bool bBloqueando = false;
	UPROPERTY(BlueprintReadOnly, Category="Estado") bool bMoribundo = false;
	UPROPERTY(BlueprintReadOnly, Category="Estado") bool bMuerto = false;
	UPROPERTY(BlueprintReadOnly, Category="Estado") TMap<ECondicion, int32> Condiciones;

	UPROPERTY(BlueprintAssignable) FAlCambiarValor AlCambiarPG;
	UPROPERTY(BlueprintAssignable) FAlCambiarValor AlCambiarEscudo;
	UPROPERTY(BlueprintAssignable) FAlCambiarValor AlCambiarAcciones;
	UPROPERTY(BlueprintAssignable) FAlCambiarValor AlCambiarFoco;
	UPROPERTY(BlueprintAssignable) FAlEvento AlQuedarMoribundo;
	UPROPERTY(BlueprintAssignable) FAlEvento AlMorir;
	UPROPERTY(BlueprintAssignable) FAlEvento AlRomperseEscudo;

	/** Se gastaron todos los Puntos de Héroe para evitar la muerte. */
	FAlEventoNativo AlSalvarseDeMorir;

	// ---- Consultas de la planilla ----
	int32 Mod(EAtributo A) const;
	/** CA = 10 + Des (hasta el límite) + competencia + armadura; +2 con el escudo levantado; −Asustado, −2 Desprevenido. */
	int32 CA() const;
	int32 Salvacion(ESalvacion S) const;
	int32 Percepcion() const;
	int32 CDClase() const;
	/** Bono de ataque con armas (Fuerza). */
	int32 Ataque() const;
	ERango RangoHabilidad(EHabilidad H) const;
	int32 Habilidad(EHabilidad H) const;
	/** Prueba contra una CD: d20 + modificador (Dado 1..20 lo fuerza, para tests). Devuelve el grado. */
	EGrado Prueba(EHabilidad H, int32 CD, int32 Dado = 0, int32* OutTotal = nullptr) const;
	EGrado TirarSalvacion(ESalvacion S, int32 CD, int32 Dado = 0) const;
	/** Un ataque de bono B contra esta ficha. */
	EGrado RecibirTiradaAtaque(int32 Bono, int32 Dado = 0, int32* OutTotal = nullptr) const;
	int32 Condicion(ECondicion C) const { const int32* V = Condiciones.Find(C); return V ? *V : 0; }
	/** Fija una condición; con Segundos > 0 desaparece sola (Desprevenido, Aturdido). */
	void SetCondicion(ECondicion C, int32 Valor, float Segundos = 0.f);
	void SubirCondicion(ECondicion C, int32 Cuanto = 1);
	int32 MuerteEn() const { return bTieneDiehard ? 5 : 4; }
	void GanarPuntoHeroe(int32 N = 1) { PuntosHeroe = FMath::Clamp(PuntosHeroe + N, 0, PuntosHeroeMax); }
	/** Romper el anatema: pierde el foco hasta la expiación. */
	void RomperAnatema() { bAnatema = true; Foco = 0; AvisarTodo(); }
	void Expiar() { bAnatema = false; }

	// ---- Consultas ----
	UFUNCTION(BlueprintPure, Category="Ficha") int32 PGMax() const;
	UFUNCTION(BlueprintPure, Category="Ficha") int32 FocoMax() const;
	UFUNCTION(BlueprintPure, Category="Escudo") bool EscudoRoto() const { return bTieneEscudo && PGEscudo <= UmbralRoturaEscudo; }
	UFUNCTION(BlueprintPure, Category="Escudo") bool EscudoDestruido() const { return !bTieneEscudo || PGEscudo <= 0; }
	/** 1.0 / 0.8 / 0.6 según cuántos ataques se hicieron dentro de la ventana. */
	UFUNCTION(BlueprintPure, Category="Acciones") float FactorAtaqueMultiple() const;

	// ---- Acciones ----
	/** Intenta gastar acciones; false si no alcanzan. */
	UFUNCTION(BlueprintCallable, Category="Acciones") bool GastarAcciones(int32 Cantidad);
	/** Registra un ataque (para la penalización por ataque múltiple) y devuelve el daño ya multiplicado. */
	UFUNCTION(BlueprintCallable, Category="Acciones") int32 RegistrarAtaque(int32 DanioBase);
	UFUNCTION(BlueprintCallable, Category="Escudo") void SetBloqueando(bool bNuevo);

	/**
	 * Aplica daño con debilidades, resistencias, inmaterialidad y escudo.
	 * Devuelve los PG que efectivamente perdió el portador.
	 */
	UFUNCTION(BlueprintCallable, Category="Ficha") int32 RecibirDanio(int32 Cantidad, ETipoDanio Tipo, bool bToqueFantasmal = false, bool bCritico = false);
	UFUNCTION(BlueprintCallable, Category="Ficha") void Curar(int32 Cantidad);
	/** Imponer las Manos: cura 6 o, si se usa sobre un no-muerto, devuelve true y el llamador aplica 2d6 vital. */
	UFUNCTION(BlueprintCallable, Category="Foco") bool GastarFoco();
	/** Levantarse del estado Moribundo con 1 PG: Herido sube 1 (regla de PF2e; reemplaza "una vez por altar"). */
	UFUNCTION(BlueprintCallable, Category="Ficha") bool Levantarse();
	/** Altar de Pharasma: restaura todo. */
	UFUNCTION(BlueprintCallable, Category="Ficha") void DescansarEnAltar();

	/** Una ronda de PF2e en tiempo real: Moribundo empeora 1 por ronda; Asustado baja 1. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") float SegundosRonda = 2.5f;
	/** Compatibilidad: duración aproximada del estado Moribundo con Herido 0 y Diehard (4 rondas). */
	float SegundosMoribundo = 10.f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Ficha") bool bTieneDiehard = true;

protected:
	virtual void BeginPlay() override;
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
	float AcumuladoAcciones = 0.f;
	float TiempoMoribundo = 0.f;
	float TiempoRonda = 0.f;
	TMap<ECondicion, float> VenceCondicion;
	TArray<float> MarcasAtaque;

	void Morir();
	/** Al llegar a Moribundo MuerteEn(): si quedan Puntos de Héroe, se gastan todos y no muere. */
	void ComprobarMuerte();
	float Ahora() const;
public:
	void AvisarTodo();
};
