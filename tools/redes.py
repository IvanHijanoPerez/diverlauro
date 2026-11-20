"""Genera el kit de Instagram de Diver Lauro (posts, historias, destacados y foto de perfil).

Uso:  python tools/redes.py
Crea plantillas HTML editables en redes-sociales/plantillas/ y las exporta a PNG con Chrome (modo headless).
Para cambiar un texto: edita este archivo (o la plantilla HTML) y vuelve a ejecutarlo.
"""
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "redes-sociales"
TPL = OUT / "plantillas"
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium",
]
PHONE = "647 91 30 22"
WEB = "diverlauro.com"

ICONS = {
    "cake": '<path d="M20 21v-8a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8"/><path d="M4 16s.5-1 2-1 2.5 2 4 2 2.5-2 4-2 2.5 2 4 2 2-1 2-1"/><path d="M2 21h20M7 8v3m5-3v3m5-3v3M7 4h.01M12 4h.01M17 4h.01"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>',
    "home": '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "chat": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "glass": '<path d="M8 22h8M12 15v7M12 15a5 5 0 0 0 5-5c0-2-.5-4-2-8H9c-1.5 4-2 6-2 8a5 5 0 0 0 5 5Z"/>',
}


def icon(name, size, color="currentColor", sw=2):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'


BASE_CSS = """
:root { --y:#EBD450; --n:#0D305D; --c:#F25C54; --b:#2B7BE4; --p:#FF4FD8; --m:#16B39A; }
* { box-sizing: border-box; }
html, body { margin: 0; width: var(--w); height: var(--h); overflow: hidden; }
body { position: relative; font-family: "Plus Jakarta Sans", sans-serif; color: var(--n); background: var(--y); }
h1, h2 { font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; letter-spacing: -.04em; line-height: .95; margin: 0; }
.script { font-family: "Kaushan Script", cursive; font-weight: 400; letter-spacing: 0; }
.logo { display: block; }
.b { position: absolute; border-radius: 50% 50% 47% 47% / 55% 55% 45% 45%;
  background-image: radial-gradient(circle at 32% 26%, rgba(255,255,255,.85) 0 5%, rgba(255,255,255,.3) 13%, transparent 34%), radial-gradient(circle at 72% 82%, rgba(0,0,0,.18), transparent 55%);
  box-shadow: inset -14px -20px 40px rgba(0,0,0,.12); }
.b::after { content: ""; position: absolute; left: 50%; top: 100%; width: 3px; height: 70%; background: linear-gradient(rgba(13,48,93,.45), transparent); }
.conf i { position: absolute; width: 18px; height: 32px; border-radius: 4px; }
.pill { display: inline-block; padding: 18px 34px; border-radius: 999px; font-weight: 800; font-size: 34px; }
.foot { position: absolute; left: 0; right: 0; bottom: 56px; display: flex; justify-content: center; gap: 22px; align-items: center; font-weight: 800; font-size: 30px; }
.foot span { display: inline-flex; align-items: center; gap: 10px; }
"""


def balloons(spec):
    return "".join(f'<span class="b" style="left:{x}px;top:{y}px;width:{w}px;height:{w*1.18:.0f}px;background-color:{c};transform:rotate({r}deg)"></span>' for x, y, w, c, r in spec)


def confetti(n, w, h, colors, seed=1):
    import random
    rnd = random.Random(seed)
    return '<div class="conf">' + "".join(
        f'<i style="left:{rnd.randint(0, w)}px;top:{rnd.randint(0, h)}px;background:{rnd.choice(colors)};transform:rotate({rnd.randint(0, 180)}deg)"></i>' for _ in range(n)) + "</div>"


