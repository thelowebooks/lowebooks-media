"""Generate a 3-question timer challenge video page from a config.
usage: python make_timer.py <config.json> <out.html>
config: {bg, fg, acc, ring, hook, hookSub, qs:[..], qsize?, endH, endSub, endLead, endTitle}
bg = background, fg = text on the background, acc = hook sub line / label colour, ring = timer ring colour.
The question card is always cream with ink text. Question text is supplied by the config (kept out of the repo).
"""
import json, sys
cfg = json.load(open(sys.argv[1]))
T = r'''<!doctype html>
<html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css">
<style>
:root{--bg:__BG__;--fg:__FG__;--acc:__ACC__;--ring:__RING__}
body{background:var(--bg)}
.frame{width:1080px;height:1920px;background:var(--bg);color:var(--fg)}
.brand{color:var(--fg)}
#hook{justify-content:center;padding:0 90px;gap:36px}
#hook h1{font-size:__HSIZE__px;margin:0}
#hook p{font-size:__SSIZE__px;margin:0;color:var(--acc)}
#q{align-items:center;justify-content:center;padding:0 80px;gap:56px}
#q .count{font-size:40px;color:var(--fg)}
#q .card{width:920px;min-height:620px;padding:72px 70px;display:flex;align-items:center;color:#1E1A16}
#q .card div{font-size:__QSIZE__px;line-height:1.08}
.timer{position:relative;width:260px;height:260px}
.timer svg{position:absolute;inset:0}
.timer .num{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:128px;color:var(--fg)}
#end{justify-content:center;padding:0 90px;gap:28px}
#end h1{font-size:136px;margin:0}
#end .sub{font-size:56px;font-weight:500;margin:0 0 60px;color:var(--acc)}
#end .book{font-size:40px;font-weight:500}
#end .title{font-size:78px}
#end .tag{font-size:44px;font-weight:700;margin-top:60px;color:var(--acc)}
</style></head>
<body><div class="frame">
<div class="brand label">Lowe Books</div>
<section id="hook" class="scene"><h1 class="display" id="h1"></h1><p class="display" id="h2"></p></section>
<section id="q" class="scene">
  <div class="count label" id="count"></div>
  <div class="card"><div class="display" id="qtext"></div></div>
  <div class="timer"><svg viewBox="0 0 260 260"><circle cx="130" cy="130" r="112" fill="none" stroke="rgba(128,128,128,.28)" stroke-width="18"/><circle id="ring" cx="130" cy="130" r="112" fill="none" stroke="var(--ring)" stroke-width="18" stroke-linecap="round" stroke-dasharray="703.7" transform="rotate(-90 130 130)"/></svg><div class="num display" id="num">5</div></div>
</section>
<section id="end" class="scene">
  <h1 class="display" id="eh"></h1>
  <p class="sub" id="es"></p>
  <div class="book" id="el"></div>
  <div class="title display" id="et"></div>
  <div class="book">by Rann Lowe · on Amazon</div>
  <div class="tag">Get curious. Scroll less.</div>
</section>
</div>
<script src="anim.js"></script>
<script>
const C = __CFG__;
const QS = C.qs;
const HOOK = 2.5, PER = 5, END = HOOK + QS.length * PER;
window.DURATION = END + 3.5;
window.EVENTS = [];
QS.forEach((_, i) => { const s = HOOK + i * PER; EVENTS.push(['pop', s]); for (let k = 1; k < PER; k++) EVENTS.push([k >= PER - 2 ? 'tickhi' : 'tick', s + k]); });
EVENTS.push(['ding', END]);
document.getElementById('h1').textContent = C.hook;
document.getElementById('h2').textContent = C.hookSub;
document.getElementById('eh').textContent = C.endH;
document.getElementById('es').textContent = C.endSub;
document.getElementById('el').textContent = C.endLead;
document.getElementById('et').textContent = C.endTitle;
function render(t) {
  show(document.getElementById('hook'), t, 0, HOOK);
  const q = document.getElementById('q');
  if (t >= HOOK && t < END) {
    const i = Math.floor((t - HOOK) / PER), lt = t - HOOK - i * PER;
    q.style.opacity = Math.min(1, (t - HOOK) / 0.25, (END - t) / 0.2);
    document.getElementById('count').textContent = (i + 1) + ' / ' + QS.length;
    const qt = document.getElementById('qtext'); qt.textContent = QS[i];
    const p = ease(lt / 0.25);
    qt.parentElement.style.transform = 'scale(' + (0.94 + 0.06 * p) + ')'; qt.style.opacity = p;
    document.getElementById('num').textContent = Math.max(1, PER - Math.floor(lt));
    document.getElementById('ring').style.strokeDashoffset = 703.7 * clamp(lt / PER, 0, 1);
  } else q.style.opacity = 0;
  show(document.getElementById('end'), t, END, DURATION + 1, {noOut: true});
}
</script></body></html>'''
out = (T.replace('__CFG__', json.dumps(cfg, ensure_ascii=False)).replace('__BG__', cfg['bg']).replace('__FG__', cfg['fg'])
       .replace('__ACC__', cfg['acc']).replace('__RING__', cfg['ring']).replace('__QSIZE__', str(cfg.get('qsize', 80)))
       .replace('__HSIZE__', str(cfg.get('hsize', 150))).replace('__SSIZE__', str(cfg.get('ssize', 80))))
open(sys.argv[2], 'w', encoding='utf-8').write(out)
print('wrote', sys.argv[2])
