# VAELITH ARKEN — BRIEF DE IMPLEMENTACIÓN

> Documento maestro de producción. Fuente de verdad para llevar el prototipo a
> vertical slice. Redactado por Marcos (2026-08-27). El diagnóstico del estado
> actual y el plan por fases están en [`AUDITORIA_2026-08-27.md`](AUDITORIA_2026-08-27.md).
> La fuente de verdad narrativa es [`guion_demo.md`](guion_demo.md).

## 1. OBJETIVO

Convertir el prototipo actual de Vaelith Arken en una vertical slice jugable de alta calidad.

El objetivo inmediato NO es crear más contenido ni generar nuevos assets.

El objetivo es utilizar y organizar los assets ya existentes y llevar a producción las mecánicas, narrativa, escenarios, enemigos, memoria y boss ya definidos.

No generar assets nuevos salvo que durante la implementación aparezca una necesidad concreta que no pueda resolverse con los assets existentes.

---

## 2. IDENTIDAD DEL JUEGO

Vaelith Arken es un plataformas de acción 2D dark fantasy.

Referencias principales:

- SLAIN
- Volgarr the Viking
- Dark Souls
- Bloodborne
- Castlevania
- Diablo

El protagonista es Vaelith Arken, un elfo drow resucitado.

Vaelith murió y fue devuelto a la vida para reparar las consecuencias de su pasado.

Antes de morir fue un poderoso practicante de la necromancia.

Muchas de las criaturas no muertas que encuentra durante el juego existen como consecuencia directa de sus actos.

Vaelith perdió sus recuerdos conscientes, pero conserva conocimientos procedurales.

Su cuerpo sabe hacer cosas que su mente no recuerda.

La historia se descubre progresivamente mediante:

- exploración;
- interacción;
- combate;
- elementos ambientales;
- fragmentos de memoria;
- comportamiento de los enemigos;
- diálogos.

---

## 3. PRINCIPIO FUNDAMENTAL

LORE Y GAMEPLAY DEBEN ESTAR INTEGRADOS.

No queremos:

"nivel de plataformas + enemigos + diálogos que cuentan la historia".

Queremos:

"el jugador realiza acciones que también le permiten descubrir quién era Vaelith".

Ejemplos:

- Vaelith reconoce mecanismos que él mismo construyó.
- Puede interactuar con cadáveres.
- Puede liberar espíritus.
- Puede utilizar mecanismos necrománticos.
- Reconoce símbolos que no recuerda haber aprendido.
- Los engendros pueden reaccionar ante él.
- Los fragmentos de memoria aparecen como consecuencia de determinadas interacciones.

---

## 4. ESTRUCTURA DE LA DEMO

La demo tiene:

```
INTRO
  ↓
LEVEL 1
  ↓
GUERRERO-ESPEJO
  ↓
RECUERDO FINAL
  ↓
FIN DE DEMO
```

No agregar inventario complejo, mapa mundial, crafting complejo, múltiples armas ni sistemas RPG que no sean necesarios para esta vertical slice.

---

## 5. INTRO

La intro debe mostrar a Vaelith despertando.

Debe enseñar:

- movimiento;
- salto;
- interacción básica;
- armas;
- primera anomalía de memoria.

El jugador empieza sin conocer la historia.

No explicar mediante exposición quién era Vaelith.

La información debe aparecer gradualmente.

La intro debe utilizar el guion actualizado del proyecto como fuente de verdad narrativa.

NO reemplazar el guion por diálogos nuevos.

---

## 6. MEMORIA

Los fragmentos de memoria son uno de los sistemas narrativos principales.

Un fragmento encontrado durante el juego desbloquea un recuerdo.

Los recuerdos NO deben ser simples textos informativos.

Deben sentirse como escenas breves, traumáticas y fragmentarias.

Regla:

Vaelith no recupera una biografía.

Recupera momentos.

Los recuerdos deben revelar progresivamente:

1. Vaelith creó criaturas.
2. Esas criaturas tenían voluntad.
3. Vaelith las utilizaba y controlaba.
4. Vaelith creó un constructo especial.
5. El constructo recibió parte de su personalidad.
6. El constructo conserva recuerdos que Vaelith perdió.

---

## 7. LEVEL 1

El Level 1 no debe ser simplemente:

caminar → matar → poción → palanca → matar → boss.

Debe funcionar como una arqueología del pasado de Vaelith.

El escenario debe contener:

- ruinas;
- cadáveres;
- símbolos;
- mecanismos;
- restos de experimentos;
- engendros;
- espíritus;
- fragmentos de memoria;
- elementos que sugieran que Vaelith estuvo allí anteriormente.

El jugador debe comenzar pensando:

"¿Dónde estoy?"

Luego:

"¿Por qué reconozco estas cosas?"

Luego:

"¿Qué relación tengo con estos muertos?"

Finalmente:

"Yo hice esto."

---

## 8. MECÁNICAS

Mantener el combate actual y hacerlo sólido antes de agregar sistemas nuevos.

Vaelith utiliza:

- espada;
- daga;
- escudo;
- ataque alto;
- ataque bajo;
- bloqueo;
- shove;
- movimiento;
- salto.

El combate debe ser deliberado y pesado.

No convertirlo en un hack & slash rápido.

---

## 9. INTERACCIÓN CON EL ENTORNO

Implementar progresivamente objetos interactivos reutilizables.

### Cadáveres

Un cadáver puede:

- ser decoración;
- activar una memoria;
- contener un espíritu;
- convertirse en enemigo;
- revelar información mediante interacción.

### Espíritus

Algunos espíritus no son enemigos.