def page(w, h, body, extra_css=""):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Diver Lauro</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Kaushan+Script&family=Plus+Jakarta+Sans:wght@500;700;800&display=block" rel="stylesheet">
<style>:root{{--w:{w}px;--h:{h}px}}{BASE_CSS}{extra_css}</style></head><body>{body}</body></html>"""


FOOT = f'<div class="foot"><span>{icon("pin", 34)} Alhaurín de la Torre</span><span>·</span><span>{icon("chat", 34)} {PHONE}</span></div>'
FOOT_LIGHT = FOOT.replace('class="foot"', 'class="foot" style="color:#fff"')
LOGO = "../../img/logo.png"
LOGO_Y = "../../img/logo-yellow.png"
LOGO_W = "../../img/logo-white.png"

DESIGNS = {}

# ----------------------------- POSTS 1080x1350 -----------------------------
W, H = 1080, 1350
DESIGNS["posts/post-1-volvemos"] = (W, H, page(W, H, f"""
{confetti(26, W, H, ['#0D305D', '#F25C54', '#2B7BE4', '#fff'], 3)}
{balloons([(650, 70, 200, '#F25C54', -6), (830, 30, 170, '#fff', 5), (760, 250, 180, '#0D305D', 3), (910, 230, 130, '#2B7BE4', -4)])}
<img class="logo" src="{LOGO}" style="position:absolute;left:80px;top:90px;width:470px">
<div style="position:absolute;left:80px;top:600px;right:80px">
  <h1 style="font-size:140px">¡Volvemos<br>a <span class="script" style="color:#F25C54">Instagram</span>!</h1>
  <p style="font-size:44px;font-weight:700;margin:40px 0 0;max-width:820px;line-height:1.25">Salón de celebraciones en Alhaurín de la Torre. Síguenos para ver <b>fechas libres</b>, ideas y novedades 🎈</p>
</div>
{FOOT}"""))

DESIGNS["posts/post-2-dia-noche"] = (W, H, page(W, H, f"""
<div style="position:absolute;inset:0 0 50% 0;background:linear-gradient(180deg,#FFF3B8,#EBD450)"></div>
<div style="position:absolute;inset:50% 0 0 0;background:radial-gradient(600px 400px at 80% 20%,rgba(122,60,255,.55),transparent 60%),linear-gradient(180deg,#0B1640,#050B1E)"></div>
<div style="position:absolute;right:-60px;top:-60px;width:380px;height:380px;border-radius:50%;background:radial-gradient(circle at 40% 40%,#fff,#FFF0A8 40%,#F5D23A 75%);box-shadow:0 0 120px 30px rgba(255,255,255,.55)"></div>
{balloons([(820, 400, 100, '#F25C54', -6), (930, 430, 84, '#2B7BE4', 5)])}
<div style="position:absolute;left:80px;top:150px"><p style="font-size:38px;font-weight:800;margin:0;letter-spacing:.14em">☀️ DE DÍA</p><h1 style="font-size:150px;margin-top:20px">Celebra<br><span class="script" style="color:#F25C54">de día</span></h1></div>
{confetti(18, W, 675, ['#EBD450', '#FF4FD8', '#fff'], 7).replace('class="conf"', 'class="conf" style="position:absolute;left:0;top:675px;width:100%;height:675px"')}
<div style="position:absolute;right:120px;top:740px;width:170px;height:170px;border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.95),transparent 30%),repeating-linear-gradient(0deg,transparent 0 15px,rgba(0,0,0,.28) 15px 17px),repeating-linear-gradient(90deg,#E6E8F4 0 15px,#8F96B8 15px 17px,#C9CDE2 17px 32px,#6C7398 32px 34px);box-shadow:0 0 90px rgba(255,255,255,.4)"></div>
<div style="position:absolute;left:80px;top:760px;color:#F7F1DD"><p style="font-size:38px;font-weight:800;margin:0;letter-spacing:.14em;color:#EBD450">🌙 DE NOCHE</p><h1 style="font-size:150px;margin-top:20px">Brinda<br><span class="script" style="color:#FF4FD8">de noche</span></h1></div>
<img src="{LOGO_Y}" style="position:absolute;right:70px;bottom:70px;width:300px">"""))

events = [("Cumpleaños", "#F25C54"), ("Comuniones", "#2B7BE4"), ("Bautizos", "#16B39A"), ("Bodas", "#9B5DE5"),
          ("Despedidas", "#FF4FD8"), ("Aniversarios", "#E0B526"), ("Comidas de empresa", "#2B7BE4"), ("Cenas de Navidad", "#F25C54"),
          ("Peñas y eventos", "#16B39A"), ("Fiestas infantiles", "#E0B526")]
pills = "".join(f'<span class="pill" style="background:{c};color:#fff;margin:0 14px 18px 0">{t}</span>' for t, c in events)
DESIGNS["posts/post-3-que-celebramos"] = (W, H, page(W, H, f"""
<div style="position:absolute;inset:0;background:radial-gradient(700px 500px at 100% 0%,rgba(122,60,255,.4),transparent 60%),#0D305D"></div>
{confetti(20, W, H, ['#EBD450', '#F25C54', '#fff'], 11)}
<div style="position:absolute;left:80px;top:110px;right:80px;color:#fff">
  <p style="font-size:36px;font-weight:800;letter-spacing:.14em;color:#EBD450;margin:0">UN SALÓN, MIL CELEBRACIONES</p>
  <h1 style="font-size:132px;margin:26px 0 60px">¿Qué <span class="script" style="color:#EBD450">celebras</span>?</h1>
  <div>{pills}</div>
