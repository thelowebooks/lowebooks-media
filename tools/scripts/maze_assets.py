import numpy as np
from PIL import Image
from scipy import ndimage
from collections import deque
import sys, os
src, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
im = np.array(Image.open(src).convert('L')).astype(np.int32)
H, W = im.shape
# crop maze #1: top-left quadrant; find bounding box of dark pixels below the "#1" label
q = im[:H//2, :W//2]
dark = q < 200
rows = np.where(dark.sum(1) > 0)[0]; cols = np.where(dark.sum(0) > 0)[0]
# label "#1" is at the top: skip rows until a gap after the label
r = rows
gaps = np.where(np.diff(r) > 20)[0]
start = r[gaps[0]+1] if len(gaps) else r[0]
sub = q[start:, :]
d2 = sub < 200
rr = np.where(d2.sum(1) > 0)[0]; cc = np.where(d2.sum(0) > 0)[0]
y0, x0, x1 = start+rr[0], cc[0], cc[-1]; y1 = y0 + (x1 - x0)
pad = 30
crop = im[max(0,y0-pad):y1+pad, max(0,x0-pad):x1+pad]
print('crop', crop.shape)
core = (crop >= 80) & (crop <= 130)
core = ndimage.binary_opening(core, structure=np.ones((3,3)), iterations=1)
lab, n = ndimage.label(core)
sizes = ndimage.sum(core, lab, range(1, n+1))
keep = lab == (1 + int(np.argmax(sizes)))
path = ndimage.binary_dilation(keep, iterations=3) & (crop > 40) & (crop < 252)
path = path | keep
print('path px', path.sum(), 'components kept', (sizes > 500).sum())
# maze without path
maze = crop.copy()
maze[ndimage.binary_dilation(keep, iterations=4) & (crop > 40)] = 255
Image.fromarray(maze.astype(np.uint8)).save(f'{outdir}/maze.png')
# geodesic distance from topmost path pixel
ys, xs = np.where(keep)
s = np.argmin(ys)
dist = np.full(keep.shape, -1, np.int32)
dq = deque([(ys[s], xs[s])]); dist[ys[s], xs[s]] = 0
h, w = keep.shape
while dq:
    y, x = dq.popleft()
    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
        ny, nx = y+dy, x+dx
        if 0 <= ny < h and 0 <= nx < w and keep[ny, nx] and dist[ny, nx] < 0:
            dist[ny, nx] = dist[y, x] + 1; dq.append((ny, nx))
reach = dist >= 0
print('reached', reach.sum(), 'of', keep.sum(), 'max dist', dist.max())
# distance for the dilated drawing mask: nearest core pixel's distance
idx = ndimage.distance_transform_edt(~reach, return_distances=False, return_indices=True)
dfull = dist[idx[0], idx[1]]
draw = ndimage.binary_dilation(keep, iterations=5)
np.save(f'{outdir}/dist.npy', np.where(draw, dfull, -1))
np.save(f'{outdir}/draw.npy', draw)
print('saved', crop.shape)
