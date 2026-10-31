"""Generate 1000x1500 Pinterest pin images for the trivia books. Usage: python make_pins.py <outdir>
Run from tools/work (needs node_modules for fonts and playwright). Questions come from the private vetted list;
this script holds only the few questions used in pins."""
import sys, os, html
from playwright.sync_api import sync_playwright

AUTHOR = 'Rann Lowe'
BOOKS = {
 'random': dict(bg='#1F6F6A', fg='#FFF5DC', acc='#F5C842', cover='covers/random.jpg', cw=480, ch=720,
                title='Random Knowledge Trivia Book', badge='300 questions'),
 'memory': dict(bg='#B23A1F', fg='#FFF5DC', acc='#F5C842', cover='covers/memory.jpg', cw=600, ch=777,
                title='Memory Lane Trivia Book for Seniors', badge='500 questions · Large print'),
}
BOOKS.update({
 'couples': dict(bg='#1E1A16', fg='#FFF5DC', acc='#F5C842', title='300 Questions Couples Should Ask'),
 'parents': dict(bg='#1F6F6A', fg='#FFF5DC', acc='#F5C842', title='300 Questions to Ask Your Parents'),
 'aboutme': dict(bg='#B23A1F', fg='#FFF5DC', acc='#F5C842', title='300 Questions About Me'),
 'mazes': dict(bg='#F5C842', fg='#1E1A16', acc='#B23A1F', onacc='#FFF5DC', title='Easy Maze Puzzle Book for Seniors'),
})
CSS = """
@import url('base.css');
body{background:var(--bg)}
.frame{width:1000px;height:1500px;background:var(--bg);color:var(--fg);padding:84px 80px 78px;display:flex;flex-direction:column}
.top{font-size:26px;color:var(--fg)}
.card .clabel{font-size:24px;color:var(--bg);margin-bottom:22px}
.card.hook .display{font-size:66px}
h1.big{font-size:122px}
h1{margin:34px 0 0;font-size:100px}
.card{margin-top:44px;padding:54px 52px;transform:rotate(-1.2deg)}
.card .display{font-size:58px;line-height:1.1}
.card.list .display{font-size:40px;line-height:1.18}
ol{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:20px}
ol li{display:flex;gap:22px;align-items:flex-start;font-family:'Bricolage',sans-serif;font-weight:700;font-size:40px;line-height:1.14;letter-spacing:-0.01em}
ol li b{flex:0 0 58px;height:58px;border-radius:50%;background:var(--acc);color:var(--onacc);display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:800}
.opts{display:flex;flex-direction:column;gap:18px;margin-top:40px}
.opt{display:flex;align-items:center;gap:24px;background:var(--fg);color:var(--bg);border-radius:28px;padding:20px 30px;font-size:40px;font-weight:700}
.opt b{flex:0 0 60px;height:60px;border-radius:50%;background:var(--acc);color:var(--onacc);display:flex;align-items:center;justify-content:center;font-family:'Bricolage',sans-serif;font-weight:800;font-size:36px}
.spacer{flex:1}
.hint{font-size:26px;color:var(--acc);margin-top:30px;margin-bottom:26px}
.foot{display:flex;flex-direction:column;gap:6px}
.foot .from{font-size:28px;font-weight:500}
.foot .title{font-size:42px}
.foot .by{font-size:28px;font-weight:500;opacity:.9}
.foot .tag{font-size:28px;font-weight:700;color:var(--acc);margin-top:14px}
.coverwrap{display:flex;justify-content:center;margin-top:50px}
.coverwrap img{box-shadow:0 30px 60px rgba(0,0,0,.4);border-radius:6px;transform:rotate(3deg)}
.badge{position:absolute;right:70px;top:700px;background:var(--acc);color:#1E1A16;border-radius:999px;padding:18px 32px;font-size:30px;transform:rotate(-8deg);font-family:'Bricolage',sans-serif;font-weight:800}
"""
def foot(b, lead):
    return f"""<div class="foot"><div class="from">{lead}</div><div class="title display">{html.escape(b['title'])}</div><div class="by">by {AUTHOR}</div><div class="tag">Get curious. Scroll less.</div></div>"""

def page(b, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}:root{{--bg:{b['bg']};--fg:{b['fg']};--acc:{b['acc']};--onacc:{b.get('onacc','#1E1A16')}}}</style></head><body>{body}<script src="anim.js"></script><script>function render(t){{}}</script></body></html>"""

def cover_pin(key, headline):
    b = BOOKS[key]
    body = f"""<div class="frame"><div class="top label">Lowe Books</div><h1 class="display">{headline}</h1>
<div class="coverwrap"><img src="{b['cover']}" width="{b['cw']}" height="{b['ch']}"></div><div class="spacer"></div>
<div class="foot"><div class="by">by {AUTHOR}</div><div class="tag">Get curious. Scroll less.</div></div></div>"""
    return page(b, body)

def hook_pin(key, headline, label, q, lead):
    b = BOOKS[key]
    body = f"""<div class="frame"><div class="top label">Lowe Books</div><div class="spacer"></div><h1 class="display big">{headline}</h1>
