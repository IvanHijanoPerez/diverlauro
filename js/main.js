/* Diver Lauro · interacciones */
(() => {
  const WHATSAPP = "34647913022";
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  /* ---------- Año del footer ---------- */
  const year = $("#year");
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- Cabecera al hacer scroll + botón WhatsApp ---------- */
  const header = $(".site-header");
  const waFloat = $(".wa-float");
  const onScroll = () => {
    const y = window.scrollY;
    header.classList.toggle("scrolled", y > 40);
    waFloat.classList.toggle("show", y > window.innerHeight * 0.6);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- Menú móvil ---------- */
  const toggle = $(".menu-toggle");
  const setMenu = (open) => {
    document.body.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  };
  toggle.addEventListener("click", () => setMenu(!document.body.classList.contains("menu-open")));
  $$("#nav a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  document.addEventListener("keydown", (e) => e.key === "Escape" && setMenu(false));

  /* ---------- Enlace activo en la navegación ---------- */
  const navLinks = $$('.nav a[href^="#"]');
  const sections = navLinks.map((a) => $(a.getAttribute("href"))).filter(Boolean);
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        navLinks.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id));
      }
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  sections.forEach((s) => spy.observe(s));

  /* ---------- Aparición al hacer scroll ---------- */
  const reveals = $$(".reveal");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("is-visible"));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    reveals.forEach((el) => io.observe(el));
  }

  /* ---------- Contadores ---------- */
  $$("[data-count]").forEach((el) => {
    const target = parseFloat(el.dataset.count);
    const dec = parseInt(el.dataset.decimals || "0", 10);
    const fmt = (n) => n.toFixed(dec).replace(".", ",");
    if (reduceMotion) { el.textContent = fmt(target); return; }
    el.textContent = fmt(0);
    const start = performance.now() + 500, dur = 1600;
    const tick = (t) => {
      const p = Math.min(Math.max((t - start) / dur, 0), 1);
      el.textContent = fmt(target * (1 - Math.pow(1 - p, 4)));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });

  /* ---------- Inclinación 3D de tarjetas ---------- */
  if (!reduceMotion && window.matchMedia("(hover: hover)").matches) {
    $$(".tilt").forEach((card) => {
      card.addEventListener("pointermove", (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(800px) rotateX(${(-y * 8).toFixed(2)}deg) rotateY(${(x * 10).toFixed(2)}deg) translateY(-6px)`;
      });
      card.addEventListener("pointerleave", () => { card.style.transform = ""; });
    });
  }

  /* ---------- Formulario → WhatsApp ---------- */
  const form = $("#reserve-form");
  if (form) {
    const dateInput = $("#f-date");
    dateInput.min = new Date().toISOString().slice(0, 10);
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = $("#f-name");
      if (!name.value.trim()) {
        name.classList.remove("invalid"); void name.offsetWidth; name.classList.add("invalid");
        name.focus();
        return;
      }
      name.classList.remove("invalid");
      const d = Object.fromEntries(new FormData(form));
      let fecha = "";
      if (d.fecha) {
        fecha = new Date(d.fecha + "T12:00:00").toLocaleDateString("es-ES", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
      }
      const lines = [
        `¡Hola! Soy ${d.nombre.trim()} y me gustaría información para celebrar en Diver Lauro.`,
        `• Celebración: ${d.tipo}`,
        fecha && `• Fecha: ${fecha}`,
        d.ninos && `• Niños: ${d.ninos}`,
        d.adultos && `• Adultos: ${d.adultos}`,
        d.mensaje && d.mensaje.trim() && `• Comentarios: ${d.mensaje.trim()}`,
      ].filter(Boolean);
      window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(lines.join("\n"))}`, "_blank", "noopener");
    });
  }

  /* ---------- Parque de bolas interactivo (hero) ---------- */
  const canvas = $(".ballpit");
  if (!canvas) return;
  const hero = canvas.parentElement;
  const ctx = canvas.getContext("2d");
  const COLORS = ["#FFC93C", "#FF6B5E", "#22CFA0", "#2F6BFF", "#FF5FA2", "#FFFFFF"];
  const G = 0.38, BOUNCE = 0.42, FRICTION = 0.995;
  let W = 0, H = 0, DPR = 1, balls = [], running = false, visible = true;
  const pointer = { x: -999, y: -999, vx: 0, vy: 0, active: false };

  const rand = (a, b) => a + Math.random() * (b - a);
  const makeBall = (x, y) => {
    const small = W < 640;
    const r = small ? rand(13, 24) : rand(18, 36);
    return { x: x ?? rand(r, W - r), y: y ?? rand(-H * 1.2, -r), vx: rand(-1.5, 1.5), vy: rand(0, 2), r, c: COLORS[(Math.random() * COLORS.length) | 0] };
  };

  const resize = () => {
    const rect = hero.getBoundingClientRect();
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = rect.width; H = rect.height;
    canvas.width = W * DPR; canvas.height = H * DPR;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    const target = Math.round(Math.min(90, Math.max(28, W / 22)));
    while (balls.length < target) balls.push(makeBall());
    if (balls.length > target + 30) balls.length = target + 30;
    balls.forEach((b) => { b.x = Math.min(Math.max(b.x, b.r), W - b.r); });
  };

  const step = () => {
    const n = balls.length;
    for (let i = 0; i < n; i++) {
      const b = balls[i];
      b.vy += G; b.vx *= FRICTION; b.vy *= FRICTION;
      // empuje del puntero
      if (pointer.active) {
        const dx = b.x - pointer.x, dy = b.y - pointer.y;
        const dist = Math.hypot(dx, dy), reach = b.r + 60;
        if (dist < reach && dist > 0.01) {
          const f = (1 - dist / reach) * 2.2;
          b.vx += (dx / dist) * f + pointer.vx * 0.08;
          b.vy += (dy / dist) * f + pointer.vy * 0.08;
        }
      }
      b.x += b.vx; b.y += b.vy;
      if (b.y > H - b.r) { b.y = H - b.r; b.vy *= -BOUNCE; b.vx *= 0.96; if (Math.abs(b.vy) < 0.6) b.vy = 0; }
      if (b.x < b.r) { b.x = b.r; b.vx = Math.abs(b.vx) * BOUNCE; }
      if (b.x > W - b.r) { b.x = W - b.r; b.vx = -Math.abs(b.vx) * BOUNCE; }
    }
    // colisiones entre bolas (2 pasadas para estabilidad)
    for (let k = 0; k < 2; k++) {
      for (let i = 0; i < n; i++) {
        const a = balls[i];
        for (let j = i + 1; j < n; j++) {
          const b = balls[j];
          const dx = b.x - a.x, dy = b.y - a.y, min = a.r + b.r;
          const d2 = dx * dx + dy * dy;
          if (d2 >= min * min || d2 === 0) continue;
          const d = Math.sqrt(d2), nx = dx / d, ny = dy / d, overlap = (min - d) / 2;
          a.x -= nx * overlap; a.y -= ny * overlap;
          b.x += nx * overlap; b.y += ny * overlap;
          const rel = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny;
          if (rel < 0) {
            const imp = -(1 + BOUNCE) * rel / 2;
            a.vx -= imp * nx; a.vy -= imp * ny;
            b.vx += imp * nx; b.vy += imp * ny;
          }
        }
      }
    }
    pointer.vx *= 0.8; pointer.vy *= 0.8;
  };

  const draw = () => {
    ctx.clearRect(0, 0, W, H);
    for (const b of balls) {
      if (b.y < -b.r) continue;
      const g = ctx.createRadialGradient(b.x - b.r * 0.35, b.y - b.r * 0.4, b.r * 0.1, b.x, b.y, b.r);
      g.addColorStop(0, "rgba(255,255,255,.75)");
      g.addColorStop(0.28, b.c);
      g.addColorStop(1, shade(b.c));
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
      ctx.fillStyle = g;
      ctx.fill();
    }
  };

  const shadeCache = {};
  function shade(hex) {
    if (shadeCache[hex]) return shadeCache[hex];
    const n = parseInt(hex.slice(1), 16);
    const f = 0.68;
    const r = ((n >> 16) & 255) * f, g = ((n >> 8) & 255) * f, b = (n & 255) * f;
    return (shadeCache[hex] = `rgb(${r | 0},${g | 0},${b | 0})`);
  }

  const loop = () => {
    if (!running) return;
    step(); draw();
    requestAnimationFrame(loop);
  };
  const start = () => { if (!running && visible && !document.hidden) { running = true; requestAnimationFrame(loop); } };
  const stop = () => { running = false; };

  resize();
  if (reduceMotion) {
    // sin animación: colocamos las bolas ya apiladas y dibujamos una vez
    balls.forEach((b) => { b.y = H - b.r - Math.random() * 60; });
    for (let i = 0; i < 400; i++) step();
    draw();
  } else {
    start();
  }

  let rT;
  window.addEventListener("resize", () => { clearTimeout(rT); rT = setTimeout(() => { resize(); if (reduceMotion) draw(); }, 120); });
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; visible && !reduceMotion ? start() : stop(); }).observe(hero);
  document.addEventListener("visibilitychange", () => (document.hidden ? stop() : !reduceMotion && start()));

  if (!reduceMotion) {
    const toLocal = (e) => { const r = canvas.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; };
    hero.addEventListener("pointermove", (e) => {
      const p = toLocal(e);
      if (pointer.active) { pointer.vx = p.x - pointer.x; pointer.vy = p.y - pointer.y; }
      pointer.x = p.x; pointer.y = p.y; pointer.active = true;
    });
    hero.addEventListener("pointerleave", () => { pointer.active = false; });
    hero.addEventListener("pointerdown", (e) => {
      if (e.target.closest("a, button")) return;
      const p = toLocal(e);
      // ¡lanza una bola nueva!
      const b = makeBall(p.x, p.y);
      b.vy = rand(-10, -6); b.vx = rand(-4, 4);
      balls.push(b);
      if (balls.length > 160) balls.shift();
      const hint = $(".hero-hint"); if (hint) hint.style.opacity = "0";
    });
  }
})();
