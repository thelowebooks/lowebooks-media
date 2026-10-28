"""Generate a timed trivia video page from a config.
usage: python make_trivia.py <config.json> <out.html>
config: {bg, ink, accent, hook, hookSub, qs:[{q, options?:[..], answer:"B"|"text", note?}], endTitle, endBook, per?}
Open-ended questions have no options; answer is the text shown at the reveal.
"""
import json, sys
cfg = json.load(open(sys.argv[1]))
TEMPLATE = r'''<!doctype html>
<html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css">
<style>
:root{--bg:__BG__;--fg:__FG__;--acc:__ACC__}
body{background:var(--bg)}
.frame{width:1080px;height:1920px;background:var(--bg);color:var(--fg)}
.brand{color:var(--acc)}
#hook{justify-content:center;padding:0 90px;gap:40px}
#hook h1{font-size:150px;margin:0}
#hook p{font-size:68px;font-weight:700;margin:0;color:var(--acc)}
#q{align-items:center;justify-content:center;padding:150px 80px 0;gap:44px}
#q .count{font-size:38px;color:var(--acc)}
#q .card{width:920px;padding:64px 60px;display:flex;align-items:center}
#q .card .display{font-size:__QSIZE__px;line-height:1.08}
.opts{display:flex;flex-direction:column;gap:22px;width:920px}
.opt{display:flex;align-items:center;gap:28px;background:var(--fg);color:var(--bg);border-radius:30px;padding:26px 34px;font-size:50px;font-weight:700;min-height:112px}
.opt b{flex:0 0 72px;height:72px;border-radius:50%;background:var(--acc);color:#1E1A16;display:flex;align-items:center;justify-content:center;font-family:'Bricolage',sans-serif;font-weight:800;font-size:44px}
.opt.good{background:var(--acc);color:#1E1A16;transform:scale(1.04)}
.opt.good b{background:#1E1A16;color:var(--acc)}
.opt.dim{opacity:.28}
.foot{height:260px;display:flex;align-items:center;justify-content:center;width:920px}
.timer{position:relative;width:240px;height:240px}
.timer svg{position:absolute;inset:0}
.timer .num{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:120px;color:var(--fg)}
.answer{display:none;font-size:70px;text-align:center;color:var(--acc);line-height:1.05;max-width:920px}
.answer small{display:block;font-size:34px;letter-spacing:.18em;text-transform:uppercase;color:var(--fg);margin-bottom:14px;font-family:'DM Sans',sans-serif;font-weight:700}
#end{justify-content:center;padding:0 90px;gap:28px}
#end h1{font-size:140px;margin:0}
#end .sub{font-size:56px;font-weight:600;margin:0 0 60px;color:var(--acc)}
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
  <div class="opts" id="opts"></div>
  <div class="foot">
    <div class="timer" id="timer"><svg viewBox="0 0 260 260"><circle cx="130" cy="130" r="112" fill="none" stroke="rgba(255,245,220,.18)" stroke-width="18"/><circle id="ring" cx="130" cy="130" r="112" fill="none" stroke="currentColor" stroke-width="18" stroke-linecap="round" stroke-dasharray="703.7" transform="rotate(-90 130 130)" style="color:var(--acc)"/></svg><div class="num display" id="num">5</div></div>
    <div class="answer display" id="answer"></div>
  </div>
</section>
<section id="end" class="scene">
  <h1 class="display">How many did you get?</h1>
  <p class="sub">Tell us in the comments.</p>
  <div class="book" id="endBook"></div>
  <div class="title display" id="endTitle"></div>
  <div class="book" id="endAuthor"></div>
  <div class="tag">Get curious. Scroll less.</div>
</section>
</div>
<script src="anim.js"></script>
<script>
const CFG = __CFG__;
const QS = CFG.qs, PER = CFG.per || 7.5, TIME = 5, HOOK = 2.5, END = HOOK + QS.length * PER;
window.DURATION = END + 3.5;
window.EVENTS = [];
QS.forEach((_, i) => { const s = HOOK + i * PER; EVENTS.push(['pop', s]); for (let k = 1; k < TIME; k++) EVENTS.push([k >= TIME - 2 ? 'tickhi' : 'tick', s + k]); EVENTS.push(['ding', s + TIME]); });
EVENTS.push(['pop', END]);
document.getElementById('h1').textContent = CFG.hook;
document.getElementById('h2').textContent = CFG.hookSub;
document.getElementById('endBook').textContent = CFG.endBook;
document.getElementById('endTitle').textContent = CFG.endTitle;
document.getElementById('endAuthor').textContent = CFG.endAuthor || 'by Rann Lowe';
const L = 'ABCD';
function render(t) {
  show(document.getElementById('hook'), t, 0, HOOK);
  const q = document.getElementById('q');
  if (t >= HOOK && t < END) {
    const i = Math.floor((t - HOOK) / PER), lt = t - HOOK - i * PER, d = QS[i];
    q.style.opacity = Math.min(1, (t - HOOK) / 0.25, (END - t) / 0.2);
    document.getElementById('count').textContent = (i + 1) + ' / ' + QS.length;
    const qt = document.getElementById('qtext'); qt.textContent = d.q;
    const p = ease(lt / 0.25);
    qt.parentElement.style.transform = 'scale(' + (0.94 + 0.06 * p) + ')'; qt.style.opacity = p;
    const reveal = lt >= TIME;
    const od = document.getElementById('opts');
    if (d.options) {
      od.style.display = 'flex';
      od.innerHTML = d.options.map((o, k) => '<div class="opt' + (reveal ? (L[k] === d.answer ? ' good' : ' dim') : '') + '"><b>' + L[k] + '</b><span>' + o + '</span></div>').join('');
    } else od.style.display = 'none';
    document.getElementById('timer').style.display = reveal ? 'none' : 'block';
    const an = document.getElementById('answer');
    an.style.display = reveal ? 'block' : 'none';
    if (reveal) an.innerHTML = '<small>Answer</small>' + (d.options ? L.indexOf(d.answer) >= 0 ? d.answer + ': ' + d.options[L.indexOf(d.answer)] : d.answer : d.answer);
    document.getElementById('num').textContent = Math.max(1, TIME - Math.floor(lt));
    document.getElementById('ring').style.strokeDashoffset = 703.7 * clamp(lt / TIME, 0, 1);
  } else q.style.opacity = 0;
  show(document.getElementById('end'), t, END, DURATION + 1, {noOut: true});
}
</script></body></html>'''
out = (TEMPLATE.replace('__CFG__', json.dumps(cfg, ensure_ascii=False))
       .replace('__BG__', cfg['bg']).replace('__FG__', cfg.get('fg', '#FFF5DC')).replace('__ACC__', cfg['accent'])
       .replace('__QSIZE__', str(cfg.get('qsize', 58))))
open(sys.argv[2], 'w', encoding='utf-8').write(out)
print('wrote', sys.argv[2])
