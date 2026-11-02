# Lowe Books media

Public media host for the Lowe Books social accounts (thelowebooks). Buffer reads the images and videos from the GitHub Pages address of this repository:
https://thelowebooks.github.io/lowebooks-media/

- `YYYY-wNN/` weekly media (pins, carousels, videos)
- `tools/work/` HTML templates and `base.css`/`anim.js` (brand look)
- `tools/scripts/render.py` renders templates to PNG or MP4 (needs Playwright, ffmpeg, `npm install` inside `tools/work`)
- `tools/maze/assets/` maze image and solution frames used by the maze video
- `tools/review/build.py` builds the weekly review page
- `data/attribution_tags.csv` Amazon Attribution links per book and platform

## Mazes
- `tools/maze/pool/<shape>-<nn>/` 24 mazes from Easy Maze Puzzle Book for Seniors (6 each: rectangle, circle, square, hexagon), built with `tools/scripts/maze_pool.py` from the book interior PDF (the PDF is never committed).
- `tools/work/make_maze.py video ../maze/pool/<name> out.html` makes a 16 s maze video (opens on the maze, 10 s countdown, solution reveal, book card); `make_maze.py pin ...` makes a 1000x1500 maze pin.
- Each maze is used once: check `batches/*.json` for maze names already used. When fewer than 6 unused remain, ask Rares for the PDF to build more.
