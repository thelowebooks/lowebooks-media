import re, sys
from spellchecker import SpellChecker
sp = SpellChecker()
extra = set("""dinosaur heirloom heirlooms mentor mentors tv groundhog genie superpower superpowers grandparents grandparent bucket wanderlust introspection mirthful icebreakers icebreaker camaraderie quirks quirky labyrinth labyrinths hexagonal ok okay selfie online offline podcast podcasts lifestyle playlist playlists bucketlist workplace milestones milestone teammate teammates nooks crannies pastime pastimes roadtrip whatsapp facetime""".split())
sp.word_frequency.load_words(extra)
for f in sys.argv[1:]:
    t = open(f).read().replace('’',"'")
    words = re.findall(r"[A-Za-z][A-Za-z']+", t)
    bad = {}
    for w in words:
        wl = w.lower().strip("'")
        if wl.endswith("'s"): wl = wl[:-2]
        if len(wl) < 3: continue
        if wl in sp: continue
        if sp.unknown([wl]):
            bad[wl] = bad.get(wl, 0) + 1
    print('==', f, sorted(bad.items()))
    # doubled words
    for m in re.finditer(r"\b(\w+)\s+\1\b", t, re.I):
        print('   doubled:', repr(t[max(0,m.start()-30):m.end()+20]))
