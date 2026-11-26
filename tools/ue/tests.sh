#!/usr/bin/env bash
# Compila el módulo y corre los tests "Vaelith.*" sin interfaz. Sale con 1 si falla alguno.
set -uo pipefail
R="$(cd "$(dirname "$0")/../.." && pwd)"; UE=~/Aplicaciones/UE_5.8
pgrep -x UnrealEditor >/dev/null && { echo "cerrá el editor primero (bloquea la compilación)"; exit 1; }
"$UE/Engine/Build/BatchFiles/Linux/Build.sh" VaelithArkenEditor Linux Development -Project="$R/VaelithArken.uproject" -WaitMutex > "$UE/_logs/build.log" 2>&1 \
  || { grep -E 'error|Error' "$UE/_logs/build.log" | head -20; exit 1; }
LOG="$UE/_logs/tests.log"
"$UE/Engine/Binaries/Linux/UnrealEditor-Cmd" "$R/VaelithArken.uproject" -nullrhi -unattended -nosplash -stdout \
  -ExecCmds="Automation RunTests Vaelith; Quit" > "$LOG" 2>&1
grep -E "Test Completed\. Result=|Error: .*Expected|LogAutomationController: Error" "$LOG" | sed 's/^\[[^]]*\]\[[^]]*\]//' | grep -v 'Condition failed'
OK=$(grep -c "Result={Success}" "$LOG"); MAL=$(grep -c "Result={Fail" "$LOG")
echo "tests: $OK ok, $MAL fallidos"
[ "$MAL" = 0 ] && [ "$OK" -gt 0 ]
