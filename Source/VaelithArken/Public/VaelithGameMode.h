// Director: guion, partida, muerte y penitencia, recuerdos y dotes, jefe y final.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/PlayerController.h"
#include "VaelithNucleo.h"
#include "VaelithGameMode.generated.h"

class AVaelithCharacter;
class AInteractuable;
class ANoMuerto;
class UAudioComponent;

UCLASS()
class VAELITHARKEN_API AVaelithPlayerController : public APlayerController
{
	GENERATED_BODY()
public:
	AVaelithPlayerController();
};

UENUM()
enum class EModoJuego : uint8 { Menu, Juego, Pausa, EligiendoDote, Muerte, Creditos };

USTRUCT()
struct FLineaActiva
{
	GENERATED_BODY()
	FLineaGuion Linea;
	float Inicio = 0.f;
};

UCLASS()
class VAELITHARKEN_API AVaelithGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	AVaelithGameMode();

	EModoJuego Modo = EModoJuego::Juego;

	// ---- Guion ----
	/** Encola una escena del guion por clave. bUnaVez: no se repite (queda como hecho). */
	void ReproducirEscena(const FString& Clave, bool bUnaVez = true);
	bool HayEscenaEnCurso() const { return Cola.Num() > 0 || Activa.Linea.Texto.Len() > 0; }
	const FLineaActiva& LineaActiva() const { return Activa; }
	/** Pulsaciones ya consumidas (tecla -> segundo real). */
	/** true una sola vez por pulsación. WasInputKeyJustPressed sigue en true dos cuadros cuando la
	 *  pausa cambia el orden de actualización: Esc pausaba y despausaba en el cuadro siguiente. */
	bool TeclaNueva(APlayerController* PC, const FKey& K);
	float Ahora() const;
	FString TextoGuion(const FString& Clave) const;

	// ---- Partida ----
	UPROPERTY() UVaelithPartida* Partida = nullptr;
	void Guardar(FName Altar);
	bool HechoOcurrido(FName H) const;
	void RegistrarHecho(FName H);
	void SumarGracia(int32 N, const FString& Motivo);
	/** Tercer eje (Gracia, Memoria, Corrupción). */
	void SumarCorrupcion(int32 N);
	/** Romper el anatema: sin foco hasta expiar; señales de desagrado de Pharasma. */
	void RomperAnatema(const FString& Que);
	/** Final según los tres ejes: "guardian", "penitente" o "nigromante". */
	FString FinalPorEjes() const;
	int32 Memoria() const { return Partida ? Partida->Recuerdos.Num() : 0; }

	// ---- Recuerdos y nivel ----
	void ActivarRecuerdo(int32 Fragmento);
	void ElegirDote(int32 Opcion);  // 0 o 1
	EDote OpcionesDote[2] = { EDote::Ninguna, EDote::Ninguna };
	static FText NombreDote(EDote D);
	static FText DescripcionDote(EDote D);

	// ---- Muerte y penitencia ----
	void JugadorMurio();
	float FundidoNegro = 1.f;  // 0..1 (lo dibuja el HUD)
	float FundidoBlanco = 0.f;

	// ---- Zonas, jefe, final ----
	void EntrarZona(float Penumbra, const FString& Musica);
	void IniciarJefe();
	void JefeDerrotado(ANoMuerto* Sombra);
	UPROPERTY() ANoMuerto* Jefe = nullptr;
	float InicioCreditos = 0.f;

	// ---- Menú ----
	void MenuIniciar();
	void MenuContinuar();
	void MenuSalir();
	void Pausar(bool bPausa);
	void VolverAlMenu();

	/** Cartel breve arriba ("Saber del Osario", "Gracia", etc.). */
	void Aviso(const FString& Titulo, const FString& Texto, float Duracion = 5.f);
	FString AvisoTitulo, AvisoTexto;
	float AvisoFin = 0.f;
	/** Texto breve bajo la mira: grado de una prueba, "Crítico", "Esquivado". */
	void Destello(const FString& Texto, float Duracion = 1.6f) { DestelloTexto = Texto; DestelloFin = Ahora() + Duracion; }
	FString DestelloTexto;
	/** Un recuerdo que irrumpe sin escena propia (la tentación): la pantalla se lava unos segundos. */
	void DestelloRecuerdo(float Segundos) { FinDestelloRecuerdo = Ahora() + Segundos; }
	float FinDestelloRecuerdo = 0.f;
	float DestelloFin = 0.f;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	TMap<FString, TArray<FLineaGuion>> Guion;
	TMap<FString, FString> Textos;
	/** Escenas que bloquean el control mientras duran (las que nacen de una interacción). */
	TSet<FString> EscenasBloqueantes;
	bool bBloqueoPorEscena = false;
	TArray<FLineaGuion> Cola;
	FLineaActiva Activa;
	float EsperaLinea = 0.f;
	float TiempoMuerte = -1.f;
	float TiempoFinal = -1.f;
	int32 RecuerdoEnCurso = 0;
	FString MusicaActual;
	TArray<float> Capturas;
	bool bTeletransportado = false;
	bool bDiagHecho = false;
	bool bProbado = false;
	int32 UsadosPrueba = 0;
	int32 TeclasPrueba = 0;
	/** Pulsaciones ya consumidas (tecla -> segundo real). */
	TMap<FKey, double> TeclasConsumidas;


	UPROPERTY() UAudioComponent* Musica = nullptr;
	UPROPERTY() UAudioComponent* Ambiente = nullptr;

	void CargarGuion();
	void PrepararJuego(bool bContinuar);
	void PrepararMenu();
	AVaelithCharacter* Jugador() const;
	AInteractuable* BuscarAltar(FName Id) const;
	void Respawnear();
	void CambiarMusica(const FString& Ruta, float Volumen = 0.5f);
};
