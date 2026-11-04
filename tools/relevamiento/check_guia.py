"""Oráculo del encargo va-03: guía de dirección artística v2 completa y con hex reales."""
import re
import sys

t = open("docs/guia_estilo_visual.md", encoding="utf-8").read()
errores = []
if "## Dirección artística v2 (2026-11-04)" not in t:
    errores.append("falta la sección v2")
    print("\n".join(errores)); sys.exit(1)
previo, v2 = t.split("## Dirección artística v2 (2026-11-04)", 1)
for sub in ("Paleta por elemento", "Variación por zona", "Significado del violeta",
            "Capas de profundidad", "Escala de referencia", "Iluminación por fuente"):
    if f"### {sub}" not in v2:
        errores.append(f"falta ### {sub}")
if "### Paleta por elemento" in v2:
    tabla = v2.split("### Paleta por elemento", 1)[1].split("###", 1)[0]
    conocidos = {h.lower() for h in re.findall(r"#[0-9A-Fa-f]{6}", previo)}
    conocidos |= {h.lower() for h in re.findall(r"~?#[0-9A-Fa-f]{6}", previo)}
    for h in re.findall(r"#[0-9A-Fa-f]{6}", tabla):
        if h.lower() not in conocidos:
            errores.append(f"{h} de la tabla de paleta no existe en la guía previa")
if len(v2.splitlines()) > 200:
    errores.append(f"la sección v2 tiene {len(v2.splitlines())} líneas (máx. ~150)")
print("\n".join(errores) or "check_guia OK")
sys.exit(1 if errores else 0)
