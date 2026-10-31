"""Generate a 5-slide Instagram carousel page (1080x1350) from a config; render with render.py still <html> 1080 1350 <prefix> 0 1 2 3 4
usage: python make_carousel.py <config.json> <out.html>
config: {c0 (hook slide bg), c0fg, num (numeral colour), hint (hint colour), c4 (end slide bg), c4fg, c4acc, h0, p0, qs:[{q,hint}], endH, endLead, endTitle}
"""
import json, sys, html
c = json.load(open(sys.argv[1]))
e = html.escape
qs = ''.join(f'''<section class="slide qs" id="s{i+1}"><div class="top label"><span>Lowe Books</span><span>{i+2} / 5</span></div><div class="n display">{i+1}</div>
  <div class="q display">{e(q['q'])}</div><div class="hint">{e(q['hint'])}</div></section>
''' for i, q in enumerate(c['qs']))
page = f'''<!doctype html>
<html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css">
<style>
.frame{{width:1080px;height:1350px}}
.slide{{position:absolute;inset:0;display:none;flex-direction:column;justify-content:space-between;padding:96px 90px}}
.top{{font-size:26px;display:flex;justify-content:space-between}}
#s0{{background:{c['c0']};color:{c['c0fg']}}}
#s0 h1{{font-size:{c.get('h0size',140)}px;margin:0 0 40px}}
#s0 p{{font-size:52px;font-weight:600;margin:0}}
.qs{{background:var(--cream)}}
.qs .n{{font-size:300px;color:{c['num']};line-height:.8}}
.qs .q{{font-size:{c.get('qsize',88)}px;line-height:1.06}}
.qs .hint{{font-size:36px;font-weight:600;color:{c['hint']}}}
#s4{{background:{c['c4']};color:{c['c4fg']}}}
#s4 h1{{font-size:120px;margin:0 0 50px}}
#s4 .from{{font-size:36px;font-weight:500}}
#s4 .title{{font-size:64px;margin:8px 0}}
#s4 .tag{{font-size:36px;font-weight:700;color:{c['c4acc']}}}
.arrow{{font-size:40px;font-weight:700}}
</style></head>
<body><div class="frame">
<section class="slide" id="s0"><div class="top label"><span>Lowe Books</span><span>1 / 5</span></div>
  <div><h1 class="display">{e(c['h0'])}</h1><p>{e(c['p0'])}</p></div><div class="arrow">Swipe →</div></section>
{qs}<section class="slide" id="s4"><div class="top label"><span>Lowe Books</span><span>5 / 5</span></div>
  <div><h1 class="display">{e(c['endH'])}</h1><div class="from">{e(c['endLead'])}</div><div class="title display">{e(c['endTitle'])}</div><div class="from">by Rann Lowe · link in bio</div></div>
  <div class="tag">Get curious. Scroll less.</div></section>
</div>
<script src="anim.js"></script>
<script>function render(n){{document.querySelectorAll('.slide').forEach((s,i)=>s.style.display=i===n?'flex':'none');}}</script></body></html>'''
open(sys.argv[2], 'w', encoding='utf-8').write(page)
print('wrote', sys.argv[2])
