"""Genera la web de Diver Lauro: portada (index.html) y páginas por tipo de celebración.

Uso:  python tools/build.py
Edita los textos aquí y vuelve a ejecutarlo. No necesita librerías externas.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://diverlauro.pages.dev"  # cámbialo cuando tengáis dominio propio (sin barra final)
PHONE = "647 91 30 22"
PHONE_INTL = "+34647913022"
WA = "34647913022"
INSTAGRAM = "https://www.instagram.com/diverlauro/"
FACEBOOK = "https://www.facebook.com/Diver-Lauro-193712877866926"
MAPS_DIR = "https://www.google.com/maps/dir/?api=1&amp;destination=36.6574069%2C-4.5781131"
MAPS_REVIEWS = "https://www.google.com/maps/search/?api=1&amp;query=Diver+Lauro+Alhaur%C3%ADn+de+la+Torre"
FONTS = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Kaushan+Script&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap"


def wa(text: str) -> str:
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(text)}"


WA_DEFAULT = wa("Hola, me gustaría información para celebrar en Diver Lauro")

EXTRA_ICONS = """      <symbol id="i-calendar" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></symbol>
      <symbol id="i-sofa" viewBox="0 0 24 24"><path d="M20 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v3"/><path d="M2 16a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v1.5a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5V11a2 2 0 0 0-4 0z"/><path d="M4 18v2M20 18v2"/></symbol>
      <symbol id="i-palette" viewBox="0 0 24 24"><circle cx="13.5" cy="6.5" r="1.5"/><circle cx="17.5" cy="10.5" r="1.5"/><circle cx="8.5" cy="7.5" r="1.5"/><circle cx="6.5" cy="12.5" r="1.5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.93 0 1.65-.75 1.65-1.69 0-.44-.18-.84-.44-1.13-.29-.29-.44-.65-.44-1.13a1.64 1.64 0 0 1 1.67-1.67h2c3.05 0 5.56-2.5 5.56-5.56C21.97 6.01 17.46 2 12 2z"/></symbol>
