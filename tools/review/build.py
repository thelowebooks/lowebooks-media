import html, json, sys
# usage: python build.py <batches/YYYY-wNN.json> [out.html]  (thumbnails live next to the output in thumbs/)
batch = json.load(open(sys.argv[1], encoding='utf-8'))
OUT = sys.argv[2] if len(sys.argv) > 2 else 'index.html'
WEEK = 'Week of ' + batch['range'].split(' to ')[0].replace('Mon ', '')
LEDE = batch.get('lede', 'Every post planned for the week, in US Eastern time, because that is where most buyers are. Tap a thumbnail to open the full video or image.')
e = html.escape
posts = batch['posts']
days = []
for p in posts:
    if not days or days[-1][0] != p['day_label']:
        days.append((p['day_label'], []))
    days[-1][1].append(p)

def card(p):
    i = p['n']; plat = p['channel']; cls = plat.lower()
    target = p.get('board') or p.get('link_note', '')
    cap = (('Title: ' + p['title'] + '\n\n') if plat == 'Pinterest' else '') + p['caption']
    tag = (p['attribution_campaign'] + ' / ' + plat + (' (pin link)' if plat == 'Pinterest' else ' (bio link)')) if p.get('attribution_tag_url') else p.get('link_note', '')
    slides = ''
    if len(p['media_urls']) > 1:
        slides = '<div class="slides">' + ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="Open slide {k} of post {i}"><img src="thumbs/{p["thumb"][:-4]}_{k-1}.jpg" alt="Slide {k}" width="150" loading="lazy"></a>' for k, u in enumerate(p['media_urls'], 1)) + '</div>'
    return f'''<article class="post">
  <a class="thumb" href="{p['media_urls'][0]}" target="_blank" rel="noopener" aria-label="Open the media for post {i}"><img src="thumbs/{p['thumb']}" alt="" width="300" loading="lazy"></a>
  <div class="body">
    <div class="meta">
      <span class="num">#{i}</span>
      <span class="chip {cls}">{plat}</span>
      <span class="fmt">{e(p['format'])}</span>
      <span class="when"><b>{p['time_et']} ET</b> <span class="bucharest">{p['time_bucharest']} Bucharest</span></span>
    </div>
    <p class="cap" id="cap{i}">{e(cap)}</p>
    {slides}
    <button class="more" type="button" aria-controls="cap{i}" aria-expanded="false">Show full caption</button>
    <dl class="facts">
      <div><dt>Book</dt><dd>{e(p['book'])}</dd></div>
      <div><dt>{'Board' if plat == 'Pinterest' else 'Where'}</dt><dd>{e(target)}</dd></div>
      <div><dt>Tracking</dt><dd>{e(tag)}</dd></div>
    </dl>
  </div>
</article>'''

sections = []
for d, items in days:
    sections.append(f'<section class="day"><h2>{d} · {len(items)} posts</h2><div class="list">' + "\n".join(card(p) for p in items) + '</div></section>')
from collections import Counter
cnt = Counter(p['channel'] for p in posts)
STATUS = batch.get('status', 'Waiting for your approval')

