# Guion: auditoría y voz de Pharasma (fase 3)

Fuente: `Content/Vaelith/Guion/guion.json` (41 escenas). Los disparadores salen de `tools/ue/construir_nivel.py` y del C++. La revisión es del 25/11.

## Regla de voz, versión 2 (Marcos, 25/11: "todo lo que ella narre tiene que sonar a ella")
La v1 era una narradora en segunda persona que hablaba *de* Vaelith. En la v2 habla **Pharasma, en primera persona, a Vaelith**: ella lo despierta, le susurra, le explica a medias. Vaelith y el jugador la escuchan a la vez.

**Quién es** (Pathfinder, la Dama de las Tumbas):
- diosa del nacimiento, la muerte, el destino, la profecía y el tiempo;
- el ser más antiguo que existe;
- juzga a cada alma en su Osario, en lo alto de una aguja.

**Cómo habla:**
- **Fría e imparcial.** No dice si una muerte fue justa ni si Vaelith es bueno o malo. No consuela ni amenaza: constata. No es cruel ni tierna. Tiene el respeto de los dioses, no su afecto, y con Vaelith pasa lo mismo.
- **Ve el destino desde el nacimiento, pero se reserva el juicio.** Habla de hilos, de tiempo, de lo que "ya vi" y de lo que "todavía no juzgo".
- **Nunca suspendió el juicio de nadie.** Por eso devolver a Vaelith es anómalo. Ella no lo llama perdón ni regalo: es una **deuda** y un hilo sin terminar.
- **Lo único que le endurece la voz son los no-muertos.** No son un pecado más: son una perversión del ciclo y le roban almas que le pertenecen.
- **Nunca miente; omite.** Explica reglas, no razones. Cuando calla, se nota.
- **El misterio:** desde que murió un dios que nadie vio venir (Aroden, sin nombrarlo), la profecía se nubló. Puede admitir que **no ve entero el final de Vaelith**. Es el gancho del juego.
- **Lenguaje:** voseo, frases cortas, sin adjetivos de terror. El tiempo y el ciclo como imágenes: el reloj de arena, el río, el hilo, la espiral.

**Su presencia sin palabras** (canon; sirve para la luz, el sonido y la tentación):
- **Señales de agrado:** chotacabras, escarabajos, rosas negras sin espinas, su espiral de plata y azul, un reloj de arena con arena roja.
- **Señales de desagrado:** escalofrío en la espalda, sabor a tierra en la boca, la sensación de haber olvidado algo importante, sangre bajo las uñas.

**Siguen igual:**
- **Los recuerdos** conservan las voces del pasado entre rayas. Pharasma los abre y los cierra.
- **La Sombra** habla en directo en la pelea final.
- **Las escenas de interacción** bloquean el control y se adelantan con E. Las de zona se leen caminando.

## Incoherencias encontradas (texto ≠ lo que pasa)
| Escena | Dice | Pasa en el juego | Propuesta |
|---|---|---|---|
| `intro` | "Te incorporás" a los ~21 s | El cuerpo se incorpora entre los 13 y los 16,5 s | Rehacer los tiempos para que la línea caiga a los 13 s |
| `zona_cementerio` | "Las tumbas más cercanas están abiertas. La tierra salió hacia afuera." | Cerca de la salida no hay tumbas abiertas; el único sarcófago abierto está a 120 m | Colocar 3–4 tumbas abiertas (tierra hacia afuera) junto a la salida, o cambiar el texto. **Propongo colocarlas**: es la imagen fuerte de la zona |
| `sombra_vista` | "Esos cortes son limpios." | En esa celda (fila 7, col 7) no hay cuerpos cortados | Poner restos con cortes limpios (huesos partidos, un escudo hendido) |
| `guardian` | "Sostiene una lanza que ya no puede levantar." | El centinela es el esqueleto sin lanza | Darle una lanza (pieza simple por script) o sacar la lanza del texto |
| `zona_torre` | "La puerta no fue forzada desde afuera: la abrieron desde adentro." | La torre no tiene puerta: la entrada es el arco en ruinas | Hablar del arco y de las marcas de fuego, que sí existen |
| `torre_subida` | escena de la escalera | No hay escalera en la torre; la escena nunca se dispara | Queda hasta que exista la escalera (pendiente visual) |
| `recuerdo_4` | etiqueta "Tocar el disco" | La pieza es un altar de Pharasma | Etiqueta "Tocar el altar", o poner un disco/rueda sobre el altar. **Propongo la rueda**: es su símbolo |
| `espejo_agua` | "Un rostro delgado, pálido… el reflejo tarda en imitarte" | El agua es un plano azul y no refleja | Se resuelve con el agua de la fase 4; el texto se mantiene |
| `vista_pueblo` | "hacia el oeste, donde el bosque se vuelve negro" | Correcto: la torre queda hacia el bosque oscuro | Mantener; agregar que las estatuas marcan el camino |
| `recuerdo_1` | No dice que abre la reja 2 | Tocar la urna abre la reja 2 y nadie lo sabe (fue el bloqueo de Marcos) | Pharasma lo insinúa al cerrar el recuerdo |
| `lectura_altar` / `altar_2` | El altar 2 no tiene escena | — | Opcional: una línea de Pharasma en el altar 2 |

