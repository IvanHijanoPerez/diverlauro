/**
 * GET /api/resenas  →  valoración y reseñas de Diver Lauro en Google (Places API New).
 *
 * Configuración en Cloudflare Pages (proyecto diverlauro → Settings):
 *   - Variables and Secrets:
 *       GOOGLE_PLACES_KEY  (secreto, obligatorio)  clave de Google Cloud con "Places API (New)"
 *       GOOGLE_PLACE_ID    (opcional)              si no se pone, se busca el negocio por nombre
 *   - Bindings → KV namespace:
 *       RESENAS_KV         (obligatorio)           almacén donde se guarda la copia de las reseñas
 *
 * Protección de costes:
 *   - Una única copia global en KV que se renueva como mucho cada 24 h (Google recibe ~1 consulta al día).
 *   - Límite duro: como mucho MAX_GOOGLE_DIA consultas a Google por día, pase lo que pase.
 *   - Si no hay clave o no hay KV, NUNCA se llama a Google.
 */
const REFRESCO_MS = 24 * 60 * 60 * 1000;
const MAX_GOOGLE_DIA = 2;
const BUSCAR = "Diver Lauro, Calle Crianza 30, Alhaurín de la Torre";
const MIN_ESTRELLAS = 4;

export async function onRequestGet({ env }) {
  if (!env.GOOGLE_PLACES_KEY) return json({ error: "sin-clave" }, 503, 300);
  if (!env.RESENAS_KV) return json({ error: "sin-kv" }, 503, 300);

  const kv = env.RESENAS_KV;
  const guardado = await kv.get("resenas", "json"); // { ts, data }
  const ahora = Date.now();

  if (guardado && ahora - guardado.ts < REFRESCO_MS) {
    return json(guardado.data, 200, 3600);
  }

  // contador diario de llamadas a Google
  const hoy = new Date().toISOString().slice(0, 10);
  const claveContador = "llamadas:" + hoy;
  const llamadas = parseInt((await kv.get(claveContador)) || "0", 10);
  if (llamadas >= MAX_GOOGLE_DIA) {
    return guardado ? json(guardado.data, 200, 3600) : json({ error: "limite" }, 503, 3600);
  }

  try {
    const headers = { "X-Goog-Api-Key": env.GOOGLE_PLACES_KEY };

    let placeId = env.GOOGLE_PLACE_ID || (guardado && guardado.placeId);
    let usadas = 0;
    if (!placeId) {
      usadas++;
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

    usadas++;
    await kv.put(claveContador, String(llamadas + usadas), { expirationTtl: 60 * 60 * 48 });
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

    await kv.put("resenas", JSON.stringify({ ts: ahora, placeId, data }));
    return json(data, 200, 3600);
  } catch (e) {
    // si Google falla, se sirve la última copia buena (aunque sea antigua)
    if (guardado) return json(guardado.data, 200, 600);
    return json({ error: "no-disponible", detalle: String((e && e.message) || e) }, 502, 600);
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
