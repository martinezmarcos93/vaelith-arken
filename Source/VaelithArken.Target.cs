using UnrealBuildTool;

public class VaelithArkenTarget : TargetRules
{
	public VaelithArkenTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("VaelithArken");
	}
}
