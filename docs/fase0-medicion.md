# Fase 0 — Medición en la GTX 1060 3 GB

Fecha: 2026-11-25. Script: `tools/ue/medir.sh`. Modo juego (no editor), 1360x768
(resolución del monitor), sin VSync ni límite de FPS. Se descartan los primeros 600
frames (carga y shaders) y se promedian los siguientes 900.

Render del proyecto: sin Lumen (GI = ninguna), reflejos SSR, sin sombras virtuales,
sin Nanite, sin campos de distancia, luz estática permitida, TAA, Vulkan SM5.

| Nivel | FPS medio | FPS 1 % bajo | CPU (hilo de juego) | GPU | VRAM máx. |
|---|---|---|---|---|---|
| Plantilla First Person | 93,5 | 48,8 | 3,3 ms | 10,2 ms | 808 MiB |
| Bosque, 50 árboles | 201,0 | 120,2 | 3,0 ms | 4,2 ms | 931 MiB |
| Bosque, 300 árboles | 184,9 | 109,1 | 3,0 ms | 4,7 ms | 908 MiB |

Bosque de prueba: suelo de 200 x 200 m, luna dinámica con sombras en cascada, luz de
cielo, niebla exponencial. Árboles de 560 a 880 triángulos como **actores sueltos**
(peor caso: sin instanciado). Captura: `Saved/Screenshots/LinuxEditor/HighresScreenshot00000.png`.

## Conclusión

- **El bosque no es el cuello de botella** (era la duda del Ministro Dragón): 300
  árboles cuestan 0,5 ms más de GPU que 50. Hay margen para un bosque denso, con
  árboles reales de Quaternius e instanciado (HISM/PCG), que es todavía más barato.
- La VRAM queda en ~0,9 GB de 3 GB: hay espacio para texturas de 1–2K.
- La plantilla (con su mapa y materiales de demostración) cuesta más GPU que el
  bosque: lo caro son las luces dinámicas y los materiales, no la geometría. Regla:
  pocas luces dinámicas, antorchas con luz estática o estacionaria.
- Margen de sobra para 60 FPS: se puede subir la calidad (sombras, postproceso) si
  hace falta, sin activar Lumen.
