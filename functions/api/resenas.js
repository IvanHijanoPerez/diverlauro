/**
 * GET /api/resenas  →  valoración y reseñas de Diver Lauro en Google (Places API New).
 *
 * Variables en Cloudflare Pages (Settings → Variables and Secrets):
 *   GOOGLE_PLACES_KEY  (secreto, obligatorio)  clave de API de Google Cloud con "Places API (New)"
 *   GOOGLE_PLACE_ID    (opcional)              si no se pone, se busca el negocio por nombre
 *
 * La respuesta se guarda 24 h en la caché de Cloudflare: Google recibe muy pocas
 * peticiones al día y no se sale del uso gratuito.
 */
const CACHE_SECONDS = 60 * 60 * 24;
const BUSCAR = "Diver Lauro, Calle Crianza 30, Alhaurín de la Torre";
const MIN_ESTRELLAS = 4;

export async function onRequestGet(context) {
  const { env, request } = context;
  const cache = caches.default;
  // misma clave de caché aunque la URL lleve parámetros
  const cacheKey = new Request(new URL("/api/resenas", request.url).toString(), { method: "GET" });

  const cached = await cache.match(cacheKey);
  if (cached) return cached;

  if (!env.GOOGLE_PLACES_KEY) return json({ error: "sin-clave" }, 503, 300);

  try {
    const headers = { "X-Goog-Api-Key": env.GOOGLE_PLACES_KEY };

    let placeId = env.GOOGLE_PLACE_ID;
    if (!placeId) {
      const s = await fetch("https://places.googleapis.com/v1/places:searchText", {
        method: "POST",
        headers: { ...headers, "Content-Type": "application/json", "X-Goog-FieldMask": "places.id" },
        body: JSON.stringify({ textQuery: BUSCAR, languageCode: "es", regionCode: "ES" }),
      });
      if (!s.ok) throw new Error("busqueda " + s.status);
      const sd = await s.json();
      placeId = sd.places && sd.places[0] && sd.places[0].id;
      if (!placeId) throw new Error("negocio no encontrado");
    }

    const r = await fetch(`https://places.googleapis.com/v1/places/${encodeURIComponent(placeId)}?languageCode=es&regionCode=ES`, {
      headers: { ...headers, "X-Goog-FieldMask": "rating,userRatingCount,googleMapsUri,reviews" },
    });
    if (!r.ok) throw new Error("detalles " + r.status);
    const d = await r.json();

    const data = {
      rating: typeof d.rating === "number" ? d.rating : null,
      total: typeof d.userRatingCount === "number" ? d.userRatingCount : null,
      mapsUri: d.googleMapsUri || null,
      reviews: (d.reviews || [])
        .map((x) => ({
          author: (x.authorAttribution && x.authorAttribution.displayName) || "Cliente de Google",
          authorUri: (x.authorAttribution && x.authorAttribution.uri) || null,
          photo: (x.authorAttribution && x.authorAttribution.photoUri) || null,
          rating: x.rating || 0,
          text: (x.text && x.text.text) || (x.originalText && x.originalText.text) || "",
          when: x.relativePublishTimeDescription || "",
        }))
        .filter((x) => x.text && x.rating >= MIN_ESTRELLAS),
    };

    const res = json(data, 200, CACHE_SECONDS);
    context.waitUntil(cache.put(cacheKey, res.clone()));
    return res;
  } catch (e) {
    return json({ error: "no-disponible", detalle: String(e && e.message || e) }, 502, 600);
  }
}

function json(obj, status, maxAge) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": `public, max-age=${maxAge}`,
    },
  });
}
