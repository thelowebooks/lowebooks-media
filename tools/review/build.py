import html, json, sys

BASE = "https://thelowebooks.github.io/lowebooks-media/2026-w44/"
WEEK = "Week of Oct 26"

# (day label ET, time ET, time Bucharest, platform, format, board/target, thumb, media file, caption, book, tag)
P = [
 ("Tue Oct 27", "8:00 PM", "Wed 02:00", "TikTok", "Video 12s", "Personal account", "couples.jpg", "video-couples.mp4",
  "Ask your partner this tonight 👀 What first attracted you to me, and has that changed over time? #couplesquestions #datenight #relationshipquestions #booktok #deepconversations",
  "Couples", "Link in bio (TikTok link later)"),
 ("Tue Oct 27", "8:00 PM", "Wed 02:00", "Instagram", "Reel 12s", "Shares to Facebook", "couples.jpg", "video-couples.mp4",
  "Ask your partner this tonight 👀\n\n\"What first attracted you to me, and has that changed over time?\"\n\n297 more in 300 Questions Couples Should Ask by Rann Lowe. Link in bio.\n\nGet curious. Scroll less.\n\n#couplesquestions #datenightideas #relationshipquestions #deepconversations #questionsforcouples #dateathome",
  "Couples", "Link in bio, tag LB-Couples / Instagram"),
 ("Tue Oct 27", "9:00 PM", "Wed 03:00", "Pinterest", "Pin 1000×1500", "Questions to Ask Your Parents", "pin-parents.jpg", "pin-parents.png",
  "Questions to ask your parents before the holidays are over. One question, a good listen, and a conversation you'll remember. This is 1 of 300 conversation starters in 300 Questions to Ask Your Parents, a great gift idea for Christmas, Mother's Day or birthdays. Get it on Amazon.",
  "Parents", "Amazon link, tag LB-Parents / Pinterest"),
 ("Wed Oct 28", "8:00 PM", "Thu 02:00", "Instagram", "Carousel 5 slides", "Shares to Facebook", "carousel.jpg", "carousel_couples_0.png",
  "3 questions to ask your partner tonight. Swipe, and don't skip the third one. 💬\n\nWhich one are you asking first? Tell us below 👇\n\n297 more in 300 Questions Couples Should Ask by Rann Lowe. Link in bio.\n\nGet curious. Scroll less.\n\n#couplesquestions #datenightideas #relationshipgoals #questionsforcouples #deepconversations #couplegoals #dateathome #conversationstarters",
  "Couples", "Link in bio, tag LB-Couples / Instagram"),
 ("Wed Oct 28", "9:00 PM", "Thu 03:00", "Pinterest", "Video pin 12s", "Date Night Ideas at Home", "couples.jpg", "video-couples.mp4",
  "Date night ideas at home: ask your partner this tonight. One question can start the best conversation of the week. Find 300 couples questions in 300 Questions Couples Should Ask, a thoughtful gift idea for anniversaries and Valentine's Day. Get it on Amazon.",
  "Couples", "Amazon link, tag LB-Couples / Pinterest"),
 ("Thu Oct 29", "8:00 PM", "Fri 02:00", "TikTok", "Video 21s", "Personal account", "aboutme.jpg", "video-aboutme.mp4",
  "3 questions. 5 seconds each. No overthinking ⏱️ Which one got you? Drop your answers below 👇 #getcurious #icebreakerquestions #questionsaboutme #conversationstarters #funquestions",
  "About Me", "Link in bio (TikTok link later)"),
 ("Thu Oct 29", "8:00 PM", "Fri 02:00", "Instagram", "Reel 21s", "Shares to Facebook", "aboutme.jpg", "video-aboutme.mp4",
  "Answer in 5 seconds. Don't overthink it. ⏱️\n\nWhich one got you? Drop your answers in the comments 👇\n\n300 more like these in 300 Questions About Me by Rann Lowe. Link in bio.\n\nGet curious. Scroll less.\n\n#icebreakerquestions #questionsaboutme #conversationstarters #funquestions #selfdiscovery #getcurious",
  "About Me", "Link in bio, tag LB-AboutMe / Instagram"),
 ("Thu Oct 29", "9:00 PM", "Fri 03:00", "Pinterest", "Video pin 25s", "Activities for Seniors", "maze.jpg", "video-maze.mp4",
  "Large print maze puzzles for seniors: can you solve this one in 15 seconds? A relaxing brain exercise and a thoughtful gift idea for grandparents. 100 easy mazes with solutions in Easy Maze Puzzle Book for Seniors. Get it on Amazon.",
  "Mazes", "Amazon link, tag LB-Mazes / Pinterest"),
 ("Fri Oct 30", "8:00 PM", "Sat 02:00", "TikTok", "Video 25s", "Personal account", "maze.jpg", "video-maze.mp4",
  "Can you beat this maze in 15 seconds? ⏱️ Start at the top, exit at the bottom. Pause if you need more time 😅 #mazepuzzle #puzzlebook #brainteaser #seniorsactivities #largeprint #puzzlesoftiktok",
  "Mazes", "Link in bio (TikTok link later)"),
 ("Fri Oct 30", "8:00 PM", "Sat 02:00", "Instagram", "Reel 25s", "Shares to Facebook", "maze.jpg", "video-maze.mp4",
  "Beat this maze in 15 seconds ⏱️\n\nStart at the top. Exit at the bottom. Pause it if you need more time.\n\n100 large-print mazes with solutions in Easy Maze Puzzle Book for Seniors by Rann Lowe. Link in bio.\n\nGet curious. Scroll less.\n\n#mazepuzzle #puzzlebook #brainteaser #seniorsactivities #largeprint #brainexercise",
  "Mazes", "Link in bio, tag LB-Mazes / Instagram"),
 ("Sun Nov 1", "8:00 PM", "Mon 03:00", "Pinterest", "Video pin 21s", "Questions to Ask Yourself", "aboutme.jpg", "video-aboutme.mp4",
  "Questions to ask yourself: answer these 3 in 5 seconds each, no overthinking. Fun self-discovery questions, icebreakers and journal prompts. 300 more in 300 Questions About Me, a great gift for anyone who loves a good conversation. Get it on Amazon.",
  "About Me", "Amazon link, tag LB-AboutMe / Pinterest"),
]

