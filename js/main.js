/* Diver Lauro · interacciones */

/* ===== Opiniones reales de Google =====
   Para mostrar reseñas, añádelas aquí copiándolas tal cual de Google:
   { autor: "Nombre", texto: "Texto de la reseña", estrellas: 5 }
   Si la lista está vacía, la web solo muestra la valoración media. */
const REVIEWS = [];

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
  const navLinks = $$('.nav a[href^="#"]');
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
        el.textContent = fmt(target * (1 - Math.pow(1 - p, 4)));
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

  /* ---------- Showcase de celebraciones ---------- */
  const tabs = $$('.showcase-tabs [role="tab"]');
  const stageImg = $(".stage-img");
  const stageCap = $(".stage-cap span");
  const panel = $("#p-show");
  let tabTimer, autoplay = true;
  const selectTab = (tab, focus = false) => {
    if (tab.getAttribute("aria-selected") === "true") return;
    tabs.forEach((t) => { t.setAttribute("aria-selected", String(t === tab)); t.tabIndex = t === tab ? 0 : -1; });
    panel.setAttribute("aria-labelledby", tab.id);
    if (focus) tab.focus();
    const src = `img/fotos/${tab.dataset.img}.webp`;
    const pre = new Image();
    pre.src = src;
    stageImg.classList.add("swap");
    const swap = () => {
      setTimeout(() => {
        stageImg.src = src;
        stageImg.alt = tab.dataset.cap;
        stageImg.width = +tab.dataset.w; stageImg.height = +tab.dataset.h;
        stageCap.textContent = tab.dataset.cap;
        requestAnimationFrame(() => stageImg.classList.remove("swap"));
      }, reduceMotion ? 0 : 280);
    };
    pre.decode ? pre.decode().then(swap, swap) : (pre.onload = swap);
  };
  tabs.forEach((t, i) => {
    t.tabIndex = i === 0 ? 0 : -1;
    t.addEventListener("click", () => { autoplay = false; selectTab(t); });
    t.addEventListener("keydown", (e) => {
      const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
      if (!d) return;
      e.preventDefault(); autoplay = false;
      selectTab(tabs[(i + d + tabs.length) % tabs.length], true);
    });
  });
  // rotación automática hasta que el usuario toque una pestaña
  if (!reduceMotion && tabs.length) {
    const showIO = new IntersectionObserver(([en]) => {
      clearInterval(tabTimer);
      if (en.isIntersecting && autoplay) {
        tabTimer = setInterval(() => {
          if (!autoplay) return clearInterval(tabTimer);
          const i = tabs.findIndex((t) => t.getAttribute("aria-selected") === "true");
          selectTab(tabs[(i + 1) % tabs.length]);
        }, 4200);
      }
    }, { threshold: 0.4 });
    showIO.observe($(".showcase"));
  }

  /* ---------- Galería: filtros ---------- */
  const items = $$(".g-item");
  $$(".filters button").forEach((btn) => btn.addEventListener("click", () => {
    $$(".filters button").forEach((b) => b.classList.toggle("active", b === btn));
    const f = btn.dataset.filter;
    items.forEach((it, i) => {
      const show = f === "all" || it.dataset.cat === f;
      it.classList.toggle("hide", !show);
      it.classList.remove("pop");
      if (show && !reduceMotion) { void it.offsetWidth; it.style.animationDelay = `${(i % 8) * 40}ms`; it.classList.add("pop"); }
    });
  }));

  /* ---------- Galería: visor ---------- */
  const lb = $("#lightbox");
  if (lb && typeof lb.showModal === "function") {
    const lbImg = $("img", lb), lbCap = $("figcaption", lb);
    let current = 0;
    const visible = () => items.filter((it) => !it.classList.contains("hide"));
    const show = (idx) => {
      const list = visible();
      current = (idx + list.length) % list.length;
      const it = list[current], img = $("img", it);
      lbImg.src = it.getAttribute("href");
      lbImg.alt = img.alt;
      lbCap.textContent = img.alt;
      lbImg.style.animation = "none"; void lbImg.offsetWidth; lbImg.style.animation = "";
    };
    items.forEach((it) => it.addEventListener("click", (e) => {
      e.preventDefault();
      show(visible().indexOf(it));
      lb.showModal();
      document.body.style.overflow = "hidden";
    }));
    lb.addEventListener("close", () => { document.body.style.overflow = ""; });
    $(".lb-close", lb).addEventListener("click", () => lb.close());
    $(".lb-prev", lb).addEventListener("click", () => show(current - 1));
    $(".lb-next", lb).addEventListener("click", () => show(current + 1));
    lb.addEventListener("click", (e) => { if (e.target === lb || e.target.tagName === "FIGURE") lb.close(); });
    lb.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
    let sx = null;
    lb.addEventListener("touchstart", (e) => { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", (e) => {
      if (sx === null) return;
      const dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
      sx = null;
    });
  }

  /* ---------- Opiniones ---------- */
  const rc = $("#review-cards");
  if (rc && REVIEWS.length) {
    const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
    rc.innerHTML = REVIEWS.map((r) => `
      <figure class="review-card reveal is-visible">
        <span class="rating-stars" aria-label="${r.estrellas || 5} estrellas">${'<svg class="ic"><use href="#i-star"/></svg>'.repeat(r.estrellas || 5)}</span>
        <blockquote>“${esc(r.texto)}”</blockquote>
        <figcaption>${esc(r.autor)} · reseña de Google</figcaption>
      </figure>`).join("");
    rc.hidden = false;
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