## Muestra de tono v2 (4 escenas + 1): **aprobar antes de reescribir el resto**
La v1 queda abajo, en el historial.

### intro (despertar)
| Momento | Pharasma |
|---|---|
| negro | Despertá. |
| abre los ojos | Soy yo quien te despierta. Nadie más podría. |
| frío | Ese frío lo traés de mi lado del río. Tardará en irse. |
| olor | Piedra húmeda, incienso apagado. Te dejé donde te enterraron. |
| se incorpora (13 s) | El cuerpo te obedece. Te lo presto. |
| ¿quién soy? | Vas a preguntarte quién sos. Te dejé el nombre. |
| título | **Vaelith Arken** |
| cierre | Lo demás lo guardo yo. Algunas cosas se recuerdan; otras se pagan. |

### recuerdo_1 (urna)
| Momento | Texto |
|---|---|
| apertura (Pharasma) | Esta urna guarda ceniza y algo tuyo. Te lo dejo ver. No te lo explico. |
| recuerdo (voces del pasado, sin cambios) | Una respiración en la oscuridad. / —¿Qué querés que sea? / Una mesa de piedra… / —Yo. / La criatura abre los ojos. / —No. Mejor que yo. |
| cierre (Pharasma) | Esa voz era la tuya. Yo también estaba ahí. Siempre estoy. |
| la reja se abre | Detrás de vos, el hierro cede. Lo que recordás abre caminos. No todos te van a gustar. |

### zona_cementerio
| Momento | Pharasma |
|---|---|
| rótulo | El camposanto de Varo |
| salida | Aire de afuera. El frío de verdad. |
| tumbas abiertas | Mirá esa tierra: empujada desde abajo. Nadie cavó. |
| (voz endurecida) | Esos cuerpos eran míos. Alguien me los quitó. Devolvémelos. |

### vista_pueblo
| Momento | Pharasma |
|---|---|
| la vista | Allá abajo, un pueblo. Ventanas encendidas. |
| nacimiento y muerte | Esta noche alguien nace ahí, y alguien muere. Los dos vienen a mí. |
| el llamado | Todavía no vas para ese lado. Algo tira de vos hacia el oeste, donde el bosque se cierra. |
| estatuas | Mis estatuas conocen el camino. Seguí la luz que encienden. |

### +1: la tentación (fase E, cadáver: "Levantar" / "Dar descanso")
| Momento | Pharasma |
|---|---|
| mirar el cadáver | Este ya cruzó. Su cuerpo quedó atrás, como quedan todos. |
| elige Dar descanso | Bien. Que la tierra lo guarde hasta que yo lo llame. |
| elige Levantar | *(sabor a tierra en la boca; escalofrío)* Sabías hacerlo. Por eso estás acá. |
| y el recuerdo | Otra vez. |

### Historial: muestra v1 (rechazada, era una narradora que hablaba de él)