e = html.escape
days = []
for i, p in enumerate(P, 1):
    if not days or days[-1][0] != p[0]:
        days.append((p[0], []))
    days[-1][1].append((i, p))

def card(i, p):
    day, t, tb, plat, fmt, target, thumb, media, cap, book, tag = p
    cls = plat.lower()
    return f'''<article class="post">
  <a class="thumb" href="{BASE}{media}" target="_blank" rel="noopener" aria-label="Open the media for post {i}"><img src="thumbs/{thumb}" alt="" width="300" loading="lazy"></a>
  <div class="body">
    <div class="meta">
      <span class="num">#{i}</span>
      <span class="chip {cls}">{plat}</span>
      <span class="fmt">{e(fmt)}</span>
      <span class="when"><b>{t} ET</b> <span class="bucharest">{tb} Bucharest</span></span>
    </div>
    <p class="cap" id="cap{i}">{e(cap)}</p>
    <button class="more" type="button" aria-controls="cap{i}" aria-expanded="false">Show full caption</button>
    <dl class="facts">
      <div><dt>Book</dt><dd>{e(book)}</dd></div>
      <div><dt>{'Board' if plat == 'Pinterest' else 'Where'}</dt><dd>{e(target)}</dd></div>
      <div><dt>Tracking</dt><dd>{e(tag)}</dd></div>
    </dl>
  </div>
</article>'''

sections = []
for d, items in days:
    sections.append(f'<section class="day"><h2>{d}</h2><div class="list">' + "\n".join(card(i, p) for i, p in items) + '</div></section>')

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
    <p class="lede">Every post in the queue, in US Eastern time, because that is where most buyers are. Tap a thumbnail to open the full video or image.</p>
  </header>
  <div class="summary" role="group" aria-label="Week summary">
    <span><b>11</b> posts</span><span><b>4</b> Pinterest</span><span><b>3</b> TikTok</span><span><b>4</b> Instagram</span><span>Status: <b>Scheduled in Buffer</b></span>
  </div>
  <div class="how"><b>How to approve</b><p>Tell Claude "approve all", or list the numbers to change, for example "change #3 and drop #7". Nothing is posted that you have not seen here.</p></div>
  {"".join(sections)}
  <footer>
    <p>Times: TikTok and Instagram at 8 PM Eastern (5 PM Pacific), Pinterest at 9 PM Eastern. US clocks go back on Sun Nov 1, so Bucharest times shift by one hour afterwards.</p>
    <p>Facebook receives the Instagram posts through auto-share. Pinterest links carry Amazon Attribution tags so sales can be traced to each platform.</p>
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
open('index.html', 'w', encoding='utf-8').write(page)
print(len(page))
