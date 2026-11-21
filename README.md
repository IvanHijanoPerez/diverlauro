# Diver Lauro · Web oficial

Web del salón de celebraciones **Diver Lauro** (Calle Crianza 30, Alhaurín de la Torre, Málaga): cumpleaños, comuniones, bautizos, bodas, despedidas, comidas de empresa y eventos, de día y de noche.

Publicada en **https://diverlauro.com/** (Cloudflare Pages: cada `git push` a `main` se publica solo; también responde en `diverlauro.pages.dev`).

## Qué incluye

- **Identidad de la marca**: amarillo `#EBD450` + azul marino `#0D305D` y el logo original a pincel.
- **Modo día / noche** automático según la hora (noche de 20:00 a 7:00), con interruptor. Recuerda la elección del visitante.
- **Animaciones ligeras** (solo CSS, sin librerías): globos que se explotan al tocarlos, confeti, bola de discoteca de noche, apariciones al hacer scroll. Se pausan cuando no se ven y respetan "reducir movimiento".
- **Páginas por celebración** (para salir en Google con cada búsqueda):
  - `/cumpleanos-infantiles-alhaurin-de-la-torre/`
  - `/comuniones-bautizos-alhaurin-de-la-torre/`
  - `/despedidas-fiestas-noche-alhaurin-de-la-torre/`
  - `/comidas-empresa-eventos-alhaurin-de-la-torre/`
- **Guías "Ideas para tu fiesta"** en `/ideas/` (cumpleaños infantil, comunión o bautizo, despedidas, comida de empresa): contenido útil que atrae visitas desde Google. Se editan en `tools/ideas.py`.
- **Contacto por cualquier canal**: WhatsApp, correo, Instagram, Facebook y teléfono.
- **Formulario → WhatsApp** con tipo de celebración, fecha, horario e invitados. No necesita servidor ni guarda datos.
- **SEO local**: datos estructurados `LocalBusiness`/`EventVenue`, `Service`, `BreadcrumbList` y `FAQPage`; Open Graph; `sitemap.xml`; `robots.txt`.
- **Kit de Instagram** en `redes-sociales/` (ver `redes-sociales/LEEME.md`).

## Estructura

```
tools/build.py        GENERA la portada, las páginas de celebración y las guías (textos, FAQ, SEO, reseñas)
tools/ideas.py        Textos de las guías de /ideas/
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

### Reseñas de Google (automáticas)

La función `functions/api/resenas.js` (Cloudflare Pages Functions) pide a Google la nota, el número de reseñas y hasta 5 reseñas (Places API New). Guarda una copia global en Cloudflare KV que se renueva cada 24 h y tiene un **límite duro de 2 consultas a Google al día** (como mucho unas 60/mes; lo normal es 1 al día). La portada las muestra solas en «Opiniones» (solo las de 4–5 estrellas con texto). Si no hay clave o Google falla, la web sigue mostrando la nota fija (4,5 · 175).

Configuración (una sola vez):
1. Google Cloud → proyecto → activar **Places API (New)** → crear **clave de API** restringida a esa API.
2. Cloudflare → **Storage & Databases → KV** → crear el namespace `diverlauro-resenas`.
3. Cloudflare → Workers & Pages → diverlauro → **Settings → Bindings** → añadir *KV namespace* con nombre de variable `RESENAS_KV` y el namespace anterior.
4. En **Settings → Variables and Secrets** → añadir el secreto `GOOGLE_PLACES_KEY` (Production) y volver a desplegar.
5. Opcional: `GOOGLE_PLACE_ID` con el ID del negocio (si no, se busca por nombre).

Para comprobarlo: abrir `https://diverlauro.com/api/resenas`.

Además, en `tools/build.py` hay una lista `REVIEWS` para poner reseñas fijas a mano (formato: `("Nombre", 5, "Texto tal cual", "hace 2 meses")`).

### Fotos nuevas

Ahora mismo la web solo usa fotos actuales del local: parque de bolas, rincón infantil, office y fachada. Cuando haya fotos nuevas, se guardan en `img/fotos/` en dos tamaños (`nombre.webp` de ~1600 px y `nombre-sm.webp` de ~800 px), sin datos GPS, y se añaden en `tools/build.py`.

## Dominio y correo

- Dominio **`diverlauro.com`** comprado en IONOS, con el DNS gestionado en **Cloudflare** (nameservers `coraline` y `guy.ns.cloudflare.com`).
- La web está conectada en Cloudflare → Workers & Pages → diverlauro → **Custom domains** (`diverlauro.com` y `www.diverlauro.com`).
- El correo `info@diverlauro.com` es de **IONOS**. En el DNS de Cloudflare **no hay que borrar** estos registros (todos en *DNS only*):
  `MX mx00.ionos.es` y `mx01.ionos.es`, `TXT v=spf1 include:_spf-eu.ionos.com ~all`, `CNAME s1-ionos._domainkey → s1.dkim.ionos.com`, `CNAME s2-ionos._domainkey → s2.dkim.ionos.com`, `CNAME autodiscover → adsredir.ionos.info`, `CNAME _dmarc → dmarc.ionos.es`.
- Si algún día cambia la dirección, edita `SITE` en `tools/build.py`, ejecuta `python tools/build.py` y sube los cambios.

## Para salir los primeros en Google

Para búsquedas locales ("salón de celebraciones Alhaurín de la Torre", "cumpleaños infantiles Alhaurín") Google enseña primero el **mapa con 3 negocios**. Eso depende sobre todo de la **ficha de Google Maps**:

1. **Ficha de Google (business.google.com)**:
   - Categoría principal **Salón de eventos** / *Salón de celebraciones*; secundarias: *Parque infantil cubierto*, *Organizador de fiestas infantiles*, *Lugar para fiestas*.
   - **Sitio web**: `https://diverlauro.com/` · **Teléfono**: 647 91 30 22 · **Horario** real (día y noche).
   - **Descripción** con las palabras clave: salón de celebraciones en Alhaurín de la Torre, cumpleaños, comuniones, despedidas, comidas de empresa, parque de bolas.
   - **Fotos nuevas** cada semana (Google premia las fichas activas) y **publicaciones** (novedades, fechas libres).
   - **Servicios**: añadir cumpleaños infantiles, comuniones y bautizos, despedidas, comidas de empresa.
2. **Reseñas**: pedirla al terminar cada fiesta (enlace directo desde la ficha → "Pedir reseñas") y **responder todas**, también las negativas.
3. **Google Search Console** (search.google.com/search-console): añadir la web, enviar `sitemap.xml` y pedir indexación de la portada y las 4 páginas.
4. **Mismos datos en todas partes**: nombre, dirección y teléfono idénticos en Google, Instagram, Facebook y directorios.
5. **Enlaces**: web en la bio de Instagram y Facebook; pedir a la web antigua (`diverlauro.wordpress.com`) que enlace a la nueva.
