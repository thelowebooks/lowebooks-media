"""Build maze video assets from the solution images in the maze book PDF.
usage: python maze_pool.py <book.pdf> <outdir> <maze ids...>
Maze ids are 1-100 in book order: 1-25 rectangle, 26-50 circle, 51-75 square, 76-100 hexagon.
For each id writes <outdir>/<shape>-<nn>/: maze_ink.png (maze with a green start dot and a red exit dot, no path),
path_000.png ... path_060.png (transparent overlays drawing the solution), meta.json.
The PDF holds one solution image per maze in book order after each section's 25 puzzle images.
The PDF itself is the book interior: never commit it.
"""
import sys, os, json, subprocess, tempfile, glob
from collections import deque
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

SHAPES = ['rectangle', 'circle', 'square', 'hexagon']
CORAL, GREEN = (232, 85, 58), (46, 158, 91)

def solution_image(pdf, mid, tmp):
    sec, k = divmod(mid - 1, 25)
    idx = sec * 50 + 25 + k
    files = sorted(glob.glob(f'{tmp}/i-*.png'))
    if not files:
        subprocess.run(['pdfimages', '-png', pdf, f'{tmp}/i'], check=True)
        files = sorted(glob.glob(f'{tmp}/i-*.png'))
    return SHAPES[sec], k + 1, Image.open(files[idx]).convert('L')

def build(img, out):
    a = np.array(img).astype(np.int32)
    ys0, xs0 = np.where(a < 200)
    p = 44
    a = np.pad(a, p, constant_values=255)[ys0.min():ys0.max() + 2 * p + 1, xs0.min():xs0.max() + 2 * p + 1]
    core = (a >= 80) & (a <= 150)
    core = ndimage.binary_opening(core, structure=np.ones((3, 3)))
    lab, n = ndimage.label(core)
    sizes = ndimage.sum(core, lab, range(1, n + 1))
    keep = lab == (1 + int(np.argmax(sizes)))
    # maze without the path
    maze = a.copy()
    maze[ndimage.binary_dilation(keep, iterations=3) & (a > 40)] = 255
    # order path pixels by geodesic distance from the topmost (then leftmost) pixel
    ys, xs = np.where(keep)
    s = np.lexsort((xs, ys))[0]
    dist = np.full(keep.shape, -1, np.int32)
    dq = deque([(ys[s], xs[s])]); dist[ys[s], xs[s]] = 0
    h, w = keep.shape
    while dq:
        y, x = dq.popleft()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and keep[ny, nx] and dist[ny, nx] < 0:
                    dist[ny, nx] = dist[y, x] + 1; dq.append((ny, nx))
    reach = dist >= 0
    idx = ndimage.distance_transform_edt(~reach, return_distances=False, return_indices=True)
    dfull = dist[idx[0], idx[1]]
    draw = ndimage.binary_dilation(keep, iterations=3)
    end = np.unravel_index(np.argmax(dist), dist.shape)
    start = (ys[s], xs[s])
    # ink image with start and exit dots
    # transparent background: ink alpha follows darkness, so the maze sits on any card colour
    alpha = (255 - np.clip(maze, 0, 255)).astype(np.uint8)
    rgba = np.zeros((h, w, 4), np.uint8); rgba[..., 3] = alpha; rgba[..., :3] = 30
    rgb = Image.fromarray(rgba, 'RGBA')
    d = ImageDraw.Draw(rgb); r = max(10, w // 45)
    for (cy, cx), col in ((start, GREEN), (end, CORAL)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    os.makedirs(out, exist_ok=True)
    rgb.save(f'{out}/maze_ink.png')
    mx = dist.max()
    for i in range(61):
        m = draw & (dfull <= mx * i / 60) & (dfull >= 0) if i else np.zeros_like(draw)
        rgba = np.zeros((h, w, 4), np.uint8); rgba[m] = (*CORAL, 255)
        Image.fromarray(rgba, 'RGBA').save(f'{out}/path_{i:03d}.png', optimize=True)
    return {'w': w, 'h': h, 'reached': int(reach.sum()), 'path_px': int(keep.sum()),
            'start': [int(start[1]), int(start[0])], 'end': [int(end[1]), int(end[0])]}

if __name__ == '__main__':
    pdf, outdir, ids = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]]
    tmp = tempfile.mkdtemp()
    for mid in ids:
        shape, num, img = solution_image(pdf, mid, tmp)
        name = f'{shape}-{num:02d}'
        meta = build(img, f'{outdir}/{name}')
        meta.update(id=mid, shape=shape, number=num)
        json.dump(meta, open(f'{outdir}/{name}/meta.json', 'w'))
        print(name, meta)