### intro (despertar)
| Antes | Después (Pharasma) |
|---|---|
| La oscuridad no desaparece cuando abrís los ojos. | Abrís los ojos. La oscuridad se queda. No tenía por qué irse. |
| Primero sentís frío. No el de una noche de invierno: una ausencia de calor… | Ese frío no es de invierno. Es el que le queda a un cuerpo que estuvo mucho tiempo sin dueño. |
| Respirás. El aire huele a piedra húmeda y a incienso apagado. | Piedra húmeda. Incienso apagado. Alguien rezó acá y no volvió a terminar el rezo. |
| ¿Dónde...? | Te preguntás dónde estás. Es la más pequeña de tus preguntas. |
| Te incorporás. El cuerpo responde, y eso resulta extraño. | *(a los 13 s, cuando se levanta)* El cuerpo obedece. A vos te sorprende. A mí, no. |
| ¿Quién soy? | Ahora te preguntás quién sos. |
| La respuesta llega antes de que termines de formular la pregunta. | Eso sí te lo dejé. |
| **Vaelith Arken** (título) | **Vaelith Arken** |
| No recordás que nadie te lo haya dicho. Simplemente está ahí. | Un nombre. Lo demás vas a tener que ganártelo. |

### recuerdo_1 (urna de la sala del altar)
| Antes | Después |
|---|---|
| *(empieza directo)* | La urna guarda ceniza y algo que es tuyo. Te lo devuelvo. No es un regalo. |
| Una respiración en la oscuridad. | Una respiración en la oscuridad. |
| —¿Qué querés que sea? | —¿Qué querés que sea? |
| Una mesa de piedra. Sobre ella, algo incompleto: carne, metal, hueso. | Una mesa de piedra. Carne, metal y hueso, todavía sin decidir qué forma tomar. |
| Una figura de espaldas. No le ves el rostro. | Alguien de espaldas. No le ves el rostro. No te hace falta. |
| —Yo. | —Yo. |
| La criatura abre los ojos. | La criatura abre los ojos. |
| —No. Mejor que yo. | —No. Mejor que yo. |
| Esa voz era la mía. *(pensamiento)* | Esa voz era la tuya. No te apures a decidir qué significa. |
| *(nada)* | Detrás de vos, el hierro cede. Lo que recordás abre caminos, aunque no siempre los que querrías. |

### zona_cementerio (salida de la cripta)
| Antes | Después |
|---|---|
| El camposanto de Varo (rótulo) | El camposanto de Varo |
| Aire. Frío de verdad, con olor a tierra removida. | Aire de afuera. Frío de verdad, y tierra removida. |
| Las tumbas más cercanas están abiertas. La tierra salió hacia afuera. | Mirá cómo quedó la tierra de esas tumbas: empujada hacia afuera. *(con las tumbas abiertas colocadas)* |
| No los desenterraron. Salieron solos. *(pensamiento)* | Nadie cavó. Salieron solos. Alguna vez supiste por qué. |

### vista_pueblo (la loma)
| Antes | Después |
|---|---|
| Desde lo alto de la loma se ve el valle. Lejos, un pueblo: ventanas encendidas, una iglesia. | Allá abajo, un pueblo. Ventanas encendidas, una iglesia. |
| Gente que cena y se va a dormir sin pensar en los muertos. *(pensamiento)* | Gente que cena sin pensar en sus muertos. Eso, alguna vez, te pareció un desperdicio. |
| Algo tira de vos en la dirección contraria, hacia el oeste, donde el bosque se vuelve negro. | Pero no es ahí adonde vas. Algo tira de vos hacia el oeste, donde el bosque se cierra. |
| Por ahí no hay sendero. Voy a tener que buscarlo. *(pensamiento)* | No hay sendero. Mis estatuas saben el camino. |

## Después de aprobar
1. Reescribir las 37 escenas restantes con esta voz.
2. Corregir las incoherencias de la tabla: tumbas abiertas en la salida, restos con cortes, lanza del centinela, rueda sobre el altar 4, tiempos del despertar.
3. Marcar como bloqueantes las escenas de interacción.
4. Revisar los textos sueltos (`saber_*`, `penitencia_*`, `moribundo`, `aviso_*`) con la misma voz.
