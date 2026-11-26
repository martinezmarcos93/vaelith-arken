"""Guion en la voz de Pharasma (v2, aprobada por Marcos el 25/11): reescribe Content/Vaelith/Guion/guion.json.

Regla (docs/guion-auditoria.md):
- Pharasma habla en primera persona, a Vaelith, con voseo. Lo despierta, le susurra, le explica a medias.
  Fría e imparcial: no consuela ni amenaza, constata. Nunca miente; omite. La voz se le endurece con los
  no-muertos (le roban almas). La vida de Vaelith es un préstamo, no un perdón.
- Los recuerdos conservan las voces del pasado ("voz" = Vaelith de antes, "sombra" = la criatura).
- "narracion" es su susurro (abajo, en el marco). "pharasma" es su voz plena (centro, dorado): solo para
  momentos de juicio (recuerdo 4, muertes).
- "bloquean": escenas que nacen de una interacción. Bloquean el control mientras duran (se adelantan con E).

Uso: python3 tools/guion_pharasma.py   (sobrescribe guion.json; el anterior queda en git)
"""
import json
import os

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RUTA = os.path.join(RAIZ, "Content", "Vaelith", "Guion", "guion.json")

N, P, V, S, R, T, RO = "narracion", "pharasma", "voz", "sombra", "recuerdo", "titulo", "rotulo"