"""
SPRITE = (ROOT / "tools/partials/sprite.html").read_text(encoding="utf-8").replace("    </defs>", EXTRA_ICONS + "    </defs>")


def ic(name: str) -> str:
    return f'<svg class="ic"><use href="#i-{name}"/></svg>'


# ---------------------------------------------------------------------------
# Celebraciones: cada una tiene su página propia (bueno para Google)
# ---------------------------------------------------------------------------
PAGES = [
    {
        "slug": "cumpleanos-infantiles-alhaurin-de-la-torre",
        "card": "Cumpleaños infantiles", "icon": "cake", "color": "#F25C54",
        "card_text": "Parque de bolas, tobogán y juegos para que los peques no paren.",
        "title": "Cumpleaños infantiles en Alhaurín de la Torre con parque de bolas | Diver Lauro",
        "desc": "Celebra el cumpleaños de tus hijos en Diver Lauro (Alhaurín de la Torre): parque de bolas con tobogán, rincón infantil, futbolín y salón climatizado para las familias. Reserva por WhatsApp.",
        "h1": "Cumpleaños infantiles en Alhaurín de la Torre",
        "kicker": "Fiestas infantiles",
        "lead": "Un salón para que los peques jueguen sin parar y los mayores estén cómodos: parque de bolas con tobogán, juegos y sitio de sobra para la merienda y la tarta.",
        "photo": ("parque-bolas", "Parque de bolas con tobogán de Diver Lauro", 1600, 960),
        "wa": "Hola, me gustaría información para celebrar un cumpleaños infantil en Diver Lauro",
        "features": [
            ("game", "Parque de bolas y tobogán", "La zona favorita de los niños, siempre a la vista de los padres."),
            ("heart", "Rincón infantil", "Mesita, sillas y pizarra para los más pequeños."),
            ("users", "Sitio para los adultos", "Mesas y sillas para merendar tranquilos mientras ellos juegan."),
            ("utensils", "Office equipado", "Frigorífico y microondas para la tarta, las bebidas y la comida."),
            ("music", "Música y TV", "Pon su canción favorita y que empiece la fiesta."),
            ("snow", "Climatizado", "Cómodo en verano y en invierno."),
        ],
        "faq": [
            ("¿Qué tiene el salón para un cumpleaños infantil?", "Parque de bolas con tobogán, rincón infantil, futbolín y pimpón para los niños, y mesas y sillas, equipo de sonido, TV y zona de office con frigorífico y microondas para los mayores. Todo climatizado."),
            ("¿Cómo reservo el cumpleaños?", f"Escríbenos por WhatsApp o llámanos al {PHONE} con la fecha, el horario y el número aproximado de niños y adultos. Te confirmamos disponibilidad y precio."),
            ("¿Puedo decorar el salón?", "Claro: globos, manteles, mesa dulce, piñata… Cuéntanos tu idea y te ayudamos a organizarla."),
            ("¿Dónde está Diver Lauro?", "En la Calle Crianza, 30, 29130 Alhaurín de la Torre (Málaga), a pocos minutos de Málaga capital, Churriana y Alhaurín el Grande."),
        ],
    },
    {
        "slug": "comuniones-bautizos-alhaurin-de-la-torre",
        "card": "Comuniones y bautizos", "icon": "heart", "color": "#2B7BE4",
        "card_text": "Comidas en familia con los niños jugando a la vista.",
        "title": "Salón para comuniones y bautizos en Alhaurín de la Torre | Diver Lauro",
        "desc": "Salón para comuniones, bautizos y celebraciones familiares en Alhaurín de la Torre (Málaga). Mesas para toda la familia, zona de juegos para los niños, sonido y climatización. Reserva por WhatsApp.",
        "h1": "Comuniones y bautizos en Alhaurín de la Torre",
        "kicker": "Celebraciones familiares",
        "lead": "Para los días importantes: espacio para montar mesas largas para toda la familia mientras los niños juegan en el parque de bolas. También bodas íntimas, aniversarios y reuniones.",
        "panel": ("heart", "#2B7BE4", "Comuniones · Bautizos · Bodas · Aniversarios"),
        "wa": "Hola, me gustaría información para celebrar una comunión o bautizo en Diver Lauro",
        "features": [
            ("users", "Mesas para todos", "Montamos las mesas como mejor os venga: imperiales o por grupos."),
            ("game", "Los niños, entretenidos", "Parque de bolas, futbolín y pimpón para que los peques disfruten."),
            ("palette", "Decóralo a tu gusto", "Manteles, centros, globos, mesa dulce… a tu estilo."),
            ("utensils", "Office equipado", "Frigorífico y microondas para la comida y las bebidas."),
            ("music", "Sonido y TV", "Para la música y el vídeo de fotos del protagonista."),
            ("snow", "Climatizado", "Cómodo en cualquier época del año."),
        ],
        "faq": [
            ("¿Cabemos todos?", "La sala es amplia y diáfana. Dinos cuántos invitados sois y te confirmamos cómo montar las mesas."),
            ("¿Se pueden celebrar bodas y aniversarios?", "Sí. Además de comuniones y bautizos celebramos bodas íntimas, aniversarios y reuniones familiares."),
            ("¿Puedo decorar el salón?", "Claro. Cada familia lo decora a su manera: colores, centros de mesa, globos o photocall."),
            ("¿Cómo reservo?", f"Escríbenos por WhatsApp o llámanos al {PHONE} con la fecha, el horario y el número de invitados. Te confirmamos disponibilidad y precio."),
        ],
    },
    {
        "slug": "despedidas-fiestas-noche-alhaurin-de-la-torre",
        "card": "Despedidas y fiestas de noche", "icon": "glass", "color": "#9B5DE5",
        "card_text": "Despedidas de soltera y soltero, cumpleaños de adultos y fiestas privadas.",
        "title": "Local para despedidas y fiestas de noche en Alhaurín de la Torre | Diver Lauro",
        "desc": "¿Despedida de soltera o soltero, cumpleaños de adultos o fiesta privada? Diver Lauro abre también de noche en Alhaurín de la Torre: música, espacio para bailar y salón climatizado. Reserva por WhatsApp.",
        "h1": "Despedidas y fiestas de noche en Alhaurín de la Torre",
        "kicker": "De noche",
        "lead": "¿Despedida de soltera o soltero, unos 40 o una fiesta con amigos? Diver Lauro también abre de noche: un salón para tu grupo con música y espacio para bailar.",
        "panel": ("glass", "#7A3CFF", "Despedidas · Cumpleaños · Fiestas privadas"),
        "night": True,
        "wa": "Hola, me gustaría información para una fiesta de noche o despedida en Diver Lauro",
        "features": [
            ("moon", "Horario de noche", "Celebra cuando más te apetezca: consúltanos el horario para tu fecha."),
            ("speaker", "Equipo de sonido", "Pon vuestra música y a darlo todo."),
            ("sofa", "Espacio para bailar", "Sala diáfana para montar la fiesta como queráis."),
            ("utensils", "Office con frigorífico", "Para las bebidas, la cena y la tarta."),
            ("palette", "Decoración libre", "Globos, photocall, temática… a vuestro gusto."),
            ("snow", "Climatizado", "Para que nadie pase calor bailando."),
        ],
        "faq": [
            ("¿Abrís de noche?", "Sí, tenemos horario de día y de noche. Dinos tu fecha y te confirmamos el horario disponible."),
            ("¿Podemos poner nuestra música?", "Sí, el salón tiene equipo de sonido y TV para vuestra música y vídeos."),
            ("¿Qué tipo de fiestas se hacen de noche?", "Despedidas de soltera y soltero, cumpleaños de adultos, aniversarios, cenas de Navidad y fiestas privadas."),
            ("¿Cómo reservo?", f"Escríbenos por WhatsApp o llámanos al {PHONE} con la fecha, el horario y cuántos sois."),
        ],
    },
    {
        "slug": "comidas-empresa-eventos-alhaurin-de-la-torre",
        "card": "Empresas, peñas y eventos", "icon": "briefcase", "color": "#16B39A",
        "card_text": "Comidas y cenas de empresa, Navidad, asociaciones y reuniones.",
        "title": "Salón para comidas de empresa y eventos en Alhaurín de la Torre | Diver Lauro",
        "desc": "Comidas y cenas de empresa, cenas de Navidad, peñas, asociaciones y reuniones en Alhaurín de la Torre (Málaga). Salón amplio y climatizado con sonido y TV, de día o de noche.",
        "h1": "Comidas de empresa y eventos en Alhaurín de la Torre",
        "kicker": "Empresas y grupos",
        "lead": "Comidas y cenas de empresa, cenas de Navidad, peñas, asociaciones o encuentros: un salón amplio y climatizado en Alhaurín de la Torre, de día o de noche.",
        "panel": ("briefcase", "#16B39A", "Empresas · Navidad · Peñas · Asociaciones"),
        "wa": "Hola, me gustaría información para una comida o evento de empresa en Diver Lauro",
        "features": [
            ("users", "Sala diáfana", "Montaje de mesas a medida de tu grupo."),
            ("speaker", "Sonido y TV", "Para música, vídeos o una presentación."),
            ("calendar", "De día o de noche", "Comidas, cenas o eventos: adaptamos el horario."),
            ("utensils", "Office equipado", "Frigorífico y microondas para catering y bebidas."),
            ("pin", "Bien comunicado", "En Alhaurín de la Torre, a minutos de Málaga capital."),
            ("snow", "Climatizado", "Cómodo en cualquier época del año."),
        ],
        "faq": [
            ("¿Hacéis cenas de empresa y de Navidad?", "Sí. Tenemos horario de día y de noche para comidas, cenas de Navidad y eventos de empresa."),
            ("¿Se puede usar la TV para una presentación?", "El salón tiene TV y equipo de sonido. Dinos qué necesitas conectar y te lo confirmamos."),
            ("¿También para peñas y asociaciones?", "Claro: encuentros, peñas, asociaciones culturales y cualquier evento de grupo."),
            ("¿Cómo reservo?", f"Escríbenos por WhatsApp o llámanos al {PHONE} con la fecha, el horario y el número de asistentes."),
        ],
    },
]

# tarjetas extra de la portada que enlazan a páginas existentes
EXTRA_CARDS = [
    ("Bodas y aniversarios", "glass", "#E0B526", "Celebraciones íntimas con mesa presidencial y mesa dulce.", PAGES[1]["slug"]),
    ("Cumpleaños de adultos", "spark", "#FF4FD8", "De 18, de 40 o de 90: música, tarta y a celebrarlo.", PAGES[2]["slug"]),
]


# ---------------------------------------------------------------------------
# Partes comunes
# ---------------------------------------------------------------------------
def head(title, desc, path, jsonld, og_image="/img/og-image.jpg"):
    url = SITE + path
    ld = "\n".join(f'  <script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n  </script>' for x in jsonld)
    return f"""<!doctype html>
