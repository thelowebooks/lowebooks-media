import re, sys, json
lines = [l.strip() for l in open(sys.argv[1]).read().splitlines() if l.strip()]
head_re = re.compile(r'^(\d{1,3})\.\s+(.+)$')
blocks, cur = [], None
for l in lines:
    if re.fullmatch(r'\d{1,3}', l):  # page numbers
        continue
    m = head_re.match(l)
    if m:
        n, rest = int(m.group(1)), m.group(2)
        if cur and cur['mode'] in ('title','ans') and n == len(cur['ans'])+1 and n <= 5 and (cur['mode']=='ans' or n==1):
            cur['ans'].append(rest); cur['mode'] = 'ans'; continue
        cur = {'n': n, 'title': rest, 'ans': [], 'mode': 'title'}
        blocks.append(cur); continue
    if cur is None: continue
    if cur['mode'] == 'title':
        cur['title'] += ' ' + l   # either title wrap or (for question blocks) options; harmless
    elif cur['mode'] == 'ans' and len(cur['ans']) < 6:
        cur['ans'][-1] += ' ' + l
out = {}
for b in blocks:
    if len(b['ans']) >= 4:
        out[b['n']] = b
def val(e):
    e2 = re.sub(r'\([^)]*\)', '', e)
    m = re.search(r'(?:~|–|-|—)\s*\$?([\d][\d.,]*)', e2)
    if not m: return None
    s = m.group(1).replace(',', '').rstrip('.')
    try: return float(s)
    except: return None
res = []
for n in sorted(out):
    b = out[n]
    ans = [a.strip() for a in b['ans'][:5]]
    vals = [val(a) for a in ans]
    nums = [v for v in vals if v is not None]
    order = None
    if len(nums) == len(ans) and len(nums) >= 4:
        if all(nums[k] >= nums[k+1] for k in range(len(nums)-1)): order = 'desc'
        elif all(nums[k] <= nums[k+1] for k in range(len(nums)-1)): order = 'asc'
        else: order = 'BROKEN'
    title = b['title']
    # trim question-block option leakage: answer blocks' titles shouldn't include options
    res.append({'n': n, 'title': title, 'answers': ans, 'values': vals, 'order': order, 'count': len(b['ans'])})
json.dump(res, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
print(len(res), 'answer blocks found')
for r in res:
    flag = '' if r['order'] in ('desc','asc') else ('  <-- ' + str(r['order']))
    if r['count'] != 5: flag += f'  <-- {r["count"]} answers'
    print(f"{r['n']:>3}. {r['title'][:75]}{flag}")
    print('      ' + ' | '.join(r['answers']))
