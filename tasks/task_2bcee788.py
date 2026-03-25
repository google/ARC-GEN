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


def generate(rows=None, cols=None, row=None, col=None, color=None, flip=None,
             xpose=None, size=10, minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    row: the row where the grid should be placed
    col: the column where the grid should be placed
    color: a digit representing a color to be used
    flip: whether the grid should be flipped horizontally
    xpose: whether the grid should be flipped vertically
    size: the width and height of the (square) grid
    minisize: the width and height of the sprite
  """
  if rows is None:
    rows, cols = [], []
    while True:
      bitmap, unshown = common.grid(minisize, minisize, 0), 0
      queue = [(common.randint(0, 2), 0)]  # Start with some random row
      while queue:
        r, c = queue.pop()
        if r < 0 or r >= minisize or c < 0 or c >= minisize: continue
        if bitmap[r][c] == 1: continue
        bitmap[r][c] = 1
        if c > 0: unshown += 1
        for dr, dc in [(-1, 0), (0, 1), (1, 0)]:
          if common.randint(0, 1) == 0: continue
          queue.append((r + dr, c + dc))
      if unshown == 0: continue
      for r in range(minisize):
        for c in range(minisize):
          if bitmap[r][c] == 0: continue
          rows.append(r)
          cols.append(c)
      break
    row, col = common.randint(1, 6), common.randint(4, 6)
    color = common.random_color(exclude=[common.red(), common.green()])
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid = common.grid(size, size)
  output = common.grid(size, size, common.green())
  for r, c in zip(rows, cols):
    output[row + r][col + c] = grid[row + r][col + c] = color
    grid[row + r][col - c - 1] = common.red() if c == 0 else common.black()
    output[row + r][col - c - 1] = color
  if flip: grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 1, 2], cols=[0, 0, 1, 2, 0], row=3, col=5,
               color=4, flip=1, xpose=0),
      generate(rows=[0, 1, 1, 1, 2], cols=[0, 0, 1, 2, 2], row=3, col=4,
               color=6, flip=0, xpose=1),
      generate(rows=[0, 1, 1], cols=[0, 0, 1], row=4, col=4,
               color=7, flip=0, xpose=0),
      generate(rows=[0, 1, 2, 2], cols=[1, 1, 0, 1], row=3, col=4,
               color=8, flip=1, xpose=1),
  ]
  test = [
      generate(rows=[0, 1, 1, 2], cols=[1, 0, 1, 0], row=3, col=4,
               color=1, flip=1, xpose=0),
  ]
  return {"train": train, "test": test}