<html lang="es" data-mode="day">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#EBD450">
  <meta name="geo.region" content="ES-MA">
  <meta name="geo.placename" content="Alhaurín de la Torre">
  <meta name="geo.position" content="36.6574069;-4.5781131">
  <meta name="ICBM" content="36.6574069, -4.5781131">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Diver Lauro">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE}{og_image}">
  <link rel="icon" href="/img/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="icon" href="/img/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="/css/styles.css">
  <script>
    (function () {{
      var m; try {{ m = localStorage.getItem("dl-mode"); }} catch (e) {{}}
      if (m !== "day" && m !== "night") {{ var h = new Date().getHours(); m = (h >= 20 || h < 7) ? "night" : "day"; }}
      document.documentElement.dataset.mode = m;
    }})();
  </script>
{ld}
</head>"""


def header(home: bool):
    p = "" if home else "/"
    links = [("celebraciones", "Celebraciones"), ("dia-noche", "Día y noche"), ("local", "El local"),
             ("opiniones", "Opiniones"), ("reservar", "Reservar"), ("contacto", "Contacto")]
    nav = "\n".join(f'        <a href="{p}#{k}">{v}</a>' for k, v in links)
    return f"""<body>
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
{SPRITE}
  <header class="site-header" id="top">
    <div class="container header-inner">
      <a class="brand" href="/" aria-label="Diver Lauro, inicio">
        <img class="logo logo-day" src="/img/logo.webp" alt="Diver Lauro" width="1400" height="295">
        <img class="logo logo-night" src="/img/logo-yellow.webp" alt="" width="1400" height="295" aria-hidden="true">
      </a>
      <nav class="nav" id="nav" aria-label="Principal">
{nav}
        <a class="btn btn-primary nav-cta" href="{WA_DEFAULT}" target="_blank" rel="noopener">{ic("chat")} WhatsApp</a>
      </nav>
      <div class="header-tools">
        <button class="mode-btn" type="button" data-mode-toggle aria-label="Cambiar a modo noche" title="Día / noche">
          <span class="mode-btn-track">{ic("sun").replace('class="ic"', 'class="ic ic-sun"')}{ic("moon").replace('class="ic"', 'class="ic ic-moon"')}</span>
        </button>
        <button class="menu-toggle" aria-controls="nav" aria-expanded="false" aria-label="Abrir menú">
          {ic("menu").replace('class="ic"', 'class="ic ic-open"')}
          {ic("close").replace('class="ic"', 'class="ic ic-close"')}
        </button>
      </div>
    </div>
  </header>
"""


def cta(text_wa=WA_DEFAULT):
    return f"""    <section class="cta" aria-labelledby="cta-title">
      <div class="cta-confetti" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
      <div class="container cta-inner reveal">
        <img class="cta-logo" src="/img/logo.webp" alt="" width="1400" height="295" loading="lazy">
        <h2 id="cta-title">¿Montamos la fiesta?</h2>
        <p>De día o de noche, para 10 o para 100. Escríbenos y reserva tu fecha.</p>
        <div class="hero-actions">
          <a class="btn btn-dark btn-lg" href="{text_wa}" target="_blank" rel="noopener">{ic("chat")} Escribir por WhatsApp</a>
          <a class="btn btn-outline-dark btn-lg" href="tel:{PHONE_INTL}">{ic("phone")} {PHONE}</a>
        </div>
      </div>
    </section>
"""


def footer():
    cel = "\n".join(f'        <a href="/{p["slug"]}/">{p["card"]}</a>' for p in PAGES)
    return f"""  <footer class="footer">
    <div class="container footer-inner">
      <div>
        <img class="footer-logo" src="/img/logo-yellow.webp" alt="Diver Lauro" width="1400" height="295" loading="lazy">
        <p class="footer-text">Salón de celebraciones en Alhaurín de la Torre, Málaga. Cumpleaños, comuniones, bodas, despedidas y eventos, de día y de noche.</p>
      </div>
      <nav class="footer-nav" aria-label="Celebraciones">
{cel}
        <a href="/#reservar">Reservar</a>
        <a href="/#contacto">Contacto</a>
      </nav>
      <div class="footer-social">
        <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram de Diver Lauro">{ic("instagram")}</a>
        <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook de Diver Lauro">{ic("facebook")}</a>
        <a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp de Diver Lauro">{ic("chat")}</a>
      </div>
    </div>
    <div class="container footer-bottom">
      <p>© <span id="year">2026</span> Diver Lauro · Calle Crianza, 30 · 29130 Alhaurín de la Torre (Málaga) · {PHONE}</p>
    </div>
  </footer>

  <a class="wa-float" href="{WA_DEFAULT}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{ic("chat")}</a>

  <script src="/js/main.js" defer></script>
