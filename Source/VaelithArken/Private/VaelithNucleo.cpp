#include "VaelithNucleo.h"
#include "Kismet/GameplayStatics.h"

const FString UVaelithGameInstance::Ranura = TEXT("VaelithArken");

bool UVaelithGameInstance::HayPartidaGuardada() const
{
	return UGameplayStatics::DoesSaveGameExist(Ranura, 0);
}
