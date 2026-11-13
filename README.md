# Diver Lauro · Web oficial

Web del salón de celebraciones y parque infantil **Diver Lauro**, en Calle Crianza 30, Alhaurín de la Torre (Málaga).

Web estática (HTML + CSS + JS, sin dependencias): rápida, responsive y lista para GitHub Pages.

## Qué incluye

- Hero con **parque de bolas interactivo** (las bolas caen, se apilan y se pueden empujar o lanzar con el ratón o el dedo).
- Secciones: celebraciones, instalaciones, cómo reservar, formulario de consulta, redes sociales, preguntas frecuentes, contacto con mapa.
- **Formulario → WhatsApp**: el cliente rellena nombre, fecha, tipo de evento e invitados y se abre WhatsApp con el mensaje ya escrito. No hace falta servidor ni se guardan datos.
- Botón flotante de WhatsApp, menú móvil animado, animaciones al hacer scroll y respeto a "reducir movimiento".
- **SEO local**: título y descripción optimizados para "salón de celebraciones Alhaurín de la Torre", datos estructurados `LocalBusiness` + `FAQPage` (schema.org), Open Graph para que el enlace se vea bien en WhatsApp/Instagram/Facebook, `sitemap.xml`, `robots.txt`, coordenadas geográficas.

## Estructura

```
index.html          Página principal (todo el contenido y el SEO)
css/styles.css      Estilos y animaciones
js/main.js          Interacciones (menú, animaciones, parque de bolas, formulario)
img/                Favicon, iconos e imagen para redes (og-image.png)
sitemap.xml         Mapa del sitio para Google
robots.txt          Permisos para buscadores
404.html            Página de error
```

## Cambiar datos

Todo está en `index.html`. Busca y reemplaza:

| Dato | Valor actual |
|---|---|
| Teléfono / WhatsApp | `647 91 30 22` · `34647913022` · `+34647913022` |
| Instagram | `https://www.instagram.com/diverlauro/` |
| Facebook | `https://www.facebook.com/Diver-Lauro-193712877866926` |
| Dirección | `Calle Crianza, 30 · 29130 Alhaurín de la Torre` |
| Valoración Google | `4,5` y `175` reseñas (en el hero) |

El número de WhatsApp del formulario está también en `js/main.js` (`WHATSAPP`).

### Añadir fotos reales

Las fotos reales del salón y de fiestas ayudan mucho (a los clientes y a Google). Guárdalas en `img/` en formato `.webp` o `.jpg` (máx. ~300 KB cada una) y añádelas con un texto `alt` descriptivo, p. ej.:

```html
<img src="img/parque-de-bolas.webp" alt="Parque de bolas de Diver Lauro en Alhaurín de la Torre" loading="lazy" width="800" height="600">
```

## Publicar con GitHub Pages

1. En GitHub: **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)`**.
2. En 1–2 minutos estará en `https://ivanhijanoperez.github.io/diverlauro/`.

### Dominio propio (recomendado)

Con un dominio tipo `diverlauro.es` (~10 €/año) se posiciona mejor y da más confianza:

1. Compra el dominio y crea en tu proveedor un registro `CNAME` `www` → `ivanhijanoperez.github.io` (y los registros `A` del dominio raíz a las IP de GitHub Pages).
2. En **Settings → Pages → Custom domain** escribe `www.diverlauro.es` y activa **Enforce HTTPS**.
3. Reemplaza en `index.html`, `sitemap.xml` y `robots.txt` todas las apariciones de `https://ivanhijanoperez.github.io/diverlauro/` por `https://www.diverlauro.es/`, y en `404.html` cambia `/diverlauro/` por `/`.

## Para salir el primero en Google (lo más importante)

La web ayuda, pero para búsquedas locales ("salón de cumpleaños Alhaurín de la Torre") Google prioriza la **ficha de Google Maps**:

1. **Google Business Profile** (business.google.com): reclamar/verificar la ficha de Diver Lauro, poner categoría principal *Salón de celebraciones* (y secundarias *Parque infantil cubierto*, *Organizador de fiestas infantiles*), horario, la URL de esta web, y **subir fotos con frecuencia**.
2. **Reseñas**: pedir a cada cliente contento que deje una reseña en Google y responderlas todas.
3. **Google Search Console** (search.google.com/search-console): añadir la web, enviar `sitemap.xml` y solicitar indexación.
4. **Mismos datos en todas partes** (nombre, dirección y teléfono idénticos en Google, Instagram, Facebook y directorios).
5. **Redes sociales**: poner el enlace de la web en la bio de Instagram y Facebook, y publicar fiestas con ubicación "Alhaurín de la Torre".
6. Cambiar la antigua web `diverlauro.wordpress.com` para que enlace a esta (o redirija).
