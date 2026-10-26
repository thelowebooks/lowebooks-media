# Lowe Books media

Public media host for the Lowe Books social accounts (thelowebooks). Buffer reads the images and videos from the GitHub Pages address of this repository:
https://thelowebooks.github.io/lowebooks-media/

- `YYYY-wNN/` weekly media (pins, carousels, videos)
- `tools/work/` HTML templates and `base.css`/`anim.js` (brand look)
- `tools/scripts/render.py` renders templates to PNG or MP4 (needs Playwright, ffmpeg, `npm install` inside `tools/work`)
- `tools/maze/assets/` maze image and solution frames used by the maze video
- `tools/review/build.py` builds the weekly review page
- `data/attribution_tags.csv` Amazon Attribution links per book and platform
