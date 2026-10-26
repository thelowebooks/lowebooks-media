import re, sys
t = open(sys.argv[1]).read().replace('’',"'")
lines=[l.strip() for l in t.splitlines()]
qs=[];cur=None
for l in lines:
    m=re.match(r'^(\d{1,3})\.\s+(.*)',l)
    if m:
        if cur: qs.append(cur)
        cur=m.group(2)
    elif cur is not None and l and not re.fullmatch(r'\d+',l):
        if cur.rstrip().endswith(('?','.')): qs.append(cur); cur=None
        else: cur+=' '+l
if cur: qs.append(cur)
for i,q in enumerate(qs): print(i, q)
