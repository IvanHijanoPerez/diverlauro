# Diver Lauro · Web oficial

Web del salón de celebraciones **Diver Lauro**, en Calle Crianza 30, Alhaurín de la Torre (Málaga): cumpleaños, comuniones, bautizos, bodas, despedidas, comidas de empresa y eventos, de día y de noche.

Web estática (HTML + CSS + JS, sin compilación). Publicada en https://diverlauro.pages.dev/

## Qué incluye

- **Identidad de la marca**: amarillo `#EBD450` + azul marino `#0D305D` y el logo original a pincel.
- **Modo día / noche**: interruptor en la cabecera y en el hero. De día, tonos amarillos y globos de colores; de noche, fondo oscuro, neones, globos metalizados, bola de discoteca y focos. Se elige solo según la hora del visitante (noche de 20:00 a 7:00) y recuerda su elección.
- **Escena 3D** en el hero con [Three.js](https://threejs.org/) (cargado desde CDN): globos que se pueden explotar con un toque (sueltan confeti), confeti cayendo y paralaje con el ratón. En móvil va más ligera; si el navegador no tiene WebGL se ve el fondo normal.
- **Fotos reales** del local y de celebraciones (optimizadas en `.webp`, sin datos GPS del móvil):
  - Selector "Un salón, mil celebraciones" (comunión, cumpleaños, boda, noche, eventos).
  - Bento del local (parque de bolas, sala, sonido, futbolín, office, rincón infantil).
  - Galería con filtros y visor a pantalla completa (teclado y deslizar en móvil).
- **Opiniones**: valoración de Google (4,5 · 175 reseñas) y lo que más destacan los clientes. Se pueden mostrar reseñas reales (ver abajo).
- **Formulario → WhatsApp** con tipo de celebración, fecha, horario (día/noche) e invitados. No necesita servidor ni guarda datos.
- **SEO local**: título/descripción para "salón de celebraciones Alhaurín de la Torre", datos estructurados `LocalBusiness` + `EventVenue` + `FAQPage`, Open Graph con imagen propia, `sitemap.xml`, `robots.txt`, coordenadas.

## Estructura

```
index.html          Página principal (contenido y SEO)
css/styles.css      Estilos, modo día/noche y animaciones
js/main.js          Interacciones (modo, menú, galería, formulario, opiniones)
js/scene.js         Escena 3D del hero (Three.js)
img/fotos/          Fotos del local (nombre.webp = grande, nombre-sm.webp = miniatura)
img/                Logo (azul, amarillo, blanco), iconos e imagen para redes (og-image.jpg)
```

## Cambiar datos

Todo está en `index.html`. Busca y reemplaza:

| Dato | Valor actual |
|---|---|
| Teléfono / WhatsApp | `647 91 30 22` · `34647913022` · `+34647913022` |
| Instagram | `https://www.instagram.com/diverlauro/` |
| Facebook | `https://www.facebook.com/Diver-Lauro-193712877866926` |
| Dirección | `Calle Crianza, 30 · 29130 Alhaurín de la Torre` |
| Valoración Google | `4,5` y `175` reseñas |

El número de WhatsApp del formulario está también en `js/main.js` (`WHATSAPP`).

### Añadir reseñas reales de Google

En `js/main.js`, al principio, rellena la lista `REVIEWS` copiando reseñas **tal cual** de Google:

```js
const REVIEWS = [
  { autor: "María G.", texto: "Texto exacto de la reseña…", estrellas: 5 },
];
```

### Añadir fotos

Guarda dos versiones en `img/fotos/` (`nombre.webp` de ~1600 px y `nombre-sm.webp` de ~800 px) y copia un bloque de la galería en `index.html`:

```html
<a class="g-item" data-cat="cumple" href="img/fotos/nombre.webp"><img src="img/fotos/nombre-sm.webp" alt="Descripción de la foto" width="800" height="600" loading="lazy"></a>
```

`data-cat` puede ser `infantil`, `comunion`, `cumple`, `boda`, `evento` o `local`.

## Publicación (Cloudflare Pages)

La web está publicada en **https://diverlauro.pages.dev/** con Cloudflare Pages, conectado a este repositorio:
cada `git push` a `main` se publica solo en 1–2 minutos.

Configuración del proyecto en Cloudflare: *Framework preset* `None`, *Build command* vacío, *Build output directory* `/`.

Recomendado: activar **Web Analytics** en Cloudflare para ver las visitas.

### Dominio propio (recomendado)

Con un dominio tipo `diverlauro.es` se posiciona mejor y da más confianza:

1. Compra el dominio (DonDominio, Dinahosting…) y cambia sus *nameservers* a los que indique Cloudflare (**Add a domain** en el panel).
2. En Cloudflare: **Workers & Pages → diverlauro → Custom domains → Set up a custom domain** → `www.diverlauro.es` y `diverlauro.es`.
3. Reemplaza en `index.html`, `sitemap.xml` y `robots.txt` todas las apariciones de `https://diverlauro.pages.dev/` por `https://www.diverlauro.es/`.

## Para salir el primero en Google (lo más importante)

La web ayuda, pero para búsquedas locales ("salón de cumpleaños Alhaurín de la Torre") Google prioriza la **ficha de Google Maps**:

1. **Google Business Profile** (business.google.com): reclamar/verificar la ficha de Diver Lauro, poner categoría principal *Salón de celebraciones* (y secundarias *Parque infantil cubierto*, *Organizador de fiestas infantiles*), horario, la URL de esta web, y **subir fotos con frecuencia**.
2. **Reseñas**: pedir a cada cliente contento que deje una reseña en Google y responderlas todas.
3. **Google Search Console** (search.google.com/search-console): añadir la web, enviar `sitemap.xml` y solicitar indexación.
4. **Mismos datos en todas partes** (nombre, dirección y teléfono idénticos en Google, Instagram, Facebook y directorios).
5. **Redes sociales**: poner el enlace de la web en la bio de Instagram y Facebook, y publicar fiestas con ubicación "Alhaurín de la Torre".
6. Cambiar la antigua web `diverlauro.wordpress.com` para que enlace a esta (o redirija).
