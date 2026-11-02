"""Generate a maze video page or a maze pin page from a pool folder.
usage: python make_maze.py video <maze_dir> <out.html> [hook] [bg]
       python make_maze.py pin   <maze_dir> <out.html> [headline]
maze_dir is relative to tools/work, e.g. ../maze/pool/circle-04 (built by tools/scripts/maze_pool.py).
Video: opens on the maze with a 10 s countdown, reveals the solution, ends on the book card (about 16 s).
Render videos at 1080x1920 and pins at 1000x1500 with tools/scripts/render.py.
"""
import sys, html as H
mode, d, out = sys.argv[1], sys.argv[2], sys.argv[3]
hook = sys.argv[4] if len(sys.argv) > 4 else ('Beat this maze in 10 seconds.' if mode == 'video' else 'Can you solve this maze?')
bg = sys.argv[5] if len(sys.argv) > 5 else '#1E1A16'
VIDEO = r'''<!doctype html>
<html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css">
<style>
body{background:__BG__}
.frame{width:1080px;height:1920px;background:__BG__;color:var(--cream)}
.brand{color:var(--yellow)}
#play{align-items:center;padding-top:240px;gap:36px}
.mh{font-size:84px;line-height:1.02;text-align:center;width:920px}
.head{height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;width:920px}
.secs{font-size:150px;color:var(--yellow);line-height:1}
.bar{width:920px;height:18px;border-radius:9px;background:rgba(255,245,220,.18);overflow:hidden}
.bar div{height:100%;background:var(--yellow);border-radius:9px}
.up{font-size:130px;color:var(--coral);line-height:1;display:none}
.mazecard{width:940px;height:940px;background:var(--cream);border-radius:56px;position:relative}
.mazecard img{position:absolute;left:40px;top:40px;width:860px;height:860px;object-fit:contain}
.tip{font-size:44px;font-weight:600;color:var(--cream);opacity:.85}
#end{justify-content:center;padding:0 90px;gap:28px}
#end h1{font-size:140px;margin:0}
#end .sub{font-size:60px;font-weight:600;margin:0 0 70px;color:var(--yellow)}
#end .book{font-size:40px;font-weight:500}
#end .title{font-size:76px}
#end .tag{font-size:44px;font-weight:700;margin-top:60px;color:var(--yellow)}
</style></head>
<body><div class="frame">
<div class="brand label">Lowe Books</div>
<section id="play" class="scene">
  <div class="mh display">__HOOK__</div>
  <div class="head"><div class="secs display" id="secs">10</div><div class="bar"><div id="bar"></div></div><div class="up display" id="up">Time's up.</div></div>
  <div class="mazecard"><img src="__DIR__/maze_ink.png"><img id="path" src="__DIR__/path_000.png" style="opacity:0"></div>
  <div class="tip" id="tip">Green dot to red dot. Go!</div>
</section>
<section id="end" class="scene">
  <h1 class="display">Did you make it?</h1>
  <p class="sub">Tell us in the comments. 100 more mazes, solutions included.</p>
  <div class="title display">Easy Maze Puzzle Book for Seniors</div>
  <div class="book">by Rann Lowe · on Amazon</div>
  <div class="tag">Get curious. Scroll less.</div>
</section>
</div>
<script src="anim.js"></script>
<script>
const DIR = '__DIR__', SECS = 10, UP = SECS, DRAW = 2.0, END = UP + 3.2;
window.DURATION = END + 3.2;
window.EVENTS = [];
for (let s = 1; s < SECS; s++) EVENTS.push([s >= SECS - 3 ? 'tickhi' : 'tick', s]);
EVENTS.push(['ding', UP]); EVENTS.push(['ding', END]);
const pre = []; for (let i = 0; i <= 60; i++) { const im = new Image(); pre.push(new Promise(r => { im.onload = r; im.onerror = () => r('err'); })); im.src = `${DIR}/path_${String(i).padStart(3, '0')}.png`; }
window.__ready = Promise.all([document.fonts.ready, ...pre]).then(() => true);
function render(t) {
  show(document.getElementById('play'), t, -1, END, {rise: 0, fin: 0.001});
  const left = clamp(SECS - t, 0, SECS), playing = t < UP;
  document.getElementById('secs').style.display = playing ? 'block' : 'none';
  document.querySelector('.bar').style.display = playing ? 'block' : 'none';
  document.getElementById('up').style.display = playing ? 'none' : 'block';
  document.getElementById('tip').style.visibility = playing ? 'visible' : 'hidden';
  document.getElementById('secs').textContent = Math.ceil(left) || 0;
  document.getElementById('bar').style.width = (left / SECS * 100) + '%';
  const p = document.getElementById('path');
  if (t >= UP + 0.4) { const i = Math.round(clamp((t - UP - 0.4) / DRAW, 0, 1) * 60); p.src = `${DIR}/path_${String(i).padStart(3, '0')}.png`; p.style.opacity = 1; } else p.style.opacity = 0;
  show(document.getElementById('end'), t, END, DURATION + 1, {noOut: true});
}
</script></body></html>'''
PIN = r'''<!doctype html>
<html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css">
<style>
.frame{width:1000px;height:1500px;background:__BG__;color:var(--cream);padding:84px 80px 78px;display:flex;flex-direction:column}
.top{font-size:26px}
h1{margin:30px 0 0;font-size:92px}
.mazecard{margin-top:40px;align-self:center;width:760px;height:760px;background:var(--cream);border-radius:44px;position:relative;transform:rotate(-1.2deg)}
.mazecard img{position:absolute;left:34px;top:34px;width:692px;height:692px;object-fit:contain}
.spacer{flex:1}
.foot{display:flex;flex-direction:column;gap:6px}
.foot .from{font-size:28px;font-weight:500}
.foot .title{font-size:42px}
.foot .tag{font-size:28px;font-weight:700;color:var(--yellow);margin-top:14px}
</style></head>
<body><div class="frame">
<div class="top label">Lowe Books</div>
<h1 class="display">__HOOK__</h1>
<div class="mazecard"><img src="__DIR__/maze_ink.png"></div>
<div class="spacer"></div>
<div class="foot"><div class="from">Green dot to red dot. Solution in</div><div class="title display">Easy Maze Puzzle Book for Seniors</div><div class="from">by Rann Lowe · 100 large-print mazes</div><div class="tag">Get curious. Scroll less.</div></div>
</div><script src="anim.js"></script><script>function render(t){}</script></body></html>'''
T = VIDEO if mode == 'video' else PIN
open(out, 'w', encoding='utf-8').write(T.replace('__DIR__', d).replace('__HOOK__', H.escape(hook)).replace('__BG__', bg))
print('wrote', out)
