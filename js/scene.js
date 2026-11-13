/* Diver Lauro · escena 3D del hero (Three.js)
   Día: globos de colores de la marca + confeti.
   Noche: globos metalizados dorados/plata/negro, bola de discoteca y focos. */
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const root = document.documentElement;
const canvas = document.getElementById("scene");

function supportsWebGL() {
  try { const c = document.createElement("canvas"); return !!(c.getContext("webgl2") || c.getContext("webgl")); } catch (e) { return false; }
}

if (!canvas || !supportsWebGL()) {
  root.classList.add("no-webgl");
} else {
  init();
}

function init() {
  const hero = canvas.closest(".hero");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const small = () => hero.clientWidth < 700;
  const { MathUtils: M } = THREE;

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, small() ? 1.5 : 1.75));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
  camera.position.set(0, 0, 18);

  /* ---------- Luces ---------- */
  const hemi = new THREE.HemisphereLight(0xffffff, 0xffe9a0, 1.1);
  const sunLight = new THREE.DirectionalLight(0xffffff, 1.6);
  sunLight.position.set(5, 8, 7);
  const pinkLight = new THREE.PointLight(0xff4fd8, 0, 30, 1.5);
  const cyanLight = new THREE.PointLight(0x39d5ff, 0, 30, 1.5);
  scene.add(hemi, sunLight, pinkLight, cyanLight);

  /* ---------- Paletas ---------- */
  const DAY = [
    { c: "#EBD450", m: 0, r: 0.2 }, { c: "#0D305D", m: 0, r: 0.22 }, { c: "#F25C54", m: 0, r: 0.2 },
    { c: "#2B7BE4", m: 0, r: 0.2 }, { c: "#FFFFFF", m: 0, r: 0.25 }, { c: "#FF7AB6", m: 0, r: 0.2 },
  ];
  const NIGHT = [
    { c: "#E8B84A", m: 0.95, r: 0.22 }, { c: "#16161C", m: 0.7, r: 0.25 }, { c: "#D6DAE6", m: 1, r: 0.18 },
    { c: "#FF4FD8", m: 0.55, r: 0.25 }, { c: "#E8B84A", m: 0.95, r: 0.22 }, { c: "#7A3CFF", m: 0.55, r: 0.25 },
  ];
  const CONF_DAY = ["#EBD450", "#0D305D", "#F25C54", "#2B7BE4", "#FFFFFF", "#16B39A"];
  const CONF_NIGHT = ["#E8B84A", "#F7F1DD", "#FF4FD8", "#39D5FF", "#D6DAE6", "#E8B84A"];

  /* ---------- Globos ---------- */
  const profile = [];
  for (let i = 0; i <= 28; i++) {
    const t = i / 28, a = t * Math.PI;
    profile.push(new THREE.Vector2(Math.max(Math.sin(a) * (0.8 + 0.2 * t), 0.001), -Math.cos(a) * 1.18));
  }
  const balloonGeo = new THREE.LatheGeometry(profile, 40);
  const knotGeo = new THREE.ConeGeometry(0.13, 0.2, 14);
  knotGeo.rotateX(Math.PI);
  const stringMat = new THREE.LineBasicMaterial({ color: 0x0d305d, transparent: true, opacity: 0.35 });

  const balloons = [];
  const balloonMeshes = [];
  const mkBalloon = (i) => {
    const g = new THREE.Group();
    const mat = new THREE.MeshPhysicalMaterial({ color: DAY[i % 6].c, roughness: 0.2, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.08 });
    const body = new THREE.Mesh(balloonGeo, mat);
    const knot = new THREE.Mesh(knotGeo, mat);
    knot.position.y = -1.24;
    const pts = [];
    for (let k = 0; k <= 12; k++) pts.push(new THREE.Vector3(Math.sin(k * 0.9) * 0.08, -1.3 - k * 0.28, 0));
    const string = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), stringMat);
    g.add(body, knot, string);
    body.userData.balloon = g;
    balloonMeshes.push(body);
    scene.add(g);
    const b = { g, mat, idx: i, home: new THREE.Vector3(), phase: Math.random() * Math.PI * 2, speed: M.randFloat(0.5, 0.9), size: M.randFloat(0.75, 1.15), scale: 0, popped: false, respawnAt: 0 };
    balloons.push(b);
    return b;
  };

  /* ---------- Confeti ---------- */
  const CONF = small() ? 80 : 130;
  const confGeo = new THREE.PlaneGeometry(0.13, 0.24);
  const confMat = new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, roughness: 0.45, metalness: 0.25 });
  const confetti = new THREE.InstancedMesh(confGeo, confMat, CONF);
  confetti.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  scene.add(confetti);
  const cp = Array.from({ length: CONF }, () => ({
    p: new THREE.Vector3(), v: new THREE.Vector3(), r: new THREE.Euler(), rv: new THREE.Vector3(), burst: 0,
  }));
  const tmpM = new THREE.Matrix4(), tmpQ = new THREE.Quaternion(), tmpS = new THREE.Vector3(1, 1, 1), tmpC = new THREE.Color();
  const setConfColors = (mode) => {
    const pal = mode === "night" ? CONF_NIGHT : CONF_DAY;
    for (let i = 0; i < CONF; i++) confetti.setColorAt(i, tmpC.set(pal[i % pal.length]));
    confetti.instanceColor.needsUpdate = true;
  };

  /* ---------- Bola de discoteca y focos ---------- */
  const disco = new THREE.Group();
  const discoBall = new THREE.Mesh(
    new THREE.SphereGeometry(1.25, 30, 18),
    new THREE.MeshStandardMaterial({ color: 0xdedfe8, metalness: 1, roughness: 0.12, flatShading: true, envMapIntensity: 1.6 })
  );
  const discoString = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, 1.2, 0), new THREE.Vector3(0, 12, 0)]),
    new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.4 })
  );
  disco.add(discoBall, discoString);
  const beams = [];
  const beamColors = [0xff4fd8, 0x39d5ff, 0xebd450, 0x9b5de5];
  beamColors.forEach((col, i) => {
    const geo = new THREE.ConeGeometry(1.5, 16, 32, 1, true);
    geo.translate(0, -8, 0);
    const mat = new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
    const beam = new THREE.Mesh(geo, mat);
    beam.userData.base = (i - 1.5) * 0.45;
    beam.userData.speed = 0.5 + i * 0.13;
    disco.add(beam);
    beams.push(beam);
  });
  disco.scale.setScalar(0.001);
  scene.add(disco);

  /* ---------- Layout ---------- */
  let hw = 1, hh = 1;
  const layout = () => {
    const w = hero.clientWidth, h = hero.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    hh = Math.tan(M.degToRad(camera.fov / 2)) * camera.position.z;
    hw = hh * camera.aspect;

    const n = small() ? 5 : 11;
    while (balloons.length < n) mkBalloon(balloons.length);
    balloons.forEach((b, i) => {
      b.g.visible = i < n;
      placeHome(b, i, n);
    });
    if (small()) disco.position.set(hw * 0.05, hh * 0.72, -3);
    else disco.position.set(hw * 0.55, hh * 0.74, -1);
    disco.userData.s = small() ? 0.5 : 0.75;
  };
  const placeHome = (b, i, n) => {
    const rnd = (k) => { const x = Math.sin((i + 1) * 12.9898 * (k + 1)) * 43758.5453; return x - Math.floor(x); };
    if (small()) {
      // móvil: franja superior, el texto queda abajo
      // móvil: franja superior reservada (el texto empieza debajo)
      b.size = 0.38 + rnd(4) * 0.12;
      b.home.set(M.lerp(-hw * 0.78, hw * 0.78, (i + 0.5) / n) + (rnd(1) - 0.5) * 0.3, M.lerp(hh * 0.56, hh * 0.7, rnd(2)), M.lerp(-1.5, 0.5, rnd(3)));
    } else {
      // escritorio: lado derecho, el texto queda a la izquierda
      const col = i % 4, row = Math.floor(i / 4);
      b.home.set(
        M.lerp(hw * 0.26, hw * 0.95, (col + rnd(1) * 0.8) / 4),
        M.lerp(-hh * 0.55, hh * 0.32, (row + rnd(2) * 0.7) / 3),
        M.lerp(-3, 1.5, rnd(3))
      );
    }
    if (!b.init) { b.g.position.copy(b.home); b.g.position.y -= hh * 1.2; b.init = true; }
  };
  const resetConf = (c, fromTop) => {
    c.p.set(M.randFloatSpread(hw * 2.2), fromTop ? hh + M.randFloat(0, hh * 2) : M.randFloatSpread(hh * 2), M.randFloat(-4, 3));
    c.v.set(M.randFloatSpread(0.3), -M.randFloat(0.5, 1.1), 0);
    c.r.set(Math.random() * 6, Math.random() * 6, Math.random() * 6);
    c.rv.set(M.randFloatSpread(4), M.randFloatSpread(4), M.randFloatSpread(4));
    c.burst = 0;
  };

  layout();
  cp.forEach((c) => resetConf(c, false));

  /* ---------- Modo ---------- */
  let mode = root.dataset.mode === "night" ? "night" : "day";
  const target = { hemi: 1.1, sun: 1.6, neon: 0, disco: 0, beam: 0, exposure: 1.05 };
  const applyModeTargets = () => {
    const night = mode === "night";
    target.hemi = night ? 0.25 : 1.1;
    target.sun = night ? 0.5 : 1.6;
    target.neon = night ? 60 : 0;
    target.disco = night ? 1 : 0;
    target.beam = night ? 0.07 : 0;
    target.exposure = night ? 1.15 : 1.05;
    hemi.groundColor.set(night ? 0x2a1660 : 0xffe9a0);
    stringMat.color.set(night ? 0xd6dae6 : 0x0d305d);
    setConfColors(mode);
  };
  applyModeTargets();
  const snap = () => {
    // aplica los valores finales sin animar (primer render / movimiento reducido)
    hemi.intensity = target.hemi; sunLight.intensity = target.sun;
    pinkLight.intensity = cyanLight.intensity = target.neon;
    disco.scale.setScalar(Math.max(target.disco * disco.userData.s, 0.001));
    beams.forEach((b) => (b.material.opacity = target.beam));
    renderer.toneMappingExposure = target.exposure;
    const pal = mode === "night" ? NIGHT : DAY;
    balloons.forEach((b) => { const p = pal[b.idx % 6]; b.mat.color.set(p.c); b.mat.metalness = p.m; b.mat.roughness = p.r; });
  };
  snap();
  window.addEventListener("dl:mode", (e) => {
    mode = e.detail === "night" ? "night" : "day";
    applyModeTargets();
    if (reduce) { snap(); render(0); }
  });

  /* ---------- Interacción ---------- */
  const pointer = new THREE.Vector2(), look = new THREE.Vector2();
  const ray = new THREE.Raycaster();
  let hovering = false;
  const toNdc = (e) => {
    const r = canvas.getBoundingClientRect();
    pointer.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  };
  const hit = () => {
    ray.setFromCamera(pointer, camera);
    const h = ray.intersectObjects(balloonMeshes.filter((m) => m.userData.balloon.visible), false)[0];
    return h && balloons.find((b) => b.g === h.object.userData.balloon && !b.popped);
  };
  hero.addEventListener("pointermove", (e) => {
    toNdc(e);
    look.set(pointer.x, pointer.y);
    if (e.pointerType === "mouse" && !e.target.closest("a, button")) {
      hovering = !!hit();
      hero.style.cursor = hovering ? "pointer" : "";
    }
  });
  hero.addEventListener("pointerleave", () => look.set(0, 0));
  hero.addEventListener("pointerdown", (e) => {
    if (e.target.closest("a, button")) return;
    toNdc(e);
    const b = hit();
    if (b) pop(b);
  });

  const pop = (b) => {
    b.popped = true;
    b.respawnAt = clock.elapsedTime + 1.4;
    // explosión de confeti desde el globo
    let n = 0;
    for (const c of cp) {
      if (n >= 26) break;
      if (c.burst > 0) continue;
      c.p.copy(b.g.position);
      const a = Math.random() * Math.PI * 2, s = M.randFloat(3, 7);
      c.v.set(Math.cos(a) * s, Math.sin(a) * s + 2, M.randFloatSpread(3));
      c.burst = 1;
      n++;
    }
    const hint = document.querySelector(".hero-hint");
    if (hint) hint.style.opacity = "0";
    if (reduce) render(0);
  };

  /* ---------- Bucle ---------- */
  const clock = new THREE.Clock();
  let running = false, visible = true;
  const render = (dt) => {
    const t = clock.elapsedTime;
    const k = reduce ? 1 : 1 - Math.pow(0.04, dt); // suavizado independiente de FPS

    // luces y bola según modo
    hemi.intensity = M.lerp(hemi.intensity, target.hemi, k);
    sunLight.intensity = M.lerp(sunLight.intensity, target.sun, k);
    pinkLight.intensity = cyanLight.intensity = M.lerp(pinkLight.intensity, target.neon, k);
    renderer.toneMappingExposure = M.lerp(renderer.toneMappingExposure, target.exposure, k);
    pinkLight.position.set(Math.sin(t * 0.9) * hw, Math.cos(t * 0.7) * hh * 0.6, 4);
    cyanLight.position.set(Math.cos(t * 0.8) * hw, Math.sin(t * 1.1) * hh * 0.6, 4);
    const ds = M.lerp(disco.scale.x, Math.max(target.disco * disco.userData.s, 0.001), k * 0.8);
    disco.scale.setScalar(ds);
    disco.visible = ds > 0.01;
    discoBall.rotation.y += dt * 0.5;
    disco.position.y += Math.sin(t * 1.3) * 0.002;
    beams.forEach((bm) => {
      bm.material.opacity = M.lerp(bm.material.opacity, target.beam, k);
      bm.rotation.z = bm.userData.base + Math.sin(t * bm.userData.speed) * 0.55;
      bm.rotation.x = Math.cos(t * bm.userData.speed * 0.8) * 0.3;
    });

    // globos
    const pal = mode === "night" ? NIGHT : DAY;
    for (const b of balloons) {
      if (!b.g.visible) continue;
      const p = pal[b.idx % 6];
      tmpC.set(p.c);
      b.mat.color.lerp(tmpC, k);
      b.mat.metalness = M.lerp(b.mat.metalness, p.m, k);
      b.mat.roughness = M.lerp(b.mat.roughness, p.r, k);

      if (b.popped && t > b.respawnAt) {
        b.popped = false; b.scale = 0;
        b.g.position.copy(b.home); b.g.position.y -= hh * 0.9;
      }
      const goal = b.popped ? 0 : b.size;
      b.scale = b.popped ? M.lerp(b.scale, 0, 1 - Math.pow(0.0001, dt)) : M.lerp(b.scale, goal, 1 - Math.pow(0.15, dt));
      b.g.scale.setScalar(Math.max(b.scale, 0.0001));
      const sway = Math.sin(t * b.speed + b.phase);
      const tx = b.home.x + sway * 0.35, ty = b.home.y + Math.sin(t * b.speed * 1.3 + b.phase * 2) * 0.35;
      b.g.position.x = M.lerp(b.g.position.x, tx, 1 - Math.pow(0.3, dt));
      b.g.position.y = M.lerp(b.g.position.y, ty, 1 - Math.pow(0.12, dt));
      b.g.position.z = M.lerp(b.g.position.z, b.home.z, 1 - Math.pow(0.3, dt));
      b.g.rotation.z = -sway * 0.12;
      b.g.rotation.y = t * 0.2 + b.phase;
    }

    // confeti
    for (let i = 0; i < CONF; i++) {
      const c = cp[i];
      if (c.burst > 0) {
        c.v.multiplyScalar(Math.pow(0.12, dt));
        c.v.y -= 6 * dt;
        c.burst -= dt * 0.25;
        if (c.burst <= 0) c.burst = 0;
      } else {
        c.v.y = M.lerp(c.v.y, -0.9, dt);
        c.v.x = Math.sin(t * 1.5 + i) * 0.35;
      }
      c.p.addScaledVector(c.v, dt);
      c.r.x += c.rv.x * dt; c.r.y += c.rv.y * dt; c.r.z += c.rv.z * dt;
      if (c.p.y < -hh - 1) resetConf(c, true);
      tmpQ.setFromEuler(c.r);
      tmpM.compose(c.p, tmpQ, tmpS);
      confetti.setMatrixAt(i, tmpM);
    }
    confetti.instanceMatrix.needsUpdate = true;

    // cámara con paralaje suave
    camera.position.x = M.lerp(camera.position.x, look.x * 0.9, 1 - Math.pow(0.1, dt));
    camera.position.y = M.lerp(camera.position.y, look.y * 0.6, 1 - Math.pow(0.1, dt));
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
  };

  const loop = () => {
    if (!running) return;
    const dt = Math.min(clock.getDelta(), 0.05);
    render(dt);
    requestAnimationFrame(loop);
  };
  const start = () => {
    if (reduce || running || !visible || document.hidden) return;
    running = true; clock.getDelta(); requestAnimationFrame(loop);
  };
  const stop = () => { running = false; };

  if (reduce) {
    balloons.forEach((b) => { b.scale = b.size; b.g.scale.setScalar(b.size); b.g.position.copy(b.home); });
    render(0);
  } else {
    start();
  }

  new ResizeObserver(() => { layout(); if (reduce) render(0); }).observe(hero);
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; visible ? start() : stop(); }).observe(hero);
  document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
}
