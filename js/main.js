/* Diver Lauro · interacciones */

(() => {
  const WHATSAPP = "34647913022";
  const root = document.documentElement;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  const year = $("#year");
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- Modo día / noche ---------- */
  const themeMeta = $('meta[name="theme-color"]');
  const modeBtn = $("[data-mode-toggle]");
  const applyMode = (mode, save = true) => {
    root.dataset.mode = mode;
    if (save) { try { localStorage.setItem("dl-mode", mode); } catch (e) {} }
    themeMeta && themeMeta.setAttribute("content", mode === "night" ? "#070F26" : "#EBD450");
    modeBtn && modeBtn.setAttribute("aria-label", mode === "night" ? "Cambiar a modo día" : "Cambiar a modo noche");
    $$("[data-set-mode]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.setMode === mode)));
    window.dispatchEvent(new CustomEvent("dl:mode", { detail: mode }));
  };
  applyMode(root.dataset.mode || "day", false);
  modeBtn && modeBtn.addEventListener("click", () => applyMode(root.dataset.mode === "night" ? "day" : "night"));
  $$("[data-set-mode]").forEach((b) => b.addEventListener("click", () => {
    applyMode(b.dataset.setMode);
    if (b.closest(".dn-card")) document.querySelector(".hero").scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
  }));

  /* ---------- Globos del hero (CSS, se explotan al tocarlos) ---------- */
  const hero = $(".hero");
  const fx = $(".hero-fx");
  if (hero && fx) {
    // pausa las animaciones cuando el hero no se ve (ahorra batería)
    new IntersectionObserver(([en]) => hero.classList.toggle("fx-paused", !en.isIntersecting)).observe(hero);
    const hint = $(".hero-hint");
    $$(".balloon", fx).forEach((b) => {
      b.addEventListener("pointerdown", () => {
        if (b.classList.contains("pop")) return;
        if (hint) hint.style.opacity = "0";
        const color = getComputedStyle(b.firstElementChild).backgroundColor;
        b.classList.add("pop");
        if (!reduceMotion) {
          const r = b.getBoundingClientRect(), f = fx.getBoundingClientRect();
          for (let i = 0; i < 12; i++) {
            const piece = document.createElement("i");
            const a = (i / 12) * Math.PI * 2, d = 50 + Math.random() * 70;
            piece.className = "burst";
            piece.style.cssText = `left:${r.left - f.left + r.width / 2}px;top:${r.top - f.top + r.height / 2}px;background:${i % 3 ? color : "var(--yellow)"};--tx:${Math.cos(a) * d}px;--ty:${Math.sin(a) * d + 30}px;--r:${Math.random() * 540}deg`;
            fx.appendChild(piece);
            piece.addEventListener("animationend", () => piece.remove());
          }
        }
        setTimeout(() => {
          b.classList.remove("pop");
          b.style.setProperty("--delay", "0s");
          b.style.animation = "none"; void b.offsetWidth; b.style.animation = "";
        }, 2200);
      });
    });
  }

  /* ---------- Cabecera + botón WhatsApp ---------- */
  const header = $(".site-header");
  const waFloat = $(".wa-float");
  const onScroll = () => {
    const y = window.scrollY;
    header.classList.toggle("scrolled", y > 30);
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

  /* ---------- Enlace activo ---------- */
  const navLinks = $$('.nav a[href^="#"]');  // solo en la portada
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) navLinks.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id));
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  navLinks.map((a) => $(a.getAttribute("href"))).filter(Boolean).forEach((s) => spy.observe(s));

  /* ---------- Aparición al hacer scroll ---------- */
  const reveals = $$(".reveal");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("is-visible"));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    reveals.forEach((el) => io.observe(el));
  }

  /* ---------- Contadores ---------- */
  const counterIO = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      counterIO.unobserve(en.target);
      const el = en.target, target = parseFloat(el.dataset.count), dec = parseInt(el.dataset.decimals || "0", 10);
      const fmt = (n) => n.toFixed(dec).replace(".", ",");
      if (reduceMotion) { el.textContent = fmt(target); return; }
      const start = performance.now() + 300, dur = 1500;
      const tick = (t) => {
        const p = Math.min(Math.max((t - start) / dur, 0), 1);
        // se lee en cada fotograma: las reseñas de Google pueden actualizar la cifra mientras se anima
        el.textContent = fmt(parseFloat(el.dataset.count) * (1 - Math.pow(1 - p, 4)));
        if (p < 1) requestAnimationFrame(tick);
      };
      el.textContent = fmt(0);
      requestAnimationFrame(tick);
    });
  });
  $$("[data-count]").forEach((el) => counterIO.observe(el));

  /* ---------- Inclinación 3D ---------- */
  if (!reduceMotion && window.matchMedia("(hover: hover)").matches) {
    $$(".tilt").forEach((card) => {
      const max = card.classList.contains("stage-frame") ? 6 : 8;
      card.addEventListener("pointermove", (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(900px) rotateX(${(-y * max).toFixed(2)}deg) rotateY(${(x * max * 1.2).toFixed(2)}deg) translateY(-4px)`;
        card.style.setProperty("--mx", `${((x + 0.5) * 100).toFixed(1)}%`);
        card.style.setProperty("--my", `${((y + 0.5) * 100).toFixed(1)}%`);
      });
      card.addEventListener("pointerleave", () => { card.style.transform = ""; });
    });
  }

  /* ---------- Reseñas de Google (vía /api/resenas, se actualizan solas) ---------- */
  const gBox = $("#google-reviews");
  if (gBox && "IntersectionObserver" in window) {
    const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
    const star = '<svg class="ic"><use href="#i-star"/></svg>';
    const render = (d) => {
      if (!d || d.error) return;
      if (typeof d.rating === "number") {
        $$('[data-g="rating"]').forEach((el) => { el.dataset.count = d.rating.toFixed(1); el.textContent = d.rating.toFixed(1).replace(".", ","); });
      }
      if (typeof d.total === "number") {
        $$('[data-g="total"]').forEach((el) => { el.dataset.count = String(d.total); el.textContent = String(d.total); });
      }
      const list = (d.reviews || []).slice(0, 6);
      if (!list.length) return;
      $(".g-reviews-list", gBox).innerHTML = list.map((r) => {
        const avatar = r.photo
          ? `<img class="rv-photo" src="${esc(r.photo)}" alt="" width="36" height="36" loading="lazy" referrerpolicy="no-referrer">`
          : `<span class="rv-avatar" aria-hidden="true">${esc((r.author || "?").charAt(0).toUpperCase())}</span>`;
        const name = r.authorUri ? `<a href="${esc(r.authorUri)}" target="_blank" rel="noopener nofollow">${esc(r.author)}</a>` : esc(r.author);
        return `<figure class="review-card g-card">
          <figcaption>${avatar}<span><strong>${name}</strong><small>${esc(r.when)}</small></span></figcaption>
          <span class="rating-stars" aria-label="${r.rating} de 5 estrellas">${star.repeat(Math.round(r.rating))}</span>
          <blockquote>${esc(r.text)}</blockquote>
        </figure>`;
      }).join("");
      if (d.mapsUri) $(".g-reviews-more", gBox).href = d.mapsUri;
      gBox.hidden = false;
    };
    const gIO = new IntersectionObserver(([en]) => {
      if (!en.isIntersecting) return;
      gIO.disconnect();
      fetch(gBox.dataset.src).then((r) => (r.ok ? r.json() : null)).then(render).catch(() => {});
    }, { rootMargin: "600px 0px" });
    gIO.observe($("#opiniones") || gBox);
  }

  /* ---------- Formulario → WhatsApp ---------- */
  const form = $("#reserve-form");
  if (form) {
    $("#f-date").min = new Date().toISOString().slice(0, 10);
    // el horario del formulario sigue al modo día/noche hasta que el usuario lo elija
    let horarioTocado = false;
    $$('input[name="horario"]', form).forEach((r) => r.addEventListener("change", () => { horarioTocado = true; }));
    const syncHorario = (mode) => {
      if (horarioTocado) return;
      const r = $(`input[name="horario"][value="${mode === "night" ? "De noche" : "De día"}"]`, form);
      if (r) r.checked = true;
    };
    syncHorario(root.dataset.mode);
    window.addEventListener("dl:mode", (e) => syncHorario(e.detail));

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
      const fecha = d.fecha ? new Date(d.fecha + "T12:00:00").toLocaleDateString("es-ES", { weekday: "long", day: "numeric", month: "long", year: "numeric" }) : "";
      const lines = [
        `¡Hola! Soy ${d.nombre.trim()} y me gustaría información para celebrar en Diver Lauro.`,
        `• Celebración: ${d.tipo}`,
        fecha && `• Fecha: ${fecha}`,
        d.horario && `• Horario: ${d.horario}`,
        d.adultos && `• Adultos: ${d.adultos}`,
        d.ninos && `• Niños: ${d.ninos}`,
        d.mensaje && d.mensaje.trim() && `• Comentarios: ${d.mensaje.trim()}`,
      ].filter(Boolean);
      window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(lines.join("\n"))}`, "_blank", "noopener");
    });
  }
})();