</div>
<img src="{LOGO_Y}" style="position:absolute;left:80px;bottom:150px;width:330px">
{FOOT_LIGHT}"""))

items = ["Parque de bolas y tobogán", "Futbolín y pimpón", "Rincón infantil", "Sonido y TV", "Office con frigorífico y microondas", "Mesas y sillas", "Aire acondicionado"]
lis = "".join(f'<li style="display:flex;align-items:center;gap:26px;margin-bottom:20px"><span style="display:grid;place-items:center;width:56px;height:56px;border-radius:50%;background:#0D305D;flex-shrink:0">{icon("check", 38, "#EBD450", 3)}</span>{t}</li>' for t in items)
DESIGNS["posts/post-4-incluye"] = (W, H, page(W, H, f"""
{balloons([(880, 40, 130, '#F25C54', 6), (960, 150, 90, '#2B7BE4', -4)])}
<div style="position:absolute;left:80px;top:110px;right:80px">
  <p style="font-size:36px;font-weight:800;letter-spacing:.14em;color:#F25C54;margin:0">EL LOCAL</p>
  <h1 style="font-size:112px;margin:22px 0 54px">Todo lo que<br>necesitas,<br><span class="script" style="color:#F25C54">ya está</span></h1>
  <ul style="list-style:none;padding:0;margin:0;font-size:40px;font-weight:800">{lis}</ul>
</div>
{FOOT}"""))

DESIGNS["posts/post-5-fechas"] = (W, H, page(W, H, f"""
<div style="position:absolute;inset:0;background:#F25C54"></div>
{confetti(24, W, H, ['#EBD450', '#0D305D', '#fff'], 5)}
<div style="position:absolute;left:50%;top:150px;width:480px;margin-left:-240px;background:#fff;border-radius:48px;box-shadow:0 40px 80px -30px rgba(0,0,0,.4);overflow:hidden;transform:rotate(-4deg)">
  <div style="background:#0D305D;color:#EBD450;text-align:center;font-weight:800;font-size:44px;padding:28px">FECHAS LIBRES</div>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;padding:34px">{"".join(f'<span style="aspect-ratio:1;border-radius:16px;display:grid;place-items:center;font-weight:800;font-size:30px;background:{"#EBD450" if i in (3, 8, 12, 17, 19) else "#F3F4F8"};color:#0D305D">{i}</span>' for i in range(1, 21))}</div>
</div>
<div style="position:absolute;left:80px;right:80px;top:770px;text-align:center;color:#fff">
  <h1 style="font-size:124px">¿Buscas <span class="script" style="color:#EBD450">fecha</span>?</h1>
  <p style="font-size:44px;font-weight:700;margin:30px 0 0;line-height:1.3">Escríbenos y te decimos qué días<br>quedan libres, de día o de noche</p>