ESCENAS = {
    # Despertar: el cuerpo se incorpora entre los 13 y los 16,5 s; "El cuerpo te obedece" cae a los 13 s.
    "intro": [
        [N, "Despertá.", 3.0, 1.0],
        [N, "Soy yo quien te despierta. Nadie más podría.", 4.0, 0.5],
        [N, "Ese frío lo traés de mi lado del río. Tarda en irse.", 3.5, 1.1],
        [N, "El cuerpo te obedece. Te lo presto.", 3.5, 0.5],
        [N, "Piedra húmeda, incienso apagado. Te dejé donde te enterraron.", 4.5],
        [N, "Vas a preguntarte quién sos. Te dejé el nombre.", 4.0, 0.8],
        [T, "Vaelith Arken", 4.0, 0.8],
        [N, "Lo demás lo guardo yo. Algunas cosas se recuerdan; otras se pagan.", 5.0],
    ],
    "continuar": [
        [RO, "La deuda continúa", 3.5, 1.0],
        [N, "Seguimos donde quedamos. La deuda también.", 3.5],
    ],
    "armas": [
        [N, "Tus dedos encuentran la empuñadura antes de buscarla.", 3.5],
        [N, "No aprendiste a usarla en esta vida. El cuerpo se acuerda de la otra.", 4.5],
        [N, "El escudo es para cuidar a los muertos. Antes no te importaban.", 4.5],
    ],
    "daga": [
        [N, "Mi espiral, en la empuñadura. Te aprieta el pecho y no sabés por qué.", 4.5],
        [R, "Una mujer. Un trono. Una rueda que gira.", 4.0],
        [N, "Me viste una vez. Vas a volver a verme.", 3.5],
    ],
    "zona_catacumba": [[RO, "Catacumbas de la Rueda", 4.0, 1.0]],
    "primer_enemigo": [
        [N, "Pasos arrastrados. No respira.", 3.0],
        [N, "Eso me lo robaron. Devolvémelo.", 3.5],
    ],
    "puerta_cerrada": [[N, "Cerrada. No todo se abre a la fuerza; a veces se abre recordando.", 4.0]],
    "lectura_nichos": [
        [N, "Los nombres de los nichos fueron raspados. A cincel.", 3.5],
        [N, "Alguien no quería que los recordaran. Yo los recuerdo a todos.", 4.0],
    ],
    "lectura_altar": [
        [N, "«Toda alma pasa por la Rueda. Ninguna queda afuera.»", 4.0],
        [N, "Debajo, con otra mano: «Ninguna, salvo las que él retuvo.»", 4.5],
        [N, "Ninguna quedó afuera. Algunas tardaron más.", 3.5],
    ],
    "espejo_agua": [
        [N, "El agua está quieta. Inclinate.", 3.0],
        [N, "Un rostro delgado, pálido, de sangre élfica. Te mira como si te esperara.", 4.5],
        [N, "Es la cara que te devolví. No la elegiste vos.", 3.5],
        [N, "El reflejo tarda un instante en imitarte. No es el agua.", 4.0],
    ],
    "sombra_vista": [
        [N, "Restos cortados hace poco. Cortes limpios.", 3.5],
        [N, "Conocés esa forma de cortar. La enseñaste.", 3.5],
    ],
    "cadaver": [
        [N, "Lo cubrís con lo que queda de su mortaja.", 3.0],
        [N, "Bien. Que la tierra lo guarde hasta que yo lo llame.", 3.5],
    ],
    "recuerdo_1": [
        [N, "Esta urna guarda ceniza y algo tuyo. Te lo dejo ver. No te lo explico.", 4.5, 0.6],
        [R, "Una respiración en la oscuridad.", 3.0, 0.6],
        [V, "—¿Qué querés que sea?", 3.0],
        [R, "Una mesa de piedra. Carne, metal y hueso, todavía sin decidir qué forma tomar.", 5.0],
        [R, "Alguien de espaldas. No le ves el rostro. No te hace falta.", 3.5],
        [V, "—Yo.", 2.0],
        [R, "La criatura abre los ojos.", 3.0],
        [V, "—No. Mejor que yo.", 3.0, 1.0],
        [N, "Esa voz era la tuya. Yo también estaba ahí. Siempre estoy.", 4.0, 0.6],
        [N, "En algún lugar de esta piedra, el hierro cede. Lo que recordás abre caminos. No todos te van a gustar.", 5.5, 1.0],
    ],
    "zona_osario": [
        [RO, "El Osario Profundo", 4.0, 1.0],
        [N, "Acá abajo los muertos no están quietos. Alguien los ató a este lugar, y no fui yo.", 4.5],
    ],
    "primer_atado": [
        [N, "Ese espíritu no ataca por odio. Está encadenado a algo.", 3.5],
        [N, "Rompé lo que lo retiene y viene a mí. No hace falta destruirlo.", 4.0],
    ],
    "alma_liberada": [
        [N, "Cruzó. La recibo.", 2.5],
        [N, "Una menos en tu cuenta.", 2.5],
    ],
    "recuerdo_2": [
        [N, "Otro pedazo de lo que fuiste. Miralo entero.", 3.5, 0.6],
        [R, "La criatura está de pie frente a vos. Todavía tiene costuras visibles.", 4.5, 0.6],
        [V, "—Atacame.", 2.0],
        [R, "No se mueve.", 2.0],
        [S, "—No quiero.", 2.5],
        [V, "—No te pregunté qué querías.", 3.0],
        [R, "La criatura baja la cabeza.", 2.5],
        [S, "—Entonces no soy como vos.", 3.0],
        [V, "—Todavía no.", 3.0, 1.0],
        [N, "Le diste voluntad. Después le pediste que no la usara. Lo recuerdo bien.", 4.5, 1.0],
    ],
    "estandarte": [
        [N, "Un estandarte podrido: un sol negro de ocho rayos.", 3.5],
        [R, "Filas de muertos marchando bajo ese sol, en silencio, al paso de alguien que no necesitaba gritar.", 5.5],
        [N, "Los conducías vos. Todos me llegaron tarde.", 3.5],
    ],
    "zona_bosque": [
        [RO, "El Bosque de los Centinelas", 4.0, 1.0],
        [N, "Pasado el arco, los pinos se cierran. Resina, humedad, ningún pájaro.", 4.5],
        [N, "Alguien mantuvo abierto este sendero mucho tiempo. Seguilo.", 4.0],
    ],
    "guardian": [
        [N, "Un soldado muerto, todavía en su puesto. Ya no le queda arma, y sigue de guardia.", 4.5],
        [N, "No ataca. Te mira pasar como a un superior.", 3.5],
        [N, "Le ordenaron vigilar. Nadie le dijo que podía irse. La orden fue tuya; el relevo también puede serlo.", 5.5],
    ],
    "guardian_herido": [[N, "No se defiende. Sigue esperando la orden.", 3.0]],
    "guardian_muerto": [
        [N, "Cae sin un sonido.", 2.5],
        [N, "Cumplía una orden tuya, y lo castigaste por cumplirla. Lo recibo igual.", 4.5],
    ],
    "guardian_relevado": [
        [V, "—Descansá, soldado. Ya no hay nada que vigilar.", 3.5],
        [N, "Baja la cabeza. Se desarma sin ruido, como quien por fin termina un turno.", 4.5],
        [N, "Lo recibo. Llegó en paz, y eso también lo anoto.", 3.5],
    ],
    "lectura_lapida": [
        [N, "«Aquí yacen los de Varo, que no abrieron sus puertas.»", 4.0],
        [N, "Debajo, otra mano: «Las abrieron después. Él se encargó.»", 4.5],
        [N, "Los de Varo me llegaron dos veces. La segunda, por vos.", 4.0],
    ],
    "recuerdo_3": [
        [N, "Ceniza otra vez. Debajo, un patio.", 3.0, 0.6],
        [R, "La criatura practica en un patio. El mismo movimiento, una y otra vez.", 4.5, 0.6],
        [V, "—Otra vez.", 2.0],
        [V, "—Más rápido.", 2.0],
        [S, "—¿Para qué?", 2.5],
        [V, "—Algún día vas a necesitarlo.", 3.0],
        [S, "—¿Para qué?", 2.5],
        [R, "Una pausa larga.", 2.0],
        [V, "—Para reemplazarme.", 3.0],
        [S, "—¿Vas a morir?", 2.5],
        [V, "—Todos mueren.", 2.5],
        [S, "—Vos también.", 3.0, 0.8],
        [N, "No le respondiste. Yo sí lo habría hecho.", 3.5, 1.0],
    ],
    "zona_torre": [
        [RO, "La Torre de Arken", 4.0, 1.0],
        [N, "Piedra quemada. Nadie derribó ese arco desde afuera: el fuego empezó adentro.", 4.5],
        [N, "Acá moriste. Lo sé porque te recibí.", 3.5, 1.2],
    ],
    "torre_subida": [[N, "Cada escalón lo subiste mil veces. Tus pies lo saben mejor que vos.", 4.5]],
    "recuerdo_4": [
        [N, "Tocá la rueda. Ya la viste girar una vez.", 3.5, 0.8],
        [R, "Oscuridad. Después, una luz gris, inmensa, sin fuente.", 4.5, 0.8],
        [R, "Una mujer sentada, el rostro velado. A su espalda, una rueda que gira sin detenerse.", 5.5],
        [P, "Vaelith Arken.", 3.5, 1.0],
        [N, "No necesité enumerarte nada. Las tumbas abiertas, las almas sometidas, el pueblo que no te entregó sus muertos y los vio levantarse esa misma noche.", 7.5],
        [P, "Creíste que la muerte era un problema sin resolver.", 4.0],
        [P, "No vas a recibir el descanso que esperabas.", 4.0],
        [N, "Te quité el poder. Te quité la memoria. Te dejé el nombre.", 4.5],
        [P, "Vas a volver. Vas a servir. Y cuando la deuda esté saldada, vas a volver a estar frente a mí.", 6.5],
        [N, "No te castigué con el olvido. Te castigué con la posibilidad de recordar.", 5.0, 1.0],
        [N, "Tu final no lo veo entero. Eso no me pasa seguido.", 4.0, 1.5],
    ],
    "sombra_aparece": [
        [N, "Al otro lado del piso partido te espera alguien con tu altura, tu escudo y tu forma de pararte.", 5.0],
        [N, "Adoptás la guardia. Hace lo mismo.", 3.0],
        [S, "—Todavía hacés eso.", 3.0],
        [V, "—¿Qué?", 2.0],
        [S, "—Cargás primero.", 3.0],
    ],
    "sombra_mitad": [
        [S, "—La espada. El escudo. La distancia.", 3.5],
        [S, "—Seguís peleando igual.", 3.0],
        [S, "—Eso que no sabés hacer también lo sabías. Solo que ya no lo recordás.", 4.5],
    ],
    "diehard": [[N, "Todavía no.", 2.5]],
    "muerte_1": [[P, "Todavía no terminaste.", 3.5, 0.8]],
    "muerte_2": [[P, "La deuda no se paga cayendo.", 3.5, 0.8]],
    "muerte_3": [[P, "Levantate, Vaelith.", 3.5, 0.8]],
    # Finales por los tres ejes (Gracia, Memoria, Corrupción): Guardián, Penitente, Nigromante.
    "final_gracia": [
        [S, "—Liberaste a los que até. Yo no habría podido.", 4.0, 1.0],
    ],
    "final_neutro": [
        [S, "—Peleás como él. Todavía no sé si pensás como él.", 4.0, 1.0],
    ],
    "final_deuda": [
        [S, "—Volviste igual que te fuiste.", 3.5, 1.0],
    ],
    "final": [
        [S, "—¿No sabés quién soy?", 3.0, 0.6],
        [V, "—No.", 2.0],
        [S, "—Claro. Te aseguraste de eso.", 3.5],
        [R, "Fuego en los pasillos. Gritos al otro lado de una puerta.", 4.0, 1.0],
        [R, "—¡Señor, nos están rodeando!", 3.0],
        [V, "—Entonces que entren.", 3.0],
        [R, "La puerta se abre. Entrás herido y te arrodillás frente a la criatura. Por primera vez parecés cansado.", 6.0],
        [V, "—Si alguna vez regreso... no me dejes recordar.", 4.5],
        [S, "—¿Por qué?", 2.5],
        [V, "—Porque si recuerdo lo que hice, voy a tener que decidir si todavía soy el mismo.", 6.0, 1.0],
        [N, "Yace frente a vos. La máscara se partió. No se parece a vos: se parece a lo que querías ser.", 6.0, 1.5],
        [S, "—Ahora sí me recordaste.", 3.5, 1.0],
        [S, "—No a mí.", 2.5],
        [S, "—A vos.", 3.5, 1.5],
        [T, "La deuda continúa.", 5.0, 2.5],
    ],
    "final_guardian": [
        [N, "Recordaste quién fuiste y no lo repetiste. Eso no lo había visto antes.", 5.0, 1.0],
    ],
    "final_penitente": [
        [N, "Sabés lo que hiciste. Lo cargás. Eso es lo único que te pedí.", 4.5, 1.0],
    ],
    "final_nigromante": [
        [N, "Volviste a usar lo que te quité. Te lo anoto, Vaelith. Todo.", 4.5, 1.0],
    ],
    "zona_cementerio": [
        [RO, "El camposanto de Varo", 4.0, 1.0],
        [N, "Aire de afuera. El frío de verdad.", 3.0],
        [N, "Mirá esa tierra: empujada desde abajo. Nadie cavó.", 3.5],
        [N, "Esos cuerpos eran míos. Alguien me los quitó. Devolvémelos.", 4.0],
    ],
    "vista_pueblo": [
        [N, "Allá abajo, un pueblo. Ventanas encendidas.", 3.5],
        [N, "Es Varo. Reconstruyeron. Podés bajar, aunque no todos te van a mirar igual.", 4.5],
        [N, "Lo que te llama está al oeste, donde el bosque se cierra.", 3.5],
        [N, "Mis estatuas conocen el camino. Seguí la luz que encienden.", 3.5],
    ],
    "zona_pueblo": [
        [RO, "Varo", 3.5, 1.0],
        [N, "Esta noche alguien nace acá, y alguien muere. Los dos vienen a mí.", 4.5],
        [N, "Los viejos de este pueblo enterraron a sus muertos dos veces. Acordate de eso cuando te hablen.", 5.0],
    ],
    # ---- La planilla en juego (fase R2): diagnósticos, tentación, anatema ----
    "diag_fallo": [[N, "Huesos y tela. Hoy no sabés leerlos.", 3.0]],
    "diag_tentacion": [
        [RO, "Respeto", 2.5, 0.3],
        [N, "Murió contra esta reja, del lado de afuera. Quería llegar a mi daga y no lo dejaron.", 5.0],
    ],
    "diag_tentacion_critico": [
        [RO, "Respeto", 2.5, 0.3],
        [N, "Murió contra esta reja, del lado de afuera. Quería llegar a mi daga y no lo dejaron.", 5.0],
        [N, "Lo encerró alguien que sabía levantar muertos. Lo sabés porque vos también sabías.", 5.0],
    ],
    "tentacion_descanso": [
        [N, "Lo dejás en paz. La reja sigue cerrada.", 3.5],
        [N, "Lo correcto casi nunca es lo corto.", 3.0],
    ],
    "tentacion_levantar": [
        [N, "Extendés la mano. El muerto se pone de pie y empuja el hierro. Te obedece, como antes.", 5.5],
        [R, "Otra vez.", 2.5, 0.8],
        [N, "Sabías hacerlo. Por eso estás acá.", 3.5],
    ],
    "reja_forzada": [[N, "El hierro cede. Tus brazos recuerdan más que vos.", 3.5]],
    "reja_firme": [[N, "El hierro no se mueve. Todavía.", 2.5]],
    "reja_rezada": [[N, "Mi sello te reconoce. No porque lo merezcas: porque me servís.", 4.0]],
    "reja_sello_mudo": [[N, "El sello no responde. Rezaste con la boca.", 3.0]],
    "diag_restos": [
        [RO, "Respeto", 2.5, 0.3],
        [N, "Un aventurero. Lo mataron de frente. En la cintura, un frasco intacto.", 4.5],
    ],
    "robo_restos": [[N, "Le sacás el frasco a un muerto. Lo que robaste era mío.", 3.5]],
    "diag_guardian": [
        [RO, "Liberación", 2.5, 0.3],
        [N, "No lo ata un ritual. Lo ata una orden. Las órdenes se revocan.", 4.0],
    ],
    "diag_guardian_critico": [
        [RO, "Liberación", 2.5, 0.3],
        [N, "No lo ata un ritual. Lo ata una orden. Las órdenes se revocan.", 4.0],
        [N, "La orden tiene tu voz.", 3.0],
    ],
    "diag_huesos": [
        [RO, "Compasión", 2.5, 0.3],
        [N, "Esta alma espera que alguien la entierre. Nada más que eso.", 4.0],
    ],
    "anatema": [[N, "Te lo anoto. Hasta que vuelvas a rezarme, mi fuerza no pasa por tus manos.", 4.5]],
    "expiacion": [
        [N, "Rezás. No te perdono: anoto que volviste.", 3.5],
        [N, "Mi fuerza vuelve a tus manos. Lo que hiciste, no se va.", 3.5],
    ],
    "salvado": [
        [P, "Todavía no.", 2.5, 0.5],
        [N, "Te devolví sin cobrarte. No te acostumbres.", 3.5],
    ],
    "estatua_guia": [
        [N, "Una de mis estatuas. El farol estaba vacío; cuando te acercás, prende.", 4.0],
        [N, "Hay más. Seguí la luz que encienden.", 3.0],
    ],
    "hondonada": [
        [N, "El terreno baja. La niebla se junta en el fondo como agua quieta.", 4.0],
        [N, "Ahí abajo está tu torre.", 3.0],
    ],
}

