# Diver Lauro · Web oficial

Web del salón de celebraciones **Diver Lauro** (Calle Crianza 30, Alhaurín de la Torre, Málaga): cumpleaños, comuniones, bautizos, bodas, despedidas, comidas de empresa y eventos, de día y de noche.

Publicada en **https://diverlauro.pages.dev/** (Cloudflare Pages: cada `git push` a `main` se publica solo).

## Qué incluye

- **Identidad de la marca**: amarillo `#EBD450` + azul marino `#0D305D` y el logo original a pincel.
- **Modo día / noche** automático según la hora (noche de 20:00 a 7:00), con interruptor. Recuerda la elección del visitante.
- **Animaciones ligeras** (solo CSS, sin librerías): globos que se explotan al tocarlos, confeti, bola de discoteca de noche, apariciones al hacer scroll. Se pausan cuando no se ven y respetan "reducir movimiento".
- **Páginas por celebración** (para salir en Google con cada búsqueda):
  - `/cumpleanos-infantiles-alhaurin-de-la-torre/`
  - `/comuniones-bautizos-alhaurin-de-la-torre/`
  - `/despedidas-fiestas-noche-alhaurin-de-la-torre/`
  - `/comidas-empresa-eventos-alhaurin-de-la-torre/`
- **Formulario → WhatsApp** con tipo de celebración, fecha, horario e invitados. No necesita servidor ni guarda datos.
- **SEO local**: datos estructurados `LocalBusiness`/`EventVenue`, `Service`, `BreadcrumbList` y `FAQPage`; Open Graph; `sitemap.xml`; `robots.txt`.
- **Kit de Instagram** en `redes-sociales/` (ver `redes-sociales/LEEME.md`).

## Estructura

```
tools/build.py        GENERA la portada y las páginas de celebración (textos, FAQ, SEO)
tools/redes.py        GENERA el kit de Instagram (PNG) desde plantillas HTML
tools/partials/       Iconos compartidos
index.html            Portada (generada)
<celebración>/        Páginas por tipo de celebración (generadas)
css/styles.css        Estilos, modo día/noche y animaciones
js/main.js            Interacciones (modo, menú, globos, formulario, opiniones)
img/fotos/            Fotos del local (nombre.webp grande, nombre-sm.webp miniatura)
img/redes/            Miniaturas de los posts para la web
redes-sociales/       Posts, historias, destacados, foto de perfil y guía de Instagram
```

## Editar la web

Los textos, preguntas frecuentes y datos de contacto están en **`tools/build.py`**. Después de cambiarlos:

```bash
python tools/build.py
```

Para regenerar los diseños de Instagram (necesita Chrome o Edge instalado):

```bash
python tools/redes.py
```

### Añadir reseñas reales de Google

En `js/main.js`, al principio, rellena `REVIEWS` copiando reseñas **tal cual** de Google:

```js
const REVIEWS = [
  { autor: "María G.", texto: "Texto exacto de la reseña…", estrellas: 5 },
];
```

### Fotos nuevas

Ahora mismo la web solo usa fotos actuales del local: parque de bolas, rincón infantil, office y fachada. Cuando haya fotos nuevas, se guardan en `img/fotos/` en dos tamaños (`nombre.webp` de ~1600 px y `nombre-sm.webp` de ~800 px), sin datos GPS, y se añaden en `tools/build.py`.

## Dominio propio

No es obligatorio para salir en Google, pero sí recomendable: un `diverlauro.es` da más confianza, se recuerda mejor y conviene tenerlo **antes** de que Google indexe mucho la dirección `pages.dev` (cambiar de dirección después hace perder algo de posicionamiento durante unas semanas).

1. Comprar el dominio (DonDominio, Dinahosting…, ~10 €/año) y apuntar sus *nameservers* a Cloudflare.
2. Cloudflare → Workers & Pages → diverlauro → **Custom domains** → `diverlauro.es` y `www.diverlauro.es`.
3. Cambiar `SITE` en `tools/build.py`, ejecutar `python tools/build.py` y subir los cambios.

## Para salir los primeros en Google

Para búsquedas locales ("salón de celebraciones Alhaurín de la Torre", "cumpleaños infantiles Alhaurín") Google enseña primero el **mapa con 3 negocios**. Eso depende sobre todo de la **ficha de Google Maps**:

1. **Ficha de Google (business.google.com)**:
   - Categoría principal **Salón de eventos** / *Salón de celebraciones*; secundarias: *Parque infantil cubierto*, *Organizador de fiestas infantiles*, *Lugar para fiestas*.
   - **Sitio web**: `https://diverlauro.pages.dev/` · **Teléfono**: 647 91 30 22 · **Horario** real (día y noche).
   - **Descripción** con las palabras clave: salón de celebraciones en Alhaurín de la Torre, cumpleaños, comuniones, despedidas, comidas de empresa, parque de bolas.
   - **Fotos nuevas** cada semana (Google premia las fichas activas) y **publicaciones** (novedades, fechas libres).
   - **Servicios**: añadir cumpleaños infantiles, comuniones y bautizos, despedidas, comidas de empresa.
2. **Reseñas**: pedirla al terminar cada fiesta (enlace directo desde la ficha → "Pedir reseñas") y **responder todas**, también las negativas.
3. **Google Search Console** (search.google.com/search-console): añadir la web, enviar `sitemap.xml` y pedir indexación de la portada y las 4 páginas.
4. **Mismos datos en todas partes**: nombre, dirección y teléfono idénticos en Google, Instagram, Facebook y directorios.
5. **Enlaces**: web en la bio de Instagram y Facebook; pedir a la web antigua (`diverlauro.wordpress.com`) que enlace a la nueva.