</body>
</html>
"""


def faq_html(items, delay=0.04):
    out = []
    for i, (q, a) in enumerate(items):
        out.append(f"""          <details class="reveal" style="--d:{delay * (i + 1):.2f}s">
            <summary>{q}{ic("plus")}</summary>
            <div class="faq-a"><p>{a}</p></div>
          </details>""")
    return "\n".join(out)


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


BUSINESS_LD = {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "EventVenue"],
    "@id": f"{SITE}/#negocio",
    "name": "Diver Lauro",
    "alternateName": "Diver Lauro Salón de Celebraciones",
    "description": "Salón de celebraciones en Alhaurín de la Torre (Málaga) para cumpleaños, comuniones, bautizos, bodas, despedidas de soltero/a, comidas de empresa y eventos privados, de día y de noche. Con parque de bolas, equipo de sonido y salón climatizado.",
    "url": f"{SITE}/",
    "logo": f"{SITE}/img/logo.png",
    "image": [f"{SITE}/img/og-image.jpg", f"{SITE}/img/fotos/parque-bolas.webp", f"{SITE}/img/fotos/fachada.webp"],
    "telephone": PHONE_INTL,
    "priceRange": "€€",
    "address": {"@type": "PostalAddress", "streetAddress": "Calle Crianza, 30", "addressLocality": "Alhaurín de la Torre",
                "addressRegion": "Málaga", "postalCode": "29130", "addressCountry": "ES"},
    "geo": {"@type": "GeoCoordinates", "latitude": 36.6574069, "longitude": -4.5781131},
    "hasMap": "https://www.google.com/maps/search/?api=1&query=36.6574069%2C-4.5781131",
    "areaServed": ["Alhaurín de la Torre", "Alhaurín el Grande", "Churriana", "Cártama", "Benalmádena", "Torremolinos", "Málaga"],
    "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in
                       ["Parque de bolas y tobogán", "Futbolín y mesa de pimpón", "Equipo de sonido y TV",
                        "Zona de office con frigorífico y microondas", "Aire acondicionado"]],
    "sameAs": [INSTAGRAM, FACEBOOK],
}

HOME_FAQ = [
    ("¿Qué celebraciones se pueden hacer en Diver Lauro?", "De todo: cumpleaños infantiles y de adultos, comuniones, bautizos, bodas y aniversarios, despedidas de soltero/a, comidas y cenas de empresa, reuniones familiares, peñas y eventos privados."),
    ("¿Se pueden hacer fiestas de noche?", "Sí. Tenemos horario de día y de noche: desde una merienda infantil hasta una cena o una fiesta nocturna. Consúltanos el horario para tu fecha."),
    ("¿Cómo reservo el salón?", f"Escríbenos por WhatsApp o llámanos al {PHONE} con la fecha, el horario, el tipo de celebración y el número aproximado de invitados. Te confirmamos disponibilidad y precio."),
    ("¿Qué incluye el salón?", "Sala amplia con mesas y sillas, parque de bolas con tobogán, futbolín, pimpón, rincón infantil, equipo de sonido y TV, zona de office con frigorífico y microondas, tronas, aseos y aire acondicionado."),
    ("¿Puedo decorarlo a mi gusto?", "¡Claro! Globos, manteles, mesas dulces, photocalls… Cuéntanos tu idea y te ayudamos."),
    ("¿Dónde está Diver Lauro?", "En la Calle Crianza, 30, 29130 Alhaurín de la Torre (Málaga), a pocos minutos de Málaga capital, Churriana y Alhaurín el Grande."),
]


# ---------------------------------------------------------------------------
# Portada
# ---------------------------------------------------------------------------
BALLOONS = [(58, 22, 120, "#F25C54", "#E8B84A", 0.0, 7), (68, 10, 100, "#FFFFFF", "#D6DAE6", 0.15, 8),
            (78, 26, 130, "#0D305D", "#1B1B22", 0.3, 9), (89, 12, 96, "#FF7AB6", "#FF4FD8", 0.45, 7.5),
            (63, 47, 110, "#2B7BE4", "#7A3CFF", 0.6, 8.5), (74, 53, 90, "#FFFFFF", "#E8B84A", 0.75, 6.5),
            (85, 43, 116, "#F25C54", "#D6DAE6", 0.9, 9.5), (94, 60, 84, "#0D305D", "#E8B84A", 1.05, 7),
            (54, 63, 80, "#16B39A", "#FF4FD8", 1.2, 8)]


def hero_fx():
    b = "\n".join(f'        <span class="balloon" style="--x:{x}%;--y:{y}%;--s:{s}px;--c:{c};--cn:{cn};--delay:{d}s;--dur:{du}s"><span></span></span>'
                  for x, y, s, c, cn, d, du in BALLOONS)
    return f"""      <div class="hero-fx" aria-hidden="true">
        <div class="hero-disco"><span class="disco-ball"></span><i></i><i></i><i></i></div>
{b}
        <div class="confetti">{"<i></i>" * 14}</div>
      </div>"""


def cel_cards():
    cards = [(p["card"], p["icon"], p["color"], p["card_text"], p["slug"]) for p in PAGES[:2]] + [EXTRA_CARDS[0]] + \
            [(PAGES[2]["card"], PAGES[2]["icon"], PAGES[2]["color"], PAGES[2]["card_text"], PAGES[2]["slug"]), EXTRA_CARDS[1],
             (PAGES[3]["card"], PAGES[3]["icon"], PAGES[3]["color"], PAGES[3]["card_text"], PAGES[3]["slug"])]
    out = []
    for i, (t, icon, color, text, slug) in enumerate(cards):
        out.append(f"""          <a class="cel-card reveal tilt" style="--d:{0.05 + i * 0.06:.2f}s;--c:{color}" href="/{slug}/">
            <span class="cel-ic">{ic(icon)}</span>
            <h3>{t}</h3>
            <p>{text}</p>
            <span class="cel-more">Ver más {ic("arrow")}</span>
          </a>""")
    return "\n".join(out)


def stars():
    return ic("star") * 4 + ic("star").replace('class="ic"', 'class="ic half"')


def build_home():
    ld = [BUSINESS_LD, faq_ld(HOME_FAQ)]
    html = head("Diver Lauro · Salón de celebraciones en Alhaurín de la Torre (Málaga)",
                f"Diver Lauro, salón de celebraciones en Alhaurín de la Torre (Málaga). Cumpleaños, comuniones, bautizos, bodas, despedidas y comidas de empresa, de día y de noche. Parque de bolas, sonido y salón climatizado. Reserva: {PHONE}.",
                "/", ld)
    html += header(True)
    html += f"""
  <main id="contenido">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-sky" aria-hidden="true"><div class="sun"></div><div class="stars"></div></div>
{hero_fx()}
      <div class="container hero-inner">
        <h1 id="hero-title">
          <span class="eyebrow reveal">{ic("pin")} Salón de celebraciones en Alhaurín de la Torre</span>
          <span class="hero-big">
            <span class="line reveal" style="--d:.08s">Celebra <em class="script">de día</em>.</span>
            <span class="line reveal" style="--d:.18s">Brinda <em class="script">de noche</em>.</span>
          </span>
        </h1>
        <p class="hero-lead reveal" style="--d:.3s">
          Cumpleaños, comuniones, bodas, despedidas, comidas de empresa… Un salón amplio con parque de bolas para los peques
          y espacio de sobra para que los mayores lo den todo. <strong>Tú pones la fiesta, nosotros el sitio.</strong>
        </p>
        <div class="mode-switch reveal" style="--d:.38s" role="group" aria-label="Elige el tipo de fiesta">
          <button type="button" data-set-mode="day">{ic("sun")} Fiesta de día</button>
          <button type="button" data-set-mode="night">{ic("moon")} Fiesta de noche</button>
          <span class="mode-switch-pill" aria-hidden="true"></span>
        </div>
        <div class="hero-actions reveal" style="--d:.46s">
          <a class="btn btn-primary btn-lg" href="#reservar">Consultar fecha {ic("arrow")}</a>
          <a class="btn btn-outline btn-lg" href="tel:{PHONE_INTL}">{ic("phone")} {PHONE}</a>
        </div>
        <a class="rating reveal" style="--d:.54s" href="#opiniones">
          <span class="rating-stars" aria-hidden="true">{stars()}</span>
          <span><strong data-count="4.5" data-decimals="1">4,5</strong> en Google · <strong data-count="175">175</strong>+ reseñas</span>
        </a>
      </div>
      <p class="hero-hint" aria-hidden="true">🎈 Toca los globos</p>
    </section>

    <div class="marquee" aria-hidden="true">
      <div class="marquee-track">
        {("<span>Cumpleaños</span><b>✦</b><span>Comuniones</span><b>✦</b><span>Bautizos</span><b>✦</b><span>Bodas</span><b>✦</b><span>Despedidas de solter@s</span><b>✦</b><span>Comidas de empresa</span><b>✦</b><span>Aniversarios</span><b>✦</b><span>Peñas y eventos</span><b>✦</b><span>Fiestas infantiles</span><b>✦</b>" * 2)}
      </div>
    </div>

    <section class="section" id="celebraciones" aria-labelledby="cel-title">
      <div class="container">
        <div class="section-head">
          <p class="kicker reveal">Un salón, mil celebraciones</p>
          <h2 id="cel-title" class="reveal" style="--d:.08s">El mismo sitio, <span class="script-hl">tu</span> fiesta</h2>
          <p class="section-lead reveal" style="--d:.16s">Cada familia y cada grupo lo transforma a su manera. Elige tu celebración y descubre todo lo que puedes hacer en Diver Lauro.</p>
        </div>
        <div class="cel-grid">
{cel_cards()}
        </div>
      </div>
    </section>

    <section class="section section-alt" id="dia-noche" aria-labelledby="dn-title">
      <div class="container">
        <div class="section-head">
          <p class="kicker reveal">Horario de día y de noche</p>
          <h2 id="dn-title" class="reveal" style="--d:.08s">¿Merienda o fiesta <span class="script-hl">hasta tarde</span>?</h2>
          <p class="section-lead reveal" style="--d:.16s">Diver Lauro abre de día y de noche, así que cabe cualquier plan. Dinos tu fecha y adaptamos el horario a tu celebración.</p>
        </div>
        <div class="dn-grid">
          <article class="dn-card dn-day reveal tilt" style="--d:.05s">
            <div class="dn-deco" aria-hidden="true"><span class="dn-sun"></span><i></i><i></i><i></i></div>
            <span class="dn-badge">{ic("sun")} De día</span>
            <h3>Risas, tarta y parque de bolas</h3>
            <ul>
              <li>{ic("check")} Cumpleaños y fiestas infantiles</li>
              <li>{ic("check")} Comuniones y bautizos</li>
              <li>{ic("check")} Comidas familiares y de empresa</li>
              <li>{ic("check")} Meriendas, baby showers y reuniones</li>
            </ul>
            <button class="btn btn-dark" type="button" data-set-mode="day">Ver la web en modo día {ic("sun")}</button>
          </article>
          <article class="dn-card dn-night reveal tilt" style="--d:.15s">
            <div class="dn-deco" aria-hidden="true"><span class="dn-disco"></span><b></b><b></b><b></b><b></b><b></b><b></b></div>
            <span class="dn-badge">{ic("moon")} De noche</span>
            <h3>Música, brindis y a bailar</h3>
            <ul>
              <li>{ic("check")} Despedidas de soltera y soltero</li>
              <li>{ic("check")} Cumpleaños y aniversarios</li>
              <li>{ic("check")} Cenas de empresa y de Navidad</li>
              <li>{ic("check")} Bodas, peñas y fiestas privadas</li>
            </ul>
            <button class="btn btn-primary" type="button" data-set-mode="night">Ver la web en modo noche {ic("moon")}</button>
          </article>
        </div>
      </div>
    </section>

    <section class="section" id="local" aria-labelledby="local-title">
      <div class="container">
        <div class="section-head">
          <p class="kicker reveal">El local</p>
          <h2 id="local-title" class="reveal" style="--d:.08s">Espacio para todos, <span class="script-hl">sin agobios</span></h2>
          <p class="section-lead reveal" style="--d:.16s">Una sala diáfana y luminosa con zona de juegos, office y todo lo necesario para que tu celebración salga redonda.</p>
        </div>
        <div class="bento">
          <figure class="ph ph-xl reveal" style="--d:.04s">
            <img src="/img/fotos/parque-bolas.webp" alt="Parque de bolas con tobogán y estructuras de colores en Diver Lauro" width="1600" height="960" loading="lazy">
            <figcaption><span class="tag">La estrella para los peques</span><strong>Parque de bolas y tobogán</strong></figcaption>
          </figure>
          <div class="tile-g tile-wide reveal" style="--d:.1s;--c:#0D305D">
            <span class="tile-ic">{ic("users")}</span>
            <strong>Sala amplia y diáfana</strong><span>Mesas y sillas para tus invitados, montadas a tu medida.</span>
          </div>
          <figure class="ph reveal" style="--d:.16s">
            <img src="/img/fotos/rincon-infantil-sm.webp" alt="Rincón infantil con mesa, sillitas y pizarra" width="800" height="450" loading="lazy">
            <figcaption><strong>Rincón infantil</strong></figcaption>
          </figure>
          <figure class="ph reveal" style="--d:.22s">
            <img src="/img/fotos/cocina-sm.webp" alt="Zona de office con frigorífico, microondas y encimera" width="800" height="480" loading="lazy">
            <figcaption><strong>Zona de office</strong></figcaption>
          </figure>
          <div class="tile-g reveal" style="--d:.28s;--c:#9B5DE5">
            <span class="tile-ic">{ic("speaker")}</span>
            <strong>Sonido y TV</strong><span>Tu música y tus vídeos.</span>
          </div>
          <div class="tile-g reveal" style="--d:.34s;--c:#F25C54">
            <span class="tile-ic">{ic("game")}</span>
            <strong>Futbolín y pimpón</strong><span>Partidos para todas las edades.</span>
          </div>
          <div class="tile-g tile-wide reveal" style="--d:.4s;--c:#2B7BE4">
            <span class="tile-ic">{ic("snow")}</span>
            <strong>Climatizado todo el año</strong><span>Aire acondicionado para celebrar cómodos en verano y en invierno.</span>
          </div>
        </div>
        <ul class="chips reveal" style="--d:.1s" aria-label="Equipamiento">
          <li>{ic("snow")} Aire acondicionado</li>
          <li>{ic("speaker")} Equipo de sonido</li>
          <li>{ic("music")} TV</li>
          <li>{ic("utensils")} Frigorífico y microondas</li>
          <li>{ic("users")} Mesas y sillas</li>
          <li>{ic("game")} Futbolín y pimpón</li>
          <li>{ic("heart")} Tronas para bebés</li>
          <li>{ic("check")} Aseos</li>
        </ul>
      </div>
    </section>

    <section class="section section-alt" id="opiniones" aria-labelledby="op-title">
      <div class="container reviews">
        <div class="review-score reveal">
          <p class="kicker">Opiniones</p>
          <h2 id="op-title">Lo que dicen <span class="script-hl">en Google</span></h2>
          <div class="score">
            <span class="score-num" data-count="4.5" data-decimals="1">4,5</span>
            <div>
              <span class="rating-stars big" aria-label="4,5 de 5 estrellas">{stars()}</span>
              <p>Más de <strong>175 reseñas</strong> en Google</p>
            </div>
          </div>
          <div class="review-actions">
            <a class="btn btn-primary" href="{MAPS_REVIEWS}" target="_blank" rel="noopener">{ic("google")} Leer opiniones</a>
            <a class="btn btn-outline" href="{MAPS_REVIEWS}" target="_blank" rel="noopener">¿Celebraste aquí? Déjanos tu opinión</a>
          </div>
        </div>
        <div class="praise">
          <p class="praise-title reveal">Lo que más destacan nuestros clientes</p>
          <ul class="praise-list">
            <li class="reveal tilt" style="--d:.05s"><span class="praise-ic" style="--c:#2B7BE4">{ic("users")}</span><strong>Espacio amplio y bien cuidado</strong><span>Sitio de sobra para mesas, juegos y baile.</span></li>
            <li class="reveal tilt" style="--d:.12s"><span class="praise-ic" style="--c:#F25C54">{ic("heart")}</span><strong>Trato cercano</strong><span>Dueños amables y atentos con cada fiesta.</span></li>
            <li class="reveal tilt" style="--d:.19s"><span class="praise-ic" style="--c:#16B39A">{ic("game")}</span><strong>Los niños lo disfrutan</strong><span>Parque de bolas y juegos para no aburrirse.</span></li>
            <li class="reveal tilt" style="--d:.26s"><span class="praise-ic" style="--c:#E0B526">{ic("snow")}</span><strong>Climatizado</strong><span>Cómodo tanto en verano como en invierno.</span></li>
          </ul>
          <div class="review-cards" id="review-cards" hidden></div>
        </div>
      </div>
    </section>

    <section class="section" id="reservar" aria-labelledby="res-title">
      <div class="container reserve">
        <div class="reserve-copy">
          <p class="kicker reveal">Consulta sin compromiso</p>
          <h2 id="res-title" class="reveal" style="--d:.08s">¿Tienes fecha? <span class="script-hl">Hablemos</span></h2>
          <p class="section-lead reveal" style="--d:.16s">Rellena estos datos y se abrirá WhatsApp con el mensaje listo para enviar. Te contestamos lo antes posible con disponibilidad y precio.</p>
          <ul class="perks reveal" style="--d:.24s">
            <li>{ic("check")} Respuesta rápida por WhatsApp</li>
            <li>{ic("check")} Horario de día o de noche</li>
            <li>{ic("check")} Trato cercano y familiar</li>
          </ul>
        </div>
        <form class="reserve-form reveal" style="--d:.12s" id="reserve-form" novalidate>
          <div class="field">
            <label for="f-name">Tu nombre</label>
            <input id="f-name" name="nombre" type="text" autocomplete="given-name" placeholder="Ej. Laura" required>
          </div>
          <div class="field-row">
            <div class="field">
              <label for="f-type">Celebración</label>
              <select id="f-type" name="tipo">
                <option>Cumpleaños infantil</option><option>Cumpleaños de adulto</option><option>Comunión</option><option>Bautizo</option>
                <option>Boda o aniversario</option><option>Despedida de soltero/a</option><option>Comida o cena de empresa</option>
                <option>Reunión familiar</option><option>Otro evento</option>
              </select>
            </div>
            <div class="field">
              <label for="f-date">Fecha</label>
              <input id="f-date" name="fecha" type="date">
            </div>
          </div>
          <fieldset class="field seg">
            <legend>Horario</legend>
            <div class="seg-opts">
              <label><input type="radio" name="horario" value="De día" checked><span>{ic("sun")} De día</span></label>
              <label><input type="radio" name="horario" value="De noche"><span>{ic("moon")} De noche</span></label>
            </div>
          </fieldset>
          <div class="field-row">
            <div class="field"><label for="f-adults">Adultos (aprox.)</label><input id="f-adults" name="adultos" type="number" min="0" inputmode="numeric" placeholder="30"></div>
            <div class="field"><label for="f-kids">Niños (aprox.)</label><input id="f-kids" name="ninos" type="number" min="0" inputmode="numeric" placeholder="15"></div>
          </div>
          <div class="field">
            <label for="f-msg">¿Algo más? <span class="opt">(opcional)</span></label>
            <textarea id="f-msg" name="mensaje" rows="3" placeholder="Horas, ideas de decoración, dudas…"></textarea>
          </div>
          <button class="btn btn-primary btn-lg btn-block" type="submit">{ic("chat")} Enviar por WhatsApp</button>
          <p class="form-note">Se abrirá WhatsApp con tu mensaje. Esta web no guarda ningún dato.</p>
        </form>
      </div>
    </section>

    <section class="section social" aria-labelledby="social-title">
      <div class="container">
        <div class="social-card reveal">
          <div class="social-copy">
            <p class="kicker kicker-light">Síguenos</p>
            <h2 id="social-title">Ideas para tu fiesta en <span class="script">@diverlauro</span></h2>
            <p>Decoraciones, celebraciones, novedades y fechas libres. Síguenos y llévate ideas para tu próxima fiesta.</p>
            <div class="social-actions">
              <a class="btn btn-light" href="{INSTAGRAM}" target="_blank" rel="noopener">{ic("instagram")} Instagram</a>
              <a class="btn btn-glass" href="{FACEBOOK}" target="_blank" rel="noopener">{ic("facebook")} Facebook</a>
            </div>
          </div>
          <div class="phone-mock" aria-hidden="true">
            <div class="phone">
              <div class="phone-head"><img src="/img/redes/perfil-sm.webp" alt="" width="34" height="34"><b>diverlauro</b></div>
              <div class="phone-grid">
                {"".join(f'<img src="/img/redes/post-{i}-sm.webp" alt="" loading="lazy" width="270" height="338">' for i in range(1, 7))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="preguntas" aria-labelledby="faq-title">
      <div class="container faq-wrap">
        <div class="section-head section-head-left">
          <p class="kicker reveal">Preguntas frecuentes</p>
          <h2 id="faq-title" class="reveal" style="--d:.08s">Lo que más nos <span class="script-hl">preguntáis</span></h2>
          <p class="section-lead reveal" style="--d:.16s">¿No encuentras tu respuesta? Escríbenos y te ayudamos.</p>
          <a class="btn btn-dark reveal" style="--d:.22s" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ic("chat")} Preguntar por WhatsApp</a>
        </div>
        <div class="faq">
{faq_html(HOME_FAQ)}
        </div>
      </div>
    </section>

    <section class="section" id="contacto" aria-labelledby="contact-title">
      <div class="container contact">
        <div class="contact-info">
          <p class="kicker reveal">Contacto</p>
          <h2 id="contact-title" class="reveal" style="--d:.08s">Ven a <span class="script-hl">conocernos</span></h2>
          <figure class="facade reveal" style="--d:.12s">
            <img src="/img/fotos/fachada-sm.webp" alt="Fachada de Diver Lauro con el cartel del salón" width="800" height="450" loading="lazy">
          </figure>
          <address class="contact-list reveal" style="--d:.16s">
            <a class="contact-item" href="{MAPS_DIR}" target="_blank" rel="noopener">
              <span class="contact-ic" style="--c:#F25C54">{ic("pin")}</span>
              <span><small>Dirección</small>Calle Crianza, 30 · 29130 Alhaurín de la Torre</span>
            </a>
            <a class="contact-item" href="tel:{PHONE_INTL}">
              <span class="contact-ic" style="--c:#2B7BE4">{ic("phone")}</span>
              <span><small>Teléfono y WhatsApp</small>{PHONE}</span>
            </a>
            <a class="contact-item" href="{INSTAGRAM}" target="_blank" rel="noopener">
              <span class="contact-ic" style="--c:#D9479B">{ic("instagram")}</span>
              <span><small>Instagram</small>@diverlauro</span>
            </a>
          </address>
        </div>
        <div class="map reveal" style="--d:.12s">
          <iframe title="Mapa de Diver Lauro en Alhaurín de la Torre" src="https://maps.google.com/maps?q=36.6574069,-4.5781131&amp;z=16&amp;hl=es&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
          <a class="btn btn-primary map-btn" href="{MAPS_DIR}" target="_blank" rel="noopener">Cómo llegar {ic("arrow")}</a>
        </div>
      </div>
    </section>