</div>
<div style="position:absolute;left:0;right:0;bottom:70px;text-align:center"><span class="pill" style="background:#0D305D;color:#EBD450;font-size:42px;padding:24px 46px">WhatsApp {PHONE}</span></div>"""))

stars = "".join(icon("star", 120, "#EBD450", 0).replace('fill="none"', 'fill="#EBD450"') for _ in range(4)) + \
    '<span style="position:relative;display:inline-block;width:120px;height:120px">' + icon("star", 120, "#EBD450", 0).replace('fill="none"', 'fill="rgba(235,212,80,.3)"') + \
    '<span style="position:absolute;inset:0;width:50%;overflow:hidden">' + icon("star", 120, "#EBD450", 0).replace('fill="none"', 'fill="#EBD450"') + '</span></span>'
DESIGNS["posts/post-6-opiniones"] = (W, H, page(W, H, f"""
<div style="position:absolute;inset:0;background:radial-gradient(700px 500px at 0% 100%,rgba(255,79,216,.35),transparent 60%),#0D305D"></div>
{confetti(18, W, H, ['#EBD450', '#fff', '#FF4FD8'], 9)}
<div style="position:absolute;left:0;right:0;top:170px;text-align:center;color:#fff">
  <p style="font-size:36px;font-weight:800;letter-spacing:.14em;color:#EBD450;margin:0">OPINIONES EN GOOGLE</p>
  <div style="font-family:'Bricolage Grotesque';font-weight:800;font-size:330px;line-height:1;margin-top:30px;letter-spacing:-.05em">4,5</div>
  <div style="display:flex;justify-content:center;gap:10px;margin-top:10px">{stars}</div>
  <p style="font-size:50px;font-weight:800;margin:60px 0 0">Más de 175 reseñas</p>
  <h1 style="font-size:120px;margin-top:40px" class="script">¡Gracias!</h1>
</div>
<img src="{LOGO_Y}" style="position:absolute;left:50%;margin-left:-170px;bottom:150px;width:340px">
{FOOT_LIGHT}"""))

DESIGNS["posts/post-7-parque-bolas"] = (W, H, page(W, H, f"""
{confetti(16, W, H, ['#0D305D', '#F25C54', '#2B7BE4', '#fff'], 4)}
<div style="position:absolute;left:70px;right:70px;top:90px;height:760px;border-radius:48px;overflow:hidden;border:14px solid #fff;box-shadow:0 40px 80px -30px rgba(13,48,93,.5);transform:rotate(-2deg)">
  <img src="../../img/fotos/parque-bolas.webp" style="width:100%;height:100%;object-fit:cover">
</div>
<span class="pill" style="position:absolute;left:110px;top:60px;background:#0D305D;color:#EBD450;transform:rotate(-4deg)">La estrella para los peques</span>
<div style="position:absolute;left:80px;right:80px;top:910px">
  <h1 style="font-size:112px">Parque de bolas<br><span class="script" style="color:#F25C54">y tobogán</span> 🎈</h1>
</div>
{FOOT}"""))

# --------------------------- HISTORIAS 1080x1920 ---------------------------
W, H = 1080, 1920
DESIGNS["historias/historia-1-reservas"] = (W, H, page(W, H, f"""
{confetti(30, W, H, ['#0D305D', '#F25C54', '#2B7BE4', '#fff'], 21)}
{balloons([(90, 220, 200, '#F25C54', -6), (760, 160, 230, '#0D305D', 5), (560, 330, 150, '#fff', 3)])}
<img class="logo" src="{LOGO}" style="position:absolute;left:50%;margin-left:-280px;top:720px;width:560px">
<div style="position:absolute;left:80px;right:80px;top:920px;text-align:center">
  <h1 style="font-size:130px">¿Celebras<br><span class="script" style="color:#F25C54">algo</span>?</h1>
  <p style="font-size:48px;font-weight:700;margin:40px 0 0;line-height:1.3">Reserva tu fecha<br>por WhatsApp</p>
  <div style="margin-top:50px"><span class="pill" style="background:#0D305D;color:#EBD450;font-size:56px;padding:30px 56px">{PHONE}</span></div>
  <p style="font-size:38px;font-weight:800;margin:110px 0 0;opacity:.7">👇 Pon aquí el sticker de enlace</p>
