shader_type canvas_item;

// Luz de contorno en pixel art: aclara los píxeles del borde superior (y a
// media intensidad los laterales) para separar la silueta
// de fondos oscuros. Trabaja en píxeles enteros de la textura: no suaviza.
// Uso: material del AnimatedSprite2D del protagonista (crítica 2026-11-04:
// "el personaje se pierde por falta de contraste").

uniform vec4 color_luz : source_color = vec4(0.463, 0.427, 0.737, 1.0); // #766DBC
uniform float intensidad : hint_range(0.0, 1.0) = 0.7;
uniform float contorno_oscuro : hint_range(0.0, 1.0) = 0.5; // borde exterior negro tenue

void fragment() {
	vec4 c = texture(TEXTURE, UV);
	vec2 px = TEXTURE_PIXEL_SIZE;
	if (c.a > 0.5) {
		// borde iluminado: arriba entero, los costados a la mitad (simétrico,
		// así no depende de flip_h)
		float arriba = step(texture(TEXTURE, UV - vec2(0.0, px.y)).a, 0.5);
		float izq = step(texture(TEXTURE, UV - vec2(px.x, 0.0)).a, 0.5);
		float der = step(texture(TEXTURE, UV + vec2(px.x, 0.0)).a, 0.5);
		float borde = arriba + 0.5 * max(izq, der);
		c.rgb = mix(c.rgb, color_luz.rgb, clamp(borde, 0.0, 1.0) * intensidad);
	} else {
		// contorno exterior oscuro de 1 px (solo en los 4 vecinos)
		float n = texture(TEXTURE, UV + vec2(px.x, 0.0)).a + texture(TEXTURE, UV - vec2(px.x, 0.0)).a
			+ texture(TEXTURE, UV + vec2(0.0, px.y)).a + texture(TEXTURE, UV - vec2(0.0, px.y)).a;
		if (n > 0.5) {
			c = vec4(0.004, 0.035, 0.004, contorno_oscuro); // #010901
		}
	}
	COLOR = c;
}