# Escenas que nacen de una interacción: bloquean el control (y la tregua frena a los no-muertos).
BLOQUEAN = ["armas", "daga", "lectura_nichos", "lectura_altar", "espejo_agua", "cadaver", "estandarte",
            "lectura_lapida", "guardian_relevado", "diag_fallo", "diag_tentacion", "diag_tentacion_critico",
            "tentacion_descanso", "tentacion_levantar", "reja_forzada", "reja_rezada", "diag_restos", "robo_restos",
            "diag_guardian", "diag_guardian_critico", "diag_huesos", "expiacion"]

TEXTOS = {
    "menu_pie": "No busca vivir. Busca merecer morir.",
    "aviso_altar": "Rezaste. Te devuelvo la vida, el foco y el escudo. La deuda queda donde estaba.",
    "aviso_daga": "Su hoja hiere a los espíritus como si tuvieran carne. Tecla 2 para alternar entre espada y daga.",
    "saber_zombi": "Carne sin voluntad, movida por energía de vacío. Lenta y obstinada. El filo de la espada la abre sin esfuerzo.",
    "saber_esqueleto": "Hueso ensamblado por un ritual. El filo resbala; un golpe de escudo (F) lo quiebra.",
    "saber_fantasma": "Un alma retenida. El acero apenas la roza; mi daga o Imponer las Manos (R) la hieren de verdad. Si está atada a algo, rompé el ancla y viene a mí.",
    "penitencia_1": "Te devuelvo. El lugar donde caíste recuerda tu caída.",
    "penitencia_2": "Otra vez. La oscuridad de este tramo se espesa con cada regreso.",
    "penitencia_3": "Yo no me canso. Vos sí. Rezá ante un altar y aliviá la carga.",
    "moribundo": "Levantate. Todavía no terminaste. (clic o R)",
    "dote_titulo": "Algo vuelve con el recuerdo",
    "controles": "WASD moverse · Shift correr · Espacio saltar|Clic izquierdo tajo · mantener para tajo potente · golpe a un enemigo desprevenido o de espaldas: crítico|Clic derecho alzar el escudo (+2 CA) · justo antes del golpe: Retribución|F golpe de escudo · Q embestida · R Imponer las Manos · T desmoralizar|G agua bendita · C poción · V tratar heridas (fuera de combate)|2 espada / daga · E interactuar · rueda elegir · E o Enter adelantar texto · Tab Registro del Osario · Esc pausa",
}


def main():
    with open(RUTA, encoding="utf-8") as f:
        g = json.load(f)
    g["_formato"] = ("escenas: lista de [estilo, texto, duración opcional, espera opcional]. Estilos: narracion (susurro de "
                     "Pharasma), pharasma (su voz plena), voz (Vaelith en un recuerdo), sombra, recuerdo, titulo, rotulo. "
                     "bloquean: escenas que bloquean el control. textos: cadenas sueltas; en 'controles' y 'creditos' las "
                     "líneas se separan con |. Generado por tools/guion_pharasma.py (no editar a mano).")
    g["escenas"] = ESCENAS
    g["bloquean"] = BLOQUEAN
    g["textos"].update(TEXTOS)
    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=1)
    n_lineas = sum(len(v) for v in ESCENAS.values())
    print(f"OK guion: {len(ESCENAS)} escenas, {n_lineas} líneas, {len(BLOQUEAN)} bloquean")


if __name__ == "__main__":
    main()
