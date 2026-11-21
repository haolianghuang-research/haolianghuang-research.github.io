/* Locally authored, low-opacity fluid pigment on the white portfolio background. */
(() => {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const settings = {
    opacity: 0.27,
    radius: 24,
    dissipation: 1.9,
    frameInterval: 1000 / 30,
  };
  let teardown = () => {};

  function start() {
    const canvas = document.createElement('canvas');
    canvas.className = 'fluid-cursor';
    canvas.setAttribute('aria-hidden', 'true');
    const context = canvas.getContext('2d', { alpha: true });
    const pigmentCanvas = document.createElement('canvas');
    const pigmentContext = pigmentCanvas.getContext('2d');
    if (!context || !pigmentContext) return () => {};
    document.body.appendChild(canvas);

    let width, height, columns, rows, count, image;
    let u, v, nextU, nextV, blue, violet, nextBlue, nextViolet;
    let pressure, nextPressure, divergence, curl;
    let lastPointer = null;
    let pendingPointer = null;
    let frame = 0;
    let lastFrame = 0;
    let freshness = 0;
    const clicks = [];

    function resize() {
      width = document.documentElement.clientWidth;
      height = window.innerHeight;
      columns = 144;
      rows = Math.max(64, Math.min(160, Math.round(columns * height / width)));
      count = columns * rows;
      const scale = Math.min(window.devicePixelRatio || 1, 1.5, 1400 / width);
      canvas.width = Math.round(width * scale);
      canvas.height = Math.round(height * scale);
      pigmentCanvas.width = columns;
      pigmentCanvas.height = rows;
      image = pigmentContext.createImageData(columns, rows);
      [u, v, nextU, nextV, blue, violet, nextBlue, nextViolet,
        pressure, nextPressure, divergence, curl] = Array.from(
        { length: 12 }, () => new Float32Array(count),
      );
      lastPointer = pendingPointer = null;
      clicks.length = 0;
      freshness = 0;
    }

    function sample(field, x, y) {
      x = Math.max(0.5, Math.min(columns - 1.501, x));
      y = Math.max(0.5, Math.min(rows - 1.501, y));
      const ix = Math.floor(x), iy = Math.floor(y);
      const fx = x - ix, fy = y - iy, i = ix + iy * columns;
      return (field[i] * (1 - fx) + field[i + 1] * fx) * (1 - fy)
        + (field[i + columns] * (1 - fx) + field[i + columns + 1] * fx) * fy;
    }

    function addPigment(x, y, dx, dy, time, amount) {
      const gx = x * columns, gy = y * rows;
      const radius = Math.max(1.3, settings.radius / width * columns);
      const radiusSquared = radius * radius;
      const mix = (Math.sin(time * 0.0012) + 1) * 0.5;
      for (let py = Math.max(1, Math.floor(gy - radius * 3));
        py < Math.min(rows - 1, gy + radius * 3); py++) {
        for (let px = Math.max(1, Math.floor(gx - radius * 3));
          px < Math.min(columns - 1, gx + radius * 3); px++) {
          const i = px + py * columns, rx = px - gx, ry = py - gy;
          const weight = Math.exp(-(rx * rx + ry * ry) / (radiusSquared * 1.5));
          u[i] += weight * (dx * columns * 6 - ry * 4) * amount;
          v[i] += weight * (dy * rows * 6 + rx * 4) * amount;
          blue[i] = Math.min(3, blue[i] + weight * (0.4 + mix * 0.9) * amount);
          violet[i] = Math.min(3, violet[i] + weight * (1.3 - mix * 0.8) * amount);
        }
      }
      freshness = 1;
    }

    function movePigment(dt) {
      for (let y = 1; y < rows - 1; y++) {
        for (let x = 1; x < columns - 1; x++) {
          const i = x + y * columns, px = x - u[i] * dt, py = y - v[i] * dt;
          nextU[i] = sample(u, px, py) * 0.985;
          nextV[i] = sample(v, px, py) * 0.985;
        }
      }
      [u, nextU] = [nextU, u];
      [v, nextV] = [nextV, v];

      // Vorticity keeps the wisp curling instead of becoming a blurred dot.
      for (let y = 1; y < rows - 1; y++) {
        for (let x = 1; x < columns - 1; x++) {
          const i = x + y * columns;
          curl[i] = 0.5 * (v[i + 1] - v[i - 1] - u[i + columns] + u[i - columns]);
        }
      }
      for (let y = 2; y < rows - 2; y++) {
        for (let x = 2; x < columns - 2; x++) {
          const i = x + y * columns;
          const cx = Math.abs(curl[i + columns]) - Math.abs(curl[i - columns]);
          const cy = Math.abs(curl[i + 1]) - Math.abs(curl[i - 1]);
          const length = Math.hypot(cx, cy) + 0.001;
          u[i] = Math.max(-180, Math.min(180, u[i] + cx / length * curl[i] * dt * 9));
          v[i] = Math.max(-180, Math.min(180, v[i] - cy / length * curl[i] * dt * 9));
        }
      }

      pressure.fill(0);
      nextPressure.fill(0);
      for (let y = 1; y < rows - 1; y++) {
        for (let x = 1; x < columns - 1; x++) {
          const i = x + y * columns;
          divergence[i] = -0.5 * (u[i + 1] - u[i - 1] + v[i + columns] - v[i - columns]);
        }
      }
      for (let iteration = 0; iteration < 12; iteration++) {
        for (let y = 1; y < rows - 1; y++) {
          for (let x = 1; x < columns - 1; x++) {
            const i = x + y * columns;
            nextPressure[i] = (divergence[i] + pressure[i - 1] + pressure[i + 1]
              + pressure[i - columns] + pressure[i + columns]) * 0.25;
          }
        }
        [pressure, nextPressure] = [nextPressure, pressure];
      }
      for (let y = 1; y < rows - 1; y++) {
        for (let x = 1; x < columns - 1; x++) {
          const i = x + y * columns;
          u[i] -= 0.5 * (pressure[i + 1] - pressure[i - 1]);
          v[i] -= 0.5 * (pressure[i + columns] - pressure[i - columns]);
        }
      }
      const fade = Math.exp(-settings.dissipation * dt);
      for (let y = 1; y < rows - 1; y++) {
        for (let x = 1; x < columns - 1; x++) {
          const i = x + y * columns, px = x - u[i] * dt, py = y - v[i] * dt;
          nextBlue[i] = sample(blue, px, py) * fade;
          nextViolet[i] = sample(violet, px, py) * fade;
        }
      }
      [blue, nextBlue] = [nextBlue, blue];
      [violet, nextViolet] = [nextViolet, violet];
      freshness *= fade;
    }

    function paint() {
      for (let i = 0; i < count; i++) {
        const total = blue[i] + violet[i], mix = total ? blue[i] / total : 0;
        const pixel = i * 4;
        image.data[pixel] = Math.round(79 + 70 * mix);
        image.data[pixel + 1] = Math.round(133 - 37 * mix);
        image.data[pixel + 2] = 207 + Math.round(14 * mix);
        image.data[pixel + 3] = Math.round(Math.min(0.75, total * 0.36) * settings.opacity * 255);
      }
      pigmentContext.putImageData(image, 0, 0);
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.drawImage(pigmentCanvas, 0, 0, canvas.width, canvas.height);
    }

    function tick(time) {
      frame = 0;
      if (document.hidden) return;
      if (time - lastFrame < settings.frameInterval) {
        frame = requestAnimationFrame(tick);
        return;
      }
      const dt = Math.min((time - lastFrame) / 1000, 0.05);
      lastFrame = time;
      if (pendingPointer) {
        const point = pendingPointer;
        pendingPointer = null;
        if (lastPointer && point.time - lastPointer.time < 100) {
          const dx = Math.max(-0.08, Math.min(0.08, point.x - lastPointer.x));
          const dy = Math.max(-0.08, Math.min(0.08, point.y - lastPointer.y));
          const distance = Math.hypot(dx * columns, dy * rows);
          if (distance > 0.05) {
            const steps = Math.min(6, Math.max(1, Math.ceil(distance / 2)));
            for (let n = 1; n <= steps; n++) {
              addPigment(lastPointer.x + dx * n / steps, lastPointer.y + dy * n / steps,
                dx, dy, time, 0.55);
            }
          }
        }
        lastPointer = point;
      }
      for (const point of clicks) {
        for (let i = 0; i < 5; i++) {
          const angle = i * Math.PI * 2 / 5;
          addPigment(point.x + 0.007 * Math.cos(angle), point.y + 0.007 * Math.sin(angle),
            0.025 * Math.cos(angle), 0.025 * Math.sin(angle), time + i * 300, 0.65);
        }
      }
      clicks.length = 0;
      if (freshness > 0.008) {
        movePigment(dt);
        paint();
        frame = requestAnimationFrame(tick);
      } else {
        context.clearRect(0, 0, canvas.width, canvas.height);
      }
    }

    function wake() {
      if (!frame && !document.hidden) {
        lastFrame = performance.now() - settings.frameInterval;
        frame = requestAnimationFrame(tick);
      }
    }

    function pointFrom(event) {
      return { x: event.clientX / width, y: event.clientY / height, time: performance.now() };
    }
    function ignore(event) {
      return document.hidden || event.target.closest(
        '.site-header, .page-outline, input, textarea, select, [contenteditable="true"]',
      );
    }
    function pointerMove(event) {
      if (event.pointerType !== 'mouse' || ignore(event)) {
        lastPointer = pendingPointer = null;
        return;
      }
      pendingPointer = pointFrom(event);
      wake();
    }
    function click(event) {
      if (ignore(event) || event.detail === 0) return;
      clicks.push(pointFrom(event));
      // Keep a rapid click sequence bounded without consuming the interaction.
      if (clicks.length > 4) clicks.shift();
      wake();
    }
    function pointerOut(event) {
      if (!event.relatedTarget) lastPointer = pendingPointer = null;
    }
    function visibilityChange() {
      cancelAnimationFrame(frame);
      frame = 0;
      resize();
    }

    resize();
    document.addEventListener('pointermove', pointerMove, { passive: true });
    document.addEventListener('click', click, { passive: true });
    document.addEventListener('pointerout', pointerOut, { passive: true });
    document.addEventListener('visibilitychange', visibilityChange);
    window.addEventListener('resize', resize, { passive: true });
    return () => {
      cancelAnimationFrame(frame);
      document.removeEventListener('pointermove', pointerMove);
      document.removeEventListener('click', click);
      document.removeEventListener('pointerout', pointerOut);
      document.removeEventListener('visibilitychange', visibilityChange);
      window.removeEventListener('resize', resize);
      canvas.remove();
    };
  }

  function syncPreference() {
    teardown();
    teardown = () => {};
    if (!reducedMotion.matches && finePointer.matches) teardown = start();
  }
  reducedMotion.addEventListener('change', syncPreference);
  finePointer.addEventListener('change', syncPreference);
  syncPreference();
})();
