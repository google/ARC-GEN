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


def generate(width=None, height=None, brow=None, bcol=None, order=None,
             flip=None, bgcolors=None, fgcolors=None, prows=None, pcols=None,
             extra_rows=None, extra_cols=None, extra_colors=None,
             extra_grids=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    brow: The row of the line.
    bcol: The column of the line.
    order: The order of the lines.
    flip: Whether to flip the grids.
    bgcolors: The background colors.
    fgcolors: The foreground colors.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    extra_rows: The rows of the extra colors.
    extra_cols: The columns of the extra colors.
    extra_colors: The extra colors.
    extra_grids: The grids of the extra colors.
  """

  def draw():
    if prows[1] - prows[0] < 2 or brow in prows: return None, None
    if pcols[1] - pcols[0] < 2 or bcol in pcols: return None, None
    if prows[1] >= brow: return None, None
    grid, output = common.grids(width, height)
    for o in [0, 1]:
      if o == order:
        for r in range(height):
          grid[r][bcol] = bgcolors[0]
      else:
        for c in range(width):
          grid[brow][c] = bgcolors[1]
    grid[prows[0]][bcol] = fgcolors[0]
    grid[prows[1]][bcol] = fgcolors[0]
    grid[brow][pcols[0]] = fgcolors[1]
    grid[brow][pcols[1]] = fgcolors[1]
    the_row = prows[0] if not flip else brow
    for row in range(prows[0], brow + 1):
      for col in range(pcols[0], pcols[1] + 1):
        if row % 2 == the_row % 2 and col % 2 == pcols[0] % 2:
          output[row][col] = fgcolors[0 if row <= prows[1] else 1]
        elif row % 2 == the_row % 2 and col % 2 != pcols[0] % 2:
          output[row][col] = bgcolors[0]
        elif row % 2 != the_row % 2 and col % 2 == pcols[0] % 2:
          output[row][col] = bgcolors[1]
        else:
          output[row][col] = bgcolors[0 if order else 1]
    if extra_colors:
      for extra_row, extra_col, extra_color, extra_grid in zip(extra_rows, extra_cols, extra_colors, extra_grids):
        g = grid if extra_grid else output
        g[extra_row][extra_col] = extra_color
    if flip: grid, output = common.flip(grid), common.flip(output)
    return grid, output

  if width is None:
    width = height = common.randint(10, 15)
    brow = common.randint(height // 2, height - 3)
    bcol = common.randint(2, width - 3)
    order, flip = common.randint(0, 1), common.randint(0, 1)
    colors = common.shuffle(list(range(1, 10)))
    bgcolors = [colors.pop(), colors.pop()]
    fgcolors = [colors.pop(), colors.pop()]
    while True:
      prows = [common.randint(1, height - 2) for _ in range(2)]
      pcols = [common.randint(1, width - 2) for _ in range(2)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=12, brow=9, bcol=2, order=0, flip=0,
               bgcolors=[4, 3], fgcolors=[2, 5], prows=[1, 6], pcols=[6, 8]),
      generate(width=10, height=10, brow=7, bcol=7, order=0, flip=1,
               bgcolors=[5, 8], fgcolors=[9, 2], prows=[1, 5], pcols=[2, 6],
               extra_rows=[5, 5], extra_cols=[3, 5], extra_colors=[8, 8],
               extra_grids=[0, 0]),
      generate(width=12, height=12, brow=9, bcol=2, order=1, flip=0,
               bgcolors=[4, 3], fgcolors=[2, 5], prows=[1, 3], pcols=[6, 8]),
      generate(width=15, height=15, brow=10, bcol=5, order=0, flip=1,
               bgcolors=[7, 1], fgcolors=[6, 3], prows=[3, 7], pcols=[3, 8]),
  ]
  test = [
      generate(width=15, height=25, brow=20, bcol=2, order=0, flip=1,
               bgcolors=[6, 5], fgcolors=[3, 2], prows=[5, 7], pcols=[5, 10],
               extra_rows=[0, 1, 2, 3, 4, 23, 24, 20],
               extra_cols=[2, 2, 2, 2, 2, 2, 2, 14],
               extra_colors=[0, 0, 0, 0, 0, 0, 0, 0],
               extra_grids=[1, 1, 1, 1, 1, 1, 1, 1]),
      generate(width=10, height=10, brow=4, bcol=5, order=0, flip=0,
               bgcolors=[9, 7], fgcolors=[8, 4], prows=[0, 3], pcols=[1, 7]),
  ]
  return {"train": train, "test": test}