</div>"""))

DESIGNS["historias/historia-2-dia-noche"] = (W, H, page(W, H, f"""
<div style="position:absolute;inset:0 0 50% 0;background:linear-gradient(180deg,#FFF3B8,#EBD450)"></div>
<div style="position:absolute;inset:50% 0 0 0;background:radial-gradient(700px 500px at 80% 20%,rgba(122,60,255,.55),transparent 60%),linear-gradient(180deg,#0B1640,#050B1E)"></div>
<div style="position:absolute;right:-80px;top:-80px;width:460px;height:460px;border-radius:50%;background:radial-gradient(circle at 40% 40%,#fff,#FFF0A8 40%,#F5D23A 75%);box-shadow:0 0 140px 40px rgba(255,255,255,.55)"></div>
{balloons([(800, 560, 120, '#F25C54', -6), (930, 610, 96, '#2B7BE4', 5)])}
<img src="{LOGO}" style="position:absolute;left:80px;top:140px;width:380px">
<div style="position:absolute;left:80px;top:420px"><p style="font-size:42px;font-weight:800;margin:0;letter-spacing:.14em">☀️ DE DÍA</p><h1 style="font-size:160px;margin-top:24px">Celebra<br><span class="script" style="color:#F25C54">de día</span></h1></div>
{confetti(22, W, 960, ['#EBD450', '#FF4FD8', '#fff'], 13).replace('class="conf"', 'class="conf" style="position:absolute;left:0;top:960px;width:100%;height:960px"')}
<div style="position:absolute;left:80px;top:1140px;color:#F7F1DD"><p style="font-size:42px;font-weight:800;margin:0;letter-spacing:.14em;color:#EBD450">🌙 DE NOCHE</p><h1 style="font-size:160px;margin-top:24px">Brinda<br><span class="script" style="color:#FF4FD8">de noche</span></h1>
<p style="font-size:44px;font-weight:700;margin:50px 0 0">Cumpleaños, comuniones, bodas,<br>despedidas y empresas</p></div>"""))

DESIGNS["historias/historia-3-web"] = (W, H, page(W, H, f"""
<div style="position:absolute;inset:0;background:radial-gradient(800px 600px at 100% 0%,rgba(122,60,255,.45),transparent 60%),#0D305D"></div>
{confetti(26, W, H, ['#EBD450', '#F25C54', '#fff', '#FF4FD8'], 17)}
<div style="position:absolute;left:80px;right:80px;top:260px;text-align:center;color:#fff">
  <p style="font-size:40px;font-weight:800;letter-spacing:.14em;color:#EBD450;margin:0">¡NOVEDAD!</p>
  <h1 style="font-size:150px;margin-top:30px">Estrenamos<br><span class="script" style="color:#EBD450">web</span></h1>
  <p style="font-size:46px;font-weight:700;margin:50px 0 0;line-height:1.35">Mira todo lo que puedes celebrar<br>y consulta tu fecha en un minuto</p>
</div>
<div style="position:absolute;left:50%;top:1020px;margin-left:-300px;width:600px;height:420px;border-radius:40px;background:#EBD450;box-shadow:0 40px 80px -30px rgba(0,0,0,.6);display:grid;place-items:center;transform:rotate(-3deg)">
  <img src="{LOGO}" style="width:440px">
