using UnrealBuildTool;

public class VaelithArken : ModuleRules
{
	public VaelithArken(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "EnhancedInput", "AIModule", "NavigationSystem", "Json", "SlateCore", "Slate", "UMG" });
	}
}