<div class="card hook" style="margin-top:56px"><div class="clabel label">{label}</div><div class="display">{html.escape(q)}</div></div><div class="spacer"></div>
{foot(b, lead)}</div>"""
    return page(b, body)

def mc_pin(key, headline, q, opts):
    b = BOOKS[key]
    o = ''.join(f'<div class="opt"><b>{l}</b><span>{html.escape(t)}</span></div>' for l, t in zip('ABCD', opts))
    body = f"""<div class="frame"><div class="top label">Lowe Books</div><h1 class="display">{headline}</h1>
<div class="card"><div class="display">{html.escape(q)}</div></div><div class="opts">{o}</div><div class="hint label">Answer in the description</div>
<div class="spacer"></div>{foot(b, 'One of 300 questions in')}</div>"""
    return page(b, body)

def list_pin(key, headline, items, lead):
    b = BOOKS[key]
    li = ''.join(f'<li><b>{i}</b><span>{html.escape(t)}</span></li>' for i, t in enumerate(items, 1))
    body = f"""<div class="frame"><div class="top label">Lowe Books</div><h1 class="display">{headline}</h1>
<div class="card list"><ol>{li}</ol></div><div class="hint label">Answers in the description</div>
<div class="spacer"></div>{foot(b, lead)}</div>"""
    return page(b, body)

def qlist_pin(key, headline, items, lead, hint='Pick one tonight'):
    """Numbered list of real book questions; no answers (not a quiz)."""
    b = BOOKS[key]
    li = ''.join(f'<li><b>{i}</b><span>{html.escape(t)}</span></li>' for i, t in enumerate(items, 1))
    body = f"""<style>ol{{gap:16px}}ol li{{font-size:35px}}ol li b{{flex:0 0 52px;height:52px;font-size:28px}}</style><div class="frame"><div class="top label">Lowe Books</div><h1 class="display">{headline}</h1>
<div class="card list" style="padding:44px 48px"><ol>{li}</ol></div><div class="hint label">{hint}</div>
<div class="spacer"></div>{foot(b, lead)}</div>"""
    return page(b, body)

def note_pin(key, headline, label, text, lead):
    """Hook pin whose card holds a short line of copy instead of a question (gift pins)."""
    return hook_pin(key, headline, label, text, lead)

def maze_pin(key, headline, label, img, lead):
    b = BOOKS[key]
    body = f"""<div class="frame"><div class="top label">Lowe Books</div><h1 class="display" style="font-size:96px">{headline}</h1>
<div class="card" style="margin-top:40px;padding:36px;transform:rotate(-1deg)"><div class="clabel label" style="margin-bottom:18px;color:var(--acc)">{label}</div><img src="{img}" style="width:80%;display:block;margin:0 auto"></div>
<div class="spacer"></div>{foot(b, lead)}</div>"""
    return page(b, body)

def render_pins(pins, out):
    os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1500})
        for name, h in pins.items():
            f = f'_pin_{name}.html'; open(f, 'w').write(h)
            pg.goto('file://' + os.path.abspath(f)); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            pg.screenshot(path=f'{out}/{name}.png'); os.remove(f)
        br.close()

PINS = {
 'random_google': hook_pin('random', 'Ask this at your next game night.', 'Then watch them guess', 'What was the original name of Google?', 'One of 300 questions in'),
 'random_wombat': mc_pin('random', 'Can you guess it?', 'What unusual feature do wombat droppings have?',
     ['They are cube-shaped', 'They glow in the dark', 'They are odorless', 'They can bounce']),
 'random_ebay': mc_pin('random', 'Weird, but true.', 'What was the first-ever item sold on eBay?',
     ['A broken laser pointer', 'A vintage comic book', 'A pair of used sneakers', 'A pack of baseball cards']),
 'random_twinkie': mc_pin('random', 'No googling.', 'What was the original filling flavor of the Twinkie?',
     ['Vanilla', 'Banana', 'Chocolate', 'Lemon']),
 'memory_bonanza': hook_pin('memory', 'Ask Grandpa this at Thanksgiving.', 'Then watch him light up', 'On "Bonanza," what was the name of the Cartwright family\'s ranch?', 'One of 500 questions in'),
 'memory_tv': list_pin('memory', '5 classic TV questions.', [
     'What town does "The Andy Griffith Show" take place in?',
     'Who played the lead in "Perry Mason"?',
     'What was the name of Lucy and Ricky\'s son on "I Love Lucy"?',
     'Who played the Skipper on "Gilligan\'s Island"?',
     'What family does "The Beverly Hillbillies" follow?'], 'From 500 questions in'),
 'memory_movies': list_pin('memory', '5 classic movie questions.', [
     'Who starred in "Breakfast at Tiffany\'s" (1961)?',
     'Who directed "Psycho" (1960)?',
     'What did the Tin Man want from the Wizard?',
     'Which 1975 film about a shark became a blockbuster?',
     'In 1985, which film sent Michael J. Fox back in time?'], 'From 500 questions in'),
 'memory_music': list_pin('memory', '5 music questions.', [
     'Who is known as the "King of Rock and Roll"?',
     'Who sang the 1967 hit "Respect"?',
     'Which festival took place in August 1969 in Bethel, New York?',
     'Which band made "Dark Side of the Moon"?',
     'Who performed "Sweet Caroline"?'], 'From 500 questions in'),
}

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1500})
        for name, h in PINS.items():
            f = f'_pin_{name}.html'; open(f, 'w').write(h)
            pg.goto('file://' + os.path.abspath(f)); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            pg.screenshot(path=f'{out}/{name}.png'); os.remove(f)
        br.close()
