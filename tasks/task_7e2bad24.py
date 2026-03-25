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


def generate(rows=None, cols=None, lengths=None, colors=None, prow=None,
             pcol=None, shown=None, flip=None, flop=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the lines.
    cols: The columns of the lines.
    lengths: The lengths of the lines.
    colors: The colors of the lines.
    prow: The row of the pixel.
    pcol: The column of the pixel.
    shown: How much of the line is shown.
    flip: Whether to flip the grid.
    flop: Whether to flop the grid.
    xpose: Whether to transpose the grid.
  """

  def draw():
    grid, output = common.grids(16, 16)
    for row, col, length, color in zip(rows, cols, lengths, colors):
      for c in range(col, col + length):
        if grid[row][c] != 0: return None, None
        if common.get_pixel(grid, row - 1, c) not in [-1, 0]: return None, None
        if common.get_pixel(grid, row + 1, c) not in [-1, 0]: return None, None
        output[row][c] = grid[row][c] = color
    r, c, rdir, i, touches = prow, pcol, 1, 0, 0
    while c < 16 and r >= 0 and r < 16:
      if output[r][c] != 0: touches += 1
      output[r][c] = 1
      if i < shown:
        if grid[r][c] != 0: return None, None
        grid[r][c] = 1
      if r + rdir < 0 or r + rdir >= 16: break
      if grid[r + rdir][c] == 2: touches, rdir = touches + 1, rdir * -1
      r, c, i = r + rdir, c + 1, i + 1
    if i < 13 or touches == 0: return None, None
    if flip: grid, output = common.flip(grid), common.flip(output)
    if flop: grid, output = common.flop(grid), common.flop(output)
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if rows is None:
    while True:
      rows, cols, lengths, colors = [], [], [], []
      for color in [2, 3]:
        row = common.randint(0, 4)
        while row < 16:
          rows.append(row)
          lengths.append(common.randint(4, 14))
          cols.append(common.randint(1, 15 - lengths[-1]))
          colors.append(color)
          row += common.randint(3, 5)
      if common.randint(0, 1): prow, pcol = 0, common.randint(0, 6)
      else: prow, pcol = common.randint(0, 6), 0
      shown = common.randint(3, 6)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[6, 10], cols=[1, 4], lengths=[9, 9], colors=[3, 2], prow=0,
               pcol=1, shown=4, flip=True, flop=True, xpose=False),
      generate(rows=[7], cols=[1], lengths=[14], colors=[3], prow=0, pcol=1,
               shown=5, flip=True, flop=False, xpose=True),
      generate(rows=[8], cols=[2], lengths=[12], colors=[2], prow=0, pcol=0,
               shown=6, flip=False, flop=False, xpose=True),
  ]
  test = [
      generate(rows=[0, 4, 4, 7, 8, 10, 13], cols=[3, 1, 5, 9, 5, 5, 2],
               lengths=[9, 4, 9, 6, 4, 7, 6], colors=[2, 3, 2, 2, 3, 2, 3],
               prow=1, pcol=0, shown=3, flip=False, flop=False, xpose=True),
      generate(rows=[1, 5, 11], cols=[11, 6, 1],
               lengths=[4, 7, 14], colors=[2, 3, 2],
               prow=6, pcol=0, shown=3, flip=True, flop=False, xpose=True),
  ]
  return {"train": train, "test": test}
