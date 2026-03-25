# Copyright 2026 Google LLC
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


def generate(width=None, height=None, prow=None, pcol=None, pcolor=None,
             rows=None, cols=None, colors=None, flip=None, flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    prow: The row of the plus.
    pcol: The column of the plus.
    pcolor: The color of the plus.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
    flip: Whether to flip the grid.
    flop: Whether to flop the grid.
  """

  if width is None:
    width, height = common.randint(7, 21), common.randint(7, 21)
    prow, pcol = common.randint(3, height - 4), common.randint(3, width - 4)
    pcolor = common.random_color(exclude=[7])
    subset = list(range(0, 10))
    subset.remove(7)
    subset.remove(pcolor)
    while True:
      rows, cols, colors = [], [], []
      for r in range(prow):
        for c in range(pcol):
          if common.randint(0, 2): continue
          cols, rows = cols + [c], rows + [r]
          colors.append(common.choice(subset))
      if rows and cols: break
    flip, flop = False, common.randint(0, 1)

  grid, output = common.grids(width, height, 7)
  for r in range(height):
    output[r][pcol] = grid[r][pcol] = pcolor
  for c in range(width):
    output[prow][c] = grid[prow][c] = pcolor
  for row, col, color in zip(rows, cols, colors):
    output[row][col] = grid[row][col] = color
    common.draw(output, row, pcol + (pcol - col), color)
    common.draw(output, prow + (prow - row), col, color)
    common.draw(output, prow + (prow - row), pcol + (pcol - col), color)
  if flip: grid, output = common.flip(grid), common.flip(output)
  if flop: grid, output = common.flop(grid), common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=10, prow=4, pcol=6, pcolor=1,
               rows=[0, 0, 1, 1, 2, 3, 3], cols=[1, 4, 2, 4, 5, 0, 3],
               colors=[9, 2, 9, 4, 3, 5, 4], flip=False, flop=True),
      generate(width=11, height=11, prow=5, pcol=4, pcolor=6,
               rows=[0, 1, 1, 2, 2, 3, 4], cols=[0, 0, 1, 0, 1, 1, 1],
               colors=[1, 2, 2, 0, 4, 4, 8], flip=False, flop=False),
      generate(width=8, height=8, prow=4, pcol=4, pcolor=3,
               rows=[0, 0, 0, 1, 2, 2, 2], cols=[0, 2, 3, 1, 0, 2, 3],
               colors=[1, 0, 8, 6, 0, 2, 0], flip=False, flop=True),
  ]
  test = [
      generate(width=17, height=11, prow=6, pcol=6, pcolor=4,
               rows=[0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5],
               cols=[3, 3, 5, 0, 2, 0, 5, 1, 3, 4, 0, 3],
               colors=[9, 9, 0, 6, 0, 8, 5, 9, 8, 3, 6, 2],
               flip=False, flop=False),
  ]
  return {"train": train, "test": test}