El jugador puede liberarlos.

La liberación puede producir:

- fragmento de memoria;
- acceso;
- recompensa;
- cambio ambiental.

No implementar todavía un sistema moral complejo.

### Mecanismos

Palancas, ruedas, puertas y mecanismos deben sentirse como parte del antiguo complejo necromántico.

Cuando sea apropiado, Vaelith puede reconocer automáticamente cómo utilizarlos.

### Engendros

No todos deben atacar inmediatamente.

Algunos pueden:

- observar a Vaelith;
- reconocerlo;
- huir;
- reaccionar antes de combatir.

Esto debe reforzar la sensación de que el protagonista está regresando a un lugar donde sus creaciones todavía lo recuerdan.

---

## 10. PLATAFORMAS

El plataformeo debe utilizar:

- desniveles;
- plataformas;
- pequeños saltos;
- plataformas colapsables si ya existen;
- obstáculos;
- espacios estrechos;
- mecanismos que modifican el recorrido.

No agregar doble salto, dash, wall jump, grappling hook ni otras habilidades nuevas salvo que sean necesarias y se decidan explícitamente después.

---

## 11. PENITENCIA

La muerte de Vaelith no debe sentirse como un simple Game Over.

Mantener el sistema de corrupción/penitencia existente.

La muerte debe tener consecuencias dentro del mundo cuando corresponda.

No implementar sistemas nuevos de penitencia hasta comprobar primero que el sistema actual funciona correctamente.

---

## 12. BOSS — GUERRERO ESPEJO

El boss final de la demo es el Guerrero-Espejo.

No es un simple clon.

Es un constructo creado por Vaelith.

Vaelith le dio parte de su propia personalidad.

El constructo conserva:

- conocimientos;
- patrones de combate;
- recuerdos;
- personalidad.

Por eso reconoce inmediatamente la forma de luchar de Vaelith.

El combate debe reflejar al jugador.

El boss debe utilizar versiones de:

- ataque alto;
- ataque bajo;
- bloqueo;
- shove;
- fintas;
- desplazamientos.

Durante el combate debe reconocer comportamientos del jugador.

El diálogo del boss debe utilizar el guion actualizado.

No inventar una nueva historia paralela.

---

## 13. REVELACIÓN DEL BOSS

La revelación importante es:

EL GUERRERO-ESPEJO NO ES VAELITH.

ES UNA CREACIÓN DE VAELITH.

Pero posee una parte de aquello que Vaelith perdió:

SU PERSONALIDAD Y SUS RECUERDOS.

Por eso el boss funciona como espejo psicológico.

---

## 14. ASSETS

Utilizar primero los assets existentes.

Ya existen recursos para:

- Vaelith;
- enemigos;
- boss;
- ruinas;
- plataformas;
- fondos;
- parallax;
- columnas;
- arcos;
- decoración funeraria;
- cadáveres;
- huesos;
- armas;
- símbolos;
- efectos ambientales;
- laboratorio;
- constructo;
- recuerdos;
- VFX de memoria.

Antes de solicitar o crear nuevos assets:

1. revisar los assets existentes;
2. comprobar si pueden reutilizarse;
3. comprobar si pueden recortarse o adaptarse;
4. comprobar si el problema puede resolverse mediante composición, escala, iluminación o programación.

Solo crear un nuevo asset si realmente falta.

Material fuente sin recortar: `assets/source_sheets/` (organizado por categoría, con `.gdignore`).
Frames ya extraídos y en uso: `assets/sprites/`.

---

## 15. OBJETIVO DE IMPLEMENTACIÓN

Primero AUDITAR el proyecto actual.

No modificar inmediatamente.

Revisar:

- estructura de escenas;
- scripts;
- player;
- enemigos;
- boss;
- HUD;
- colisiones;
- cámara;
- tiles;
- fondos;
- parallax;
- interacción;
- sistema de memoria;
- transición de escenas;
- errores actuales.

Después producir un diagnóstico:

1. Qué ya funciona.
2. Qué funciona parcialmente.
3. Qué está roto.
4. Qué falta para implementar la experiencia descrita.
5. Qué conviene refactorizar antes de continuar.

Después implementar por etapas.

Prioridad:

1. estabilidad;
2. movimiento;
3. combate;
4. cámara;
5. escenario;
6. enemigos;
7. interacción;
8. memoria;
9. narrativa;
10. boss;
11. pulido audiovisual.

No agregar sistemas innecesarios.

No rehacer código que ya funciona sin una razón concreta.

No generar contenido nuevo si puede resolverse con el contenido existente.

---

## 16. REGLA DE PRODUCCIÓN

El proyecto debe avanzar en paralelo:

```
GAMEPLAY ↔ ASSETS
```

No producir grandes cantidades de assets por adelantado.

Si durante la implementación aparece una necesidad concreta:

"Necesitamos X para que esta sección funcione."

Entonces detenerse y documentar exactamente qué asset falta (en `docs/ASSETS_PENDIENTES.md`).

Ese asset se producirá posteriormente.

---

## 17. CRITERIO DE ÉXITO

La demo debe conseguir que un jugador que no conoce el lore pase por esta progresión:

```
"¿Quién soy?"
  ↓
"¿Por qué sé hacer esto?"
  ↓
"¿Por qué estos muertos me resultan familiares?"
  ↓
"¿Yo hice esto?"
  ↓
"¿Quién es este guerrero?"
  ↓
"¿Por qué conoce mi forma de pelear?"
  ↓
"Él fue creado por mí."
  ↓
"Él recuerda quién era yo."
  ↓
FIN DE DEMO
```