page = f'''<title>Lowe Books Weekly Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<style>
/* Layout: one narrow column of posts grouped by US day; thumbnail left, caption and facts right; stacks below 560px */
:root {{
  --bg: #FBF6EA; --surface: #FFFDF7; --fg: #1E1A16; --muted: #6A6155; --line: #E6DCC6;
  --accent: #D9432C; --teal: #0E6F6B; --gold: #B97C00; --tint: #F3EAD3;
  --display: "Bricolage Grotesque", "Arial Narrow", system-ui, sans-serif;
  --body: "DM Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg: #15120E; --surface: #1F1B16; --fg: #F5EFE0; --muted: #A89F8F; --line: #38312A;
    --accent: #FF7B63; --teal: #55C7BF; --gold: #F2B632; --tint: #2A241C; color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --bg: #15120E; --surface: #1F1B16; --fg: #F5EFE0; --muted: #A89F8F; --line: #38312A;
  --accent: #FF7B63; --teal: #55C7BF; --gold: #F2B632; --tint: #2A241C; color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 15px; line-height: 1.5;
  padding-block: 28px 56px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
.wrap {{ max-width: 780px; margin: 0 auto; display: grid; gap: 28px; }}
header {{ display: grid; gap: 10px; }}
.brand {{ font: 700 12px/1 var(--body); letter-spacing: .14em; text-transform: uppercase; color: var(--accent); }}
h1 {{ font: 800 clamp(30px, 6vw, 44px)/1.05 var(--display); margin: 0; text-wrap: balance; }}
.lede {{ margin: 0; color: var(--muted); max-width: 60ch; }}
.summary {{ display: flex; flex-wrap: wrap; gap: 8px 18px; font-variant-numeric: tabular-nums; padding-block: 12px; border-block: 1px solid var(--line); }}
.summary span b {{ font-weight: 700; }}
.how {{ background: var(--tint); border-radius: 10px; padding: 14px 16px; display: grid; gap: 4px; }}
.how b {{ font-family: var(--display); font-weight: 600; }}
.how p {{ margin: 0; }}
.day {{ display: grid; gap: 12px; }}
h2 {{ font: 600 13px/1 var(--body); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin: 0; display: flex; align-items: center; gap: 12px; }}
h2::after {{ content: ""; flex: 1; height: 1px; background: var(--line); }}
.list {{ display: grid; gap: 12px; }}
.post {{ display: grid; grid-template-columns: 104px minmax(0, 1fr); gap: 16px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 14px; }}
.thumb {{ display: block; align-self: start; border-radius: 8px; overflow: hidden; background: var(--tint); }}
.thumb img {{ display: block; width: 100%; height: auto; }}
.body {{ min-width: 0; display: grid; gap: 10px; align-content: start; }}
.meta {{ display: flex; flex-wrap: wrap; align-items: center; gap: 6px 10px; font-size: 13px; }}
.num {{ font: 600 13px var(--display); color: var(--muted); font-variant-numeric: tabular-nums; }}
.chip {{ font: 700 11px/1 var(--body); letter-spacing: .06em; text-transform: uppercase; padding: 5px 8px; border-radius: 999px; border: 1.5px solid currentColor; }}
.chip.pinterest {{ color: var(--accent); }}
.chip.instagram {{ color: var(--gold); }}
.chip.tiktok {{ color: var(--teal); }}
.fmt {{ color: var(--muted); }}
.when {{ margin-left: auto; font-variant-numeric: tabular-nums; text-align: right; }}
.when .bucharest {{ color: var(--muted); font-size: 12px; margin-left: 6px; }}
.slides {{ display: flex; gap: 6px; overflow-x: auto; }}
.slides img {{ display: block; width: 84px; height: auto; border-radius: 6px; border: 1px solid var(--line); }}
.cap {{ margin: 0; white-space: pre-line; overflow-wrap: anywhere; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
.cap.open {{ display: block; }}
.more {{ justify-self: start; font: 500 13px var(--body); color: var(--accent); background: none; border: 0; padding: 2px 0; cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }}
.more:focus-visible, .thumb:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.facts {{ margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 6px 16px; font-size: 13px; padding-top: 10px; border-top: 1px dashed var(--line); }}
.facts div {{ min-width: 0; }}
dt {{ color: var(--muted); font-size: 11px; letter-spacing: .08em; text-transform: uppercase; }}
dd {{ margin: 0; overflow-wrap: anywhere; }}
footer {{ color: var(--muted); font-size: 13px; display: grid; gap: 6px; }}
footer p {{ margin: 0; }}
@media (max-width: 560px) {{
  .post {{ grid-template-columns: 1fr; }}
  .thumb {{ width: 120px; }}
  .when {{ margin-left: 0; text-align: left; flex-basis: 100%; }}
}}
@media (prefers-reduced-motion: no-preference) {{ .more {{ transition: opacity .15s; }} .more:hover {{ opacity: .7; }} }}
</style>
<div class="wrap">
  <header>
    <div class="brand">Lowe Books · thelowebooks</div>
    <h1>{WEEK}: what goes out</h1>
    <p class="lede">{e(LEDE)}</p>
  </header>
  <div class="summary" role="group" aria-label="Week summary">
    <span><b>{len(posts)}</b> posts</span><span><b>{cnt["Pinterest"]}</b> Pinterest</span><span><b>{cnt["TikTok"]}</b> TikTok</span><span><b>{cnt["Instagram"]}</b> Instagram</span><span>Status: <b>{STATUS}</b></span>
  </div>
  <div class="how"><b>How to approve</b><p>Tell Claude "approve all", or list the numbers to change, for example "change #3 and drop #7". Nothing is scheduled until you approve.</p></div>
  {"".join(sections)}
  <footer>
    <p>Times: videos on TikTok and Instagram at 8 PM Eastern (5 PM Pacific), the same video as a Pinterest video pin at 9 PM, image pins at 12 PM and 4 PM, Instagram carousels at 6 PM. US clocks went back on Sun Nov 1, so Bucharest is 7 hours ahead of Eastern this week.</p>
    <p>Facebook is paused. Pinterest links carry Amazon Attribution tags so sales can be traced to each platform.</p>
  </footer>
</div>
<script>
document.querySelectorAll('.more').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var c = document.getElementById(b.getAttribute('aria-controls'));
    var open = c.classList.toggle('open');
    b.setAttribute('aria-expanded', open);
    b.textContent = open ? 'Hide full caption' : 'Show full caption';
  }});
}});
</script>
'''
open(OUT, 'w', encoding='utf-8').write(page)
print(len(page))