</div>
<div style="position:absolute;left:0;right:0;top:1560px;text-align:center"><span class="pill" style="background:#EBD450;color:#0D305D;font-size:50px;padding:28px 52px">{WEB}</span>
<p style="font-size:36px;font-weight:800;margin:60px 0 0;color:#fff;opacity:.7">👆 Pon aquí el sticker de enlace</p></div>"""))

# ----------------------- DESTACADOS (portadas) 1080x1920 -----------------------
HL = [("cumples", "cake", "#EBD450", "#0D305D"), ("comuniones", "heart", "#EBD450", "#0D305D"), ("noche", "moon", "#0D305D", "#EBD450"),
      ("el-local", "home", "#EBD450", "#0D305D"), ("reservas", "calendar", "#EBD450", "#0D305D"), ("opiniones", "star", "#0D305D", "#EBD450")]
for name, ic, bg, fg in HL:
    DESIGNS[f"destacados/destacado-{name}"] = (W, H, page(W, H, f"""
<div style="position:absolute;inset:0;background:{bg}"></div>
<div style="position:absolute;left:50%;top:50%;width:620px;height:620px;margin:-310px 0 0 -310px;border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.22),transparent 60%)">{icon(ic, 330, fg, 1.7)}</div>"""))

# ----------------------------- PERFIL 1080x1080 -----------------------------
W, H = 1080, 1080
DESIGNS["perfil/perfil-amarillo"] = (W, H, page(W, H, f"""
{confetti(14, W, 220, ['#0D305D', '#F25C54', '#2B7BE4', '#fff'], 2)}
{confetti(14, W, 220, ['#0D305D', '#F25C54', '#2B7BE4', '#fff'], 6).replace('class="conf"', 'class="conf" style="position:absolute;left:0;top:860px;width:100%;height:220px"')}
<img src="{LOGO}" style="position:absolute;left:50%;top:50%;width:880px;transform:translate(-50%,-58%)">
<p style="position:absolute;left:0;right:0;top:640px;text-align:center;margin:0;font-weight:800;font-size:58px;letter-spacing:.06em">SALÓN DE CELEBRACIONES</p>"""))
DESIGNS["perfil/perfil-azul"] = (W, H, page(W, H, f"""
<div style="position:absolute;inset:0;background:#0D305D"></div>
{confetti(14, W, 220, ['#EBD450', '#F25C54', '#fff'], 2)}
{confetti(14, W, 220, ['#EBD450', '#F25C54', '#fff'], 6).replace('class="conf"', 'class="conf" style="position:absolute;left:0;top:860px;width:100%;height:220px"')}
<img src="{LOGO_Y}" style="position:absolute;left:50%;top:50%;width:880px;transform:translate(-50%,-58%)">
<p style="position:absolute;left:0;right:0;top:640px;text-align:center;margin:0;font-weight:800;font-size:58px;letter-spacing:.06em;color:#fff">SALÓN DE CELEBRACIONES</p>"""))

# --------------------- PORTADAS (Facebook y Google) ---------------------
# Facebook: 1640x856. Lo importante va en el centro (en móvil recorta los lados y en PC arriba/abajo).
W, H = 1640, 856
DESIGNS["portadas/portada-facebook"] = (W, H, page(W, H, f"""
<div style="position:absolute;inset:0 50% 0 0;background:linear-gradient(180deg,#FFF3B8,#EBD450)"></div>
<div style="position:absolute;inset:0 0 0 50%;background:radial-gradient(600px 400px at 70% 20%,rgba(122,60,255,.55),transparent 60%),linear-gradient(180deg,#0B1640,#050B1E)"></div>
{confetti(30, W, H, ['#0D305D', '#F25C54', '#2B7BE4', '#fff', '#FF4FD8'], 31)}
{balloons([(250, 150, 150, '#F25C54', -6), (380, 110, 120, '#fff', 5), (330, 330, 130, '#0D305D', 3)])}
<div style="position:absolute;right:250px;top:120px;width:170px;height:170px;border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.95),transparent 30%),repeating-linear-gradient(0deg,transparent 0 15px,rgba(0,0,0,.28) 15px 17px),repeating-linear-gradient(90deg,#E6E8F4 0 15px,#8F96B8 15px 17px,#C9CDE2 17px 32px,#6C7398 32px 34px);box-shadow:0 0 90px rgba(255,255,255,.4)"></div>
<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:760px;padding:56px 60px;border-radius:48px;background:#fff;box-shadow:0 40px 80px -30px rgba(0,0,0,.45);text-align:center">
  <img src="{LOGO}" style="width:520px">
  <p style="margin:18px 0 0;font-weight:800;font-size:40px;letter-spacing:.04em">SALÓN DE CELEBRACIONES</p>
  <p style="margin:10px 0 0;font-weight:700;font-size:30px;color:#4C5F80">Alhaurín de la Torre · De día y de noche</p>
  <p style="margin:26px 0 0"><span class="pill" style="background:#0D305D;color:#EBD450;font-size:32px;padding:16px 34px">{WEB} · {PHONE}</span></p>
