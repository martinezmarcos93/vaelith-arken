#include "Instancias.h"
#include "Components/HierarchicalInstancedStaticMeshComponent.h"

AInstancias::AInstancias()
{
	PrimaryActorTick.bCanEverTick = false;
	RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Raiz"));
	RootComponent->SetMobility(EComponentMobility::Static);
}

void AInstancias::OnConstruction(const FTransform& Transform)
{
	Super::OnConstruction(Transform);
	Armar();
}

void AInstancias::BeginPlay()
{
	Super::BeginPlay();
	if (Componentes.Num() == 0) Armar();
}

void AInstancias::Armar()
{
	for (UHierarchicalInstancedStaticMeshComponent* C : Componentes)
	{
		if (C) C->DestroyComponent();
	}
	Componentes.Reset();
	for (const FGrupoInstancias& G : Grupos)
	{
		if (!G.Malla || G.Transformadas.Num() == 0) continue;
		UHierarchicalInstancedStaticMeshComponent* C = NewObject<UHierarchicalInstancedStaticMeshComponent>(this, NAME_None, RF_Transient);
		C->SetMobility(EComponentMobility::Static);
		C->SetupAttachment(RootComponent);
		C->SetStaticMesh(G.Malla);
		C->SetCastShadow(G.bSombra);
		C->SetCollisionEnabled(G.bColision ? ECollisionEnabled::QueryAndPhysics : ECollisionEnabled::NoCollision);
		if (G.Distancia > 0.f) C->SetCullDistances(FMath::RoundToInt(G.Distancia * 0.8f), FMath::RoundToInt(G.Distancia));
		C->RegisterComponent();
		C->AddInstances(G.Transformadas, false, true);
		Componentes.Add(C);
	}
}
