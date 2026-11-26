using UnrealBuildTool;

public class VaelithArkenEditorTarget : TargetRules
{
	public VaelithArkenEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("VaelithArken");
	}
}
