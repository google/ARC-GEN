# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generator."""

import common


def generate(width=None, height=None, boxwidth=None, boxheight=None, row=None,
             col=None, rows=None, cols=None, boxcolor=None, dotcolor=None,
             b=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    boxwidth: the width of the box
    boxheight: the height of the box
    row: the row of the box
    col: the column of the box
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    boxcolor: the color of the box
    dotcolor: the color of the dots
    b: the integer used for all background cells
  """
  if width is None:
    width, height = common.randint(8, 24), common.randint(8, 24)
    boxwidth = common.randint(3, width // 2)
    boxheight = common.randint(3, height // 2)
    row = common.randint(1, height - boxheight - 2)
    col = common.randint(1, width - boxwidth - 2)
    pixels, rows, cols = common.random_pixels(width, height, 0.02), [], []
    for r, c in pixels:
      if r + 1 >= row and r <= row + boxheight:
        if c + 1 >= col and c <= col + boxwidth:
          continue
      rows.append(r)
      cols.append(c)
    colors = common.random_colors(3)
    boxcolor, dotcolor, b = colors[0], colors[1], colors[2]

  grid, output = common.grids(width, height, b)
  for r in range(row, row + boxheight):
    for c in range(col, col + boxwidth):
      output[r][c] = grid[r][c] = boxcolor
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = dotcolor
    rdiff, cdiff = 0, 0
    rdiff = rdiff if r >= row else 1
    rdiff = rdiff if r < row + boxheight else -1
    cdiff = cdiff if c >= col else 1
    cdiff = cdiff if c < col + boxwidth else -1
    if rdiff != 0 and cdiff != 0: continue
    while output[r + rdiff][c + cdiff] != boxcolor:
      output[r + rdiff][c + cdiff] = dotcolor
      r, c = r + rdiff, c + cdiff
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=9, boxwidth=3, boxheight=4, row=1, col=2,
               rows=[3, 7], cols=[9, 7], boxcolor=3, dotcolor=4, b=8),
      generate(width=12, height=10, boxwidth=3, boxheight=3, row=2, col=3,
               rows=[8], cols=[3], boxcolor=1, dotcolor=8, b=2),
      generate(width=12, height=14, boxwidth=4, boxheight=4, row=4, col=3,
               rows=[0, 6, 11], cols=[4, 10, 1], boxcolor=4, dotcolor=2, b=1),
      generate(width=18, height=14, boxwidth=5, boxheight=4, row=5, col=7,
               rows=[1, 3, 4, 5, 11], cols=[8, 11, 15, 2, 13], boxcolor=5,
               dotcolor=4, b=1),
  ]
  test = [
      generate(width=21, height=19, boxwidth=8, boxheight=6, row=5, col=7,
               rows=[1, 2, 2, 3, 7, 9, 13, 17, 17],
               cols=[9, 2, 17, 13, 19, 2, 15, 3, 11], boxcolor=8, dotcolor=1,
               b=2),
  ]
  return {"train": train, "test": test}
