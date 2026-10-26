import re, sys, difflib
for f in sys.argv[1:]:
    t = open(f).read().replace('’',"'")
    # join wrapped lines
    lines = [l.strip() for l in t.splitlines()]
    qs, cur = [], None
    for l in lines:
        m = re.match(r'^(\d{1,3})\.\s+(.*)', l)
        if m:
            if cur: qs.append(cur)
            cur = [int(m.group(1)), m.group(2)]
        elif cur and l and not re.fullmatch(r'\d+', l) and not l.istitle():
            if not cur[1].rstrip().endswith('?'):
                cur[1] += ' ' + l
            else:
                qs.append(cur); cur = None
        elif cur and (not l):
            pass
    if cur: qs.append(cur)
    nums = [q[0] for q in qs]
    print('==', f, 'questions parsed:', len(qs))
    # numbering resets
    seqs, s = [], []
    for n in nums:
        if s and n != s[-1] + 1:
            seqs.append(s); s = []
        s.append(n)
    seqs.append(s)
    print('   numbering runs:', [(x[0], x[-1], len(x)) for x in seqs])
    noq = [q for q in qs if not q[1].strip().endswith('?')]
    for q in noq[:15]: print('   no "?":', q[0], q[1][:90])
    texts = [re.sub(r'\W+',' ', q[1].lower()).strip() for q in qs]
    for i in range(len(texts)):
        for j in range(i+1, len(texts)):
            r = difflib.SequenceMatcher(None, texts[i], texts[j]).ratio()
            if r > 0.8:
                print(f'   near-dup ({r:.2f}): [{qs[i][0]}] {qs[i][1][:80]}  ||  [{qs[j][0]}] {qs[j][1][:80]}')
