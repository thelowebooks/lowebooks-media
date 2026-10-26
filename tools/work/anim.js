// Shared timing helpers: every frame is drawn from the time t alone.
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const ease = p => 1 - Math.pow(1 - clamp(p, 0, 1), 3);
// Show an element between [start, end): fade + rise in, fade out.
function show(el, t, start, end, opts = {}) {
  const fin = opts.fin ?? 0.3, fout = opts.fout ?? 0.2, rise = opts.rise ?? 40, scaleFrom = opts.scaleFrom ?? 1;
  if (t < start || t >= end) { el.style.opacity = 0; return; }
  const pin = ease((t - start) / fin);
  const pout = opts.noOut ? 1 : clamp((end - t) / fout, 0, 1);
  el.style.opacity = Math.min(pin, pout);
  const s = scaleFrom + (1 - scaleFrom) * pin;
  el.style.transform = `translateY(${(1 - pin) * rise}px) scale(${s})`;
}
window.__ready = document.fonts.ready.then(() => true);