{cta()}  </main>

"""
    html += footer()
    (ROOT / "index.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# Páginas por celebración
# ---------------------------------------------------------------------------
def build_page(p):
    path = f"/{p['slug']}/"
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": p["card"], "item": SITE + path}]},
        {"@context": "https://schema.org", "@type": "Service", "name": p["h1"], "serviceType": p["card"],
         "description": p["desc"], "areaServed": "Alhaurín de la Torre, Málaga",
         "provider": {"@id": f"{SITE}/#negocio", "@type": "LocalBusiness", "name": "Diver Lauro", "telephone": PHONE_INTL,
                      "address": BUSINESS_LD["address"]}, "url": SITE + path},
        faq_ld(p["faq"]),
    ]
    if "photo" in p:
        name, alt, w, h = p["photo"]
        visual = f"""<figure class="page-photo reveal" style="--d:.15s"><img src="/img/fotos/{name}.webp" alt="{alt}" width="{w}" height="{h}"></figure>"""
    else:
        icon, color, label = p["panel"]
        visual = f"""<div class="page-panel reveal{' page-panel-night' if p.get('night') else ''}" style="--d:.15s;--c:{color}" aria-hidden="true">
            <span class="pp-ic">{ic(icon)}</span>
            <span class="pp-b pp-b1"></span><span class="pp-b pp-b2"></span><span class="pp-b pp-b3"></span>
            <span class="pp-label">{label}</span>
          </div>"""
    feats = "\n".join(f"""          <li class="feat reveal tilt" style="--d:{0.04 + i * 0.06:.2f}s"><span class="feat-ic">{ic(icon)}</span><strong>{t}</strong><span>{d}</span></li>"""
                      for i, (icon, t, d) in enumerate(p["features"]))
    others = "\n".join(f"""          <a class="cel-card cel-card-sm reveal" style="--c:{o['color']}" href="/{o['slug']}/"><span class="cel-ic">{ic(o['icon'])}</span><h3>{o['card']}</h3><span class="cel-more">Ver más {ic('arrow')}</span></a>"""
                       for o in PAGES if o is not p)
    wa_link = wa(p["wa"])
    html = head(p["title"], p["desc"], path, ld)
    html += header(False)
    html += f"""
  <main id="contenido">
    <section class="page-hero{' page-hero-night' if p.get('night') else ''}" aria-labelledby="page-title">
      <div class="container page-hero-inner">
        <div>
          <nav class="crumbs reveal" aria-label="Migas de pan"><a href="/">Inicio</a> <span aria-hidden="true">/</span> <span>{p['card']}</span></nav>
          <p class="kicker reveal" style="--d:.05s">{p['kicker']}</p>
          <h1 id="page-title" class="reveal" style="--d:.1s">{p['h1']}</h1>
          <p class="hero-lead reveal" style="--d:.18s">{p['lead']}</p>
          <div class="hero-actions reveal" style="--d:.26s">
            <a class="btn btn-primary btn-lg" href="{wa_link}" target="_blank" rel="noopener">{ic('chat')} Consultar por WhatsApp</a>
            <a class="btn btn-outline btn-lg" href="tel:{PHONE_INTL}">{ic('phone')} {PHONE}</a>
          </div>
          <a class="rating reveal" style="--d:.34s" href="/#opiniones">
            <span class="rating-stars" aria-hidden="true">{stars()}</span>
            <span><strong>4,5</strong> en Google · <strong>175</strong>+ reseñas</span>
          </a>
        </div>
        {visual}
      </div>
    </section>

    <section class="section" aria-labelledby="inc-title">
      <div class="container">
        <div class="section-head">
          <p class="kicker reveal">Qué te ofrecemos</p>
          <h2 id="inc-title" class="reveal" style="--d:.08s">Todo listo para <span class="script-hl">tu fiesta</span></h2>
        </div>
        <ul class="feat-grid">
{feats}
        </ul>
      </div>
    </section>

    <section class="section section-alt" aria-labelledby="steps-title">
      <div class="container">
        <div class="section-head">
          <p class="kicker reveal">Así de fácil</p>
          <h2 id="steps-title" class="reveal" style="--d:.08s">Reserva en <span class="script-hl">3 pasos</span></h2>
        </div>
        <ol class="steps">
          <li class="step reveal" style="--d:.05s"><span class="step-n">1</span><h3>Escríbenos</h3><p>Por WhatsApp o por teléfono: qué celebras, cuándo y cuántos sois.</p></li>
          <li class="step reveal" style="--d:.15s"><span class="step-n">2</span><h3>Elige día y horario</h3><p>De día o de noche. Te confirmamos disponibilidad y precio sin compromiso.</p></li>
          <li class="step reveal" style="--d:.25s"><span class="step-n">3</span><h3>¡A celebrar!</h3><p>Trae la tarta y las ganas. El resto, lo pone Diver Lauro.</p></li>
        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container faq-wrap">
        <div class="section-head section-head-left">
          <p class="kicker reveal">Preguntas frecuentes</p>
          <h2 id="faq-title" class="reveal" style="--d:.08s">Resolvemos tus <span class="script-hl">dudas</span></h2>
          <a class="btn btn-dark reveal" style="--d:.16s" href="{wa_link}" target="_blank" rel="noopener">{ic('chat')} Preguntar por WhatsApp</a>
        </div>
        <div class="faq">
{faq_html(p['faq'])}
        </div>
      </div>
    </section>

    <section class="section section-alt" aria-labelledby="more-title">
      <div class="container">
        <div class="section-head">
          <p class="kicker reveal">También celebramos</p>
          <h2 id="more-title" class="reveal" style="--d:.08s">Otras <span class="script-hl">celebraciones</span></h2>
        </div>
        <div class="cel-grid cel-grid-sm">
{others}
        </div>
      </div>
    </section>

{cta(wa_link)}  </main>

"""
    html += footer()
    out = ROOT / p["slug"] / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")


def build_sitemap():
    from datetime import date
    today = date.today().isoformat()
    urls = [("/", "1.0")] + [(f"/{p['slug']}/", "0.8") for p in PAGES]
    body = "\n".join(f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{pr}</priority>\n  </url>" for u, pr in urls)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /redes-sociales/\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    build_home()
    for page in PAGES:
        build_page(page)
    build_sitemap()
    print("OK:", "index.html +", len(PAGES), "páginas + sitemap.xml + robots.txt")
