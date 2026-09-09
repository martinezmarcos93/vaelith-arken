# tools/img_pipeline/

Pipeline **local y offline** para reparar y recolorear imágenes a la identidad
cromática del juego. No forma parte del juego: son utilidades de desarrollo que
producen PNGs para meter a mano en `assets/`.

Decidido y montado el 2026-09-09 (ver
`Documents/Claude-Vault/Roadmaps/roadmap_sesion_2026-09-09.md` y
`docs/analisis_herramientas_ia_pixel_art.md` §"Pipeline de reparación/recolor").

## Qué hay

| Archivo | Qué es |
|---|---|
| `recolor.py` | Recolorea una imagen (o carpeta) a `palette_canon.hex` — los 14 colores núcleo de `docs/guia_estilo_visual.md`. Envoltorio sobre **pyxelate**. `--dither`, `--extended`, `--factor`, `--no-accents`, `--check`. |
| `fix_ai.py` | Convierte "falso pixel art" (renders de IA, upscales, JPG) en pixel art real con grilla alineada. Envoltorio sobre **pixelfixer** (vendorizado). `--colors`, `--grid-from`, `--json`. |
| `palette_canon.hex` | Los 14 hex del núcleo. Fuente única: `docs/guia_estilo_visual.md` §1. |
| `palette_extended.hex` | Variantes de §1.1–1.2. Se suman con `--extended`. |
| `_compat.py` | Shim de `skimage.morphology.footprint_rectangle` para que pyxelate corra en Python 3.9. Importar **antes** que pyxelate. |
| `requirements.txt` | Dependencias del venv (pyxelate pineado por commit + deps). |
| `make_cert_bundle.ps1` | Regenera el bundle de certificados para el workaround SSL. |
| `vendor/pixel-art-fixer/` | Código de `pixelfixer` (Retro Diffusion, **MIT**). Vendorizado porque su `pyproject.toml` pide Python ≥3.10 sólo por metadata; el código corre en 3.9. Ver `UPSTREAM_COMMIT.txt`. |

No versionado (en `.gitignore`): `.venv/`, `.certs/`, `_samples/`.

## Montaje del entorno (PowerShell)

La red del estudio intercepta TLS (CA "Avast Web/Mail Shield Root") y `pip`/`git`
fallan con `CERTIFICATE_VERIFY_FAILED`. El workaround exporta las raíces de
Windows (que incluyen la de Avast) a un bundle PEM.

```powershell
# 1. bundle de certificados
powershell -ExecutionPolicy Bypass -File tools\img_pipeline\make_cert_bundle.ps1

# 2. venv con el Python 3.9 de miniconda (NO el 3.13 del sistema)
& "C:\tools\miniconda3\python.exe" -m venv tools\img_pipeline\.venv

# 3. deps, apuntando pip al bundle
$env:PIP_CERT       = "tools\img_pipeline\.certs\win-root-bundle.pem"
$env:GIT_SSL_CAINFO = $env:PIP_CERT
tools\img_pipeline\.venv\Scripts\python.exe -m pip install -r tools\img_pipeline\requirements.txt
```

## Uso

```powershell
$py = "tools\img_pipeline\.venv\Scripts\python.exe"

# Recolorear un pack de terceros a la paleta canónica, verificando el resultado
& $py tools\img_pipeline\recolor.py assets\sprites\tilesets\dungeon_golopin_free\ ^
      tools\img_pipeline\_samples\golopin_canon\ --check

# Con tramado y paleta extendida (para fondos/props, no para UI/personajes)
& $py tools\img_pipeline\recolor.py entrada.png salida.png --dither floyd --extended

# Reparar una referencia de IA a pixel art real, después pasarla por recolor
& $py tools\img_pipeline\fix_ai.py "ref_ia.png" tmp_fixed.png
& $py tools\img_pipeline\recolor.py tmp_fixed.png final.png --check
```

## Notas

- **Todo el pipeline es offline en ejecución** — los scripts no llaman a ninguna
  API. La única fase con red es instalar los paquetes.
- `recolor.py` preserva el canal alpha (lo binariza en 128 por defecto,
  `--alpha-threshold 0` lo deja tal cual).
- **Para tileset / fondo usar siempre `--no-accents`.** pyxelate mapea cada
  color de origen al más cercano de la paleta, y sin ese flag cualquier tono
  cálido del pack termina en el rojo de peligro `#B41F1C`, que `guia_estilo_visual.md`
  §1.2 reserva para amenazas activas. El flag lo quita de la paleta antes de
  cuantizar (el rojo-óxido ambiental `#4d1409` se conserva). Ejemplo real:
  `dungeon_golopin_free` sin el flag metía ~1776 px de rojo de peligro en la hoja.
- `fix_ai.py` informa `consensus`/`confidence` por archivo: `unanimous/high` es
  fiable, `arbitrated/low` conviene mirarlo a ojo. La detección tarda segundos a
  decenas de segundos por imagen grande.
- `vendor/pixel-art-fixer/pixelfixer/cli.py` tiene imports rotos (referencia el
  nombre viejo `detector`). No se usa: los envoltorios llaman a la API directo.
- Estas herramientas **no reemplazan** la decisión de `guia_estilo_visual.md` §6
  (los sprites animados se pixelan a mano en LibreSprite). Sirven para bajar
  packs de terceros a la paleta y para limpiar referencias, no para producir el
  sprite final desde cero.