</div>"""))

# Google (ficha de empresa): 1080x608 (16:9)
W, H = 1080, 608
DESIGNS["portadas/portada-google"] = (W, H, page(W, H, f"""
{confetti(14, 360, H, ['#0D305D', '#F25C54', '#2B7BE4', '#fff'], 41).replace('class="conf"', 'class="conf" style="position:absolute;left:720px;top:0;width:360px;height:608px"')}
{balloons([(820, 40, 140, '#F25C54', -6), (940, 110, 100, '#2B7BE4', 5), (860, 230, 110, '#fff', 3)])}
<img src="{LOGO}" style="position:absolute;left:70px;top:80px;width:520px">
<div style="position:absolute;left:70px;top:240px;width:700px">
  <h1 style="font-size:64px">Salón de celebraciones<br>en Alhaurín de la Torre</h1>
  <p style="font-size:30px;font-weight:700;margin:22px 0 0">Cumpleaños · Comuniones · Bodas · Despedidas · Empresas</p>
  <p style="margin:26px 0 0"><span class="pill" style="background:#0D305D;color:#EBD450;font-size:28px;padding:14px 30px">☀️ De día y 🌙 de noche · {WEB}</span></p>
</div>"""))


def find_chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists() or shutil.which(c):
            return c
    raise SystemExit("No encuentro Chrome/Edge para exportar las imágenes.")


def main():
    chrome = find_chrome()
    profile = OUT / ".chrome-perfil-temporal"
    for key, (w, h, html) in DESIGNS.items():
        tpl = TPL / f"{key.replace('/', '__')}.html"
        tpl.parent.mkdir(parents=True, exist_ok=True)
        tpl.write_text(html, encoding="utf-8")
        png = OUT / f"{key}.png"
        png.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        f"--user-data-dir={profile}", "--virtual-time-budget=20000", f"--window-size={w},{h}",
                        f"--screenshot={png}", tpl.resolve().as_uri()], check=False, capture_output=True, timeout=120)
        print(("OK  " if png.exists() else "ERR ") + str(png.relative_to(ROOT)))
    shutil.rmtree(profile, ignore_errors=True)

    # miniaturas para la web (móvil de la sección "Síguenos")
    try:
        from PIL import Image
        web = ROOT / "img/redes"
        web.mkdir(parents=True, exist_ok=True)
        for i, key in enumerate(["post-1-volvemos", "post-2-dia-noche", "post-3-que-celebramos", "post-4-incluye", "post-5-fechas", "post-6-opiniones"], 1):
            im = Image.open(OUT / f"posts/{key}.png").convert("RGB")
            im.thumbnail((270, 338))
            im.save(web / f"post-{i}-sm.webp", "WEBP", quality=80)
        im = Image.open(OUT / "perfil/perfil-amarillo.png").convert("RGB")
        im.thumbnail((96, 96))
        im.save(web / "perfil-sm.webp", "WEBP", quality=85)
        print("OK  img/redes/ (miniaturas para la web)")
    except ImportError:
        print("Pillow no instalado: no se generan las miniaturas de la web")


if __name__ == "__main__":
    main()
